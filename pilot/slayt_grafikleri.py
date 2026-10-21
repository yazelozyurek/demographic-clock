"""Final sunumdaki grafiklerin slayt boyutundaki sürümleri (büyük yazı, başlıksız: başlık slaytta).
Çalıştırma (proje klasöründen veya herhangi bir yerden):  python pilot/slayt_grafikleri.py
Önce 04 ve 05 notebook'ları çalışmış olmalı (clean/t0_tablosu.csv, clean/para_okul_tablosu.csv)."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "outputs"
MAVI, TURUNCU, YESIL, GRI = "#2a78d6", "#eb6834", "#1baf7a", "#9e9e9e"
YAZI, YAZI2, ZEMIN = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": ZEMIN, "axes.facecolor": ZEMIN, "savefig.facecolor": ZEMIN,
    "axes.edgecolor": "#c9c8c3", "axes.labelcolor": YAZI2, "xtick.color": YAZI2, "ytick.color": YAZI2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": "#e6e5e1", "grid.linewidth": 0.8, "font.size": 15, "axes.titlesize": 16,
    "axes.labelsize": 15, "xtick.labelsize": 14, "ytick.labelsize": 14, "legend.fontsize": 14,
})
DPI = 200    # figsize (inç) × 100 = slayttaki piksel boyutu; 200 dpi = keskin görüntü

df = pd.read_csv(KOK / "clean/countries_1950_2100.csv", low_memory=False)
df = df[df["pop2023"] >= 100]
t0 = pd.read_csv(KOK / "clean/t0_tablosu.csv").set_index("Location")
po = pd.read_csv(KOK / "clean/para_okul_tablosu.csv")

# ---------- Slayt 1: yenilenme düzeyinin altındaki ülke sayısı ----------
sayi = df.assign(alt=df["TFR"] < 2.1).groupby("Time")["alt"].sum()
fig, ax = plt.subplots(figsize=(7.6, 4.1))
ax.plot(sayi.loc[:2023], color=MAVI, lw=3, label="UN estimate")
ax.plot(sayi.loc[2023:], color=MAVI, lw=2.4, ls=(0, (4, 3)), label="UN projection")
ax.axvline(2023.5, color=YAZI2, lw=0.8)
for y, ha, dx, dy in [(1950, "left", 10, 62), (2023, "right", -12, 14), (2100, "right", -12, 14)]:
    ax.scatter([y], [sayi[y]], s=60, color=MAVI, edgecolor=ZEMIN, linewidth=1.5, zorder=3)
    ax.annotate(f"{sayi[y]} in {y}", (y, sayi[y]), xytext=(dx, dy),
                textcoords="offset points", ha=ha, fontsize=15, color=YAZI, fontweight="bold")
ax.set_ylim(0, 215); ax.set_xlim(1950, 2101)
ax.set_ylabel("Countries (of 200)")
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(CIKTI / "slide1_below_replacement.png", dpi=DPI); plt.close(fig)
print("slayt 1:", sayi[1950], sayi[2023], sayi[2100])

# ---------- Slayt 3: dönüm noktasında gelir ve eğitim (adil ölçek) ----------
def yillik(veri, kodlar):
    veri = veri[veri["ISO3_code"].isin(kodlar) & (veri["deger"] > 0)]
    s = {}
    for kod, d in veri.groupby("ISO3_code"):
        d = d.sort_values("year"); yy = np.arange(d["year"].min(), d["year"].max() + 1)
        s[kod] = pd.Series(np.interp(yy, d["year"], np.log(d["deger"])), index=yy)
    return pd.DataFrame(s).loc[1950:2015]
kodlar = t0["ISO3_code"]
G = yillik(pd.read_csv(KOK / "data_dis/gdp-per-capita-maddison-project-database.csv")
           .rename(columns={"code": "ISO3_code", "gdp_per_capita": "deger"}), kodlar)
E = yillik(pd.read_csv(KOK / "data_dis/barrolee_BL_v3_F2534.csv")
           .rename(columns={"WBcode": "ISO3_code", "yr_sch": "deger"}), kodlar)
po["yil"] = po["t0"].round().astype(int)
po["z_gelir"] = [(np.log(v) - np.log(po["gelir"]).median()) / G.loc[y].std() for v, y in zip(po["gelir"], po["yil"])]
po["z_egitim"] = [(np.log(v) - np.log(po["egitim"]).median()) / E.loc[y].std() for v, y in zip(po["egitim"], po["yil"])]

fig, a = plt.subplots(figsize=(9.8, 4.3))
etiket = {"Bangladesh": ("Bangladesh", -1, -1), "Türkiye": ("Türkiye", 1, 1),
          "Saudi Arabia": ("Saudi Arabia", -1, 1), "Republic of Korea": ("Rep. of Korea", 1, -1)}
rng = np.random.default_rng(3)
for satir, sutun in enumerate(["z_egitim", "z_gelir"]):
    yk = satir + rng.uniform(-0.12, 0.12, len(po))
    etiketli = po["Location"].isin(etiket)
    yk[etiketli.values] = satir
    a.hlines(satir, po[sutun].quantile(0.1), po[sutun].quantile(0.9), color="#c9c8c3", lw=12, zorder=0, capstyle="round")
    a.scatter(po[sutun][~etiketli], yk[~etiketli.values], s=48, color=GRI, alpha=0.75, edgecolor=ZEMIN, linewidth=1.2, zorder=2)
    for ulke, (ad, yon_e, yon_g) in etiket.items():
        j = np.where(po["Location"] == ulke)[0][0]
        r = MAVI if ulke == "Türkiye" else YAZI
        yon = yon_e if sutun == "z_egitim" else yon_g
        a.scatter(po[sutun].iloc[j], satir, s=95, color=r, edgecolor=ZEMIN, linewidth=1.5, zorder=3)
        a.annotate(ad, (po[sutun].iloc[j], satir), xytext=(0, 30 * yon), textcoords="offset points",
                   ha="center", va="center", fontsize=14, color=r, fontweight="bold" if ulke == "Türkiye" else None,
                   arrowprops=dict(arrowstyle="-", color=r, lw=0.8, shrinkA=0, shrinkB=5))
a.axvline(0, color=YAZI2, lw=0.8, ls=":")
a.text(0.02, 1.48, "typical country", fontsize=13, color=YAZI2)
a.set_yticks([0, 1], ["Young women's\nschooling", "Income\nper person"])
a.set_ylim(-0.6, 1.6); a.grid(axis="y", visible=False)
a.set_xlabel("Distance from the typical country, in units of that year's world spread")
fig.tight_layout()
fig.savefig(CIKTI / "slide3_spread.png", dpi=DPI); plt.close(fig)

# ---------- Slayt 4: Türkiye nüfusu ve UN tahmin aralıkları ----------
ov = pd.read_csv(KOK / "data/WPP2024_Demographic_Indicators_OtherVariants_csv.gz", encoding="utf-8-sig",
                 usecols=["LocID", "Variant", "Time", "TPopulation1July"])
ov = ov[(ov["LocID"] == 792) & ov["Variant"].str.contains("PI") & (ov["Time"] <= 2100)]
pi = ov.pivot(index="Time", columns="Variant", values="TPopulation1July") / 1000
trp = df[df["Location"] == "Türkiye"].set_index("Time")["TPopulation1July"] / 1000
zirve = trp.idxmax()
fig, a = plt.subplots(figsize=(9.2, 4.2))
a.fill_between(pi.index, pi["Lower 95 PI"], pi["Upper 95 PI"], color=MAVI, alpha=0.12, lw=0, label="95% prediction interval")
a.fill_between(pi.index, pi["Lower 80 PI"], pi["Upper 80 PI"], color=MAVI, alpha=0.22, lw=0, label="80% prediction interval")
a.plot(trp.loc[:2023], color=MAVI, lw=3, label="UN estimate")
a.plot(trp.loc[2023:], color=MAVI, lw=2.4, ls=(0, (4, 3)), label="UN Medium projection")
a.axvline(2023.5, color=YAZI2, lw=0.8)
a.scatter([zirve], [trp[zirve]], s=70, color=MAVI, edgecolor=ZEMIN, linewidth=1.5, zorder=3)
a.annotate(f"peak {zirve}: {trp[zirve]:.1f} M", (zirve, trp[zirve]), xytext=(-4, 16), textcoords="offset points",
           ha="center", fontsize=14, color=YAZI, fontweight="bold")
a.annotate(f"2100: {trp[2100]:.1f} M\n95%: {pi.at[2100, 'Lower 95 PI']:.0f}–{pi.at[2100, 'Upper 95 PI']:.0f} M",
           (2100, trp[2100]), xytext=(-10, -16), textcoords="offset points", ha="right", va="top", fontsize=14, color=YAZI)
a.set_ylabel("Population (millions)"); a.set_ylim(0, 135); a.set_xlim(1950, 2101)
a.legend(frameon=False, loc="upper left", fontsize=13)
fig.tight_layout()
fig.savefig(CIKTI / "slide4_population.png", dpi=DPI); plt.close(fig)
print("slayt 4: zirve", zirve, round(trp[zirve], 1), "| 2100", round(trp[2100], 1),
      round(pi.at[2100, "Lower 95 PI"], 1), round(pi.at[2100, "Upper 95 PI"], 1))

# ---------- Dışarıda kalan yerlerin tam listesi (slayt 1: "listed, not hidden") ----------
hepsi = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["Location", "pop2023"]).drop_duplicates()
t0t = pd.read_csv(KOK / "clean/t0_tablosu.csv")
aday = t0t[t0t["guvenilir"] & t0t["t0"].between(1952, 2013)]
liste = pd.concat([
    hepsi[hepsi["pop2023"] < 100].assign(reason="Under 100,000 people in 2023: not in any analysis"),
    t0t[~t0t["Location"].isin(aday["Location"])].assign(reason="Turning point not seen in 1952–2013: clock only, not in money-or-school test"),
    aday[~aday["Location"].isin(po["Location"])].assign(reason="No Maddison income or Barro–Lee schooling data: not in money-or-school test"),
])[["Location", "pop2023", "reason"]].rename(columns={"pop2023": "population_2023_thousands"})
liste.to_csv(CIKTI / "excluded_places.csv", index=False)
print("dışarıda kalanlar:", liste["reason"].str[:20].value_counts().to_dict())
