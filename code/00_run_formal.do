version 18.0
********************************************************************
**# 正式入口待接入：先确定 SPECIFICATIONS.csv、数据版本和验收规则
**# 将下面阶段替换为已审定的项目 do-file，逐行明确执行顺序
********************************************************************
display as error "Formal pipeline is not configured. Read README.md and AGENTS.md."
error 459
* do "$CODE/01_data_preparation/01_clean/01_firm_year_clean.do"
* do "$CODE/01_data_preparation/02_analysis_data/01_firm_year_analysis.do"
* do "$CODE/02_main_regressions/01_main.do"
* do "$CODE/03_robustness/01_alternative_sample.do"
* 图表由对应分析脚本直接导出到本次 outputs/tables 或 outputs/figures。
* 内部 QA 由任务配置的 qa_entry 另行执行，不进入生产入口。
