"""ML sağlamlık kontrolü (jüri yedeği). Ana model random forest; OLS ve LASSO ikincil. Plan: pilot/ml_kontrol_plan.md (sonuçtan önce yazıldı).
Soru: 1950'deki gelir, eğitim, coğrafya (ve bebek ölümü) dönüm yılını "tipik yıl" tahmininden iyi tahmin ediyor mu?
Çalıştırma:  python pilot/ml_kontrol.py   (önce 04 ve 05 notebook'ları)
Çıktı: outputs/ml_kontrol_sonuc.csv, outputs/ml_kontrol_onem.csv"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LassoCV, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

KOK = Path(__file__).resolve().parent.parent

# ---------- ekvatora uzaklık: haritadaki ülkelerin alan ağırlıklı merkezi ----------
topo = json.load(open(KOK / "arac/world-50m.json"))
sk, tr = topo["transform"]["scale"], topo["transform"]["translate"]
yaylar = []
for yay in topo["arcs"]:
    x = y = 0; nok = []
    for dx, dy in yay:
        x += dx; y += dy; nok.append((x * sk[0] + tr[0], y * sk[1] + tr[1]))
    yaylar.append(np.array(nok))
def halka(idx):
    r = np.vstack([yaylar[i] if i >= 0 else yaylar[~i][::-1] for i in idx])
    return np.vstack([r, r[:1]])
def alan_ve_enlem(r):
    x, y = r[:, 0], r[:, 1]; c = x[:-1] * y[1:] - x[1:] * y[:-1]; A = c.sum() / 2
    return abs(A), (((y[:-1] + y[1:]) * c).sum() / (6 * A) if abs(A) > 1e-6 else y.mean())
parca = {}                                            # aynı id'li birden çok geometri olabilir (ör. Avustralya'nın adaları)
for g in topo["objects"]["countries"]["geometries"]:
    if g.get("id") is None: continue
    pol = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"] if g["type"] == "MultiPolygon" else []
    parca.setdefault(int(g["id"]), []).extend(alan_ve_enlem(halka(p[0])) for p in pol)
enlem = {k: sum(a * e for a, e in v) / sum(a for a, _ in v) for k, v in parca.items() if v}

# ---------- veri ----------
d = pd.read_csv(KOK / "clean/para_okul_tablosu.csv")[["LocID", "ISO3_code", "Location", "bolge", "t0"]]
d["ekvator"] = d["LocID"].map(enlem).abs()

gelir = pd.read_csv(KOK / "data_dis/gdp-per-capita-maddison-project-database.csv")
gelir = gelir[gelir["year"].between(1950, 1955)].sort_values("year").groupby("code")["gdp_per_capita"].first()
d["log_gelir_1950"] = np.log(d["ISO3_code"].map(gelir))

egitim = pd.read_csv(KOK / "data_dis/barrolee_BL_v3_F2534.csv")
d["egitim_1950"] = d["ISO3_code"].map(egitim[egitim["year"] == 1950].set_index("WBcode")["yr_sch"])

wpp = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["LocID", "Time", "IMR"])
d["log_imr_1950"] = np.log(d["LocID"].map(wpp[wpp["Time"] == 1950].set_index("LocID")["IMR"]))

bolge = pd.get_dummies(d["bolge"], prefix="bolge", drop_first=True, dtype=float)
d = pd.concat([d, bolge], axis=1)
SET = {"A": ["log_gelir_1950", "egitim_1950", "ekvator", *bolge.columns],
       "B": ["log_gelir_1950", "egitim_1950", "ekvator", *bolge.columns, "log_imr_1950"]}

MODEL = {
    "OLS": lambda: make_pipeline(StandardScaler(), LinearRegression()),
    "LASSO": lambda: make_pipeline(StandardScaler(), LassoCV(cv=5, max_iter=50000)),
    "Random forest": lambda: RandomForestRegressor(n_estimators=500, min_samples_leaf=3, random_state=0),
}

# ---------- LOO-CV ----------
satirlar, karsilastirma = [], []
for set_ad, ozellik in SET.items():
    s = d.dropna(subset=ozellik).reset_index(drop=True)
    X, y = s[ozellik].to_numpy(), s["t0"].to_numpy()
    n = len(s)
    hata = {"Takvim (baz)": np.array([y[i] - np.median(np.delete(y, i)) for i in range(n)])}
    for ad, kur in MODEL.items():
        tah = np.empty(n)
        for i in range(n):
            egit = np.arange(n) != i
            m = kur().fit(X[egit], y[egit]); tah[i] = m.predict(X[i:i + 1])[0]
        hata[ad] = y - tah
    for ad, h in hata.items():
        satirlar.append({"set": set_ad, "n": n, "model": ad,
                         "medyan_mutlak_hata": np.median(np.abs(h)), "ortalama_mutlak_hata": np.mean(np.abs(h))})
        if ad != "Takvim (baz)":
            karsilastirma.append((len(satirlar) - 1, wilcoxon(np.abs(h), np.abs(hata["Takvim (baz)"])).pvalue))
    print(f"Set {set_ad}: n = {n}, çıkan ülke: {sorted(set(d['Location']) - set(s['Location']))}")

sonuc = pd.DataFrame(satirlar)
idx, ham = zip(*karsilastirma)
sonuc.loc[list(idx), "p_ham"] = ham
ana = sonuc.index[sonuc["model"] == "Random forest"]                  # karar sadece ana modelde (2 set, Holm)
sonuc.loc[ana, "p_holm"] = multipletests(sonuc.loc[ana, "p_ham"], method="holm")[1]
baz = sonuc[sonuc["model"] == "Takvim (baz)"].set_index("set")["medyan_mutlak_hata"]
sonuc["takvimi_gecti"] = (sonuc["medyan_mutlak_hata"] < sonuc["set"].map(baz)) & (sonuc["p_holm"] < 0.05)
sonuc.round(3).to_csv(KOK / "outputs/ml_kontrol_sonuc.csv", index=False)
print(sonuc.round(3).to_string(index=False))

# ---------- betimsel: random forest permütasyon önemi (Set A, bütün veri) ----------
s = d.dropna(subset=SET["A"])
rf = MODEL["Random forest"]().fit(s[SET["A"]], s["t0"])
pi = permutation_importance(rf, s[SET["A"]], s["t0"], n_repeats=200, random_state=0,
                            scoring="neg_median_absolute_error")
onem = pd.DataFrame({"ozellik": SET["A"], "onem_yil": pi.importances_mean}).sort_values("onem_yil", ascending=False)
onem.round(2).to_csv(KOK / "outputs/ml_kontrol_onem.csv", index=False)
print("\nPermütasyon önemi (karıştırılınca medyan mutlak hata kaç yıl artıyor; eğitim verisi üzerinde, betimsel):")
print(onem.round(2).to_string(index=False))
