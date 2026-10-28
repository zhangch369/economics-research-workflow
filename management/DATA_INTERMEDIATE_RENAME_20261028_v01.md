# 中间数据目录拼写修正：2026-10-28

模板此前的中间数据目录使用了错误拼写`data_intermeidate`。自本版起统一使用正确名称：

`data_intermediate/`

## 影响范围

- 项目根目录及目录树中的拼写。
- `run.py`、`export_replication.py`和内部QA目录的硬编码路径。
- macOS、Windows、Linux机器配置示例。
- 服务器根目录配置示例。
- `.gitignore`、项目元数据、README、数据布局、输出布局、工作流与服务器协作文档。

`data_raw/`和`data_analysis/`语义不变，原有合成原始数据及分析数据不改名。

## 验证

公开工作树重新运行Stata合成演示，结果`20261028_v03`、内部QA为PASS。随后完整检查7/7通过，覆盖重复运行与防覆盖、PNG/DOC格式、数据目录镜像、迁移、公开包独立运行、离线服务器计划和实际样本及完整b/V比较。

本地报告：`outputs/runs/layout_checks/run_20261028_v02.json`。
