import json, sys, numpy as np, pandas as pd
OW, BL = sys.argv[1], sys.argv[2]
v = json.load(open("/Users/yazelsudeozyurek/asa data python/arac/gezgin_veri.json"))
u = pd.DataFrame(v["ulkeler"])
g = pd.read_csv(f"{OW}/gdp-per-capita-maddison-project-database.csv").rename(columns={"code":"iso3","gdp_per_capita":"val"})
def bl(f):
    d = pd.read_csv(f"{BL}/{f}.csv"); return d.rename(columns={"WBcode":"iso3","yr_sch":"val"})[["iso3","year","val"]]
srcs = {"gelir": g[["iso3","year","val"]], "egitim_kadin": bl("F2534"), "egitim_toplam": bl("MF")}
iso = set(u.iso3)
P = {}
for k,df in srcs.items():
    df = df[df.iso3.isin(iso) & df.val.notna() & (df.val>0)]
    out = {}
    for i,d in df.groupby("iso3"):
        d = d.sort_values("year"); yrs = np.arange(max(1950,d.year.min()), min(2020,d.year.max())+1)
        if len(yrs)>1: out[i] = pd.Series(np.interp(yrs, d.year, np.log(d.val)), index=yrs)
    P[k] = pd.DataFrame(out)
rng = np.random.default_rng(11)
def run(maxw, label):
    ok = u[(u.t0>=1952)&(u.t0<=2013)&((u.hi-u.lo)<=maxw)].copy(); ok["yr"]=ok.t0.round().astype(int)
    for k,Pk in P.items():
        ok[k] = [Pk.at[y,i] if (i in Pk.columns and y in Pk.index) else np.nan for i,y in zip(ok.iso3,ok.yr)]
    ok = ok.dropna(subset=list(P)); n=len(ok)
    print(f"\n=== {label}: {n} ülke | {ok.bolge.value_counts().to_dict()}")
    res = {}
    for k in P:
        sd = ok[k].std(); world = np.mean([P[k].loc[y].dropna().std() for y in ok.yr]); res[k]=(sd,world)
        w = ok.pop2023/ok.pop2023.sum(); m = (w*ok[k]).sum(); sdw = np.sqrt((w*(ok[k]-m)**2).sum())
        print(f"  {k:14s} t0'da SD(log) {sd:.3f}  dünya {world:.3f}  daralma {sd/world:.2f}  | nüfus ağırlıklı SD {sdw:.3f} daralma {sdw/world:.2f}  | medyan {np.exp(ok[k].median()):.1f}")
    for e in ["egitim_kadin","egitim_toplam"]:
        B=[]
        for _ in range(3000):
            i = rng.integers(0,n,n); d=ok.iloc[i]
            B.append((d["gelir"].std()/res["gelir"][1])/(d[e].std()/res[e][1]))
        print(f"  göreli daralma gelir/{e}: {(res['gelir'][0]/res['gelir'][1])/(res[e][0]/res[e][1]):.2f}  %95 [{np.percentile(B,2.5):.2f}, {np.percentile(B,97.5):.2f}]")
    # Eşik ile t0 tahmini (bir ülkeyi dışarıda bırakarak): eşik = diğer ülkelerin t0'daki medyanı
    for k in P:
        err=[]
        for j,r in enumerate(ok.itertuples()):
            thr = np.median(np.delete(ok[k].values, j))
            s = P[k][r.iso3].dropna()
            above = s[s>=thr]
            if len(above)==0 or s.iloc[0]>=thr: err.append(np.nan); continue
            err.append(above.index[0]-r.t0)
        err=np.array(err); ok[f"err_{k}"]=err
        print(f"  eşik tahmini {k:14s}: tahmin edilebilen {np.isfinite(err).sum()}/{n}, medyan |hata| {np.nanmedian(np.abs(err)):.1f} yıl, ortalama |hata| {np.nanmean(np.abs(err)):.1f} yıl")
    both = ok[[f"err_gelir","err_egitim_kadin"]].dropna()
    a, b = both.iloc[:,0].abs().values, both.iloc[:,1].abs().values
    from scipy.stats import wilcoxon
    print(f"  aynı ülkelerde (n={len(both)}): gelir |hata| medyan {np.median(a):.1f}, kadın eğitimi {np.median(b):.1f}, Wilcoxon p={wilcoxon(a,b).pvalue:.4f}")
    return ok
ok = run(25, "ana analiz (aralık ≤ 25 yıl)")
run(15, "sağlamlık (aralık ≤ 15 yıl)")
show = ["Türkiye","Republic of Korea","Bangladesh","Iran (Islamic Republic of)","Brazil","India","China","Venezuela (Bolivarian Republic of)","Mexico","Egypt","Indonesia","Kenya"]
t = ok.set_index("ad").reindex(show)[["yr","gelir","egitim_kadin","egitim_toplam","err_gelir","err_egitim_kadin"]].copy()
for c in ["gelir","egitim_kadin","egitim_toplam"]: t[c]=np.exp(t[c])
print(t.round({"gelir":0,"egitim_kadin":1,"egitim_toplam":1,"err_gelir":0,"err_egitim_kadin":0}))

print("\n=== Kıyas: sadece takvim yılı (her ülkeye diğerlerinin medyan t0'ı)")
t0 = ok.t0.values
base = np.array([abs(t0[j]-np.median(np.delete(t0,j))) for j in range(len(t0))])
print(f"  medyan |hata| {np.median(base):.1f} yıl, ortalama {base.mean():.1f}")
m = np.isfinite(ok.err_egitim_kadin.values)
from scipy.stats import wilcoxon
print(f"  aynı {m.sum()} ülkede: takvim {np.median(base[m]):.1f} vs kadın eğitimi {np.nanmedian(np.abs(ok.err_egitim_kadin.values[m])):.1f}, Wilcoxon p={wilcoxon(base[m], np.abs(ok.err_egitim_kadin.values[m])).pvalue:.4f}")
m2 = np.isfinite(ok.err_gelir.values)
print(f"  aynı {m2.sum()} ülkede: takvim {np.median(base[m2]):.1f} vs gelir {np.nanmedian(np.abs(ok.err_gelir.values[m2])):.1f}, Wilcoxon p={wilcoxon(base[m2], np.abs(ok.err_gelir.values[m2])).pvalue:.4f}")
tr = ok[ok.ad=="Türkiye"].iloc[0]
print("\nTürkiye 1981: gelir", round(np.exp(tr.gelir)), "| kadın eğitimi", round(np.exp(tr.egitim_kadin),2), "| toplam", round(np.exp(tr.egitim_toplam),2), "| t0'daki medyan kadın eğitimi", round(np.exp(ok.egitim_kadin.median()),2))
print("Türkiye kadın eğitimi eşiği geçiş yılı ~", int(tr.t0 + tr.err_egitim_kadin))
print("kadın eğitimi t0'da min/max:", ok.loc[ok.egitim_kadin.idxmin(),"ad"], round(np.exp(ok.egitim_kadin.min()),2), "/", ok.loc[ok.egitim_kadin.idxmax(),"ad"], round(np.exp(ok.egitim_kadin.max()),2))
r = ok.assign(ek=np.exp(ok.egitim_kadin), gl=np.exp(ok.gelir)).sort_values("ek")
print("\nTürkiye sırası (genç kadın eğitimi, düşükten yükseğe):", list(r.ad).index("Türkiye")+1, "/", len(r))
print("Türkiye'den düşük olanlar:", ", ".join(f"{a} {e:.1f}" for a,e in zip(r.ad[:list(r.ad).index('Türkiye')], r.ek)))
print("gelir sırası (düşükten):", list(ok.sort_values('gelir').ad).index("Türkiye")+1, "/", len(ok))
