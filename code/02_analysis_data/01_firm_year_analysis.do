version 18.0
********************************************************************
**# 02 中间面板 → 分析数据；记录缺失，不将未知补成零
********************************************************************
use "$INTERMEDIATE/panel.dta", clear
gen byte eligible = !missing(y, x)
keep if eligible
xtset firm_id year
sort firm_id year
save "$ANALYSIS/analysis.dta"
