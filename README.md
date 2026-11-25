# The Demographic Clock

**ASA DataQuest 2026 · Türkiye edition · Undergraduate**
Team **Stat4Sight**, Kırıkkale University, Department of Statistics:
Yazel Sude Özyürek · Elif Zarife Yıldırım · Zehra İklil Canatar · Rojbin Bağatur

🥉 Ranked 3rd in Best Statistical Insight, ASA DataQuest 2026 Türkiye  
▶ [Watch the narrated video (4:25)](https://github.com/yazelozyurek/demographic-clock/releases/tag/v1.0)

> This repository was kept private during the competition, as the rules required, and made public afterwards.

## Questions and main results

Data: UN World Population Prospects 2024 (WPP2024), 200 countries with at least 100,000 people (99.98% of the world population), 1950–2023 estimates. Values after 2023 are UN projections and are always shown dashed.

| Question | Method | Result |
|---|---|---|
| **Q1** Do countries follow the same fertility path, only at different times? | One shared logistic (S) curve plus one time shift per country, after SITAR growth curves (Cole et al., 2010). The shift is the country's *turning point*: the year fertility falls fastest. | One curve explains 94% of the variation in children per woman (calendar year alone: 27%; a level shift with the same number of parameters: 87%). Best typical error 20 years ahead in backtests from 1983, 1993 and 2003. Regions differ in timing (Kruskal–Wallis p ≈ 0.00005). |
| **Q2** At the turning point: income or education? | 66 countries that turned in 1952–2013, linked to Maddison income and Barro–Lee schooling of women aged 25–34. Spread relative to world spread (bootstrap CI) and leave-one-out threshold prediction. | No wealth threshold: income at the turn ranged from $1,100 to $24,000 and predicted the year worse than the calendar (14.0 vs 9.5 years, p < 0.001). Women's education was 1.34× tighter (95% CI 1.09–1.67) but no better than the calendar. |
| **Q3** Does health turn first? | A second clock: the year life expectancy rose fastest, found with the same shared-curve method (115 countries whose fertility turning point is observed). | In 94% of countries the health clock turned first, a median of 18 years earlier; Spearman ρ = 0.77 (0.71 within regions). Knowing it cuts the error in guessing the fertility turning year from 12 to 6 years (leave-one-out). |
| **Q4** Is health a cause? | A natural experiment: the medicines and vaccines of the 1940s helped most where those diseases killed most. Country-level predicted-mortality instrument of Kreitmeir & Überfuhr (2024), after Acemoglu & Johnson (2007); two-stage least squares, 50 countries. Three tests, each pre-registered in the git history before its results. | Where the medicines raised life expectancy more, children per woman fell further by 1990: about 10% more life expectancy → 0.44 fewer children (95% weak-IV-robust CI 0.18–0.69; first-stage F = 43), while total births rose. The two other tests (turning-year timing; HIV reverse shock) could not tell. With 1940 health held fixed the instrument turns weak, so this supports, but does not settle, a causal reading. |

Q1–Q3 are country-level associations, not causes; Q4 supports, but does not settle, a causal reading. Türkiye turned around 1982, about 17 years after its health clock (1965).

## Repository structure

```
notebooks/   01–06: data overview, cleaning, EDA, the Demographic Clock (Q1), income or education (Q2), final figures
pilot/       scripts for the slide figures, cover, map, animation, health clock (Q3), robustness checks and video editing
kesif/       exploratory correlation search (about 960 logged tests, FDR-corrected, permutation-calibrated) and the three
             pre-registered causal tests: d_neden/, e_hiv/, f_kreitmeir/ (plan.md committed before each result)
clean/       derived tables (country panel, turning points, income-or-education table, health clock)
data_dis/    external data (Maddison, Barro–Lee, Kreitmeir & Überfuhr, World Bank HIV) with sources and licences in KAYNAKLAR.md
outputs/     figures, animation and tables (e.g. excluded_places.csv lists every place left out, with the reason)
sunum/       slide generator and slide sources (the narration is in each slide's notes); video/ holds the video edit plans
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
   python pilot/kapak_saat.py                # cover (still image)
   python pilot/kapak_animasyon.py           # cover animation
   SLAYT=1 python pilot/kapak_video.py       # cover clip used in the slides
   TEMA=koyu SADE=1 python pilot/animasyon.py  # slide animation
   python pilot/ml_kontrol.py                # pre-registered random-forest robustness check (plan: pilot/ml_kontrol_plan.md)
   python kesif/d_neden/neden_testi.py       # Q4 test 1: Acemoglu–Johnson instrument, turning-year design (needs data_dis/aj2007/, see below)
   python kesif/e_hiv/hiv_testi.py           # Q4 test 2: HIV reverse shock
   python kesif/f_kreitmeir/ku_testi.py      # Q4 test 3 (main): revised instrument, long differences
   python pilot/neden_grafigi.py             # Q4 slide figures
   python sunum/slayt_uret.py <folder>       # slide HTML
   ```

5. **Narrated video.** It was edited from the team's own screen recording of the slides (the recording and the final
   video, about 175 MB, are not in the repository). Cut list: `sunum/video/kurgu_plani_30ekim.json`.
   ```
   python pilot/kurgu_ses.py sunum/video/kurgu_plani_30ekim.json <audio.wav>          # cuts and levels the audio
   python sunum/video/gostergeler_zaman.py <audio.wav>                               # highlight timing (Whisper word timestamps)
   swift pilot/kurgu_video.swift sunum/video/kurgu_plani_30ekim.json <audio.wav> <edit.mov> sunum/video/gostergeler_30ekim.json
   swift pilot/yuksek_kalite.swift <edit.mov> <video.mp4> 20 srgb                      # final H.264 encode
   ```
   Card and in-card highlight positions: `sunum/video/kutular.json`, `sunum/video/parcalar.json` (`sunum/video/parcalar_olc.py`).

## Data sources

- United Nations, DESA, Population Division (2024). *World Population Prospects 2024*.
- Bolt, J. & van Zanden, J. L. (2025). Maddison-style estimates of the evolution of the world economy: A new 2023 update. *Journal of Economic Surveys*, 39(2), 631–671. Data: Maddison Project Database 2023 (CC BY 4.0), via Our World in Data.
- Barro, R. & Lee, J.-W. (2013). A new data set of educational attainment in the world, 1950–2010. *Journal of Development Economics*, 104, 184–198. Data: version 3.
- Acemoglu, D. & Johnson, S. (2007). Disease and development: The effect of life expectancy on economic growth. *Journal of Political Economy*, 115(6), 925–985. Data: MIT Economics data archive (not redistributed here; download `disease.dta` into `data_dis/aj2007/`).
- Kreitmeir, D. & Überfuhr, T. (2024). Disease and development – The predicted mortality instrument revisited. *Journal of Applied Econometrics*, 39(2), 327–337. Data: ZBW Journal Data Archive, doi:10.15456/jae.2023321.1041806336 (CC BY 4.0), in `data_dis/kreitmeir/`.
- Bloom, D. E., Canning, D. & Fink, G. (2014). Disease and development revisited. *Journal of Political Economy*, 122(6), 1355–1366.
- World Bank, World Development Indicators, SH.DYN.AIDS.ZS: HIV prevalence, ages 15–49 (UNAIDS estimates), CC BY 4.0.
- Cole, T. J., Donaldson, M. D. C. & Ben-Shlomo, Y. (2010). SITAR: a useful instrument for growth curve analysis. *International Journal of Epidemiology*, 39(6), 1558–1566.
- Natural Earth (public domain), via world-atlas 2.0.2, for the map.
- American Statistical Association (2022). *Ethical Guidelines for Statistical Practice*.

## Use of AI

We used an AI assistant as a working tool: to write analysis code, propose and test methods, design the figures and draft the slides and narration. The team chose the questions, made the final decisions, reviewed and edited the AI-written code, and re-ran all of it before submission to confirm that every number reproduces.

## License

Code is released under the MIT License. Data files keep their original licences (see Data sources and `data_dis/KAYNAKLAR.md`).
