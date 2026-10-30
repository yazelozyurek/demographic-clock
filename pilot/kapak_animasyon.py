"""Hareketli kapak (A, 24 Ekim): "Saat işliyor". kapak_saat.py'nin (mavi tema) animasyonlu hali; veri ve yerleşim aynı.
Akrep 1920'den 2023'e döner; geçtiği her ülkenin noktası dönüm yılında parlayarak yanar. Beyaz sağlık bandı noktalardan önce
dolar (sağlık önce). Türkiye'nin halkaları 1965 ve 1982'de yanar. 2023'ten sonraki noktalar (UN projeksiyonu) soluk gelir.
Sonda merkezdeki ortak eğri belirir. İlk kare = son hal (PDF'e aktarılınca tam kapak görünsün diye); kısa bir geçişle saat sıfırlanır.
Çalıştırma (proje klasöründen):  python pilot/kapak_animasyon.py
Çıktı: outputs/final_0_cover_anim.webp (+ outputs/final_0_cover_anim_onizleme_*.png)"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

KOK = Path(__file__).resolve().parent.parent
ZEMIN, HALKA1, HALKA2 = "#101C27", "#3A5168", "#4A6680"
METIN, METIN2, CENTIK1, CENTIK2, AKREP, SAGLIK = "#FFFFFF", "#C9D4DC", "#8FA1AE", "#3D5163", "#FFD166", "#F2F7FF"
BOLGE = {"Asia": "#4DA3FF", "Africa": "#FF7A3D", "Europe": "#2FD49A",
         "Latin America and the Caribbean": "#FFC233", "Northern America": "#FF5FA2", "Oceania": "#A98BFF"}
BAS, SON = 1920, 2080
aci = lambda y: (np.asarray(y, float) - BAS) / (SON - BAS) * 2 * np.pi
U, L, K = 6.97, 1.67, 0.0816
FPS, SUPURME_SN, PARLAMA = 15, 7.0, 6                                            # parlama: kaç kare sürer (hafif sürüm: 8 → 6)
SIMDI = 2023.5

df = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["Location", "bolge", "Time", "TFR", "pop2023"])
df = df[df["pop2023"] >= 100]
tt = pd.read_csv(KOK / "clean/t0_tablosu.csv")
Y = df.pivot(index="Location", columns="Time", values="TFR")
yil = Y.columns.values.astype(float)

# ---------- sabit katman (kapak_saat.py ile aynı) ----------
fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=ZEMIN)                       # 1920×1080: ekrandaki boyut; 2880×1620 sürümü tarayıcıda takılıyordu
hale = fig.add_axes([0, 0, 1, 1]); hale.set_axis_off()
gx, gy = np.meshgrid(np.linspace(0, 19.2, 480), np.linspace(10.8, 0, 270))
d = np.hypot(gx - 19.2 * 0.735, gy - 10.8 * 0.5)
img = np.zeros(gx.shape + (4,))
for (r_, g_, b_), merkez, gen, guc in [((0.18, 0.42, 1.0), 0, 4.6, 0.34), ((0.48, 0.32, 1.0), 3.0, 1.5, 0.20)]:
    a_ = guc * np.exp(-((d - merkez) / gen) ** 2)
    img[..., :3] += np.array([r_, g_, b_]) * a_[..., None]; img[..., 3] = np.maximum(img[..., 3], a_)
img[..., :3] = np.clip(img[..., :3] / np.maximum(img[..., 3:], 1e-6), 0, 1)
hale.imshow(img, extent=[0, 19.2, 0, 10.8], interpolation="bilinear"); hale.set_xlim(0, 19.2); hale.set_ylim(0, 10.8)
MERKEZ_X, MERKEZ_Y, YARI = 0.735, 0.50, 0.215
ax = fig.add_axes([MERKEZ_X - YARI, MERKEZ_Y - YARI * 19.2 / 10.8, 2 * YARI, 2 * YARI * 19.2 / 10.8], projection="polar", facecolor="none")
ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
ax.set_rlim(0, 1.3); ax.grid(False); ax.spines["polar"].set_visible(False); ax.set_xticks([]); ax.set_yticks([])
th = np.linspace(0, 2 * np.pi, 720)
ax.plot(th, np.full_like(th, 0.74), color=HALKA1, lw=1.2)
ax.plot(th, np.full_like(th, 1.22), color=HALKA2, lw=1.6)
for y in range(BAS, SON, 2):
    uzun = y % 20 == 0
    ax.plot([aci(y)] * 2, [1.22, 1.17 if uzun else 1.20], color=CENTIK1 if uzun else CENTIK2, lw=2 if uzun else 1)
for y in range(BAS, SON, 20):
    ax.text(aci(y), 1.31, str(y), color=METIN, fontsize=17, fontweight="bold", ha="center", va="center")

# ---------- ülke noktaları (her biri ayrı; görünürlük karede değişir) ----------
tt = tt.assign(t=tt["t0"].clip(BAS + 0.5, SON - 0.5)).sort_values(["t", "bolge"])
tt["kutu"] = ((tt["t"] - BAS) // 2).astype(int)
tt["sira"] = tt.groupby("kutu").cumcount()
nokta = []
for _, r in tt.iterrows():
    a = aci(BAS + 2 * r["kutu"] + 1); rr = 0.785 + 0.042 * r["sira"]; renk = BOLGE[r["bolge"]]
    parla = ax.scatter([a], [rr], s=0, color=renk, alpha=0, lw=0, zorder=3)
    if r["guvenilir"]:
        par = [ax.scatter([a], [rr], s=300, color=renk, alpha=0.25, lw=0, zorder=3), ax.scatter([a], [rr], s=80, color=renk, lw=0, zorder=4)]
        taban_alfa = [0.25, 1.0]
    else:
        par = [ax.scatter([a], [rr], s=52, facecolor=ZEMIN, edgecolor=renk, linewidth=1.6, zorder=4)]
        taban_alfa = [1.0]
    nokta.append(dict(t=float(r["t0"]), par=par, alfa=taban_alfa, parla=parla, dolu=bool(r["guvenilir"])))

# ---------- sağlık saati bandı (karede akrebe kadar çizilir) ----------
sg = pd.read_csv(KOK / "clean/saglik_saati.csv").dropna(subset=["t0_saglik"])
ts = sg["t0_saglik"].clip(BAS, SON).values
yy = np.linspace(BAS, SON, 640)
yog = np.exp(-0.5 * ((yy[:, None] - ts[None, :]) / 2.5) ** 2).sum(1); yog /= yog.max()
taban = 0.725
iz = np.where(yog > 0.06, taban - 0.09 * yog, np.nan)
bant = []
def bant_ciz(son_yil):
    for c in bant: c.remove()
    bant.clear()
    m = yy <= son_yil
    if m.sum() < 2: return
    for k_, al in [(0.035, 0.10), (0.018, 0.20)]:
        bant.append(ax.fill_between(aci(yy[m]), np.where(yog[m] > 0.06, iz[m] - k_, np.nan), taban, color=SAGLIK, alpha=al, lw=0, zorder=4))
    bant.append(ax.fill_between(aci(yy[m]), iz[m], taban, color=SAGLIK, alpha=0.62, lw=0, zorder=5))
    bant.extend(ax.plot(aci(yy[m]), iz[m], color=SAGLIK, lw=1.6, alpha=1.0, zorder=5))

gg = sg[sg["guvenilir"]]
m_h, m_f = gg["t0_saglik"].median(), gg["t0"].median()
yay = np.linspace(aci(m_h), aci(m_f) - 0.02, 80)
ortanca = ax.plot(yay, np.full_like(yay, 0.56), color="#FFFFFF", lw=2.0, zorder=9) + \
    [ax.annotate("", xy=(aci(m_f), 0.56), xytext=(yay[-6], 0.56), arrowprops=dict(arrowstyle="-|>", color="#FFFFFF", lw=2.0, mutation_scale=16), zorder=9),
     ax.text(aci(1990), 0.40, f"median\n≈ {gg['fark'].median():.0f} years", color="#FFFFFF", fontsize=14, fontweight="bold", ha="center", va="center", linespacing=1.2, zorder=9)]
etiket_saglik = ax.text(aci(2003), 0.585, "health clock", color=SAGLIK, fontsize=14, fontweight="bold", ha="center", va="center", zorder=7)
etiket_dogurganlik = ax.text(aci(2052), 0.93, "fertility clock", color=METIN2, fontsize=14, fontweight="bold", ha="center", va="center", zorder=7)

# ---------- Türkiye ----------
trr = tt.set_index("Location").loc["Türkiye"]
tr_f, tr_h = float(trr["t0"]), float(sg.set_index("Location").loc["Türkiye", "t0_saglik"])
a_f, r_f = aci(BAS + 2 * trr["kutu"] + 1), 0.785 + 0.042 * trr["sira"]
a_h = aci(tr_h); r_h = taban - 0.09 * float(np.interp(BAS + a_h / (2 * np.pi) * (SON - BAS), yy, yog)) / 2
halka_h = ax.scatter([a_h], [r_h], s=420, facecolor="none", edgecolor="#FFFFFF", linewidth=2.6, zorder=8)
halka_f = ax.scatter([a_f], [r_f], s=420, facecolor="none", edgecolor="#FFFFFF", linewidth=2.6, zorder=8)
yol_a = np.linspace(a_h, a_f, 60); yol_r = np.linspace(r_h, r_f, 60) - 0.10 * np.sin(np.linspace(0, np.pi, 60))
a_l, r_l = aci(1985.8), 1.60
turkiye = ax.plot(yol_a[3:-4], yol_r[3:-4], color="#FFFFFF", lw=2.2, zorder=8) + \
    [ax.annotate("", xy=(yol_a[-4], yol_r[-4]), xytext=(yol_a[-8], yol_r[-8]), arrowprops=dict(arrowstyle="-|>", color="#FFFFFF", lw=2.2, mutation_scale=18), zorder=8)] + \
    ax.plot([a_f, a_l], [r_f + 0.04, r_l - 0.06], color="#FFFFFF", lw=1.2, alpha=0.8, zorder=8, clip_on=False) + \
    [ax.text(a_l, r_l, "Türkiye: health 1965 → fertility 1982", color="#FFFFFF", fontsize=15, fontweight="bold", ha="center", va="center", zorder=9)]

# ---------- akrep ----------
akrep = [ax.plot([0, 0], [0.50, 1.25], color=AKREP, lw=lw, alpha=al, solid_capstyle="round", zorder=6)[0] for lw, al in [(14, 0.10), (7, 0.22), (3, 1.0)]]
akrep_yazi = ax.text(0, 0.46, "", color=AKREP, fontsize=16, fontweight="bold", ha="center", va="center", zorder=7)

# ---------- merkez ----------
t0s = tt.set_index("Location")["t0"]
ic = fig.add_axes([MERKEZ_X - 0.075, MERKEZ_Y - 0.10, 0.15, 0.19], facecolor="none")
ic.axis("off"); ic.set_xlim(-90, 110); ic.set_ylim(0.6, 8.4)
bolge = df.drop_duplicates("Location").set_index("Location")["bolge"]
merkez = [(ic.plot(yil[yil <= 2023] - t0s[u], Y.loc[u].values[yil <= 2023], color=BOLGE[bolge[u]], lw=0.7, alpha=0.45)[0], 0.45) for u in Y.index]
z = np.linspace(-90, 110, 300); egri = L + (U - L) / (1 + np.exp(K * z))
merkez += [(ic.plot(z, egri, color=METIN, lw=lw, alpha=al, solid_capstyle="round")[0], al) for lw, al in [(9, 0.08), (4.5, 0.2), (2.4, 1.0)]]
merkez += [(ic.text(5, 8.0, "one shared path", color=METIN, fontsize=13, fontweight="bold", ha="left"), 1.0),
           (ic.text(5, 7.0, "R² = 0.94", color=METIN2, fontsize=12, ha="left"), 1.0)]

def gorunur(sanatcilar, f):
    for s in sanatcilar:
        s.set_visible(f > 0); s.set_alpha(f) if f > 0 else None

def kare(akrep_yil, gelecek=1.0, merkez_f=1.0, parlama_kare=None):
    """Bir kareyi çiz: akrep_yil'e kadar olanlar görünür; gelecek = 2023 sonrası noktaların görünürlüğü; merkez_f = merkezin."""
    for n in nokta:
        if n["t"] <= SIMDI:
            f = 1.0 if n["t"] <= akrep_yil else 0.0
        else:
            f = gelecek                                                               # projeksiyon: yavaşça belirir (boş halka)
        for s, al in zip(n["par"], n["alfa"]):
            s.set_visible(f > 0); s.set_alpha(al * f)
        k = parlama_kare.get(id(n)) if parlama_kare else None
        if k is not None and k < PARLAMA:
            g = 1 - k / PARLAMA
            n["parla"].set_sizes([300 + 700 * g ** 2]); n["parla"].set_alpha((0.55 if n["dolu"] else 0.35) * g); n["parla"].set_visible(True)
        else:
            n["parla"].set_visible(False)
    bant_ciz(min(akrep_yil, SIMDI) if akrep_yil < SIMDI else SON)
    # 24 Ekim: iki etiket akrep 2015'i geçince belirir (önce 2003 ve m_f = 1987 idi). Akrep ve yıl yazısı
    # "health clock" ile "median ≈ 18 years" yazılarının üstünden geçmesin. Son kare değişmez.
    etiket_saglik.set_visible(akrep_yil >= 2015)
    gorunur(ortanca, 1.0 if akrep_yil >= 2015 else 0.0)
    etiket_dogurganlik.set_visible(gelecek > 0); etiket_dogurganlik.set_alpha(min(1.0, gelecek))
    halka_h.set_visible(akrep_yil >= tr_h); halka_f.set_visible(akrep_yil >= tr_f)
    gorunur(turkiye, 1.0 if akrep_yil >= tr_f + 2 else 0.0)
    a = aci(min(akrep_yil, SIMDI))
    for c in akrep: c.set_data([a, a], [0.50, 1.25])
    akrep_yazi.set_position((a + 0.09, 0.46)); akrep_yazi.set_text(str(int(min(akrep_yil, 2023))))
    for s, al in merkez:
        s.set_visible(merkez_f > 0); s.set_alpha(al * merkez_f)
    fig.canvas.draw()
    return Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[..., :3].copy())

# ---------- zaman çizelgesi ----------
SON_HAL = kare(SIMDI, 1.0, 1.0)
BOS_HAL = kare(BAS, 0.0, 0.0)
kareler, sureler = [SON_HAL], [700]                                              # PDF için ilk kare = son hal
for i in range(1, 7):                                                            # saat sıfırlanıyor (yumuşak geçiş)
    kareler.append(Image.blend(SON_HAL, BOS_HAL, i / 6)); sureler.append(60)
n_s = int(SUPURME_SN * FPS); onceki = BAS; ilk_kare = {}
onizle = {1950: None, 1970: None, 1990: None, 2010: None}
for i in range(n_s + 1):
    u = i / n_s
    akrep_yil = BAS + (SIMDI - BAS) * (0.7 * u + 0.3 * (3 * u ** 2 - 2 * u ** 3))   # hafif yumuşatılmış, neredeyse sabit hız
    for n in nokta:
        if onceki < n["t"] <= akrep_yil or (i == 0 and n["t"] <= BAS + 0.5):
            ilk_kare[id(n)] = i
    parlama = {k: i - v for k, v in ilk_kare.items()}
    im = kare(akrep_yil, 0.0, 0.0, parlama); kareler.append(im); sureler.append(round(1000 / FPS))
    for y in onizle:
        if onizle[y] is None and akrep_yil >= y:
            onizle[y] = im
    onceki = akrep_yil
for i in range(1, 9):                                                            # 2023 sonrası (UN projeksiyonu) belirir (hafif sürüm: 15 → 8 kare)
    kareler.append(kare(SIMDI, i / 8, 0.0)); sureler.append(round(1000 / FPS))
for i in range(1, 11):                                                           # merkezde ortak eğri belirir (hafif sürüm: 20 → 10 kare)
    kareler.append(kare(SIMDI, 1.0, i / 10)); sureler.append(round(1000 / FPS))
kareler.append(SON_HAL); sureler.append(25000)                                   # son hal 25 sn bekler, sonra başa döner

cikti = KOK / "outputs/final_0_cover_anim.webp"
kareler[0].save(cikti, save_all=True, append_images=kareler[1:], duration=sureler, loop=0, quality=82, method=4, kmin=0, kmax=0)   # kmax=0: ara tam kare yok
# (GIF denendi, 24 Ekim: ortak 255 renklik palet bölge renklerini bozdu → kullanılmıyor)
for y, im in onizle.items():
    im.save(KOK / f"outputs/final_0_cover_anim_onizleme_{y}.png")
SON_HAL.save(KOK / "outputs/final_0_cover_anim_onizleme_son.png")
print(f"Yazıldı: {len(kareler)} kare · hareket {sum(sureler[:-1]) / 1000:.1f} sn + 25 sn bekleme · "
      f"WebP {cikti.stat().st_size / 1e6:.1f} MB")
