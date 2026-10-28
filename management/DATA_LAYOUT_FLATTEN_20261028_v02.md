# 数据目录扁平化：2026-10-28 第2版

数据层不再重复code的`01_data_preparation`父目录。现行结构：

```text
data_raw/demo/v01/
data_intermediate/01_clean/
data_analysis/01_clean/
data_analysis/02_analysis_data/
```

## 实现

- `config/tasks.json`的每个派生数据产物同时登记`module`和`data_module`。
- `module`继续指向`code/`下真实生产目录。
- 任务级`data_directories`登记数据层允许出现的目录。
- `data_module`决定具体产物目录：中间面板为`01_clean`，分析数据为`02_analysis_data`。
- `data_analysis/01_clean/`保留为项目级清洗分析输入目录，不复制合成fixture。
- 运行器只创建任务登记的目录，不再复制完整code树。
- 公开复现包只包含登记的数据目录。
- 内部QA核对实际登记的数据目录，不再要求空目录镜像code。

## 验证

公开分支合成演示`20261028_v09`通过，完整检查7/7通过；实际中间数据写入`data_intermediate/01_clean/`，分析数据写入`data_analysis/02_analysis_data/`，`data_analysis/01_clean/`作为项目级清洗输入目录保留。详细报告为`outputs/runs/layout_checks/run_20261028_v05.json`。

## 01/02双目录补充

按用户确认，`data_analysis`下同时保留`01_clean/`和`02_analysis_data/`。任务配置通过`data_directories`登记两个目录，分析产物通过`data_module=02_analysis_data`落盘。`01_clean/`以`.gitkeep`保留，不复制合成fixture。
