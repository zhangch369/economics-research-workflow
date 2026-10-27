version 18.0
* 内部检查入口；不进入对外复现包，生产入口不依赖本文件。
do "$CODE/90_qa/01_check_clean_data.do"
do "$CODE/90_qa/02_check_analysis_data.do"
do "$CODE/90_qa/03_check_estimates.do"
