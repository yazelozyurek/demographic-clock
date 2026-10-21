"""Build tidy feature table (ISO3_code + features) from OWID grapher CSVs.
Usage: python -I 01_ozellik_tablosu.py <download_root> <t0_table_csv> <out_csv>
All features are measured at a fixed baseline year (1950; 1961 for FAO calories)
or are timing features (first year a threshold is crossed, linear interpolation)."""
import sys, numpy as np, pandas as pd

root, t0path, out = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = pd.read_csv(t0path)
iso = set(t0.ISO3_code)

def load(slug, col=None):
    d = pd.read_csv(f"{root}/{slug}/data.csv")
    d = d[d.code.isin(iso)]
    col = col or d.columns[3]
    return d[["code", "year", col]].rename(columns={col: "v"}).dropna()

def at_year(d, y, window=0):
    """value at year y (if window>0, nearest observation within +-window years)."""
    if window == 0:
        s = d[d.year == y].set_index("code").v
    else:
        dd = d[(d.year - y).abs() <= window].copy()
        dd["dist"] = (dd.year - y).abs()
        s = dd.sort_values("dist").groupby("code").v.first()
    return s

def cross_year(d, thr, direction="up", y0=1950, y1=2050):
    """First year the (interpolated) series crosses thr. Left-censored (already past at
    first obs >= y0) -> first obs year; never crossed by last obs -> last obs year + 1.
    Returns (year, censor flag: 0 none, -1 left, +1 right)."""
    res = {}
    for c, g in d[(d.year >= y0) & (d.year <= y1)].groupby("code"):
        g = g.sort_values("year")
        y, v = g.year.values.astype(float), g.v.values.astype(float)
        if len(y) < 2:
            continue
        past = v >= thr if direction == "up" else v <= thr
        if past[0]:
            res[c] = (y[0], -1); continue
        if not past.any():
            res[c] = (y[-1] + 1, 1); continue
        i = np.argmax(past)
        yc = y[i-1] + (thr - v[i-1]) * (y[i] - y[i-1]) / (v[i] - v[i-1])
        res[c] = (yc, 0)
    s = pd.DataFrame(res, index=["yr", "cens"]).T
    return s

F = {}; C = {}
urb = load("share-of-population-urban")
urbp = load("urban-population-share-2050", "share__area_type_urban__data_type_projections__projected")
urb_all = pd.concat([urb, urbp[urbp.year > urb.year.max()]])
F["urban_share_1950"] = at_year(urb, 1950)
s = cross_year(urb_all, 30, "up"); F["urban30_year"] = s.yr; C["urban30_year"] = s.cens
s = cross_year(urb_all, 50, "up"); F["urban50_year"] = s.yr; C["urban50_year"] = s.cens

cm = load("child-mortality")            # % of children dying before age 5
F["child_mort_1950_log"] = np.log(at_year(cm, 1950))
F["child_mort_1960_log"] = np.log(at_year(cm, 1960))   # fallback baseline (1950 coverage thin)
s = cross_year(cm, 10, "down", y0=1800); F["child_mort_below10pct_year"] = s.yr; C["child_mort_below10pct_year"] = s.cens

lit = load("cross-country-literacy-rates")
F["literacy_1950"] = at_year(lit, 1950)

vd = load("electoral-democracy-index", "electdem_vdem__estimate_best")
F["vdem_electdem_1950"] = at_year(vd, 1950)

pdn = load("population-density")
F["pop_density_1950_log"] = np.log(at_year(pdn, 1950))

le = load("life-expectancy")
F["life_exp_1950"] = at_year(le, 1950)
s = cross_year(le, 50, "up", y0=1850); F["life_exp50_year"] = s.yr; C["life_exp50_year"] = s.cens

cal = load("daily-per-capita-caloric-supply")
F["calories_1961"] = at_year(cal, 1961)

edu = load("share-of-women-15-years-and-older-with-no-education")   # col: some_formal_education_both_sexes
F["some_formal_edu_1950"] = at_year(edu, 1950)
s = cross_year(edu, 50, "up", y0=1870); F["some_formal_edu50_year"] = s.yr; C["some_formal_edu50_year"] = s.cens

enr = load("primary-enrollment-selected-countries")
F["primary_net_enrol_1950"] = at_year(enr, 1950, window=2)
s = cross_year(enr, 50, "up", y0=1820); F["primary_enrol50_year"] = s.yr; C["primary_enrol50_year"] = s.cens

cp = load("contraceptive-prevalence-any-methods-of-women-ages-15-49")
s = cross_year(cp, 20, "up", y0=1960); s = s[s.cens == 0]   # only bracketed crossings
F["contracep20_year"] = s.yr; C["contracep20_year"] = s.cens

flfp = load("female-labor-force-participation-rates")
F["female_lfp_1991_POSTT0"] = at_year(flfp, 1991)

tab = pd.DataFrame(F); tab.index.name = "ISO3_code"
for k, v in C.items():
    tab[k + "_cens"] = v
tab = t0[["ISO3_code"]].merge(tab.reset_index(), on="ISO3_code", how="left")
tab.to_csv(out, index=False)
print(tab.drop(columns="ISO3_code").notna().sum().to_string())
print(tab[[c for c in tab if c.endswith("_cens")]].apply(lambda s: s.value_counts()).T)
