Kreitmeir and Überfuhr, "Disease and development – The predicted
mortality instrument revisited"

This paper revisits the predicted mortality instrument introduced by
Acemoglu and Johnson in their article

  "Disease and Development: The Effect of Life Expectancy on Economic
  Growth", Journal of Political Economy, 2007, 115(6):925-985, is
  posted at the following website:
  https://economics.mit.edu/people/faculty/daron-acemoglu/data-archive

Appendix C (Section F) of the Acemoglu-Johnson article describes the
construction and the sources of their data.

We use the original predicted mortality instrument of the Acemoglu-Johnson
article and four revised predicted mortality instruments which differentiate
themselves concerning the inclusion of country-level and town-level mortality
rates in the construction process. The instrumental variables and data on
outcome variables are in the file ku_data.csv and also in the Stata data
file ku_data.dta.

These files contain 243 observations and 44 variables. The units of
observation are countries and these are the rows in the data files.
The columns are the variables, which are defined as follows.

Variable Names and Descriptions:

country                         Country
ctry                            Country code
iso3                            ISO-3 code
un_code                         UN code
startrich                       1 if initially rich country
startmedium                     1 if initially middle-income country
startpoor                       1 if initially poor country
kubasesample47                  Baseline sample of 47 countries; Acemoglu and Johnson (2007)
ctrycluster                     Country code used in clustering
kusample9and2ctryplustown       Countries with at least 9/13 rates non-missing & pneumonia and tball non-missing  (Country-level suppl. w. town-level)
kusample9and2ctry               Countries with at least 9/13 rates non-missing & pneumonia and tball non-missing (Country-level)
kusample9and2ctryrepltown       Countries with at least 9/13 rates non-missing & pneumonia and tball non-missing (Country-level repl. w. town-level)
kusample9and2maxall             Countries with at least 9/13 rates non-missing & pneumonia and tball non-missing  (Max)
kusample10and2ctryplustown      Countries with at least 10/13 rates non-missing & pneumonia and tball non-missing  (Country-level suppl. w. town-level)
kusample10and2ctry              Countries with at least 10/13 rates non-missing & pneumonia and tball non-missing (Country-level)
kusample10and2ctryrepltown      Countries with at least 10/13 rates non-missing & pneumonia and tball non-missing (Country-level repl. w. town-level)
kusample10and2maxall            Countries with at least 10/13 rates non-missing & pneumonia and tball non-missing  (Max)
changemortality                 Change in predicted mortality; Acemoglu and Johnson (2007)
changemortctry                  Change in predicted mortality (Country-level)
changemortctryplustown          Change in predicted mortality (Country-level suppl. w. town-level)
changemortctryrepltown          Change in predicted mortality (Country-level repl. w. town-level)
changemortmaxall                Change in predicted mortality (Max)
changemortminall                Change in predicted mortality (Min)
avgchangemortctry               Change in predicted average mortality (Country-level)
avgchangemortctryplustown       Change in predicted average mortality (Country-level suppl. w. town-level)
avgchangemortctryrepltown       Change in predicted average mortality (Country-level repl. w. town-level)
avgchangemortmaxall             Change in predicted average mortality (Max)
avgchangemortminall             Change in predicted average mortality (Min)
changelifeexpect                Change in Ln(LEB); 1940-1980
changelifeexpect_40_00          Change in Ln(LEB); 1940-2000
changelifeexpect_40_90          Change in Ln(LEB); 1940-1990
changelifeexpect_1930_40        Change in Ln(LEB); 1930-1940
changelifeexpect_1900_40        Change in Ln(LEB); 1900-1940
changelogpopulation             Change in Ln(Population); 1940-1980
changelogpopulation_40_00       Change in Ln(Population); 1940-2000
changelogpopulation_1900_40     Change in Ln(Population); 1900-1940
changegdp                       Change in Ln(GDP); 1940-1980
changegdp_40_00                 Change in Ln(GDP); 1940-2000
changegdp_1900_40               Change in Ln(GDP); 1900-1940
changegdppc                     Change in Ln(GDP per capita); 1940-1980
changegdppc_40_00               Change in Ln(GDP per capita); 1940-2000
changegdppc_1900_40             Change in Ln(GDP per capita); 1900-1940
changetotalbirths               Change in Ln(Total Births); 1940-1980
changetotalbirths_40_90         Change in Ln(Total Births); 1940-1990


To replicate the tables in the main text and in the Appendix, the
following Stata user-written commands must be installed: ivreg2,
weakivtest, and weakiv. Each of these commands can be
installed from within Stata by typing (for example) "ssc install
ivreg2".


The results in Tables 1-3 of the main text can be replicated by
running the Stata do-files

Table_1.do
Table_2.do
Table_3.do

using the Stata data file ku_data.dta.


Similarly, the results in Tables A.1-A.15 in the Appendix can be
replicated by running the Stata do-files

Table_A1.do
Table_A2.do
Table_A3.do
Table_A4.do
Table_A5.do
Table_A6.do
Table_A7.do
Table_A8.do
Table_A9.do
Table_A10.do
Table_A11.do
Table_A12.do
Table_A13.do
Table_A14.do
Table_A15.do

using the Stata data file ku_data.dta.
