# Exploratory search B: new external data vs fertility turning point (t0)

**Not for the presentation.** Exploratory only. Run on 18 Oct 2026.

## How to reproduce
Downloads went to the scratchpad (`kesif_indir/b_dis/<slug>/data.csv`), outside the project.
```
python -I 01_ozellik_tablosu.py <download_root> ../../clean/t0_tablosu.csv ozellik_tablosu.csv
python -I 02_testler.py ../../clean/t0_tablosu.csv ozellik_tablosu.csv .
python -I 03_saglamlik.py ../../clean/t0_tablosu.csv ozellik_tablosu.csv ../../data_dis/barrolee_BL_v3_F2564.csv ../../data_dis/gdp-per-capita-maddison-project-database.csv .
```
Files:
- `ozellik_tablosu.csv`: the features, plus censoring flags for the timing features (−1 = already past the threshold at the first observation, +1 = never crossed).
- `test_kaydi.csv`: every test, 104 of them t0 tests with BH q-values, plus 6 collinearity checks left out of the FDR.
- `permutasyon_null.csv`, `loo_top3.csv`, `out02.txt`, `out03.txt`: run outputs.

## Sources
All are Our World in Data grapher CSVs, downloaded 2026-10-18 from `https://ourworldindata.org/grapher/<slug>.csv?v=1&csvType=full&useColumnShortNames=true`.

| slug | original provider (as OWID cites it) | used? |
|---|---|---|
| share-of-population-urban, urban-population-share-2050 | UN DESA World Urbanization Prospects (OWID processing) | yes |
| child-mortality | Gapminder + UN IGME | yes |
| cross-country-literacy-rates | OWID compilation (UNESCO; van Zanden et al. 2014) | yes |
| electoral-democracy-index | V-Dem | yes |
| population-density | HYDE + UN WPP | yes |
| life-expectancy | Riley, HMD, UN WPP (from 1950 this is WPP) | yes, flagged as WPP-derived |
| daily-per-capita-caloric-supply | FAO (starts 1961) | yes, 1961 baseline |
| share-of-women-15-years-and-older-with-no-education | OWID long-run series. Despite the slug, the column is `some_formal_education_both_sexes`. Likely Lee–Lee / van Zanden; **verify before any reuse** | yes, overlaps Barro–Lee |
| primary-enrollment-selected-countries | Lee & Lee (2016) + UNESCO, net primary enrolment | yes |
| contraceptive-prevalence-any-methods-of-women-ages-15-49 | UN / World Bank WDI | yes, flagged as **proximate, near-mechanical** |
| female-labor-force-participation-rates | ILO modelled estimates via WDI (1990+) | yes, flagged **POST-t0** |
| share-of-the-labor-force-employed-in-agriculture, share-of-employment-in-agriculture | ILO (1991+) | no, data start after t0 |
| age-at-marriage-women | 2001+, n = 41 | no |
| share-of-population-in-extreme-poverty | surveys 1980s+ | no |
| maternal-mortality | 1950 n = 14 | no |
| gross-enrollment-ratio-in-primary-education | 1970+, n = 42 | no |
| female-labor-force-participation-oecd | 4 countries | no |
| mean-years-of-schooling-female | 1990+, duplicates Barro–Lee | no |

## Results
Primary sample: `guvenilir == True`, n = 115 (t0 range 1955–2019). All 1950 baselines therefore fall before t0.

### Spearman ρ with t0
"Within" means both variables are ranked within region first.

| feature | n | ρ | within | ρ (all 200) | within (200) |
|---|---|---|---|---|---|
| year contraception ≥20% (proximate) | 24 | 0.70 | 0.78 | 0.77 | 0.65 |
| year life expectancy ≥50 (WPP-derived) | 114 | 0.70 | 0.62 | 0.89 | 0.63 |
| literacy 1950 | 93 | −0.66 | −0.63 | −0.83 | −0.59 |
| some formal education 1950 | 59 | −0.65 | −0.61 | −0.84 | −0.51 |
| life expectancy 1950 (WPP) | 114 | −0.65 | −0.58 | −0.85 | −0.58 |
| net primary enrolment 1950 | 59 | −0.59 | −0.53 | −0.80 | −0.46 |
| log child mortality 1960 | 75 | 0.55 | 0.50 | 0.86 | 0.54 |
| urban share 1950 | 114 | −0.46 | −0.37 | −0.71 | −0.46 |
| V-Dem democracy 1950 | 89 | −0.41 | −0.29 | −0.51 | −0.21 |
| calories 1961 | 84 | −0.29 | −0.37 | −0.61 | −0.38 |
| female LFP 1991 (post-t0) | 102 | −0.09 | 0.01 | 0.08 | 0.02 |

95 of the 104 tests have q < 0.05. The full list is in `test_kaydi.csv`.

### Null calibration
t0 was permuted 1,000 times within the primary sample, and the max |ρ| over the 18 features was recorded each time.

| feature set | 95th percentile of null max \|ρ\| | real best \|ρ\| |
|---|---|---|
| all 18 features | 0.42 (99th percentile: 0.54) | 0.70 |
| without the flagged features | 0.35 | 0.66 (literacy) |

### Leave-one-out prediction
Linear t0 ~ x, compared with the median t0 of the other countries. Values are median absolute errors in years.

| feature | n | model | baseline | Wilcoxon p |
|---|---|---|---|---|
| life expectancy 50 year | 114 | 8.2 | 12.3 | 3e-7 |
| contraception 20% year | 24 | 7.3 | 12.3 | 0.007 |
| literacy 1950 | 93 | 8.8 | 11.3 | 1e-4 |
| some formal education 1950 | 59 | 8.7 | 9.3 | 0.007 |
| net primary enrolment 1950 | 59 | 7.4 | 9.3 | 0.007 |

### Is it new? Partial Spearman controls, primary sample
- **Literacy 1950** correlates ρ = 0.82 with Barro–Lee women's schooling in 1950.
  - Controlling for Barro–Lee, its partial ρ falls from −0.66 to **−0.32** (n = 71).
  - Controlling for log GDP 1950, it stays at **−0.67**.
- Some formal education and primary enrolment show the same pattern:
  - Given Barro–Lee: −0.38 and −0.31.
  - Given GDP: −0.62 and −0.54.
- **Urban share 1950:**
  - Given Barro–Lee: −0.31.
  - Given GDP: −0.22 (q ≈ 0.06).
- **V-Dem democracy 1950:** given Barro–Lee, partial ρ is −0.22 (q ≈ 0.07, not significant).
- **Within regions,** literacy holds up:
  - Africa −0.70 (n = 22)
  - Asia −0.58 (n = 33)
  - Latin America −0.72 (n = 28)
  - Oceania −0.47 (n = 9, not significant)
- **Missing literacy:** 22 of the 115 primary countries have no 1950 literacy value, 11 of them in Asia.

## Honest verdict
- **There is a strong, robust and non-mechanical correlate: baseline literacy / education in 1950** (ρ ≈ −0.66).
  - It holds within regions.
  - It is far above the permutation null.
  - It cuts the LOO error by about 2.5 years.
  - It does not weaken when income is controlled.
- **But it is mostly the same "education at baseline" signal Barro–Lee already gave.** Literacy is only modestly stronger, and its partial ρ given Barro–Lee is −0.32. So it is not a new discovery.
- **The two top raw correlates are not usable as findings:**
  - Life-expectancy timing (ρ = 0.70) is WPP-derived. It restates the "mortality first" pattern inside the same UN model.
  - Contraceptive timing is a proximate determinant and has n = 24.
- **Generic caveat for all the timing features:** every country "modernises" in a sequence, so timing-vs-timing correlations partly reflect a shared development ordering.
- **Other limits:**
  - These are ecological, observational associations, not causes.
  - Some 1950 literacy values are UNESCO estimates.
  - The coverage gaps are not random.
