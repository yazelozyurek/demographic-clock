"""Final sunumun kapak ve 4 içerik slaytını üretir (kaynakça elle yazılı, açık temada renkleri çevrilerek kopyalanır).
Düzen: her içerik slaytı aynı iskelet = üst yazı + başlık + tek satır alt başlık · hizalı kart ızgarası · "What it means" bandı · dipnot.
Her grafik bir kartın içinde; kart başlıkları hep aynı stilde (grafiklerin kendi içinde başlık yok).
Sayılar clean/ ve outputs/ dosyalarından gelir; elle yazılanlar 04/05 notebook çıktılarıdır.
Çalıştırma:  python sunum/slayt_uret.py <slayt klasörü>          → Taslak 1 (mavi)
             TEMA=acik python sunum/slayt_uret.py <slayt klasörü> → Taslak 2 (açık)"""
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
            "pop": "/_blob/7f1af236fa5dd9d9d4c17865920fb95b", "three": "/_blob/0c33c6deb84f3597cf8497d0eeb2b478"}
else:      # Taslak 1 sunumuna yüklü görseller
    BLOB = {"cover": "/_blob/f69f4620deb9aeb3e9a1fa4c09a03881", "gif": "/_blob/a9abf229ad9e7c9c9c41caa06e4d9776",
            "regions": "/_blob/22f79961c14eb6d2cce5e5feff16c9cb", "hist": "/_blob/b762ce40843ed4b19c9e233a3c00bc59",
            "corr": "/_blob/25a9e727fe782b64d03b408bf316fa7a", "map": "/_blob/9cd760a97941af07ca69daa5cdef74b3",
            "pairs": "/_blob/a2ba1d79c53b9f7b6fd0038117bbc707", "spread": "/_blob/afc4421084826537284e3f6d07ce4877",
            "pop": "/_blob/48fb614e93609f297677809fe4af714b", "three": "/_blob/4b28a971c0a6c58f3c65af80e4fcae2d"}

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
     '2010–2030. Inner arcs show each region’s middle half of turning years; a gold hand marks 2023. In the centre, all countries’ curves shifted to '
     'their own turning point form one shared S-curve (R² = 0.94)" style="position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover">\n'
     '<p style="font-size:26px;letter-spacing:3px;text-transform:uppercase;color:#7FB0F0">ASA DataQuest 2026 · Undergraduate</p>\n'
     '<h1 style="font-family:\'Source Serif 4\', Georgia, serif;font-size:92px;font-weight:600;line-height:1.04;color:#FFFFFF;width:880px">The Demographic Clock</h1>\n'
     '<p style="font-size:34px;line-height:1.35;color:#B9C6CF;width:760px">Same path, different time zones: what sets the timing of the fertility transition?</p>\n'
     '<div style="flex:1"></div>\n<div style="display:flex;flex-direction:column;gap:10px;width:760px">\n'
     '<p style="font-size:24px;line-height:1.4;color:#9FB0BD">Each dot is a country at its turning point, the year its fertility fell fastest '
     '(hollow: inferred). Inner arcs: each region’s typical turning years. Gold hand: 2023. Centre: all 200 paths shifted to that year form one curve.</p>\n'
     '<p style="font-size:24px;line-height:1.4;color:#9FB0BD"><span style="color:#4DA3FF">●</span> Asia <span style="color:#FF7A3D">●</span> Africa '
     '<span style="color:#2FD49A">●</span> Europe <span style="color:#FFC233">●</span> Latin Am. <span style="color:#FF5FA2">●</span> N. Am. '
     '<span style="color:#A98BFF">●</span> Oceania</p>\n'
     '<div style="border-top:1px solid #3A4B5A;padding-top:16px;display:flex;flex-direction:column;gap:6px">\n'
     '<p style="font-size:32px;font-weight:600;color:#FFFFFF">Stat4Sight</p>\n'
     '<p style="font-size:26px;line-height:1.35;color:#D3DCE2">Elif Zarife Yıldırım · Rojbin Bağatur</p>\n'
     '<p style="font-size:26px;line-height:1.35;color:#D3DCE2">Zehra İklil Canatar · Yazel Sude Özyürek</p>\n'
     '<p style="font-size:24px;line-height:1.35;color:#B9C6CF">Kırıkkale University, Department of Statistics</p>\n</div>\n</div>\n')
s += kapat("Hello, we are Stat4Sight from Kırıkkale University. Every country is moving from large families to small ones. "
           "Our project asks two things: is it the same journey everywhere, and what sets its timing?")
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
             '<span style="color:#FF8A3D">Q1</span> Same path, or only different timing? · <span style="color:#FF8A3D">Q2</span> At the turning point: money or school?',
             kanca)
huni = '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-around">\n'
for w, g, yazi, renk, sag in [(380, "#FF6A2B, #FF8A5C", "555 rows", "#FF8A5C", "362.9 bn ✗ counted ~45×"),
                              (162, "#FF4F7A, #FF7A9A", "237", "#E8EEF2", "countries · 8.09 bn ✓ = World"),
                              (137, "#7A6CFF, #9B8CFF", "200", "#FFFFFF", "<b>our sample</b> · 99.98% of people"),
                              (84, "#3987e5, #5FA0F0", "112", "#E8EEF2", "turning point seen 1952–2013 · 69%"),
                              (60, "#2FB7FF, #6FD0FF", "66", "#E8EEF2", "+ income and schooling data · 67%")]:
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
           "still averaged six children. The fair question is <b>when</b> each country changes.")
s += DIPNOT.format("UN World Population Prospects 2024 · 1950–2023 estimates; dashed = UN projections · every excluded place is listed by name (excluded_places.csv)")
s += kapat(f"In 2023, women in the Republic of Korea had {kor:.2f} children on average; women in Niger had {nij:.2f}. "
           "In 1950, only 3 of 200 countries were below replacement; by 2023 it was 103. So we asked: do countries follow the same path, "
           "and when they reach the turning point, are they rich, or are their young women in school?\n\n"
           "Our data is UN World Population Prospects 2024. Summing every row of the file gives 363 billion people, because regions repeat countries; "
           "countries alone give the correct 8.09 billion. We keep the 200 countries above 100,000 people, 99.98 percent of the world, "
           "and list every place we leave out. Values after 2023 are UN projections, always drawn dashed.")
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
           "94 percent; a level shift with the same number of parameters reaches only 87. In backtests from 1983, 1993 and 2003, "
           "the shared curve had the smallest typical error twenty years ahead.\n\nOn the map, the clock runs from Europe to Africa, and a Kruskal–Wallis test "
           "confirms that regions turn at different times. In 2023, Nigeria is at its turning point, Türkiye passed it about forty years ago, Japan about ninety.")
yaz("clock", s)

# =============== Slayt 3: Para mı, okul mu? · solda grafik + 2 kart, sağda tablo kartı ===============
ulkeler = [("Bangladesh", "Bangladesh"), ("India", "India"), ("Republic of Korea", "Rep. of Korea"), ("Indonesia", "Indonesia"),
           ("Türkiye", "Türkiye"), ("Iran (Islamic Republic of)", "Iran"), ("Brazil", "Brazil"), ("Mexico", "Mexico"),
           ("Saudi Arabia", "Saudi Arabia")]
lg = np.log(po["gelir"]); gmin, gmax = lg.min(), lg.max()
emin, emax = po["egitim"].min(), po["egitim"].max()
s = bolum_ac("money", "3 · Money or school?", "Money does not set the clock; schooling is steadier",
             "66 countries with a turning point in 1952–2013 · Maddison income · Barro–Lee schooling of women aged 25–34")
s += '<div style="display:grid;grid-template-columns:860px 1fr;gap:16px">\n<div style="display:flex;flex-direction:column;gap:16px">\n'
s += kart("Where 66 countries stood at their turning point",
          gorsel("spread", "Dot plot of 66 countries at their turning point, coloured by region: income widely spread from Bangladesh to Saudi Arabia, young women’s schooling more tightly grouped; Türkiye above typical in income, below in schooling", 822, 296))
s += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">\n'
s += kart("Spread vs world spread",
          cubuk("Income", 0.64, "0.64", "linear-gradient(90deg, #B04A20, #FF8A3D)", 300, 130) + "\n"
          + cubuk("Schooling", 0.48, "0.48", "linear-gradient(90deg, #3987e5, #3FC1FF)", 300, 130, True) + "\n"
          + '<p style="font-size:24px;line-height:1.3;color:#C9D4DC">Schooling <b>1.34×</b> tighter<br>95% CI 1.09–1.67</p>')
s += kart("Error guessing the year",
          cubuk("Income", 14.0, "14.0", "linear-gradient(90deg, #B04A20, #FF8A3D)", 16, 130) + "\n"
          + cubuk("Schooling", 9.5, "9.5", "linear-gradient(90deg, #3987e5, #3FC1FF)", 16, 130) + "\n"
          + cubuk("Calendar", 9.5, "9.5", "#5E6873", 16, 130) + "\n"
          + '<p style="font-size:24px;line-height:1.3;color:#C9D4DC">years · income worse, <b>p &lt; 0.001</b><br>schooling = calendar, p = 0.75</p>')
s += '</div>\n</div>\n'
tablo = ('<div style="display:grid;grid-template-columns:1.5fr 0.8fr 1.1fr 0.8fr;gap:5px">'
         + baslik_satiri(["Country", "Year", "Income", "School"], ["left", "right", "right", "right"]))
for anahtar, ad in ulkeler:
    r = po.loc[anahtar]; tr_ = anahtar == "Türkiye"
    tablo += hucre(ad, "#3987e5" if tr_ else "#1E2E3C", kalin=tr_, sol=True) + hucre(str(int(round(r["t0"]))), "#1E2E3C", kalin=tr_)
    tablo += hucre(f"${r['gelir']:,.0f}", karis("#2A1E1A", "#D95926", (np.log(r["gelir"]) - gmin) / (gmax - gmin)), kalin=tr_)
    tablo += hucre(f"{r['egitim']:.1f}", karis("#16263A", "#3987e5", (r["egitim"] - emin) / (emax - emin)), kalin=tr_)
tablo += hucre("<i>Median of 66</i>", "#253645", sol=True) + hucre("–", "#253645")
tablo += hucre(f"<i>${po['gelir'].median():,.0f}</i>", "#253645") + hucre(f"<i>{po['egitim'].median():.1f}</i>", "#253645") + "</div>\n"
tablo += ('<div style="flex:1"></div>\n<p style="font-size:24px;line-height:1.3;color:#9FB0BD"><span style="color:#FF8A3D">■</span> richer · '
          '<span style="color:#5FA0F0">■</span> more schooling · GDP per person (2011 $) · school: years</p>')
s += kart("Nine countries at their turning point", tablo)
s += '</div>\n'
s += anlam("Countries began their decline at incomes from $1,100 to $24,000 a person: no wealth threshold sets the clock. Schooling was "
           "more alike but did not predict the year either. These are patterns, not causes.")
s += DIPNOT.format("Leave-one-out thresholds · paired Wilcoxon tests · bootstrap CI (5,000 resamples) · country-level association, not causation")
s += kapat("Next we asked what countries looked like at their turning point. We linked 66 countries that turned between "
           "1952 and 2013 to Maddison income data and Barro–Lee schooling of women aged 25 to 34.\n\nIncome varied hugely: Bangladesh turned at about "
           "1,100 dollars per person, Saudi Arabia at 24,000. Schooling was more similar: scaled by each measure’s world spread, it is 1.34 times "
           "more concentrated, with a bootstrap interval from 1.09 to 1.67.\n\nThen the honest test: using the typical level as a threshold to predict "
           "the turning-point year. Income misses by 14 years, worse than simply guessing the typical year. Schooling misses by 9.5 years, but so "
           "does the calendar.\n\nSo money does not set the clock. Schooling is a steadier marker, but not a timer.")
yaz("money", s)

# =============== Slayt 4: Türkiye · solda 2 grafik kartı, sağda tablo + sınırlar kartı ===============
tr = df[df["Location"] == "Türkiye"].set_index("Time")
yillar = [1950, 1982, 2023, 2047, 2100]
satirlar = [("People (M)", tr["TPopulation1July"] / 1000, "{:.1f}", "#3987e5"), ("Children", tr["TFR"], "{:.2f}", "#d95926"),
            ("Life exp.", tr["LEx"], "{:.1f}", "#199e70"), ("Median age", tr["MedianAgePop"], "{:.1f}", "#9085e9"),
            ("Infant deaths", tr["IMR"], "{:.0f}", "#d55181")]
poT = po.loc["Türkiye"]; gelir_alt = int((po["gelir"] < poT["gelir"]).sum()); egitim_ust = int((po["egitim"] > poT["egitim"]).sum())
s = bolum_ac("turkiye", "4 · Türkiye, limits and ethics", "Türkiye turned early for its schooling; its future is a range",
             f"Turning point 1982 · richer than {gelir_alt} of 66 countries at their turning points, but less schooling than {egitim_ust}")
s += '<div style="display:grid;grid-template-columns:860px 1fr;gap:16px">\n<div style="display:flex;flex-direction:column;gap:16px">\n'
s += kart("Population, with UN prediction intervals",
          gorsel("pop", "Türkiye population: UN estimate to 2023, Medium projection peaking in 2047 at 91.4 million and 65.3 million in 2100, with 80% and 95% prediction intervals widening to 26–125 million", 822, 232))
s += kart("Three clocks: children per woman",
          gorsel("three", "Children per woman 1950–2100 for Japan, Türkiye, Nigeria and the world; dots mark turning points: Türkiye 1982, Nigeria 2025; Japan turned about 1935, before the data", 822, 232))
s += '</div>\n<div style="display:flex;flex-direction:column;gap:16px">\n'
bes = '<div style="display:grid;grid-template-columns:1.55fr 1fr 1fr 1fr 1fr 1fr;gap:5px">\n<p></p>'
for y in yillar:
    bes += (f'<p style="font-size:24px;line-height:1.2;font-weight:600;color:{"#4FB3FF" if y == 1982 else "#9FB0BD"};padding:1px 8px;'
            f'text-align:right">{y}{"*" if y > 2023 else ""}</p>')
for ad, seri, bicim, renk in satirlar:
    v = seri.loc[yillar].values; lo, hi = v.min(), v.max()
    bes += f'<p style="font-size:24px;line-height:1.3;color:{renk};font-weight:600;padding:3px 4px">{ad}</p>'
    for y, x in zip(yillar, v):
        bes += hucre(bicim.format(x), karis("#16222E", renk, 0.15 + 0.85 * (x - lo) / (hi - lo)),
                     ek="border:1px dashed #9FB0BD;font-style:italic;" if y > 2023 else "")
bes += (f'</div>\n<p style="font-size:24px;line-height:1.3;color:#9FB0BD">1982 = turning point · * UN projection (dashed) · '
        f'{"deeper" if ACIK else "brighter"} = higher</p>')
s += kart("Türkiye at five moments", bes)
iddia = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px 20px">\n'
for m in ["Causes: these are patterns", "Individual-level claims", "That UN figures are observed",
          "Results for pre-1950 turns", "That further along is better", "That projections are forecasts"]:
    iddia += f'<p style="font-size:24px;line-height:1.3;color:#C9D4DC">· {m}</p>\n'
iddia += '</div>'
s += kart("What we do not claim", iddia, "flex:1;border-left:5px solid #d95926")
s += '</div>\n</div>\n'
s += anlam("Türkiye’s decline began while young women’s schooling was still low (3.6 vs a typical 5.5 years). Its population likely peaks "
           "near 2047; for 2100, plan with the range (26–125 million), not one number.")
s += DIPNOT.format("Guided by the ASA Ethical Guidelines for Statistical Practice (2022) · UN WPP 2024, Medium and probabilistic variants · infant deaths per 1,000 births")
s += kapat(f"Türkiye turned around 1982. It was richer than {gelir_alt} of these 66 countries at their turning points, but its young women had "
           f"less schooling than {egitim_ust} of them.\n\nThe UN projects Türkiye’s population to peak in 2047 at 91 million. By 2100 its 95 percent "
           "interval runs from 26 to 125 million, so we show a range, not a number.\n\nOur limits: these are country-level patterns, not causes, and "
           "they say nothing about individual women. Many UN figures are themselves model estimates where registration is weak. Countries that turned "
           "before 1950 are outside the money-or-school test. And the clock is not a race: being further along is not better.")
yaz("turkiye", s)

if ACIK:   # kaynakça elle yazılı: mavi sürümden renkleri çevirerek kopyala
    yaz("references", (KOK / "sunum/slaytlar_kaynak/slides/references.html").read_text())
print("yazıldı: cover, question, clock, money, turkiye" + (", references (açık)" if ACIK else ""))
