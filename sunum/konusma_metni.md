# Konuşma metni: The Demographic Clock (FİNAL koyu sunum, 21 Ekim)

- **Sunum (yeni link):** https://claude.ai/artifact/MEYv3jt4EcXwixohtjvXd4 · eski sunumlar aynen duruyor.
- **Uzunluk:** 621 kelime (21 Ekim, horoz örneği ve Q2 "hayır bir sonuçtur" cümlesi eklendi). Dakikada 130 kelimeyle yaklaşık 4,7 dakika, animasyon ve duraklamalarla yaklaşık 5,0 dakika, yani sınırda. Sınır 5 dakika. Provada 5:00'ı geçerse ilk kısaltılacak yer: Slayt 2'deki "a level shift with the same number of parameters reaches only 87" (−12 kelime).
- **21 Ekim, horoz örneği:** Slayt 3'e "But first is not the same as cause: a rooster crows before every sunrise…" eklendi. Yer açmak için Slayt 3'ün ilk cümlesi ve tarama cümlesi kısaldı. Slayt 4'teki "16 years" → "17 years" düzeltildi (1982 − 1965). Sunumdaki slayt notlarına HENÜZ işlenmedi. Eski hal: `sunum/eski_surumler/konusma_metni_horoz_oncesi.md`.
- **21 Ekim değişiklikleri:** Q3 ("Health first?") eklendi; Slayt 3 artık "What moves with the clock?" (Q2 kısaldı, Q3 ana grafik). Kapak isim sırası: Yazel, Elif, Zehra, Rojbin. Slayt 1 bandı "So we ask when…" oldu. Yapay zekâ beyanı Sürüm 2. Kapanışa "Our next question: what starts the health clock?" eklendi (arkadaşının fikri). Eski hal: `sunum/eski_surumler/konusma_metni_q3_oncesi.md`.
- **Dil:** Her bölümde önce okunacak İngilizce metin, altında Türkçe karşılığı var. Türkçe kısım sadece anlamak içindir, okunmayacak.
- **"What it means" bantları:** Her içerik slaytının altında sarı çerçeveli bir yorum bandı var. Bantlar okunmayacak; jüri slaytı tek başına okurken anlamı onlardan görür. Metinleri ve Türkçe karşılıkları en altta.
- **Kontrol listesi:** Sayılar doğru mu? Cümleler sana doğal geliyor mu? Takıldığın kelime var mı? Değiştirmek istediğin yeri işaretle.

---

## Kapak (yaklaşık 15 sn)

> Hello, we are Stat4Sight from Kırıkkale University. Every country is moving from large families to small ones. Our project asks three things: is it the same journey everywhere, does money or school set its timing, and does health come first?

*Merhaba, biz Kırıkkale Üniversitesi'nden Stat4Sight takımıyız (okunuşu: "stat for sayt"). Her ülke kalabalık ailelerden küçük ailelere doğru ilerliyor. Projemiz üç şey soruyor: Bu yolculuk her yerde aynı mı, zamanlamasını para mı yoksa okul mu belirliyor, ve sağlık önce mi geliyor?*

## Slayt 1 · Soru ve veri (yaklaşık 55 sn)

> In 2023, women in the Republic of Korea had 0.72 children on average; women in Niger had 6.06. In 1950, only 3 of 200 countries were below replacement; by 2023 it was 103. So we asked: do countries follow the same path, and what moves with their turning point: money, school, or health?
>
> Our data is UN World Population Prospects 2024. Summing every row of the file gives 363 billion people, because regions repeat countries; countries alone give the correct 8.09 billion. We keep the 200 countries above 100,000 people, 99.98 percent of the world, and list every place we leave out. Values after 2023 are UN projections, always drawn dashed.

*2023'te Kore Cumhuriyeti'nde kadın başına ortalama 0,72 çocuk düşüyordu, Nijer'de 6,06. 1950'de 200 ülkenin sadece 3'ü yenilenme düzeyinin altındaydı, 2023'te bu sayı 103 oldu. Bu yüzden sorduk: Ülkeler aynı yolu mu izliyor ve dönüm noktalarıyla birlikte ne yürüyor: para mı, okul mu, sağlık mı?*

*Verimiz UN Dünya Nüfus Beklentileri 2024. Dosyadaki bütün satırları toplayınca 363 milyar insan çıkıyor, çünkü bölgeler ülkeleri tekrar ediyor. Sadece ülkeleri toplayınca doğru sayı olan 8,09 milyar çıkıyor. Nüfusu 100 binin üstündeki 200 ülkeyi tutuyoruz; bu, dünya nüfusunun %99,98'i. Dışarıda bıraktığımız her yeri listeliyoruz. 2023 sonrası değerler UN projeksiyonu, hep kesikli çiziyoruz.*

## Slayt 2 · Demografik Saat (yaklaşık 65 sn + animasyon)

> Our first try fitted an S-shaped curve to each country separately. It fit, but gave nonsense: for Japan, whose decline happened before 1950, it said women started at nine children.
>
> So we borrowed the SITAR idea from children’s growth charts: one shared S-curve, and one number per country — its turning point, the year fertility falls fastest. Watch what happens when we shift each country.
>
> *(Burada animasyonun oynamasını bekle.)*
>
> By calendar year, time explains 27 percent of the differences between countries. Shifted to their own turning points, one curve explains 94 percent; a level shift with the same number of parameters reaches only 87. In backtests, the shared curve had the smallest typical error twenty years ahead.
>
> On the map, the clock runs from Europe to Africa, and a Kruskal–Wallis test confirms that regions turn at different times. In 2023, Nigeria is at its turning point, Türkiye passed it about forty years ago, Japan about ninety.

*İlk denememizde her ülkeye ayrı bir S eğrisi oturttuk. Eğriler veriye uydu ama saçma sonuçlar verdi: Düşüşü 1950'den önce olan Japonya için "kadınlar 9 çocukla başlamış" dedi.*

*Bu yüzden çocuk büyüme eğrilerinde kullanılan SITAR fikrini ödünç aldık: tek bir ortak S eğrisi ve her ülke için tek bir sayı. Bu sayı ülkenin dönüm noktası, yani doğurganlığın en hızlı düştüğü yıl. Her ülkeyi kaydırınca ne olduğunu izleyin.*

*Takvim yılına göre zaman, ülkeler arasındaki farkların %27'sini açıklıyor. Kendi dönüm noktalarına kaydırınca tek eğri %94'ünü açıklıyor. Aynı sayıda parametreyle düzey kaydırma ise %87'de kalıyor. Geriye dönük testlerde ortak eğri 20 yıl sonrasını tipik olarak en az hatayla tahmin etti.*

*Haritada saat Avrupa'dan Afrika'ya doğru ilerliyor. Kruskal–Wallis testi de bölgelerin farklı zamanlarda döndüğünü doğruluyor. 2023'te Nijerya dönüm noktasında, Türkiye onu yaklaşık 40 yıl önce geçti, Japonya yaklaşık 90 yıl önce.*

## Slayt 3 · Saatle birlikte ne yürüyor? Para, okul, sağlık (yaklaşık 70 sn)

> Our data can show when a country turns, not why, so we checked what lines up with that moment.
>
> First, money or school. In 66 countries, income at the turning point ranged from 1,100 to 24,000 dollars. As a threshold it missed the year by 14 years, worse than guessing the typical year. Schooling was steadier, but no better than the calendar.
>
> That no is a result, not a failure, and it led us to the oldest prediction of transition theory: does health come first? We measured a second clock, the year life expectancy rose fastest, with the same shared curve. In 94 percent of 115 countries it came first, a median of 18 years earlier, and the two clocks move together, rho 0.77. We screened many candidates, with multiple-test correction.
>
> But first is not the same as cause: a rooster crows before every sunrise, yet it does not make the sun rise. So money does not set the clock; health moves with it.

*Verimiz bir ülkenin ne zaman döndüğünü gösterebiliyor, nedenini değil. Bu yüzden o anla neyin örtüştüğüne baktık.*

*Önce para mı, okul mu. 66 ülkede dönüm noktasındaki gelir 1.100 ile 24.000 dolar arasında değişiyordu. Eşik olarak kullanılınca yılı 14 yıl şaşırdı; bu, tipik yılı tahmin etmekten bile kötü. Eğitim daha istikrarlıydı, ama takvimden daha iyi değildi.*

*Bu "hayır" bir başarısızlık değil, bir sonuç; ve bizi demografik dönüşüm teorisinin en eski tahminine götürdü: Sağlık önce mi geliyor? İkinci bir saat ölçtük: yaşam beklentisinin en hızlı yükseldiği yıl, aynı ortak eğri yöntemiyle. 115 ülkenin %94'ünde bu saat önce döndü, medyan 18 yıl önce; iki saat birlikte yürüyor, rho 0,77. Birçok aday değişkeni çoklu test düzeltmesiyle taradık.*

*Ama önce gelmek, sebep olmak demek değil: Horoz her sabah güneş doğmadan önce öter, ama güneşi o doğurmaz. Yani saati para kurmuyor; saatle birlikte yürüyen şey sağlık.*

> ℹ️ **Bilgi notu (slaytta yok, okunması zorunlu değil; jüri sorarsa ya da süre kalırsa):** As a robustness check, a pre-registered random forest using 1950 income, schooling and geography did not beat the calendar, while simpler linear models did by about two years, mainly through young women's schooling in 1950. Income never helped, so money does not set the clock, and schooling matters as a starting point rather than a threshold.

*Türkçesi: Sağlamlık kontrolü olarak, 1950'deki gelir, eğitim ve coğrafyayı kullanan, önceden kaydedilmiş bir random forest modeli takvimi geçemedi; daha basit doğrusal modeller ise yaklaşık iki yıl farkla geçti ve bu kazanç esas olarak 1950'deki genç kadın eğitiminden geldi. Gelir hiç yardımcı olmadı; yani saati para kurmuyor, okul ise bir eşik olarak değil, bir başlangıç noktası olarak önem taşıyor. (Kaynak: `pilot/ml_kontrol_plan.md`. Okunursa +≈20 sn, süre 5:00'ı aşar.)*

## Slayt 4 · Türkiye, sınırlar ve etik (yaklaşık 50 sn)

> Türkiye turned around 1982, about 17 years after its health clock. It was richer than 45 of these 66 countries at their turning points, but its young women had less schooling than 54 of them.
>
> The UN projects Türkiye’s population to peak in 2047 at 91 million. By 2100 its 95 percent interval runs from 26 to 125 million, so we show a range, not a number.
>
> Our limits: these patterns say nothing about individual women. Where registration is weak, UN figures are model estimates, and health and fertility may come from the same surveys. And the clock is not a race: being further along is not better.

*Türkiye 1982 civarında döndü, sağlık saatinden yaklaşık 17 yıl sonra. O anda bu 66 ülkenin 45'inden daha zengindi, ama genç kadınlarının eğitimi 54'ünden daha düşüktü.*

*UN, Türkiye nüfusunun 2047'de 91 milyonla zirve yapacağını öngörüyor. 2100 için %95 aralığı 26 ile 125 milyon arası. Bu yüzden tek bir sayı değil, bir aralık gösteriyoruz.*

*Sınırlarımız: Bu örüntüler tek tek kadınlar hakkında bir şey söylemiyor. Kayıt sisteminin zayıf olduğu yerlerde UN rakamları modelle üretilmiş tahminler ve sağlık ile doğurganlık aynı anketlerden gelebiliyor. Ve saat bir yarış değil: Yolda daha ileride olmak daha iyi olmak demek değil.*

## Kaynakça · Kapanış (yaklaşık 15 sn)

> Same path, different time zones. The clock shows where each country stands on the path, not where it should be. Our next question: what starts the health clock? Our code and data sources are listed here, and we used an AI assistant as described. Thank you.

*Aynı yol, farklı saat dilimleri. Saat, her ülkenin yolda nerede durduğunu gösterir, nerede olması gerektiğini değil. Sıradaki sorumuz: Sağlık saatini ne başlatıyor? Kodumuz ve veri kaynaklarımız burada listeli. Yapay zekâ asistanını anlatıldığı şekilde kullandık. Teşekkürler.*

---

## Kaynakça slaytının tam metni (İngilizce slaytta, Türkçesi anlamak için)

Değiştirmek istediğin satırı işaretle ya da yeni halini yaz. ✅ 21 Ekim: Yapay zekâ beyanı Sürüm 2 FİNAL sunumda. Q3 için yeni kaynak gerekmedi (yaşam beklentisi WPP'den).

**Sol sütun: References / Kaynakça**

| # | İngilizce (slaytta) | Türkçesi |
|---|---|---|
| 1 | United Nations, DESA, Population Division (2024). *World Population Prospects 2024*: Medium variant, probabilistic variants and supplement. | Birleşmiş Milletler, Ekonomik ve Sosyal İşler Dairesi, Nüfus Bölümü (2024). *Dünya Nüfus Beklentileri 2024*: Orta varyant, olasılıksal varyantlar ve ek dosya. |
| 2 | Bolt, J. & van Zanden, J. L. (2025). Maddison-style estimates of the evolution of the world economy: A new 2023 update. *Journal of Economic Surveys*, 39(2), 631–671. Data: Maddison Project Database 2023. | Bolt ve van Zanden (2025). Dünya ekonomisinin gelişimine dair Maddison tarzı tahminler: 2023 güncellemesi. *Journal of Economic Surveys* dergisi. Veri: Maddison Projesi Veritabanı 2023 (kişi başı gelir). |
| 3 | Barro, R. & Lee, J.-W. (2013). A new data set of educational attainment in the world, 1950–2010. *Journal of Development Economics*, 104, 184–198. Data: version 3 (2021 update). | Barro ve Lee (2013). Dünyada eğitim düzeyine dair yeni bir veri seti, 1950–2010. *Journal of Development Economics* dergisi. Veri: 3. sürüm (2021 güncellemesi). |
| 4 | Cole, T. J., Donaldson, M. D. C. & Ben-Shlomo, Y. (2010). SITAR: a useful instrument for growth curve analysis. *International Journal of Epidemiology*, 39(6), 1558–1566. | Cole, Donaldson ve Ben-Shlomo (2010). SITAR: büyüme eğrisi analizi için kullanışlı bir araç. *International Journal of Epidemiology* dergisi. (Ortak eğri fikrini buradan aldık.) |
| 5 | American Statistical Association (2022). *Ethical Guidelines for Statistical Practice*. | Amerikan İstatistik Derneği (2022). *İstatistik Uygulamaları için Etik İlkeler*. |
| 6 | Income series downloaded via Our World in Data (CC BY 4.0). | Gelir serisi Our World in Data üzerinden indirildi (CC BY 4.0 lisansı). |
| 7 | Natural Earth (public domain), via world-atlas 2.0.2: country borders for the map. | Natural Earth (kamu malı), world-atlas 2.0.2 üzerinden: haritadaki ülke sınırları. |

**Sağ sütun**

| Bölüm | İngilizce (slaytta) | Türkçesi |
|---|---|---|
| Reproducibility / Tekrarlanabilirlik | Python 3.13 (pandas, NumPy, SciPy, statsmodels, Matplotlib). Notebooks 01–06 and the scripts in pilot/ reproduce every number and figure. excluded_places.csv names every place left out, with the reason. Code: private GitHub repository, made public after the competition. | Python 3.13 (pandas, NumPy, SciPy, statsmodels, Matplotlib). 01–06 notebook'ları ve pilot/ klasöründeki programlar her sayıyı ve grafiği yeniden üretir. excluded_places.csv dışarıda bırakılan her yeri sebebiyle listeler. Kod: özel (gizli) GitHub deposu, yarışmadan sonra herkese açılacak. *(Kural gereği jüriye de link verilmiyor.)* |
| Use of AI / Yapay zekâ kullanımı | We used an AI assistant as a working tool: to write analysis code, propose and test methods, design the figures and draft the slides and narration. The team chose the questions, made the final decisions, reviewed and edited the AI-written code, and re-ran all of it before submission to confirm that every number reproduces. | Yapay zekâ asistanını bir çalışma aracı olarak kullandık: analiz kodunu yazmak, yöntem önermek ve test etmek, grafikleri tasarlamak, slaytların ve konuşma metninin taslağını hazırlamak için. Soruları ekip seçti, son kararları ekip verdi, yapay zekânın yazdığı kodu gözden geçirip düzenledi ve teslimden önce hepsini yeniden çalıştırarak her sayının aynı çıktığını doğruladı. *(⚠️ Teslimden ÖNCE doğru olmalı: (1) ekip AI kodunu gerçekten düzenlemiş olmalı (grafik yazısı/rengi, yorum satırı ya da 07 notebook'u), (2) 01–06 + pilot/ programları baştan çalıştırılıp sayılar aynı çıkmış olmalı. 18 Ekim taslağı. Eski hali: "We used Claude (Anthropic), an AI assistant, extensively: …". Araç adı sözlü sorulursa söylenecek: "Claude, by Anthropic".)* |
| Kapanış (büyük yazı) | **Same path, different time zones.** The clock shows where a country stands on the path, not where it should be. | **Aynı yol, farklı saat dilimleri.** Saat, bir ülkenin yolda nerede durduğunu gösterir, nerede olması gerektiğini değil. |

## "What it means" bantları (slaytta yazılı, okunmayacak)

| Slayt | İngilizce (slaytta) | Türkçesi |
|---|---|---|
| 1 | The world is moving to small families, but not in step: in 2023 half the countries were below replacement while some still averaged six children. So we ask **when** each country changes, and what goes with that moment. | Dünya küçük ailelere doğru gidiyor ama aynı adımla değil: 2023'te ülkelerin yarısı yenilenme düzeyinin altındaydı, bazılarında ise ortalama hâlâ altı çocuktu. Bu yüzden her ülkenin **ne zaman** değiştiğini ve o anda nelerin bir arada olduğunu soruyoruz. |
| 2 | Countries differ mainly in **when** they turn, not how: given its own clock, one curve fits 94%, and regions differ clearly in timing (p < 0.001). A later clock is not a worse country. | Ülkeler esas olarak **ne zaman** döndüklerinde farklılaşıyor, nasıl döndüklerinde değil: Her ülkeye kendi saati verilince tek eğri %94 uyuyor ve bölgelerin zamanlaması açıkça farklı (p < 0,001). Saati geride olan ülke daha kötü bir ülke değil. |
| 3 | No wealth threshold sets the clock. Health moves with it: in 94% of countries, life expectancy rose fastest first, a median 18 years earlier. These are patterns, not causes. | Saati kuran bir zenginlik eşiği yok. Saatle birlikte yürüyen şey sağlık: Ülkelerin %94'ünde yaşam beklentisi önce en hızlı yükselişini yaptı, medyan 18 yıl önce. Bunlar örüntü, neden değil. |
| 4 | Türkiye's decline began while young women's schooling was still low (3.6 vs a typical 5.5 years). Its population likely peaks near 2047; for 2100, plan with the range (26–125 million), not one number. | Türkiye'nin düşüşü, genç kadınların eğitimi hâlâ düşükken başladı (tipik 5,5 yıla karşı 3,6 yıl). Nüfusu büyük ihtimalle 2047 civarında zirve yapacak; 2100 için tek bir sayıyla değil, aralıkla (26–125 milyon) plan yapılmalı. |

## Jüri sorarsa (yeni eklenenler)

- **"Kruskal–Wallis neden?"** Dönüm yılları normal dağılmıyor ve gruplar küçük (Avrupa'da sadece 4 ülkenin dönüm noktası veride görülüyor). Bu yüzden ortalama yerine sıraları karşılaştıran parametrik olmayan bir test seçtik. İkili karşılaştırmalarda Mann–Whitney kullandık ve çoklu test için Holm düzeltmesi yaptık. Fark esas olarak Afrika ile diğer bölgeler arasında.
- **"Haritadaki taralı ülkeler ne?"** Dönüm noktası veride görülmeyen, modelle çıkarılan ülkeler (85 ülke). Örneğin Avrupa 1950'den önce dönmüştü, Afrika'nın çoğu ise yeni dönüyor. Bunu gizlemek yerine gösteriyoruz.
- **⚠️ UNUTMA, "40 yıl" karışıklığı.** Slayt 2'deki "Türkiye passed it about forty years ago" cümlesi, Türkiye'nin **kendi** dönüm yılından (1982) 2023'e geçen süre. Japonya'yla ilgisi yok. Jüri "Türkiye Japonya'nın 40 yıl gerisinde mi?" diye karıştırırsa üç ayrı ölçüyü söyle:
  1. TFR'nin 2,1'in altına inişine göre: Japonya 1957, Türkiye 2017 → **60 yıl**.
  2. 4 göstergeli ikize göre (TFR, LEx, log IMR, medyan yaş): Türkiye 2023 ≈ Japonya 1980 → **≈ 40 yıl**. İspanya 1987 / Fransa 1988 / İtalya 1984 ile de 35–39 yıl, yani sonuç tek ülkeye bağlı değil.
  3. Dönüm yıllarının farkına göre: 1982 − 1935 → **≈ 47 yıl** (Japonya'nınki 1950 öncesi, çıkarımla, aralık 1930–1946).
  - Kısa cevap (EN): *"'Forty years past its turning point' is Türkiye's own clock, not a gap to Japan. The gap to Japan depends on the yardstick: 60 years on the 2.1 line, about 40 on a four-indicator profile."*
- **"Sağlık önce gelir" sonucu mekanik değil mi?** Kısmen olabilir: Kayıt sistemi zayıf ülkelerde UN ölümü ve doğurganlığı aynı anketlerden tahmin ediyor, bu ilişkiyi biraz şişirebilir (Slayt 4'te "That UN series are independent" diye yazdık). Ama ilişki bölge içinde de sürüyor (ρ = 0,71) ve teorinin önceden yaptığı bir tahmin; sonradan uydurulmadı (14 Ekim'den beri planımızdaydı).
- **"Neden yaşam beklentisi, neden bebek ölümü değil?"** Yaşam beklentisi yaş yapısından bağımsız; kaba ölüm hızı ise yaş yapısına, o da doğurganlığa bağlı. Bebek ölümüyle de benzer sonuç çıkıyor (`kesif/a_wpp/SONUC.md`).
- **"Kaç şey denediniz?"** Üç ayrı aramada yaklaşık 960 test; hepsine çoklu test düzeltmesi (Benjamini–Hochberg) ve dönüm yıllarını karıştırarak şans kalibrasyonu. En güçlü gerçek sonuç (ρ = 0,77) şansla çıkabilecek en iyi değerin (≈ 0,58) çok üstünde (`kesif/OZET.md`).
- **"Aradaki 18 yıl sabit mi?"** Hayır. Çeyrekler arası 10–26 yıl; "A fixed health-to-fertility lag" iddia etmiyoruz.
- **"Kapaktaki beyaz bant ne?"** Sağlık saati: her ülkenin yaşam beklentisinin en hızlı yükseldiği yıl (aynı ortak eğri yöntemiyle). Bant, o yıllarda kaç ülkenin sağlık saatinin döndüğünü gösteriyor; dış noktalar doğurganlık saati. Ok iki saatin ortancaları arasındaki farkı gösteriyor (≈ 18 yıl, 115 ülke). Beyaz halkalar Türkiye (sağlık 1965 → doğurganlık 1982).
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
| Türkiye 1982, 45/66, 54/66, 5 an tablosu, zirve 2047 91 M, 2100 26–125 M | 05 notebook'u, `clean/`, OtherVariants dosyası |
| Saat ≈ 40 / ≈ 90 / dönüm noktasında | animasyon (10'a yuvarlanmış) |
| Q3: %94, medyan 18 yıl, ρ 0,77 (bölge içi 0,71), Türkiye sağlık 1965 / doğurganlık 1982 | `pilot/saglik_saati.py` → `clean/saglik_saati.csv` (115 ülke) |
| Hata 12 → 6 yıl (LOO) | `kesif/a_wpp/loo_top3.csv` |
| Gelir katkısı yok (p = 0,84, 64 ülke) | Claude'un ek kontrolü, `kesif/OZET.md` |
