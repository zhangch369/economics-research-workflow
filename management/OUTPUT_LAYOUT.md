# 输出分类与日期版次命名（当前有效）

先按用途，再按code的模块查找；日期和版次写在输出文件名上。不再以时间或随机后缀运行文件夹作为outputs的主要分类。

```text
outputs/
├── tables/02_main_regressions/main_table_demo_20261027_v01.doc
├── figures/02_main_regressions/main_figure_demo_20261027_v01.png
├── logs/02_main_regressions/analysis_demo_20261027_v01.log
├── estimates/02_main_regressions/main_estimate_demo_20261027_v01.ster
├── samples/02_main_regressions/main_sample_demo_20261027_v01.dta
├── qa/90_qa/metrics_demo_20261027_v01.csv
├── provenance/02_main_regressions/demo_20261027_v01/   该版的源文件和配置快照
└── runs/demo/run_20261027_v01.json                    状态和所有产物准确路径
```

## 文件与版次

文件名使用“用途_任务_YYYYMMDD_vNN.扩展名”，例如main_table_demo_20261027_v01.doc。v01就是第1版，v02为第2版；不使用随机串、UUID或哈希作为版本名。哈希仅在指纹记录内验证内容，不承担目录分类或版本命名。来源原件、代码/配置源文件保留原名；provenance中代码快照保留原相对文件名，外层明确所属日期和版次，便于原样恢复。

run.py、export_replication.py和server_sync.py默认使用北京时间当天日期，同一任务同日自动递增版次。可用--date YYYYMMDD --edition N明确指定；已经使用的版次拒绝覆盖。版次保留记录独占创建只解决版次重复，不等于跨聊天任务锁、缓存或依赖调度。

## 所有语言共用

图片只输出PNG，回归表只输出DOC。outreg2使用word选项生成DOC；临时TXT在同一表全部列完成后精确删除，不能在追加列之间删除。控制台.txt/.log属于logs；QA指标.csv属于qa，QA图片也只PNG。Stata启动进程的工作目录设为对应模块logs，包装do-file本身也带日期和版次，所以Stata自动日志沿用可读名称。

图表导出语句仍在对应分析代码中。使用启动器提供的明确产物宏，例如outreg2 using "$MAIN_TABLE"、graph export "$MAIN_FIGURE"；不能再假定$OUT下面有某个随机运行文件夹。$OUT现在指向outputs根目录。Python同样从project_layout.RunLayout或已登记的产物路径取得tables/figures/logs位置，不把研究图表写入日志目录。

## 数据与清理

数据分类见DATA_LAYOUT.md：data_intermediate和data_analysis逐级镜像code，不按运行时间建目录。每个数据文件同样带日期和版次。

每次任务结束与每周检查：列出确认无用的临时txt、废弃输出、未被保留版本引用的重复产物，写明具体路径、理由、可回收空间（有实测时）和是否已经获准删除。根据内容区分历史正式表格txt与临时txt；正式表图、有效日志、实际样本与复现来源不能仅因扩展名或旧日期被清理。已确认不需要的具体文件按用户授权清理，并保留清单；尚未确认的候选先提醒。

验收：runs记录、config/tasks.json产物字典、EXHIBITS及写作引用与真实文件一致；所有生成文件可读、带日期版次；不再生成随机后缀文件夹。

## 唯一图表格式

图片示例main_figure_demo_20261027_v01.png，回归表示例main_table_demo_20261027_v01.doc。Stata使用graph export对应PNG路径, as(png)，回归使用outreg2对应DOC路径, word。新任务配置将产物kind分别标为figure和regression_table，路径工具拒绝其他扩展名。历史PDF/TXT等不自动删除；清理只作用于本次精确的outreg2临时同名TXT，其他日志/QA文本保留。
