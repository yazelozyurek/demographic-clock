capture log close
set more off
program drop _all
macro drop _all
scalar drop _all
clear all

global root "C:\"

use $root/ku_data.dta, clear

ivreg2 changelogpopulation (changelifeexpect=changemortality) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortctry) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortctryplustown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortctryrepltown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changelogpopulation (changelifeexpect=changemortmaxall) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)



ivreg2 changetotalbirths (changelifeexpect=changemortality) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortctry) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortctryplustown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortctryrepltown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changetotalbirths (changelifeexpect=changemortmaxall) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)



ivreg2 changegdp (changelifeexpect=changemortality) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortctry) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortctryplustown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortctryrepltown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdp (changelifeexpect=changemortmaxall) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)



ivreg2 changegdppc (changelifeexpect=changemortality) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortctry) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortctryplustown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortctryrepltown) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)

ivreg2 changegdppc (changelifeexpect=changemortmaxall) if kubasesample47 == 1, cluster(ctrycluster) small
* Effective F-statistic
weakivtest
* Weak-IV-robust confidence interval
weakiv,  gridpoints(1000) gridmult(4)