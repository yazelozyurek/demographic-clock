# Keşif C: Çok yöntemli korelasyon araması ve sıfır kalibrasyonu (sunuma GİRMEZ)

Tarih: 18 Ekim 2026. Sonuç (t0) = TFR'nin en hızlı düştüğü yıl (`clean/t0_tablosu.csv`).

## Örneklemler
- **S66:** `clean/para_okul_tablosu.csv` (dış veri + WPP). Gelir 2 ülkede eksik olduğu için tek değişkenli testlerde n = 64.
- **S115:** `guvenilir == True` (sadece WPP özellikleri + ekvator uzaklığı). t0 1955–2019.

## Özellikler
- 16 WPP özelliği: 1950 ve 1960 düzeyleri, 1950→1970 değişimler, nüfus, yoğunluk, göç, SRB, ekvator.
- 13 dış özellik: Maddison gelir, Barro–Lee eğitim ve kompozisyon, cinsiyet farkı.
- TFR ailesi kullanılmadı.
- 1960/1970 özellikleri `post_t0_risk = True` olarak işaretli: t0'ı 1970'ten önce olan ülkelerde bu ölçümler t0'dan SONRAya düşüyor.

## Kod (çalıştırma sırası)
1. `ozellik.py`
2. `tarama_tek.py 200`
3. `cok_degiskenli.py 200`: `OMP_NUM_THREADS=1` ile çalıştırın, yaklaşık 50 dakika sürüyor.
4. `ek_karsilastirma.py`
5. `birlestir.py`

Çıktılar:
- `test_log_hepsi.csv`: 539 test, BH q değerleriyle.
- `null_tek.csv`, `null_cok.csv`
- `loo_sonuc.csv`
- `kararlilik.csv`
- `ozet.txt`

## Bulgular
1. **Toplam 539 test yapıldı.** 313'ünde q < 0,05 çıktı. Bunların çoğu, aynı "kalkınma düzeyi" sinyalinin farklı yöntemlerle tekrar ölçülmesi.
2. **En güçlü ilişkiler** (hepsi t0'dan önce ölçülmüş):

   | Özellik | Örneklem | İlişki |
   |---|---|---|
   | LEx 1950 | S115 | ρ = −0,65 |
   | LEx 1950 | S66 | ρ = −0,58 |
   | Q5, CDR, IMR 1950 | S115 | ρ ≈ +0,53…+0,61 |
   | Her iki cinsiyetin eğitimi, 25–64 yaş, 1950 | S66 | ρ = −0,60, r = −0,65 |
   | Genç kadın eğitimi 1950 | S66 | ρ = −0,56 |
   | Okula gitmemiş oranı | S66 | ρ = +0,59 |
   | log yoğunluk 1950 | S66 / S115 | ρ = −0,46 / −0,42 |

   - Bu ilişkiler bölge sabitlenince, gelir sabitlenince ve t0 ≥ 1972 alt örnekleminde sürüyor.
   - Kantil regresyonda üç kantilde de eğim aynı yönde.
   - **Gelir 1950 zayıf:** ρ = −0,22, p = 0,07. Ekvator uzaklığı da anlamsız.
3. **Sıfır kalibrasyonu (200 permütasyon, bütün tarama tekrarlandı):**
   - S66: En iyi |Spearman| gerçekte 0,62, sıfırın 95. yüzdeliği 0,38.
   - S115: En iyi |Spearman| gerçekte 0,72, sıfırın 95. yüzdeliği 0,27.
   - Bütün yöntemlerde (dcor, MI, spline, partial) sıfırın en büyük değeri gerçek değeri hiç geçmedi.
   - Yani arama tek başına bu büyüklükte bir ilişki üretmiyor.
4. **LOO tahmini (medyan mutlak hata, yıl):**
   - S115:
     - Baz: 12,0
     - LEx 1950 tek başına OLS: 8,5 (p < 0,001)
     - En iyi çok değişkenli model (random forest): 6,4
     - Sıfırda en iyi modelin 5. yüzdeliği: 10,0
   - S66:
     - Baz: 9,5
     - Eğitim (iki cinsiyet) OLS: 7,0, p = 0,017
     - LEx 1950 tek başına: 7,3
     - LASSO: 6,2
     - Gradient boosting: 5,0
     - Sıfırın 5. yüzdeliği: 7,9
   - Çok değişkenli modeller, en iyi tek değişkene karşı:
     - Sadece S115'teki random forest anlamlı (p = 0,008).
     - S66'da anlamlı değil (p = 0,06–0,13).
   - Not: "Kat içinde en iyi 1 değişkeni seç" yöntemi S66'da bazı geçemedi (9,1). Sıralamada en iyi çıkan değişken (okula gitmemiş oranı), doğrusal modelde en iyi değil.
5. **Kararlılık seçimi:** log Q5 1950 ve log yoğunluk 1950 iki örneklemde de en kararlı değişkenler (yaklaşık 0,75–0,97). S66'da eğitim 0,71. Değişkenler birbiriyle çok ilişkili olduğu için hangi değişkenin seçileceği, birbirine yakın göstergeler arasında el değiştiriyor.

## Karar
**Güçlü ve sağlam bir ilişki VAR. Ama "zenginlik" ya da coğrafya değil, 1950'deki genel kalkınma ve ölüm düzeyi.**
- 1950'de yaşam beklentisi yüksek, çocuk ölümü düşük ve nüfusu daha eğitimli olan ülkeler dönüm noktasına daha erken ulaştı.
- Bu, demografik dönüşüm teorisinin "önce ölüm, sonra doğurganlık" sırasıyla tutarlı.
- Etki büyüklüğü: |ρ| yaklaşık 0,6. LOO hatası bazın %30–47 altında. Ama ülke düzeyinde tahmin hatası hâlâ 5–8 yıl.

**Nedensellik değil. Olası karıştırıcılar:**
- Genel kalkınma ve devlet kapasitesi
- Kentleşme
- Sömürge geçmişi
- Aile planlaması programları
- Din ve kültür
- Ada ve küçük devlet etkisi (yoğunluk için)

**Ölçüm notu:** Veri kaydı zayıf ülkelerde UN'in 1950 LEx ve TFR tahminleri ortak model girdilerine dayanıyor olabilir. Bu da ilişkiyi kısmen şişirebilir.

**Yoğunluk bulgusu beklenmedik.** Tek bir aramada çıktığı için doğrulayıcı bir sonuç sayılmamalı.
