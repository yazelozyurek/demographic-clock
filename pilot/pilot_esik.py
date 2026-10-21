import json, sys, numpy as np, pandas as pd
D = sys.argv[1]
v = json.load(open("/Users/yazelsudeozyurek/asa data python/arac/gezgin_veri.json"))
u = pd.DataFrame(v["ulkeler"])[["iso3","ad","bolge","t0","lo","hi","pop2023"]]
g = pd.read_csv(f"{D}/gdp-per-capita-maddison-project-database.csv").rename(columns={"code":"iso3","gdp_per_capita":"gdp"})
s = pd.read_csv(f"{D}/mean-years-of-schooling-long-run.csv"); s = s.rename(columns={s.columns[-1]:"edu","code":"iso3"})
urb = pd.read_csv(f"{D}/share-of-population-urban.csv"); urb = urb.rename(columns={urb.columns[-1]:"urb","code":"iso3"})
def at(df, col, iso, t):
    d = df[(df.iso3==iso)&df[col].notna()].sort_values("year")
    if len(d)<2 or t < d.year.min() or t > d.year.max(): return np.nan
    return np.exp(np.interp(t, d.year, np.log(d[col].clip(lower=1e-3))))
ok = u[(u.t0>=1950)&(u.t0<=2015)&((u.hi-u.lo)<=25)].copy()
for col,df in [("gdp",g),("edu",s),("urb",urb)]:
    ok[col] = [at(df,col,i,t) for i,t in zip(ok.iso3, ok.t0)]
print("t0 1950-2015 ve aralık <=25 yıl olan ülke:", len(ok))
c = ok.dropna(subset=["gdp","edu","urb"])
print("üç veride de olan:", len(c))
rng = np.random.default_rng(1)
def sdlog(x): return np.std(np.log(x), ddof=1)
for col in ["gdp","edu","urb"]:
    x = c[col].values
    b = [sdlog(rng.choice(x,len(x))) for _ in range(2000)]
    print(f"{col}: medyan {np.median(x):8.2f}  min {x.min():8.2f}  max {x.max():9.2f}  max/min {x.max()/x.min():6.1f}x  SD(log) {sdlog(x):.3f} [{np.percentile(b,2.5):.3f}, {np.percentile(b,97.5):.3f}]  p10-p90 oranı {np.percentile(x,90)/np.percentile(x,10):.1f}x")
# paired bootstrap of ratio SD(log gdp)/SD(log edu)
idx = [rng.integers(0,len(c),len(c)) for _ in range(2000)]
r = [sdlog(c.gdp.values[i])/sdlog(c.edu.values[i]) for i in idx]
print("SD(log gelir)/SD(log eğitim):", round(sdlog(c.gdp)/sdlog(c.edu),2), np.percentile(r,[2.5,97.5]).round(2))
pd.set_option("display.width",200)
show = ["Türkiye","Republic of Korea","Bangladesh","Iran (Islamic Republic of)","Brazil","India","China","Kenya","Mexico","Egypt","Indonesia","Viet Nam","Saudi Arabia","Kuwait","Sri Lanka","Myanmar","South Africa","Ghana"]
print(c.set_index("ad").reindex(show)[["t0","gdp","edu","urb"]].round({"t0":0,"gdp":0,"edu":1,"urb":0}))
print("\nEn zengin 5 (t0'da):"); print(c.nlargest(5,"gdp")[["ad","t0","gdp","edu"]].round(1).to_string(index=False))
print("\nEn yoksul 5 (t0'da):"); print(c.nsmallest(5,"gdp")[["ad","t0","gdp","edu"]].round(1).to_string(index=False))
print("\nkorelasyonlar t0 ile:", c[["t0","gdp","edu","urb"]].corr(method="spearman").round(2).iloc[0].to_dict())
