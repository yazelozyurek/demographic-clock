"""Konuşma metnini Whisper'ın kelime zamanlarıyla hizalamak için yardımcılar (gostergeler_zaman.py kullanır).

Metin slayt notlarından (<aside>) alınır, cümlelere bölünür; sayılar ve özel adlar okunuşa çevrilir. duz() hem beklenen metni
hem Whisper'ın yazdığını aynı biçime getirir (küçük harf, noktalama yok, sayılar sözle, sesteş kelimeler aynı), böylece iki
kelime dizisi difflib ile eşlenebilir. Sadece metin işler; ses üretmez.
"""
import re
import unicodedata
from pathlib import Path

SLAYT = Path(__file__).resolve().parents[2] / "sunum/slaytlar_kaynak/slides"
SAYFALAR = [("cover", "1_kapak"), ("question", "2_soru_ve_veri"), ("clock", "3_demografik_saat"),
            ("money", "4_saatle_ne_yuruyor"), ("turkiye", "5_bir_soru_daha"), ("references", "6_kapanis")]
OKUNUS = [("Stat4Sight", "Stat for Sight"), ("Kırıkkale", "Kirikkale"), ("Türkiye’s", "Turkiye's"), ("Türkiye", "Turkiye"),
          ("0.72", "zero point seven two"), ("6.06", "six point zero six"), ("8.09", "eight point zero nine"),
          ("99.98", "ninety-nine point nine eight"), ("0.77", "zero point seven seven"), ("0.44", "zero point four four"),
          ("1,100", "one thousand one hundred"), ("24,000", "twenty-four thousand"), ("1940s", "nineteen forties"),
          (r"\b363\b", "three hundred sixty-three"), (r"\b1950\b", "nineteen fifty"), (r"\b1965\b", "nineteen sixty-five"),
          (r"\b1982\b", "nineteen eighty-two"), (r"\b1990\b", "nineteen ninety"), (r"\b2023\b", "twenty twenty-three"),
          (r"\b2024\b", "twenty twenty-four"), (r"\b2047\b", "twenty forty-seven"), (r"\b2100\b", "twenty one hundred"),
          (r"\b103\b", "one hundred and three"), (r"\b115\b", "one hundred fifteen"), (r"\b125\b", "one hundred twenty-five"),
          (r"\b200\b", "two hundred"), (r"\b27\b", "twenty-seven"), (r"\b94\b", "ninety-four"), (r"\b18\b", "eighteen"),
          (r"\b14\b", "fourteen"), (r"\b26\b", "twenty-six"), (r"\b3\b", "three"),
          (r"\bUN\b", "U N"), (r"\bGDP\b", "G D P"), (r"\bSITAR\b", "sitar"), ("SuperImposition", "superimposition"),
          ("S-shaped", "S shaped"), ("S-curve", "S curve"), (r"\brho\b", "roe"), (r"\bNiger\b", "Nee-zhair"), (" — ", ", ")]
BOL = r"(?<=[.?!])\s+"
MODEL = "mlx-community/whisper-small.en-mlx"   # Whisper (mlx-whisper) modeli: sadece yazıya çevirme ve kelime zamanları


def cumleler():
    """[(sıra, dosya, paragraf_no, asıl cümle, okunuş, paragrafın son cümlesi mi)]"""
    liste, n = [], 0
    for ad, dosya in SAYFALAR:
        s = (SLAYT / f"{ad}.html").read_text(encoding="utf-8")
        metin = re.findall(r"<aside>(.*?)</aside>", s, flags=re.S)[0]
        for pi, p in enumerate([p.strip() for p in re.split(r"\n\s*\n", metin.strip()) if p.strip()]):
            okunus = p
            for eski, yeni in OKUNUS:
                okunus = re.sub(eski, yeni, okunus)
            assert not re.search(r"\d", okunus), f"sayı kaldı: {okunus}"
            asil = [c for c in re.split(BOL, p) if c.strip()]
            oku = [c for c in re.split(BOL, okunus) if c.strip()]
            assert len(asil) == len(oku), (asil, oku)
            for k, (a, o) in enumerate(zip(asil, oku)):
                n += 1
                liste.append((n, dosya, pi, a, o, k == len(asil) - 1))
    return liste


BIR = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
       "seventeen eighteen nineteen").split()
ON = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def iki(n):
    return BIR[n] if n < 20 else ON[n // 10] + ("" if n % 10 == 0 else " " + BIR[n % 10])


def uc(n):
    return iki(n) if n < 100 else BIR[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + iki(n % 100))


def soz(t):
    """Whisper'ın rakamla yazdığı sayıyı okunuşa çevirir (0.72 → zero point seven two, 2023 → twenty twenty three)."""
    if m := re.fullmatch(r"(\d+)\.(\d+)", t):
        return soz(m[1]) + " point " + " ".join(BIR[int(c)] for c in m[2])
    if m := re.fullmatch(r"(\d{4})s", t):
        s = soz(m[1])
        return s[:-1] + "ies" if s.endswith("y") else s + "s"
    if not t.isdigit():
        return t
    n = int(t)
    if 1910 <= n <= 2100 and not 2000 <= n <= 2009:
        bas, son = divmod(n, 100)
        return iki(bas) + (" hundred" if son == 0 else " " + iki(son))
    return (uc(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + uc(n % 1000))) if n >= 1000 else uc(n)


def duz(metin):
    """İki taraf da aynı biçime: küçük harf, noktalama yok, sayılar okunuşla, birbirine karışan sesteş kelimeler aynı."""
    m = unicodedata.normalize("NFKD", metin.replace("’", "'")).encode("ascii", "ignore").decode().lower()
    m = re.sub(r"(?<=\d),(?=\d{3})", "", m).replace("%", " percent")
    m = re.sub(r"\$(\d+)", r"\1 dollars", m)   # Whisper "$1,100" yazarsa "dollars" eksik sayılmasın
    m = re.sub(r"stat ?(4|for|four) ?sight", "statforsight", m)
    m = re.sub(r"[^a-z0-9.' ]+", " ", m)
    m = re.sub(r"(?<!\d)\.|\.(?!\d)", " ", m)
    m = re.sub(r"\bu n\b", "un", re.sub(r"\bg d p\b", "gdp", " ".join(m.split())))
    m = " ".join(soz(t) for t in m.split()).replace("hundred and", "hundred")
    es = {"turkey": "turkiye", "turkiyes": "turkiye's", "row": "rho", "roe": "rho", "nizhair": "niger", "nijer": "niger",
          "for": "four", "to": "two", "too": "two"}
    return [es.get(w, w) for w in m.split()]


def beklenen(okunus):
    return okunus.replace("Nee-zhair", "Niger")   # Whisper Niger'i "Niger" diye yazar; "Nigeria" yazarsa hata
