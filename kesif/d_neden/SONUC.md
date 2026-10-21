# Sonuç: Doğal deney testi (21 Ekim 2026)

Plan: `plan.md` (commit ef38cd2, analizden önce). Kod: `neden_testi.py`. Çıktı: `log.txt`, `sonuc.csv`.

## Ana sonuç: ZAYIF ARAÇ → sebebi ayıramadık (ön kayıttaki 1. satır)

| Model | n | π (1. aşama) | F | indirgenmiş form p | β (2SLS) | Anderson–Rubin %95 |
|---|---|---|---|---|---|---|
| **ANA:** PM40, kontrol LE40 + gelir 1940 | 25 | +5,9 (p 0,37) | **0,8** | 0,51 | yorumlanmaz | sınırsız |
| D1: 47 ülke (çıkarımla saatler dahil) | 47 | +0,3 (p 0,96) | 0,0 | 0,87 | yorumlanmaz | sınırsız |
| D2: dört hastalık endeksi (sıtma + tüberküloz + zatürre + çiçek) | 25 | p 0,26 | 1,3 | 0,41 | yorumlanmaz | sınırsız |
| D3: kontrolsüz | 25 | +21,2 (p 0,002) | 9,2 | 0,022 | 0,79 | [0,11; 2,58] |

- D4 (bir ülkeyi dışarıda bırakma): ana β −7,1 ile 1,6 arasında zıplıyor → tamamen kararsız.
- Dört hastalık endeksi AJ endeksiyle neredeyse aynı (Spearman 0,94), sonuç da aynı.
- Karşılaştırma: düz OLS β = 0,56 (p 0,02), yani birliktelik bu 25 ülkede de var. Sorun birliktelikte değil, sebebi ayırmakta.

## Veri doğru okundu mu? (replikasyon kontrolü)

AJ'nin kendi 1. aşamasını kendi örnekleminde (45 ülke, 1940→1980) tekrar ettik: Δlog yaşam beklentisi ~ Δtahmini ölüm, katsayı −0,17, t = −4,8. Yani araç AJ örnekleminde güçlü, veriyi doğru okuyoruz.

## Neden bizde zayıf?

- AJ'nin örnekleminde güç büyük ölçüde **zengin ve yoksul ülke farkından** geliyor (1940'ta zenginlerin tahmini ölümü düşük, kazançları küçük). Bizim 25 ülke hepsi gelişmekte olan ülke (hiçbiri "başlangıçta zengin" değil); bunların içinde araç sağlığı ayırt edemiyor (PM40 ile 1940→1980 yaşam beklentisi artışı arasında Spearman −0,08).
- Bloom, Canning & Fink (2014) da AJ'ye benzer bir eleştiri yapmıştı.
- **D3 dersi:** Kontrol olmadan sonuç "anlamlı ve sebep gibi" görünüyor (AR aralığı 0'ı dışlıyor). 1940 sağlığı ve geliri eklenince kayboluyor. Yani kontrolsüz sonuç Hikâye 2'yi (kalkınma ikisini de sürüklüyor) yansıtıyor. Kontrol değişkeninin neden şart olduğunun canlı örneği.

## Yorum (ön kayıttaki kurala göre)

> "This natural experiment did not move the health clock enough within our 25 developing countries to separate health from development."

Bu, "sağlık sebep değil" demek DEĞİL; "bu araçla ayıramadık" demek. Q3'ün birliktelik bulgusu aynen geçerli.

## Sonraki seçenekler (yeni test sayılır, her biri ayrı ön kayıtla)

1. **Kreitmeir & Überfuhr (2024)** yeni ülke düzeyi aracı, daha geniş kapsam (sunucu şu an erişilemiyor).
2. **Ters şok:** HIV/AIDS ya da kriz dönemlerinde yaşam beklentisi düşünce doğurganlık düşüşü duraksadı mı (olay çalışması, WPP içinde)?
3. **Ülke içi zaman yapısı:** ülke ve yıl sabit etkili dağıtılmış gecikme modeli (sebep değil, ama kesitsellikten güçlü).
