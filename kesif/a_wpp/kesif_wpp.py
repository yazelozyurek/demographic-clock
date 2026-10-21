"""Exploratory search: WPP-derived features vs fertility turning point t0.
Run from project root:  python kesif/a_wpp/kesif_wpp.py
Writes only into kesif/a_wpp/."""
import numpy as np, pandas as pd, warnings
from pathlib import Path
from scipy import stats
from scipy.optimize import curve_fit
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]; OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(2026)

t = pd.read_csv(ROOT/"clean/t0_tablosu.csv").set_index("LocID")
d = pd.read_csv(ROOT/"clean/countries_1950_2100.csv", low_memory=False)
d = d[d.LocID.isin(t.index)]
P = lambda v, lo=1950, hi=2100: d[(d.Time>=lo)&(d.Time<=hi)].pivot(index="LocID", columns="Time", values=v).reindex(t.index)

F = {}          # feature -> Series
META = {}       # feature -> dict(group, note)
def add(name, s, group, note=""):
    F[name] = s.reindex(t.index).astype(float); META[name] = dict(group=group, note=note)

# ---------- 1) threshold-crossing years (linear interpolation, full 1950-2100 series)
def cross_year(M, thr, rising):
    out = pd.Series(np.nan, index=M.index); cens = pd.Series(False, index=M.index)
    yrs = M.columns.values.astype(float)
    for i, row in M.iterrows():
        v = row.values
        ok = (v >= thr) if rising else (v <= thr)
        if ok[0]: cens[i] = True; continue         # already past threshold in 1950 -> left-censored
        if not ok.any(): continue                  # never crosses by 2100 -> right-censored
        j = np.argmax(ok); y0, y1, a, b = yrs[j-1], yrs[j], v[j-1], v[j]
        out[i] = y0 + (thr-a)/(b-a)*(y1-y0) if b != a else y1
    return out, cens
CENS = {}
specs = [("LEx", [45,50,55,60,65,70], True), ("IMR", [200,150,100,75,50,30], False),
         ("Q5", [300,250,200,150,100,50], False), ("CDR", [25,20,15,10], False),
         ("LE15", [50,55,60], True), ("LExFemale", [50,60,70], True)]
for v, thrs, rising in specs:
    M = P(v)
    for thr in thrs:
        y, c = cross_year(M, thr, rising)
        nm = f"yr_{v}_{'ge' if rising else 'le'}{thr}"
        add(nm, y, "timing", "threshold crossing year; left-censored(<=1950) dropped")
        CENS[nm] = c

# ---------- 2) shared-curve midpoint years for mortality (same method as t0, 1950-2023 only)
def sig(z, L, U, k): return L + (U-L)/(1+np.exp(k*z))      # decreasing if k>0
def shared_shift(Y, init, p0, rounds=8):
    yil = Y.columns.values.astype(float); aday = np.arange(1850, 2150.5, 0.5); s = init.astype(float)
    for _ in range(rounds):
        z = (yil[None,:]-s.values[:,None]).ravel()
        (L,U,k),_ = curve_fit(sig, z, Y.values.ravel(), p0=p0, maxfev=20000)
        tab = sig(yil[None,:]-aday[:,None], L, U, k)
        err = ((tab[None]-Y.values[:,None,:])**2).sum(2)
        s = pd.Series(aday[err.argmin(1)], index=Y.index)
    edge = (s<=1850.5)|(s>=2149.5)
    return s.where(~edge), (L,U,k)
Ylex = P("LEx", 1950, 2023)
init = Ylex.apply(lambda r: r.index[np.argmax(r.values>=55)] if (r>=55).any() else 2030, axis=1)
s_lex, par_lex = shared_shift(Ylex, init, p0=[75,35,-0.05])
add("mid_LEx_shared", s_lex, "timing", f"shared logistic shift for LEx 1950-2023, params {np.round(par_lex,3)}")
Yimr = np.log(P("IMR", 1950, 2023))
init = Yimr.apply(lambda r: r.index[np.argmax(r.values<=np.log(80))] if (r<=np.log(80)).any() else 2030, axis=1)
s_imr, par_imr = shared_shift(Yimr, init, p0=[1.5,5.3,0.05])
add("mid_logIMR_shared", s_imr, "timing", f"shared logistic shift for log IMR 1950-2023, params {np.round(par_imr,3)}")

# ---------- 3) baseline levels 1950 and 1960
def lvl(v, y): return P(v, y, y)[y]
for y in (1950, 1960):
    add(f"logIMR_{y}", np.log(lvl("IMR",y)), "baseline")
    add(f"logQ5_{y}", np.log(lvl("Q5",y)), "baseline")
    add(f"LEx_{y}", lvl("LEx",y), "baseline")
    add(f"CDR_{y}", lvl("CDR",y), "baseline")
    add(f"LE15_{y}", lvl("LE15",y), "baseline")
    add(f"LE65_{y}", lvl("LE65",y), "baseline")
    add(f"Q1550F_{y}", lvl("Q1550Female",y), "baseline")
    add(f"LEgapFM_{y}", lvl("LExFemale",y)-lvl("LExMale",y), "baseline")
    add(f"logPop_{y}", np.log(lvl("TPopulation1July",y)), "baseline")
    add(f"logDensity_{y}", np.log(lvl("PopDensity",y)), "baseline")
    add(f"SRB_{y}", lvl("SRB",y), "baseline")
    add(f"PopSexRatio_{y}", lvl("PopSexRatio",y), "baseline")
add("CNMR_avg1950_60", P("CNMR",1950,1960).mean(1), "baseline")
add("absCNMR_avg1950_60", P("CNMR",1950,1960).abs().mean(1), "baseline")
# leakage group (TFR family / mechanically linked) -- logged but flagged
for y in (1950, 1960):
    for v in ["TFR","CBR","NRR","MAC","MedianAgePop","PopGrowthRate"]:
        add(f"LEAK_{v}_{y}", lvl(v,y), "leak", "TFR-family / mechanically linked")

# ---------- 4) early change 1950-1970
add("dlogIMR_1950_70", (np.log(lvl("IMR",1970))-np.log(lvl("IMR",1950)))/20, "change")
add("dLEx_1950_70", (lvl("LEx",1970)-lvl("LEx",1950))/20, "change")
add("dCDR_1950_70", (lvl("CDR",1970)-lvl("CDR",1950))/20, "change")
add("dlogQ5_1950_70", (np.log(lvl("Q5",1970))-np.log(lvl("Q5",1950)))/20, "change")
add("dLEx_1950_60", (lvl("LEx",1960)-lvl("LEx",1950))/10, "change")

# ---------- testing
def wr(x, g):  # within-region percentile rank
    return x.groupby(g).rank(pct=True)
samples = {"primary_reliable115": t.guvenilir.astype(bool), "secondary_all200": pd.Series(True, index=t.index)}
rows = []
for sname, mask in samples.items():
    T = t.t0[mask]; G = t.bolge[mask]
    for f, s in F.items():
        x = s[mask]; ok = x.notna()&T.notna(); n = int(ok.sum())
        if n < 10: continue
        r, p = stats.spearmanr(x[ok], T[ok])
        rr = wr(x[ok], G[ok]); tt = wr(T[ok], G[ok]); r2, p2 = stats.spearmanr(rr, tt)
        proj = np.nan
        if META[f]["group"]=="timing": proj = int((x[ok]>=2024).sum())
        base = dict(feature=f, group=META[f]["group"], sample=sname, n=n, n_threshold_ge2024=proj,
                    n_leftcensored=int(CENS[f][mask].sum()) if f in CENS else np.nan)
        rows.append({**base, "method":"spearman", "rho":r, "p":p})
        rows.append({**base, "method":"spearman_within_region", "rho":r2, "p":p2})
# extra: timing features restricted to countries where the mortality year is BEFORE t0 (prospective subset)
for sname, mask in samples.items():
    T = t.t0[mask]; G = t.bolge[mask]
    for f in ["mid_LEx_shared","mid_logIMR_shared","yr_LEx_ge55","yr_IMR_le100","yr_CDR_le10","yr_LEx_ge60"]:
        x = F[f][mask]; ok = x.notna()&(x<T); n=int(ok.sum())
        r,p = stats.spearmanr(x[ok],T[ok]); r2,p2 = stats.spearmanr(wr(x[ok],G[ok]), wr(T[ok],G[ok]))
        base = dict(feature=f+"|before_t0_only", group="timing_subset", sample=sname, n=n, n_threshold_ge2024=int((x[ok]>=2024).sum()), n_leftcensored=np.nan)
        rows.append({**base,"method":"spearman","rho":r,"p":p}); rows.append({**base,"method":"spearman_within_region","rho":r2,"p":p2})
log = pd.DataFrame(rows)
log["q_BH"] = multipletests(log.p.fillna(1), method="fdr_bh")[1]
log.to_csv(OUT/"test_log.csv", index=False)
print("total tests:", len(log))

# ---------- null calibration (primary sample, non-leak features, both methods)
mask = samples["primary_reliable115"]; T = t.t0[mask].values; G = t.bolge[mask]
feats = [f for f in F if META[f]["group"]!="leak"]
def maxabs(Tv):
    m = 0; Ts = pd.Series(Tv, index=G.index)
    for f in feats:
        x = F[f][mask]; ok = x.notna().values
        if ok.sum()<10: continue
        r = stats.spearmanr(x.values[ok], Tv[ok])[0]
        r2 = stats.spearmanr(wr(x[ok], G[ok]), wr(Ts[ok], G[ok]))[0]
        m = max(m, abs(r), abs(r2))
    return m
real = maxabs(T)
null = np.array([maxabs(rng.permutation(T)) for _ in range(300)])
p95 = np.quantile(null, .95)
print(f"null calib: real max|rho|={real:.3f}, null 95th={p95:.3f}, perm p={(null>=real).mean():.4f}")

# ---------- LOO for top 3 (primary, non-leak, raw spearman)
L1 = log[(log["sample"]=="primary_reliable115")&(log.method=="spearman")&(log.group.isin(["timing","baseline","change"]))].copy()
L1["a"] = L1.rho.abs(); top = L1.sort_values("a", ascending=False).head(3).feature.tolist()
loo = []
for f in top + ["LEx_1950", "LEx_1960", "logIMR_1950"]:
    x = F[f][mask]; ok = x.notna(); xv = x[ok].values; tv = t.t0[mask][ok].values; g = G[ok].values
    em, eb, er = [], [], []
    for i in range(len(xv)):
        j = np.arange(len(xv))!=i
        b1, b0 = np.polyfit(xv[j], tv[j], 1)
        em.append(abs(b0+b1*xv[i]-tv[i])); eb.append(abs(np.median(tv[j])-tv[i]))
        same = j & (g==g[i]); er.append(abs((np.median(tv[same]) if same.any() else np.median(tv[j]))-tv[i]))
    em, eb, er = map(np.array, (em, eb, er))
    loo.append(dict(role="top3" if f in top else "extra_fixed_date", feature=f, n=len(xv), MAE_model=np.median(em), MAE_median=np.median(eb),
                    MAE_region_median=np.median(er), wilcoxon_p_vs_median=stats.wilcoxon(em, eb).pvalue,
                    wilcoxon_p_vs_region=stats.wilcoxon(em, er).pvalue))
loo = pd.DataFrame(loo); loo.to_csv(OUT/"loo_top3.csv", index=False)

# ---------- descriptive "mortality first" lag (not tested against t0: contains t0)
lag = []
for f in ["yr_LEx_ge50","yr_LEx_ge55","yr_IMR_le100","yr_IMR_le50","mid_LEx_shared","mid_logIMR_shared"]:
    x = F[f][mask]; ok = x.notna(); dl = t.t0[mask][ok]-x[ok]
    lag.append(dict(feature=f, n=int(ok.sum()), median_lag=dl.median(), iqr_lag=dl.quantile(.75)-dl.quantile(.25),
                    share_mortality_first=(dl>0).mean(), sd_lag=dl.std(), sd_t0_same=t.t0[mask][ok].std()))
lag = pd.DataFrame(lag); lag.to_csv(OUT/"lag_descriptive.csv", index=False)

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 20)
for s in samples:
    S = log[(log["sample"]==s)].pivot_table(index="feature", columns="method", values=["rho","q_BH","n"])
    S["a"] = S[("rho","spearman")].abs(); print("\n==", s); print(S.sort_values("a", ascending=False).head(20).round(3))
print(loo.round(3))
P1 = log[(log["sample"]=="primary_reliable115")&(log.group=="timing")&(log.method=="spearman")]
print("primary: timing features with any threshold year >=2024:", P1[P1.n_threshold_ge2024>0][["feature","n","n_threshold_ge2024"]].to_string())
print("primary: share t0 > 1960:", (t.t0[t.guvenilir]>1960).mean().round(3), " t0 range", t.t0[t.guvenilir].min(), t.t0[t.guvenilir].max())
print(log[log.group=="timing_subset"].round(3).to_string())
print("max q among all tests:", round(log.q_BH.max(),3), " tests with q<0.05:", (log.q_BH<0.05).sum())
print("weakest/non-significant primary tests:"); print(log[(log["sample"]=="primary_reliable115")&(log.q_BH>=0.05)][["feature","method","n","rho","q_BH"]].round(3).to_string()); print(lag.round(2))
print("null quantiles", np.quantile(null,[.5,.95,.99]).round(3))
pd.Series(dict(real_max=real, null_p95=p95, null_p99=np.quantile(null,.99), n_perm=len(null),
               perm_p=(null>=real).mean(), n_features=len(feats))).to_csv(OUT/"null_calibration.csv")
