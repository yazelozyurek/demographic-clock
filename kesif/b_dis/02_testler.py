"""Spearman tests, within-region tests, BH-FDR, permutation null, LOO for top 3.
Usage: python -I 02_testler.py <t0_table_csv> <feature_csv> <out_dir>"""
import sys, numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

t0p, fp, od = sys.argv[1:4]
t = pd.read_csv(t0p)[["ISO3_code", "bolge", "t0", "guvenilir"]]
f = pd.read_csv(fp)
d = t.merge(f, on="ISO3_code")
feats = [c for c in f.columns if c != "ISO3_code" and not c.endswith("_cens")]
timing = [c for c in feats if c.endswith("_year")]

DEF = {
 "urban_share_1950": "urban share of population (%), 1950 [UN WUP via OWID]",
 "urban30_year": "first year urban share >=30% (interp.; 1950-2050 incl. UN proj.)",
 "urban50_year": "first year urban share >=50% (interp.; 1950-2050 incl. UN proj.)",
 "child_mort_1950_log": "log under-5 mortality (%), 1950 [Gapminder/IGME via OWID]",
 "child_mort_1960_log": "log under-5 mortality (%), 1960 (fallback baseline)",
 "child_mort_below10pct_year": "first year under-5 mortality <=10% (interp., 1800+)",
 "literacy_1950": "adult literacy rate (%), 1950 [OWID compilation, UNESCO]",
 "vdem_electdem_1950": "V-Dem electoral democracy index, 1950",
 "pop_density_1950_log": "log population density, 1950 [OWID/HYDE/WPP]",
 "life_exp_1950": "life expectancy at birth, 1950 [OWID = UN WPP] (WPP-derived)",
 "life_exp50_year": "first year life expectancy >=50 (interp., 1850+) (WPP-derived post-1950)",
 "calories_1961": "daily per-capita calorie supply, 1961 [FAO via OWID] (1961 baseline)",
 "some_formal_edu_1950": "share of pop. 15+ with some formal education (%), 1950 [Lee-Lee/van Zanden via OWID] (overlaps Barro-Lee)",
 "some_formal_edu50_year": "first year share with some formal education >=50% (interp., 1870+)",
 "primary_net_enrol_1950": "net primary enrolment rate (%), 1950+-2 [Lee-Lee/UNESCO via OWID]",
 "primary_enrol50_year": "first year net primary enrolment >=50% (interp., 1820+)",
 "contracep20_year": "first year contraceptive prevalence (any method) >=20% (bracketed only) [WDI/UN via OWID] PROXIMATE, near-mechanical",
 "female_lfp_1991_POSTT0": "female labour-force participation (%), 1991 [ILO via OWID/WDI] POST-t0, leakage",
}

def within_rank(sub, x):
    g = sub.groupby("bolge")
    ok = g[x].transform("size") >= 3
    s = sub[ok]
    return s.groupby("bolge")[x].rank(pct=True), s.groupby("bolge")["t0"].rank(pct=True)

rows = []
samples = {"primary_115": d[d.guvenilir], "all_200": d}
for sname, S in samples.items():
    for x in feats:
        sub = S[["bolge", "t0", x]].dropna()
        r, p = stats.spearmanr(sub[x], sub.t0)
        rows.append(dict(feature=x, definition=DEF[x], sample=sname, method="spearman", n=len(sub), rho=r, p=p))
        a, b = within_rank(sub, x)
        r, p = stats.spearmanr(a, b)
        rows.append(dict(feature=x, definition=DEF[x], sample=sname, method="spearman_within_region", n=len(a), rho=r, p=p))
        if x in timing:   # sensitivity: drop censored crossing years
            sub2 = S[["t0", x, x + "_cens"]].dropna()
            sub2 = sub2[sub2[x + "_cens"] == 0]
            r, p = stats.spearmanr(sub2[x], sub2.t0)
            rows.append(dict(feature=x, definition=DEF[x], sample=sname, method="spearman_uncensored_only", n=len(sub2), rho=r, p=p))
log = pd.DataFrame(rows)
log["q_BH"] = multipletests(log.p, method="fdr_bh")[1]
log.to_csv(f"{od}/test_kaydi.csv", index=False)
print("total tests:", len(log))
pd.set_option("display.width", 250)
P = log[(log["sample"] == "primary_115")].pivot(index="feature", columns="method", values="rho").round(2)
P["n"] = log[(log["sample"] == "primary_115") & (log.method == "spearman")].set_index("feature").n
P["q"] = log[(log["sample"] == "primary_115") & (log.method == "spearman")].set_index("feature").q_BH.round(4)
P["rho_all200"] = log[(log["sample"] == "all_200") & (log.method == "spearman")].set_index("feature").rho.round(2)
P["rhoW_all200"] = log[(log["sample"] == "all_200") & (log.method == "spearman_within_region")].set_index("feature").rho.round(2)
P = P.reindex(P.spearman.abs().sort_values(ascending=False).index)
print(P.to_string())

# ---- permutation null (primary sample, raw Spearman over all features, pairwise complete)
S = samples["primary_115"].reset_index(drop=True)
rng = np.random.default_rng(2026)
X = S[feats]
def maxabs(y):
    return max(abs(stats.spearmanr(X[x][X[x].notna()], y[X[x].notna()])[0]) for x in feats)
real = maxabs(S.t0.values)
null = np.array([maxabs(rng.permutation(S.t0.values)) for _ in range(1000)])
print(f"\nNULL: real max|rho|={real:.3f}; perm 95th pct={np.percentile(null,95):.3f}; 99th={np.percentile(null,99):.3f}; p_maxT={(null>=real).mean():.4f}")
# exclude flagged (proximate/post-t0/WPP-derived) features
clean = [x for x in feats if x not in ("contracep20_year", "female_lfp_1991_POSTT0", "life_exp_1950", "life_exp50_year")]
def maxabs2(y):
    return max(abs(stats.spearmanr(X[x][X[x].notna()], y[X[x].notna()])[0]) for x in clean)
real2 = maxabs2(S.t0.values)
null2 = np.array([maxabs2(rng.permutation(S.t0.values)) for _ in range(1000)])
print(f"NULL (non-flagged features only): real max|rho|={real2:.3f}; perm 95th={np.percentile(null2,95):.3f}")

# ---- LOO for top 3 (primary raw |rho|)
prim = log[(log["sample"] == "primary_115") & (log.method == "spearman")]
top = prim.reindex(prim.rho.abs().sort_values(ascending=False).index).feature.head(3).tolist()
top_clean = prim[prim.feature.isin(clean)].reindex(prim[prim.feature.isin(clean)].rho.abs().sort_values(ascending=False).index).feature.head(3).tolist()
loo_rows = []
for x in dict.fromkeys(top + top_clean):
    sub = S[["t0", x]].dropna().reset_index(drop=True)
    e_m, e_b = [], []
    for i in range(len(sub)):
        tr = sub.drop(i)
        b1, b0 = np.polyfit(tr[x], tr.t0, 1)
        e_m.append(abs(b0 + b1 * sub[x][i] - sub.t0[i]))
        e_b.append(abs(tr.t0.median() - sub.t0[i]))
    w = stats.wilcoxon(e_m, e_b)
    loo_rows.append(dict(feature=x, n=len(sub), MAE_median_model=np.median(e_m), MAE_median_baseline=np.median(e_b), wilcoxon_p=w.pvalue, top3_all=x in top, top3_nonflagged=x in top_clean))
loo = pd.DataFrame(loo_rows)
loo.to_csv(f"{od}/loo_top3.csv", index=False)
print("\nLOO:\n", loo.round(3).to_string())
pd.DataFrame({"null_max_abs_rho_all": null, "null_max_abs_rho_nonflagged": null2}).to_csv(f"{od}/permutasyon_null.csv", index=False)
