version 18.0
********************************************************************
**# 03 单列示例：企业—年份；同期 x/y；企业及年份 FE；企业聚类
**## 未设计处理与对照，不作因果解释；不缩尾、不取对数、不差分
********************************************************************
use "$ANALYSIS_FILE", clear
reghdfe y x, absorb(firm_id year) vce(cluster firm_id)
outreg2 using "$MAIN_TABLE", replace ctitle(Synthetic_demo) dec(6)
estimates save "$MAIN_ESTIMATE"
gen byte estimation_sample = e(sample)
save "$MAIN_SAMPLE"

* 合成示例描述图，不作因果解释。
twoway scatter y x, name(demo_scatter, replace) xtitle("Synthetic x") ytitle("Synthetic y")
graph export "$MAIN_FIGURE", replace
