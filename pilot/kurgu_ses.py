"""Video kurgusunun ses kısmı (29 Ekim): kurgu planındaki bölümleri kayıtlardan keser, her kaydın sesini aynı düzeye getirir,
tepeleri sınırlar, birleşim yerlerine kısa geçiş koyar ve tek bir WAV yazar.

Kullanım (proje klasöründen):  python pilot/kurgu_ses.py sunum/video/kurgu_plani_30ekim.json <cikti.wav>
- Ses macOS'un afconvert aracıyla okunur (48 kHz, 2 kanal); kurulum gerekmez.
- Düzey: her kaydın konuşma anlarındaki (10 ms parçalar) ortanca düzeyi HEDEF_DB'ye çekilir (en fazla +24 dB);
  sınırlayıcı ortancayı biraz düşürdüğü için kazanç bir kez daha ölçülüp düzeltilir.
- Sınırlayıcı: 10 ms'lik tepe zarfı ESIK'i geçerse kazanç yumuşakça düşürülür; ses kesilmez, patlama olmaz.
- Plan alanları (30 Ekim): "sessiz": n → n saniye sessizlik (görüntü kısmı goruntu_bas'tan alınır); "sustur": [[a, b], …] →
  kaynak kayıtta a–b arası sıfırlanır (sayfa çevirirken tuş sesi).
Görüntü kısmı: swift pilot/kurgu_video.swift (aynı planı okur, bu WAV'ı ses olarak koyar).
"""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np
from scipy.ndimage import maximum_filter1d, minimum_filter1d, uniform_filter1d

SR = 48000
HEDEF_DB, EN_FAZLA_KAZANC = -24.0, 24.0
ESIK = 0.7          # sınırlayıcı eşiği (yaklaşık -3 dBFS)
GECIS = 0.010       # birleşim yerlerinde açılış/kapanış (sn)


def oku(yol):
    gecici = Path(tempfile.mkdtemp()) / "ses.wav"
    subprocess.run(["afconvert", "-f", "WAVE", "-d", f"LEI16@{SR}", "-c", "2", str(yol), str(gecici)], check=True)
    with wave.open(str(gecici)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32).reshape(-1, 2) / 32768
    gecici.unlink()
    gecici.parent.rmdir()
    return x


def konusma_duzeyi(x):
    k = len(x) // 480
    db = 20 * np.log10(np.sqrt((x[:k * 480].mean(1).reshape(k, 480) ** 2).mean(1)) + 1e-9)
    esik = max(np.percentile(db, 10) + 12, -60)
    return float(np.median(db[db > esik]))


def sinirla(x):
    tepe = maximum_filter1d(np.abs(x).max(1), size=480)
    g = np.minimum(1.0, ESIK / (tepe + 1e-9))
    g = uniform_filter1d(minimum_filter1d(g, size=480), size=480)
    return np.clip(x * g[:, None], -0.99, 0.99)


def gecis(x):
    n = min(int(GECIS * SR), len(x) // 2)
    r = np.linspace(0, 1, n, dtype=np.float32)[:, None]
    x = x.copy()
    x[:n] *= r
    x[-n:] *= r[::-1]
    return x


plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
cikti = Path(sys.argv[2])
hepsi = []
for p in plan["parcalar"]:
    x = oku(Path(p["kaynak"]).expanduser())
    for a, z in p.get("sustur", []):   # tuş sesi: sessizlikteki aralık sıfırlanır (kenarlarda 20 ms geçiş)
        i, j = int(a * SR), int(z * SR)
        n = int(0.02 * SR)
        x[i:j] *= np.r_[np.linspace(1, 0, n), np.zeros(j - i - 2 * n), np.linspace(0, 1, n)].astype(np.float32)[:, None]
    for a, z, kaz in p.get("yukselt", []):   # alçak söylenmiş kelime: a–b arası kaz dB yükseltilir (kenarlarda 20 ms geçiş)
        i, j = int(a * SR), int(z * SR)
        n = int(0.02 * SR)
        g = np.full(j - i, 10 ** (kaz / 20), np.float32)
        g[:n] = np.linspace(1, g[0], n)
        g[-n:] = np.linspace(g[0], 1, n)
        x[i:j] *= g[:, None]
    bolumler = [np.zeros((int(round(b["sessiz"] * SR)), 2), np.float32) if "sessiz" in b
                else x[int(b["bas"] * SR): int(b["son"] * SR)] for b in p["bolumler"]]
    for b, y in zip(p["bolumler"], bolumler):
        if "sessiz" not in b:
            assert abs(len(y) / SR - (b["son"] - b["bas"])) < 0.01, f"{p['ad']}: bölüm kaydın dışında ({b})"
    once = konusma_duzeyi(np.concatenate(bolumler))
    kazanc = min(HEDEF_DB - once, EN_FAZLA_KAZANC)
    for _ in range(2):
        islenmis = [gecis(sinirla(y * 10 ** (kazanc / 20))) for y in bolumler]
        sonra = konusma_duzeyi(np.concatenate(islenmis))
        kazanc = min(kazanc + HEDEF_DB - sonra, EN_FAZLA_KAZANC)
    bolumler = islenmis
    sure = sum(len(y) for y in bolumler) / SR
    print(f"{p['ad']}: {sure:.1f} sn · konuşma {once:.1f} → {sonra:.1f} dBFS (kazanç {kazanc:+.1f} dB)")
    hepsi += bolumler
tum = np.concatenate(hepsi)
with wave.open(str(cikti), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((tum * 32767).astype(np.int16).tobytes())
print(f"yazıldı: {cikti} · {int(len(tum) / SR // 60)}:{len(tum) / SR % 60:04.1f}")
