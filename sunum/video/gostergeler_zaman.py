"""Gösterge (çerçeve + spot ışığı) zamanlarını SON videonun kendi sesinden hesaplar (30 Ekim).
Önceki yol (ilk videonun zamanlarını yeni kesimlere taşımak) kesimler değişince kayıyordu ("On the map" geç yanıyordu).
Kart içi odak (30 Ekim akşam, kullanıcı: "ilgili kart gösterilecek ve kartın içinde neyden bahsediliyorsa onlar da ayrı ayrı
konuşurken parlasın"): konuşulan kart sarı çerçeveyle işaretli kalır; kartın içinde o an söylenen satır, çubuk, panel ya da
yazı ayrıca ince bir sarı çerçeveyle parlar ve spot ışığı o parçaya daralır (kartın geri kalanı öteki kartlar kadar kararır).
Çalıştırma (mlx-whisper, soundfile ve scipy kurulu bir Python ortamıyla; Whisper sadece kelime zamanları için):
  python sunum/video/gostergeler_zaman.py <son_ses.wav> [kutular.json] [parcalar.json] [--zaman <onbellek.json>]
  kutular.json: kartların yeri (varsayılan sunum/video/kutular.json); parcalar.json: kart içi satır/yazıların yeri
  (sunum/video/parcalar_olc.py ölçer, varsayılan sunum/video/parcalar.json). Grafik resimlerinin içindeki bölgeler aşağıda
  RESIM sözlüğünde, slayt pikseliyle (ön izlemeden okundu). --zaman: Whisper kelime zamanları bu dosyaya yazılır/okunur.
Okur: sunum/video/kurgu_plani_30ekim.json (sayfa sınırları, bekleme) ve sunum/video/gostergeler_30ekim.json (animasyon ayarı korunur).
Yazar: sunum/video/gostergeler_30ekim.json (gostergeler = çerçeveler, isik = spot ışığının sırayla geçtiği dikdörtgenler)."""
import sys, json, difflib
from pathlib import Path
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
sys.path.insert(0, str(Path(__file__).resolve().parent))
import metin_hizala as u

arg = sys.argv[1:]
onbellek = None
if "--zaman" in arg:
    i = arg.index("--zaman"); onbellek = Path(arg[i + 1]); del arg[i:i + 2]
ses_yol = arg[0]
kut = json.load(open(arg[1] if len(arg) > 1 else "sunum/video/kutular.json"))
par = json.load(open(arg[2] if len(arg) > 2 else "sunum/video/parcalar.json"))
plan = json.load(open("sunum/video/kurgu_plani_30ekim.json"))["parcalar"][0]["bolumler"]
eski = json.load(open("sunum/video/gostergeler_30ekim.json"))
# kaynak saniyesi → videodaki saniye (sayfa sınırları için)
h, t = [], 0.0
for b in plan:
    d = b.get("sessiz") or (b["son"] - b["bas"]); h.append((t, b)); t += d
def cikti(k):
    for a, b in h:
        if "sessiz" not in b and b["bas"] <= k < b["son"]: return a + k - b["bas"]
    return min([a for a, b in h if "sessiz" not in b and b["bas"] >= k], default=t)
bekleme = [(a, a + b["sessiz"]) for a, b in h if "sessiz" in b][0]
SAYFA = {"question": (cikti(19.7), cikti(86.06)), "clock": (cikti(86.06), cikti(161.85)),
         "money": (cikti(161.85), cikti(272.95)), "turkiye": (cikti(272.95), cikti(373.6))}

if onbellek and onbellek.exists():
    hyp = [tuple(x) for x in json.loads(onbellek.read_text())]
else:
    import mlx_whisper
    x, sr = sf.read(ses_yol, dtype="float32"); x = x.mean(1)
    r = mlx_whisper.transcribe(resample_poly(x, 1, sr // 16000).astype(np.float32), path_or_hf_repo=u.MODEL, language="en", word_timestamps=True,
                               condition_on_previous_text=False, initial_prompt="Stat4Sight, Kırıkkale, Türkiye, SITAR, Niger, UN, GDP.")
    hyp = [(tk, w["start"]) for s in r["segments"] for w in s["words"] for tk in u.duz(w["word"])]
    if onbellek: onbellek.write_text(json.dumps(hyp))
bek = [tk for c in u.cumleler() for tk in u.duz(u.beklenen(c[4]))]
zaman = [None] * len(bek)
for blk in difflib.SequenceMatcher(None, bek, [tk for tk, _ in hyp], autojunk=False).get_matching_blocks():
    for d in range(blk.size): zaman[blk.a + d] = hyp[blk.b + d][1]
bilinen = [i for i, z in enumerate(zaman) if z is not None]
bset = set(bilinen)
for i in range(len(zaman)):
    if zaman[i] is None:
        o = max([j for j in bilinen if j < i], default=None); s_ = min([j for j in bilinen if j > i], default=None)
        zaman[i] = zaman[s_] if o is None else zaman[o] if s_ is None else zaman[o] + (zaman[s_] - zaman[o]) * (i - o) / (s_ - o)
# Kısa parçalarla ayrıca doğrulanan başlangıçlar: hizalama bu üç ifadede 0,25–0,7 sn kayıyordu. KAYNAK kayıttaki saniye
# olarak yazılır, plana göre videodaki ana çevrilir (kesim değişince kaymasın; ilk değerler 30 Ekim v3: 33,3 / 135,85 / 119,9).
KESIN = {"So we asked": 38.03, "As a threshold": 171.08, "In 2023, Nigeria": 141.24}
ZAYIF = []
def bul(ifade):
    if ifade in KESIN: return cikti(KESIN[ifade])
    w = u.duz(u.beklenen(ifade)); n = len(w)
    yer = [i for i in range(len(bek) - n + 1) if bek[i:i + n] == w]
    assert len(yer) == 1, (ifade, len(yer))
    i = yer[0]
    if i not in bset: ZAYIF.append(ifade)   # ilk kelime doğrudan eşleşmedi, komşulardan tahmin
    return zaman[i]

# --- yerler (slayt CSS pikseli, 1920x1080) → çıktı videosunun 1920x1080 pikseli ---
K = 1920 / 2818   # kayıt 2880x1800, slayt 1,5 kat; kesim x 31, y 90, 2818 genişlik
def cevir(x, y, w, h, pay):
    x, y, w, h = x - pay, y - pay, w + 2 * pay, h + 2 * pay
    return {"x": round((x * 1.5 - 31) * K, 1), "y": round(y * 1.5 * K, 1), "w": round(w * 1.5 * K, 1), "h": round(h * 1.5 * K, 1)}
def birlesim(*kutular):
    x0 = min(k["x"] for k in kutular); y0 = min(k["y"] for k in kutular)
    x1 = max(k["x"] + k["w"] for k in kutular); y1 = max(k["y"] + k["h"] for k in kutular)
    return {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}
def kart(sayfa, ad):
    return [k for k in kut[sayfa] if k["ad"].startswith(ad)][0]
# Animasyonun son sahnesi (Nijerya/Türkiye/Japonya etiketleri): klibin 1920x1080 pikseli, kartta 147,264.2 noktasında 526 genişlikte
def anim(x0, y0, x1, y1, o=526 / 1920):
    return {"x": 147 + x0 * o, "y": 264.2 + y0 * o, "w": (x1 - x0) * o, "h": (y1 - y0) * o}
def xy(x0, y0, x1, y1): return {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}
RESIM = {   # grafik resimlerinin içindeki bölgeler (ön izleme üzerinde ızgarayla okundu, slayt pikseli)
    "question": {"proj": xy(482, 270, 758, 470),           # bölge grafiği: UN projeksiyonu (gölgeli alan, kesikli çizgiler)
                 "hist_1950": xy(228, 579, 386, 810), "hist_2023": xy(576, 579, 736, 810)},
    "clock": {"avrupa": xy(1072, 293, 1205, 352), "afrika": xy(1056, 345, 1178, 502),
              "nijerya": anim(955, 368, 1415, 465), "turkiye_a": anim(1045, 532, 1465, 625), "japonya": anim(1378, 662, 1797, 755)},
    "money": {"x_saglik": xy(1108, 687, 1538, 711), "ust_yazi": xy(924, 284, 1341, 333), "rho": xy(924, 377, 1021, 403)},
    "turkiye": {"x_ilac": xy(246, 634, 1029, 656), "cizim": xy(236, 304, 1036, 602),
                "tepe": xy(1461, 301, 1639, 344), "aralik": xy(1634, 285, 1757, 427)},
}
def parca(sayfa, ad):
    if ad in RESIM.get(sayfa, {}): return RESIM[sayfa][ad]
    if ad == "bt_ortak": return birlesim(*[par["clock"][k] for k in ("bt_shared", "bt_049", "bt_038", "bt_041")])
    if ad == "hata_okul_takvim": return birlesim(par["money"]["hata_okul"], par["money"]["hata_takvim"])
    if ad == "cip_iki": return birlesim(par["turkiye"]["cip_timing"], par["turkiye"]["cip_hiv"])
    if ad == "cip_fert2": return par["turkiye"]["cip_fert"]
    if ad == "sol_sutun": return birlesim(*[kart("money", k) for k in ("kart: Q2 · Error", "kart: Q2 · Where", "kart: Once 1950")])
    return par[sayfa][ad]

# --- konuşma sırası: (sayfa, kart ya da tek parça, başlangıç ifadesi, bitiş ifadesi, [(kart içi parça, başlangıç, bitiş)], kart çerçevesi) ---
# bitiş None: sayfa sonu (kart) ya da kartın sonu (parça); "BEKLEME": animasyonun büyüdüğü an. Tek parça (dipnot, alt başlık): ince çerçeve.
G = [
 ("question", "kanca", "In 2023, the total fertility rate", "The histograms show",
  [("kanca_kore", "In 2023, the total fertility rate", "and 6.06 in Niger"), ("kanca_nijer", "and 6.06 in Niger", None)], True),
 ("question", "kart: How the 200", "The histograms show", "So we asked",
  [("hist_1950", "in 1950, only 3", "by 2023, 103"), ("hist_2023", "by 2023, 103", None)], True),
 ("question", "Q satırı", "So we asked", "Our data is",
  [("q1", "So we asked", "and what moves"), ("q2", "and what moves", "or health"), ("q3", "or health", None)], False),
 ("question", "dip_veri", "Our data is", "In the funnel", [], None),
 ("question", "kart: From raw file", "In the funnel", "list every place",
  [("huni_555", "In the funnel", "countries alone give"), ("huni_237", "countries alone give", "We keep 200"),
   ("huni_200", "We keep 200", None)], True),
 ("question", "dip_liste", "list every place", "and draw UN projections dashed", [], None),
 ("question", "kart: Total fertility rate by region", "and draw UN projections dashed", None,
  [("proj", "and draw UN projections dashed", None)], True),

 ("clock", "kart: Variation explained", "Our first try fitted", "but gave implausible",
  [("r2_ayri", "Our first try fitted", None)], True),
 ("clock", "dip_16", "but gave implausible", "So we borrowed", [], None),
 ("clock", "dip_sitar", "So we borrowed", "one shared S-curve", [], None),
 ("clock", "alt_egri", "one shared S-curve", "Watch what happens", [], None),
 ("clock", "kart: Shift each country", "Watch what happens", "BEKLEME", [], True),
 ("clock", "kart: Variation explained", "By calendar year", "and it predicted best",
  [("r2_takvim", "By calendar year", "Shifted to their own"), ("r2_zaman", "Shifted to their own", None)], True),
 ("clock", "kart: Backtest", "and it predicted best", "On the map", [("bt_ortak", "and it predicted best", None)], True),
 ("clock", "kart: The clock on a map", "On the map", "In 2023, Nigeria",
  [("avrupa", "the clock runs from Europe", "to Africa"), ("afrika", "to Africa", None)], True),
 ("clock", "kart: Shift each country", "In 2023, Nigeria", None,
  [("nijerya", "In 2023, Nigeria", "Türkiye passed it"), ("turkiye_a", "Türkiye passed it", "Japan about ninety"),
   ("japonya", "Japan about ninety", None)], True),

 ("money", "sol_sutun", "First, income or education", "GDP per person", [], True),
 ("money", "kart: Q2 · Where", "GDP per person", "As a threshold", [("yer_gelir", "GDP per person", None)], True),
 ("money", "kart: Q2 · Error", "As a threshold", "Women’s education",
  [("hata_gelir", "As a threshold", "worse than guessing"), ("hata_takvim", "worse than guessing", None)], True),
 ("money", "kart: Q2 · Where", "Women’s education", "but no better than", [("yer_okul", "Women’s education", None)], True),
 ("money", "kart: Q2 · Error", "but no better than", "That no is a result", [("hata_okul_takvim", "but no better than", None)], True),
 ("money", "alt_q3", "and it led us", "We measured a second clock", [], None),
 ("money", "kart: Q3 · Two clocks", "We measured a second clock", "We screened",
  [("x_saglik", "We measured a second clock", "Above the line"), ("ust_yazi", "Above the line", "and the two clocks"),
   ("rho", "and the two clocks", None)], True),
 ("money", "dip_tarama", "We screened", "So income does not set the clock", [], None),
 ("money", "bant", "So income does not set the clock", "But first is not", [], True),
 ("money", "dip_neden", "But first is not", None, [], None),

 ("turkiye", "alt_q4", "So, one more question", "We ran three tests", [], None),
 ("turkiye", "kart: Q4", "We ran three tests", "but does not settle it",
  [("testler", "We ran three tests", "Two could not tell"), ("cip_iki", "Two could not tell", "The third is"),
   ("cip_fert", "The third is", "in the 1940s"), ("x_ilac", "in the 1940s", "Where they saved"),
   ("cizim", "Where they saved", "about ten percent"), ("satir_10", "about ten percent", "This supports"),
   ("cip_fert2", "This supports", None)], True),
 ("turkiye", "kart: What we do not claim", "but does not settle it", "Türkiye’s health clock",
  [("iddia_neden", "but does not settle it", None)], True),
 ("turkiye", "kart: Türkiye", "Türkiye’s health clock", "Our limits",
  [("tr_baslik", "Türkiye’s health clock", "Its population likely"), ("tepe", "Its population likely", "for 2100 we show"),
   ("aralik", "for 2100 we show", None)], True),
 ("turkiye", "kart: What we do not claim", "Our limits", None,
  [("iddia_birey", "these are country patterns", "and the clock is not"), ("iddia_yaris", "and the clock is not", None)], True),
]
KART_ONCE, PARCA_ONCE = 0.25, 0.15     # çerçeve kelimeden bu kadar önce belirir (göz sesi biraz önden izler)
KART = {"kalin": 5, "yaricap": 14, "gecis": 0.3}
PARCA = {"kalin": 3.5, "yaricap": 8, "gecis": 0.2}
cerceve, isik = [], []
for sayfa, hedef, ifade, son_ifade, parcalar, kart_cercevesi in G:
    b = max(bul(ifade) - KART_ONCE, SAYFA[sayfa][0] + 0.25)
    if son_ifade == "BEKLEME": s = bekleme[0]
    elif son_ifade: s = bul(son_ifade) - KART_ONCE
    else: s = SAYFA[sayfa][1] - 0.3
    if ifade.startswith("By calendar"): b = max(b, bekleme[1] + 0.1)
    s = min(s, SAYFA[sayfa][1] - 0.3)
    tek = kart_cercevesi is None
    yer_css = kart(sayfa, hedef) if hedef.startswith(("kart:", "kanca", "Q satırı", "bant")) else parca(sayfa, hedef)
    yer = cevir(yer_css["x"], yer_css["y"], yer_css["w"], yer_css["h"], 4 if tek else 6)
    stil = PARCA if tek else KART
    if kart_cercevesi is not False:
        cerceve.append({"sayfa": sayfa, "tur": "parca" if tek else "kart", "hedef": hedef, "ifade": ifade, "bas": round(b, 2), "son": round(s, 2), **yer, **stil})
    print(f"{b:6.1f}–{s:6.1f}  {hedef[:34]:34s} ← {ifade}")
    # kart içi parçalar: zamanlar, sonra spot ışığının sırası (parça yokken kartın kendisi)
    pz = []
    for ad, pb_ifade, ps_ifade in parcalar:
        pb = max(bul(pb_ifade) - PARCA_ONCE, b)
        ps = (bul(ps_ifade) - PARCA_ONCE) if ps_ifade else s
        pz.append([ad, pb, min(ps, s), pb_ifade])
    for i in range(len(pz) - 1):            # art arda parçalar arasında boşluk kalmasın
        if pz[i + 1][1] - pz[i][2] < 0.4: pz[i][2] = pz[i + 1][1]
    an = b
    for ad, pb, ps, pb_ifade in pz:
        if pb - an > 0.05: isik.append({"bas": round(an, 2), "son": round(pb, 2), **yer, "yaricap": stil["yaricap"]})
        y = parca(sayfa, ad); py = cevir(y["x"], y["y"], y["w"], y["h"], 4)
        cerceve.append({"sayfa": sayfa, "tur": "parca", "hedef": f"{hedef} › {ad}", "ifade": pb_ifade, "bas": round(pb, 2), "son": round(ps, 2), **py, **PARCA})
        isik.append({"bas": round(pb, 2), "son": round(ps, 2), **py, "yaricap": PARCA["yaricap"]})
        print(f"   {pb:6.1f}–{ps:6.1f}  ({ps - pb:4.1f} sn)  › {ad}")
        an = ps
    if s - an > 0.05: isik.append({"bas": round(an, 2), "son": round(s, 2), **yer, "yaricap": stil["yaricap"]})
if ZAYIF: print("ilk kelimesi komşulardan tahmin edilen ifadeler:", ZAYIF)
kisa = [c for c in cerceve if c["son"] - c["bas"] < 0.6]
if kisa: print("UYARI 0,6 sn'den kısa:", [(c["hedef"], round(c["son"] - c["bas"], 2)) for c in kisa])
an = dict(eski["animasyon"]); an["dondur"] = True
json.dump({"gostergeler": cerceve, "isik": isik, "animasyon": an}, open("sunum/video/gostergeler_30ekim.json", "w"), ensure_ascii=False, indent=1)
print(f"çerçeve {len(cerceve)}, ışık dikdörtgeni {len(isik)}")
