version 18.0
********************************************************************
**# 01 原始 CSV → 保存中间面板；不覆盖原始数据
********************************************************************
import delimited using "$RAW/demo/v1/firm_year.csv", clear varnames(1)
label variable y "合成结果变量；unknown 保持缺失"
label variable x "合成解释变量，无因果解释"
sort firm_id year
save "$INTERMEDIATE/panel.dta"
