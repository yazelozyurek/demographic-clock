# ML sağlamlık kontrolü: ön kayıt (pre-registration)

**Yazıldığı an:** 18 Ekim 2026, model çalıştırılmadan ÖNCE. Bu dosya sonuç görüldükten sonra değiştirilmeyecek.
Sonuçlar ayrı bir dosyaya yazılacak (`outputs/ml_kontrol_sonuc.csv`) ve aşağıdaki plana göre yorumlanacak.

## Soru
1950'de ölçülen özelliklerle (66 ülkenin hiçbiri henüz dönmemişken, en erken t0 = 1952)
esnek bir model, bir ülkenin dönüm yılını (t0) "diğer ülkelerin tipik yılı" tahmininden daha iyi tahmin edebilir mi?

Q2 ile ilişkisi: Q2 "dönüm anında gelir/eğitim ortak bir eşik mi?" diye soruyor. Bu kontrol aynı iddiayı başka
bir açıdan sınıyor: "Para, okul ya da coğrafya zamanlamayı söylüyor mu?"

## Örneklem
`clean/para_okul_tablosu.csv` içindeki 66 ülke (Q2 ile aynı). Bir özelliği eksik olan ülke o özellik setinden
çıkarılır ve sayısı raporlanır.

## Özellikler (önceden sabit)
- **Set A (ana):** log kişi başı gelir 1950 (Maddison), genç kadın (25–34) eğitim yılı 1950 (Barro–Lee F2534),
  ekvatora uzaklık (alan ağırlıklı merkezin |enlemi|, `arac/world-50m.json`), bölge (kukla değişken).
- **Set B (ek):** Set A + log bebek ölüm hızı 1950 (WPP). Gerekçe: "önce ölüm, sonra doğurganlık" teorisi.
- Gelir 1950 yoksa 1950–1955 arasındaki ilk dolu yıl kullanılır.

## Modeller
- **Ana model: Random forest** (500 ağaç, min_samples_leaf = 3, random_state = 0). Kullanıcının seçimi, sonuçlar görülmeden önce (18 Ekim).
- Baz: takvim, yani eğitim kümesindeki t0 medyanı.
- İkincil (sadece karşılaştırma için raporlanır): doğrusal regresyon (OLS), LASSO (iç 5 katlı CV, standartlaştırılmış özellikler).

## Doğrulama ve başarı ölçütü
- Bir ülkeyi dışarıda bırakarak çapraz doğrulama (LOO-CV). Her ülkenin tahmini, o ülke hiç görülmeden yapılır.
- Ana ölçü: medyan mutlak hata (yıl), Q2 ile aynı. Ek: ortalama mutlak hata.
- Random forest "takvimi geçti" sayılır, ancak: medyan mutlak hatası daha düşükse VE mutlak hatalar üzerinde eşleştirilmiş
  Wilcoxon testi p < 0,05 ise (2 set = 2 karşılaştırma, Holm düzeltmesi). OLS ve LASSO'nun p-değerleri ayrıca raporlanır,
  karara girmez.
- Özellik önemi (random forest permütasyon önemi) sadece betimsel raporlanır, nedensellik iddiası yapılmaz.

## Önceden yazılmış yorum
- Random forest geçemezse: "Esnek bir model bile para, okul ve coğrafyayla takvimi geçemiyor" → Q2'nin
  "saati para kurmuyor, okul bir zamanlayıcı değil" sonucunu destekler.
- Random forest geçerse: dürüstçe raporlanır, hangi set ve hangi özelliklerle olduğu yazılır. Q2 metni gerekirse
  güncellenir.

---

## Sonuç (18 Ekim, plan yazıldıktan SONRA eklendi)
- **Ana model (random forest), ön kayıtlı ölçüte göre takvimi GEÇEMEDİ.** Set A: 8,5 yıla karşı 9,5 (p = 0,12).
  Set B: 8,1 yıla karşı 9,5 (ham p = 0,035, Holm p = 0,069).
- **İkincil modeller (OLS, LASSO) geçti:** yaklaşık 7,0–7,5 yıl, p ≈ 0,004–0,007. Bunu saklamıyoruz.
- RF'nin geride kalmasının olası sebebi: n = 64 küçük, ilişki kabaca doğrusal ve ağaç modelleri doğrusal eğilimi basamaklarla yaklaşıklıyor.
- **Keşif (ön kayıtta yok, `pilot/ml_kontrol_kesif.py`):** Kazanç büyük ölçüde 1950'deki genç kadın eğitiminden ve bebek ölümünden geliyor.
  - Eğitim 1950 tek başına 7,8 yıl (p = 0,035), ρ = −0,56. 1950'de +1 yıl eğitim, yaklaşık 5,7 yıl erken dönüm.
  - log IMR 1950 tek başına 6,8 yıl (p = 0,014), ρ = +0,48.
  - Gelir 1950 tek başına 10,1 yıl (takvimden kötü), ρ = −0,22 (anlamsız). Ekvator bu 64 ülkede ilişkisiz (ρ = +0,11).
- **Yorum:** Para yine zamanlamayı söylemiyor. Okul, eşik olarak zamanlayıcı değil (Q2), ama 1950'deki başlangıç düzeyi olarak
  bir sinyal taşıyor. Nedensellik iddiası yok; eğitim ve bebek ölümü aynı kalkınmanın parçaları.
