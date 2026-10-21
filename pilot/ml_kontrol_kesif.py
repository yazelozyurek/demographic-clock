"""KEŞİF (ön kayıtta YOK, sonuçlar görüldükten sonra eklendi, 18 Ekim): ml_kontrol.py'deki OLS kazancı hangi özellikten?
Her özellik tek başına, LOO-CV ile OLS; takvim bazına karşı Wilcoxon (düzeltmesiz, betimsel)."""
import runpy, io, contextlib
import numpy as np, pandas as pd
from scipy.stats import wilcoxon, spearmanr
from sklearn.linear_model import LinearRegression
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path("pilot/ml_kontrol.py")
d, bolge_sut = g["d"].dropna(subset=g["SET"]["A"]).reset_index(drop=True), [c for c in g["d"].columns if c.startswith("bolge_")]
y = d["t0"].to_numpy(); n = len(y)
baz = np.array([abs(y[i] - np.median(np.delete(y, i))) for i in range(n)])
def loo(cols):
    X = d[cols].to_numpy(); e = np.empty(n)
    for i in range(n):
        m = np.arange(n) != i; e[i] = abs(y[i] - LinearRegression().fit(X[m], y[m]).predict(X[i:i+1])[0])
    return e
print(f"n = {n}, takvim medyan |hata| = {np.median(baz):.1f}")
for ad, cols in [("sadece bölge", bolge_sut), ("sadece eğitim 1950", ["egitim_1950"]), ("sadece log gelir 1950", ["log_gelir_1950"]),
                 ("sadece ekvator", ["ekvator"]), ("sadece log IMR 1950", ["log_imr_1950"]), ("bölge + eğitim", bolge_sut + ["egitim_1950"]),
                 ("Set A (hepsi)", g["SET"]["A"])]:
    e = loo(cols); print(f"{ad:24s} medyan |hata| = {np.median(e):4.1f}   p = {wilcoxon(e, baz).pvalue:.3f}")
for c in ["egitim_1950", "log_gelir_1950", "ekvator", "log_imr_1950"]:
    r, p = spearmanr(d[c], d["t0"]); print(f"t0 ~ {c:15s} ρ = {r:+.2f}  p = {p:.3g}")
m = LinearRegression().fit(d[["egitim_1950"]], y); print(f"eğitim 1950: her +1 yıl → dönüm {m.coef_[0]:+.1f} yıl")
print(d[["Location","egitim_1950","t0"]].sort_values("egitim_1950").iloc[[0,1,2,-3,-2,-1]].round(1).to_string(index=False))
