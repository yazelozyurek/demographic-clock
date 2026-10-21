"""Koyu temalı, renkli slayt grafikleri (final sunum v3).
Çalıştırma:  python pilot/slayt_koyu.py   (önce 04 ve 05 çalışmış olmalı)
Palet: dataviz koyu paleti, #0F1A24 zemininde renk körlüğü testinden geçti (6 bölge)."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "outputs"
import os
TEMA = os.environ.get("TEMA", "mavi")                                          # mavi (taslak 1) · grafit · acik (taslak 2)
GRAFIT, ACIK = TEMA == "grafit", TEMA == "acik"
SON = {"grafit": "_g", "acik": "_a"}.get(TEMA, "")
ZEMIN, KART = {"grafit": ("#141518", "#1C1D21"), "acik": ("#F3F2EE", "#FBFBF9")}.get(TEMA, ("#0F1A24", "#15222E"))
YAZI, YAZI2, IZGARA = {"grafit": ("#ECECEE", "#A3A5AB", "#2E3036"),
                       "acik": ("#1F2328", "#5E6873", "#E4E3DE")}.get(TEMA, ("#E8EEF2", "#9FB0BD", "#253645"))
ORTA = {"grafit": "#2B2D33", "acik": "#F1F0EC"}.get(TEMA, "#1E2E3C")              # ısı haritasının nötr ortası
VURGU = "#1F2328" if ACIK else "#FFFFFF"                                         # dünya çizgisi, etiketler, halkalar
BOLGE = {"Asia": "#3987e5", "Africa": "#d95926", "Europe": "#199e70",
         "Latin America and the Caribbean": "#c98500", "Northern America": "#d55181", "Oceania": "#9085e9"}
if ACIK:   # dataviz açık paleti (açık zeminde testten geçti; düşük kontrastlı renkler hep etiketli)
    BOLGE = {"Asia": "#2a78d6", "Africa": "#eb6834", "Europe": "#1baf7a",
             "Latin America and the Caribbean": "#eda100", "Northern America": "#e87ba4", "Oceania": "#6250d6"}
KISA = {"Latin America and the Caribbean": "Latin America", "Northern America": "N. America"}
TFR_RENK = LinearSegmentedColormap.from_list("tfr", ["#2fb7ff", "#7a6cff", "#ff4f7a", "#ff6a2b"])   # kapakla aynı
plt.rcParams.update({
    "figure.facecolor": KART, "axes.facecolor": KART, "savefig.facecolor": KART,
    "axes.edgecolor": IZGARA, "axes.labelcolor": YAZI2, "xtick.color": YAZI2, "ytick.color": YAZI2,
    "text.color": YAZI, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": IZGARA, "grid.linewidth": 0.8, "font.size": 14, "axes.titlesize": 15,
    "xtick.labelsize": 13, "ytick.labelsize": 13, "legend.fontsize": 13,
})
DPI = 200
def parla(ax, x, y, renk, lw=2.6, ls="-"):
    for k, a in [(4.0, 0.10), (2.2, 0.18)]:
        ax.plot(x, y, color=renk, lw=lw * k, alpha=a, ls=ls, solid_capstyle="round")
    ax.plot(x, y, color=renk, lw=lw, ls=ls, solid_capstyle="round")

df = pd.read_csv(KOK / "clean/countries_1950_2100.csv", low_memory=False)
df = df[df["pop2023"] >= 100]

# ---------- S1-A: bölgelere göre TFR (nüfus ağırlıklı), 1950–2100 ----------
w = df.assign(wt=df["TFR"] * df["TPopulation1July"])
bt = w.groupby(["bolge", "Time"])[["wt", "TPopulation1July"]].sum()
bt = (bt["wt"] / bt["TPopulation1July"]).unstack(0)
dunya = w.groupby("Time")["wt"].sum() / w.groupby("Time")["TPopulation1July"].sum()
fig, ax = plt.subplots(figsize=(7.84, 2.42))
ax.axvspan(2023.5, 2100, color=VURGU, alpha=0.03, lw=0)
for b, r in BOLGE.items():
    parla(ax, bt.index[bt.index <= 2023], bt.loc[:2023, b], r)
    parla(ax, bt.index[bt.index >= 2023], bt.loc[2023:, b], r, lw=2, ls=(0, (3, 2)))
parla(ax, dunya.index[dunya.index <= 2023], dunya.loc[:2023], VURGU, lw=2.2)
parla(ax, dunya.index[dunya.index >= 2023], dunya.loc[2023:], VURGU, lw=1.8, ls=(0, (3, 2)))
son = bt.loc[2100].sort_values()
etiket_y = {}
yer = np.linspace(1.0, 4.4, len(son))                       # etiketleri üst üste binmesin diye yay
for (b, v), yy in zip(son.items(), yer):
    ax.text(2103, yy, KISA.get(b, b), color=BOLGE[b], fontsize=13, va="center", fontweight="bold")
ax.text(1952, 5.95, "World", color=VURGU, fontsize=13, fontweight="bold")
ax.axhline(2.1, color=YAZI2, lw=1, ls=":")
ax.text(2040, 2.18, "replacement 2.1", color=YAZI2, fontsize=12)
ax.text(2026, 6.4, "UN projection →", color=YAZI2, fontsize=12)
ax.set_xlim(1950, 2100); ax.set_ylim(0.8, 7)
ax.set_ylabel("Children per woman")
fig.subplots_adjust(left=0.075, right=0.785, top=0.97, bottom=0.12)
fig.savefig(CIKTI / f"v3_s1_regions{SON}.png", dpi=DPI); plt.close(fig)
print("S1-A dünya TFR 1950/2023/2100:", round(dunya[1950], 2), round(dunya[2023], 2), round(dunya[2100], 2))

# ---------- S1-B: TFR dağılımı, 4 yıl (histogram) ----------
yillar = [1950, 1990, 2023, 2100]
kutu = np.arange(0.5, 8.6, 0.4)
fig, axs = plt.subplots(1, 4, figsize=(7.84, 2.42), sharey=True)
for ax, y in zip(axs, yillar):
    v = df.loc[df["Time"] == y, "TFR"]
    n, kenar, yamalar = ax.hist(v, bins=kutu, edgecolor=KART, linewidth=1.2)
    for yama, sol in zip(yamalar, kenar[:-1]):
        yama.set_facecolor(TFR_RENK(np.clip((sol - 1) / 6, 0, 1)))
    ax.axvline(2.1, color=VURGU, lw=1, ls=":")
    ax.set_title(f"{y}" + (" (proj.)" if y > 2023 else "") + f"\n{(v < 2.1).sum()} below 2.1", color=YAZI, fontsize=13.5, fontweight="bold")
    ax.text(0.97, 0.95, f"median\n{v.median():.1f}", transform=ax.transAxes, ha="right", va="top", fontsize=12, color=YAZI2)
    ax.set_xticks([2, 4, 6, 8]); ax.grid(axis="x", visible=False)
axs[0].set_ylabel("Countries")
fig.subplots_adjust(left=0.09, right=0.99, top=0.80, bottom=0.12, wspace=0.12)
fig.savefig(CIKTI / f"v3_s1_hist{SON}.png", dpi=DPI); plt.close(fig)
print("S1-B medyanlar:", [round(df.loc[df.Time == y, "TFR"].median(), 2) for y in yillar])

# ---------- S1-C: korelasyon ısı haritası (2023) ----------
d23 = df[df["Time"] == 2023].copy()
d23["log IMR"] = np.log(d23["IMR"])
deg = {"TFR": "Fertility", "LEx": "Life exp.", "log IMR": "Infant mort. (log)", "MedianAgePop": "Median age",
       "MAC": "Mean age at birth", "CNMR": "Net migration"}                    # LE65 ≈ LEx, PopGrowth = aritmetik: kalabalık yapmasın
K = d23[list(deg)].corr().rename(index=deg, columns=deg)
ISI = LinearSegmentedColormap.from_list("isi", ["#3987e5", ORTA, "#e66767"])
K = K.iloc[1:, :-1]                                         # alt üçgen: her çift bir kez
M = np.where(np.tril(np.ones(K.shape), 0) == 1, K.values, np.nan)
fig, ax = plt.subplots(figsize=(7.84, 2.42))
ax.imshow(M, cmap=ISI, vmin=-1, vmax=1, aspect="auto")
for i in range(K.shape[0]):
    for j in range(K.shape[1]):
        v = M[i, j]
        if np.isnan(v): continue
        ax.text(j, i, f"{v:.2f}".replace("0.", ".").replace("-.", "−."), ha="center", va="center", fontsize=11,
                color=("#FFFFFF" if abs(v) > 0.5 else (YAZI if abs(v) > 0.35 else YAZI2)), fontweight="bold" if abs(v) > 0.8 else None)
KISA_D = {"Fertility": "Fertility", "Life exp.": "Life exp.", "Infant mort. (log)": "Infant mort.", "Median age": "Median age", "Mean age at birth": "Age at birth"}
ax.set_xticks(range(K.shape[1]), [KISA_D[c] for c in K.columns], rotation=25, ha="right", fontsize=11.5)
ax.set_yticks(range(K.shape[0]), K.index, fontsize=11.5)
fig.text(0.70, 0.78, "red: rise together", color="#C43B3B" if ACIK else "#e66767", fontsize=12, ha="left", fontweight="bold")
fig.text(0.70, 0.66, "blue: move opposite", color="#2563B8" if ACIK else "#5f9fec", fontsize=12, ha="left", fontweight="bold")
fig.text(0.70, 0.54, "bold: |r| > 0.8", color=YAZI2, fontsize=12.5, ha="left")
ax.grid(False)
for s in ax.spines.values(): s.set_visible(False)
fig.subplots_adjust(left=0.215, right=0.67, top=0.98, bottom=0.27)
fig.savefig(CIKTI / f"v3_s1_corr{SON}.png", dpi=DPI); plt.close(fig)
print("S1-C TFR–LEx r =", round(K.loc["Life exp.", "Fertility"], 2), "| TFR–median age r =", round(K.loc["Median age", "Fertility"], 2))

# ---------- S2-B: bölgelere göre dönüm yılı (t0) ----------
t0t = pd.read_csv(KOK / "clean/t0_tablosu.csv")
sira = ["Europe", "Northern America", "Latin America and the Caribbean", "Asia", "Oceania", "Africa"]
fig, ax = plt.subplots(figsize=(8.6, 2.5))
rng = np.random.default_rng(1)
for i, b in enumerate(sira):
    d = t0t[t0t["bolge"] == b]
    x = d["t0"].clip(upper=2078); y = i + rng.uniform(-0.22, 0.22, len(d))
    g = d["guvenilir"].values
    ax.scatter(x[g], y[g], s=30, color=BOLGE[b], edgecolor=KART, linewidth=0.6, zorder=3)
    ax.scatter(x[~g], y[~g], s=30, facecolor="none", edgecolor=BOLGE[b], linewidth=1.1, alpha=0.8, zorder=3)
    ax.text(2083, i, f"median {d['t0'].median():.0f}", color=BOLGE[b], fontsize=12, va="center", fontweight="bold")
for u, ad, dx, dy in [("Türkiye", "Türkiye", 9, 0.5), ("Republic of Korea", "Korea", -12, 0.5), ("Nigeria", "Nigeria", 0, 0.5)]:
    r = t0t[t0t["Location"] == u].iloc[0]; i = sira.index(r["bolge"])
    ax.annotate(ad, (r["t0"], i), xytext=(r["t0"] + dx, i + dy), color=VURGU, fontsize=12, ha="center", fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=VURGU, lw=0.8))
    ax.scatter([r["t0"]], [i], s=60, facecolor="none", edgecolor=VURGU, linewidth=1.6, zorder=4)
ax.set_yticks(range(len(sira)), [KISA.get(b, b) for b in sira], fontsize=12)
for t, b in zip(ax.get_yticklabels(), sira): t.set_color(BOLGE[b])
ax.set_xlim(1915, 2080); ax.set_ylim(-0.6, len(sira) - 0.1); ax.grid(axis="y", visible=False)
ax.axvline(2023.5, color=YAZI2, lw=0.8, ls=":")
ax.set_title("Turning point of each country (filled: well observed; hollow: inferred)", loc="left", color=YAZI, fontsize=13, fontweight="bold")
fig.subplots_adjust(left=0.15, right=0.82, top=0.86, bottom=0.12)
fig.savefig(CIKTI / f"v3_s2_turning{SON}.png", dpi=DPI); plt.close(fig)

# ---------- S3-A: dönüm noktasında gelir ve eğitim, bölge renkli ----------
po = pd.read_csv(KOK / "clean/para_okul_tablosu.csv")
def yillik(veri, kodlar):
    veri = veri[veri["ISO3_code"].isin(kodlar) & (veri["deger"] > 0)]
    s = {}
    for kod, d in veri.groupby("ISO3_code"):
        d = d.sort_values("year"); yy = np.arange(d["year"].min(), d["year"].max() + 1)
        s[kod] = pd.Series(np.interp(yy, d["year"], np.log(d["deger"])), index=yy)
    return pd.DataFrame(s).loc[1950:2015]
G = yillik(pd.read_csv(KOK / "data_dis/gdp-per-capita-maddison-project-database.csv")
           .rename(columns={"code": "ISO3_code", "gdp_per_capita": "deger"}), t0t["ISO3_code"])
E = yillik(pd.read_csv(KOK / "data_dis/barrolee_BL_v3_F2534.csv")
           .rename(columns={"WBcode": "ISO3_code", "yr_sch": "deger"}), t0t["ISO3_code"])
po["yil"] = po["t0"].round().astype(int)
po["z_gelir"] = [(np.log(v) - np.log(po["gelir"]).median()) / G.loc[y].std() for v, y in zip(po["gelir"], po["yil"])]
po["z_egitim"] = [(np.log(v) - np.log(po["egitim"]).median()) / E.loc[y].std() for v, y in zip(po["egitim"], po["yil"])]
isaret = {"Asia": "o", "Latin America and the Caribbean": "s", "Africa": "^", "Europe": "D"}
fig, a = plt.subplots(figsize=(8.22, 3.19))
rng = np.random.default_rng(3)
etiket = {"Bangladesh": ("Bangladesh", -1, -1), "Türkiye": ("Türkiye", 1, 1),
          "Saudi Arabia": ("Saudi Arabia", -1, 1), "Republic of Korea": ("Korea", 1, 1)}
for satir, sutun in enumerate(["z_egitim", "z_gelir"]):
    a.hlines(satir, po[sutun].quantile(0.1), po[sutun].quantile(0.9), color=VURGU, alpha=0.10, lw=16, capstyle="round", zorder=0)
    for b, m in isaret.items():
        d = po[po["bolge"] == b]
        a.scatter(d[sutun], satir + rng.uniform(-0.16, 0.16, len(d)), s=46, marker=m, color=BOLGE[b], edgecolor=KART,
                  linewidth=0.8, alpha=0.95, zorder=2)
    for ulke, (ad, ye, yg) in etiket.items():
        j = np.where(po["Location"] == ulke)[0][0]; yon = ye if sutun == "z_egitim" else yg
        a.scatter(po[sutun].iloc[j], satir, s=110, facecolor="none", edgecolor=VURGU, linewidth=1.8, zorder=3)
        a.annotate(ad, (po[sutun].iloc[j], satir), xytext=(0, 24 * yon), textcoords="offset points", ha="center", va="center",
                   fontsize=12.5, color=VURGU, fontweight="bold", arrowprops=dict(arrowstyle="-", color=VURGU, lw=0.8, shrinkB=6))
a.axvline(0, color=YAZI2, lw=0.8, ls=":")
a.set_yticks([0, 1], ["Young women's\nschooling", "Income\nper person"], fontsize=13)
a.set_ylim(-0.65, 1.75); a.set_xlim(-1.85, 1.75); a.grid(axis="y", visible=False)
a.set_xlabel("Distance from the typical country (in units of that year's world spread)", fontsize=12.5)
x0 = 0.18
for b, m in isaret.items():
    fig.text(x0, 0.93, ("● " if m == "o" else "■ " if m == "s" else "▲ " if m == "^" else "◆ ") + KISA.get(b, b),
             color=BOLGE[b], fontsize=12.5, fontweight="bold")
    x0 += 0.19 if b != "Latin America and the Caribbean" else 0.22
fig.subplots_adjust(left=0.18, right=0.98, top=0.88, bottom=0.16)
fig.savefig(CIKTI / f"v3_s3_spread{SON}.png", dpi=DPI); plt.close(fig)

# ---------- S4-A: Türkiye nüfusu + UN tahmin aralıkları ----------
ov = pd.read_csv(KOK / "data/WPP2024_Demographic_Indicators_OtherVariants_csv.gz", encoding="utf-8-sig",
                 usecols=["LocID", "Variant", "Time", "TPopulation1July"])
ov = ov[(ov["LocID"] == 792) & ov["Variant"].str.contains("PI") & (ov["Time"] <= 2100)]
pi = ov.pivot(index="Time", columns="Variant", values="TPopulation1July") / 1000
trp = df[df["Location"] == "Türkiye"].set_index("Time")["TPopulation1July"] / 1000
zirve = trp.idxmax()
fig, a = plt.subplots(figsize=(8.22, 2.42))
a.fill_between(pi.index, pi["Lower 95 PI"], pi["Upper 95 PI"], color="#3987e5", alpha=0.18, lw=0, label="95% interval")
a.fill_between(pi.index, pi["Lower 80 PI"], pi["Upper 80 PI"], color="#3987e5", alpha=0.32, lw=0, label="80% interval")
parla(a, trp.loc[:2023].index, trp.loc[:2023], "#2a78d6" if ACIK else "#5FA0F0", lw=2.8)
parla(a, trp.loc[2023:].index, trp.loc[2023:], "#2a78d6" if ACIK else "#5FA0F0", lw=2.2, ls=(0, (3, 2)))
a.scatter([zirve], [trp[zirve]], s=70, color=VURGU, zorder=5)
a.annotate(f"peak {zirve}: {trp[zirve]:.1f} M", (zirve, trp[zirve]), xytext=(0, 14), textcoords="offset points",
           ha="center", fontsize=13, color=VURGU, fontweight="bold")
a.annotate(f"2100: {trp[2100]:.1f} M\n95%: {pi.at[2100, 'Lower 95 PI']:.0f}–{pi.at[2100, 'Upper 95 PI']:.0f} M", (2100, trp[2100]),
           xytext=(-8, -14), textcoords="offset points", ha="right", va="top", fontsize=12.5, color=YAZI)
a.axvline(2023.5, color=YAZI2, lw=0.8)
a.set_ylabel("Millions"); a.set_ylim(0, 135); a.set_xlim(1950, 2101)
a.legend(frameon=False, loc="upper left", fontsize=12, labelcolor=YAZI)
fig.subplots_adjust(left=0.095, right=0.965, top=0.96, bottom=0.12)
fig.savefig(CIKTI / f"v3_s4_population{SON}.png", dpi=DPI); plt.close(fig)

# ---------- S4-B: Türkiye, Japonya, Nijerya, dünya: TFR ----------
fig, a = plt.subplots(figsize=(8.22, 2.42))
uc = {"Japan": BOLGE["Africa"], "Türkiye": BOLGE["Asia"], "Nigeria": BOLGE["Europe"]}
for u, r in uc.items():
    s = df[df["Location"] == u].set_index("Time")["TFR"]
    parla(a, s.loc[:2023].index, s.loc[:2023], r, lw=2.6); parla(a, s.loc[2023:].index, s.loc[2023:], r, lw=2, ls=(0, (3, 2)))
    t = t0t.set_index("Location").at[u, "t0"]
    if 1950 <= t <= 2100:
        a.scatter([t], [s.loc[int(round(t))]], s=80, color=r, edgecolor=VURGU, linewidth=1.5, zorder=5)
parla(a, dunya.loc[:2023].index, dunya.loc[:2023], VURGU, lw=1.6); parla(a, dunya.loc[2023:].index, dunya.loc[2023:], VURGU, lw=1.3, ls=(0, (3, 2)))
a.text(2098, 0.45, "Japan · ≈1935, before the data", ha="right", color=uc["Japan"], fontsize=12.5, fontweight="bold")
a.text(1986, 4.55, "Türkiye · 1982", color=uc["Türkiye"], fontsize=12.5, fontweight="bold")
a.text(2030, 4.9, "Nigeria · 2025", color=uc["Nigeria"], fontsize=12.5, fontweight="bold")
a.text(1952, 5.25, "World", color=VURGU, fontsize=12.5, fontweight="bold")
a.axhline(2.1, color=YAZI2, lw=1, ls=":"); a.axvline(2023.5, color=YAZI2, lw=0.8)
a.set_ylabel("Children per woman"); a.set_ylim(0.2, 7.2); a.set_xlim(1950, 2100)
fig.subplots_adjust(left=0.095, right=0.965, top=0.96, bottom=0.12)
fig.savefig(CIKTI / f"v3_s4_three{SON}.png", dpi=DPI); plt.close(fig)
print("S2-S4 grafikleri kaydedildi")
