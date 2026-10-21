"""Q3 "Sağlık önce mi geliyor?": sağlık saati (yaşam beklentisinin en hızlı yükseldiği yıl) ile doğurganlık saati (t0).
Sağlık saati, t0 ile aynı yöntemle bulunur: tek ortak S eğrisi + ülke başına zaman kayması, sadece 1950–2023 verisiyle
(kesif/a_wpp/kesif_wpp.py ile aynı hesap). Karşılaştırma, dönüm noktası veride görülen 115 ülkede yapılır.
Çalıştırma:  python pilot/saglik_saati.py          → koyu (mavi) tema
             TEMA=acik python pilot/saglik_saati.py → açık tema
Çıktı: clean/saglik_saati.csv, outputs/v3_s3_health{_a}.png"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parent.parent
TEMA = os.environ.get("TEMA", "mavi")
ACIK = TEMA == "acik"
SON = "_a" if ACIK else ""
KART, YAZI, YAZI2, IZGARA = ("#FBFBF9", "#1F2328", "#5E6873", "#E4E3DE") if ACIK else ("#15222E", "#E8EEF2", "#9FB0BD", "#253645")
VURGU = "#1F2328" if ACIK else "#FFFFFF"
BOLGE = {"Asia": "#3987e5", "Africa": "#d95926", "Europe": "#199e70",
         "Latin America and the Caribbean": "#c98500", "Northern America": "#d55181", "Oceania": "#9085e9"}
if ACIK:
    BOLGE = {"Asia": "#2a78d6", "Africa": "#eb6834", "Europe": "#1baf7a",
             "Latin America and the Caribbean": "#eda100", "Northern America": "#e87ba4", "Oceania": "#6250d6"}
KISA = {"Latin America and the Caribbean": "Latin America", "Northern America": "N. America"}

# ---------- sağlık saati: ortak eğri + zaman kayması (t0 ile aynı "dene-düzelt" algoritması) ----------
t0 = pd.read_csv(KOK / "clean/t0_tablosu.csv").set_index("LocID")
d = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["LocID", "Time", "LEx"])
Y = d[(d["Time"] <= 2023) & d["LocID"].isin(t0.index)].pivot(index="LocID", columns="Time", values="LEx").reindex(t0.index)

def egri(z, L, U, k):                       # k < 0 iken yükselen S eğrisi: L'den U'ya
    return L + (U - L) / (1 + np.exp(k * z))
yil = Y.columns.values.astype(float)
aday = np.arange(1850, 2150.5, 0.5)
kayma = Y.apply(lambda r: r.index[np.argmax(r.values >= 55)] if (r >= 55).any() else 2030, axis=1).astype(float)
for _ in range(8):                          # 1) kaymalar sabitken ortak eğri, 2) eğri sabitken her ülkenin kayması
    z = (yil[None, :] - kayma.values[:, None]).ravel()
    (L, U, k), _ = curve_fit(egri, z, Y.values.ravel(), p0=[75, 35, -0.05], maxfev=20000)
    tablo = egri(yil[None, :] - aday[:, None], L, U, k)
    hata = ((tablo[None] - Y.values[:, None, :]) ** 2).sum(2)
    kayma = pd.Series(aday[hata.argmin(1)], index=Y.index)
kayma = kayma.where((kayma > 1850.5) & (kayma < 2149.5))     # sınıra dayananlar belirsiz
print(f"ortak LEx eğrisi: {L:.1f} → {U:.1f} yıl, k = {k:.3f}")

s = t0[["Location", "ISO3_code", "bolge", "t0", "guvenilir"]].copy()
s["t0_saglik"] = kayma
s["fark"] = s["t0"] - s["t0_saglik"]                      # + ise sağlık önce döndü
s.reset_index().to_csv(KOK / "clean/saglik_saati.csv", index=False)

g = s[s["guvenilir"] & s["t0_saglik"].notna()].copy()
r, p = spearmanr(g["t0_saglik"], g["t0"])
ri = spearmanr(g.groupby("bolge")["t0_saglik"].rank(pct=True), g.groupby("bolge")["t0"].rank(pct=True))[0]
once = (g["fark"] > 0).mean()
print(f"n = {len(g)}, ρ = {r:.3f} (p = {p:.1e}), bölge içi ρ = {ri:.2f}, sağlık önce = %{100 * once:.0f}, "
      f"medyan fark = {g['fark'].median():.1f} yıl (IQR {g['fark'].quantile(.25):.0f}–{g['fark'].quantile(.75):.0f})")
print(g.set_index("Location").loc[["Türkiye", "Republic of Korea", "Brazil", "India", "Bangladesh"], ["t0_saglik", "t0", "fark"]].round(1))

# ---------- slayt grafiği ----------
plt.rcParams.update({"figure.facecolor": KART, "axes.facecolor": KART, "savefig.facecolor": KART, "axes.edgecolor": IZGARA,
                     "axes.labelcolor": YAZI2, "xtick.color": YAZI2, "ytick.color": YAZI2, "text.color": YAZI,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": IZGARA,
                     "grid.linewidth": 0.8, "font.size": 14, "xtick.labelsize": 13, "ytick.labelsize": 13})
fig, ax = plt.subplots(figsize=(9.92, 4.66))
lo, hi = 1925, 2030
ax.fill_between([lo, hi], [lo, hi], [hi, hi], color=VURGU, alpha=0.035, lw=0)
ax.plot([lo, hi], [lo, hi], color=YAZI2, lw=1.4, ls=(0, (4, 3)))
ax.text(2004, 2000.5, "same year", color=YAZI2, fontsize=12.5, rotation=31, ha="center", va="bottom")
for b, renk in BOLGE.items():
    x = g[g["bolge"] == b]
    if len(x): ax.scatter(x["t0_saglik"], x["t0"], s=58, color=renk, edgecolor=KART, lw=1.2, zorder=3, label=KISA.get(b, b))
tr = g.set_index("Location").loc["Türkiye"]
ax.scatter(tr["t0_saglik"], tr["t0"], s=240, facecolor="none", edgecolor=VURGU, lw=2.2, zorder=4)
ax.annotate(f"Türkiye: health {tr['t0_saglik']:.0f}, fertility {tr['t0']:.0f}", (tr["t0_saglik"], tr["t0"]), xytext=(1977, 1969.5),
            textcoords="data", ha="left", va="center", fontsize=13.5, fontweight="bold", color=VURGU,
            arrowprops=dict(arrowstyle="-", color=VURGU, lw=1.2))
ax.text(1930, 2023, f"Above the line: health turned first\n{100 * once:.0f}% of countries · median {g['fark'].median():.0f} years earlier",
        fontsize=14, color=YAZI, va="top", linespacing=1.4)
ax.text(1930, 2004.5, f"ρ = {r:.2f}", fontsize=14, color=YAZI, fontweight="bold", va="top")
ax.set_xlim(lo, hi); ax.set_ylim(1950, 2025)
ax.set_xlabel("Health clock: year life expectancy rose fastest", fontsize=13.5)
ax.set_ylabel("Fertility clock (turning point)", fontsize=13.5)
ax.legend(loc="lower right", frameon=False, fontsize=12.5, ncol=3, handletextpad=0.2, columnspacing=1.0, labelcolor=YAZI2)
fig.subplots_adjust(left=0.085, right=0.985, top=0.97, bottom=0.135)
fig.savefig(KOK / f"outputs/v3_s3_health{SON}.png", dpi=200); plt.close(fig)
print("yazıldı:", f"outputs/v3_s3_health{SON}.png")
