# Sonuç: HIV "ters şok" testi (21 Ekim 2026)

Plan: `plan.md` (commit bbedcc9, analizden önce). Kod: `hiv_testi.py`. Çıktı: `log.txt`, `sonuc_ulkeler.csv`.

## Ön koşul: Sağlık şoku gerçekten oldu ✅

1990→2005 medyan değişim: yaşam beklentisi yüksek HIV ülkelerinde **−5,7 yıl**, düşük HIV ülkelerinde **+5,8 yıl**. 5 yaş altı ölüm (binde) yüksek HIV'de sadece −7,5 azaldı (Botsvana, Lesotho, Esvatini, Güney Afrika, Zimbabve'de arttı), düşük HIV'de −54 azaldı.

## Ana test (ön kayıtlı): FARK YOK

| Ölçü | Yüksek HIV | Düşük HIV | Fark | Permütasyon p |
|---|---|---|---|---|
| **ANA:** 2005 TFR'sinin ortak yoldan sapması (1990 konumundan), n = 8 / 9 | +0,04 | +0,22 | −0,18 | **0,40** |
| D1: doz, Spearman(HIV tepe, sapma), n = 24 | | | ρ = −0,03 | 0,87 |
| D2: pencere 1990→2010 | +0,36 | +0,43 | −0,08 | 0,87 |
| D3: TFR1990 > 6,5 dahil, n = 11 / 21 | −0,03 | +0,04 | −0,07 | 0,71 |
| D4: basit eğim farkı (1995–2010 − 1980–1990, çocuk/yıl) | +0,03 | −0,03 | +0,06 | **0,001** |

**Ön kayıttaki kurala göre yorum:** "Fark ayırt edilemedi." 1990'daki konumlarından bakınca, yüksek HIV ülkeleri 2005'e ortak yolun beklediği yerde vardı.

## D4 neden farklı? (SONRADAN yapılan tanı kontrolü, ön kayıtta yok, kanıt sayılmaz)

D4'ü iki parçaya ayırıp her parçayı ortak eğrinin o noktadaki beklentisiyle karşılaştırdık (medyan, çocuk/yıl; eksi = yoldan hızlı, artı = yoldan yavaş):

| | 1980–1990 | 1995–2010 |
|---|---|---|
| Yüksek HIV | **−0,051** (yoldan hızlı) | **+0,034** (yoldan yavaş) |
| Düşük HIV | −0,012 | +0,005 |

Yani yüksek HIV ülkeleri 1980'lerde ortak yoldan **daha hızlı** düşüyordu, HIV döneminde (1995–2010) ise **daha yavaş**. Bu desen iki hikâyeyle açıklanabilir:
1. **HIV duraklaması:** Sağlık bozulunca düşüş yavaşladı (Q3'ün sağlık → doğurganlık hikâyesiyle tutarlı; biyolojik etki ters yönde olduğu için daha da dikkat çekici).
2. **Ortalamaya dönüş:** Çok hızlı düşen ülkeler zaten sonra yavaşlar.

Ana ölçü (1990 başlangıçlı) bunları ayıramadı, çünkü 1990–1995'teki hızlı düşüş ile sonraki yavaşlama birbirini götürüyor. 1995 başlangıcını şimdi seçmek, sonucu görerek pencere seçmek olur (çatallanan yollar). **Bu yüzden bu desen sadece yeni bir ön kayıtlı test için fikir.**

## Bir sonraki adım için öneri (yeni ön kayıt gerekir)

Her ülkenin **kendi** şok zamanına hizalanmış olay çalışması: yaşam beklentisinin tepe yaptığı yıl = 0. Bu yıldan önceki ve sonraki 10 yılda doğurganlığın ortak yoldan sapması, düşük HIV ülkelerinin aynı takvim yıllarıyla karşılaştırılır. Pencere sonuçtan değil, her ülkenin kendi sağlık verisinden gelir.

## Bilinen sınırlar

Az ülke (8–11 / 9–21), HIV'in biyolojik etkisi, prezervatif kampanyaları, Kenya ve Gana'daki HIV'den bağımsız duraklama, UN'in HIV ölümlerini UNAIDS modelinden alması.
