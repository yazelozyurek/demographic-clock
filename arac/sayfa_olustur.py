"""Demografik Saat Gezgini: tek dosyalık HTML sayfasını oluşturur (PROTOTİP).

Çalıştırma (proje klasöründen):  python arac/sayfa_olustur.py
Girdi : arac/gezgin_sablon.html, arac/gezgin_veri.json, arac/world-50m.json
Çıktı : arac/gezgin.html
Harita: Natural Earth 1:50m (world-atlas 2.0.2). Özellik kimlikleri ISO 3166-1 sayısal kodları = UN LocID.
"""
import json
from pathlib import Path

import numpy as np

A = Path(__file__).resolve().parent
veri = json.loads((A / "gezgin_veri.json").read_text())
topo = json.loads((A / "world-50m.json").read_text())
geoms = topo["objects"]["countries"]["geometries"]

# 1) Antarktika'yı çıkar
geoms[:] = [g for g in geoms if g.get("id") != "010"]

# 2) Kimliği olmayan özellikler: UN'in ülke kapsamına göre kimlik ver
#    (UN WPP Kosova'yı ayrı, Somaliland'ı Somali'nin, Kuzey Kıbrıs'ı Kıbrıs'ın parçası olarak verir)
ata = {"Kosovo": "412", "Somaliland": "706", "N. Cyprus": "196"}
for g in geoms:
    if g.get("id") in (None, ""):
        ad = g.get("properties", {}).get("name")
        print("kimliksiz özellik:", ad, "->", ata.get(ad, "veri yok"))
        if ad in ata:
            g["id"] = ata[ad]

# 3) Fransa'nın denizaşırı bölgelerini ayrı çiz (WPP'de ayrı yerler)
tr_ = topo["transform"]
arcs = []
for a in topo["arcs"]:
    q = np.cumsum(np.array(a, dtype=float), axis=0)
    arcs.append(q * tr_["scale"] + tr_["translate"])


def halka_merkez(halka):
    pts = np.vstack([arcs[i] if i >= 0 else arcs[~i][::-1] for i in halka])
    return pts.mean(0)


hedef = {"254": (-53.2, 4.0), "312": (-61.5, 16.2), "474": (-61.0, 14.6), "638": (55.5, -21.1), "175": (45.1, -12.8)}
fra = next(g for g in geoms if g.get("id") == "250")
assert fra["type"] == "MultiPolygon"
kalan, yeni = [], {}
for poly in fra["arcs"]:
    lon, lat = halka_merkez(poly[0])
    en = min(hedef, key=lambda k: (hedef[k][0] - lon) ** 2 + (hedef[k][1] - lat) ** 2)
    if (hedef[en][0] - lon) ** 2 + (hedef[en][1] - lat) ** 2 < 3.0 ** 2:
        yeni.setdefault(en, []).append(poly)
    else:
        kalan.append(poly)
fra["arcs"] = kalan
for k, polys in yeni.items():
    geoms.append({"type": "MultiPolygon", "id": k, "arcs": polys, "properties": {}})
print("Fransa'dan ayrılan:", sorted(yeni))

ids = {int(g["id"]) for g in geoms if g.get("id")}
eksik = [u["ad"] for u in veri["ulkeler"] if u["id"] not in ids]
print("haritada olmayan:", eksik)
veri["meta"]["haritada_yok"] = eksik


def gom(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


html = (A / "gezgin_sablon.html").read_text()
html = html.replace("__VERI__", gom(veri)).replace("__DUNYA__", gom(topo))
(A / "gezgin.html").write_text(html)
print("yazıldı:", A / "gezgin.html", f"{len(html) / 1e6:.2f} MB")
