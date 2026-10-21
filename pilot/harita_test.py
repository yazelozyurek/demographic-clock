"""Slayt 2 için: (1) dünya "saat haritası" (her ülke dönüm yılına göre renkli), (2) bölgeler arası klasik test.
Çalıştırma:  python pilot/harita_test.py   (önce 04 notebook'u: clean/t0_tablosu.csv)
Harita: arac/world-50m.json (Natural Earth / world-atlas 2.0.2), Equal Earth izdüşümü; geopandas gerekmez.
Test: dönüm noktası veride görülen ülkeler (guvenilir = True) · Kruskal–Wallis + ikili Mann–Whitney (Holm düzeltmesi)."""
import json
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.stats import kruskal, mannwhitneyu
from statsmodels.stats.multitest import multipletests

KOK = Path(__file__).resolve().parent.parent
import os
TEMA = os.environ.get("TEMA", "mavi")
EK = {"grafit": "_g", "acik": "_a"}.get(TEMA, "")
KART, YAZI, YAZI2 = {"grafit": ("#1C1D21", "#ECECEE", "#A3A5AB"), "acik": ("#FBFBF9", "#1F2328", "#5E6873")}.get(TEMA, ("#15222E", "#E8EEF2", "#9FB0BD"))
OKYANUS, BOS, HUCRE = {"grafit": ("#24262B", "#3A3C42", "#2E3036"), "acik": ("#EDF1F5", "#D9DADD", "#EEEDEA")}.get(TEMA, ("#1A2836", "#33475A", "#253645"))
SAAT_RENK = LinearSegmentedColormap.from_list("saat", ["#2fb7ff", "#7a6cff", "#ff4f7a", "#ff6a2b"])   # kapakla aynı
BAS, SON = 1930, 2050

# ---------- topojson çözücü ----------
topo = json.load(open(KOK / "arac/world-50m.json"))
sk, tr = topo["transform"]["scale"], topo["transform"]["translate"]
yaylar = []
for yay in topo["arcs"]:
    x = y = 0; noktalar = []
    for dx, dy in yay:
        x += dx; y += dy; noktalar.append((x * sk[0] + tr[0], y * sk[1] + tr[1]))
    yaylar.append(np.array(noktalar))
def halka(idx):
    parca = [yaylar[i] if i >= 0 else yaylar[~i][::-1] for i in idx]
    return np.vstack([p if k == 0 else p[1:] for k, p in enumerate(parca)])
def poligonlar(g):
    if g["type"] == "Polygon": return [[halka(r) for r in g["arcs"]]]
    if g["type"] == "MultiPolygon": return [[halka(r) for r in p] for p in g["arcs"]]
    return []

def equal_earth(lon, lat):
    A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
    lam, phi = np.radians(lon), np.radians(lat)
    th = np.arcsin(np.sqrt(3) / 2 * np.sin(phi))
    x = 2 * np.sqrt(3) * lam * np.cos(th) / (3 * (9 * A4 * th**8 + 7 * A3 * th**6 + 3 * A2 * th**2 + A1))
    y = A4 * th**9 + A3 * th**7 + A2 * th**3 + A1 * th
    return x, y

ADA = {"Somaliland": 706, "N. Cyprus": 196, "Kosovo": 412}                     # UN kapsamına göre
FRANSA_DISI = {254: (-53, 4), 312: (-61.5, 16.2), 474: (-61, 14.6), 638: (55.5, -21.1), 175: (45.1, -12.8)}
parcalar = []                                                                    # (LocID, dış halka)
for g in topo["objects"]["countries"]["geometries"]:
    kimlik = ADA.get(g["properties"].get("name"), g.get("id"))
    if kimlik is None: continue
    kimlik = int(kimlik)
    if kimlik == 10: continue                                                    # Antarktika
    for p in poligonlar(g):
        dis = p[0]
        if kimlik == 250:                                                        # Fransa'nın denizaşırı bölgeleri ayrı ülke
            m = dis.mean(axis=0)
            for lid, (lo, la) in FRANSA_DISI.items():
                if abs(m[0] - lo) < 4 and abs(m[1] - la) < 4: kimlik_p = lid; break
            else: kimlik_p = 250
            parcalar.append((kimlik_p, dis))
        else:
            parcalar.append((kimlik, dis))

t0 = pd.read_csv(KOK / "clean/t0_tablosu.csv")
kapsam = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["LocID", "pop2023"]).drop_duplicates()
kucuk = set(kapsam.loc[kapsam["pop2023"] < 100, "LocID"])
tt = t0.set_index("LocID")
norm = Normalize(BAS, SON)

fig = plt.figure(figsize=(10.28, 3.04))
ax = fig.add_axes([0.0, 0.02, 0.68, 0.96]); ax.set_axis_off(); ax.set_aspect("equal")
# kenar (küre çerçevesi)
la = np.linspace(-90, 90, 200)
la = np.linspace(-58, 90, 200)
xe, ye = equal_earth(np.r_[np.full(200, -180), np.full(200, 180)], np.r_[la, la[::-1]])
ax.fill(xe, ye, color=OKYANUS, lw=0)
dolu, bos, gri = [], [], []
for lid, dis in parcalar:
    x, y = equal_earth(dis[:, 0], dis[:, 1])
    xy = np.column_stack([x, y])
    if lid in tt.index:
        r = tt.loc[lid]; renk = SAAT_RENK(norm(min(max(r["t0"], BAS), SON)))
        (dolu if r["guvenilir"] else bos).append((xy, renk))
    else:
        gri.append(xy)
ax.add_collection(PolyCollection(gri, facecolors=BOS, edgecolors=KART, linewidths=0.25))
ax.add_collection(PolyCollection([p for p, _ in dolu], facecolors=[c for _, c in dolu], edgecolors=KART, linewidths=0.3))
ax.add_collection(PolyCollection([p for p, _ in bos], facecolors=[c for _, c in bos], edgecolors=KART, linewidths=0.3,
                                 hatch="////", alpha=0.75))
ax.autoscale_view()
# renk anahtarı
ck = fig.add_axes([0.71, 0.50, 0.27, 0.07])
grad = np.linspace(0, 1, 256)[None, :]
ck.imshow(grad, aspect="auto", cmap=SAAT_RENK, extent=[BAS, SON, 0, 1]); ck.set_yticks([])
ck.set_xticks([1940, 1960, 1980, 2000, 2020, 2040]); ck.tick_params(colors=YAZI2, labelsize=11.5, length=0)
for s in ck.spines.values(): s.set_visible(False)
ck.axvline(2023.5, color=YAZI, lw=2)
fig.text(0.71, 0.62, "Year of the turning point", color=YAZI2, fontsize=12.5)
fig.text(0.71, 0.30, "Hatched: turning point inferred\n(not seen in 1950–2023)", color=YAZI2, fontsize=12, va="top")
fig.text(0.71, 0.82, "Europe first · Africa now", color=YAZI, fontsize=13.5, fontweight="bold")
fig.patch.set_facecolor(KART)
fig.savefig(KOK / f"outputs/v3_s2_map{EK}.png", dpi=200, facecolor=KART); plt.close(fig)
eksik = sorted(set(t0["LocID"]) - {lid for lid, _ in parcalar})
print("haritada çizilmeyen t0 ülkesi:", eksik)

# ---------- bölgeler arası test ----------
g = t0[t0["guvenilir"]]
kisa = {"Africa": "Africa", "Asia": "Asia", "Europe": "Europe", "Latin America and the Caribbean": "Lat. Am.", "Oceania": "Oceania"}
gruplar = {kisa[b]: d["t0"].values for b, d in g.groupby("bolge") if b in kisa}
H, p = kruskal(*gruplar.values())
ciftler = list(combinations(gruplar, 2))
ham = [mannwhitneyu(gruplar[a], gruplar[b]).pvalue for a, b in ciftler]
holm = multipletests(ham, method="holm")[1]
sonuc = pd.DataFrame({"a": [a for a, _ in ciftler], "b": [b for _, b in ciftler], "p_ham": ham, "p_holm": holm})
sonuc.to_csv(KOK / "outputs/bolge_testleri.csv", index=False)
print(f"Kruskal–Wallis H = {H:.1f}, p = {p:.1e}, n = {len(g)}  |  n:", {k: len(v) for k, v in gruplar.items()})
print("medyanlar:", {k: round(float(np.median(v))) for k, v in gruplar.items()})
print(sonuc.round(4).to_string(index=False))

# ---------- ikili p-değeri ısı haritası (slayt 2 kartı) ----------
from matplotlib.colors import LinearSegmentedColormap as LSC
ad = list(gruplar)                                                               # Africa, Asia, Europe, Lat. Am., Oceania
P = pd.DataFrame(np.nan, index=ad, columns=ad)
for (a, b), ph in zip(ciftler, holm):
    P.loc[b, a] = ph if ad.index(b) > ad.index(a) else np.nan; P.loc[a, b] = ph
P = P.iloc[1:, :-1]
fig, ax = plt.subplots(figsize=(5.03, 1.72))
renk = LSC.from_list("p", [HUCRE, "#7a6cff", "#ff4f7a"])
for i, r in enumerate(P.index):
    for j, c in enumerate(P.columns):
        if j > i: continue
        v = P.loc[r, c]; z = np.clip(-np.log10(v) / 4, 0, 1) if v < 0.05 else 0
        ax.add_patch(plt.Rectangle((j, i), 0.96, 0.92, color=renk(z)))
        ax.text(j + 0.48, i + 0.46, "<0.001" if v < 0.001 else (f"{v:.3f}" if v < 0.1 else f"{v:.2f}"), ha="center", va="center", fontsize=11,
                color="#FFFFFF" if v < 0.05 else YAZI, fontweight="bold" if v < 0.05 else None)
ax.set_xlim(0, P.shape[1]); ax.set_ylim(P.shape[0], 0)
ax.set_xticks(np.arange(P.shape[1]) + 0.48, P.columns, fontsize=11, color=YAZI2)
ax.set_yticks(np.arange(P.shape[0]) + 0.46, P.index, fontsize=11, color=YAZI2)
ax.tick_params(length=0); ax.xaxis.tick_top()
for s_ in ax.spines.values(): s_.set_visible(False)
ax.text(4.1, 0.5, f"Kruskal–Wallis\np = {p:.0e}".replace("e-0", "×10⁻").replace("5×10⁻5", "0.00005"), fontsize=11.5, color=YAZI, va="center")
ax.text(4.1, 2.3, "coloured: differ\n(Holm p < 0.05)", fontsize=11, color="#C2185B" if TEMA == "acik" else "#ff7a9a", va="center")
fig.patch.set_facecolor(KART); ax.set_facecolor(KART)
fig.subplots_adjust(left=0.17, right=0.70, top=0.80, bottom=0.03)
fig.savefig(KOK / f"outputs/v3_s2_pairs{EK}.png", dpi=200, facecolor=KART); plt.close(fig)
