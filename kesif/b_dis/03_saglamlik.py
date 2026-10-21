"""Robustness: partial Spearman of top non-flagged features controlling for already-used
Barro-Lee women's schooling (25-64, 1950) and log Maddison GDP pc (1950). Appends to the
test log and recomputes BH-FDR across ALL logged tests.
Usage: python -I 03_saglamlik.py <t0_csv> <feature_csv> <barrolee_F2564_csv> <maddison_csv> <out_dir>"""
import sys, numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
t0p, fp, blp, mdp, od = sys.argv[1:6]
t = pd.read_csv(t0p)[["ISO3_code", "bolge", "t0", "guvenilir"]]
f = pd.read_csv(fp)
bl = pd.read_csv(blp).query("year == 1950")[["WBcode", "yr_sch"]].rename(columns={"WBcode": "ISO3_code", "yr_sch": "BL_women_sch_1950"})
md = pd.read_csv(mdp).query("year == 1950")[["code", "gdp_per_capita"]]
md = md.assign(log_gdp_1950=np.log(md.gdp_per_capita)).rename(columns={"code": "ISO3_code"})[["ISO3_code", "log_gdp_1950"]]
d = t.merge(f, on="ISO3_code").merge(bl, on="ISO3_code", how="left").merge(md, on="ISO3_code", how="left")
S = d[d.guvenilir]

def partial_spearman(sub, x, y, z):
    r = sub[[x, y] + z].rank()
    res = lambda v: r[v] - np.c_[np.ones(len(r)), r[z].values] @ np.linalg.lstsq(np.c_[np.ones(len(r)), r[z].values], r[v], rcond=None)[0]
    rho = np.corrcoef(res(x), res(y))[0, 1]
    df = len(sub) - 2 - len(z)
    tt = rho * np.sqrt(df / (1 - rho**2))
    return rho, 2 * stats.t.sf(abs(tt), df)

rows = []
for x in ["literacy_1950", "some_formal_edu_1950", "primary_net_enrol_1950", "urban_share_1950", "vdem_electdem_1950", "child_mort_1960_log"]:
    for z in (["BL_women_sch_1950"], ["log_gdp_1950"]):
        sub = S[[x, "t0"] + z].dropna()
        rho, p = partial_spearman(sub, x, "t0", z)
        rows.append(dict(feature=x, definition=f"partial Spearman given {z[0]}", sample="primary_115", method="partial_spearman", n=len(sub), rho=rho, p=p))
    # reference: the already-used control's own rho in the same subsample
    sub = S[[x, "t0", "BL_women_sch_1950"]].dropna()
    r, p = stats.spearmanr(sub.BL_women_sch_1950, sub.t0)
    rows.append(dict(feature="BL_women_sch_1950 (reference)", definition=f"same subsample as {x}", sample="primary_115", method="spearman", n=len(sub), rho=r, p=p))
    r, p = stats.spearmanr(sub[x], sub.BL_women_sch_1950)
    rows.append(dict(feature=f"{x} vs BL_women_sch_1950", definition="collinearity check (feature vs control), not a t0 test, excluded from FDR", sample="primary_115", method="collinearity_check", n=len(sub), rho=r, p=p))
log = pd.read_csv(f"{od}/test_kaydi.csv")
log = log[~log.method.isin(["partial_spearman", "collinearity_check"])]
log = log[~log.feature.str.contains("BL_women", regex=False)]
log = pd.concat([log, pd.DataFrame(rows)], ignore_index=True)
m = log.method != "collinearity_check"
log["q_BH"] = np.nan
log.loc[m, "q_BH"] = multipletests(log.loc[m, "p"], method="fdr_bh")[1]
print("t0 tests in FDR:", int(m.sum()))
log.to_csv(f"{od}/test_kaydi.csv", index=False)
print("total tests now:", len(log))
print(log.iloc[-len(rows):].round(4).to_string())
miss = S[S.literacy_1950.isna()].bolge.value_counts()
print("\nprimary countries missing literacy_1950:", miss.to_dict())
for reg, g in S.dropna(subset=["literacy_1950"]).groupby("bolge"):
    if len(g) >= 8:
        r, p = stats.spearmanr(g.literacy_1950, g.t0); print(f"  literacy rho within {reg}: {r:.2f} (n={len(g)}, p={p:.3g})")
