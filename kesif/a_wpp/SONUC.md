# Keşif A — WPP içi özellikler ve t0 (sunuma girmeyecek)

Çalıştırma: `python kesif/a_wpp/kesif_wpp.py` (proje kökünden, yaklaşık 15 sn).
Dosyalar: `test_log.csv` (316 test, BH q), `null_calibration.csv`, `loo_top3.csv`, `lag_descriptive.csv`.

## Ne yapıldı
- 61 özellik (+24 "LEAK" işaretli TFR ailesi, +6 "yalnızca t0'dan önce" alt örneği), 2 örneklem (güvenilir 115 / tümü 200), 2 yöntem (Spearman; bölge içi sıra Spearman). Toplam **316 test**, Benjamini–Hochberg; 266'sı q < 0,05.
- Ölüm zamanlaması: eşik geçiş yılları (LEx 45–70, IMR 200–30, Q5, CDR, LE15) ve t0 ile **aynı yöntemle** (ortak lojistik + ülke başına zaman kayması, sadece 1950–2023) LEx ve log IMR orta nokta yılları.
- Null kalibrasyon: güvenilir örneklemde t0 300 kez karıştırıldı, 61 özellik × 2 yöntem üzerinden max |ρ|.

## Ana sonuçlar (güvenilir 115)
| Özellik | n | ρ | bölge içi ρ | q | LOO medyan |hata| model / medyan / bölge medyanı |
|---|---|---|---|---|---|
| LEx orta nokta yılı (ortak eğri) | 115 | 0,77 | 0,71 | <1e-10 | 6,2 / 12,0 / 10,5 yıl |
| CDR ≤ 10 yılı | 114 | 0,73 | 0,69 | <1e-10 | 7,5 / 11,8 / 10,0 |
| LEx ≥ 60 yılı | 113 | 0,73 | 0,67 | <1e-10 | 7,4 / 11,8 / 9,5 |
| LEx 1960 düzeyi (sabit tarih) | 115 | −0,72 | −0,65 | <1e-10 | 6,8 / 12,0 / 10,5 |
| (karşılaştırma) TFR 1960 — LEAK | 115 | 0,64 | 0,65 | — | — |

- Null: gerçek max |ρ| = 0,774; karışık veride %95'lik = 0,58 (%99 = 0,62). Hiçbir permütasyon gerçeği geçmedi.
- Wilcoxon (model hatası vs medyan ve vs bölge medyanı): hepsi p ≤ 0,005.
- "Önce ölüm": LEx orta noktası t0'dan medyan 18 yıl önce (%94 ülkede önce); LEx 55 eşiği 20 yıl önce (%98). Ama gecikmenin SD'si 11,7 yıl (t0'ın SD'si 15,5) → gecikme sabit değil.
- İlişki yok: 1950 nüfus (ρ −0,02), 1950–60 göç (0,03), SRB, 1950–70 iyileşme hızı (dLEx −0,10).

## Dürüst yorum
- Güçlü ve sağlam (bölge içinde de, null'u açık farkla geçiyor, LOO hatası yarıya iniyor). Demografik dönüşüm teorisinin klasik "önce ölüm, sonra doğurganlık" sırasıyla tutarlı.
- Ama büyük ölçüde **beklenen** bir sonuç: İkisi de aynı "kalkınma zamanlamasının" damgaları (karıştırıcı). Nedensellik yok.
- Kısmen mekanik/ölçüm kaynaklı: CDR yaş yapısına (dolayısıyla doğurganlığa) bağlı; veri zayıf ülkelerde UN ölüm ve doğurganlığı aynı kaynaklardan birlikte tahmin ediyor ve seriler düzleştirilmiş. LEx yaş yapısından bağımsız olduğu için en temiz aday.
- Eşik yıllarının bir kısmı t0'dan SONRA (LEx ≥ 70: 25 ülkede 2024+ projeksiyon). Sadece "t0'dan önce" alt örneği (sonuca göre seçim, dikkat): LEx orta nokta ρ 0,79.
- 200 ülke örneğinde ρ 0,91'e çıkıyor, ama uçlardaki t0'lar çıkarım ve UN projeksiyonu (Afrika için ölüm de projeksiyon) → şişkin.
