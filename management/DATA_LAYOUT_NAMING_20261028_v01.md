# 分析阶段与原始快照命名整理（中间版本，已取代）

> 本记录的嵌套数据目录方案已被`DATA_LAYOUT_FLATTEN_20261028_v02.md`取代；保留原记录用于追溯。

本版按用户意见整理两个目录名称：

|对象|旧名称|现行名称|
|---|---|---|
|分析数据构建代码|`code/01_data_preparation/02_build/`|`code/01_data_preparation/02_analysis_data/`|
|中间数据镜像目录|`data_intermediate/01_data_preparation/02_build/`|`data_intermediate/01_data_preparation/02_analysis_data/`|
|分析数据镜像目录|`data_analysis/01_data_preparation/02_build/`|`data_analysis/01_data_preparation/02_analysis_data/`|
|合成原始快照|`data_raw/demo/v1/`|`data_raw/demo/v01/`|

`02_analysis_data`直接说明该阶段产出分析数据；`v01`使用两位版次格式，与模板其余日期版次命名一致。原有分析数据文件整体迁移，文件名和内容未改。

## 验证

公开分支重新运行Stata合成演示，结果`20261028_v05`、内部QA为PASS；实际分析数据写入`02_analysis_data`，原始CSV从`demo/v01`读取。随后完整检查7/7通过，覆盖重复运行与防覆盖、PNG/DOC格式、目录镜像、迁移、公开包独立运行、离线服务器计划和实际样本及完整b/V比较。

本地报告：`outputs/runs/layout_checks/run_20261028_v03.json`。
