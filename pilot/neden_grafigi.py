"""Q4 slayt grafikleri (koyu tema): doğal deney saçılım grafiği + Türkiye nüfus aralığı (kompakt).
Doğal deney: Kreitmeir & Überfuhr (2024) ülke düzeyi tahmini ölüm aracı (kesif/f_kreitmeir/, ön kayıt commit 52407d4).
x = 1940'lardaki ilaç ve aşıların öngördüğü yıllık ölüm düşüşü (13 bulaşıcı hastalık, 1.000 kişi başına), y = ΔTFR 1950→1990 (WPP).
Çalıştırma (proje klasöründen):  python pilot/neden_grafigi.py
Çıktı: outputs/v3_s4_cause.png, outputs/v3_s4_pop_compact.png"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parent.parent
KART, YAZI, YAZI2, IZGARA, VURGU = "#15222E", "#E8EEF2", "#9FB0BD", "#253645", "#FFFFFF"
BOLGE = {"Asia": "#3987e5", "Africa": "#d95926", "Europe": "#199e70",
         "Latin America and the Caribbean": "#c98500", "Northern America": "#d55181", "Oceania": "#9085e9"}
KISA = {"Latin America and the Caribbean": "Latin America", "Northern America": "N. America"}
plt.rcParams.update({"figure.facecolor": KART, "axes.facecolor": KART, "savefig.facecolor": KART, "axes.edgecolor": IZGARA,
                     "axes.labelcolor": YAZI2, "xtick.color": YAZI2, "ytick.color": YAZI2, "text.color": YAZI,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": IZGARA,
                     "grid.linewidth": 0.8, "font.size": 14, "xtick.labelsize": 13, "ytick.labelsize": 13})
DPI = 200

df = pd.read_csv(KOK / "clean/countries_1950_2100.csv", low_memory=False)
df = df[df["pop2023"] >= 100]

# ---------- Q4: doğal deney (ana analizdeki 50 ülke) ----------
K = pd.read_csv(KOK / "data_dis/kreitmeir/ku_data.csv")
x = K[(K["kusample9and2ctry"] == 1) & K["changemortctry"].notna() & K["changelifeexpect"].notna()].set_index("iso3")
w = df.pivot_table(index="ISO3_code", columns="Time", values="TFR")
bolge = df.drop_duplicates("ISO3_code").set_index("ISO3_code")["bolge"]
ad = df.drop_duplicates("ISO3_code").set_index("ISO3_code")["Location"]
x["dusus"] = -10 * x["changemortctry"]                       # 100 kişi başına → 1.000 kişi başına, pozitif = düşüş
x["dTFR"] = (w[1990] - w[1950]).reindex(x.index)
x["bolge"] = bolge.reindex(x.index); x["ad"] = ad.reindex(x.index)
x = x.dropna(subset=["dTFR"])
assert len(x) == 50, len(x)
r = sm.OLS(x["dTFR"], sm.add_constant(x["dusus"])).fit()

fig, a = plt.subplots(figsize=(9.0, 4.0))
xs = np.linspace(0, x["dusus"].max() * 1.04, 50)
a.plot(xs, r.params.iloc[0] + r.params.iloc[1] * xs, color=VURGU, lw=1.6, ls=(0, (5, 3)), zorder=2)
for b, renk in BOLGE.items():
    for zengin, dolgu in [(0, renk), (1, "none")]:
        s = x[(x["bolge"] == b) & (x["startrich"] == zengin)]
        if len(s):
            a.scatter(s["dusus"], s["dTFR"], s=62, facecolor=dolgu, edgecolor=renk if zengin else KART, lw=1.8 if zengin else 1.1,
                      zorder=3, label=KISA.get(b, b) if zengin == 0 or not len(x[(x["bolge"] == b) & (x["startrich"] == 0)]) else None)
etiket = {"LKA": (8, 6, "left"), "MEX": (8, -6, "left"), "KOR": (8, 0, "left"), "GTM": (-9, 0, "right"), "EGY": (8, -6, "left")}
for iso, (dx, dy, ha) in etiket.items():
    if iso in x.index:
        a.annotate({"KOR": "Rep. of Korea", "USA": "United States"}.get(iso, x.at[iso, "ad"]), (x.at[iso, "dusus"], x.at[iso, "dTFR"]),
                   xytext=(dx, dy), textcoords="offset points", ha=ha, va="center", fontsize=12.5, color=YAZI)
a.text(0.99, 0.97, "More deaths prevented →\nlarger fall in children per woman", transform=a.transAxes, ha="right", va="top",
       fontsize=13.5, color=YAZI, fontweight="bold", linespacing=1.35)
a.scatter([], [], s=62, facecolor="none", edgecolor=YAZI2, lw=1.8, label="rich in 1940")
h, l = a.get_legend_handles_labels()
fig.legend(h, l, loc="upper left", bbox_to_anchor=(0.005, 0.995), frameon=False, fontsize=12, ncol=7, handletextpad=0.1,
           columnspacing=0.9, labelcolor=YAZI2)
a.axhline(0, color=YAZI2, lw=0.8)
a.set_xlim(0, x["dusus"].max() * 1.06)
a.set_xlabel("Deaths per 1,000 people a year that the 1940s medicines could prevent (13 diseases)", fontsize=13)
a.set_ylabel("Change in children\nper woman, 1950→1990", fontsize=13)
fig.subplots_adjust(left=0.105, right=0.985, top=0.9, bottom=0.15)
fig.savefig(KOK / "outputs/v3_s4_cause.png", dpi=DPI); plt.close(fig)
print(f"Q4: n = {len(x)}, eğim {r.params.iloc[1]:+.3f} çocuk / (1.000 kişide 1 ölüm), p = {r.pvalues.iloc[1]:.4f}; "
      f"x aralığı {x['dusus'].min():.1f}–{x['dusus'].max():.1f}")

# ---------- Türkiye nüfusu + UN tahmin aralıkları (kompakt, büyük yazı) ----------
ov = pd.read_csv(KOK / "data/WPP2024_Demographic_Indicators_OtherVariants_csv.gz", encoding="utf-8-sig",
                 usecols=["LocID", "Variant", "Time", "TPopulation1July"])
ov = ov[(ov["LocID"] == 792) & ov["Variant"].str.contains("PI") & (ov["Time"] <= 2100)]
pi = ov.pivot(index="Time", columns="Variant", values="TPopulation1July") / 1000
trp = df[df["Location"] == "Türkiye"].set_index("Time")["TPopulation1July"] / 1000
zirve = trp.idxmax()
fig, a = plt.subplots(figsize=(6.68, 2.3))
a.fill_between(pi.index, pi["Lower 95 PI"], pi["Upper 95 PI"], color="#3987e5", alpha=0.18, lw=0)
a.fill_between(pi.index, pi["Lower 80 PI"], pi["Upper 80 PI"], color="#3987e5", alpha=0.32, lw=0)
for k, al in [(4.0, 0.10), (2.2, 0.18), (1.0, 1.0)]:
    a.plot(trp.loc[:2023].index, trp.loc[:2023], color="#5FA0F0", lw=2.8 * k, alpha=al, solid_capstyle="round")
    a.plot(trp.loc[2023:].index, trp.loc[2023:], color="#5FA0F0", lw=2.2 * k, alpha=al, ls=(0, (3, 2)))
a.scatter([zirve], [trp[zirve]], s=60, color=VURGU, zorder=5)
a.annotate(f"peak {zirve}: {trp[zirve]:.0f} M", (zirve, trp[zirve]), xytext=(0, 12), textcoords="offset points",
           ha="center", fontsize=13.5, color=VURGU, fontweight="bold")
a.annotate(f"2100, 95%:\n{pi.at[2100, 'Lower 95 PI']:.0f}–{pi.at[2100, 'Upper 95 PI']:.0f} M", (2100, pi.at[2100, "Lower 95 PI"]),
           xytext=(-6, 4), textcoords="offset points", ha="right", va="bottom", fontsize=13, color=YAZI)
a.text(1953, 128, "shaded: UN 80% / 95%", fontsize=12.5, color=YAZI2, va="top")
a.axvline(2023.5, color=YAZI2, lw=0.8)
a.set_ylabel("Millions", fontsize=13); a.set_ylim(0, 135); a.set_xlim(1950, 2101); a.set_xticks([1950, 2000, 2050, 2100])
fig.subplots_adjust(left=0.12, right=0.975, top=0.95, bottom=0.14)
fig.savefig(KOK / "outputs/v3_s4_pop_compact.png", dpi=DPI); plt.close(fig)
print("yazıldı: outputs/v3_s4_cause.png, outputs/v3_s4_pop_compact.png")
