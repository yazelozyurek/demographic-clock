"""Kapak videosu (24 Ekim): hareketli kapağın 30 fps MP4 sürümü, slaytın yazılarıyla birlikte (tam kapak slaytı).
Neden: slayttaki animasyonlu WebP Safari'de takılıyor. Video kaydında bu MP4 kullanılabilir.
(DÜZELTME, 25 Ekim: "slayt formatı <video> taşımıyor" yanlıştı. Slides tipi kısa klip taşıyor: <img src="durağan resim"
data-video="klip">, en fazla 20 MB H.264 MP4; sunumda klip oynar, PDF/PPTX ve küçük resimlerde durağan resim görünür.
Bunun için SLAYT=1 kipi eklendi, aşağıya bak.)

Ne yapar:
1) Yazı katmanı: sunum/slaytlar_kaynak/slides/cover.html'den resim (<img>) çıkarılır, zemin saydam yapılır ve sayfa headless
   Chrome'da 1920x1080 çizilir (Google Fonts: Source Serif 4, IBM Plex Sans). Yazı tipleri yüklenmezse betik durur:
   sayfa kırmızı zeminle başlar, zemin ancak iki yazı tipi de yüklenince saydamlaşır.
2) Kadran: çizim pilot/kapak_animasyon.py'den alınır. O dosyanın "zaman çizelgesi" bölümünden önceki kısmı aynen çalıştırılır
   (dosya değiştirilmez, WebP'ye dokunulmaz); böylece video ile slayttaki animasyon aynı çizimi kullanır.
3) Zaman çizelgesi, 30 fps (WebP'deki süreler saniye olarak aynı, kare sayıları iki katı):
   boş kadran 0,5 sn → akrep 1920'den 2023'e (7 sn, aynı yumuşatma; her ülke dönüm yılında 0,4 sn parlar) →
   2023 sonrası noktalar belirir (0,53 sn) → merkezde ortak eğri belirir (0,67 sn) → son hal 12 sn bekler.
   WebP'nin başındaki "son hal + geçiş" (PDF'e aktarılınca tam kapak görünsün diye) videoda yok.
   WebP'den tek çizim farkı: akrebin son 0,4 sn'sinde yanan 9 ülkenin parlaması WebP'de akrep durunca kesiliyor,
   burada sönerek bitiyor. Son kare WebP'nin son karesiyle aynı çizim.
4) Her kareye yazı katmanı bindirilir, kareler PNG olarak yazılır, pilot/mp4_yaz.swift ile MP4'e çevrilir
   (H.264 High, BT.709, son kare bekleme süresi boyunca sabit 30 fps tekrar edilir).

Çalıştırma (proje klasöründen):  python pilot/kapak_video.py
  KARE_DIZIN=<klasör>  kareleri ve yazı katmanını o klasörde bırakır (verilmezse geçici klasör kullanılır, sonra silinir)
  BEKLE_SN=<sn>        son halin bekleme süresi (varsayılan 12; SLAYT=1 ile 45)
  SLAYT=1              (25 Ekim) sunumun kapak slaytına konan klip: outputs/final_0_cover_clip.mp4 + durağan resmi
                       outputs/final_0_cover_still.png (yazısız son hal; PDF'te ve küçük resimlerde bu görünür).
                       Yazı katmanı YOK (yazılar slaytta HTML olarak duruyor; Chrome ve internet gerekmez).
                       Klip WebP gibi başlar: son hal 0,7 sn → 0,4 sn'de sıfırlanır → sonra yukarıdaki akış; böylece
                       durağan resimden klibe geçiş ve klibin başa dönüşü (sunumda döngüyle oynar) sıçramasız olur.
                       Son hal 45 sn bekler (kapak konuşması ~20 sn; klip konuşma sırasında başa dönmesin).
                       Kodlama: anahtar kare 10 sn'de bir (dosya küçük kalsın, sınır 20 MB), renk etiketi sRGB.
Gerekenler: Google Chrome (/Applications), internet (yazı tipleri için), Xcode komut satırı araçları (swift).
Kontrol:  swift pilot/mp4_kontrol.swift outputs/final_0_cover_video.mp4 <klasör>
Çıktı: outputs/final_0_cover_video.mp4 (1920x1080, 30 fps, H.264, yaklaşık 20,7 sn)"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image

KOK = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FPS = 30
BOS_SN = 0.5                                                        # başta boş kadran
SLAYT = os.environ.get("SLAYT") == "1"                              # sunumun içindeki klip (yazısız)
BEKLE_SN = float(os.environ.get("BEKLE_SN", "45" if SLAYT else "12"))   # sonda son hal
CIKTI = KOK / ("outputs/final_0_cover_clip.mp4" if SLAYT else "outputs/final_0_cover_video.mp4")
DURAGAN = KOK / "outputs/final_0_cover_still.png"                   # SLAYT: klibin durağan resmi
SON_SN, GECIS_SN = 0.7, 0.4                                          # SLAYT: başta son hal ve sıfırlanma (WebP'deki gibi)
basla = time.time()

# ---------- 1) yazı katmanı (headless Chrome, saydam zemin) ----------
FONT = ('<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">')
CSS = ("*{margin:0;box-sizing:border-box} body{margin:0} section{position:relative;width:1920px;height:1080px;overflow:hidden} "
       "aside{display:none} section > *:not([style*=\"position:absolute\"]){position:relative} "      # slayt önizlemesiyle aynı
       "html,body,section{background:transparent!important} html.bekliyor{background:#ff0000!important}")
JS = """Promise.all([document.fonts.load('700 96px "Source Serif 4"'), document.fonts.load('400 24px "IBM Plex Sans"', 'Aİğışöü')])
  .then(function () { return document.fonts.ready; }).then(function () {
    var yuklu = [];
    document.fonts.forEach(function (f) { if (f.status === "loaded") yuklu.push(f.family.replace(/["']/g, "") + " " + f.weight); });
    document.body.setAttribute("data-fonts", JSON.stringify(yuklu));
    if (yuklu.indexOf("Source Serif 4 700") >= 0 && yuklu.indexOf("IBM Plex Sans 400") >= 0)
      document.documentElement.classList.remove("bekliyor");
  });"""


def yazi_katmani(dizin):
    slayt = (KOK / "sunum/slaytlar_kaynak/slides/cover.html").read_text(encoding="utf-8")
    resim = re.findall(r"<img\b[^>]*>", slayt)
    if len(resim) != 1:
        sys.exit(f"cover.html'de 1 resim bekleniyordu, {len(resim)} bulundu")
    sayfa = dizin / "kapak_yazi.html"
    sayfa.write_text(f"<!doctype html><html class='bekliyor'><head><meta charset='utf-8'>{FONT}<style>{CSS}</style></head>"
                     f"<body>{slayt.replace(resim[0], '')}<script>{JS}</script></body></html>", encoding="utf-8")
    png = dizin / "kapak_yazi.png"
    profil = tempfile.mkdtemp(prefix="kapak_chrome_")
    ortak = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
             f"--user-data-dir={profil}", "--window-size=1920,1080", "--virtual-time-budget=6000", "--force-color-profile=srgb"]
    try:
        dom = subprocess.run(ortak + ["--dump-dom", sayfa.as_uri()], capture_output=True, text=True, timeout=180).stdout
        subprocess.run(ortak + ["--default-background-color=00000000", f"--screenshot={png}", sayfa.as_uri()],
                       capture_output=True, timeout=180, check=True)
    finally:
        shutil.rmtree(profil, ignore_errors=True)
    m = re.search(r'data-fonts="([^"]*)"', dom)
    yuklu = sorted(set(json.loads(html.unescape(m.group(1))))) if m else []
    katman = np.asarray(Image.open(png).convert("RGBA"))
    if katman.shape != (1080, 1920, 4):
        sys.exit(f"Yazı katmanı boyutu beklenmedik: {katman.shape}")
    if katman[0, 0, 3] != 0 or not {"Source Serif 4 700", "IBM Plex Sans 400"} <= set(yuklu):
        sys.exit(f"Yazı tipleri yüklenmedi (internet bağlantısı?). Yüklenen: {yuklu}")
    return katman, yuklu


# ---------- 2) kadran çizimi: kapak_animasyon.py'nin zaman çizelgesinden önceki kısmı, aynen ----------
KAYNAK = KOK / "pilot/kapak_animasyon.py"
kod = KAYNAK.read_text(encoding="utf-8")
ISARET = "# ---------- zaman çizelgesi ----------"
if kod.count(ISARET) != 1:
    sys.exit(f"{KAYNAK.name} içinde '{ISARET}' satırı bulunamadı")
c = {"__file__": str(KAYNAK), "__name__": "kapak_animasyon_cizim"}
exec(compile(kod.split(ISARET)[0], str(KAYNAK), "exec"), c)
kare, nokta, BAS, SIMDI = c["kare"], c["nokta"], c["BAS"], c["SIMDI"]
WEBP_FPS = c["FPS"]                                                  # 15
c["PARLAMA"] = round(c["PARLAMA"] / WEBP_FPS * FPS)                 # parlama 0,4 sn: 6 kare (15 fps) → 12 kare (30 fps)
N_SUPURME = round(c["SUPURME_SN"] * FPS)                            # akrep 7 sn: 210 aralık
N_GELECEK = round(8 / WEBP_FPS * FPS)                               # WebP'de 8 kare (0,53 sn) → 16
N_MERKEZ = round(10 / WEBP_FPS * FPS)                               # WebP'de 10 kare (0,67 sn) → 20

# ---------- 3) kareler ----------
kalici = os.environ.get("KARE_DIZIN")
dizin = Path(kalici) if kalici else Path(tempfile.mkdtemp(prefix="kapak_video_"))
kareler = dizin / "kareler"
kareler.mkdir(parents=True, exist_ok=True)
for eski in kareler.glob("kare_*.png"):                              # önceki çalıştırmanın kareleri
    eski.unlink()
if not SLAYT:
    katman, yuklu = yazi_katmani(dizin)
    print("yazı tipleri:", ", ".join(yuklu))
    alfa = katman[..., 3:4].astype(np.float32) / 255
    on_plan = katman[..., :3].astype(np.float32) * alfa             # Chrome'un PNG'si düz (premultiplied olmayan) alfa
    ters = 1 - alfa


def bindir(im):
    if SLAYT:                                                        # yazılar slaytta HTML olarak duruyor
        return im
    return Image.fromarray(np.rint(np.asarray(im, dtype=np.float32) * ters + on_plan).astype(np.uint8))


sayac = 0
def yaz(im, kac=1):
    global sayac
    ilk = kareler / f"kare_{sayac:05d}.png"
    bindir(im).save(ilk, compress_level=2)
    for _ in range(kac - 1):                                         # aynı kare: dosya kopyalanır
        sayac += 1
        shutil.copyfile(ilk, kareler / f"kare_{sayac:05d}.png")
    sayac += 1


if SLAYT:                                                            # son hal → saat sıfırlanır (yumuşak geçiş)
    bas_son, bas_bos = kare(SIMDI, 1.0, 1.0), kare(BAS, 0.0, 0.0)
    yaz(bas_son, round(SON_SN * FPS))
    n_gecis = round(GECIS_SN * FPS)
    for i in range(1, n_gecis):
        yaz(Image.blend(bas_son, bas_bos, i / n_gecis))
yaz(kare(BAS, 0.0, 0.0), round(BOS_SN * FPS))                       # boş kadran (akrep 1920'de)
ilk_kare, onceki = {}, BAS
for i in range(N_SUPURME + 1):                                       # akrep 1920 → 2023,5
    u = i / N_SUPURME
    akrep_yil = BAS + (SIMDI - BAS) * (0.7 * u + 0.3 * (3 * u ** 2 - 2 * u ** 3))   # WebP'deki yumuşatma
    for n in nokta:
        if onceki < n["t"] <= akrep_yil or (i == 0 and n["t"] <= BAS + 0.5):
            ilk_kare[id(n)] = i
    yaz(kare(akrep_yil, 0.0, 0.0, {k: i - v for k, v in ilk_kare.items()}))
    onceki = akrep_yil
for i in range(1, N_GELECEK + 1):                                    # 2023 sonrası (boş halkalar) belirir
    yaz(kare(SIMDI, i / N_GELECEK, 0.0, {k: N_SUPURME + i - v for k, v in ilk_kare.items()}))   # son parlamalar söner
assert all(N_SUPURME + N_GELECEK - v >= c["PARLAMA"] for v in ilk_kare.values()), "merkez belirirken parlama sürüyor"
for i in range(1, N_MERKEZ + 1):                                     # merkezde ortak eğri belirir
    son_kare = kare(SIMDI, 1.0, i / N_MERKEZ)
    yaz(son_kare)
son_hal = kare(SIMDI, 1.0, 1.0)                                      # WebP'nin son hali (SON_HAL) ile aynı çağrı
assert np.array_equal(np.asarray(son_kare), np.asarray(son_hal)), "son kare son hal değil"
if SLAYT:
    assert np.array_equal(np.asarray(bas_son), np.asarray(son_hal)), "klibin ilk karesi son hal değil"
    son_hal.save(DURAGAN)                                            # durağan resim = klibin ilk ve son karesi
if kalici:
    son_hal.save(dizin / "kadran_son.png")                           # kontrol için (yazısız kadran)
cizim_sn = time.time() - basla
print(f"{sayac} kare çizildi ({cizim_sn:.0f} sn): " + (f"son hal {round(SON_SN * FPS)} + geçiş {round(GECIS_SN * FPS) - 1} + " if SLAYT else "")
      + f"boş {round(BOS_SN * FPS)} + akrep {N_SUPURME + 1} + gelecek {N_GELECEK} "
      f"+ merkez {N_MERKEZ}; parlama {c['PARLAMA']} kare; son hal {BEKLE_SN:g} sn bekler")

# ---------- 4) MP4 ----------
swift = shutil.which("swift") or "/usr/bin/swift"
ek = ["10", "srgb"] if SLAYT else []                                 # SLAYT: anahtar kare 10 sn, sRGB etiketi
subprocess.run([swift, str(KOK / "pilot/mp4_yaz.swift"), str(kareler), str(FPS), str(CIKTI), f"{BEKLE_SN:g}"] + ek, check=True)
if SLAYT and CIKTI.stat().st_size > 20e6:
    sys.exit(f"Klip {CIKTI.stat().st_size / 1e6:.1f} MB: sunum klibi en fazla 20 MB olabilir")
if not kalici:
    shutil.rmtree(dizin, ignore_errors=True)
print(f"Bitti: {CIKTI.relative_to(KOK)} · {sayac / FPS + BEKLE_SN:.2f} sn · {CIKTI.stat().st_size / 1e6:.1f} MB · "
      f"toplam {time.time() - basla:.0f} sn")
