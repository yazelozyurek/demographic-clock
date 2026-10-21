"""Tek değişkenli tarama + bütün-arama sıfır kalibrasyonu (t0 permütasyonu).
Çalıştırma: python kesif/c_yontem/tarama_tek.py   → test_log_tek.csv, null_tek.csv"""
import sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from patsy import dmatrix
from sklearn.feature_selection import mutual_info_regression
from joblib import Parallel, delayed

sys.path.insert(0, str(Path(__file__).parent))
from ozellik import yukle, OZELLIK, SONRA_OLCULEN

warnings.filterwarnings("ignore")
BURA = Path(__file__).parent
N_NULL = int(sys.argv[1]) if len(sys.argv) > 1 else 200


def dcor(x, y):
    a = np.abs(x[:, None] - x[None, :]); b = np.abs(y[:, None] - y[None, :])
    A = a - a.mean(0) - a.mean(1)[:, None] + a.mean(); B = b - b.mean(0) - b.mean(1)[:, None] + b.mean()
    dxy, dxx, dyy = (A * B).mean(), (A * A).mean(), (B * B).mean()
    return np.sqrt(max(dxy, 0) / np.sqrt(dxx * dyy))


def resid(v, Z):
    Z = np.column_stack([np.ones(len(v)), Z]); return v - Z @ np.linalg.lstsq(Z, v, rcond=None)[0]


def partial_spearman(x, y, Z):
    rx, ry = resid(stats.rankdata(x), Z), resid(stats.rankdata(y), Z)
    r = np.corrcoef(rx, ry)[0, 1]; df = len(x) - 2 - Z.shape[1]
    t = r * np.sqrt(df / max(1 - r * r, 1e-12)); return r, 2 * stats.t.sf(abs(t), df)


def ftest_basis(x, y, kind):
    if kind == "spline":
        X = np.asarray(dmatrix("cr(x, df=4) - 1", {"x": x}))
        X = np.column_stack([np.ones(len(x)), X[:, 1:]]) if np.linalg.matrix_rank(np.column_stack([np.ones(len(x)), X])) < X.shape[1] + 1 else np.column_stack([np.ones(len(x)), X])
    else:
        z = (x - x.mean()) / x.std(); X = np.column_stack([np.ones(len(x)), z, z ** 2])
    m = sm.OLS(y, X).fit(); return m.rsquared, m.f_pvalue


def tek_test(x, y, Zreg, Zgdp, hizli=False):
    """Bir özellik için bütün yöntemler. hizli=True: permütasyon p'si yok (sıfır kalibrasyonu)."""
    out = {}
    out["pearson"] = stats.pearsonr(x, y)
    if np.all(x > 0) and stats.skew(x) > 1:
        out["pearson_log"] = stats.pearsonr(np.log(x), y)
    out["spearman"] = stats.spearmanr(x, y)
    out["kendall"] = stats.kendalltau(x, y)
    out["partial_spearman|region"] = partial_spearman(x, y, Zreg)
    if Zgdp is not None:
        out["partial_spearman|log_gdp_1950"] = partial_spearman(x, y, Zgdp)
    out["spline_df4_R2"] = ftest_basis(x, y, "spline")
    out["poly2_R2"] = ftest_basis(x, y, "poly")
    d = dcor(x, y)
    mi = mutual_info_regression(x[:, None], y, n_neighbors=3, random_state=0)[0]
    if hizli:
        out["dcor"] = (d, np.nan); out["mutual_info"] = (mi, np.nan)
    else:
        rng = np.random.default_rng(1)
        pd_ = (1 + sum(dcor(x, rng.permutation(y)) >= d for _ in range(999))) / 1000
        pm = (1 + sum(mutual_info_regression(x[:, None], rng.permutation(y), n_neighbors=3, random_state=0)[0] >= mi
                      for _ in range(199))) / 200
        out["dcor"] = (d, pd_); out["mutual_info"] = (mi, pm)
    return {k: (float(v[0]), float(v[1])) for k, v in out.items()}


def hazirla(d, ad):
    reg = pd.get_dummies(d.bolge, drop_first=True, dtype=float).to_numpy()
    feats = []
    for f in OZELLIK[ad]:
        ok = d[f].notna().to_numpy()
        if ad == "S66": ok &= d.log_gdp_1950.notna().to_numpy()
        Zgdp = d.loc[ok, ["log_gdp_1950"]].to_numpy() if (ad == "S66" and f != "log_gdp_1950") else None
        feats.append((f, ok, d.loc[ok, f].to_numpy(float), reg[ok], Zgdp))
    return feats


def tarama(feats, y_all, hizli):
    res = []
    for f, ok, x, Zr, Zg in feats:
        for meth, (st, p) in tek_test(x, y_all[ok], Zr, Zg, hizli).items():
            res.append((f, meth, int(ok.sum()), st, p))
    return res


def main():
    data = yukle(); log = []; nulls = []
    for ad, d in data.items():
        y = d.t0.to_numpy(float); feats = hazirla(d, ad)
        for f, meth, n, st, p in tarama(feats, y, hizli=False):
            log.append(dict(family="univariate", sample=ad, feature=f, method=meth, n=n, statistic=st, p=p,
                            post_t0_risk=f in SONRA_OLCULEN))
        # bölge (kategorik)
        g = [d.t0[d.bolge == b].to_numpy() for b in d.bolge.unique() if (d.bolge == b).sum() >= 2]
        H, p = stats.kruskal(*g); eta = (H - len(g) + 1) / (len(d) - len(g))
        log.append(dict(family="univariate", sample=ad, feature="region", method="kruskal_wallis_eta2", n=len(d),
                        statistic=eta, p=p, post_t0_risk=False))
        # etkileşimler: özellik × bölge3 (F testi, ekleme terimi modeline karşı)
        for f in OZELLIK[ad]:
            s = d.dropna(subset=[f])
            m0 = smf.ols(f"t0 ~ {f} + C(bolge3)", s).fit(); m1 = smf.ols(f"t0 ~ {f} * C(bolge3)", s).fit()
            F, p, _ = m1.compare_f_test(m0)
            log.append(dict(family="interaction", sample=ad, feature=f"{f} x region", method="ols_interaction_F",
                            n=len(s), statistic=F, p=p, post_t0_risk=f in SONRA_OLCULEN))
        # sıfır kalibrasyonu: t0'ı karıştır, tek değişkenli taramayı aynen tekrarla (perm p'siz)
        def bir_perm(seed):
            yp = np.random.default_rng(seed).permutation(y)
            r = pd.DataFrame(tarama(feats, yp, hizli=True), columns=["feature", "method", "n", "stat", "p"])
            row = {"sample": ad, "seed": seed, "min_p_analytic": r.p.min()}
            for meth, gg in r.groupby("method"): row[f"max_abs_{meth}"] = gg.stat.abs().max()
            return row
        nulls += Parallel(n_jobs=8)(delayed(bir_perm)(1000 + i) for i in range(N_NULL))
        print(ad, "bitti", flush=True)
    pd.DataFrame(log).to_csv(BURA / "test_log_tek.csv", index=False)
    pd.DataFrame(nulls).to_csv(BURA / "null_tek.csv", index=False)


if __name__ == "__main__":
    main()
