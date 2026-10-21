"""SONRADAN tanı kontrolleri (ön kayıtta YOK, kanıt sayılmaz): ana sonucun başlangıç TFR'sine ve tek ülkelere duyarlılığı.
Çalıştırma: python kesif/f_kreitmeir/sonradan_kontrol.py"""
import importlib.util, sys
from pathlib import Path
import numpy as np
KOK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ku", KOK / "ku_testi.py"); ku = importlib.util.module_from_spec(spec)
sys.stdout = open("/dev/null", "w"); spec.loader.exec_module(ku); sys.stdout = sys.__stdout__
ana = ku.ana.copy()
ana["tfr50"] = ku.w["TFR"][1950].reindex(ana.index)
r = ku.iv(ana, kontrol=("tfr50",))
print(f"S1: + TFR1950 kontrolü        n {r['n']} · F {r['F']:.1f} · β {r['beta']:+.2f} (p {r['p']:.3f}) · AR {r['AR']}")
d = ana.dropna(subset=["dTFR_1950_1990", "changelifeexpect"])
loo = {i: ku.iv(d.drop(i))["beta"] for i in d.index}
lo, hi = min(loo, key=loo.get), max(loo, key=loo.get)
print(f"S2: bir ülke dışarıda β        {loo[lo]:+.2f} ({lo} çıkınca) … {loo[hi]:+.2f} ({hi} çıkınca)")
print(f"S3: başlangıç ölçüleri arası Spearman: araç~lnLE40 {d[['z','lnLE40']].corr('spearman').iloc[0,1]:+.2f}, araç~TFR1950 {d[['z','tfr50']].corr('spearman').iloc[0,1]:+.2f}")
