# Konuşma metni: The Demographic Clock (FİNAL koyu sunum, Q4'lü, 22 Ekim)

- **Sunum:** https://claude.ai/artifact/MEYv3jt4EcXwixohtjvXd4 (22 Ekim, sürüm 20: Q4'lü hali yayında; slayt notları bu metinle birebir aynı). Eski sunumlar aynen duruyor.
- **Uzunluk:** 596 kelime. Dakikada 130 kelimeyle yaklaşık 4,6 dakika, animasyon ve duraklamalarla yaklaşık 4,9 dakika. Sınır 5 dakika. Provada 5:00'ı geçerse kısaltma sırası: (1) Slayt 2'deki ", and it predicted best in backtests" (−6 kelime), (2) Slayt 4'teki "Türkiye's health clock turned in 1965, its fertility clock in 1982." (−11; bu bilgi slaytta da yazıyor).
- **21 Ekim, Q4 (tırmanan hikâye):** Slayt 4 artık "One more question": Q4 doğal deney (Kreitmeir & Überfuhr 2024 aracı, 50 ülke) + üç ön kayıtlı testin sonucu + Türkiye + sınırlar. Kapak ve Slayt 1 bilerek "üç soru" diyor; Q4 sürpriz olarak geliyor. Horoz cümlesi Slayt 3'ün sonuna alındı, böylece Slayt 4'e köprü oluyor. Kaynakçaya 4 kaynak eklendi. Eski hal: `sunum/eski_surumler/konusma_metni_q4_oncesi.md`.
- **Önceki değişiklikler (21 Ekim):** Q3 ("Health first?") eklendi; horoz örneği eklendi; Q2 "That no is a result, not a failure" diye çerçevelendi; kapak isim sırası Yazel, Elif, Zehra, Rojbin; yapay zekâ beyanı Sürüm 2.
- **Dil:** Her bölümde önce okunacak İngilizce metin, altında Türkçe karşılığı var. Türkçe kısım sadece anlamak içindir, okunmayacak.
- **"What it means" bantları:** Her içerik slaytının altında sarı çerçeveli bir yorum bandı var. Bantlar okunmayacak; jüri slaytı tek başına okurken anlamı onlardan görür. Metinleri ve Türkçe karşılıkları en altta.
- **Kontrol listesi:** Sayılar doğru mu? Cümleler sana doğal geliyor mu? Takıldığın kelime var mı? Değiştirmek istediğin yeri işaretle.

### Q4 için kısaltılan cümleler (geri almak istersen)

| Slayt | Eski hali | Yeni hali | Neden |
|---|---|---|---|
| 1 | "Summing every row **of the file** gives 363 billion people…; countries alone give **the correct** 8.09 billion. We keep **the 200 countries above 100,000 people**, 99.98 percent of the world, and list every place we leave out. **Values after 2023 are UN projections, always drawn dashed.**" | "Summing every row gives 363 billion people…; countries alone give 8.09 billion. We keep 200 countries, 99.98 percent of the world, list every place we leave out, and always draw UN projections dashed." | Aynı bilgi, daha kısa |
| 2 | "…one curve explains 94 percent; **a level shift with the same number of parameters reaches only 87. In backtests, the shared curve had the smallest typical error twenty years ahead.**" | "…one curve explains 94 percent, and it predicted best in backtests." | %87 ve backtest tablosu slaytta duruyor |
| 2 | "On the map, the clock runs from Europe to Africa, **and a Kruskal–Wallis test confirms that regions turn at different times.**" | "On the map, the clock runs from Europe to Africa." | Test slaytta ve bantta duruyor (p < 0,001) |
| 3 | "**Our data can show when a country turns, not why, so we checked what lines up with that moment.**" (18 Ekim'de senin seçtiğin (b) cümlesi) | "Next: what lines up with the turning point?" | "Neden değil" mesajını artık horoz ve Q4 taşıyor. Geri istersen +10 kelime |
| 4 | Türkiye'nin "45/66 daha zengin, 54/66 daha az eğitim" cümlesi ve "kayıt sistemi zayıf yerlerde UN tahmini" cümlesi | Konuşmadan çıktı | İkisi de slaytta yazılı (Türkiye kartı ve "What we do not claim") |

---

## Kapak (yaklaşık 15 sn)

> Hello, we are Stat4Sight from Kırıkkale University. Every country is moving from large families to small ones. Our project asks three things: is it the same journey everywhere, does money or school set its timing, and does health come first?

*Merhaba, biz Kırıkkale Üniversitesi'nden Stat4Sight takımıyız (okunuşu: "stat for sayt"). Her ülke kalabalık ailelerden küçük ailelere doğru ilerliyor. Projemiz üç şey soruyor: Bu yolculuk her yerde aynı mı, zamanlamasını para mı yoksa okul mu belirliyor, ve sağlık önce mi geliyor?*

*(Not: Kapak bilerek "üç şey" diyor. Dördüncü soru Slayt 4'te sürpriz olarak geliyor.)*

## Slayt 1 · Soru ve veri (yaklaşık 45 sn)

> In 2023, women in the Republic of Korea had 0.72 children on average; women in Niger had 6.06. In 1950, only 3 of 200 countries were below replacement; by 2023 it was 103. So we asked: do countries follow the same path, and what moves with their turning point: money, school, or health?
>
> Our data is UN World Population Prospects 2024. Summing every row gives 363 billion people, because regions repeat countries; countries alone give 8.09 billion. We keep 200 countries, 99.98 percent of the world, list every place we leave out, and always draw UN projections dashed.

*2023'te Kore Cumhuriyeti'nde kadın başına ortalama 0,72 çocuk düşüyordu, Nijer'de 6,06. 1950'de 200 ülkenin sadece 3'ü yenilenme düzeyinin altındaydı, 2023'te bu sayı 103 oldu. Bu yüzden sorduk: Ülkeler aynı yolu mu izliyor ve dönüm noktalarıyla birlikte ne yürüyor: para mı, okul mu, sağlık mı?*

*Verimiz UN Dünya Nüfus Beklentileri 2024. Bütün satırları toplayınca 363 milyar insan çıkıyor, çünkü bölgeler ülkeleri tekrar ediyor; sadece ülkeleri toplayınca 8,09 milyar çıkıyor. 200 ülkeyi tutuyoruz (dünya nüfusunun %99,98'i), dışarıda bıraktığımız her yeri listeliyoruz ve UN projeksiyonlarını hep kesikli çiziyoruz.*

## Slayt 2 · Demografik Saat (yaklaşık 55 sn + animasyon)

> Our first try fitted an S-shaped curve to each country separately. It fit, but gave nonsense: for Japan, whose decline happened before 1950, it said women started at nine children.
>
> So we borrowed the SITAR idea from children’s growth charts: one shared S-curve, and one number per country — its turning point, the year fertility falls fastest. Watch what happens when we shift each country.
>
> *(Burada animasyonun oynamasını bekle.)*
>
> By calendar year, time explains 27 percent of the differences between countries. Shifted to their own turning points, one curve explains 94 percent, and it predicted best in backtests.
>
> On the map, the clock runs from Europe to Africa. In 2023, Nigeria is at its turning point, Türkiye passed it about forty years ago, Japan about ninety.

*İlk denememizde her ülkeye ayrı bir S eğrisi oturttuk. Eğriler veriye uydu ama saçma sonuçlar verdi: Düşüşü 1950'den önce olan Japonya için "kadınlar 9 çocukla başlamış" dedi.*

*Bu yüzden çocuk büyüme eğrilerinde kullanılan SITAR fikrini ödünç aldık: tek bir ortak S eğrisi ve her ülke için tek bir sayı. Bu sayı ülkenin dönüm noktası, yani doğurganlığın en hızlı düştüğü yıl. Her ülkeyi kaydırınca ne olduğunu izleyin.*

*Takvim yılına göre zaman, ülkeler arasındaki farkların %27'sini açıklıyor. Kendi dönüm noktalarına kaydırınca tek eğri %94'ünü açıklıyor ve geriye dönük testlerde en iyi tahmini o yaptı.*

*Haritada saat Avrupa'dan Afrika'ya doğru ilerliyor. 2023'te Nijerya dönüm noktasında, Türkiye onu yaklaşık 40 yıl önce geçti, Japonya yaklaşık 90 yıl önce.*

## Slayt 3 · Saatle birlikte ne yürüyor? Para, okul, sağlık (yaklaşık 70 sn)

> Next: what lines up with the turning point?
>
> First, money or school. In 66 countries, income at the turning point ranged from 1,100 to 24,000 dollars. As a threshold it missed the year by 14 years, worse than guessing the typical year. Schooling was steadier, but no better than the calendar.
>
> That no is a result, not a failure, and it led us to the oldest prediction of transition theory: does health come first? We measured a second clock, the year life expectancy rose fastest, with the same shared curve. In 94 percent of 115 countries it came first, a median of 18 years earlier, and the two clocks move together, rho 0.77. We screened many candidates, with multiple-test correction.
>
> So money does not set the clock; health moves with it. But first is not the same as cause: a rooster crows before every sunrise, yet it does not make the sun rise.

*Sırada şu soru var: Dönüm noktasıyla ne örtüşüyor?*

*Önce para mı, okul mu. 66 ülkede dönüm noktasındaki gelir 1.100 ile 24.000 dolar arasında değişiyordu. Eşik olarak kullanılınca yılı 14 yıl şaşırdı; bu, tipik yılı tahmin etmekten bile kötü. Eğitim daha istikrarlıydı, ama takvimden daha iyi değildi.*

*Bu "hayır" bir başarısızlık değil, bir sonuç; ve bizi demografik dönüşüm teorisinin en eski tahminine götürdü: Sağlık önce mi geliyor? İkinci bir saat ölçtük: yaşam beklentisinin en hızlı yükseldiği yıl, aynı ortak eğri yöntemiyle. 115 ülkenin %94'ünde bu saat önce döndü, medyan 18 yıl önce; iki saat birlikte yürüyor, rho 0,77. Birçok aday değişkeni çoklu test düzeltmesiyle taradık.*

*Yani saati para kurmuyor; saatle birlikte yürüyen şey sağlık. Ama önce gelmek, sebep olmak demek değil: Horoz her sabah güneş doğmadan önce öter, ama güneşi o doğurmaz.*

*(Not: Horoz cümlesi bilerek sonda. Jüri "bitti" derken Slayt 4'e köprü oluyor.)*

> ℹ️ **Bilgi notu (slaytta yok, okunması zorunlu değil; jüri sorarsa ya da süre kalırsa):** As a robustness check, a pre-registered random forest using 1950 income, schooling and geography did not beat the calendar, while simpler linear models did by about two years, mainly through young women's schooling in 1950. Income never helped, so money does not set the clock, and schooling matters as a starting point rather than a threshold.

*Türkçesi: Sağlamlık kontrolü olarak, 1950'deki gelir, eğitim ve coğrafyayı kullanan, önceden kaydedilmiş bir random forest modeli takvimi geçemedi; daha basit doğrusal modeller ise yaklaşık iki yıl farkla geçti ve bu kazanç esas olarak 1950'deki genç kadın eğitiminden geldi. Gelir hiç yardımcı olmadı; yani saati para kurmuyor, okul ise bir eşik olarak değil, bir başlangıç noktası olarak önem taşıyor. (Kaynak: `pilot/ml_kontrol_plan.md`. Okunursa +≈20 sn, süre 5:00'ı aşar.)*

## Slayt 4 · Bir soru daha: Sağlık bir sebep mi? + Türkiye + sınırlar (yaklaşık 65 sn)

> So, one more question: is health a cause, or just the rooster? We ran three tests, each planned before seeing its results. Two could not tell. The third is a natural experiment: in the 1940s, new medicines and vaccines reached the world at once, and countries hit hardest by those diseases gained most. Where they saved more lives, more babies were born, but each woman had fewer: about ten percent more life expectancy, 0.44 fewer children by 1990. This supports health as a cause, but does not settle it, because the signal comes from how sick countries were in 1940.
>
> Türkiye’s health clock turned in 1965, its fertility clock in 1982. Its population likely peaks in 2047; for 2100 we show a range, 26 to 125 million.
>
> Our limits: these are country patterns, not facts about individual women, and the clock is not a race.

*O zaman bir soru daha: Sağlık bir sebep mi, yoksa sadece horoz mu? Üç test yaptık; her birini sonucunu görmeden önce planladık. İkisi ayırt edemedi. Üçüncüsü bir doğal deney: 1940'larda yeni ilaçlar ve aşılar dünyaya aynı anda ulaştı ve bu hastalıklardan en çok etkilenen ülkeler en çok kazandı. Daha çok hayat kurtarılan yerlerde daha çok bebek doğdu, ama kadın başına daha az: Yaşam beklentisi yaklaşık yüzde on daha fazla artınca, 1990'a kadar kadın başına 0,44 daha az çocuk. Bu, sağlığın bir sebep olduğunu destekliyor ama kesinleştirmiyor, çünkü sinyal ülkelerin 1940'ta ne kadar hasta olduğundan geliyor.*

*Türkiye'nin sağlık saati 1965'te, doğurganlık saati 1982'de döndü. Nüfusu büyük ihtimalle 2047'de zirve yapacak; 2100 için bir aralık gösteriyoruz: 26 ile 125 milyon.*

*Sınırlarımız: Bunlar ülke örüntüleri, tek tek kadınlar hakkında gerçekler değil; ve saat bir yarış değil.*

**Slayt 4'ün üzerindeki yazılar (okunmayacak):**

| Yer | İngilizce (slaytta) | Türkçesi |
|---|---|---|
| Üst yazı · başlık | 4 · One more question · **Where medicines saved more lives, fertility later fell further** | 4 · Bir soru daha · **İlaçların daha çok hayat kurtardığı yerlerde doğurganlık sonra daha çok düştü** |
| Alt başlık | Q4 Is health a cause? A natural experiment in 50 countries · then Türkiye and our limits | Q4 Sağlık bir sebep mi? 50 ülkede bir doğal deney · ardından Türkiye ve sınırlarımız |
| Grafik kartı | Q4 · The 1940s medicines as a natural experiment | Q4 · Doğal deney olarak 1940'ların ilaçları |
| Grafik ekseni | x: deaths per 1,000 people a year that the 1940s medicines could prevent (13 diseases) · y: change in children per woman, 1950→1990 | x: 1940'ların ilaç ve aşılarının önleyebileceği yıllık ölüm (1.000 kişide, 13 hastalık) · y: 1950→1990 kadın başına çocuk değişimi |
| Grafik altı | About 10% more life expectancy (1940–80) → 0.44 fewer children per woman by 1990 (95% CI 0.18–0.69, first stage F = 43) · yet total births rose | Yaşam beklentisi ~%10 daha fazla artınca (1940–80) → 1990'a kadar kadın başına 0,44 daha az çocuk (%95 GA 0,18–0,69, 1. aşama F = 43) · yine de toplam doğum arttı |
| Üç test | ✗ Timing · F < 1 · ✗ HIV shock · p = 0.40 · ✓ Fertility fall | ✗ Zamanlama (dönüm yılı) · F < 1 · ✗ HIV şoku · p = 0,40 · ✓ Doğurganlık düşüşü |
| Türkiye kartı | Türkiye: health 1965 → fertility 1982 · At its turn, richer than 45 of 66 countries, with less schooling than 54 · peak 2047 at 91 M; for 2100, a range (26–125 M) | Türkiye: sağlık 1965 → doğurganlık 1982 · Dönüm anında 66 ülkenin 45'inden zengin, ama 54'ünden az eğitimli · zirve 2047'de 91 milyon; 2100 için bir aralık (26–125 milyon) |
| What we do not claim | A settled cause · Individual-level facts · Observed UN figures · Independent UN series · Projections as forecasts · That ahead is better | Kesinleşmiş bir sebep · Bireyler hakkında gerçekler · UN rakamlarının gözlem olduğu · UN serilerinin birbirinden bağımsız olduğu · Projeksiyonların kehanet olduğu · Önde olmanın daha iyi olduğu |
| Dipnot | Natural experiment: Kreitmeir & Überfuhr (2024) instrument, after Acemoglu & Johnson (2007) · two-stage least squares, weak-IV-robust 95% CI · Each test's plan was committed before its results · HIV: World Bank (UNAIDS) · Türkiye: UN WPP 2024 intervals · ASA Ethical Guidelines (2022) | Doğal deney: Kreitmeir & Überfuhr (2024) aracı, Acemoglu & Johnson (2007) temelli · iki aşamalı en küçük kareler, zayıf araca dayanıklı %95 aralık · Her testin planı sonuçlarından önce kaydedildi · HIV: Dünya Bankası (UNAIDS) · Türkiye: UN WPP 2024 aralıkları · ASA Etik İlkeleri (2022) |

## Kaynakça · Kapanış (yaklaşık 15 sn)

> Same path, different time zones: the clock shows where each country stands, not where it should be. Our next question: what starts the health clock? Sources and our use of an AI assistant are listed here. Thank you.

*Aynı yol, farklı saat dilimleri: Saat, her ülkenin nerede durduğunu gösterir, nerede olması gerektiğini değil. Sıradaki sorumuz: Sağlık saatini ne başlatıyor? Kaynaklar ve yapay zekâ asistanını nasıl kullandığımız burada yazılı. Teşekkürler.*

---

## Kaynakça slaytının tam metni (İngilizce slaytta, Türkçesi anlamak için)

Değiştirmek istediğin satırı işaretle ya da yeni halini yaz. 21 Ekim: Q4 için 4 kaynak eklendi; yer açmak için dergi adları kısaltıldı ve iki satır birleştirildi.

**Sol sütun: References / Kaynakça**

| # | İngilizce (slaytta) | Türkçesi |
|---|---|---|
| 1 | United Nations, DESA, Population Division (2024). *World Population Prospects 2024*: Medium variant, probabilistic variants and supplement. | Birleşmiş Milletler Nüfus Bölümü (2024). *Dünya Nüfus Beklentileri 2024*: Orta varyant, olasılıksal varyantlar ve ek dosya. |
| 2 | Bolt, J. & van Zanden, J. L. (2025). Maddison-style estimates of the evolution of the world economy: A new 2023 update. *J. Economic Surveys*, 39(2), 631–671. Data via Our World in Data (CC BY 4.0). | Bolt ve van Zanden (2025). Maddison tarzı dünya ekonomisi tahminleri, 2023 güncellemesi. Veri Our World in Data üzerinden (CC BY 4.0). |
| 3 | Barro, R. & Lee, J.-W. (2013). A new data set of educational attainment in the world, 1950–2010. *J. Development Economics*, 104, 184–198. Data: v3. | Barro ve Lee (2013). Dünyada eğitim düzeyine dair yeni bir veri seti, 1950–2010. Veri: 3. sürüm. |
| 4 | Cole, T. J., Donaldson, M. D. C. & Ben-Shlomo, Y. (2010). SITAR: a useful instrument for growth curve analysis. *Int. J. Epidemiology*, 39(6), 1558–1566. | Cole, Donaldson ve Ben-Shlomo (2010). SITAR: büyüme eğrisi analizi için kullanışlı bir araç. (Ortak eğri fikrini buradan aldık.) |
| 5 | Acemoglu, D. & Johnson, S. (2007). Disease and development: The effect of life expectancy on economic growth. *J. Political Economy*, 115(6), 925–985. | Acemoglu ve Johnson (2007). Hastalık ve kalkınma: yaşam beklentisinin ekonomik büyümeye etkisi. ("Tahmini ölüm" aracını icat eden makale.) |
| 6 | Bloom, D. E., Canning, D. & Fink, G. (2014). Disease and development revisited. *J. Political Economy*, 122(6), 1355–1366. | Bloom, Canning ve Fink (2014). Hastalık ve kalkınma yeniden. (Başlangıç sağlığı eleştirisi; bizim "kesinleştirmiyor" dememizin sebebi.) |
| 7 | Kreitmeir, D. & Überfuhr, T. (2024). Disease and development – The predicted mortality instrument revisited. *J. Applied Econometrics*, 39(2), 327–337. Data: ZBW Journal Data Archive (CC BY 4.0). | Kreitmeir ve Überfuhr (2024). Tahmini ölüm aracı yeniden. (Kullandığımız yenilenmiş araç ve verisi.) |
| 8 | World Bank, World Development Indicators: HIV prevalence, ages 15–49 (UNAIDS estimates). | Dünya Bankası, Dünya Kalkınma Göstergeleri: 15–49 yaş HIV yaygınlığı (UNAIDS tahminleri). |
| 9 | American Statistical Association (2022). *Ethical Guidelines for Statistical Practice*. · Natural Earth (public domain), via world-atlas 2.0.2: map borders. | Amerikan İstatistik Derneği (2022), *İstatistik Uygulamaları için Etik İlkeler* · Natural Earth (kamu malı): harita sınırları. |

**Sağ sütun**

| Bölüm | İngilizce (slaytta) | Türkçesi |
|---|---|---|
| Reproducibility / Tekrarlanabilirlik | Python 3.13 (pandas, NumPy, SciPy, statsmodels, Matplotlib). Notebooks 01–06 and the scripts in pilot/ and kesif/ reproduce every number and figure; each test's plan was committed before its results. excluded_places.csv names every place left out, with the reason. Code: private GitHub repository, made public after the competition. | 01–06 notebook'ları ile pilot/ ve kesif/ klasörlerindeki programlar her sayıyı ve grafiği yeniden üretir; her testin planı sonuçlarından önce kaydedildi. excluded_places.csv dışarıda bırakılan her yeri sebebiyle listeler. Kod: özel (gizli) GitHub deposu, yarışmadan sonra herkese açılacak. *(Kural gereği jüriye de link verilmiyor.)* |
| Use of AI / Yapay zekâ kullanımı | We used an AI assistant as a working tool: to write analysis code, propose and test methods, design the figures and draft the slides and narration. The team chose the questions, made the final decisions, reviewed and edited the AI-written code, and re-ran all of it before submission to confirm that every number reproduces. | Yapay zekâ asistanını bir çalışma aracı olarak kullandık: analiz kodunu yazmak, yöntem önermek ve test etmek, grafikleri tasarlamak, slaytların ve konuşma metninin taslağını hazırlamak için. Soruları ekip seçti, son kararları ekip verdi, yapay zekânın yazdığı kodu gözden geçirip düzenledi ve teslimden önce hepsini yeniden çalıştırarak her sayının aynı çıktığını doğruladı. *(⚠️ Teslimden ÖNCE doğru olmalı: (1) ekip AI kodunu gerçekten düzenlemiş olmalı, (2) 01–06 + pilot/ + kesif/d_neden, e_hiv, f_kreitmeir programları baştan çalıştırılıp sayılar aynı çıkmış olmalı. Araç adı sözlü sorulursa: "Claude, by Anthropic".)* |
| Kapanış (büyük yazı) | **Same path, different time zones.** The clock shows where a country stands on the path, not where it should be. | **Aynı yol, farklı saat dilimleri.** Saat, bir ülkenin yolda nerede durduğunu gösterir, nerede olması gerektiğini değil. |

## "What it means" bantları (slaytta yazılı, okunmayacak)

| Slayt | İngilizce (slaytta) | Türkçesi |
|---|---|---|
| 1 | The world is moving to small families, but not in step: in 2023 half the countries were below replacement while some still averaged six children. So we ask **when** each country changes, and what goes with that moment. | Dünya küçük ailelere doğru gidiyor ama aynı adımla değil: 2023'te ülkelerin yarısı yenilenme düzeyinin altındaydı, bazılarında ise ortalama hâlâ altı çocuktu. Bu yüzden her ülkenin **ne zaman** değiştiğini ve o anda nelerin bir arada olduğunu soruyoruz. |
| 2 | Countries differ mainly in **when** they turn, not how: given its own clock, one curve fits 94%, and regions differ clearly in timing (p < 0.001). A later clock is not a worse country. | Ülkeler esas olarak **ne zaman** döndüklerinde farklılaşıyor, nasıl döndüklerinde değil: Her ülkeye kendi saati verilince tek eğri %94 uyuyor ve bölgelerin zamanlaması açıkça farklı (p < 0,001). Saati geride olan ülke daha kötü bir ülke değil. |
| 3 | No wealth threshold sets the clock. Health moves with it: in 94% of countries, life expectancy rose fastest first, a median 18 years earlier. These are patterns, not causes. | Saati kuran bir zenginlik eşiği yok. Saatle birlikte yürüyen şey sağlık: Ülkelerin %94'ünde yaşam beklentisi önce en hızlı yükselişini yaptı, medyan 18 yıl önce. Bunlar örüntü, neden değil. |
| 4 | Where the 1940s medicines saved more lives, births first rose, but children per woman fell further by 1990. One of three tests, each planned in advance, supports health as a cause; none settles it. | 1940'lardaki ilaçların daha çok hayat kurtardığı yerlerde doğumlar önce arttı, ama kadın başına çocuk sayısı 1990'a kadar daha çok düştü. Her biri önceden planlanmış üç testten biri sağlığın bir sebep olduğunu destekliyor; hiçbiri kesin sonuç vermiyor. |

## Jüri sorarsa

### Q4 (doğal deney) soruları (21 Ekim)

- **"Doğal deney ne demek? Araç değişken (*instrumental variable*) ne?"** Sağlığı, ülkenin kalkınmasından bağımsız bir sebeple değiştiren bir olay. 1940'larda penisilin, streptomisin, DDT ve aşılar dünyaya aynı anda geldi. Bir ülke 1940'ta bu hastalıklardan ne kadar çok ölüyorsa, o kadar çok kazandı. Bu "şans" payını araç olarak kullanıp iki aşamada tahmin ettik: önce araç → yaşam beklentisi artışı (F = 43, güçlü), sonra tahmin edilen artış → doğurganlık düşüşü.
  - EN: *"A natural experiment is a shock to health that does not come from a country's own development. The 1940s medicines arrived everywhere at once; countries whose deaths came from those diseases gained most."*
- **"Neden 'kanıtladık' demiyorsunuz?"** Çünkü 1940'taki başlangıç sağlığını (F 2,2) ya da 1950 doğurganlığını (F 7,5) sabit tuttuğumuzda araç zayıflıyor. Yani sinyal büyük ölçüde "1940'ta kim daha hastaydı" farkından geliyor ve bu da kalkınmayla karışabilir. Literatürde de tartışma bu: Bloom, Canning & Fink (2014) ve Acemoglu & Johnson'ın cevabı.
  - EN: *"Because once we hold 1940 health fixed, the instrument becomes weak. The signal comes from how sick countries were in 1940, which may also reflect development. That is the open debate in the literature."*
- **"Deneye deneye mi buldunuz?"** Hayır. Üç test yaptık, her birinin planı sonuçtan önce projenin sürüm geçmişine (git) kaydedildi ve saat damgalı. İkisi sonuç vermedi, onları da raporluyoruz. Üç deneme için Bonferroni düzeltmesiyle bile ana test anlamlı (p = 0,001 × 3 = 0,003).
  - EN: *"We ran three tests and wrote each plan down, with a timestamp, before seeing its results. Two failed and we report them. Even corrected for three tries, the main result holds."*
- **"Toplam doğum hem artıp hem nasıl azalıyor?"** Toplam doğum = kadın sayısı × kadın başına doğum. Sağlık iyileşince çok daha fazla kız çocuğu hayatta kalıp anne oldu, bu yüzden toplam doğum arttı (Kreitmeir & Überfuhr'un da bulgusu, biz tekrar ettik: +2,33). Ama her kadın daha az çocuk yaptı (−4,37). Demografik dönüşümün kendisi: önce nüfus patlaması, sonra küçülen aileler.
- **"Türkiye neden bu grafikte yok?"** Türkiye'nin 1940 için ülke düzeyinde hastalık verisi yok. Kasaba verisiyle tamamlanan sürümde (69 ülke) Türkiye var ve sonuç aynı yönde (β −2,91), ama o sürümde aralık 0'ı içeriyor ve yazarlar o sürümlerde ön-eğilim (*pre-trend*) buldu. Bu yüzden ana test, yazarların tercih ettiği ülke düzeyi sürüm.
- **"Neden 1950→1990?"** WPP 1950'de başlıyor. Q3'e göre doğurganlık sağlıktan ~18 yıl sonra dönüyor, şok 1940'larda geldi. Pencere 1980'de bitince etki küçük, 2000'de bitince daha büyük (−2,19 / −4,37 / −5,64). Bu, gecikmeyle tutarlı.
- **"HIV testi neden sonuç vermedi?"** Sağlık şoku oldu (yaşam beklentisi −5,7 yıla karşı +5,8 yıl), ama HIV doğurganlığı biyolojik olarak da düşürüyor; iki etki birbirini götürebilir. Ülke sayısı da az (8'e karşı 9). Ön kayıttaki kurala göre "ayırt edilemedi".
- **"İlk test (Acemoglu–Johnson, dönüm yılı) neden başarısız?"** Araç, sağlığın **ne kadar** düzeldiğini tahmin etmek için kurulmuş, **ne zaman** düzeldiğini değil. Dönüm yılını sorunca iki veride de zayıf kaldı (F 0,8 ve 0,9). Ayrıca sadece 25 ülke vardı.
- **"Kreitmeir verisini nereden aldınız?"** Dergi arşivi (ZBW) 21 Ekim'de erişilemiyordu. Dosyalar İnternet Arşivi'nin 2024 kopyasından indirildi; boyutları arşiv kaydıyla birebir aynı ve makaledeki 1. aşama katsayısını (−0,399) aynen tekrar ettik (`data_dis/KAYNAKLAR.md`).
- **"Q3 ile Q4 nasıl bağlanıyor?"** Q3: sağlık önce dönüyor (sıra ve birliktelik). Q4: sağlığa dışarıdan gelen bir şok, doğurganlığı sonradan daha çok düşürüyor (sebep yönünü destekliyor). Horoz örneği ikisinin arasındaki köprü.

### Önceki sorular

- **"Kruskal–Wallis neden?"** Dönüm yılları normal dağılmıyor ve gruplar küçük (Avrupa'da sadece 4 ülkenin dönüm noktası veride görülüyor). Bu yüzden ortalama yerine sıraları karşılaştıran parametrik olmayan bir test seçtik. İkili karşılaştırmalarda Mann–Whitney kullandık ve çoklu test için Holm düzeltmesi yaptık. Fark esas olarak Afrika ile diğer bölgeler arasında.
- **"Haritadaki taralı ülkeler ne?"** Dönüm noktası veride görülmeyen, modelle çıkarılan ülkeler (85 ülke). Örneğin Avrupa 1950'den önce dönmüştü, Afrika'nın çoğu ise yeni dönüyor. Bunu gizlemek yerine gösteriyoruz.
- **⚠️ UNUTMA, "40 yıl" karışıklığı.** Slayt 2'deki "Türkiye passed it about forty years ago" cümlesi, Türkiye'nin **kendi** dönüm yılından (1982) 2023'e geçen süre. Japonya'yla ilgisi yok. Jüri "Türkiye Japonya'nın 40 yıl gerisinde mi?" diye karıştırırsa üç ayrı ölçüyü söyle:
  1. TFR'nin 2,1'in altına inişine göre: Japonya 1957, Türkiye 2017 → **60 yıl**.
  2. 4 göstergeli ikize göre (TFR, LEx, log IMR, medyan yaş): Türkiye 2023 ≈ Japonya 1980 → **≈ 40 yıl**. İspanya 1987 / Fransa 1988 / İtalya 1984 ile de 35–39 yıl, yani sonuç tek ülkeye bağlı değil.
  3. Dönüm yıllarının farkına göre: 1982 − 1935 → **≈ 47 yıl** (Japonya'nınki 1950 öncesi, çıkarımla, aralık 1930–1946).
  - Kısa cevap (EN): *"'Forty years past its turning point' is Türkiye's own clock, not a gap to Japan. The gap to Japan depends on the yardstick: 60 years on the 2.1 line, about 40 on a four-indicator profile."*
- **"'Sağlık önce gelir' sonucu mekanik değil mi?"** Kısmen olabilir: Kayıt sistemi zayıf ülkelerde UN ölümü ve doğurganlığı aynı anketlerden tahmin ediyor, bu ilişkiyi biraz şişirebilir (Slayt 4'te "Independent UN series" iddia etmiyoruz). Ama ilişki bölge içinde de sürüyor (ρ = 0,71) ve teorinin önceden yaptığı bir tahmin; sonradan uydurulmadı (14 Ekim'den beri planımızdaydı). Q4'teki doğal deney ise Kreitmeir'in 1940 hastalık verisini kullanıyor, UN'in tahminlerinden bağımsız.
- **"Neden yaşam beklentisi, neden bebek ölümü değil?"** Yaşam beklentisi yaş yapısından bağımsız; kaba ölüm hızı ise yaş yapısına, o da doğurganlığa bağlı. Bebek ölümüyle de benzer sonuç çıkıyor (`kesif/a_wpp/SONUC.md`).
- **"Kaç şey denediniz?"** Korelasyon taramasında üç ayrı aramada yaklaşık 960 test; hepsine çoklu test düzeltmesi (Benjamini–Hochberg) ve dönüm yıllarını karıştırarak şans kalibrasyonu. En güçlü gerçek sonuç (ρ = 0,77) şansla çıkabilecek en iyi değerin (≈ 0,58) çok üstünde (`kesif/OZET.md`). Sebep için ayrıca 3 ön kayıtlı test (yukarıda).
- **"Aradaki 18 yıl sabit mi?"** Hayır. Çeyrekler arası 10–26 yıl.
- **"Kapaktaki beyaz bant ne?"** Sağlık saati: her ülkenin yaşam beklentisinin en hızlı yükseldiği yıl (aynı ortak eğri yöntemiyle). Bant, o yıllarda kaç ülkenin sağlık saatinin döndüğünü gösteriyor; dış noktalar doğurganlık saati. Ok iki saatin ortancaları arasındaki farkı gösteriyor (≈ 18 yıl, 115 ülke). Beyaz halkalar Türkiye (sağlık 1965 → doğurganlık 1982).
- **"Sağlık harcamaları?"** That is a natural next question. Health spending data start only in 2000, after most countries had already turned, so we could not test it fairly. (Türkçesi: Harcama verisi 2000'de başlıyor, çoğu ülke o zamana kadar dönmüştü; adil test edemedik.)
- **"Animasyon PDF'te oynar mı?"** Oynamaz, ama ilk karesi bilerek son sahne yapıldı. Böylece PDF'te de ana bulgu (tek eğri, %94) görünüyor.

## Sayıların kaynağı (kontrol için)

| Sayı | Nereden? |
|---|---|
| Kore 0,72 / Nijer 6,06 (2023) | `clean/countries_1950_2100.csv`, `sunum/slayt_uret.py` otomatik çekiyor |
| 3 → 47 → 103 → 187 ülke, medyan 6,0 / 3,6 / 2,0 / 1,7 | `pilot/slayt_koyu.py` (histogram) |
| Korelasyonlar (−0,82, −0,87, −0,91) | `pilot/slayt_koyu.py` (ısı haritası, 2023, 200 ülke) |
| 555 / 362,9 milyar / 237 / 8,09 milyar / 200 / %99,98 / 112 (%69) / 66 (%67) | 01, 02, 04, 05 notebook'ları |
| R² 0,27 / 0,60 / 0,87 / 0,94 / 0,99, 16 ülke sınırda, backtest tablosu | 04_demografik_saat + ek hesap (ülke ortalaması 0,602, ayrı eğri 0,988) |
| Kruskal–Wallis p = 0,00005, ikili Holm p'leri | `pilot/harita_test.py` → `outputs/bolge_testleri.csv` |
| 66 ülke, 1.100 $ / 24.000 $, 1,34 [1,09–1,67], 14 / 9,5 / 9,5 yıl, p'ler | 05_para_mi_okul_mu |
| Türkiye 1982, 45/66, 54/66, zirve 2047 91 M, 2100 26–125 M | 05 notebook'u, `clean/`, OtherVariants dosyası |
| Saat ≈ 40 / ≈ 90 / dönüm noktasında | animasyon (10'a yuvarlanmış) |
| Q3: %94, medyan 18 yıl, ρ 0,77 (bölge içi 0,71), Türkiye sağlık 1965 / doğurganlık 1982 | `pilot/saglik_saati.py` → `clean/saglik_saati.csv` (115 ülke) |
| Hata 12 → 6 yıl (LOO) | `kesif/a_wpp/loo_top3.csv` |
| Gelir katkısı yok (p = 0,84, 64 ülke) | Claude'un ek kontrolü, `kesif/OZET.md` |
| Q4: 50 ülke, F = 43, β −4,37 → %10'da 0,44 çocuk, %95 GA 0,18–0,69, toplam doğum +2,33 | `kesif/f_kreitmeir/ku_testi.py` → `sonuc.csv`, `log.txt` (ön kayıt commit 52407d4) |
| Q4: başlangıç sağlığı sabitken F 2,2, 1950 TFR sabitken F 7,5 | `sonuc.csv` (D4), `log_sonradan.txt` (sonradan, kanıt değil) |
| Test 1: F 0,8 (25 ülke) | `kesif/d_neden/` (ön kayıt commit ef38cd2) |
| Test 2: HIV p = 0,40, yaşam beklentisi −5,7 / +5,8 | `kesif/e_hiv/log.txt` (ön kayıt commit bbedcc9) |
| Grafik: 1.000 kişide önlenebilir ölüm (araç × −10), eğim −0,225 | `pilot/neden_grafigi.py` → `outputs/v3_s4_cause.png` |
