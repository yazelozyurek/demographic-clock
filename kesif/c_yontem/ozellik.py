"""Keşif (sunuma girmez): t0 için aday özellikleri kurar. Bütün özellikler 1950-1970 arası ölçülür.
İki örneklem:
  S66  = clean/para_okul_tablosu.csv (dış veri + WPP özellikleri)
  S115 = clean/t0_tablosu.csv, guvenilir == True (sadece WPP özellikleri + ekvator)
Ekvator uzaklığı kodu pilot/ml_kontrol.py'den kopyalandı (orijinal değiştirilmedi)."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parents[2]


def ekvator_enlemi():
    topo = json.load(open(KOK / "arac/world-50m.json"))
    sk, tr = topo["transform"]["scale"], topo["transform"]["translate"]
    yaylar = []
    for yay in topo["arcs"]:
        x = y = 0; nok = []
        for dx, dy in yay:
            x += dx; y += dy; nok.append((x * sk[0] + tr[0], y * sk[1] + tr[1]))
        yaylar.append(np.array(nok))

    def halka(idx):
        r = np.vstack([yaylar[i] if i >= 0 else yaylar[~i][::-1] for i in idx])
        return np.vstack([r, r[:1]])

    def alan_ve_enlem(r):
        x, y = r[:, 0], r[:, 1]; c = x[:-1] * y[1:] - x[1:] * y[:-1]; A = c.sum() / 2
        return abs(A), (((y[:-1] + y[1:]) * c).sum() / (6 * A) if abs(A) > 1e-6 else y.mean())

    parca = {}
    for g in topo["objects"]["countries"]["geometries"]:
        if g.get("id") is None: continue
        pol = [g["arcs"]] if g["type"] == "Polygon" else g["arcs"] if g["type"] == "MultiPolygon" else []
        parca.setdefault(int(g["id"]), []).extend(alan_ve_enlem(halka(p[0])) for p in pol)
    return {k: sum(a * e for a, e in v) / sum(a for a, _ in v) for k, v in parca.items() if v}


WPP_SUT = ["LEx", "IMR", "Q5", "CDR", "PopDensity", "TPopulation1July", "CNMR", "SRB",
           "LExFemale", "LExMale", "LE65", "Q1550"]


def wpp_ozellik(locid):
    w = pd.read_csv(KOK / "clean/countries_1950_2100.csv", usecols=["LocID", "Time", *WPP_SUT])
    w = w[w.Time.between(1950, 1970)]
    y = {t: w[w.Time == t].set_index("LocID") for t in (1950, 1960, 1970)}
    f = pd.DataFrame(index=pd.Index(locid, name="LocID"))
    m = lambda t, c: f.index.map(y[t][c])
    f["lex_1950"] = m(1950, "LEx"); f["lex_1960"] = m(1960, "LEx")
    f["log_imr_1950"] = np.log(m(1950, "IMR")); f["log_imr_1960"] = np.log(m(1960, "IMR"))
    f["log_q5_1950"] = np.log(m(1950, "Q5"))
    f["cdr_1950"] = m(1950, "CDR")
    f["le65_1950"] = m(1950, "LE65")
    f["q1550_1950"] = m(1950, "Q1550")
    f["lex_fm_gap_1950"] = m(1950, "LExFemale") - m(1950, "LExMale")
    f["log_pop_1950"] = np.log(m(1950, "TPopulation1July"))
    f["log_dens_1950"] = np.log(m(1950, "PopDensity"))
    cn = w[w.Time.between(1950, 1959)].groupby("LocID")["CNMR"].mean()
    f["cnmr_1950s"] = f.index.map(cn)
    f["srb_1950"] = m(1950, "SRB")
    f["lex_gain_5070"] = m(1970, "LEx") - m(1950, "LEx")
    f["imr_decl_5070"] = np.log(m(1950, "IMR")) - np.log(m(1970, "IMR"))
    return f


def dis_ozellik(iso3):
    f = pd.DataFrame(index=pd.Index(iso3, name="ISO3_code"))
    g = pd.read_csv(KOK / "data_dis/gdp-per-capita-maddison-project-database.csv")
    def gdp(a, b):
        s = g[g.year.between(a, b)].sort_values("year").groupby("code")["gdp_per_capita"].first()
        return np.log(f.index.map(s).astype(float))
    f["log_gdp_1950"] = gdp(1950, 1955)
    f["log_gdp_1960"] = gdp(1960, 1960)
    f["gdp_growth_5070"] = gdp(1970, 1970) - f["log_gdp_1950"]
    bl = {k: pd.read_csv(KOK / f"data_dis/barrolee_BL_v3_{k}.csv") for k in ("F2534", "F2564", "MF2564")}
    def b(k, yil, sut):
        d = bl[k]; return f.index.map(d[d.year == yil].set_index("WBcode")[sut]).astype(float)
    f["sch_f2534_1950"] = b("F2534", 1950, "yr_sch")
    f["sch_f2534_1960"] = b("F2534", 1960, "yr_sch")
    f["sch_gain_f2534_5070"] = b("F2534", 1970, "yr_sch") - f["sch_f2534_1950"]
    f["nosch_f2534_1950"] = b("F2534", 1950, "lu")
    f["secplus_f2534_1950"] = b("F2534", 1950, "ls") + b("F2534", 1950, "lh")
    f["sch_f2564_1950"] = b("F2564", 1950, "yr_sch")
    f["sch_mf2564_1950"] = b("MF2564", 1950, "yr_sch")
    f["nosch_mf2564_1950"] = b("MF2564", 1950, "lu")
    f["gap_mf_minus_f_1950"] = f["sch_mf2564_1950"] - f["sch_f2564_1950"]
    f["ratio_f_to_mf_1950"] = (f["sch_f2564_1950"] + 0.1) / (f["sch_mf2564_1950"] + 0.1)
    return f


def bolge3(s):
    """Küçük bölgeleri birleştir (etkileşim testleri için)."""
    return s.replace({"Europe": "Other", "Oceania": "Other", "Northern America": "Other"})


def yukle():
    enl = ekvator_enlemi()
    t = pd.read_csv(KOK / "clean/t0_tablosu.csv")
    s115 = t[t.guvenilir].reset_index(drop=True)[["Location", "LocID", "ISO3_code", "bolge", "t0"]]
    s66 = pd.read_csv(KOK / "clean/para_okul_tablosu.csv")[["Location", "LocID", "ISO3_code", "bolge", "t0"]]
    out = {}
    for ad, d in (("S66", s66), ("S115", s115)):
        d = d.copy()
        d["equator_dist"] = d.LocID.map(enl).abs()
        d = d.join(wpp_ozellik(d.LocID).reset_index(drop=True))
        if ad == "S66":
            d = d.join(dis_ozellik(d.ISO3_code).reset_index(drop=True))
        d["bolge3"] = bolge3(d.bolge)
        out[ad] = d
    return out


OZ_WPP = ["equator_dist", "lex_1950", "lex_1960", "log_imr_1950", "log_imr_1960", "log_q5_1950", "cdr_1950",
          "le65_1950", "q1550_1950", "lex_fm_gap_1950", "log_pop_1950", "log_dens_1950", "cnmr_1950s",
          "srb_1950", "lex_gain_5070", "imr_decl_5070"]
OZ_DIS = ["log_gdp_1950", "log_gdp_1960", "gdp_growth_5070", "sch_f2534_1950", "sch_f2534_1960",
          "sch_gain_f2534_5070", "nosch_f2534_1950", "secplus_f2534_1950", "sch_f2564_1950", "sch_mf2564_1950",
          "nosch_mf2564_1950", "gap_mf_minus_f_1950", "ratio_f_to_mf_1950"]
OZELLIK = {"S66": OZ_WPP + OZ_DIS, "S115": OZ_WPP}
# 1970'e kadar ölçülen özellikler, t0'ı 1970'ten önce olan ülkelerde t0 SONRASINA düşer (sızıntı riski)
SONRA_OLCULEN = ["lex_1960", "log_imr_1960", "lex_gain_5070", "imr_decl_5070", "log_gdp_1960",
                 "gdp_growth_5070", "sch_f2534_1960", "sch_gain_f2534_5070"]

if __name__ == "__main__":
    d = yukle()
    for ad, x in d.items():
        print(ad, x.shape, x.t0.describe()[["min", "max"]].tolist())
        print(x[OZELLIK[ad]].isna().sum()[lambda s: s > 0])
