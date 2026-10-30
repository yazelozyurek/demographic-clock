"""30 Ekim kaydının kurgu planı, sürüm 2 (takım geri bildirimi: yarım 'So'lar, tekrar, duraklamalar, sayfa geçişleri, animasyon).
Çalıştırma: python sunum/video/kurgu_plani_30ekim_uret.py <db.npy> <eski_plan.json> <eski_gostergeler.json> <kutular.json> <yazi.json>
Sürüm 3 (kullanıcı: "nefes, takılma, bekleme kalmasın, akış pürüzsüz olsun"): nefesler susturulup çıkarılır, duraklamalar 0,28 sn, sayfa geçişleri ~0,5 sn.
- db.npy: kaynak kaydın 10 ms'lik ses düzeyi (dBFS); eski_*: sürüm 1 plan ve gösterge listesi (zamanları yeni plana taşınır).
Yazar: sunum/video/kurgu_plani_30ekim.json ve sunum/video/gostergeler_30ekim.json (göstergeler + büyüyen animasyon)."""
import sys, json, numpy as np
from pathlib import Path
db = np.load(sys.argv[1]); eski_plan = json.load(open(sys.argv[2])); eski_g = json.load(open(sys.argv[3])); kut = json.load(open(sys.argv[4]))
kelimeler = json.load(open(sys.argv[5]))["kelimeler"]   # Whisper kelime zamanları (kaynak kayıt)
KAYNAK = "~/Desktop/Ekran Kaydı 2026-10-30 12.24.24.mov"
BEKLE, GIF_BAS = 11.5, 0.0          # animasyon beklemesi (sn); video klibi takvim görünümüyle başlıyor
# (bas, son, kısaltma bu andan sonra) — elle seçilen bölümler; sayfa geçişleri solma efektinden hemen önce birleşiyor
B = [(3.2, 18.78, 15.0, "kapak (animasyon bitene kadar kısaltma yok)"),
     (19.5, 50.95, 0, "2. sayfaya geçiş (solma 19,55–19,85) … 'Our data is … 2024.'"),
     (65.75, 85.25, 0, "huni cümlesi ('the funnel…'; 61,6'daki 'In' parçası ilk denemenin 'billion' sonunu taşıdığı için çıkarıldı) … 'dashed.'"),
     (86.0, 90.55, 0, "3. sayfaya geçiş (~86,05) … 'each country'"),
     (90.88, 100.85, 0, "'separately' (kullanıcı geri istedi; yükseltme yok, önündeki 0,6 sn boşluk kısaldı) … 'nine children.'"),
     (108.35, 125.6, 0, "'So we borrowed…' (103,5'teki yarım 'So, we' çıkarıldı) … 'Watch what happens…'"),
     ("BEKLE",),
     (125.6, 148.6, 0, "'By calendar year…' … 'Japan about ninety.'"),
     (161.85, 177.85, 0, "4. sayfa: 'First, income…' ikinci denemesi"),
     (188.65, 192.4, 0, "'Women's education…'"),
     (200.45, 208.0, 0, "'That no is a result…' … 'does health come first?'"),
     (214.1, 221.0, 0, "'We measured a second clock…' (208,5'teki yarım deneme çıkarıldı)"),
     (228.85, 260.5, 0, "'Above the line…' … 'sun rise.'"),
     (272.95, 277.1, 0, "5. sayfa: 'So, one more question…' (4. sayfadaki fazladan 'So,' çıkarıldı)"),
     (281.2, 298.6, 0, "'We ran three tests…' … 'gained most.'"),
     (320.0, 333.3, 0, "'Where they saved more lives…' ikinci denemesi"),
     (342.1, 372.75, 0, "'This supports…' … 'not a race.'"),
     (373.55, 391.2, 0, "kaynakçaya geçiş (solma 373,6–373,8) … 'Thank you.' + 1,6 sn kapanış")]
SUSTUR = [[18.75, 20.1], [85.2, 86.5], [372.65, 374.15], [389.95, 391.2]]   # sonuncusu: kaydı durdururken tuş sesi
ESIK_DB, KISA_ADA, UZUN, KALAN = -58, 0.10, 0.45, 0.3   # -52 konuşmayı da kesiyordu (75 yerde), -58 güvenli
NEFES_DB, NEFES_SURE = -50, 0.7   # bu kadar alçak ve kısa, hiçbir kelimeye denk gelmeyen ses adası nefes sayılır
ses = db > ESIK_DB
def kelime_payi(a, b):   # a–b aralığının Whisper kelimeleriyle örtüşen payı
    return sum(max(0, min(b, w["e"]) - max(a, w["s"])) for w in kelimeler) / max(b - a, 1e-6)
# 0,15 sn'den kısa ses adaları (nefes, tık) suskunluk sayılır
i = 0
while i < len(ses):
    if ses[i]:
        j = i
        while j < len(ses) and ses[j]: j += 1
        if (j - i) / 100 < KISA_ADA and db[i:j].max() < -50 and kelime_payi(i / 100, j / 100) < 0.25: ses[i:j] = False   # kısa kelimeler korunur
        i = j
    else: i += 1
NEFESLER = []
i = 0
while i < len(ses):
    if ses[i]:
        j = i
        while j < len(ses) and ses[j]: j += 1
        a, b = i / 100, j / 100
        once_sessiz = not ses[max(0, i - 10):i].any()   # önünde en az 0,1 sn suskunluk (30 Ekim: 'everywhere?' ve 'million.' kuyruğu nefes sanılmıştı)
        if b - a <= NEFES_SURE and np.median(db[i:j]) < NEFES_DB and kelime_payi(a, b) < 0.25 and once_sessiz:
            ses[i:j] = False; NEFESLER.append([round(a - 0.02, 2), round(b + 0.02, 2)])
        i = j
    else: i += 1
SUSTUR = SUSTUR + NEFESLER
def suskunluklar(a, b):
    out = []; i = int(a * 100)
    while i < int(b * 100):
        if not ses[i]:
            j = i
            while j < int(b * 100) and not ses[j]: j += 1
            if (j - i) / 100 >= UZUN and i > int(a * 100) and j < int(b * 100): out.append((i / 100, j / 100))
            i = j
        else: i += 1
    return out
bolumler = []
for b in B:
    if b[0] == "BEKLE":
        bolumler.append({"sessiz": BEKLE, "goruntu_bas": 113.0, "not": "animasyon beklemesi (görüntüyü büyüyen animasyon kaplıyor)"}); continue
    a, z, kis, not_ = b
    parca = [(a, z)]
    if kis is not None:
        yeni, cur = [], a
        for sa, sz in suskunluklar(a, z):
            if sa < kis or any(not (sz < m0 or sa > m1) for m0, m1 in SUSTUR): continue
            yeni.append((cur, sa + 0.13)); cur = sz - (KALAN - 0.13)   # konuşma başlangıcı tarafında pay daha geniş
        parca = yeni + [(cur, z)]
    for k, (pa, pz) in enumerate(parca):
        bolumler.append({"bas": round(pa, 3), "son": round(pz, 3), "not": not_ if k == 0 else "duraklama kısaltıldı"})
# Kuyruk payı (30 Ekim, kullanıcı: 'race' yarım duyuluyor): son ünsüz ('s', 'f', 'th') -58 dB'nin altında söner, 0,13 sn'lik pay
# yetmeyebiliyor. Her kesimde ses, o yerin gürültü tabanının 5 dB üstünde ve sönmeye devam ettiği sürece (en fazla 0,3 sn) korunur;
# kelime başları için aynısı geriye doğru. Yeni bir ses başlarsa (düzey 4 dB yükselirse) durulur.
def kuyruk(i, adim, sinir):
    yer = slice(i, i + 80) if adim > 0 else slice(max(0, i - 80), i)
    esik = max(np.percentile(db[yer], 10) + 5, -72); k = i if adim > 0 else i - 1; n = 0
    en_az = db[k]
    while n < 30 and (k < sinir if adim > 0 else k >= sinir) and esik < db[k] < -50 and db[k] <= en_az + 4:
        en_az = min(en_az, db[k]); k += adim; n += 1
    if n < 3: return 0
    bas_ = db[k - adim * n: k - adim * n + 3 * adim: adim].max(); son_ = db[k - 3 * adim: k: adim].min() if adim > 0 else db[k + 1: k + 4].min()
    taban = esik - 5
    return n if bas_ >= taban + 8 and bas_ - son_ >= 6 else 0   # düz oda gürültüsü kuyruk sayılmaz (duraklamayı uzatırdı)
gercek = [d for d in bolumler if "sessiz" not in d]
UZATILAN = []
for x, y in zip(gercek, gercek[1:]):
    if abs(y["bas"] - x["son"]) < 0.02 or y["bas"] < x["son"]: continue
    e, s0 = int(round(x["son"] * 100)), int(round(y["bas"] * 100))
    n = kuyruk(e, +1, s0 - 3)
    if n: x["son"] = round(min(x["son"] + n / 100 + 0.03, y["bas"] - 0.01), 3); UZATILAN.append(("son", e / 100, x["son"]))
    n = kuyruk(s0, -1, int(round(x["son"] * 100)) + 1)
    if n: y["bas"] = round(max(y["bas"] - n / 100 - 0.03, x["son"] + 0.01), 3); UZATILAN.append(("bas", s0 / 100, y["bas"]))
for m in SUSTUR:   # tuş sesi aralığı uzatılan kuyruğa binmesin
    for _, ilk, yeni in UZATILAN:
        if m[0] < ilk < m[1] and yeni > m[0] and yeni > ilk: m[0] = yeni
def harita(bl):
    h, t = [], 0.0
    for d in bl:
        u = d.get("sessiz") or (d["son"] - d["bas"]); h.append((t, t + u, d)); t += u
    return h, t
yeni_h, toplam = harita(bolumler); eski_h, _ = harita(eski_plan["parcalar"][0]["bolumler"])
def cikti_zamani(kaynak):   # kaynak saniyesi → yeni videodaki saniye (çıkarılmış yerdeyse bir sonraki bölümün başı)
    for a, z, d in yeni_h:
        if "sessiz" not in d and d["bas"] <= kaynak < d["son"]: return a + kaynak - d["bas"]
    sonraki = [a for a, z, d in yeni_h if "sessiz" not in d and d["bas"] >= kaynak]
    return min(sonraki) if sonraki else toplam
def kaynak_zamani(eski):    # eski videodaki saniye → kaynak saniyesi
    for a, z, d in eski_h:
        if a <= eski < z: return (d["goruntu_bas"] if "sessiz" in d else d["bas"]) + eski - a if "sessiz" not in d else None
    return None
Tw = [a for a, z, d in yeni_h if "sessiz" in d][0]
p3_bas = cikti_zamani(86.06); p3_son = cikti_zamani(148.75)
G = []
for g in eski_g:
    kb, ks = kaynak_zamani(g["bas"]), kaynak_zamani(g["son"])
    yb = cikti_zamani(kb) if kb is not None else Tw
    ys = cikti_zamani(ks) if ks is not None else Tw + BEKLE
    if g["ifade"].startswith("Watch"): ys = Tw            # bekleme sırasında büyük animasyon var
    if g["ifade"].startswith("By calendar"): yb = Tw + BEKLE + 0.1
    G.append({**g, "bas": round(yb, 2), "son": round(ys, 2)})
a = [x for x in kut["clock"] if x["ad"] == "animasyon"][0]
k = 1920 / 2818   # slayt pikseli → çıktı (1920 genişlikte): ekranda slayt x*1.5, y*1.5+90; kesim x 31, y 90, genişlik 2818
animasyon = {"video": "outputs/final_anim_video_1080.mp4",   # VIDEO=1 TEMA=koyu SADE=1 python pilot/animasyon.py → mp4_yaz.swift
             "kucuk": {"x": round((a["x"] * 1.5 - 31) * k, 1), "y": round(a["y"] * 1.5 * k, 1), "w": round(a["w"] * 1.5 * k, 1), "h": round(a["h"] * 1.5 * k, 1)},
             "buyuk": {"x": 240, "y": 135, "w": 1440, "h": 810}, "gorunur": [round(p3_bas, 3), round(p3_son, 3)],
             "bekleme": [round(Tw, 3), round(Tw + BEKLE, 3)], "gif_bekleme_basi": GIF_BAS}
plan = {"aciklama": "30 Ekim asıl kayıt, kurgu sürüm 2. Saniyeler kaynak kayıttaki zamanlar. sessiz: o kadar saniye sessizlik (görüntü goruntu_bas'tan). sustur: tuş sesi için sıfırlanan aralıklar.",
        "kesim": {"x": 31, "y": 90, "genislik": 2818, "yukseklik": 1585}, "cikti": {"genislik": 2560, "yukseklik": 1440},
        "parcalar": [{"ad": "tam kayıt", "kaynak": KAYNAK, "sustur": SUSTUR, "bolumler": bolumler}]}
Path("sunum/video/kurgu_plani_30ekim.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
Path("sunum/video/gostergeler_30ekim.json").write_text(json.dumps({"gostergeler": G, "animasyon": animasyon}, ensure_ascii=False, indent=1))
print("kuyruk payı:", " ".join(f"{t}{a:.2f}→{b:.2f}" for t, a, b in UZATILAN))
print(f"nefes {len(NEFESLER)} · bölüm {len(bolumler)} · toplam {int(toplam // 60)}:{toplam % 60:04.1f} · bekleme {Tw:.1f}–{Tw + BEKLE:.1f} · 3. sayfa {p3_bas:.1f}–{p3_son:.1f}")
for g in G: print(f"  {g['bas']:6.1f}–{g['son']:6.1f} {g['hedef'][:30]}")
