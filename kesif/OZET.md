# Korelasyon araması: genel özet (18 Ekim 2026, keşif, SUNUMA GİRMEZ)

Soru: Bir ülkenin doğurganlık dönüm yılıyla (t0) güçlü ilişkili bir özellik var mı?
Üç ajan, toplam yaklaşık 960 test (316 + 104 + 539). Her ajanda BH-FDR ve t0'ı karıştırarak bütün aramanın şans kalibrasyonu yapıldı.
Ayrıntılar: `a_wpp/SONUC.md`, `b_dis/SONUC.md`, `c_yontem/SONUC.md`.

| Sinyal | En iyi ölçü | ρ (115 gözlenen ülke) | Şans eşiği (null %95) | LOO hata (takvim bazı) | Not |
|---|---|---|---|---|---|
| Ölüm önce düşer | LEx yükselişinin orta yılı | 0,77 | 0,58 | 6,2 (12,0) | Teoriyle uyumlu; UN aynı kaynaklardan tahmin ettiği için kısmen mekanik olabilir |
| Ölüm düzeyi 1950 | LEx 1950 | −0,65 | 0,27–0,38 | 8,5 (12,0) | Claude bağımsız doğruladı: ρ = −0,648 |
| Başlangıç eğitimi | Okuryazarlık 1950 / Barro–Lee kadın 1950 | −0,66 / −0,56 | 0,42 | 7,0–8,8 | İki kaynak aynı sinyal (r = 0,82) |
| Kentleşme, demokrasi 1950 | | −0,46 / −0,41 | | | Kontrollerle −0,2…−0,3 |
| Nüfus yoğunluğu 1950 | | −0,42 | | | Beklenmedik, ada/küçük ülke etkisi olabilir, sadece keşif |
| Gelir 1950 | Maddison | −0,22 (anlamsız) | | takvimden kötü | Hiçbir testte yardım etmedi |
| Ekvator, yağış, göç, nüfus | | ≈ 0 | | | İlişki yok |

Claude'un ek kontrolü (64 ülke, standart katsayılar, yıl/1 SD):
- eğitim 1950 + LEx 1950 birlikte: eğitim −5,2 (p = 0,001), LEx −4,1 (p = 0,007), R² 0,41. İkisi ρ = 0,67 ilişkili ama ikisi de ayrı bilgi taşıyor.
- + log gelir + bölge: eğitim −6,6 (p < 0,001), LEx −3,8 (p = 0,013), gelir +0,3 (p = 0,84), R² 0,52.

Sonuç: Sağlam ilişki "1950'deki kalkınma düzeyi (ölüm ve eğitim) → daha erken dönüm", |ρ| ≈ 0,6–0,77. Para değil.
Nedensellik yok; karıştırıcılar: genel kalkınma, devlet kapasitesi, kentleşme, aile planlaması programları, din/kültür, sömürge geçmişi.
