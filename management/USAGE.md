# 新项目使用指南 / Starting a New Project

[中文](#中文) | [English](#english)

## 中文

下面的步骤以 macOS 为例，Windows 和 Linux 选择对应的机器配置文件。首次配置约 10–20 分钟，不包括安装软件或处理真实数据。

### 1. 取得一个独立的项目副本

在 [仓库首页](https://github.com/zhangch369/economics-research-workflow) 点击 **Code → Download ZIP**，解压后把文件夹重命名为你的项目名称。解压后的文件夹就是项目根目录，`code/`、`management/` 和 `writing/` 直接位于其中。

也可以在终端克隆：

```bash
git clone https://github.com/zhangch369/economics-research-workflow.git my-research-project
cd my-research-project
```

克隆副本会保留原仓库的 Git 历史和 `origin`。如果准备连接自己的仓库，先执行 `git remote remove origin`，再按自己的 GitHub 仓库地址添加新远端；不要把研究数据或代码误推送到模板仓库。ZIP 副本没有 Git 历史，需要时在项目根目录执行 `git init`。

### 2. 安装并检查运行环境

准备 Python 3.9 或更新版本、Stata 18，以及 Stata 扩展包 `reghdfe`、`ftools` 和 `outreg2`。启动器不会自动安装这些软件。

在项目根目录复制示例配置：

```bash
cp config/machine.mac.example.json config/machine.local.json
```

打开 `config/machine.local.json`，填写实际的 Stata 可执行文件路径，并按需要设置三层数据路径。Windows 使用 `machine.windows.example.json`，Linux 使用 `machine.linux.example.json`。`machine.local.json` 已被 Git 忽略，请勿在其中存放密钥。

### 3. 先运行合成示例

```bash
python3 run.py --task demo
```

运行结束后，打开终端显示的 `outputs/runs/demo/run_YYYYMMDD_vNN.json`。从记录中的artifacts查看表格、图形、样本和QA；日志位于 `outputs/logs/02_main_regressions/`。成功的内部演示应显示 `PASS`，分析数据包含 392 条观测、80 家企业。

如果失败，先打开`outputs/logs/` 对应模块下的日志，检查 Stata 路径和扩展包。**合成示例通过只说明示例流程可运行，不代表真实项目已经复现或因果识别成立。**

### 4. 登记自己的研究任务

1. 修改 `project.json` 和 `management/STATUS.md`，写明研究项目名称、问题和当前状态。
2. 在 `management/DATA_REGISTRY.csv` 中登记输入数据来源、版本、分析单位、主键和缺失规则。真实原始数据放在 `data_raw/` 或机器配置指定的位置；不要提交受限数据。
3. 在 `management/SPECIFICATIONS.csv` 中登记分析单位、处理与对照、因变量、解释变量及时间、样本、变换顺序、固定效应、聚类和识别限制。未知项明确标为待定。
4. 把 `management/templates/TASK.md` 复制到新建的 `management/tasks/`，填写第一个交付物、输入、允许修改的文件和验收标准。

`data_raw/demo/` 是仓库包含的合成例外；其他原始数据默认被 Git 忽略。`data_analysis/` 默认允许纳入 Git，**提交前必须确认数据允许公开**。本地机器配置、`outputs/` 和 `releases/` 默认被忽略；忽略规则不等于备份或访问控制。

### 5. 接入正式 Stata 流程

1. 在 `code/01_data_preparation/01_clean/`、`code/01_data_preparation/02_analysis_data/`、`code/02_main_regressions/` 等目录编写自己的 do-file，按阶段保存中间与分析数据。普通回归逐列显式写出，并紧接 `outreg2` 输出。
2. 修改 `code/00_run_formal.do`，替换当前的占位报错，明确列出已审核的阶段执行顺序。默认占位文件会主动报错，不能直接作为正式入口。
3. 在 `config/tasks.json` 的 `formal` 项填写经确认的 `scope`、`entry`、`output_module`、`inputs`、`artifacts` 和 `expected`；需要内部 QA 时设置 `qa_entry`、`qa_artifacts` 与 `qa_expected`。`entry` 和 QA 入口是相对于 `code/` 的路径，输入用 `area/path` 登记，产物用 `area/module/stem/suffix` 指定用途、对应代码模块、文件主体与扩展名；expected列出产物宏名。确认输入、产物和验收条件后，再把 `enabled` 改为 `true`。
4. 从项目根目录执行 `python3 run.py --task formal`，再核对本次运行的日志、实际样本、估计与 QA。

实际路径和项目示例可参考 `demo` 任务及对应 do-file。不要把示例数据的运行结果当作自己的正式结果。

### 6. 使用 AI agent 与继续项目

把 [首次启动提示词](../ai_records/NEW_PROJECT.txt) 的研究问题、数据位置和第一个交付物填好，交给能读取项目文件的 AI agent。简单任务可由一个 agent 完成；适合拆分时按 [协作规范](AGENT_WORKFLOW.md) 指定文件所有权与只读审查。不同平台是否支持子 agent 和自动读取指令，需要各自核实。

每次重要任务结束，依据实际证据更新 `management/STATUS.md`；重要规格或决策记录到 `management/DECISIONS.md` 和恢复卡。论文关键数字通过 `management/CLAIMS.csv` 和 `management/EXHIBITS.csv` 关联到对应运行、估计和样本。

## English

These instructions use macOS as an example. Choose the corresponding machine configuration on Windows or Linux. Initial setup usually takes 10–20 minutes, excluding software installation and data work.

### 1. Create a project copy

On the [repository page](https://github.com/zhangch369/economics-research-workflow), select **Code → Download ZIP**, extract it, and rename the folder for your project. The extracted folder is the project root.

Alternatively, clone the repository:

```bash
git clone https://github.com/zhangch369/economics-research-workflow.git my-research-project
cd my-research-project
```

A clone retains the template's Git history and `origin`. Before connecting your own repository, run `git remote remove origin` and add your own remote. A ZIP download has no Git history; run `git init` in the project root if you need version control.

### 2. Configure the environment

Install Python 3.9+, Stata 18, and the Stata packages `reghdfe`, `ftools`, and `outreg2`. The launcher does not install dependencies. On macOS:

```bash
cp config/machine.mac.example.json config/machine.local.json
```

Edit `config/machine.local.json` to point to your Stata executable and, if needed, your three data directories. Use the Windows or Linux example on those systems. The local file is Git-ignored; do not store credentials in it.

### 3. Run the synthetic demonstration

```bash
python3 run.py --task demo
```

Open the `outputs/runs/demo/run_YYYYMMDD_vNN.json` file printed by the launcher and use its artifact paths. Logs are under `outputs/logs/<module>/`; tables, figures, estimates, samples, and checks have their own top-level type directories. A successful internal demo reports `PASS`; its analysis dataset has 392 observations and 80 firms. If it fails, inspect the logs and check the Stata path and packages. Passing the synthetic demo does not validate a real project or its identification strategy.

### 4. Register the project

1. Update `project.json` and `management/STATUS.md` with the project identity and current state.
2. Register each input's source, version, unit, key, and missing-value rules in `management/DATA_REGISTRY.csv`.
3. Record the research specification in `management/SPECIFICATIONS.csv`, including treatment and comparison, outcomes, timing, sample, transformations, fixed effects, clustering, and identification limitations.
4. Copy `management/templates/TASK.md` into a new `management/tasks/` directory and define the first deliverable and its acceptance criteria.

The bundled `data_raw/demo/` is a synthetic exception to the raw-data ignore rule. Other raw data are ignored by default; `data_analysis/` can be tracked. Check that data can be shared before committing. Ignore rules are not access controls or backups.

### 5. Configure the formal Stata pipeline

Write project do-files in the numbered `code/` stages, saving intermediate and analysis datasets. Replace the deliberate placeholder error in `code/00_run_formal.do` with the reviewed stage order. In `config/tasks.json`, fill the `formal` task's `scope`, `entry`, `output_module`, `inputs`, `artifacts`, and `expected`; configure `qa_entry`, `qa_artifacts`, and `qa_expected` when applicable. The `entry` paths are relative to `code/`; inputs use `area/path`, while artifacts use `area/module/stem/suffix`; `expected` lists artifact macro names. Enable the task only after defining the inputs and acceptance criteria.

Then run `python3 run.py --task formal` and inspect the logs, actual estimation samples, estimates, and QA. Use the demo task as a structural example, not as a formal result.

### 6. Use AI assistance and maintain progress

Fill in [the new-project prompt](../ai_records/NEW_PROJECT.txt) and give it to an agent that can read the project files. The [collaboration guide](AGENT_WORKFLOW.md) describes optional delegation, file ownership, and read-only review; platform support varies. Update project status from actual evidence and record important decisions and handoffs. Link key manuscript claims to exhibits, specifications, runs, estimates, and samples in the existing registries.

## 日期版次与目录 / Dates, editions, and directories

数据目录逐级镜像code；outputs先按tables/figures/logs等分类，再按模块。输出文件名直接带YYYYMMDD_vNN，无随机后缀目录。包内已有分析v01时，第一次运行会自动选用v02，保留已附带的分析文件。不要强制覆盖已有版次。

Intermediate and analysis directories mirror `code/` recursively. Output filenames carry `YYYYMMDD_vNN` under type-first output directories. If an analysis edition is already bundled, the next run selects an unused edition. Exported replication archives exclude internal QA; the workflow template itself retains the internal QA examples.
