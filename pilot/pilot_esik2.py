import json, sys, numpy as np, pandas as pd
D = sys.argv[1]
v = json.load(open("/Users/yazelsudeozyurek/asa data python/arac/gezgin_veri.json"))
u = pd.DataFrame(v["ulkeler"])
g = pd.read_csv(f"{D}/gdp-per-capita-maddison-project-database.csv").rename(columns={"code":"iso3","gdp_per_capita":"gdp"})
s = pd.read_csv(f"{D}/mean-years-of-schooling-long-run.csv"); s = s.rename(columns={s.columns[-1]:"edu","code":"iso3"})
iso = set(u.iso3)
def panel(df,col):
    df = df[df.iso3.isin(iso) & df[col].notna() & (df[col]>0)]
    out = {}
    for i,d in df.groupby("iso3"):
        d = d.sort_values("year"); yrs = np.arange(max(1950,d.year.min()), min(2020,d.year.max())+1)
        if len(yrs): out[i] = pd.Series(np.interp(yrs, d.year, np.log(d[col])), index=yrs)
    return pd.DataFrame(out)          # yıl x ülke, log değer
G, E = panel(g,"gdp"), panel(s,"edu")
ok = u[(u.t0>=1950)&(u.t0<=2015)&((u.hi-u.lo)<=25)].copy()
ok["yr"] = ok.t0.round().astype(int)
ok = ok[ok.iso3.isin(G.columns) & ok.iso3.isin(E.columns)]
ok["lg"] = [G.at[y,i] if y in G.index else np.nan for i,y in zip(ok.iso3,ok.yr)]
ok["le"] = [E.at[y,i] if y in E.index else np.nan for i,y in zip(ok.iso3,ok.yr)]
ok = ok.dropna(subset=["lg","le"])
print("gelir + eğitim verisi olan ülke:", len(ok), "/ 200 | bölgeler:", ok.bolge.value_counts().to_dict())
# Kıyas: aynı ülkeler, aynı yıl dağılımında rastgele bir anda (her ülke için t0 yerine rastgele kaydırılmış bir yıl)
rng = np.random.default_rng(7)
def ratio(idx):
    d = ok.iloc[idx]
    return np.std(d["lg"],ddof=1), np.std(d["le"],ddof=1)
sg, se = ratio(np.arange(len(ok)))
# Kıyas dağılımı: aynı yıllardaki bütün ülkelerin yayılımı
bg = np.mean([G.loc[y].dropna().std() for y in ok.yr])
be = np.mean([E.loc[y].dropna().std() for y in ok.yr])
print(f"Gelir:  t0'daki SD(log) {sg:.3f} | aynı yıllarda dünya SD(log) {bg:.3f} | daralma oranı {sg/bg:.2f}")
print(f"Eğitim: t0'daki SD(log) {se:.3f} | aynı yıllarda dünya SD(log) {be:.3f} | daralma oranı {se/be:.2f}")
B=[]
for _ in range(2000):
    i = rng.integers(0,len(ok),len(ok)); a,b = ratio(i); B.append((a/bg)/(b/be))
print("göreli daralma (gelir/eğitim):", round((sg/bg)/(se/be),2), np.percentile(B,[2.5,97.5]).round(2))
# Permütasyon: t0 yerine rastgele yıllar -> 'eşik' gerçekten t0'ya mı özgü?
perm_g, perm_e = [], []
for _ in range(1000):
    yrs = rng.integers(1950,2016,len(ok))
    lg = [G.at[y,i] for i,y in zip(ok.iso3,yrs)]; le = [E.at[y,i] for i,y in zip(ok.iso3,yrs)]
    perm_g.append(np.std(lg,ddof=1)); perm_e.append(np.std(le,ddof=1))
print(f"Rastgele yıllar: gelir SD medyan {np.median(perm_g):.3f}, eğitim SD medyan {np.median(perm_e):.3f}")
print(f"p (gelir t0 SD <= rastgele): {np.mean(np.array(perm_g)<=sg):.3f} | p (eğitim): {np.mean(np.array(perm_e)<=se):.3f}")
print("Türkiye:", ok[ok.ad=="Türkiye"][["yr"]].values.ravel(), "gelir", round(np.exp(ok[ok.ad=='Türkiye']["lg"].iloc[0])), "eğitim", round(np.exp(ok[ok.ad=='Türkiye']["le"].iloc[0]),1))
print("eğitim t0'da: medyan", round(np.exp(ok["le"].median()),1), "p10-p90", np.exp(np.percentile(ok.le,[10,90])).round(1), "| gelir medyan", round(np.exp(ok["lg"].median())), "p10-p90", np.exp(np.percentile(ok["lg"],[10,90])).round(0))
