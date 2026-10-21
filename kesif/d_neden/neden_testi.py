"""Ön kayıtlı doğal deney testi (plan: kesif/d_neden/plan.md, commit ef38cd2).
Araç: Acemoglu & Johnson (2007) tahmini ölüm, 1940 (PM40). Açıklayıcı: sağlık saati. Sonuç: doğurganlık saati (t0).
Çalıştırma (proje klasöründen):  python kesif/d_neden/neden_testi.py
Çıktı: ekrana tablo + kesif/d_neden/sonuc.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

KOK = Path(__file__).resolve().parent.parent.parent
aj = pd.read_stata(KOK / "data_dis/aj2007/disease.dta")
aj = aj[(aj["year"] == 1940) & (aj["sjbasesamplenoncomm"] == 1) & (aj["sample40"] == 1)].copy()
aj["dort"] = aj[["malaria", "tball", "pneumonia", "smallpox"]].sum(axis=1)   # dört büyük hastalık (1940 ölüm hızı)
aj["loggdp40"] = np.log(aj["gdppcmadd"])
s = pd.read_csv(KOK / "clean/saglik_saati.csv")
d = aj.merge(s, left_on="shortnam", right_on="ISO3_code", how="inner")
d = d[d["t0_saglik"].notna() & d["t0"].notna()]
S25 = d[d["guvenilir"] == True].copy()
S47 = d.copy()

def ols(y, X):
    return sm.OLS(y, sm.add_constant(X)).fit(cov_type="HC1")

def iv(df, arac="compsjmhatit", kontrol=("lifeexpect", "loggdp40")):
    k = list(kontrol)
    y, x, z, W = df["t0"].values, df["t0_saglik"].values, df[arac].values, df[k].values if k else np.empty((len(df), 0))
    ilk = ols(x, np.column_stack([z, W]))                     # 1. aşama
    pi, F = ilk.params[1], ilk.tvalues[1] ** 2                 # tek araçta dayanıklı F = t²
    ind = ols(y, np.column_stack([z, W]))                      # indirgenmiş form
    # 2SLS: x yerine 1. aşama tahmini; standart hata gerçek x ile kurulan artıklardan (HC1)
    Xh = sm.add_constant(np.column_stack([ilk.fittedvalues, W]))
    Xg = sm.add_constant(np.column_stack([x, W]))
    b = np.linalg.lstsq(Xh, y, rcond=None)[0]
    u = y - Xg @ b
    n, p = Xh.shape
    A = np.linalg.inv(Xh.T @ Xh)
    V = A @ (Xh.T * u ** 2) @ Xh @ A * n / (n - p)
    beta, se = b[1], np.sqrt(V[1, 1])
    # Anderson–Rubin %95 kümesi: y − β0·x, araca karşı anlamsız kalan β0'lar
    izgara = np.arange(-6, 6.0001, 0.01)
    kabul = [b0 for b0 in izgara if ols(y - b0 * x, np.column_stack([z, W])).pvalues[1] > 0.05]
    if not kabul: ar = "boş"
    elif np.isclose(min(kabul), izgara[0]) or np.isclose(max(kabul), izgara[-1]): ar = f"sınırsız ({min(kabul):.2f}…{max(kabul):.2f} ızgarada)"
    else:
        bosluk = np.diff(kabul).max() > 0.011
        ar = f"[{min(kabul):.2f}, {max(kabul):.2f}]" + (" (parçalı)" if bosluk else "")
    o = ols(y, np.column_stack([x, W]))                        # karşılaştırma için OLS
    return dict(n=n, pi=pi, pi_p=ilk.pvalues[1], F=F, ind=ind.params[1], ind_p=ind.pvalues[1],
                beta=beta, beta_se=se, beta_p=2 * stats.norm.sf(abs(beta / se)), AR=ar, ols_beta=o.params[1], ols_p=o.pvalues[1])

satir = {
    "ANA: S25, PM40, kontrol LE40+gelir40": iv(S25),
    "D1: S47 (çıkarımla saatler dahil)": iv(S47),
    "D2: S25, dört hastalık endeksi": iv(S25, arac="dort"),
    "D3: S25, kontrolsüz": iv(S25, kontrol=()),
}
loo = [iv(S25.drop(i))["beta"] for i in S25.index]
sonuc = pd.DataFrame(satir).T
pd.set_option("display.width", 200, "display.max_columns", 20)
print(f"S25 ülkeleri: {', '.join(sorted(S25['Location']))}\n")
print(sonuc.to_string(float_format=lambda v: f"{v:.3f}"))
print(f"\nD4: bir ülkeyi dışarıda bırakınca ana β: {min(loo):.2f} … {max(loo):.2f}")
print("\nkorelasyon S25 (Spearman): PM40~LE40", round(stats.spearmanr(S25["compsjmhatit"], S25["lifeexpect"])[0], 2),
      "· PM40~dört", round(stats.spearmanr(S25["compsjmhatit"], S25["dort"])[0], 2))
sonuc.to_csv(KOK / "kesif/d_neden/sonuc.csv")
