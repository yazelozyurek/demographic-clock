"""Bütün test kayıtlarını birleştirir, Benjamini–Hochberg FDR (bütün testler tek aile) uygular,
sıfır kalibrasyonu özetini yazar. Çalıştırma: python kesif/c_yontem/birlestir.py → test_log_hepsi.csv, ozet.txt"""
from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

B = Path(__file__).parent
log = pd.concat([pd.read_csv(B / f) for f in ("test_log_tek.csv", "test_log_cok.csv", "test_log_ek.csv")], ignore_index=True)
ok = log.p.notna()
log.loc[ok, "q_BH"] = multipletests(log.loc[ok, "p"], method="fdr_bh")[1]
log.to_csv(B / "test_log_hepsi.csv", index=False)

out = [f"Toplam test: {ok.sum()} (p-değerli), kayıt: {len(log)}",
       f"q<0.05: {(log.q_BH < 0.05).sum()}, q<0.01: {(log.q_BH < 0.01).sum()}"]
for fam, g in log[ok].groupby("family"):
    out.append(f"  {fam}: {len(g)} test, q<0.05: {(g.q_BH < 0.05).sum()}")

nt, nc = pd.read_csv(B / "null_tek.csv"), pd.read_csv(B / "null_cok.csv")
uni = log[log.family == "univariate"]
out.append("\n== Tek değişkenli tarama: gerçek en iyi |istatistik| vs permütasyon sıfırı ==")
for s in ("S66", "S115"):
    x, nn = uni[uni["sample"] == s], nt[nt["sample"] == s]
    out.append(f"-- {s} ({len(nn)} permütasyon)")
    for c in [c for c in nn.columns if c.startswith("max_abs_") and nn[c].notna().any()]:
        m = c[8:]; xm = x[x.method == m]
        i = xm.statistic.abs().idxmax()
        out.append(f"  {m:32s} gerçek {abs(xm.statistic[i]):.3f} ({xm.feature[i]})  null p95 {nn[c].quantile(.95):.3f}  "
                   f"null maks {nn[c].max():.3f}  P(null>=gerçek) {(nn[c] >= abs(xm.statistic[i])).mean():.3f}")
    out.append(f"  en küçük analitik p: gerçek {x.p.min():.2e}, null 5. yüzdelik {nn.min_p_analytic.quantile(.05):.2e}")

loo = pd.read_csv(B / "loo_sonuc.csv")
out.append("\n== LOO tahmin (medyan |hata|, yıl) ==\n" + loo.round(3).to_string(index=False))
out.append("\n== Çok değişkenli sıfır: en iyi modelin LOO medyan |hatası| (t0 karıştırılmış) ==")
for s, g in nc.groupby("sample"):
    real = loo[(loo["sample"] == s) & (loo.featureset == "pre_t0_only")].median_abs_err.min()
    out.append(f"  {s}: gerçek en iyi {real:.2f}; null 5. yüzdelik {g.best_model_mae.quantile(.05):.2f}, "
               f"null medyan {g.best_model_mae.median():.2f}, P(null<=gerçek) {(g.best_model_mae <= real).mean():.3f} (n_perm={len(g)})")
kr = pd.read_csv(B / "kararlilik.csv")
out.append("\n== LASSO kararlılık seçimi (500 bootstrap), ilk 8 ==")
for s, g in kr.groupby("sample"):
    out.append(f"-- {s}\n" + g.head(8).round(3).to_string(index=False))
open(B / "ozet.txt", "w").write("\n".join(out))
print("\n".join(out))
