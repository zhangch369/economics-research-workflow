# 经济学科研项目模板

**本目录就是项目根目录和 Git 根目录，所有功能目录直接平级。**

```text
项目根目录/
├── code/                         生产代码按运行顺序分类；90_qa 为内部检查
├── config/                       任务、机器和服务器配置
├── data_raw/                     原始数据，不入 Git
├── data_intermeidate/             中间数据，不入 Git，沿用用户指定拼写
├── data_analysis/                清洗好的回归数据，纳入 Git
├── outputs/                      每次运行的日志、估计、样本和表图
├── management/                   状态、数据/规格登记、决策与复现说明
├── research_notes/               AI 整理的 Markdown 思考报告
├── ai_records/                   核心聊天与恢复卡
├── writing/                      Word、LaTeX、Beamer、PPT 正式稿
└── releases/                     固定版本与对外复现包
```

本仓库为个人使用的实证研究工作流模板，提供合成数据演示。正式研究数据、私人聊天和本机配置不包含在仓库中。

## 从这里开始

1. 读 [AGENTS.md](AGENTS.md)、[project.json](project.json)、[当前状态](management/STATUS.md)。
2. 从 config/ 中选择机器配置示例，复制成 machine.local.json，填写 Stata 实际路径。Mac 示例：`cp config/machine.mac.example.json config/machine.local.json`。
3. 在项目根目录执行 `python3 run.py --task demo`。需要 Stata 18、reghdfe、ftools、outreg2 和 Python 3.9+；启动器不自动安装依赖。合成示例应有392条分析观测、80个企业。

机器配置默认使用根目录内 data_raw、data_intermeidate、data_analysis。原始和中间数据可按需要放到挂载盘；要纳入当前 Git 的分析数据需位于本仓库内。搬迁时保留相同相对布局，按任务传输数据版本。

## 代码分类

生产入口 code/00_run_demo.do 按顺序调用 00_setup、01_clean、02_analysis_data、03_regressions。稳健性放 04_robustness。图表导出语句直接写在对应分析代码中：回归后立即 outreg2，绘图后立即 graph export；生成文件保存到本次 outputs/ 下的 tables/ 或 figures/，不单设图表导出阶段。阶段内文件也编号并标明数据类型与用途，例如 01_clean/01_firm_year_clean.do。清洗、估计、QA 分文件。

内部 QA 留在 code/90_qa/，由任务配置单独调用，不被生产入口依赖。内部运行通过时记录 qa_status=PASS；对外包用 `python3 export_replication.py` 导出，排除内部 QA 并移除其任务调用，记录 qa_status=NOT_RUN。公开导出不等于自动上传或发布。

## 涉及服务器时必须遵守

本机和服务器使用**同一根目录设计**，code、config、三层数据、输出与文档目录直接平级；两台机器的绝对根路径、Stata 路径可以不同。

**本机相关代码有变更 → 生成差异 → 项目负责人 同意 → 同步服务器 → 远端验证 → 记录版本。** 没有本次同意，agent 不得自动连接、上传或修改服务器。同步代码的同意不自动扩大为重跑回归或重建数据。

有服务器任务时，按 [服务器协作说明](management/SERVER_SYNC.md) 登记 server.local.json。执行 `python3 server_sync.py plan` 只在本机比较代码和已记录快照，列出待同步项；它不连接服务器。未取得远端快照时明确记为未核实；不能把“本机改好了”写成“服务器已同步”。实际完成后保留远端代码指纹、目录核对和授权记录。

无服务器任务时保持 enabled=false。具体项目原有的服务器授权限制继续适用。

管理细则见 [工作流规范](management/WORKFLOW.md)。简易思考报告放 research_notes/，正式论文与汇报放 writing/，核心聊天放 ai_records/。不要另建未登记的完整子项目副本。

## 新项目与多 agent 协作

新项目从 [启动清单](management/NEW_PROJECT.md) 开始，也可复制 [首次启动提示词](ai_records/NEW_PROJECT.txt)。较大任务用 [任务卡](management/templates/TASK.md) 定义交付物和文件所有权；按 [协作规范](management/AGENT_WORKFLOW.md) 调用执行者与只读审查者。简单任务保持单 agent。

关键论文结论登记在 management/CLAIMS.csv，并关联既有 EXHIBITS.csv。任务状态由协调者依据实际证据维护。[自动化路线图](management/AUTOMATION_ROADMAP.md) 明确已提供与未实现能力；当前不提供自动缓存、依赖调度或状态面板。

新项目应检查版本控制与忽略规则。合成示例验证不代表真实项目验收。

## outputs 分类

每次运行内，logs/ 放日志，tables/ 放 outreg2、Stata、Python 研究表格，figures/ 放研究图片。其他分类及示例见 [输出分类](management/OUTPUT_LAYOUT.md)。
