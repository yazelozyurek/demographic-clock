# Dış veri kaynakları (indirme tarihi: 16 Ekim 2026)

| Dosya | Kaynak | İndirme adresi | Atıf |
|---|---|---|---|
| gdp-per-capita-maddison-project-database.csv | Maddison Project Database 2023 (Our World in Data üzerinden) | https://ourworldindata.org/grapher/gdp-per-capita-maddison-project-database.csv | Bolt, J. & van Zanden, J. L. (2025). Maddison-style estimates of the evolution of the world economy: A new 2023 update. *Journal of Economic Surveys*, 39(2), 631–671. doi:10.1111/joes.12618 (çevrim içi 2024). Veri: Maddison Project Database 2023, doi:10.34894/INZBF2, CC BY 4.0. |
| mean-years-of-schooling-long-run.csv | Lee & Lee (2016) uzun dönem eğitim, 15–64 yaş (Our World in Data üzerinden) | https://ourworldindata.org/grapher/mean-years-of-schooling-long-run.csv | Lee, J.-W. & Lee, H. (2016). Human capital in the long run. *Journal of Development Economics*, 122, 147–169. |
| barrolee_BL_v3_F2564.csv | Barro–Lee v3, kadın, 25–64 yaş, 1950–2015, 5 yıllık | https://barrolee.github.io/BarroLeeDataSet/BLData/BL_v3_F2564.csv | Barro, R. & Lee, J.-W. (2013). A new data set of educational attainment in the world, 1950–2010. *Journal of Development Economics*, 104, 184–198. |
| barrolee_BL_v3_F2534.csv | Barro–Lee v3, kadın, **25–34 yaş** (ana analizde kullanılan; doğurganlık çağındaki kadınlar). BL_v3_F.csv dosyasından agefrom == 25 satırları | https://barrolee.github.io/BarroLeeDataSet/BLData/BL_v3_F.csv | Aynı |
| barrolee_BL_v3_MF2564.csv | Barro–Lee v3, iki cinsiyet, 25–64 yaş | https://barrolee.github.io/BarroLeeDataSet/BLData/BL_v3_MF2564.csv | Aynı |

- Our World in Data verileri CC BY 4.0 lisanslı. Kaynak gösterilerek kullanılabilir.
- Ülkeler ISO3 koduyla eşleştirilir (WPP `ISO3_code`, OWID `code`, Barro–Lee `WBcode`).
- Atıflar 17 Ekim 2026'da doğrulandı (Maddison: research.rug.nl / IDEAS; Barro–Lee: NBER w15902, Harvard; SITAR: Bristol research portal).
- Barro–Lee: makale 1950–2010; kullandığımız veri v3 (2021 güncellemesi, 1950–2015).
- Yöntem atfı: Cole, T. J., Donaldson, M. D. C. & Ben-Shlomo, Y. (2010). SITAR — a useful instrument for growth curve analysis. *International Journal of Epidemiology*, 39(6), 1558–1566.

## Acemoglu & Johnson (2007) — tahmini ölüm aracı (21 Ekim 2026'da indirildi)

- Atıf: Acemoglu, D. & Johnson, S. (2007). Disease and Development: The Effect of Life Expectancy on Economic Growth. *Journal of Political Economy*, 115(6), 925–985.
- Kaynak: MIT Economics, Daron Acemoglu Data Archive → "Disease and Development" (https://economics.mit.edu/people/faculty/daron-acemoglu/data-archive). Dosyalar: `disease.dta`, `disease_stacked.dta`, `changes4080.dta`, `maketable3v10b.do`, `maketable4v10.do`, `maketable10v10.do`.
- Klasör: `data_dis/aj2007/`. Lisans belirtilmemiş, bu yüzden depoya konmadı (.gitignore).
- Kullanılan sütunlar: `compsjmhatit` (tahmini ölüm), `lifeexpect`, `gdppcmadd`, `sample40`, `sjbasesamplenoncomm`, `startrich`, hastalık ölüm hızları (`malaria`, `tball`, `pneumonia`, `smallpox`).

## HIV yaygınlığı (21 Ekim 2026'da indirildi)

- Dünya Bankası, World Development Indicators, `SH.DYN.AIDS.ZS` "Prevalence of HIV, total (% of population ages 15-49)" (kaynak: UNAIDS). API: https://api.worldbank.org/v2/country/all/indicator/SH.DYN.AIDS.ZS?format=json&per_page=20000&date=1990:2023 (lisans CC BY 4.0).
- Klasör: `data_dis/hiv_wb/` (ham JSON + `hiv_prevalence_15_49.csv`).
