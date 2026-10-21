# Ön kayıt: "Sağlık saati doğurganlık saatini öne çekiyor mu?" (doğal deney, Acemoglu & Johnson aracı)

**Yazıldığı an:** 21 Ekim 2026. Bu plan, sonuçlara bakılmadan yazıldı ve analizden ÖNCE git'e kaydedildi (commit zamanı kanıttır).
Sonuçlara bakmadan yapılan tek şey: veri dosyalarının sütunlarını ve örneklemdeki ülke sayısını saymak.

## Soru

Q3 şunu buldu: sağlık saati (yaşam beklentisinin en hızlı yükseldiği yıl) ile doğurganlık saati (t0) birlikte gidiyor (ρ = 0,77) ve sağlık %94 önce dönüyor. Ama bu birliktelik iki hikâyeyle de açıklanabilir:
1. Sağlık doğurganlığı öne çekiyor (çocuklar hayatta kalınca daha az doğum).
2. Kalkınma ikisini birden öne çekiyor, sağlık sadece daha hızlı tepki veriyor.

Bu test, kalkınmadan bağımsız bir sağlık şokuyla (doğal deney) 1'i 2'den ayırmaya çalışır.

## Araç (instrument)

**Acemoglu & Johnson (2007), JPE 115(6): 925–985, "tahmini ölüm" (predicted mortality, `compsjmhatit`).** 1940'ta her ülkede ölümlerin hangi bulaşıcı hastalıklardan (sıtma, tüberküloz, zatürre, çiçek, kızamık, tifo, difteri, boğmaca…) geldiğine ve bu hastalıklara karşı ilaç ve aşıların dünyaya yayıldığı tarihlere göre kurulur. Mantık: 1940'larda penisilin, streptomisin, DDT ve aşılar herkese aynı anda geldi; ölümleri bu hastalıklardan gelen ülkeler daha çok kazandı. 1950'den sonra araç her yerde ≈ 0, yani bilgi tek bir sayıda: **1940 değeri (PM40)**.

Veri: MIT veri arşivi, `disease.dta` (indirme 21 Ekim 2026) → `data_dis/aj2007/`.

## Örneklem

- **Ana (S25):** AJ temel örneklemi (`sjbasesamplenoncomm==1`), 1940 verisi var (`sample40==1`), bizim doğurganlık dönüm noktası veride görülen (`guvenilir`) ve sağlık saati bulunan ülkeler → **25 ülke** (hiçbiri "başlangıçta zengin" değil). Türkiye 1940 verisi olmadığı için örneklemde YOK.
- **Duyarlılık (S47):** 1940 verisi olan 47 AJ ülkesinin hepsi, dönüm noktası çıkarımla bulunanlar dahil (Avrupa'nın 1950 öncesi saatleri model çıkarımı).

## Ana model (tek ön kayıtlı test)

İki aşamalı en küçük kareler (2SLS), dayanıklı standart hata (HC1):

- **1. aşama:** `t0_saglik = a + π·PM40 + γ1·LE40 + γ2·log(GDPpc40) + e`
- **2. aşama:** `t0 = b + β·t0_saglik(tahmin) + δ1·LE40 + δ2·log(GDPpc40) + u`

LE40 (AJ'nin 1940 yaşam beklentisi) ve 1940 geliri (Maddison, AJ dosyası) kontrol: **"1940'ta aynı derecede hasta ve aynı derecede yoksul iki ülkeden, ölümleri tedavisi bulunan hastalıklardan gelen hangisiyse"** karşılaştırması.

- **Beklenen işaret:** π < 0 (tedavi edilebilir ölüm payı yüksek → sağlık saati daha erken). β > 0 (sağlık saati 1 yıl öne gelince doğurganlık saati β yıl öne gelir).
- **Raporlanacaklar:** π ve 1. aşama F (dayanıklı), indirgenmiş form (t0 ~ PM40 + kontroller), β ve **Anderson–Rubin %95 aralığı** (zayıf araca dayanıklı), karşılaştırma için OLS β.

## Durdurma ve yorum kuralları (sonuçtan önce yazıldı)

| Durum | Yorum |
|---|---|
| F < 10 | "Zayıf araç." β yorumlanmaz; sadece indirgenmiş form ve AR aralığı yazılır. Sonuç: "Bu doğal deney sağlık saatini yeterince oynatmıyor; sebebi ayıramadık." |
| F ≥ 10, AR aralığı 0'ı dışlıyor, β > 0 | "Doğal deney, sağlığın doğurganlık saatini öne çektiğini DESTEKLİYOR (25 ülke)." Asla "kanıtladı" denmez. |
| F ≥ 10, AR aralığı 0'ı içeriyor | "Araç sağlık saatini oynatıyor, ama doğurganlık saatine etkisi ayırt edilemiyor." |
| β < 0 anlamlı | Ters yön: raporlanır, hikâye buna göre düzeltilir. |

## Duyarlılık (betimsel, ayrı p-değeri yorumlanmaz)

1. **S47** (çıkarımla bulunan saatler dahil).
2. **Dört büyük hastalık endeksi** (kullanıcının fikri, sonuçtan önce seçildi): 1940'taki sıtma + tüberküloz + zatürre + çiçek ölüm hızlarının toplamı, PM40 yerine araç. Seçim gerekçesi: o dönemin en büyük dört bulaşıcı katili ve her birine 1940'larda yayılan bir müdahale var (DDT/klorokin, streptomisin/BCG, penisilin/sülfa, aşı).
3. **Kontrolsüz** model (LE40 ve gelir olmadan): karıştırıcının ne kadar etkili olduğunu görmek için.
4. **Bir ülkeyi dışarıda bırakma:** β'nın en küçük ve en büyük değeri (tek ülkeye bağımlılık).

## Bilinen sorunlar (önceden yazıldı)

- **Dışlama kısıtı:** 1940 hastalık yapısı doğurganlığı sağlık dışından da etkileyebilir (coğrafya, tropik iklim, sömürge geçmişi). Kontroller bunu azaltır, yok etmez.
- **Örneklem küçük (25).** Güç düşük; "bulamadık" ≠ "etki yok".
- **Ölçüm:** AJ'nin 1940 hastalık verisi eski kaynaklara (Milletler Cemiyeti, ulusal raporlar) dayanıyor ve tartışmalı (Bloom, Canning & Fink 2014; AJ'nin cevabı NBER w20064). Sağlık saati 1950–2023 verisiyle bulunduğu için 1950 öncesi dönenlerin saati çıkarım.
- **Türkiye örneklemde yok.**
- Daha geniş ülke kapsamlı yeni sürüm (Kreitmeir & Überfuhr 2024, J Appl Econometrics) şu an sunucusuna erişilemediği için kullanılmadı; erişilirse sağlamlık olarak eklenir.

## Ne zaman slayta girer?

Sonuç ne olursa olsun önce ekiple konuşulur. Slayt yapısı sonuçtan sonra kararlaştırılır.
