"""SONRADAN tanı 2 (ön kayıtta YOK, kanıt sayılmaz): 'başlangıç sağlığı sabitken araç zayıflıyor' bulgusunu netleştirmek.
Sorular (sonuçtan önce listelendi, 24 Ekim 2026):
 a) Aracın ne kadarı 1940 sağlığından ibaret? (z ~ lnLE40 R²; + TFR1950)
 b) lnLE40 sabitken etki KAYBOLUYOR mu, yoksa sadece BULANIKLAŞIYOR mu? (1. aşama, indirgenmiş form, β; kontrolsüzle yan yana)
 c) Aynısı TFR1950 sabitken.
 d) Duyarlılık (Conley, Hansen & Rossi 2012 tarzı): araç doğurganlığı sağlık dışından γ kadar doğrudan etkiliyorsa sonuç hangi γ'da bozulur?
    γ*, indirgenmiş formun yüzdesi olarak; başlangıç koşullarının bağın ne kadarını 'açıkladığı' ile karşılaştırılır.
 e) Oransal sonuç ΔlnTFR (mutlak 'düşecek yer' itirazına karşı tanı).
Çalıştırma: python kesif/f_kreitmeir/sonradan_kontrol2.py"""
import importlib.util, sys
from pathlib import Path
import numpy as np
import statsmodels.api as sm
KOK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ku", KOK / "ku_testi.py"); ku = importlib.util.module_from_spec(spec)
sys.stdout = open("/dev/null", "w"); spec.loader.exec_module(ku); sys.stdout = sys.__stdout__
ana = ku.ana.copy()
ana["tfr50"] = ku.w["TFR"][1950].reindex(ana.index)
ana["dlnTFR"] = np.log(ku.w["TFR"][1990].reindex(ana.index)) - np.log(ana["tfr50"])
d = ana.dropna(subset=["dTFR_1950_1990", "changelifeexpect", "z", "lnLE40", "tfr50"]).copy()
Y, X, Z, g = d["dTFR_1950_1990"].values, d["changelifeexpect"].values, d["z"].values, d["ctrycluster"].values
print(f"n {len(d)} ülke, {len(np.unique(g))} küme")

def W(k):
    return d[list(k)].values if k else np.empty((len(d), 0))

# a) aracın ne kadarı başlangıç koşulu?
for ad, k in [("lnLE40", ["lnLE40"]), ("TFR1950", ["tfr50"]), ("lnLE40 + TFR1950", ["lnLE40", "tfr50"])]:
    print(f"a) araç ~ {ad:<17} R² = {sm.OLS(Z, sm.add_constant(d[k])).fit().rsquared:.2f}")

# b, c) kayboluyor mu, bulanıklaşıyor mu?
print("\nb/c) kontrol            | 1. aşama π [%95]            F    | indirgenmiş form ρ [%95]     p     | β (2SLS)  AR %95")
rf = {}
for ad, k in [("yok", ()), ("lnLE40", ("lnLE40",)), ("TFR1950", ("tfr50",)), ("ikisi", ("lnLE40", "tfr50"))]:
    f1 = ku.kume_ols(X, np.column_stack([Z, W(k)]), g); r1 = ku.kume_ols(Y, np.column_stack([Z, W(k)]), g); iv = ku.iv(d, kontrol=k)
    rf[ad] = r1.params[1]
    c1, c2 = f1.conf_int()[1], r1.conf_int()[1]
    print(f"     {ad:<17} | {f1.params[1]:+.3f} [{c1[0]:+.3f}; {c1[1]:+.3f}]  {f1.tvalues[1] ** 2:5.1f} | "
          f"{r1.params[1]:+.3f} [{c2[0]:+.3f}; {c2[1]:+.3f}]  {r1.pvalues[1]:.3f} | {iv['beta']:+.2f}    {iv['AR']}")

# d) duyarlılık: indirgenmiş formun yüzde kaçı sağlık dışı olursa AR aralığı 0'ı içerir?
def p_rf(gam):
    return ku.kume_ols(Y - gam * Z, Z[:, None], g).pvalues[1]
lo, hi = 0.0, rf["yok"]
for _ in range(60):
    m = (lo + hi) / 2
    lo, hi = (m, hi) if p_rf(m) < 0.05 else (lo, m)
pay = lo / rf["yok"]
print(f"\nd) kırılma noktası: indirgenmiş formun %{100 * pay:.0f}'i sağlık dışı bir yoldan geliyorsa AR %95 aralığı 0'ı içerir "
      f"(γ* = {lo:+.3f}, ρ = {rf['yok']:+.3f})")
for ad in ["lnLE40", "TFR1950", "ikisi"]:
    print(f"   {ad:<8} sabitken indirgenmiş form %{100 * (1 - rf[ad] / rf['yok']):.0f} küçülüyor "
          f"(bağın bu kadarı başlangıç koşuluyla 'açıklanıyor'; sağlık dışı yolun üst sınırı)")

# e) oransal sonuç
e = ku.iv(d, y="dlnTFR")
print(f"\ne) ΔlnTFR 1950→1990: F {e['F']:.1f} · β {e['beta']:+.3f} (p {e['p']:.3f}) · AR {e['AR']} · "
      f"çeviri: yaşam beklentisi %10 daha çok artınca TFR %{100 * (np.exp(0.1 * e['beta']) - 1):+.1f} değişir")
ek = ku.iv(d, y="dlnTFR", kontrol=("lnLE40",))
print(f"   + lnLE40: F {ek['F']:.1f} · β {ek['beta']:+.3f} · AR {ek['AR']}")
