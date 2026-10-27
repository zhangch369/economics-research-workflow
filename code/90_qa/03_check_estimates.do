version 18.0
********************************************************************
**# 04 独立 QA：重新载入正式衔接文件与估计，不依赖前序内存
********************************************************************
use "$OUT/samples/demo_sample.dta", clear
isid firm_id year
assert estimation_sample == 1
assert _N == 392
estimates use "$OUT/estimates/demo.ster"
assert e(N) == 392
assert e(N_clust) == 80
assert !missing(_b[x], _se[x])
assert _se[x] > 0
file open metrics using "$OUT/qa/metrics.csv", write text
file write metrics "N,N_clust,b_x,se_x" _n
file write metrics %12.0f (e(N)) "," %12.0f (e(N_clust)) "," %24.17g (_b[x]) "," %24.17g (_se[x]) _n
file close metrics
file open qa using "$OUT/qa/QA_PASS.txt", write text
file write qa "PASS" _n
file close qa
