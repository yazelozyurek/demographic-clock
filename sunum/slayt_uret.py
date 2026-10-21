"""Final sunumun kapak ve 4 içerik slaytını üretir (kaynakça elle yazılı, açık temada renkleri çevrilerek kopyalanır).
Düzen: her içerik slaytı aynı iskelet = üst yazı + başlık + tek satır alt başlık · hizalı kart ızgarası · "What it means" bandı · dipnot.
Her grafik bir kartın içinde; kart başlıkları hep aynı stilde (grafiklerin kendi içinde başlık yok).
Sayılar clean/ ve outputs/ dosyalarından gelir; elle yazılanlar 04/05 notebook çıktılarıdır.
Çalıştırma:  python sunum/slayt_uret.py <slayt klasörü>          → FİNAL koyu sunum (Q3 + Q4, 21 Ekim)
             ONIZLEME=1 python sunum/slayt_uret.py <klasör>     → aynı slaytlar, görseller outputs/ klasöründen (yerel önizleme)
             DESTE=eski python sunum/slayt_uret.py <klasör>    → eski koyu sunumun görselleri (Taslak 1)
             TEMA=acik python sunum/slayt_uret.py <slayt klasörü> → Taslak 2 (açık; Q3 grafiği henüz yok)"""
import os
import re
import sys
from pathlib import Path
import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parent.parent
HEDEF = Path(sys.argv[1])
ACIK = os.environ.get("TEMA") == "acik"
if ACIK:   # Taslak 2 sunumuna yüklü görseller
    BLOB = {"cover": "/_blob/4f5ae148ff8dcd4232549969b85d67dd", "gif": "/_blob/7aaadda36e683e53ad6e872b38bd8bfa",
            "regions": "/_blob/6ec1acd18f6b686a2beb677e9920d788", "hist": "/_blob/16810a26b6bb3154b23715b8a007dc42",
            "corr": "/_blob/19f640f26140ca291c0ff1c9b02b55ac", "map": "/_blob/f1db96afb818ceb6841c43319eb41931",
            "pairs": "/_blob/480fe8b5220e025a3c643900a99f1114", "spread": "/_blob/6afc521136c9be963ef368147eb4afee",
            "pop": "/_blob/7f1af236fa5dd9d9d4c17865920fb95b", "three": "/_blob/0c33c6deb84f3597cf8497d0eeb2b478", "health": ""}
elif os.environ.get("DESTE") != "eski":   # FİNAL koyu sunum (https://claude.ai/artifact/MEYv3jt4EcXwixohtjvXd4)
    BLOB = {"cover": "/_blob/fffb88015fe5885854f6b1925247f566", "gif": "/_blob/499a19039b078b0fd7247e0f155a4f1e",
            "regions": "/_blob/21253fd0c70125b06abe8643d716cf88", "hist": "/_blob/282a6f13b1afbe1383e7d81ff7c95070",
            "corr": "/_blob/4697bf3d112167be2b61548e6c9cd8ac", "map": "/_blob/4aec6eb7a607c658a140c8dd7310536e",
            "pairs": "/_blob/be4ff1fd6ab3b9712ad0cbc9060f0725", "spread": "/_blob/bf6e5f05e6acc33d4de0afcd9296bb99",
            "pop": "/_blob/8ca44322eccafc5bc2e8b4bd18f27157", "three": "/_blob/970a39face59db71f46dd40819e62d1b",
            "health": "/_blob/b1d72b545cb86a90463a2ba68ed58cf6"}
else:      # Taslak 1 sunumuna yüklü görseller
    BLOB = {"cover": "/_blob/f69f4620deb9aeb3e9a1fa4c09a03881", "gif": "/_blob/a9abf229ad9e7c9c9c41caa06e4d9776",
            "regions": "/_blob/22f79961c14eb6d2cce5e5feff16c9cb", "hist": "/_blob/b762ce40843ed4b19c9e233a3c00bc59",
            "corr": "/_blob/25a9e727fe782b64d03b408bf316fa7a", "map": "/_blob/9cd760a97941af07ca69daa5cdef74b3",
            "pairs": "/_blob/a2ba1d79c53b9f7b6fd0038117bbc707", "spread": "/_blob/afc4421084826537284e3f6d07ce4877",
            "pop": "/_blob/48fb614e93609f297677809fe4af714b", "three": "/_blob/4b28a971c0a6c58f3c65af80e4fcae2d", "health": ""}
for _k in ("cause", "popc"): BLOB.setdefault(_k, "")   # Q4 görselleri: sunuma yüklenince final sözlüğüne id'leri yazılır
if os.environ.get("ONIZLEME"):   # yerel önizleme (sadece final koyu sunum): görseller doğrudan outputs/ klasöründen
    _o = "file://" + str(KOK / "outputs") + "/"
    BLOB = {k: _o + v for k, v in {"cover": "final_0_cover_clock2.png", "gif": "final_anim_son_kare_dark_sade.png",
            "regions": "v3_s1_regions.png", "hist": "v3_s1_hist.png", "corr": "v3_s1_corr.png", "map": "v3_s2_map.png",
            "pairs": "v3_s2_pairs.png", "spread": "v3_s3_spread.png", "pop": "v3_s4_population.png", "three": "v3_s4_three.png",
            "health": "v3_s3_health.png", "cause": "v3_s4_cause.png", "popc": "v3_s4_pop_compact.png"}.items()}

# ---------- tema: slaytlar mavi renklerle yazılır, açık temada renkler bu tabloyla çevrilir ----------
ACIK_RENK = {"#1C2E3E": "#FDFDFB", "#0F1A24": "#F3F2EE", "#15222E": "#FBFBF9", "#253645": "#E0DED8", "#101C27": "#F7F6F2",
             "#16232F": "#F3F2EE", "#1E3A5C": "#FFF4D9", "#1A2740": "#FFFBF0", "#2F4A66": "#EED9A6", "#1B3354": "#E8F1FC",
             "#2A1F3D": "#FCEDE6", "#3A5578": "#D9DDE3", "#3A4B5A": "#D6D4CE", "#1E2E3C": "#ECEBE7", "#2E4254": "#E2E6EA",
             "#16263A": "#E9F1FB", "#16222E": "#F1F1EF", "#2A1E1A": "#F8EEE8", "#4A2A1C": "#F6E1D5",
             "#E8EEF2": "#1F2328", "#FFFFFF": "#1F2328", "#EEF2F4": "#1F2328", "#9FB0BD": "#5E6873", "#7F92A1": "#6B7480",
             "#C9D4DC": "#3F4B56", "#D3DCE2": "#3F4B56", "#B9C6CF": "#4A525B",
             "#4FB3FF": "#2563B8", "#7FB0F0": "#2563B8", "#FF8A3D": "#C2501C", "#FF8A5C": "#C2501C", "#5FA0F0": "#2A78D6",
             "#FFD166": "#B7791F", "#3FC1FF": "#5C9FE8", "#5E6873": "#AEB4BB", "#7F8C99": "#C5CAD0",
             "#4DA3FF": "#2A78D6", "#FF7A3D": "#EB6834", "#2FD49A": "#1BAF7A", "#FFC233": "#EDA100", "#FF5FA2": "#E87BA4",
             "#A98BFF": "#6250D6"}
def tema(metin):
    if not ACIK: return metin
    metin = metin.replace("color:#0F1A24", "color:#1F2328")                 # renkli çubukların üstündeki yazı koyu kalır
    metin = metin.replace("#B04A20, #FF8A3D", "#F6B48C, #EE8F5C").replace("#FF6A2B, #FF8A5C", "#FF8A55, #FFAD85")
    return re.sub(r"#[0-9A-Fa-f]{6}", lambda m: ACIK_RENK.get(m.group(0).upper(), m.group(0)), metin)

def yazi_rengi(zemin):
    """Hücre yazısı: açık temada açık hücrede koyu, koyu/renkli hücrede beyaz (#FEFEFE çeviriye girmez)."""
    if not ACIK: return "#FFFFFF"
    zemin = tema(zemin)
    if not zemin.startswith("#"): return "#FEFEFE"
    r, g, b = (int(zemin[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return "#1F2328" if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.55 else "#FEFEFE"

def karis(a, b, t):
    a, b = tema(a), tema(b)
    a = np.array([int(a[i:i + 2], 16) for i in (1, 3, 5)]); b = np.array([int(b[i:i + 2], 16) for i in (1, 3, 5)])
    return "#" + "".join(f"{int(round(v)):02X}" for v in a + (b - a) * float(np.clip(t, 0, 1)))

# ---------- ortak parçalar (her slaytta aynı) ----------
BG = "background:radial-gradient(ellipse at 85% 0%, #1C2E3E, #0F1A24)"
KUTU = "background:#15222E;border:1px solid #253645;border-radius:14px"
H3 = "font-size:26px;line-height:1.2;font-weight:600;color:#FFFFFF"
DIPNOT = '<p style="position:absolute;left:128px;bottom:52px;width:1660px;font-size:24px;color:#7F92A1">{}</p>\n'

def bolum_ac(no, ust, baslik, alt, sag=""):
    """Slayt iskeleti: üst yazı, başlık, tek satır alt başlık (sağda isteğe bağlı kart). Yükseklik hep aynı."""
    return (f'<section id="{no}" data-transition="fade" style="{BG};color:#E8EEF2;font-family:\'IBM Plex Sans\', Arial, sans-serif;'
            f'padding:64px 128px 132px;display:flex;flex-direction:column;gap:16px">\n'
            f'<div style="display:flex;flex-direction:row;gap:32px;align-items:end">\n<div style="flex:1;display:flex;flex-direction:column;gap:6px">\n'
            f'<p style="font-size:24px;line-height:1.3;letter-spacing:2px;text-transform:uppercase;color:#4FB3FF">{ust}</p>\n'
            f'<h2 style="font-family:\'Source Serif 4\', Georgia, serif;font-size:50px;font-weight:600;line-height:1.1;color:#FFFFFF">{baslik}</h2>\n'
            f'<p style="font-size:26px;line-height:1.3;color:#9FB0BD">{alt}</p>\n</div>\n{sag}</div>\n')

def kart(baslik, icerik, ek=""):
    """Her içerik parçası aynı kartta: üstte başlık, altta içerik."""
    return (f'<div style="display:flex;flex-direction:column;gap:8px;{KUTU};padding:12px 18px;{ek}">\n'
            f'<h3 style="{H3}">{baslik}</h3>\n{icerik}\n</div>\n')

def gorsel(anahtar, alt, w, h):
    return f'<img src="{BLOB[anahtar]}" alt="{alt}" style="width:{w}px;height:{h}px;object-fit:contain">'

def anlam(metin):
    return ('<div style="display:flex;flex-direction:row;gap:18px;align-items:center;background:linear-gradient(90deg, #1E3A5C, #1A2740);'
            'border:1px solid #2F4A66;border-left:6px solid #FFD166;border-radius:12px;padding:12px 22px">'
            '<p style="width:200px;font-size:24px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:#FFD166">What it means</p>'
            f'<p style="width:1380px;font-size:24px;line-height:1.35;color:#FFFFFF">{metin}</p></div>\n')

def hucre(metin, zemin, kalin=False, sol=False, ek=""):
    return (f'<p style="background:{zemin};color:{yazi_rengi(zemin)};font-size:24px;line-height:1.3;padding:3px 12px;border-radius:6px;'
            f'text-align:{"left" if sol else "right"};{"font-weight:600;" if kalin else ""}{ek}">{metin}</p>')

def cubuk(etiket, deger, metin, renk, olcek, etiket_w=250, parla=False):
    golge = "box-shadow:0 0 18px rgba(63,193,255,0.55);" if parla else ""
    return (f'<div style="display:flex;flex-direction:row;gap:10px;align-items:center">'
            f'<p style="width:{etiket_w}px;font-size:24px;line-height:1.2;color:{"#FFFFFF" if parla else "#C9D4DC"}">{etiket}</p>'
            f'<p style="width:{max(int(deger * olcek), 70)}px;background:{renk};{golge}color:#0F1A24;font-size:24px;line-height:1.2;font-weight:600;'
            f'padding:1px 10px;border-radius:6px;text-align:right">{metin}</p></div>')

def baslik_satiri(adlar, hizalar, pad="1px 12px"):
    return "".join(f'<p style="font-size:24px;line-height:1.2;color:#9FB0BD;padding:{pad};text-align:{h}">{a}</p>' for a, h in zip(adlar, hizalar))

def kapat(notlar):
    return f"<aside>{notlar}</aside>\n</section>\n"

def yaz(ad, s):
    (HEDEF / f"{ad}.html").write_text(tema(s))

df = pd.read_csv(KOK / "clean/countries_1950_2100.csv", low_memory=False)
df = df[df["pop2023"] >= 100]
d23 = df[df["Time"] == 2023].set_index("Location")
kor, nij = d23.at["Republic of Korea", "TFR"], d23.at["Niger", "TFR"]
po = pd.read_csv(KOK / "clean/para_okul_tablosu.csv").set_index("Location")

# =============== Kapak ===============
s = ('<section id="cover" data-transition="fade" style="background:#101C27;color:#EEF2F4;font-family:\'IBM Plex Sans\', Arial, sans-serif;'
     'padding:104px 128px 96px;display:flex;flex-direction:column;gap:18px">\n'
     f'<img src="{BLOB["cover"]}" alt="The Demographic Clock: a glowing clock dial from 1920 to 2080. Each of 200 countries is a dot at the year its '
     'fertility fell fastest, coloured by region; Europe clusters around 1930–1950, Latin America and Asia around 1965–2000, Africa around '
     '2010–2030. A white inner band is the health clock, the years life expectancy rose fastest; it runs a median 18 years ahead. Türkiye is ringed: '
     'health 1965, fertility 1982. A gold hand marks 2023. In the centre, all countries’ curves shifted to their own turning point form one shared S-curve (R² = 0.94)" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">\n'
     '<p style="font-size:26px;letter-spacing:3px;text-transform:uppercase;color:#7FB0F0">ASA DataQuest 2026 · Undergraduate</p>\n'
     '<h1 style="font-family:\'Source Serif 4\', Georgia, serif;font-size:96px;font-weight:700;line-height:1.02;letter-spacing:-1px;color:#FFFFFF;width:940px;'
     'background:linear-gradient(100deg, #6FB8FF 0%, #A98BFF 50%, #FF8A5C 100%);background-clip:text;-webkit-background-clip:text;-webkit-text-fill-color:transparent">The Demographic Clock</h1>\n'
     '<p style="font-size:34px;line-height:1.35;color:#C9D4DC;width:780px">Same path, different time zones. Health turns first; money does not set the clock.</p>\n'
     '<div style="flex:1"></div>\n<div style="display:flex;flex-direction:column;gap:10px;width:760px">\n'
     '<p style="font-size:24px;line-height:1.4;color:#9FB0BD">Each dot is a country at its turning point, the year its fertility fell fastest '
     '(hollow: inferred). White inner band: the health clock, the year life expectancy rose fastest. White rings: Türkiye. Gold hand: 2023. '
     'Centre: all 200 paths shifted to their turning point form one curve.</p>\n'
     '<p style="font-size:24px;line-height:1.4;color:#9FB0BD"><span style="color:#4DA3FF">●</span> Asia <span style="color:#FF7A3D">●</span> Africa '
     '<span style="color:#2FD49A">●</span> Europe <span style="color:#FFC233">●</span> Latin Am. <span style="color:#FF5FA2">●</span> N. Am. '
     '<span style="color:#A98BFF">●</span> Oceania</p>\n'
     '<div style="border-top:1px solid #3A4B5A;padding-top:16px;display:flex;flex-direction:column;gap:6px">\n'
     '<p style="font-size:32px;font-weight:600;color:#FFFFFF">Stat4Sight</p>\n'
     '<p style="font-size:26px;line-height:1.35;color:#D3DCE2">Yazel Sude Özyürek · Elif Zarife Yıldırım</p>\n'
     '<p style="font-size:26px;line-height:1.35;color:#D3DCE2">Zehra İklil Canatar · Rojbin Bağatur</p>\n'
     '<p style="font-size:24px;line-height:1.35;color:#B9C6CF">Kırıkkale University, Department of Statistics</p>\n</div>\n</div>\n')
s += kapat("Hello, we are Stat4Sight from Kırıkkale University. Every country is moving from large families to small ones. "
           "Our project asks three things: is it the same journey everywhere, does money or school set its timing, and does health come first?")
yaz("cover", s)

# =============== Slayt 1: Soru ve veri · 2×2 kart ızgarası ===============
SAYI = "font-family:'Source Serif 4', Georgia, serif;font-size:44px;font-weight:600;line-height:1.1;white-space:nowrap"
def kanca_sayi(deger, renk, ulke):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:0px">'
            f'<p style="{SAYI};color:{renk}">{deger:.2f}</p><p style="font-size:24px;line-height:1.2;color:#C9D4DC;white-space:nowrap">{ulke}</p></div>')
kanca = (f'<div style="width:420px;display:flex;flex-direction:column;align-items:center;gap:6px;{KUTU};padding:10px 22px">'
         f'<div style="display:flex;flex-direction:row;align-items:center;justify-content:center;gap:28px">'
         + kanca_sayi(kor, "#4FB3FF", "Korea") + '<p style="font-size:24px;color:#7F92A1">vs</p>' + kanca_sayi(nij, "#FF8A3D", "Niger")
         + '</div><p style="font-size:24px;line-height:1.2;color:#9FB0BD;white-space:nowrap">children per woman, 2023</p></div>\n')
s = bolum_ac("question", "1 · Question and data", "One journey, very different times",
             '<span style="color:#FF8A3D">Q1</span> Same path, only different timing? · <span style="color:#FF8A3D">Q2</span> Money or school? · '
             '<span style="color:#FF8A3D">Q3</span> Health first?',
             kanca)
huni = '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-around">\n'
for w, g, yazi, renk, sag in [(380, "#FF6A2B, #FF8A5C", "555 rows", "#FF8A5C", "362.9 bn ✗ counted ~45×"),
                              (162, "#FF4F7A, #FF7A9A", "237", "#E8EEF2", "countries · 8.09 bn ✓ = World"),
                              (137, "#7A6CFF, #9B8CFF", "200", "#FFFFFF", "<b>our sample</b> · 99.98% of people"),
                              (84, "#3987e5, #5FA0F0", "112", "#E8EEF2", "turning point seen 1952–2013 · 69%"),
                              (60, "#2FB7FF, #6FD0FF", "66", "#E8EEF2", "+ Maddison income, Barro–Lee schooling · 67%")]:
    huni += (f'<div style="display:flex;flex-direction:row;gap:14px;align-items:center"><p style="width:{w}px;background:linear-gradient(90deg, {g});color:#0F1A24;'
             f'font-size:24px;line-height:1.2;font-weight:600;padding:1px 10px;border-radius:6px">{yazi}</p>'
             f'<p style="font-size:24px;line-height:1.2;color:{renk}">{sag}</p></div>\n')
huni += '</div>'
s += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">\n'
s += kart("Children per woman by region, 1950–2100",
          gorsel("regions", "Line chart: population-weighted children per woman by region, 1950–2100; Africa highest, Europe lowest, all converging near replacement by 2100 in the UN projection", 784, 232))
s += kart("Correlations across 200 countries, 2023",
          gorsel("corr", "Correlation heatmap, 2023: fertility −0.82 with life expectancy and −0.87 with median age; life expectancy and infant mortality −0.91", 784, 232))
s += kart("How the 200 countries are spread",
          gorsel("hist", "Histograms of children per woman across 200 countries: 3 below 2.1 in 1950, 47 in 1990, 103 in 2023, 187 in 2100 (UN projection); medians 6.0, 3.6, 2.0, 1.7", 784, 232))
s += kart("From raw file to sample", huni)
s += '</div>\n'
s += anlam("The world is moving to small families, but not in step: in 2023 half the countries were below replacement while some "
           "still averaged six children. So we ask <b>when</b> each country changes, and what goes with that moment.")
s += DIPNOT.format("UN World Population Prospects 2024 · 1950–2023 estimates; dashed = UN projections · every excluded place is listed by name (excluded_places.csv)")
s += kapat(f"In 2023, women in the Republic of Korea had {kor:.2f} children on average; women in Niger had {nij:.2f}. "
           "In 1950, only 3 of 200 countries were below replacement; by 2023 it was 103. So we asked: do countries follow the same path, "
           "and what moves with their turning point: money, school, or health?\n\n"
           "Our data is UN World Population Prospects 2024. Summing every row gives 363 billion people, because regions repeat countries; "
           "countries alone give 8.09 billion. We keep 200 countries, 99.98 percent of the world, list every place we leave out, "
           "and always draw UN projections dashed.")
yaz("question", s)

# =============== Slayt 2: Demografik Saat · üstte 2 büyük kart, altta 3 eşit kart ===============
r2 = [("Calendar year only", 0.27, "#5E6873", False), ("Country average", 0.60, "#7F8C99", False),
      ("Curve + level shift", 0.87, "linear-gradient(90deg, #6250d6, #9085e9)", False),
      ("Curve + time shift", 0.94, "linear-gradient(90deg, #3987e5, #3FC1FF)", True),
      ("Separate curves*", 0.99, "#5E6873", False)]
bt = [("1983→2003", 1.11, 0.56, 0.49), ("1993→2013", 0.77, 0.56, 0.38), ("2003→2023", 0.59, 0.51, 0.41)]
s = bolum_ac("clock", "2 · The Demographic Clock", "One shared path, shifted in time for each country",
             "Fitted on 1950–2023 only · 200 countries · one shared S-curve, one time shift (turning point) per country")
s += '<div style="display:grid;grid-template-columns:562px 1fr;gap:16px">\n'
s += kart("Shift each country to its own clock",
          gorsel("gif", "Animation: 200 countries’ fertility curves slide from calendar time onto one shared S-curve; R² rises from 27% to 94%; in 2023 Nigeria is at its turning point, Türkiye about 40 years past it, Japan about 90", 526, 296))
s += kart("The clock on a map: year each country’s fertility fell fastest",
          gorsel("map", "World map coloured by turning-point year: Europe, North America and Australia turned before 1960 (mostly inferred), Latin America and Asia between 1965 and 2000, most of Africa after 2000", 1046, 296))
s += '</div>\n<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px">\n'
r2_icerik = '<div style="display:flex;flex-direction:column;gap:4px">' + "".join(cubuk(ad, v, f"{v:.2f}", renk, 245, 235, p) for ad, v, renk, p in r2) + '</div>'
s += kart("Variation explained (R²)", r2_icerik)
bt_icerik = ('<div style="display:grid;grid-template-columns:150px 1fr 1fr 1fr;gap:5px">'
             + baslik_satiri(["Data to", "Naive", "Separate", "Shared"], ["left", "right", "right", "right"], "1px 8px"))
for ad, n, a, o in bt:
    bt_icerik += hucre(ad, "#1E2E3C", sol=True) + hucre(f"{n:.2f}", karis("#4A2A1C", "#D95926", (n - 0.5) / 0.65))
    bt_icerik += hucre(f"{a:.2f}", "#2E4254") + hucre(f"{o:.2f}", "linear-gradient(90deg, #3987e5, #3FC1FF)", kalin=True)
bt_icerik += '</div>\n<p style="font-size:24px;line-height:1.2;color:#9FB0BD">median |error|, children per woman</p>'
s += kart("Backtest: error 20 years ahead", bt_icerik)
s += kart("Regions turn at different times",
          gorsel("pairs", "Pairwise Mann–Whitney tests of turning-point years between regions, Holm-adjusted: Africa differs from Asia (p = 0.023), Europe (p = 0.047) and Latin America (p &lt; 0.001); Kruskal–Wallis p = 0.00005", 503, 172))
s += '</div>\n'
s += anlam("Countries differ mainly in <b>when</b> they turn, not how: given its own clock, one curve fits 94%, and regions differ clearly "
           "in timing (p&#160;&lt;&#160;0.001). A later clock is not a worse country.")
s += DIPNOT.format("After SITAR growth curves (Cole et al., 2010) · * 16 of 200 separate fits hit their limits · region tests: 115 well-observed countries")
s += kapat("Our first try fitted an S-shaped curve to each country separately. It fit, but gave nonsense: for Japan, whose decline happened before 1950, "
           "it said women started at nine children.\n\nSo we borrowed the SITAR idea from children’s growth charts: one shared S-curve, and one number "
           "per country — its turning point, the year fertility falls fastest. Watch what happens when we shift each country.\n\n"
           "By calendar year, time explains 27 percent of the differences between countries. Shifted to their own turning points, one curve explains "
           "94 percent, and it predicted best in backtests.\n\nOn the map, the clock runs from Europe to Africa. "
           "In 2023, Nigeria is at its turning point, Türkiye passed it about forty years ago, Japan about ninety.")
yaz("clock", s)

# =============== Slayt 3: Ne saatle birlikte yürüyor? · solda Q2 (3 kart), sağda Q3 ana grafik ===============
sg = pd.read_csv(KOK / "clean/saglik_saati.csv")
sg = sg[sg["guvenilir"] & sg["t0_saglik"].notna()]
sg_once = 100 * (sg["fark"] > 0).mean(); sg_fark = sg["fark"].median()
s = bolum_ac("money", "3 · What moves with the clock?", "Money does not set the clock; health turns first",
             '<span style="color:#FF8A3D">Q2</span> Money or school? 66 countries, Maddison and Barro–Lee · '
             '<span style="color:#FF8A3D">Q3</span> Health first? 115 countries, UN WPP')
s += '<div style="display:grid;grid-template-columns:640px 1fr;gap:16px">\n<div style="display:flex;flex-direction:column;gap:16px">\n'
s += kart("Q2 · Error guessing the turning year",
          cubuk("Income", 14.0, "14.0", "linear-gradient(90deg, #B04A20, #FF8A3D)", 16, 150) + "\n"
          + cubuk("Schooling", 9.5, "9.5", "linear-gradient(90deg, #3987e5, #3FC1FF)", 16, 150) + "\n"
          + cubuk("Calendar", 9.5, "9.5", "#5E6873", 16, 150) + "\n"
          + '<p style="font-size:24px;line-height:1.3;color:#C9D4DC">years · income worse than the calendar, <b>p &lt; 0.001</b> · '
            'schooling no better, p = 0.75</p>')
s += kart("Q2 · Where countries stood at the turn",
          f'<p style="font-size:24px;line-height:1.3;color:#C9D4DC">Income <b style="color:#FF8A3D">${po["gelir"].min():,.0f} – ${po["gelir"].max():,.0f}</b>: no wealth threshold</p>'
          f'<p style="font-size:24px;line-height:1.3;color:#C9D4DC">Schooling <b style="color:#5FA0F0">{po["egitim"].min():.1f} – {po["egitim"].max():.1f} years</b>: '
          '1.34× tighter (CI 1.09–1.67)</p>')
s += kart("Once 1950 health and schooling are known",
          '<p style="font-size:24px;line-height:1.3;color:#C9D4DC">income adds <b style="color:#FFFFFF">nothing</b> (p = 0.84, 64 countries)</p>',
          "flex:1")
s += '</div>\n'
s += kart("Q3 · Two clocks: health turns first, fertility follows",
          gorsel("health", f"Scatter plot of 115 countries: x is the year life expectancy rose fastest, y is the year fertility fell fastest. "
                 f"{sg_once:.0f}% of countries lie above the same-year line, a median {sg_fark:.0f} years later; Spearman rho 0.77. "
                 "Türkiye: health 1965, fertility 1982", 972, 457)
          + '\n<p style="font-size:24px;line-height:1.3;color:#C9D4DC">Knowing the health clock cuts the error in guessing the fertility clock from '
            '<b>12 to 6 years</b> (leave-one-out) · within regions ρ = 0.71</p>')
s += '</div>\n'
s += anlam(f"No wealth threshold sets the clock. Health moves with it: in {sg_once:.0f}% of countries, life expectancy rose fastest first, "
           f"a median {sg_fark:.0f} years earlier. These are patterns, not causes.")
s += DIPNOT.format("<b>External data</b>: income from the Maddison Project Database 2023 (GDP per person, via Our World in Data) · schooling from Barro–Lee v3, women 25–34<br>"
                  "Health clock: same shared-curve method on UN WPP life expectancy, 1950–2023 · many other candidates screened (FDR) · association, not cause")
s += kapat("Next: what lines up with the turning point?\n\n"
           "First, money or school. In 66 countries, income at the turning point ranged from 1,100 to 24,000 dollars. As a threshold it missed "
           "the year by 14 years, worse than guessing the typical year. Schooling was steadier, but no better than the calendar.\n\n"
           "That no is a result, not a failure, and it led us to the oldest prediction of transition theory: does health come first? We measured "
           f"a second clock, the year life expectancy rose fastest, with the same shared curve. In {sg_once:.0f} percent of 115 countries it came "
           f"first, a median of {sg_fark:.0f} years earlier, and the two clocks move together, rho 0.77. We screened many candidates, with "
           "multiple-test correction.\n\n"
           "So money does not set the clock; health moves with it. But first is not the same as cause: a rooster crows before every sunrise, "
           "yet it does not make the sun rise.")
yaz("money", s)

# =============== Slayt 4: Q4 sebep testi + Türkiye + sınırlar · solda doğal deney grafiği, sağda Türkiye ve "iddia etmediklerimiz" ===============
# Sayılar ön kayıtlı testlerin çıktılarından (kesif/d_neden, kesif/e_hiv, kesif/f_kreitmeir); HIV p-değeri kesif/e_hiv/log.txt'ten.
ku = pd.read_csv(KOK / "kesif/f_kreitmeir/sonuc.csv", index_col=0)
ku_ana = ku.loc["ANA: ülke düzeyi, ΔTFR 1950→1990"]
ku_ar = [float(v) for v in re.findall(r"-?\d+\.\d+", ku_ana["AR"])]          # zayıf araca dayanıklı %95 aralık, ΔlnLE başına
b10, ar_lo, ar_hi = 0.1 * float(ku_ana["beta"]), -0.1 * ku_ar[1], -0.1 * ku_ar[0]   # yaşam beklentisi ~%10 daha çok artınca (çocuk azalışı)
ku_F = float(ku_ana["F"])
aj_F = float(pd.read_csv(KOK / "kesif/d_neden/sonuc.csv", index_col=0).iloc[0]["F"])
hiv_p = 0.40
assert ku.loc["D6: veri kontrolü, Δln toplam doğum 1940→80", "beta"] > 0          # toplam doğum arttı
trs = pd.read_csv(KOK / "clean/saglik_saati.csv").set_index("Location").loc["Türkiye"]
tr_s, tr_d = int(np.floor(trs["t0_saglik"] + 0.5)), int(np.floor(trs["t0"] + 0.5))   # .5 yukarı: 1965, 1982
poT = po.loc["Türkiye"]; gelir_alt = int((po["gelir"] < poT["gelir"]).sum()); egitim_ust = int((po["egitim"] > poT["egitim"]).sum())
YAZ = "font-size:24px;line-height:1.3;color:#C9D4DC"
def test_cip(isaret, metin):
    renk = "#2FD49A" if isaret == "✓" else "#FF8A3D"
    return (f'<p style="font-size:24px;line-height:1.2;color:#E8EEF2;background:#16222E;border:1px solid #3A4B5A;border-radius:8px;'
            f'padding:3px 12px;white-space:nowrap"><b style="color:{renk}">{isaret}</b> {metin}</p>')
s = bolum_ac("turkiye", "4 · One more question", "Where medicines saved more lives, fertility later fell further",
             '<span style="color:#FF8A3D">Q4</span> Is health a cause? A natural experiment in 50 countries · then Türkiye and our limits')
s += '<div style="display:grid;grid-template-columns:940px 1fr;gap:16px">\n'
s += kart("Q4 · The 1940s medicines as a natural experiment",
          gorsel("cause", "Scatter plot of 50 countries: x is how many deaths per 1,000 people a year the medicines and vaccines of the 1940s could "
                 "prevent, given each country's 1940 disease mix (0 to 10); y is the change in children per woman from 1950 to 1990. The fitted line "
                 "falls: more deaths prevented, larger fall in fertility. Rich countries of 1940 sit at the left; Republic of Korea, Sri Lanka, "
                 "Egypt, Mexico and Guatemala are labelled", 900, 400)
          + f'\n<p style="{YAZ}">About 10% more life expectancy (1940–80) → <b style="color:#FFFFFF">{-b10:.2f} fewer children</b> per woman by 1990 '
            f'(95% CI {ar_lo:.2f}–{ar_hi:.2f}, first stage F = {ku_F:.0f}) · yet total births rose</p>'
          + '\n<div style="display:flex;flex-direction:row;gap:10px;align-items:center">'
            f'<p style="{YAZ};white-space:nowrap">Three tests:</p>'
          + test_cip("✗", f"Timing · F &lt; {np.ceil(aj_F):.0f}") + test_cip("✗", f"HIV shock · p = {hiv_p:.2f}") + test_cip("✓", "Fertility fall")
          + '</div>')
s += '<div style="display:flex;flex-direction:column;gap:16px">\n'
s += kart(f"Türkiye: health {tr_s} → fertility {tr_d}",
          gorsel("popc", "Türkiye population 1950–2100: UN estimate to 2023, then the Medium projection peaking in 2047 at 91 million, with 80% and "
                 "95% prediction intervals widening to 26–125 million in 2100", 668, 230)
          + f'\n<p style="{YAZ}">At its turn, richer than {gelir_alt} of 66 countries, with less schooling than {egitim_ust} · '
            'peak 2047 at 91 M; for 2100, a range (26–125 M)</p>')
iddia = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 20px">\n'
for m in ["A settled cause", "Individual-level facts", "Observed UN figures", "Independent UN series",
          "Projections as forecasts", "That ahead is better"]:
    iddia += f'<p style="{YAZ}">· {m}</p>\n'
iddia += '</div>'
s += kart("What we do not claim", iddia, "flex:1;border-left:5px solid #d95926")
s += '</div>\n</div>\n'
s += anlam("Where the 1940s medicines saved more lives, births first rose, but children per woman fell further by 1990. "
           "One of three tests, each planned in advance, supports health as a cause; none settles it.")
s += DIPNOT.format("<b>Natural experiment</b>: Kreitmeir &amp; Überfuhr (2024) instrument, after Acemoglu &amp; Johnson (2007) · two-stage least squares, "
                   "weak-IV-robust 95% CI<br>Each test's plan was committed before its results · HIV: World Bank (UNAIDS) · Türkiye: UN WPP 2024 "
                   "intervals · ASA Ethical Guidelines (2022)")
s += kapat("So, one more question: is health a cause, or just the rooster? We ran three tests, each planned before seeing its results. "
           "Two could not tell. The third is a natural experiment: in the 1940s, new medicines and vaccines reached the world at once, and "
           "countries hit hardest by those diseases gained most. Where they saved more lives, more babies were born, but each woman had fewer: "
           f"about ten percent more life expectancy, {-b10:.2f} fewer children by 1990. This supports health as a cause, but does not settle it, "
           "because the signal comes from how sick countries were in 1940.\n\n"
           f"Türkiye’s health clock turned in {tr_s}, its fertility clock in {tr_d}. Its population likely peaks in 2047; for 2100 we show "
           "a range, 26 to 125 million.\n\nOur limits: these are country patterns, not facts about individual women, and the clock is not a race.")
yaz("turkiye", s)

if ACIK:   # kaynakça elle yazılı: mavi sürümden renkleri çevirerek kopyala
    yaz("references", (KOK / "sunum/slaytlar_kaynak/slides/references.html").read_text())
print("yazıldı: cover, question, clock, money, turkiye" + (", references (açık)" if ACIK else ""))
