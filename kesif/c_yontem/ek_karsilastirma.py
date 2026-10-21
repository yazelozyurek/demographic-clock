"""Ek: çok değişkenli modeller en iyi TEK değişkenden daha mı iyi? (aynı LOO, eşleştirilmiş Wilcoxon)
Ayrıca: lex_1950 ile eğitim (S66) birbirinin yerine mi geçiyor? Çalıştırma: python kesif/c_yontem/ek_karsilastirma.py"""
import sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression

sys.path.insert(0, str(Path(__file__).parent))
from ozellik import yukle
from cok_degiskenli import MODELLER, matris, loo, baz_hata

warnings.filterwarnings("ignore")
B = Path(__file__).parent
data = yukle(); log = []
EN_IYI = {"S66": "sch_mf2564_1950", "S115": "lex_1950"}
for ad, d in data.items():
    y = d.t0.to_numpy(float); _, X = matris(d, ad, True)
    tek = loo(lambda: LinearRegression(), d[[EN_IYI[ad]]].to_numpy(float), y)
    for m in ("LASSO_nestedCV", "RandomForest", "GradientBoosting"):
        h = loo(MODELLER[m], X, y); p = stats.wilcoxon(np.abs(h), np.abs(tek)).pvalue
        log.append(dict(family="predictive_vs_best_univariate", sample=ad, feature=f"pre_t0_only vs {EN_IYI[ad]}",
                        method=f"LOO_{m}_vs_OLS_single_wilcoxon", n=len(y),
                        statistic=np.median(np.abs(h)) - np.median(np.abs(tek)), p=p, post_t0_risk=False))
    if ad == "S66":   # iki 'kalkınma' göstergesi birlikte
        for cols in (["lex_1950"], ["lex_1950", "sch_mf2564_1950"], ["lex_1950", "sch_mf2564_1950", "log_gdp_1950"]):
            s = d.dropna(subset=cols); yy = s.t0.to_numpy(float)
            h = loo(lambda: LinearRegression(), s[cols].to_numpy(float), yy); hb = baz_hata(yy)
            log.append(dict(family="predictive", sample=ad, feature="+".join(cols), method="LOO_OLS_vs_baseline_wilcoxon",
                            n=len(yy), statistic=np.median(np.abs(h)) - np.median(np.abs(hb)),
                            p=stats.wilcoxon(np.abs(h), np.abs(hb)).pvalue, post_t0_risk=False,
                            note=f"medAE={np.median(np.abs(h)):.2f}"))
r = pd.DataFrame(log); r.to_csv(B / "test_log_ek.csv", index=False); print(r.round(4).to_string())
