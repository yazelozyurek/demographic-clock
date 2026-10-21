"""Demografik Saat Gezgini: veri hazırlama (PROTOTİP, 14 Ekim 2026)

Çalıştırma (proje klasöründen):  python arac/veri_hazirla.py
Girdi : clean/countries_1950_2100.csv, data/..._OtherVariants_csv.gz, arac/world-50m.json
Çıktı : arac/gezgin_veri.json   (sayfa şablonu bu dosyayı gömer: arac/sayfa_olustur.py)

Adımlar
  1. K1: 2023 nüfusu >= 100 bin olan 200 ülke.
  2. Ortak eğri + zaman kayması modeli (SITAR benzeri, M1), sadece 1950-2023 verisiyle.
  3. t0 aralığı: model seçimi (M1/M2/M3) +/- 1,96 x blok bootstrap standart hatası (B=100).
  4. Demografik ikiz: standartlaştırma parametreleri ve eşleşme kalitesi eşikleri
     (ikiz araması tarayıcıda yapılır; adaylar sadece gözlenmiş yıllar, 1950-2023).
  5. UN tahmin aralıkları (80% / 95% PI): TFR ve nüfus, 2024-2100.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parent.parent
YIL0, YIL1, SON_TAHMIN = 1950, 2100, 2023
TAU_T = 60.0          # zaman kaymasının büzülme (shrinkage) ölçeği, yıl
B = 100               # bootstrap tekrar sayısı
BLOK = 8              # bootstrap blok uzunluğu, yıl
rng = np.random.default_rng(2026)

# ---------------------------------------------------------------- 1. veri
df = pd.read_csv(ROOT / "clean/countries_1950_2100.csv")
# K1 ile dışarıda kalan 37 yer: haritada gizlenmez, "analiz dışı" diye gösterilir
disarida = (df[df.pop2023 < 100].drop_duplicates("LocID")[["LocID", "Location", "pop2023"]]
            .rename(columns={"LocID": "id", "Location": "ad"}).round(1).to_dict("records"))
df = df[(df.pop2023 >= 100) & df.Time.between(YIL0, YIL1)].sort_values(["LocID", "Time"]).reset_index(drop=True)
ulkeler = df.drop_duplicates("LocID")[["LocID", "ISO3_code", "Location", "bolge", "pop2023"]].reset_index(drop=True)
n = len(ulkeler)
assert n == 200
yillar = np.arange(YIL0, YIL1 + 1)
assert len(df) == n * len(yillar)
genis = {v: df.pivot(index="LocID", columns="Time", values=v).loc[ulkeler.LocID].values
         for v in ["TFR", "LEx", "IMR", "MedianAgePop", "TPopulation1July"]}

# ---------------------------------------------------------------- 2. ortak eğri modeli (M1)
tahmin = df.Time <= SON_TAHMIN
t_obs = df.loc[tahmin, "Time"].values.astype(float)
c_obs = pd.factorize(df.loc[tahmin, "LocID"])[0]          # ulkeler ile aynı sıra (LocID'ye göre sıralı)
y_obs = df.loc[tahmin, "TFR"].values
m = len(y_obs)


def egri(t, U, L, k, t0):
    return L + (U - L) / (1 + np.exp(np.clip(k * (t - t0), -50, 50)))


TAU = {"dt": TAU_T, "dlk": 0.5, "dU": 1.0, "dL": 0.5}
BLOKLAR = {"M1": ["dt"], "M2": ["dt", "dlk"], "M3": ["dt", "dlk", "dU", "dL"]}


def fit(y, p0, model="M1"):
    """Ortak eğri + ülkeye özgü sapmalar. p = [U, L, log k, T0, blok_1 (n), blok_2 (n), ...]
    M1: sadece zaman kayması; M2: + hız; M3: + düzey. Sapmalar sıfıra doğru büzülür (TAU)."""
    bl = BLOKLAR[model]

    def acil(p):
        v = {b: p[4 + i * n: 4 + (i + 1) * n] for i, b in enumerate(bl)}
        z = np.zeros(n)
        return (p[0] + v.get("dU", z), p[1] + v.get("dL", z), np.exp(p[2] + v.get("dlk", z)), p[3] + v["dt"])

    def resid(p):
        Uu, Ll, kk, tt = acil(p)
        r = [egri(t_obs, Uu[c_obs], Ll[c_obs], kk[c_obs], tt[c_obs]) - y]
        r += [p[4 + i * n: 4 + (i + 1) * n] / TAU[b] for i, b in enumerate(bl)]
        return np.concatenate(r)
    S = lil_matrix((m + len(bl) * n, 4 + len(bl) * n), dtype=int)
    S[:m, :4] = 1
    for i in range(len(bl)):
        S[np.arange(m), 4 + i * n + c_obs] = 1
        S[m + i * n + np.arange(n), 4 + i * n + np.arange(n)] = 1
    p0 = np.r_[p0, np.zeros(4 + len(bl) * n - len(p0))]
    p = least_squares(resid, p0, jac_sparsity=S, method="trf", x_scale="jac", max_nfev=400).x
    return p, acil(p)


def baslangic_t0(seri, esik=4.3):
    """TFR'nin esik değerini ilk kez aşağı kestiği yıl (sadece başlangıç değeri için)."""
    alt = np.where(seri < esik)[0]
    if len(alt) == 0:
        return 2060.0
    return 1940.0 if alt[0] == 0 else float(yillar[alt[0]])


T0 = 1985.0
p0 = np.r_[7.0, 1.7, np.log(0.08), T0, [baslangic_t0(s) - T0 for s in genis["TFR"]]]
p_hat, (_, _, _, t0) = fit(y_obs, p0, "M1")
U, L, k = p_hat[0], p_hat[1], np.exp(p_hat[2])
yhat = egri(t_obs, U, L, k, t0[c_obs])
t0_m2 = fit(y_obs, p_hat, "M2")[1][3]
t0_m3 = fit(y_obs, p_hat, "M3")[1][3]


def r2(y, yh):
    return 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()


r2_takvim = r2(y_obs, df.loc[tahmin].groupby("Time").TFR.transform("mean").values)
r2_kayma = r2(y_obs, yhat)
r2_ulke = np.array([r2(y_obs[c_obs == i], yhat[c_obs == i]) for i in range(n)])
print(f"Ortak eğri: U={U:.2f} L={L:.2f} k={k:.3f} | R2 takvim={r2_takvim:.3f} kayma={r2_kayma:.3f}")

# ---------------------------------------------------------------- 3. blok bootstrap
artik = (y_obs - yhat).reshape(n, -1)            # ülke x yıl (74)
T = artik.shape[1]
boot = np.empty((B, n))
for b in range(B):
    bas = rng.integers(0, T - BLOK + 1, size=(n, int(np.ceil(T / BLOK))))
    idx = (bas[:, :, None] + np.arange(BLOK)).reshape(n, -1)[:, :T]
    y_b = yhat + np.take_along_axis(artik, idx, axis=1).ravel()
    boot[b] = fit(y_b, p_hat, "M1")[1][3]
    if b % 20 == 0:
        print("bootstrap", b)
# Not: Model yanlış belirlendiğinde (ör. Japonya'nın TFR'si ortak alt düzeyin altında) artık bootstrap'ı
# yanlı olabiliyor; yüzdelik aralık nokta tahminini dışarıda bırakabiliyor. Bu yüzden aralık =
# model seçimi aralığı (M1, M2, M3) +/- 1,96 x bootstrap standart hatası.
se = boot.std(axis=0, ddof=1)
modeller = np.stack([t0, t0_m2, t0_m3])
lo = modeller.min(0) - 1.96 * se
hi = modeller.max(0) + 1.96 * se

# ---------------------------------------------------------------- 4. demografik ikiz
X = np.stack([genis["TFR"], genis["LEx"], np.log(genis["IMR"]), genis["MedianAgePop"]], axis=-1)  # n x 151 x 4
gozlem = yillar <= SON_TAHMIN
mu = X[:, gozlem].reshape(-1, 4).mean(0)
sd = X[:, gozlem].reshape(-1, 4).std(0)
Z = (X - mu) / sd
aday = Z[:, gozlem].reshape(-1, 4)
aday_ulke = np.repeat(np.arange(n), gozlem.sum())
aday_yil = np.tile(yillar[gozlem], n)
agac = cKDTree(aday)
# eşleşme kalitesi eşikleri: gözlenen her ülke-yıl için başka ülkeden en yakın adayın uzaklığı
d_all, i_all = agac.query(Z[:, gozlem].reshape(-1, 4), k=80)
sorgu_ulke = np.repeat(np.arange(n), gozlem.sum())
ilk = np.array([d[aday_ulke[i] != u][0] for d, i, u in zip(d_all, i_all, sorgu_ulke)])
esik = {"cok_yakin": float(np.percentile(ilk, 50)), "yakin": float(np.percentile(ilk, 90))}
print("ikiz eşikleri:", esik)
# referans eşleşme dağılımı: gözlenen her ülke-yıl ve her BAŞKA ülke için o ülkedeki en iyi eşleşmenin uzaklığı.
# Tek bir referans ülkeyle yapılan karşılaştırmanın kalitesi bu dağılımdaki yüzdelik sırasıyla verilir.
Zo = Z[:, gozlem]
ref_d = []
for i in range(n):
    best = np.linalg.norm(Zo[i][:, None, None, :] - Zo[None, :, :, :], axis=-1).min(axis=2)   # 74 x n
    ref_d.append(np.delete(best, i, axis=1).ravel())
ref_d = np.concatenate(ref_d)
ref_q = np.percentile(ref_d, np.arange(101))
print("referans eşleşme yüzdelikleri (10, 30, 50):", ref_q[[10, 30, 50]].round(3))
# kontrol: Türkiye için Japonya'daki en yakın yıl
tr = int(np.where(ulkeler.Location == "Türkiye")[0][0]); jp = int(np.where(ulkeler.Location == "Japan")[0][0])
for yil in [1990, 2023, 2050]:
    dd = np.linalg.norm(Z[jp, gozlem] - Z[tr, yil - YIL0], axis=1)
    print(f"Türkiye {yil} ~ Japonya {yillar[gozlem][dd.argmin()]} (d={dd.min():.2f})")

# ---------------------------------------------------------------- 5. UN tahmin aralıkları
ov = pd.read_csv(ROOT / "data/WPP2024_Demographic_Indicators_OtherVariants_csv.gz",
                 usecols=["LocID", "Variant", "Time", "TFR", "TPopulation1July"], encoding="utf-8-sig")
ov = ov[ov.Variant.str.contains("PI") & ov.LocID.isin(ulkeler.LocID) & ov.Time.between(2024, YIL1)]
ad = {"Lower 95 PI": "l95", "Lower 80 PI": "l80", "Median PI": "med", "Upper 80 PI": "u80", "Upper 95 PI": "u95"}
pi = {}
for v, kisa in ad.items():
    g = ov[ov.Variant == v]
    for col, isim, nd in [("TFR", "tfr", 3), ("TPopulation1July", "pop", 1)]:
        w = g.pivot(index="LocID", columns="Time", values=col).reindex(index=ulkeler.LocID, columns=range(2024, YIL1 + 1))
        assert w.notna().all().all(), (v, col)
        pi.setdefault(isim, {})[kisa] = np.round(w.values, nd).tolist()

# ---------------------------------------------------------------- çıktı
def yuvarla(a, nd):
    return np.round(a, nd).tolist()


cikti = {
    "meta": {
        "olusturma": "2026-10-14", "kaynak": "UN World Population Prospects 2024",
        "yillar": [YIL0, YIL1], "son_tahmin": SON_TAHMIN,
        "egri": {"U": round(U, 4), "L": round(L, 4), "k": round(k, 5)},
        "r2": {"takvim": round(r2_takvim, 4), "kayma": round(r2_kayma, 4)},
        "ikiz_esik": esik, "ikiz_q": ref_q.round(4).tolist(), "ikiz_mu": mu.round(5).tolist(), "ikiz_sd": sd.round(5).tolist(),
        "bootstrap": {"B": B, "blok": BLOK},
    },
    "ulkeler": [
        {"id": int(r.LocID), "iso3": r.ISO3_code, "ad": r.Location, "bolge": r.bolge, "pop2023": round(float(r.pop2023), 1),
         "t0": round(float(t0[i]), 2), "se": round(float(se[i]), 2), "lo": round(float(lo[i]), 2), "hi": round(float(hi[i]), 2), "r2": round(float(r2_ulke[i]), 3)}
        for i, r in ulkeler.iterrows()
    ],
    "seri": {"tfr": yuvarla(genis["TFR"], 3), "lex": yuvarla(genis["LEx"], 2), "imr": yuvarla(genis["IMR"], 2),
             "yas": yuvarla(genis["MedianAgePop"], 2), "pop": yuvarla(genis["TPopulation1July"], 1)},
    "pi": pi,
    "disarida": disarida,
}
(ROOT / "arac/gezgin_veri.json").write_text(json.dumps(cikti, ensure_ascii=False, separators=(",", ":")))
print("yazıldı:", ROOT / "arac/gezgin_veri.json")
print(ulkeler.assign(t0=t0, m2=t0_m2, m3=t0_m3, se=se, lo=lo, hi=hi).set_index("Location").loc[
    ["Türkiye", "Japan", "Nigeria", "Niger", "Republic of Korea", "India", "France"], ["t0", "m2", "m3", "se", "lo", "hi"]].round(1))
print("aralık genişliği (yıl), medyan:", np.median(hi - lo).round(1), "| >25 yıl olan ülke:", int((hi - lo > 25).sum()))
