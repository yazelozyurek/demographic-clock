# Kapak görseli: 200 ülkenin TFR "manzarası" (1950–2100), dönüm yılına göre sıralı.
# Proje klasöründen çalıştır:  python pilot/kapak.py
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d.art3d import Line3DCollection

BG = "#16232F"
d = pd.read_csv("clean/countries_1950_2100.csv", usecols=["LocID", "Time", "TFR", "pop2023"])
d = d[d.pop2023 >= 100]
t0 = pd.read_csv("clean/t0_tablosu.csv").set_index("LocID")["t0"]
Y = d.pivot(index="LocID", columns="Time", values="TFR")
Y = Y.loc[t0.loc[Y.index].sort_values().index]          # erken dönenler önde
yil = Y.columns.values.astype(float)

renk = LinearSegmentedColormap.from_list("tfr", ["#2fb7ff", "#7a6cff", "#ff4f7a", "#ff6a2b"])
fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=BG)
ax = fig.add_axes([0.30, -0.20, 0.72, 1.12], projection="3d", facecolor=BG)
ax.set_axis_off()

for i, (_, satir) in enumerate(Y.iterrows()):
    z = satir.values
    x = yil
    y = np.full_like(x, i)
    p = np.column_stack([x, y, z])
    seg = np.stack([p[:-1], p[1:]], axis=1)
    c = renk(np.clip((z[:-1] - 1) / 6, 0, 1))
    c[:, 3] = np.where(x[:-1] <= 2023, 0.95, 0.35)        # 2024 sonrası projeksiyon: soluk
    for lw, a in [(5, 0.06), (2.6, 0.15)]:                 # parıltı
        cg = c.copy(); cg[:, 3] *= a / 0.95
        ax.add_collection3d(Line3DCollection(seg, colors=cg, linewidths=lw))
    ax.add_collection3d(Line3DCollection(seg, colors=c, linewidths=0.9))

# yenilenme düzeyi cephesi: her ülkenin TFR'si 2,1'in altına ilk indiği yıl
cephe = []
for i, (_, satir) in enumerate(Y.iterrows()):
    alt = satir[satir < 2.1]
    if len(alt):
        cephe.append((alt.index[0], i, 2.1))
cephe = np.array(cephe, dtype=float)
cephe[:, 0] = pd.Series(cephe[:, 0]).rolling(15, center=True, min_periods=1).median().rolling(9, center=True, min_periods=1).mean()
for lw, a in [(7, 0.10), (3.5, 0.25), (1.4, 0.95)]:
    ax.plot(cephe[:, 0], cephe[:, 1], cephe[:, 2], color="#FFF4E0", alpha=a, lw=lw)

# zemin ızgarası
for gx in np.arange(1950, 2101, 10):
    ax.plot([gx, gx], [0, len(Y)], [0, 0], color="#2fb7ff", alpha=0.18, lw=0.8)
for gy in np.arange(0, len(Y) + 1, 20):
    ax.plot([1950, 2100], [gy, gy], [0, 0], color="#2fb7ff", alpha=0.18, lw=0.8)
# 2023 çizgisi: tahmin | projeksiyon
ax.plot([2023.5, 2023.5], [0, len(Y)], [0, 0], color="#EEF2F4", alpha=0.7, lw=1.4)

ax.set_xlim(1950, 2100); ax.set_ylim(0, len(Y)); ax.set_zlim(0, 8.5)
ax.set_box_aspect((2.2, 1.6, 0.75))
ax.view_init(elev=28, azim=-58)
fig.savefig("outputs/final_0_cover.png", facecolor=BG)
print("Kaydedildi: outputs/final_0_cover.png")
