version 18.0
********************************************************************
**# 合成示例：仅检验项目工作流，不代表任何真实项目的研究结果
********************************************************************
do "$CODE/00_setup/01_setup_environment.do"
do "$CODE/01_clean/01_firm_year_clean.do"
do "$CODE/02_analysis_data/01_firm_year_analysis.do"
do "$CODE/03_regressions/01_main.do"
