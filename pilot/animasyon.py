"""Hizalanma animasyonu: 200 ülkenin TFR çizgileri takvim zamanından demografik zamana kayar.
Çalıştırma (proje klasöründen):  python pilot/animasyon.py
Girdi : clean/countries_1950_2100.csv, clean/t0_tablosu.csv  (önce 04 notebook'u çalışmış olmalı)
Çıktı : outputs/final_anim_same_path.gif (1280x720, 15 fps, yaklaşık 13 sn, döngü)
Koyu sunum teması için:  TEMA=koyu python pilot/animasyon.py  → outputs/final_anim_same_path_dark.gif
        outputs/final_anim_ilk_kare.png, outputs/final_anim_son_kare.png
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.patheffects
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.collections import LineCollection

KOK = Path(__file__).resolve().parent.parent
KOYU = os.environ.get("TEMA") in ("koyu", "grafit", "acik")   # acik: açık renkler ama büyük yazı (taslak 2)
if os.environ.get("TEMA") == "grafit":   # 2. taslak: nötr koyu zemin
    MAVI, TURUNCU, YESIL, GRI = "#3987e5", "#d95926", "#199e70", "#A3A5AB"
    YAZI, YAZI2, ZEMIN, CIZGI, IZGARA = "#ECECEE", "#A3A5AB", "#1C1D21", "#2E3036", "#2E3036"
elif os.environ.get("TEMA") == "acik":
    MAVI, TURUNCU, YESIL, GRI = "#2a78d6", "#eb6834", "#1baf7a", "#9e9e9e"
    YAZI, YAZI2, ZEMIN, CIZGI, IZGARA = "#1F2328", "#52514e", "#FBFBF9", "#c9c8c3", "#E4E3DE"
elif KOYU:   # sunumun koyu paleti (renk körlüğü testinden geçen ilk 3 renk)
    MAVI, TURUNCU, YESIL, GRI = "#3987e5", "#d95926", "#199e70", "#8FA1AE"
    YAZI, YAZI2, ZEMIN, CIZGI, IZGARA = "#E8EEF2", "#9FB0BD", "#15222E", "#253645", "#253645"
else:
    MAVI, TURUNCU, YESIL, GRI = "#2a78d6", "#eb6834", "#1baf7a", "#9e9e9e"
    YAZI, YAZI2, ZEMIN, CIZGI, IZGARA = "#0b0b0b", "#52514e", "#fcfcfb", "#c9c8c3", "#e6e5e1"
FS = (1.6 if os.environ.get("SADE") == "1" else 1.15) if KOYU else 1.0   # slayt sürümü küçültüldüğü için yazılar büyük
SON = {"koyu": "_dark", "grafit": "_grafit", "acik": "_acik"}.get(os.environ.get("TEMA"), "") + ("_sade" if os.environ.get("SADE") == "1" else "")
U, L, K = 6.97, 1.67, 0.0816                       # 04 notebook'unun ortak eğrisi
VIDEO = os.environ.get("VIDEO") == "1"   # 30 Ekim: video kurgusu için yüksek çözünürlüklü kareler (slayt GIF'i değişmez)
FPS = 30 if VIDEO else 15

df = pd.read_csv(KOK / "clean/countries_1950_2100.csv")
df = df[df["pop2023"] >= 100]
t0 = pd.read_csv(KOK / "clean/t0_tablosu.csv").set_index("Location")["t0"]
tum = df.pivot(index="Location", columns="Time", values="TFR")
yil = tum.columns.values.astype(float)
gozlem = yil <= 2023
vurgu = {"Japan": TURUNCU, "Türkiye": MAVI, "Nigeria": YESIL}
etiket_yili = {"Japan": 1962, "Türkiye": 1986, "Nigeria": 2003}   # etiketin çizgi üzerindeki yeri
digerleri = [u for u in tum.index if u not in vurgu]

# --- zaman çizelgesi (saniye) ---
def zaman_cizelgesi():
    kareler = []
    # her kare: (e = kayma oranı, c = ortak eğri görünürlüğü, d = "bugün saat kaç?" sahnesi)
    for _ in range(int(1.5 * FPS)): kareler.append((0.0, 0.0, 0.0))     # 1) takvim görünümü
    n = int(3.5 * FPS)
    for i in range(n):                                                   # 2) kayma (yumuşak başla-bitir)
        s = i / (n - 1); kareler.append((s * s * (3 - 2 * s), 0.0, 0.0))
    for _ in range(int(1.0 * FPS)): kareler.append((1.0, 0.0, 0.0))
    n = int(1.0 * FPS)
    for i in range(n): kareler.append((1.0, (i + 1) / n, 0.0))         # 3) ortak eğri belirir
    for _ in range(int(1.5 * FPS)): kareler.append((1.0, 1.0, 0.0))
    n = int(1.0 * FPS)
    for i in range(n): kareler.append((1.0, 1.0, (i + 1) / n))          # 4) 2023'teki konumlar belirir
    for _ in range(int(3.5 * FPS)): kareler.append((1.0, 1.0, 1.0))
    # ilk kare = son sahne: PDF'e aktarılınca GIF'in sadece ilk karesi görünür; döngüde de kesintisiz geçiş olur
    return kareler if VIDEO else [(1.0, 1.0, 1.0)] + kareler   # videoda döngü takvim görünümüyle başlar
KARELER = zaman_cizelgesi()

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=150 if VIDEO else 100)
fig.patch.set_facecolor(ZEMIN); ax.set_facecolor(ZEMIN)
fig.subplots_adjust(top=0.80, bottom=0.12, left=0.07, right=0.97)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
for s in ["left", "bottom"]: ax.spines[s].set_color(CIZGI)
ax.grid(color=IZGARA, lw=0.8); ax.set_axisbelow(True)
ax.set_ylim(0.5, 9); ax.set_ylabel("Total fertility rate (births per woman)", color=YAZI2, fontsize=12 * FS)
ax.tick_params(colors=YAZI2, labelsize=11 * FS)
ax.axhline(2.1, color=YAZI2, lw=0.8, ls=":")
ax.text(0.005, (2.1 - 0.5) / (9 - 0.5) + 0.015, "replacement level 2.1", transform=ax.transAxes, color=YAZI2, fontsize=10 * FS,
        bbox=dict(facecolor=ZEMIN, edgecolor="none", alpha=0.85, pad=1.5), zorder=5)

gri = LineCollection([], colors=GRI, linewidths=0.6, alpha=0.25)
ax.add_collection(gri)
duz, kesik, etiket = {}, {}, {}
for u, r in vurgu.items():
    duz[u], = ax.plot([], [], color=r, lw=2.6, zorder=3)
    kesik[u], = ax.plot([], [], color=r, lw=2.1, ls=(0, (4, 3)), zorder=3)
    etiket[u] = ax.text(0, 0, u, color=r, fontsize=13 * FS, fontweight="bold", zorder=8 if VIDEO else 4, ha="left",
                        va="top" if u == "Japan" else "bottom")
    if VIDEO:   # ülke adı ortak eğrinin ve gri çizgilerin altında kalmasın
        etiket[u].set_path_effects([matplotlib.patheffects.withStroke(linewidth=5, foreground=ZEMIN)])
z = np.linspace(-110, 140, 400)
ortak, = ax.plot(z, L + (U - L) / (1 + np.exp(K * z)), color=YAZI, lw=2.2, zorder=4, alpha=0)
ortak_yazi = ax.text(-104, 7.25, "one shared S-curve", color=YAZI, fontsize=12 * FS, alpha=0)
# 4. sahne: 2023'teki konumlar ("demografik saat")
# t0'ların birkaç yıllık belirsizliği var (Türkiye 1979–1983, Japonya 1930–1946), bu yüzden saat 10'a yuvarlanır
saat = {u: int(10 * np.floor((2023 - t0[u]) / 10 + 0.5)) for u in vurgu}
yazi_yeri = ({"Nigeria": (10, 5.9), "Türkiye": (52, 4.3), "Japan": (100, 3.0)} if os.environ.get("SADE") == "1"
             else {"Nigeria": (12, 5.7), "Türkiye": (57, 3.95), "Japan": (100, 3.05)})
nokta, not_ = {}, {}
for u, r in vurgu.items():
    x23, y23 = 2023 - t0[u], tum.at[u, 2023]
    nokta[u] = ax.scatter([x23], [y23], s=0, color=r, edgecolor=ZEMIN, linewidth=2, zorder=6)
    if os.environ.get("SADE") == "1":
        ikinci = "at its turning point" if saat[u] == 0 else f"≈ {saat[u]} years past it"
    else:
        ikinci = "at its turning point" if saat[u] == 0 else f"≈ {saat[u]} years past its turning point"
    not_[u] = ax.annotate(f"{u} in 2023\n{ikinci}", (x23, y23), xytext=yazi_yeri[u],
                          ha="left" if u == "Nigeria" else "center", va="center", fontsize=12.5 * FS, color=r, fontweight="bold",
                          bbox=dict(facecolor=ZEMIN, edgecolor="none", alpha=0.9, pad=2),
                          arrowprops=dict(arrowstyle="-", color=r, lw=1.2, shrinkA=2, shrinkB=6), zorder=7, alpha=0)
    not_[u].arrow_patch.set_alpha(0)
proj_cizgi = ax.axvline(2023.5, color=YAZI2, lw=0.9)
proj_yazi = ax.text(2026, 8.55, "UN projection →", color=YAZI2, fontsize=11 * FS)

SADE = os.environ.get("SADE") == "1"     # slayt sürümü: başlık ve kaynak satırı slaytta, animasyonda yok
if SADE:
    fig.subplots_adjust(top=0.90, bottom=0.11)
else:
    fig.text(0.015, 0.965, "Countries walk the same fertility path; they differ mainly in when",
             fontsize=19 * FS, fontweight="bold", color=YAZI, va="top")
UST = 0.975 if SADE else 0.895
alt_takvim = fig.text(0.015, UST, "By calendar year: fertility paths look scattered   ·   R² = 27%",
                      fontsize=14 * FS, color=YAZI2, va="top")
alt_demo = fig.text(0.015, UST, "Each country shifted to its own turning point (t₀): one path   ·   R² = 94%",
                    fontsize=14 * FS, color=YAZI2, va="top", alpha=0)
alt_saat = fig.text(0.015, UST, f"2023: Nigeria at its turning point · Türkiye ≈ {saat['Türkiye']} yrs past · Japan ≈ {saat['Japan']} yrs past",
                    fontsize=14 * FS, color=YAZI2, va="top", alpha=0)
xetiket_takvim = fig.text(0.52, 0.035, "Year", ha="center", fontsize=12 * FS, color=YAZI2)
xetiket_demo = fig.text(0.52, 0.035, "Years since the country's turning point (t₀)", ha="center", fontsize=12 * FS, color=YAZI2, alpha=0)
if not SADE: fig.text(0.015, 0.008, "200 countries · solid: UN estimates 1950–2023 · dashed: UN WPP 2024 Medium projection · "
         "turning points estimated from 1950–2023 only",
         fontsize=9 * FS, color=YAZI2)

def ciz(kare):
    e, c, d = KARELER[kare]
    # eksen sınırları takvimden demografik zamana kayar
    ax.set_xlim(1946 + e * (-110 - 1946), 2104 + e * (140 - 2104))
    # gri çizgiler (sadece gözlem dönemi)
    gri.set_segments([np.column_stack([yil[gozlem] - e * t0[u], tum.loc[u].values[gozlem]]) for u in digerleri])
    for u in vurgu:
        x = yil - e * t0[u]; y = tum.loc[u].values
        duz[u].set_data(x[gozlem], y[gozlem]); kesik[u].set_data(x[yil >= 2023], y[yil >= 2023])
        ey = etiket_yili[u]
        dy = -0.35 if u == "Japan" else 0.18                       # Japonya etiketi çizginin altında
        etiket[u].set_position((ey - e * t0[u] + 1.5 * (1 - e) + 3 * e, tum.at[u, ey] + dy))
        etiket[u].set_alpha(1 - d)                                    # 4. sahnede yerini yeni yazılara bırakır
        nokta[u].set_sizes([150 * min(1.0, 1.6 * d)])
        not_[u].set_alpha(d); not_[u].arrow_patch.set_alpha(d)
    # yazıların geçişi
    a_takvim = float(np.clip(1 - e / 0.15, 0, 1)); a_demo = float(np.clip((e - 0.85) / 0.15, 0, 1))
    ax.tick_params(axis="x", labelcolor=matplotlib.colors.to_rgba(YAZI2, max(a_takvim, a_demo)))
    xetiket_takvim.set_alpha(a_takvim); xetiket_demo.set_alpha(a_demo)
    proj_cizgi.set_alpha(a_takvim); proj_yazi.set_alpha(a_takvim)
    # alt başlıklar: önce biri kaybolur, sonra öteki belirir
    alt_takvim.set_alpha(float(np.clip(1 - 2 * c, 0, 1)))
    alt_demo.set_alpha(float(np.clip(2 * c - 1, 0, 1) * np.clip(1 - 2 * d, 0, 1)))
    alt_saat.set_alpha(float(np.clip(2 * d - 1, 0, 1)))
    ortak.set_alpha(c); ortak_yazi.set_alpha(c)
    return []

if VIDEO:
    klasor = Path(os.environ["VIDEO_KLASOR"]); klasor.mkdir(parents=True, exist_ok=True)
    for i in range(len(KARELER)):
        ciz(i); fig.savefig(klasor / f"kare_{i:05d}.png", facecolor=ZEMIN)
    print(f"{len(KARELER)} kare, {len(KARELER) / FPS:.2f} sn → {klasor}"); raise SystemExit
ciz(1); fig.savefig(KOK / f"outputs/final_anim_ilk_kare{SON}.png", facecolor=ZEMIN)
ciz(len(KARELER) - 1); fig.savefig(KOK / f"outputs/final_anim_son_kare{SON}.png", facecolor=ZEMIN)
anim = FuncAnimation(fig, ciz, frames=len(KARELER), blit=False)
anim.save(KOK / f"outputs/final_anim_same_path{SON}.gif", writer=PillowWriter(fps=FPS), savefig_kwargs={"facecolor": ZEMIN})
boyut = (KOK / f"outputs/final_anim_same_path{SON}.gif").stat().st_size / 1e6
print(f"{len(KARELER)} kare, {len(KARELER) / FPS:.1f} sn, {boyut:.1f} MB")
