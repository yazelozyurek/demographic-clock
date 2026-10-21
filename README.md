# The Demographic Clock

**ASA DataQuest 2026 · Türkiye edition · Undergraduate**
Team **Stat4Sight**, Kırıkkale University, Department of Statistics:
Yazel Sude Özyürek · Elif Zarife Yıldırım · Zehra İklil Canatar · Rojbin Bağatur

> This repository was kept private during the competition, as the rules required, and made public afterwards.

## Questions and main results

Data: UN World Population Prospects 2024 (WPP2024), 200 countries with at least 100,000 people (99.98% of the world population), 1950–2023 estimates. Values after 2023 are UN projections and are always shown dashed.

| Question | Method | Result |
|---|---|---|
| **Q1** Do countries follow the same fertility path, only at different times? | One shared logistic (S) curve plus one time shift per country, after SITAR growth curves (Cole et al., 2010). The shift is the country's *turning point*: the year fertility falls fastest. | One curve explains 94% of the variation in children per woman (calendar year alone: 27%; a level shift with the same number of parameters: 87%). Best typical error 20 years ahead in backtests from 1983, 1993 and 2003. Regions differ in timing (Kruskal–Wallis p ≈ 0.00005). |
| **Q2** At the turning point: money or school? | 66 countries that turned in 1952–2013, linked to Maddison income and Barro–Lee schooling of women aged 25–34. Spread relative to world spread (bootstrap CI) and leave-one-out threshold prediction. | No wealth threshold: income at the turn ranged from $1,100 to $24,000 and predicted the year worse than the calendar (14.0 vs 9.5 years, p < 0.001). Schooling was 1.34× tighter (95% CI 1.09–1.67) but no better than the calendar. |
| **Q3** Does health turn first? | A second clock: the year life expectancy rose fastest, found with the same shared-curve method (115 countries whose fertility turning point is observed). | In 94% of countries the health clock turned first, a median of 18 years earlier; Spearman ρ = 0.77 (0.71 within regions). Knowing it cuts the error in guessing the fertility turning year from 12 to 6 years (leave-one-out). |

These are country-level associations, not causes. Türkiye turned around 1982, about 17 years after its health clock (1965).

## Repository structure

```
notebooks/   01–06: data overview, cleaning, EDA, the Demographic Clock (Q1), money or school (Q2), final figures
pilot/       scripts for the slide figures, cover, map, animation, health clock (Q3) and robustness checks
kesif/       exploratory correlation search (about 960 logged tests, FDR-corrected, permutation-calibrated)
clean/       derived tables (country panel, turning points, money-or-school table, health clock)
data_dis/    external data (Maddison, Barro–Lee) with sources and licences in KAYNAKLAR.md
outputs/     figures, animation and tables (e.g. excluded_places.csv lists every place left out, with the reason)
arac/        interactive "Demographic Clock" explorer (prototype)
sunum/       slide generator, slide sources and narration script (English, with Turkish translation)
data/        raw UN WPP2024 files — NOT in the repository (see below)
```

Many comments and file names are in Turkish.

## How to reproduce

1. **Environment:** Python 3.13 (Anaconda). `pip install -r requirements.txt`
2. **Raw data:** download from <https://population.un.org/wpp/Download/> into `data/`:
   - `WPP2024_Demographic_Indicators_Medium_csv.gz`
   - `WPP2024_Demographic_Indicators_OtherVariants_csv.gz`
   - `WPP2024_Supplement_Births_and_LE60.csv`
   - `WPP2024_Demographic_Indicators_notes.csv`
3. **Notebooks**, in order, from inside `notebooks/` (Restart & Run All): `01` → `02` (writes `clean/countries_1950_2100.csv`) → `03` → `04` (writes `clean/t0_tablosu.csv`) → `05` (writes `clean/para_okul_tablosu.csv`) → `06`.
4. **Figures and slides**, from the project folder:
   ```
   python pilot/slayt_grafikleri.py          # outputs/excluded_places.csv
   python pilot/saglik_saati.py              # Q3: clean/saglik_saati.csv, outputs/v3_s3_health.png
   python pilot/slayt_koyu.py                # slide charts
   python pilot/harita_test.py               # map and region tests
   python pilot/kapak_saat.py                # cover
   TEMA=koyu SADE=1 python pilot/animasyon.py  # slide animation
   python pilot/ml_kontrol.py                # pre-registered random-forest robustness check (plan: pilot/ml_kontrol_plan.md)
   python sunum/slayt_uret.py <folder>       # slide HTML
   ```

## Data sources

- United Nations, DESA, Population Division (2024). *World Population Prospects 2024*.
- Bolt, J. & van Zanden, J. L. (2025). Maddison-style estimates of the evolution of the world economy: A new 2023 update. *Journal of Economic Surveys*, 39(2), 631–671. Data: Maddison Project Database 2023 (CC BY 4.0), via Our World in Data.
- Barro, R. & Lee, J.-W. (2013). A new data set of educational attainment in the world, 1950–2010. *Journal of Development Economics*, 104, 184–198. Data: version 3.
- Cole, T. J., Donaldson, M. D. C. & Ben-Shlomo, Y. (2010). SITAR: a useful instrument for growth curve analysis. *International Journal of Epidemiology*, 39(6), 1558–1566.
- Natural Earth (public domain), via world-atlas 2.0.2, for the map.
- American Statistical Association (2022). *Ethical Guidelines for Statistical Practice*.

## Use of AI

We used an AI assistant as a working tool: to write analysis code, propose and test methods, design the figures and draft the slides and narration. The team chose the questions, made the final decisions, reviewed and edited the AI-written code, and re-ran all of it before submission to confirm that every number reproduces.
