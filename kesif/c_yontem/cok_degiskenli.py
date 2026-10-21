"""Çok değişkenli modeller (iç içe LOO), LASSO kararlılık seçimi, kantil regresyon, sağlamlık
ve çok değişkenli sıfır kalibrasyonu (t0 permütasyonu → en iyi modelin LOO hatası).
Çalıştırma: python kesif/c_yontem/cok_degiskenli.py [N_NULL]
Çıktı: test_log_cok.csv, loo_sonuc.csv, null_cok.csv, kararlilik.csv"""
import sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, Lasso, RidgeCV, LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from joblib import Parallel, delayed

sys.path.insert(0, str(Path(__file__).parent))
from ozellik import yukle, OZELLIK, SONRA_OLCULEN
from tarama_tek import partial_spearman

warnings.filterwarnings("ignore")
BURA = Path(__file__).parent
N_NULL = int(sys.argv[1]) if len(sys.argv) > 1 else 200


class EnIyiK:
    """Kat İÇİNDE |Spearman|'a göre en iyi k özelliği seçip OLS kurar (dürüst tarama + model)."""
    def __init__(self, k): self.k = k
    def fit(self, X, y):
        self.imp = SimpleImputer(strategy="median").fit(X); X = self.imp.transform(X)
        r = [abs(stats.spearmanr(X[:, j], y)[0]) if X[:, j].std() > 0 else 0 for j in range(X.shape[1])]
        self.sec = np.argsort(np.nan_to_num(r))[::-1][:self.k]
        self.m = LinearRegression().fit(X[:, self.sec], y); return self
    def predict(self, X): return self.m.predict(self.imp.transform(X)[:, self.sec])


MODELLER = {
    "OLS_best1_selected_in_fold": lambda: EnIyiK(1),
    "OLS_top3_selected_in_fold": lambda: EnIyiK(3),
    "LASSO_nestedCV": lambda: make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                                            LassoCV(cv=5, n_alphas=30, max_iter=20000)),
    "Ridge_nestedCV": lambda: make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                                            RidgeCV(alphas=np.logspace(-2, 3, 20))),
    "RandomForest": lambda: make_pipeline(SimpleImputer(strategy="median"),
                                          RandomForestRegressor(n_estimators=150, min_samples_leaf=3,
                                                                max_features=0.33, random_state=0)),
    "GradientBoosting": lambda: make_pipeline(SimpleImputer(strategy="median"),
                                              GradientBoostingRegressor(n_estimators=150, max_depth=2,
                                                                        learning_rate=0.05, subsample=0.8,
                                                                        random_state=0)),
}


def loo(kur, X, y):
    n = len(y); tah = np.empty(n)
    for i in range(n):
        e = np.arange(n) != i; tah[i] = kur().fit(X[e], y[e]).predict(X[i:i + 1])[0]
    return y - tah


def baz_hata(y): return np.array([y[i] - np.median(np.delete(y, i)) for i in range(len(y))])


def matris(d, ad, sadece_once):
    oz = [f for f in OZELLIK[ad] if not (sadece_once and f in SONRA_OLCULEN)]
    reg = pd.get_dummies(d.bolge, prefix="reg", drop_first=True, dtype=float)
    X = pd.concat([d[oz], reg], axis=1)
    return X.columns.tolist(), X.to_numpy(float)


def bir_null(X, y, seed):
    yp = np.random.default_rng(seed).permutation(y)
    return {m: np.median(np.abs(loo(k, X, yp))) for m, k in MODELLER.items()}


def main():
    data = yukle(); log, loo_rows, nulls, karar = [], [], [], []
    tek = pd.read_csv(BURA / "test_log_tek.csv")
    for ad, d in data.items():
        y = d.t0.to_numpy(float); bh = baz_hata(y)
        loo_rows.append(dict(sample=ad, featureset="-", model="baseline_median_of_others", n=len(y),
                             median_abs_err=np.median(np.abs(bh)), mean_abs_err=np.mean(np.abs(bh)), p_vs_base=np.nan))
        # en iyi tek değişken (tüm veride, sızıntısız özellikler arasından; bilerek iyimser) → sabit OLS
        sp = tek[(tek["sample"] == ad) & (tek.method == "spearman") & (~tek.post_t0_risk)]
        best = sp.loc[sp.statistic.abs().idxmax(), "feature"]
        s = d.dropna(subset=[best]); yb = s.t0.to_numpy(float)
        h = loo(lambda: LinearRegression(), s[[best]].to_numpy(float), yb); hb = baz_hata(yb)
        p = stats.wilcoxon(np.abs(h), np.abs(hb)).pvalue
        loo_rows.append(dict(sample=ad, featureset=best, model="OLS_best_univariate_fixed(optimistic)", n=len(yb),
                             median_abs_err=np.median(np.abs(h)), mean_abs_err=np.mean(np.abs(h)), p_vs_base=p,
                             base_same_n=np.median(np.abs(hb))))
        log.append(dict(family="predictive", sample=ad, feature=best, method="LOO_OLS_fixed_vs_baseline_wilcoxon",
                        n=len(yb), statistic=np.median(np.abs(h)) - np.median(np.abs(hb)), p=p, post_t0_risk=False))
        # kantil regresyon (en iyi özellik)
        for q in (0.25, 0.5, 0.75):
            m = smf.quantreg(f"t0 ~ {best}", s).fit(q=q)
            log.append(dict(family="quantile", sample=ad, feature=best, method=f"quantreg_q{q}_slope", n=len(s),
                            statistic=m.params[best], p=m.pvalues[best], post_t0_risk=False))
        # sağlamlık: t0 >= 1972 alt örneği (1970'e kadarki özellikler kesin t0 öncesi), en iyi 6 özellik
        top = (tek[(tek["sample"] == ad) & (tek.method == "spearman")]
               .assign(a=lambda z: z.statistic.abs()).nlargest(6, "a").feature.tolist())
        alt = d[d.t0 >= 1972]
        for f in dict.fromkeys(top + [best]):
            ss = alt.dropna(subset=[f]); r, p = stats.spearmanr(ss[f], ss.t0)
            log.append(dict(family="sensitivity_t0>=1972", sample=ad, feature=f, method="spearman", n=len(ss),
                            statistic=r, p=p, post_t0_risk=False))
        # karıştırıcı kontrolü: kalkınma düzeyi vekili lex_1950'yi sabitleyince ne kalıyor?
        for f in OZELLIK[ad]:
            if f == "lex_1950": continue
            ss = d.dropna(subset=[f, "lex_1950"])
            r, p = partial_spearman(ss[f].to_numpy(float), ss.t0.to_numpy(float), ss[["lex_1950"]].to_numpy(float))
            log.append(dict(family="confounder_check", sample=ad, feature=f, method="partial_spearman|lex_1950",
                            n=len(ss), statistic=r, p=p, post_t0_risk=f in SONRA_OLCULEN))
        # çok değişkenli LOO: ana set = sadece 1950/1950'ler özellikleri; ikincil = hepsi
        for sadece_once in (True, False):
            fs = "pre_t0_only" if sadece_once else "all_incl_1960_1970"
            cols, X = matris(d, ad, sadece_once)
            for mad, kur in MODELLER.items():
                h = loo(kur, X, y); p = stats.wilcoxon(np.abs(h), np.abs(bh)).pvalue
                loo_rows.append(dict(sample=ad, featureset=fs, model=mad, n=len(y), median_abs_err=np.median(np.abs(h)),
                                     mean_abs_err=np.mean(np.abs(h)), p_vs_base=p))
                log.append(dict(family="predictive", sample=ad, feature=fs, method=f"LOO_{mad}_vs_baseline_wilcoxon",
                                n=len(y), statistic=np.median(np.abs(h)) - np.median(np.abs(bh)), p=p,
                                post_t0_risk=not sadece_once))
            print(ad, fs, "LOO bitti", flush=True)
            if sadece_once:
                # LASSO kararlılık seçimi (Meinshausen–Bühlmann): 500 yarım alt örnek, seyrek alfa ızgarası
                # (tüm veride 1–8 değişken seçen alfalar); kararlılık = ızgaradaki en yüksek seçilme oranı.
                # Ayrıca CV alfasında 500 bootstrap seçilme oranı (CV alfası küçük → neredeyse hepsi seçilir).
                pre = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
                Z = pre.fit_transform(X)
                yc = y - y.mean()
                acv = LassoCV(cv=5, n_alphas=30, max_iter=20000).fit(Z, y).alpha_
                amax = np.max(np.abs(Z.T @ yc)) / len(y)
                izgara = [a for a in amax * np.logspace(0, -2, 40)
                          if 1 <= (Lasso(alpha=a, max_iter=20000).fit(Z, y).coef_ != 0).sum() <= 8]
                rng = np.random.default_rng(7); sec = np.zeros((len(izgara), len(cols))); boot = np.zeros(len(cols))
                for _ in range(500):
                    i = rng.choice(len(y), len(y) // 2, replace=False)
                    for j, a in enumerate(izgara):
                        sec[j] += Lasso(alpha=a, max_iter=20000).fit(Z[i], y[i]).coef_ != 0
                    b = rng.integers(0, len(y), len(y))
                    boot += Lasso(alpha=acv, max_iter=20000).fit(Z[b], y[b]).coef_ != 0
                karar += [dict(sample=ad, feature=c, stability_max_over_sparse_grid=sec[:, k].max() / 500,
                               bootstrap_freq_at_cv_alpha=boot[k] / 500, n_alpha_grid=len(izgara))
                          for k, c in enumerate(cols)]
                # sıfır kalibrasyonu: aynı model ailesi, t0 karıştırılmış
                res = Parallel(n_jobs=8)(delayed(bir_null)(X, y, 5000 + i) for i in range(N_NULL))
                for i, r in enumerate(res):
                    nulls.append(dict(sample=ad, seed=5000 + i, best_model_mae=min(r.values()), **r))
                print(ad, "null bitti", flush=True)
    pd.DataFrame(log).to_csv(BURA / "test_log_cok.csv", index=False)
    pd.DataFrame(loo_rows).to_csv(BURA / "loo_sonuc.csv", index=False)
    pd.DataFrame(nulls).to_csv(BURA / "null_cok.csv", index=False)
    pd.DataFrame(karar).sort_values(["sample", "stability_max_over_sparse_grid"], ascending=[True, False]).to_csv(BURA / "kararlilik.csv", index=False)


if __name__ == "__main__":
    main()
