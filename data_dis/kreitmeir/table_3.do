capture log close
set more off
program drop _all
macro drop _all
scalar drop _all
clear all

global root "C:\"

use $root/ku_data.dta, clear

ivreg2 changelogpopulation (changelifeexpect=changemortality) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortctry) if kusample9and2ctry == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortctryplustown) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortctryrepltown) if kusample9and2ctryrepltown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortmaxall) if kusample9and2maxall == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)



ivreg2 changetotalbirths (changelifeexpect=changemortality) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortctry) if kusample9and2ctry == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortctryplustown) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortctryrepltown) if kusample9and2ctryrepltown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortmaxall) if kusample9and2maxall == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)



ivreg2 changegdp (changelifeexpect=changemortality) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortctry) if kusample9and2ctry == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortctryplustown) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortctryrepltown) if kusample9and2ctryrepltown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortmaxall) if kusample9and2maxall == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)



ivreg2 changegdppc (changelifeexpect=changemortality) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortctry) if kusample9and2ctry == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortctryplustown) if kusample9and2ctryplustown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortctryrepltown) if kusample9and2ctryrepltown == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortmaxall) if kusample9and2maxall == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)