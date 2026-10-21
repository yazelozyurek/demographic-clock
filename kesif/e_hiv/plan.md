# Ön kayıt: "Ters şok". HIV/AIDS sağlığı bozunca doğurganlık düşüşü yavaşladı mı?

**Yazıldığı an:** 21 Ekim 2026. Plan, doğurganlık sonuçlarına bakılmadan yazıldı ve analizden ÖNCE git'e kaydedildi.
Sonuçtan önce yapılan tek şey: HIV verisini indirmek ve en yüksek yaygınlık değerlerine göre ülkeleri saymak (tedavi grubunu tanımlamak için).

## Fikir

Q3: sağlık saati doğurganlık saatinden önce dönüyor. Sağlık doğurganlığı öne çekiyorsa (çocuklar hayatta kalınca daha az doğum), **tersi de görülmeli:** sağlık birden bozulduğunda doğurganlık düşüşü yavaşlamalı. 1990–2005 arasında HIV/AIDS, Afrika'nın güneyinde ve doğusunda yaşam beklentisini 10–20 yıl düşürdü. Bu, kalkınmadan bağımsız gelen bir sağlık şoku.

**Önemli:** HIV doğurganlığı biyolojik olarak da düşürür (enfekte kadınlarda gebelik olasılığı daha düşük). Bu etki ters yönde çalışır. Yani:
- Düşüş **yavaşladıysa** → biyolojik etkiye rağmen yavaşladı → "sağlık → doğurganlık" yönünde destek.
- Düşüş **hızlandıysa** → biyolojik etki baskın ya da sağlık kanalı yok; ayırt edilemez.
- **Fark yoksa** → iki etki birbirini götürmüş olabilir ya da hiçbiri yok; ayırt edilemez.

## Gruplar (Dünya Bankası SH.DYN.AIDS.ZS, 15–49 yaş HIV yaygınlığı, 1990–2023, indirme 21 Ekim 2026)

- Evren: Sahra altı Afrika (UN alt bölgeleri: Doğu, Batı, Orta, Güney Afrika; Kuzey Afrika hariç), nüfus ≥ 100 bin (K1).
- **Tedavi (yüksek HIV):** en yüksek yaygınlık ≥ %10 → 11 ülke (Zimbabve, Esvatini, Botsvana, Lesotho, Güney Afrika, Malavi, Zambiya, Namibya, Mozambik, Uganda, Kenya).
- **Kontrol (düşük HIV):** en yüksek yaygınlık < %3.
- Arada kalanlar (%3–10) ana karşılaştırmada yok, doz analizinde var.

## Sonuç ölçüsü: "ortak yoldan sapma" (kendi Demografik Saat'imizle)

1. Ortak eğri (U, L, k) ana modelden: `clean/t0_tablosu.csv` kaymalarıyla 1950–2023 verisine tek `curve_fit`.
2. Her ülkeyi 1990'daki TFR'sine göre ortak eğrinin üstüne yerleştir (eğrinin o TFR'ye eşit olduğu an).
3. Ortak eğri o noktadan 15 yıl ilerletilir → 2005 için beklenen TFR.
4. **Sapma D = gerçek TFR(2005) − beklenen TFR(2005).** D > 0: ülke ortak yoldan daha yavaş düştü (duraklama).

1990 TFR'si 6,5'in üstünde olanlar ana analizde dışarıda (eğrinin tepesi düz olduğu için konum belirsiz); duyarlılıkta dahil.

## Ana test (tek ön kayıtlı test)

- **İstatistik:** medyan D (tedavi) − medyan D (kontrol).
- **Çıkarım:** permütasyon testi. Tedavi etiketleri tedavi + kontrol ülkeleri arasında 10.000 kez rastgele dağıtılır; çift yönlü p.
- **Sağlık şoku gerçekten oldu mu? (betimsel ön koşul):** 1990→2005 yaşam beklentisi ve Q5 (5 yaş altı ölüm) değişimi, iki grupta. Tedavi grubunda sağlık kötüleşmediyse test anlamsızdır.

## Duyarlılık (betimsel)

1. **Doz:** bütün Sahra altı ülkelerde Spearman(en yüksek HIV yaygınlığı, D).
2. **Pencere:** 1990→2010.
3. 1990 TFR'si > 6,5 olanlar dahil (konum eğrinin U − 0,05 noktasına sabitlenir).
4. Ortak eğri yerine basit eğim: 1995–2010 yıllık ortalama TFR değişimi − 1980–1990 yıllık ortalama TFR değişimi (fark içinde fark).

## Yorum kuralları (sonuçtan önce yazıldı)

| Sonuç | Yorum |
|---|---|
| p < 0,05, tedavi D > kontrol D | "HIV şoku olan ülkelerde doğurganlık düşüşü ortak yoldan daha çok yavaşladı. Biyolojik etki ters yönde olduğu için bu, sağlık → doğurganlık hikâyesiyle tutarlı." Sebep "kanıtlandı" denmez. |
| p < 0,05, tedavi D < kontrol D | "Daha hızlı düştü; biyolojik etki ya da başka kanallar baskın. Sağlık kanalını bu testle ayıramıyoruz." |
| p ≥ 0,05 | "Fark ayırt edilemedi." |

## Bilinen sorunlar (önceden yazıldı)

- HIV'in biyolojik etkisi (yukarıda) ve davranış değişiklikleri (prezervatif kampanyaları doğurganlığı da düşürür).
- Güney Afrika ülkeleri zaten daha erken düşüşe başlamıştı; ortak eğrideki konuma yerleştirme bunu kısmen düzeltir.
- Az ülke: tedavi 11, kontrol belki 15–20.
- UN, bu ülkelerde ölümü HIV modelleriyle (UNAIDS) tahmin ediyor; doğurganlık ise anket ve sayımlardan. Yine de iki seri aynı modelden gelmiyor.
- Ortak eğri, tedavi ülkelerinin 1990 sonrası verisini de içeren 200 ülkeyle kuruldu (11/200, etkisi ihmal edilebilir).
- Kenya ve Gana gibi ülkelerdeki 2000 civarı "doğurganlık duraklaması" HIV'den bağımsız da görüldü (Bongaarts); kontrol grubu bunu yakalamak için var.
