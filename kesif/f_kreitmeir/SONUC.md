# Sonuç: Yenilenmiş tahmini ölüm aracıyla uzun fark testi (21 Ekim 2026)

Plan: `plan.md` (commit 52407d4, analizden önce). Kod: `ku_testi.py` (ön kayıtlı), `sonradan_kontrol.py` (sonradan, kanıt değil).
Çıktı: `log.txt`, `log_sonradan.txt`, `sonuc.csv`.

## Ana test (ön kayıtlı): DESTEKLİYOR

| | n | F | β (ΔTFR / ΔlnLE) | p | Anderson–Rubin %95 |
|---|---|---|---|---|---|
| **ANA:** ülke düzeyi araç, ΔTFR 1950→1990 | 50 | **42,9** | **−4,37** | 0,001 | **[−6,94; −1,79]** |

- **Çeviri:** 1940–1980 arasında yaşam beklentisi ~%10 daha çok artan ülkede, 1950–1990 arasında kadın başına **0,44 çocuk daha fazla** düşüş.
- Ön kayıttaki kurala göre: F ≥ 10 ve AR aralığı tamamen 0'ın altında → **"Doğal deney, sağlık iyileşmesinin doğurganlık düşüşünü büyüttüğünü destekliyor (50 ülke)."**
- Üç sebep denemesi yapıldığı için Bonferroni ile bile anlamlı (0,001 × 3 = 0,003).

## Ön kayıtlı duyarlılıklar

| | n | F | β | AR %95 | Not |
|---|---|---|---|---|---|
| D1a: pencere 1950→1980 | 50 | 42,9 | −2,19 | [−4,30; 0,08] | Etki daha küçük |
| D1b: pencere 1950→2000 | 50 | 42,9 | −5,64 | [−8,27; −3,07] | Etki büyüyor → gecikmeyle tutarlı (Q3: ~18 yıl) |
| D2: AJ orijinali | 47 | 48,8 | −3,36 | [−6,36; −0,78] | Aynı yön |
| D2: ülke + kasaba (Türkiye dahil) | 63 | 20,6 | −2,91 | [−5,85; 1,44] | Aynı yön, aralık 0'ı içeriyor |
| D2: kasaba yerine | 63 | 29,5 | −3,89 | [−7,23; −1,59] | Aynı yön |
| D2: en yüksek | 63 | 26,3 | −2,86 | [−5,37; 0,69] | Aynı yön, aralık 0'ı içeriyor |
| D3: sadece düşük/orta gelir | 39 | 14,5 | −4,94 | [−10,47; −0,28] | Zengin–yoksul farkına dayanmıyor |
| **D4: + başlangıç sağlığı (ln LE1940)** | 50 | **2,2** | −5,60 | sınırsız | **Araç zayıflıyor** |
| D5: saat tasarımı (t0 ~ t0_saglik) | 23 | 0,9 | 0,72 | sınırsız | 1. denemedeki gibi zayıf |
| D6: veri kontrolü, Δln toplam doğum 1940→80 | 40 | 62,0 | **+2,33** | [1,34; 3,38] | Yazarların bulgusu tekrarlandı |

## Sonradan tanı kontrolleri (ön kayıtta yok, kanıt sayılmaz)

- **S1: + 1950 TFR kontrolü:** F 7,5, β −1,85 (p 0,58). Başlangıç doğurganlığı sabitken de araç zayıflıyor.
- **S2: bir ülke dışarıda:** β −5,58 (Guatemala çıkınca) ile −3,96 (Meksika çıkınca) arasında. Tek ülkeye bağlı değil.
- **S3:** araç, 1940 yaşam beklentisiyle (Spearman +0,62) ve 1950 TFR'siyle (−0,42) güçlü ilişkili.

## Dürüst yorum

1. **Yön Q3 ile aynı ve güçlü:** Yeni ilaç ve aşılardan daha çok kazanan ülkelerde doğurganlık 1990'a kadar daha çok düştü. Etki pencere uzadıkça büyüyor (gecikmeyle tutarlı).
2. **Çarpıcı ikili bulgu:** Aynı sağlık şoku **toplam doğumu artırdı** (D6, daha çok insan hayatta kaldı) ama **kadın başına doğumu azalttı** (ana test). Demografik dönüşümün kendisi: önce nüfus patlaması, sonra küçülen aileler.
3. **Ama karar verici değil:** Aracın gücü büyük ölçüde ülkelerin 1940'ta ne kadar hasta olduğundan geliyor. Başlangıç sağlığı (D4) ya da başlangıç doğurganlığı (S1) sabit tutulunca araç zayıflıyor ve ayıramıyoruz. Bu, literatürdeki açık tartışmanın aynısı (Bloom, Canning & Fink 2014 ve Acemoglu & Johnson'ın cevabı).
4. **Doğru cümle:** "A natural experiment points the same way: where new medicines raised life expectancy more, fertility fell more by 1990. But the signal comes from how sick countries were in 1940, so it supports our story without settling it."
