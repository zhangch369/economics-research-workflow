# 经济学科研工作流 / Empirical Economics Research Workflow

[中文](#中文) | [English](#english)

## 中文

详细启动步骤：[中英文使用指南](management/USAGE.md)。


项目采用扁平布局。代码按论文部分组织，数据仅为合成演示。

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

图表语句放在对应分析代码中，回归后立即outreg2、绘图后立即graph export。新图片固定输出PNG，新回归表固定输出DOC；outreg2的临时TXT在同一张表全部列导出后删除。当前示例产物路径由tasks.json统一登记并通过宏传给Stata。内部QA留code/90_qa，生产入口独立；公开包用`python3 export_replication.py`导出，移除内部QA和其任务调用。规则见[OUTPUT_LAYOUT](management/OUTPUT_LAYOUT.md)。

## 服务器与维护

本机与服务器使用相同扁平目录设计。相关代码变更后先运行`python3 server_sync.py plan`列离线差异，获得项目负责人对本次同步的同意后才连接/同步；远端核验后登记完成。该工具不建立网络连接。详见[SERVER_SYNC](management/SERVER_SYNC.md)。

每次任务结束和每周检查：提醒清理确认无用的临时txt、废弃输出和无保留依赖的重复文件，列具体路径和可删依据。正式DOC表格、有效日志和复现依赖按用途识别；不因扩展名直接删除。禁止新生成随机后缀文件夹。

管理说明在management，思考报告在research_notes，正式稿在writing，核心对话在ai_records。新项目从[NEW_PROJECT](management/NEW_PROJECT.md)启动；当前正式任务仍未接入，不能将模板历史PASS当成研究成果。

## English

This repository is a personal workflow template for empirical economics research. It includes a synthetic demonstration, Stata analysis scripts, project management templates, and optional AI-assisted collaboration guidance. It does not contain private research data, personal chat transcripts, or local machine configurations.

### Getting started

For a complete walkthrough, see the **[bilingual new-project guide](management/USAGE.md)**.

1. Read [AGENTS.md](AGENTS.md), [project.json](project.json), and [project status](management/STATUS.md). For a new project, follow the [startup checklist](management/NEW_PROJECT.md). The detailed documentation and templates are currently in Chinese.
2. Copy the appropriate example configuration to `config/machine.local.json` and set the path to your Stata executable. For macOS:

   ```bash
   cp config/machine.mac.example.json config/machine.local.json
   ```

3. From the project root, run the synthetic demonstration:

   ```bash
   python3 run.py --task demo
   ```

The demonstration requires Python 3.9+, Stata 18, and the Stata packages `reghdfe`, `ftools`, and `outreg2`. The launcher does not install dependencies. The expected analysis dataset contains 392 observations for 80 firms. A successful synthetic run does not validate a real research project or its identification strategy.

### Project layout

| Directory | Purpose |
| --- | --- |
| `code/` | Numbered Stata production stages; `90_qa/` contains internal checks |
| `config/` | Task definitions and machine/server configuration examples |
| `data_raw/`, `data_intermediate/`, `data_analysis/` | Raw, intermediate, and analysis data |
| `outputs/` | Type-first tables, figures, logs, estimates, samples, checks, provenance, and readable run records |
| `management/` | Project status, data and specification registries, task cards, and workflow rules |
| `research_notes/`, `ai_records/` | Research notes and important AI session handoffs |
| `writing/`, `releases/` | Manuscripts and presentations; fixed versions and replication packages |

Raw and intermediate data are ignored by Git, apart from the included synthetic fixture; analysis data are tracked when added. Avoid committing confidential data and local configuration. Paths for the three data layers can be set independently in the machine configuration.

### Analysis and outputs

The demo entry point runs setup, cleaning, analysis-data construction, and regression stages in order. Formal data preparation and estimation use Stata. Ordinary regressions are written explicitly and followed immediately by `outreg2`; tables and figures are exported in the relevant analysis scripts. New figures are PNG only and new regression tables are DOC only.

Outputs are organized by type first: `outputs/tables/`, `figures/`, `logs/`, `estimates/`, `samples/`, `qa/`, `provenance/`, and `runs/`, followed by the code module. Generated filenames contain a date and edition such as `main_table_demo_20261027_v01.doc`; no random-suffix version directories are created. Intermediate and analysis directories mirror the complete relative directory tree under `code/`. Repeated runs advance the edition and refuse overwrites, including when the clone already contains a versioned analysis file. See the [output layout](management/OUTPUT_LAYOUT.md).

Internal QA is invoked separately by the task configuration and is not required by the production entry point. `python3 export_replication.py` builds a local replication archive that excludes internal QA and records `qa_status=NOT_RUN`; it does not publish or upload the archive.

### AI collaboration and project management

For substantial tasks, use the [task card](management/templates/TASK.md) to record deliverables, inputs, dependencies, file ownership, and acceptance criteria. The [collaboration guide](management/AGENT_WORKFLOW.md) describes optional delegation and read-only evidence-based review. Simple tasks can use a single agent. Key manuscript claims can be linked to specifications, runs, estimates, and samples in `management/CLAIMS.csv` and `management/EXHIBITS.csv`.

Automatic dependency scheduling, caching, task locking, and a status dashboard are **not implemented**; see the [automation roadmap](management/AUTOMATION_ROADMAP.md).

### Server work

Local and server projects use the same directory layout, while absolute paths may differ. Before remote changes, generate a local plan and obtain the project owner's approval for that specific synchronization. `python3 server_sync.py plan` compares local files with a recorded snapshot without connecting to the server. A local change or an old snapshot does not establish the current remote state. See the [server guide](management/SERVER_SYNC.md).

### Readable versions and cleanup

Use `--date YYYYMMDD --edition N` only to request an unused edition. Default editions increase automatically. The top-level code follows data preparation, main regressions, robustness, mechanisms, and extensions; data preparation contains cleaning and analysis-data construction submodules. Table and figure export commands remain in the relevant analysis scripts.

After a task and during a configured weekly check, list unused temporary text files, superseded outputs, and unreferenced duplicates. Retain required DOC tables, estimation samples, logs, and reproducibility evidence according to purpose. Cleanup candidates require explicit scope and authorization; no automatic deletion is implemented. This repository does not install a personal reminder automatically.
