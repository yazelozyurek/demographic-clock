"""Ön kayıtlı uzun fark testi (plan: kesif/f_kreitmeir/plan.md, commit 52407d4).
Araç: Kreitmeir & Überfuhr (2024) ülke düzeyi tahmini ölüm değişimi. Açıklayıcı: Δln yaşam beklentisi 1940→1980.
Sonuç: ΔTFR 1950→1990 (WPP). Standart hatalar ctrycluster kümelemeli.
Çalıştırma (proje klasöründen):  python kesif/f_kreitmeir/ku_testi.py
Çıktı: ekrana tablo + kesif/f_kreitmeir/sonuc.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

KOK = Path(__file__).resolve().parent.parent.parent
K = pd.read_csv(KOK / "data_dis/kreitmeir/ku_data.csv")
p = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["ISO3_code", "pop2023", "Time", "TFR", "LEx"])
p = p[p["pop2023"] >= 100]
w = p.pivot_table(index="ISO3_code", columns="Time", values=["TFR", "LEx"])
s = pd.read_csv(KOK / "clean/saglik_saati.csv").set_index("ISO3_code")

def veri(bayrak, arac):
    """Bir örneklemin işaretli satırları (aynı ülkenin başka coğrafi tanımları dışarıda) + WPP değişkenleri."""
    x = K[(K[bayrak] == 1) & K[arac].notna()].copy()
    assert not x["iso3"].duplicated().any()
    x = x.set_index("iso3")
    for a, b in [(1950, 1980), (1950, 1990), (1950, 2000)]:
        x[f"dTFR_{a}_{b}"] = (w["TFR"][b] - w["TFR"][a]).reindex(x.index)
    x["lnLE40"] = np.log(w["LEx"][1980].reindex(x.index)) - x["changelifeexpect"]
    x["t0"] = s["t0"].reindex(x.index); x["t0_saglik"] = s["t0_saglik"].reindex(x.index); x["guv"] = s["guvenilir"].reindex(x.index)
    x["z"] = x[arac]
    return x

def kume_ols(y, X, g):
    return sm.OLS(y, sm.add_constant(X)).fit(cov_type="cluster", cov_kwds={"groups": g})

def iv(df, y="dTFR_1950_1990", x="changelifeexpect", kontrol=()):
    d = df.dropna(subset=[y, x, "z", *kontrol])
    Y, X, Z, g = d[y].values, d[x].values, d["z"].values, d["ctrycluster"].values
    W = d[list(kontrol)].values if kontrol else np.empty((len(d), 0))
    ilk = kume_ols(X, np.column_stack([Z, W]), g)
    ind = kume_ols(Y, np.column_stack([Z, W]), g)
    Xh = sm.add_constant(np.column_stack([ilk.fittedvalues, W])); Xg = sm.add_constant(np.column_stack([X, W]))
    b = np.linalg.lstsq(Xh, Y, rcond=None)[0]; u = Y - Xg @ b
    A = np.linalg.inv(Xh.T @ Xh); n, k = Xh.shape
    S = sum(np.outer(Xh[g == c].T @ u[g == c], Xh[g == c].T @ u[g == c]) for c in np.unique(g))
    G = len(np.unique(g)); V = A @ S @ A * (G / (G - 1)) * ((n - 1) / (n - k))   # Stata "small" düzeltmesi
    beta, se = b[1], np.sqrt(V[1, 1])
    adim = 0.01 if "t0" not in y else 0.02
    izgara = np.arange(-30, 30.0001, adim) if "t0" not in y else np.arange(-6, 6.0001, adim)
    kabul = [b0 for b0 in izgara if kume_ols(Y - b0 * X, np.column_stack([Z, W]), g).pvalues[1] > 0.05]
    if not kabul: ar = "boş"
    elif np.isclose(min(kabul), izgara[0]) or np.isclose(max(kabul), izgara[-1]): ar = f"sınırsız ({min(kabul):.2f}…{max(kabul):.2f})"
    else: ar = f"[{min(kabul):.2f}, {max(kabul):.2f}]" + (" (parçalı)" if np.diff(kabul).max() > adim * 1.1 else "")
    o = kume_ols(Y, np.column_stack([X, W]), g)
    return dict(n=n, kume=G, pi=ilk.params[1], F=ilk.tvalues[1] ** 2, ind=ind.params[1], ind_p=ind.pvalues[1],
                beta=beta, se=se, p=2 * stats.t.sf(abs(beta / se), G - 1), AR=ar, ols=o.params[1], ols_p=o.pvalues[1])

ana = veri("kusample9and2ctry", "changemortctry")
satir = {"ANA: ülke düzeyi, ΔTFR 1950→1990": iv(ana)}
satir["D1a: pencere 1950→1980"] = iv(ana, y="dTFR_1950_1980")
satir["D1b: pencere 1950→2000"] = iv(ana, y="dTFR_1950_2000")
for ad, bayrak, arac in [("AJ orijinali", "kubasesample47", "changemortality"), ("ülke + kasaba", "kusample9and2ctryplustown", "changemortctryplustown"),
                         ("kasaba yerine", "kusample9and2ctryrepltown", "changemortctryrepltown"), ("en yüksek", "kusample9and2maxall", "changemortmaxall")]:
    satir[f"D2: {ad}"] = iv(veri(bayrak, arac))
satir["D3: sadece düşük/orta gelir"] = iv(ana[ana["startrich"] == 0])
satir["D4: + ln LE1940 kontrolü"] = iv(ana, kontrol=("lnLE40",))
saat = ana[(ana["guv"] == True) & ana["t0_saglik"].notna()]
satir["D5: saat tasarımı (t0 ~ t0_saglik)"] = iv(saat, y="t0", x="t0_saglik")
satir["D6: veri kontrolü, Δln toplam doğum 1940→80"] = iv(ana, y="changetotalbirths")

sonuc = pd.DataFrame(satir).T
pd.set_option("display.width", 250, "display.max_columns", 20)
print(sonuc.to_string(float_format=lambda v: f"{v:.3f}"))
b = satir["ANA: ülke düzeyi, ΔTFR 1950→1990"]["beta"]
print(f"\nÇeviri: yaşam beklentisi 1940→80 arasında ~%10 daha çok artınca (ΔlnLE +0,1), 1950→90 TFR değişimi {0.1 * b:+.2f} çocuk.")
print(f"Ana örneklem: {len(ana.dropna(subset=['dTFR_1950_1990', 'changelifeexpect']))} ülke, zengin {int(ana['startrich'].sum())}. "
      f"Medyan ΔTFR 1950→90: {ana['dTFR_1950_1990'].median():.2f}, medyan ΔlnLE: {ana['changelifeexpect'].median():.2f}")
sonuc.to_csv(KOK / "kesif/f_kreitmeir/sonuc.csv")
