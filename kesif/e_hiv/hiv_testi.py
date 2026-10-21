"""Ön kayıtlı "ters şok" testi (plan: kesif/e_hiv/plan.md, commit bbedcc9).
HIV yüksek (en yüksek yaygınlık ≥ %10) ve düşük (< %3) Sahra altı ülkelerinde 1990→2005 doğurganlığın ortak yoldan sapması.
Çalıştırma (proje klasöründen):  python kesif/e_hiv/hiv_testi.py
Çıktı: ekrana tablo + kesif/e_hiv/sonuc_ulkeler.csv"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import spearmanr

KOK = Path(__file__).resolve().parent.parent.parent
rng = np.random.default_rng(2026)
p = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["LocID", "ISO3_code", "Location", "altbolge", "pop2023", "Time", "TFR", "LEx", "Q5"])
t0 = pd.read_csv(KOK / "clean/t0_tablosu.csv").set_index("LocID")["t0"]

# 1) ortak eğri: ana modelin kaymalarıyla 1950–2023 verisine tek curve_fit
def egri(z, L, U, k):
    return L + (U - L) / (1 + np.exp(k * z))
g = p[(p["Time"] <= 2023) & p["LocID"].isin(t0.index)]
(L, U, k), _ = curve_fit(egri, g["Time"] - g["LocID"].map(t0), g["TFR"], p0=[1.7, 7, 0.08])
print(f"ortak eğri: U = {U:.3f}, L = {L:.3f}, k = {k:.4f}")

def sapma(tfr0, yil, sabitle=False):
    """1990 TFR'sine göre eğriye yerleştir, `yil` yıl ilerlet, beklenen TFR'yi döndür."""
    if sabitle: tfr0 = min(tfr0, U - 0.05)
    if not (L < tfr0 < U): return np.nan
    z = np.log((U - L) / (tfr0 - L) - 1) / k
    return egri(z + yil, L, U, k)

# 2) gruplar
hiv = pd.read_csv(KOK / "data_dis/hiv_wb/hiv_prevalence_15_49.csv").groupby("iso3")["hiv"].max()
SSA = ["Eastern Africa", "Western Africa", "Middle Africa", "Southern Africa"]
w = p[p["altbolge"].isin(SSA) & (p["pop2023"] >= 100)].pivot_table(index=["ISO3_code", "Location"], columns="Time", values=["TFR", "LEx", "Q5"])
u = pd.DataFrame({"tfr90": w["TFR"][1990], "tfr95": w["TFR"][1995], "tfr05": w["TFR"][2005], "tfr10": w["TFR"][2010],
                  "tfr80": w["TFR"][1980], "dLEx": w["LEx"][2005] - w["LEx"][1990], "dQ5": w["Q5"][2005] - w["Q5"][1990]}).reset_index()
u["hiv_tepe"] = u["ISO3_code"].map(hiv)
print(f"Sahra altı ülke: {len(u)}, HIV verisi olmayan: {u['hiv_tepe'].isna().sum()} ({', '.join(u.loc[u['hiv_tepe'].isna(), 'Location'])})")
u["grup"] = np.select([u["hiv_tepe"] >= 10, u["hiv_tepe"] < 3], ["yuksek", "dusuk"], "ara")
u.loc[u["hiv_tepe"].isna(), "grup"] = "veri_yok"
u["D05"] = u["tfr05"] - [sapma(a, 15) for a in u["tfr90"]]
u["D10"] = u["tfr10"] - [sapma(a, 20) for a in u["tfr90"]]
u["D05_sabit"] = u["tfr05"] - [sapma(a, 15, True) for a in u["tfr90"]]
u["egim_farki"] = (u["tfr10"] - u["tfr95"]) / 15 - (u["tfr90"] - u["tfr80"]) / 10      # fark içinde fark (yıllık)
u.to_csv(KOK / "kesif/e_hiv/sonuc_ulkeler.csv", index=False)

def test(df, col, ad):
    x = df[df["grup"].isin(["yuksek", "dusuk"])].dropna(subset=[col])
    y = x[col].values; t = (x["grup"] == "yuksek").values
    fark = np.median(y[t]) - np.median(y[~t])
    perm = np.array([np.median(y[s]) - np.median(y[~s]) for s in (rng.permutation(t) for _ in range(10000))])
    pval = (np.abs(perm) >= abs(fark)).mean()
    print(f"{ad:<46} n = {t.sum()} yüksek / {(~t).sum()} düşük · medyan {np.median(y[t]):+.2f} vs {np.median(y[~t]):+.2f} · fark {fark:+.2f} · p = {pval:.4f}")
    return fark, pval

print("\nÖn koşul (sağlık şoku oldu mu?), 1990→2005 medyan:")
print(u[u["grup"].isin(["yuksek", "dusuk"])].groupby("grup")[["dLEx", "dQ5"]].median().round(1))
print("\nANA TEST")
ana = u[u["tfr90"] <= 6.5]
test(ana, "D05", "ANA: sapma 2005, TFR1990 ≤ 6,5")
print("\nDuyarlılık")
r = spearmanr(ana["hiv_tepe"], ana["D05"], nan_policy="omit")
print(f"{'D1: doz, Spearman(HIV tepe, D05)':<46} n = {ana[['hiv_tepe','D05']].dropna().shape[0]} · ρ = {r[0]:+.2f} · p = {r[1]:.4f}")
test(ana, "D10", "D2: pencere 1990→2010")
test(u, "D05_sabit", "D3: TFR1990 > 6,5 dahil (sabitlenmiş)")
test(u, "egim_farki", "D4: eğim farkı (1995–2010 − 1980–1990)")
print("\nYüksek HIV ülkeleri:")
print(ana[ana["grup"] == "yuksek"][["Location", "hiv_tepe", "tfr90", "tfr05", "D05", "dLEx", "dQ5"]].round(2).to_string(index=False))
print("\nDüşük HIV ülkeleri:")
print(ana[ana["grup"] == "dusuk"][["Location", "hiv_tepe", "tfr90", "tfr05", "D05", "dLEx", "dQ5"]].round(2).to_string(index=False))
