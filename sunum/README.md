# Sunum klasörü

## ⭐ FİNAL koyu sunum (22 Ekim, Q3 + Q4'lü, sürüm 20): https://claude.ai/artifact/MEYv3jt4EcXwixohtjvXd4
- Q4 (22 Ekim): Slayt 4 = doğal deney (`pilot/neden_grafigi.py` → `outputs/v3_s4_cause.png`, `v3_s4_pop_compact.png`; analiz `kesif/f_kreitmeir/`) + Türkiye + sınırlar. Kaynakça +4 kaynak.
- Yerel önizleme: `ONIZLEME=1 python sunum/slayt_uret.py <klasör>` (görseller outputs/'tan). Q4 önizlemeleri `onizleme/q4_*.png`. Q4 öncesi kaynaklar `eski_surumler/slaytlar_kaynak_q4_oncesi/`.
- Kaynak: `slaytlar_kaynak/` (deck.json + slides). Üretim: `python pilot/saglik_saati.py` → `python sunum/slayt_uret.py <klasör>/project/slides` → `slaytlar_kaynak/slides/references.html`'i kopyala.
- Q3 grafiği: `outputs/v3_s3_health.png` (`pilot/saglik_saati.py`, veri `clean/saglik_saati.csv`).
- Eski koyu sunum (RBtUDKTNEkZzcXgiZFYXJ6) aynen duruyor; Q3 öncesi kaynaklar `eski_surumler/taslak1_koyu_q3_oncesi/`.

- **Final sunum (çevrim içi, düzenlenebilir):** https://claude.ai/artifact/RBtUDKTNEkZzcXgiZFYXJ6
  PDF veya PowerPoint olarak indirmek için sunum sayfasındaki indirme / Share menüsünü kullan.
- `konusma_metni.md`: İngilizce konuşma metni + Türkçe karşılığı + sayıların kaynak tablosu.
- `slaytlar_kaynak/`: Sunumun yedek kaynak dosyaları (her slaytın HTML'i ve deck.json).
  Slaytlardaki görseller `../outputs/` klasöründe: final_anim_same_path.gif, final_2_money_or_school.png, final_3_turkiye.png.
- Hoca ara rapor sunumu (Türkçe, 15 Ekim): https://claude.ai/artifact/AYJCa9WxkccNUmNX2F2HYy

## Koyu, renkli sürüm (17 Ekim, sürüm 8)
- Grafikler: `pilot/kapak_saat.py` (kapak: saat kadranı; eski 3B manzara `pilot/kapak.py`), `pilot/slayt_koyu.py` (slaytlardaki koyu grafikler), `TEMA=koyu python pilot/animasyon.py` (koyu animasyon).
- 2–4. slaytların renkli tabloları: `python sunum/slayt_uret.py <klasör>` (sayılar clean/ dosyalarından gelir).
- `onizleme/`: her slaytın yaklaşık görüntüsü (headless Chrome ile alındı).

## Sürüm 12 (17 Ekim)
- Bütün slaytlar (kaynakça hariç): `python sunum/slayt_uret.py sunum/slaytlar_kaynak/slides`
- Harita ve bölge testi: `python pilot/harita_test.py` → `outputs/v3_s2_map.png`, `v3_s2_pairs.png`, `bolge_testleri.csv`
- Kapak: `python pilot/kapak_saat.py` · koyu animasyon: `TEMA=koyu python pilot/animasyon.py`
- Sıra: 04 → 05 notebook'ları → `pilot/slayt_koyu.py` → `pilot/harita_test.py` → `pilot/kapak_saat.py` → `sunum/slayt_uret.py`

## Taslak 2: açık renk (17 Ekim)
- Link: https://claude.ai/artifact/2iPFsKcDQaWZnYpob4h4M3 (özel; paylaşmak için Share menüsü). Mavi sürüm (Taslak 1) aynen duruyor.
- Aynı içerik, açık krem zemin (#F3F2EE / kart #FBFBF9), dataviz açık paleti. Grafit denemesi beğenilmedi, açık sürüm onun yerine geçti.
- Üretim: `TEMA=acik` ile pilot/slayt_koyu.py, pilot/harita_test.py, pilot/kapak_saat.py, pilot/animasyon.py; sonra `TEMA=acik python sunum/slayt_uret.py <klasör>`.
- Kaynak dosyalar ve ön izlemeler: `sunum/taslak2_acik/`.
- Not: Bir metin değişirse iki sunum da yeniden üretilmeli (ayrı dosyalar).

## Düzen (17 Ekim gece)
- Her içerik slaytı aynı iskelet: üst yazı + başlık + tek satır alt başlık · hizalı kart ızgarası · "What it means" bandı · dipnot.
- Grafiklerin içinde başlık yok; başlık kartta. Grafikler kart boyutunda çiziliyor (`pilot/slayt_koyu.py`, `pilot/harita_test.py`).
- Slayttaki animasyon sade sürüm: `TEMA=koyu SADE=1` / `TEMA=acik SADE=1 python pilot/animasyon.py` (başlıksız, büyük yazılı). Video için tam sürüm aynen duruyor.
- Korelasyon tablosu 6 değişkene indi (LE65 ve PopGrowthRate çıkarıldı: biri LEx'in neredeyse aynısı, öbürü aritmetik).

## 4 sunum linki (17 Ekim gece)
| Sürüm | Link |
|---|---|
| ESKİ düzen · koyu | https://claude.ai/artifact/NRPyWAD6MqBaFtmax9E1kk |
| ESKİ düzen · açık | https://claude.ai/artifact/VqbTEVuW4vrT3BMkFsheKk |
| YENİ düzen · koyu | https://claude.ai/artifact/RBtUDKTNEkZzcXgiZFYXJ6 |
| YENİ düzen · açık | https://claude.ai/artifact/2iPFsKcDQaWZnYpob4h4M3 |
