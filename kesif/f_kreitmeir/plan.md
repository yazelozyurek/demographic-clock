# Ön kayıt: Yenilenmiş "tahmini ölüm" aracıyla sağlık → doğurganlık testi (Kreitmeir & Überfuhr 2024)

**Yazıldığı an:** 21 Ekim 2026. Plan, doğurganlık sonuçlarına bakılmadan yazıldı ve analizden ÖNCE git'e kaydedildi.
Sonuçtan önce yapılanlar: veri dosyalarını okumak, örneklemlerdeki ülke sayılarını saymak, makalenin 1. aşama katsayısını
veri kontrolü olarak tekrarlamak (−0,399, makaleyle aynı). Doğurganlıkla ilgili hiçbir sonuç hesaplanmadı.

## Bu, üçüncü sebep denemesi (hepsi raporlanır)

1. `kesif/d_neden/`: Acemoglu & Johnson aracı, saat tasarımı, 25 ülke → zayıf araç (F 0,8).
2. `kesif/e_hiv/`: HIV ters şoku → ana test fark yok (p 0,40).
3. **Bu plan.** Neden yeni bir deneme? (a) Yenilenmiş araç daha geniş ülke kapsamlı ve yazarlara göre ön-eğilim (*pre-trend*) testinden geçen tek sürüm "sadece ülke düzeyi" olanı. (b) 1. denemeden öğrendiğimiz: araç bir **değişim miktarını** (1940–1980 yaşam beklentisi artışı) tahmin etmek için tasarlandı, bir zamanlamayı (dönüm yılı) değil. Bu yüzden ana test aracın kendi "uzun fark" tasarımıyla kurulur.

## Veri

- **Kreitmeir & Überfuhr (2024)**, *J Appl Econometrics* 39(2): 327–337. Replikasyon verisi `ku_data.csv` (CC BY 4.0). ZBW Journal Data Archive'a erişilemediği için İnternet Arşivi kopyasından indirildi (kayıt tarihleri 14.03.2024 ve 11.07.2024); dosya boyutları arşivdeki üst veriyle birebir aynı. → `data_dis/kreitmeir/`
- **Doğurganlık:** WPP2024 TFR (`clean/countries_1950_2100.csv`), K1: nüfus ≥ 100 bin.
- Aynı ülkenin farklı coğrafi tanımlarından, her örneklemde o örneklemin işaretli satırı kullanılır (ör. Brezilya 21 kasaba).

## Ana model (tek ön kayıtlı test)

**Araç:** yazarların tercih ettiği `changemortctry` (sadece ülke düzeyi). **Örneklem:** yazarların "homojen" örneklemi `kusample9and2ctry == 1`, WPP verisi olan → **52 ülke** (yaşam beklentisi değişimi olan 50).

İki aşamalı en küçük kareler, standart hata `ctrycluster` kümelemeli (yazarlar gibi):

- **1. aşama:** `ΔlnLEB(1940→1980) = a + π·changemortctry + e`
- **2. aşama:** `ΔTFR(1950→1990) = b + β·ΔlnLEB(tahmin) + u`

**Neden 1950→1990:** WPP'nin ilk yılı 1950. Sağlık şoku 1940'lar ve 1950'lerde geldi; Q3'e göre doğurganlık sağlıktan medyan 18 yıl sonra dönüyor, yani tepki 1970'ler ve 1980'lerde beklenir.

- **Beklenen işaret:** π < 0 (tahmini ölüm daha çok düşünce yaşam beklentisi daha çok artar; makalede doğrulandı). **β < 0** (yaşam beklentisi daha çok artan ülkede 1950–1990 doğurganlık düşüşü daha büyük).
- **Raporlanacaklar:** π, etkin F (tek araçta kümelemeli dayanıklı F = t²), indirgenmiş form, β (ve "yaşam beklentisi %10 daha çok artınca TFR kaç çocuk değişir" çevirisi), Anderson–Rubin %95 aralığı, karşılaştırma için OLS.

## Yorum kuralları (sonuçtan önce yazıldı)

| Durum | Yorum |
|---|---|
| F < 10 | "Zayıf araç; ayıramadık." β yorumlanmaz. |
| F ≥ 10, AR aralığı tamamen 0'ın altında | "Doğal deney, sağlık iyileşmesinin doğurganlık düşüşünü büyüttüğünü DESTEKLİYOR (52 ülke)." "Kanıtladı" denmez. |
| F ≥ 10, AR aralığı 0'ı içeriyor | "Araç sağlığı oynatıyor, ama doğurganlık düşüşüne etkisi ayırt edilemiyor." |
| F ≥ 10, AR aralığı tamamen 0'ın üstünde | "Ters yön: sağlık iyileşmesi 1950–1990'da doğurganlığı yüksek tuttu." Hikâye buna göre düzeltilir. |

## Duyarlılık (betimsel, ayrı p-değeri yorumlanmaz)

1. **Pencere:** ΔTFR 1950→1980 ve 1950→2000.
2. **Diğer araç sürümleri** (her biri kendi örneklemiyle): AJ orijinali (47), ülke + kasaba (69, Türkiye dahil), kasaba yerine (69), en yüksek (69). Not: yazarlara göre bu dördünde ön-eğilim var.
3. **Sadece düşük ve orta gelirli ülkeler** (`startrich == 0`), yazarların sağlamlık kontrolü.
4. **Başlangıç sağlığı kontrolü** (Bloom, Canning & Fink 2014 eleştirisi): ln LE1940 = ln(WPP LEx1980) − ΔlnLEB(1940→1980) eklenir.
5. **Saat tasarımı** (1. denemeyle karşılaştırma için): t0 ~ t0_saglik, araç `changemortctry`, bizim güvenilir saatlerle örtüşen 23 ülke, kontrolsüz.
6. **Veri kontrolü:** yazarların toplam doğum sonucunu tekrar etmek: Δln(toplam doğum, 1940→1980) ~ ΔlnLEB, aynı araç ve örneklem (makale: pozitif ve anlamlı).

## Bilinen sorunlar (önceden yazıldı)

- **Toplam doğum ≠ TFR.** Yazarlar sağlık iyileşince toplam doğumun arttığını buldu; bu, daha çok kadının doğurganlık yaşına ulaşmasından da gelebilir. Biz kadın başına çocuk sayısını (TFR) test ediyoruz.
- **Karışık kaynaklar:** yaşam beklentisi değişimi (1940–1980) Kreitmeir verisinden, TFR (1950–1990) WPP'den.
- **Dışlama kısıtı:** 1940 hastalık yapısı doğurganlığı sağlık dışından da etkileyebilir (coğrafya, sömürge geçmişi, başlangıç gelir düzeyi).
- **Zengin ülkeler:** 11 başlangıçta zengin ülkede 1950 TFR'si zaten düşüktü; güç kısmen zengin–yoksul farkından gelebilir (Duyarlılık 3 bunu kontrol eder).
- Türkiye ana örneklemde yok (sadece ülke + kasaba sürümlerinde var).
