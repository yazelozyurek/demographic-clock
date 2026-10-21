capture log close
set more off
program drop _all
macro drop _all
scalar drop _all
clear all

global root "C:\"

use $root/ku_data.dta, clear

reg changelifeexpect changemortality if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect changemortctry if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect changemortctryplustown if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect changemortctryrepltown if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect changemortmaxall if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)

reg changelifeexpect_1930_40 changemortality if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1930_40 changemortctry if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1930_40 changemortctryplustown if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1930_40 changemortctryrepltown if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1930_40 changemortmaxall if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)

reg changelifeexpect_1900_40 changemortality if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1900_40 changemortctry if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1900_40 changemortctryplustown if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1900_40 changemortctryrepltown if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)
reg changelifeexpect_1900_40 changemortmaxall if kubasesample47 == 1, cluster(ctrycluster)
di e(r2_a)