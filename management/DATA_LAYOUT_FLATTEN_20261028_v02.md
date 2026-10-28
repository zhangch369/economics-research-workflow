# 数据目录扁平化：2026-10-28 第2版

数据层不再重复code的`01_data_preparation`父目录。现行结构：

```text
data_raw/demo/v01/
data_intermediate/01_clean/
data_analysis/02_analysis_data/
```

## 实现

- `config/tasks.json`的每个派生数据产物同时登记`module`和`data_module`。
- `module`继续指向`code/`下真实生产目录。
- `data_module`决定扁平数据目录，分别是`01_clean`和`02_analysis_data`。
- 运行器只创建任务登记的目录，不再复制完整code树。
- 公开复现包只包含登记的数据目录。
- 内部QA核对实际登记的数据目录，不再要求空目录镜像code。

## 验证

公开分支合成演示`20261028_v07`通过，完整检查7/7通过；实际中间数据写入`data_intermediate/01_clean/`，实际分析数据写入`data_analysis/02_analysis_data/`。详细报告为`outputs/runs/layout_checks/run_20261028_v04.json`。
