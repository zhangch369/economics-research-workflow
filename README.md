# 经济学科研复现模板

项目采用扁平布局。研究组织参照NUSTP的论文部分；不包含NUSTP真实研究数据或回归结果。

```text
项目根目录/
├── code/                    00_setup；01_data_preparation；02_main_regressions；03_robustness；04_mechanisms；05_extensions；90_qa
├── data_raw/                来源原件，不入Git
├── data_intermediate/       目录逐级镜像code，不入Git
├── data_analysis/           目录逐级镜像code，纳入Git
├── outputs/                 tables、figures、logs、estimates、samples、qa、provenance、runs
├── config/                  任务、机器与服务器配置
├── management/              管理说明、状态、登记与决策
├── research_notes/          AI思考报告
├── ai_records/              核心聊天与恢复卡
├── writing/                 Word、LaTeX、Beamer、PPT正式稿
└── releases/                日期与版次命名的对外复现包
```

## 先运行示例

1. 读AGENTS.md、project.json、management/STATUS.md；从config选择机器配置，复制为machine.local.json并填写Stata路径。
2. 在根目录执行`python3 run.py --task demo`。需要Stata18、reghdfe、ftools、outreg2及Python3.9+。所有正式清洗、分析数据构造和回归仍由Stata执行。
3. 查看终端给出的`outputs/runs/demo/run_YYYYMMDD_vNN.json`，按其中artifacts准确路径打开表图、估计和实际样本。合成示例有392条分析记录、80个企业，不是任何真实论文结果。

## 找数据、结果与版次

数据目录逐级对应实际code目录，新增专题/研究线要一起镜像；同一数据由生产代码所在模块归档，下游显式引用，不到处复制。分类见[DATA_LAYOUT](management/DATA_LAYOUT.md)。

示例：`data_intermediate/01_data_preparation/01_clean/firm_year_panel_demo_20261027_v01.dta`；`data_analysis/01_data_preparation/02_build/firm_year_analysis_demo_20261027_v01.dta`。

outputs先按用途分类，再按模块：表格在`outputs/tables/02_main_regressions/`，图在figures，日志在logs；不再用日期或随机后缀文件夹作为主要分类。文件直接标日期和版次，例如`main_table_demo_20261027_v01.doc`。同日重复运行自动递增为v02、v03；--date和--edition可明确指定，已有版次不覆盖。包内已有同名分析文件时，也自动避开该版次。

图表语句放在对应分析代码中，回归后立即outreg2、绘图后立即graph export。当前示例产物路径由tasks.json统一登记并通过宏传给Stata。内部QA留code/90_qa，生产入口独立；公开包用`python3 export_replication.py`导出，移除内部QA和其任务调用。规则见[OUTPUT_LAYOUT](management/OUTPUT_LAYOUT.md)。

## 服务器与维护

本机与服务器使用相同扁平目录设计。相关代码变更后先运行`python3 server_sync.py plan`列离线差异，获得Zhangchi对本次同步的同意后才连接/同步；远端核验后登记完成。该工具不建立网络连接。详见[SERVER_SYNC](management/SERVER_SYNC.md)。

每次任务结束和每周检查：提醒清理确认无用的临时txt、废弃输出和无保留依赖的重复文件，列具体路径和可删依据。历史正式表格txt、有效日志和复现依赖按用途识别；不因扩展名直接删除。禁止新生成随机后缀文件夹。

管理说明在management，思考报告在research_notes，正式稿在writing，核心对话在ai_records。新项目从[NEW_PROJECT](management/NEW_PROJECT.md)启动；当前正式任务仍未接入，不能将模板历史PASS当成研究成果。

输出格式固定：图片只PNG，回归表只DOC。同一表全部列导出后清理outreg2临时TXT；日志/QA文本和历史结果按用途保留。
