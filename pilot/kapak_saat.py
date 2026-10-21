"""Kapak görseli v2: "Demografik Saat" kadranı.
Kadranın çevresi = takvim yılı (1920 saat 12'de, saat yönünde 2080'e). Her nokta bir ülke: dönüm noktası yılına (t0,
04 notebook'u) yerleşir, aynı yıllara düşen ülkeler dışa doğru üst üste dizilir (dairesel nokta histogramı).
Renk = bölge; dolu = dönüm noktası veride görülüyor, boş = çıkarımla bulundu. Akrep = 2023.
Merkez = 200 ülkenin TFR seyri kendi dönüm noktasına kaydırılmış hali ve tek ortak eğri (R² 0.94).
v3 (21 Ekim, Q3): iç yaylar yerine SAĞLIK SAATİ bandı (yaşam beklentisinin en hızlı yükseldiği yıl, clean/saglik_saati.csv;
her yıl kaç ülkenin sağlık saatinin döndüğü, yumuşatılmış). Türkiye iki beyaz halkayla: sağlık 1965 → doğurganlık 1982.
Çalıştırma:  python pilot/saglik_saati.py ; python pilot/kapak_saat.py  →  outputs/final_0_cover_clock2.png
(eski v2 kapak: pilot/kapak_saat_q3_oncesi.py → final_0_cover_clock.png)"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parent.parent
import os
TEMA = os.environ.get("TEMA", "mavi")
GRAFIT, ACIK = TEMA == "grafit", TEMA == "acik"
SON_AD = {"grafit": "_g", "acik": "_a"}.get(TEMA, "")
ZEMIN = {"grafit": "#141518", "acik": "#F7F6F2"}.get(TEMA, "#101C27")
HALKA1, HALKA2 = {"grafit": ("#3A3C42", "#4A4C53"), "acik": ("#D6D4CE", "#C4C2BB")}.get(TEMA, ("#3A5168", "#4A6680"))
METIN, METIN2 = ("#1F2328", "#4A525B") if ACIK else ("#FFFFFF", "#C9D4DC")
CENTIK1, CENTIK2 = ("#6B7480", "#C9C7C0") if ACIK else ("#8FA1AE", "#3D5163")
AKREP = "#D97706" if ACIK else "#FFD166"
BOLGE = {"Asia": "#4DA3FF", "Africa": "#FF7A3D", "Europe": "#2FD49A",          # slayt paletinin daha parlak tonları (kapak)
         "Latin America and the Caribbean": "#FFC233", "Northern America": "#FF5FA2", "Oceania": "#A98BFF"}
if os.environ.get("TEMA") == "acik":   # açık zemin: dataviz açık paleti
    BOLGE = {"Asia": "#2a78d6", "Africa": "#eb6834", "Europe": "#1baf7a",
             "Latin America and the Caribbean": "#eda100", "Northern America": "#e87ba4", "Oceania": "#6250d6"}
BAS, SON = 1920, 2080
aci = lambda y: (np.asarray(y, float) - BAS) / (SON - BAS) * 2 * np.pi
U, L, K = 6.97, 1.67, 0.0816                                                     # 04 notebook'unun ortak eğrisi

df = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["Location", "bolge", "Time", "TFR", "pop2023"])
df = df[df["pop2023"] >= 100]
tt = pd.read_csv(KOK / "clean/t0_tablosu.csv")
Y = df.pivot(index="Location", columns="Time", values="TFR")
yil = Y.columns.values.astype(float)

fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=ZEMIN)
# arka plan: kadranın arkasında yumuşak ışık halesi
hale = fig.add_axes([0, 0, 1, 1]); hale.set_axis_off()
gx, gy = np.meshgrid(np.linspace(0, 19.2, 480), np.linspace(10.8, 0, 270))
d = np.hypot(gx - 19.2 * 0.735, gy - 10.8 * 0.5)
img = np.zeros(gx.shape + (4,))
for (r_, g_, b_), merkez, gen, guc in ([((0.55, 0.75, 1.0), 0, 4.6, 0.30), ((1.0, 0.78, 0.60), 3.0, 1.4, 0.22)] if ACIK else
                                    [((0.55, 0.55, 0.60), 0, 4.6, 0.16), ((0.85, 0.55, 0.35), 3.0, 1.4, 0.10)] if GRAFIT else
                                    [((0.18, 0.42, 1.0), 0, 4.6, 0.34), ((0.48, 0.32, 1.0), 3.0, 1.5, 0.20)]):
    a_ = guc * np.exp(-((d - merkez) / gen) ** 2)
    img[..., :3] += np.array([r_, g_, b_]) * a_[..., None]; img[..., 3] = np.maximum(img[..., 3], a_)
img[..., :3] = np.clip(img[..., :3] / np.maximum(img[..., 3:], 1e-6), 0, 1)
hale.imshow(img, extent=[0, 19.2, 0, 10.8], interpolation="bilinear")
hale.set_xlim(0, 19.2); hale.set_ylim(0, 10.8)
MERKEZ_X, MERKEZ_Y, YARI = 0.735, 0.50, 0.215                                    # kadranın yeri (figür oranı, genişliğe göre)
ax = fig.add_axes([MERKEZ_X - YARI, MERKEZ_Y - YARI * 19.2 / 10.8, 2 * YARI, 2 * YARI * 19.2 / 10.8],
                  projection="polar", facecolor="none")
ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)
ax.set_rlim(0, 1.3); ax.grid(False); ax.spines["polar"].set_visible(False); ax.set_xticks([]); ax.set_yticks([])

th = np.linspace(0, 2 * np.pi, 720)
ax.plot(th, np.full_like(th, 0.74), color=HALKA1, lw=1.2)                     # iç çember
ax.plot(th, np.full_like(th, 1.22), color=HALKA2, lw=1.6)                     # dış çember
for y in range(BAS, SON, 2):                                                     # çentikler
    uzun = y % 20 == 0
    ax.plot([aci(y)] * 2, [1.22, 1.17 if uzun else 1.20], color=CENTIK1 if uzun else CENTIK2, lw=2 if uzun else 1)
for y in range(BAS, SON, 20):
    ax.text(aci(y), 1.31, str(y), color=METIN, fontsize=17, fontweight="bold", ha="center", va="center")

# dairesel nokta histogramı: 2 yıllık kutular, her kutuda dışa doğru dizilim
tt = tt.assign(t=tt["t0"].clip(BAS + 0.5, SON - 0.5)).sort_values(["t", "bolge"])
tt["kutu"] = ((tt["t"] - BAS) // 2).astype(int)
tt["sira"] = tt.groupby("kutu").cumcount()
for _, r in tt.iterrows():
    a = aci(BAS + 2 * r["kutu"] + 1); rr = 0.785 + 0.042 * r["sira"]; renk = BOLGE[r["bolge"]]
    if r["guvenilir"]:
        ax.scatter([a], [rr], s=300, color=renk, alpha=0.25, lw=0, zorder=3)      # parıltı
        ax.scatter([a], [rr], s=80, color=renk, lw=0, zorder=4)
    else:
        ax.scatter([a], [rr], s=52, facecolor=ZEMIN, edgecolor=renk, linewidth=1.6, zorder=4)

# SAĞLIK SAATİ: iç çemberin hemen içinde, her yıl kaç ülkenin sağlık saatinin döndüğü (2 yıllık çekirdekle yumuşatılmış)
SAGLIK = "#F2F7FF"
sg = pd.read_csv(KOK / "clean/saglik_saati.csv").dropna(subset=["t0_saglik"])
ts = sg["t0_saglik"].clip(BAS, SON).values
yy = np.linspace(BAS, SON, 640)
yog = np.exp(-0.5 * ((yy[:, None] - ts[None, :]) / 2.5) ** 2).sum(1); yog /= yog.max()
taban = 0.725
iz = np.where(yog > 0.06, taban - 0.09 * yog, np.nan)                            # boş yıllarda bant çizilmez
for k_, al in [(0.035, 0.10), (0.018, 0.20)]:
    ax.fill_between(aci(yy), np.where(yog > 0.06, iz - k_, np.nan), taban, color=SAGLIK, alpha=al, lw=0, zorder=4)
ax.fill_between(aci(yy), iz, taban, color=SAGLIK, alpha=0.62, lw=0, zorder=5)
ax.plot(aci(yy), iz, color=SAGLIK, lw=1.6, alpha=1.0, zorder=5)
# iki saatin ortancası (dönüm noktası veride görülen 115 ülke): sağlık önce, doğurganlık ≈ 18 yıl sonra
gg = sg[sg["guvenilir"]]
m_h, m_f = gg["t0_saglik"].median(), gg["t0"].median()
yay = np.linspace(aci(m_h), aci(m_f) - 0.02, 80)
ax.plot(yay, np.full_like(yay, 0.56), color="#FFFFFF", lw=2.0, zorder=9)
ax.annotate("", xy=(aci(m_f), 0.56), xytext=(yay[-6], 0.56), arrowprops=dict(arrowstyle="-|>", color="#FFFFFF", lw=2.0, mutation_scale=16), zorder=9)
ax.text(aci(1990), 0.40, f"median\n≈ {gg['fark'].median():.0f} years", color="#FFFFFF", fontsize=14, fontweight="bold", ha="center", va="center", linespacing=1.2, zorder=9)
ax.text(aci(2003), 0.585, "health clock", color=SAGLIK, fontsize=14, fontweight="bold", ha="center", va="center", zorder=7)
ax.text(aci(2052), 0.93, "fertility clock", color=METIN2, fontsize=14, fontweight="bold", ha="center", va="center", zorder=7)

# TÜRKİYE: sağlık saati (iç bant) → doğurganlık saati (dış nokta)
trr = tt.set_index("Location").loc["Türkiye"]
a_f, r_f = aci(BAS + 2 * trr["kutu"] + 1), 0.785 + 0.042 * trr["sira"]
a_h = aci(float(sg.set_index("Location").loc["Türkiye", "t0_saglik"])); r_h = taban - 0.09 * float(np.interp(BAS + a_h / (2 * np.pi) * (SON - BAS), yy, yog)) / 2
for (a_, r_) in [(a_f, r_f), (a_h, r_h)]:
    ax.scatter([a_], [r_], s=420, facecolor="none", edgecolor="#FFFFFF", linewidth=2.6, zorder=8)
yol_a = np.linspace(a_h, a_f, 60); yol_r = np.linspace(r_h, r_f, 60) - 0.10 * np.sin(np.linspace(0, np.pi, 60))
ax.plot(yol_a[3:-4], yol_r[3:-4], color="#FFFFFF", lw=2.2, zorder=8)
ax.annotate("", xy=(yol_a[-4], yol_r[-4]), xytext=(yol_a[-8], yol_r[-8]),
            arrowprops=dict(arrowstyle="-|>", color="#FFFFFF", lw=2.2, mutation_scale=18), zorder=8)
a_l, r_l = aci(1985.8), 1.60
ax.plot([a_f, a_l], [r_f + 0.04, r_l - 0.06], color="#FFFFFF", lw=1.2, alpha=0.8, zorder=8, clip_on=False)
ax.text(a_l, r_l, "Türkiye: health 1965 → fertility 1982", color="#FFFFFF", fontsize=15, fontweight="bold", ha="center", va="center", zorder=9)

# akrep: 2023
for lw, al in [(14, 0.10), (7, 0.22), (3, 1.0)]:
    ax.plot([aci(2023.5)] * 2, [0.50, 1.25], color=AKREP, lw=lw, alpha=al, solid_capstyle="round", zorder=6)
ax.text(aci(2023.5) + 0.09, 0.46, "2023", color=AKREP, fontsize=16, fontweight="bold", ha="center", va="center", zorder=7)

# merkez: aynı yol (kendi dönüm noktasına kaydırılmış 200 ülke + ortak eğri)
t0 = tt.set_index("Location")["t0"]
ic = fig.add_axes([MERKEZ_X - 0.075, MERKEZ_Y - 0.10, 0.15, 0.19], facecolor="none")
ic.axis("off"); ic.set_xlim(-90, 110); ic.set_ylim(0.6, 8.4)
bolge = df.drop_duplicates("Location").set_index("Location")["bolge"]
for u in Y.index:
    g = yil <= 2023
    ic.plot(yil[g] - t0[u], Y.loc[u].values[g], color=BOLGE[bolge[u]], lw=0.7, alpha=0.45)
z = np.linspace(-90, 110, 300)
egri = L + (U - L) / (1 + np.exp(K * z))
for lw, al in [(9, 0.08), (4.5, 0.2), (2.4, 1.0)]:
    ic.plot(z, egri, color=METIN, lw=lw, alpha=al, solid_capstyle="round")
ic.text(5, 8.0, "one shared path", color=METIN, fontsize=13, fontweight="bold", ha="left")
ic.text(5, 7.0, "R² = 0.94", color=METIN2, fontsize=12, ha="left")

fig.savefig(KOK / f"outputs/final_0_cover_clock2{SON_AD}.png", facecolor=ZEMIN, dpi=150)
print(f"Kaydedildi · {len(tt)} ülke noktası · dolu {int(tt['guvenilir'].sum())} · kesilen (t0 > {SON}) {(tt['t0'] > SON).sum()}")
