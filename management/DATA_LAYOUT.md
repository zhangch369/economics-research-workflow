# 数据目录：按产出阶段扁平归档

三层数据根目录与code根目录平级。派生数据不复制code的完整层级，避免出现重复且难读的`data_analysis/01_data_preparation/02_analysis_data`。

```text
code/01_data_preparation/01_clean/01_firm_year_clean.do
  → data_intermediate/01_clean/firm_year_panel_demo_20261027_v01.dta

code/01_data_preparation/02_analysis_data/01_firm_year_analysis.do
  → data_analysis/02_analysis_data/firm_year_analysis_demo_20261027_v01.dta

data_analysis/01_clean/
  → 项目级清洗分析输入的保留目录

data_raw/demo/v01/firm_year.csv
  → 原始合成输入，按来源和版本留存
```

## 显式映射

`config/tasks.json`在任务级`data_directories`登记本任务允许存在的数据目录；每个中间或分析产物另登记：

- `module`：生产该数据的code相对目录，用于验证生产代码真实存在。
- `data_module`：数据根目录下的扁平相对目录，用于决定实际落盘位置。

合成任务映射：

|目录或产物|code模块|数据根|data_module|
|---|---|---|---|
|中间面板|`01_data_preparation/01_clean`|`data_intermediate`|`01_clean`|
|分析层清洗输入|`01_data_preparation/01_clean`|`data_analysis`|`01_clean`|
|分析数据|`01_data_preparation/02_analysis_data`|`data_analysis`|`02_analysis_data`|

运行器只创建任务实际登记的`data_directories`和数据产物`data_module`，不再根据完整code目录树批量创建空镜像目录。`data_analysis/01_clean/`当前用`.gitkeep`保留目录，不复制合成fixture；真实项目需要时可登记项目级清洗分析输入。

## 研究线与版本

普通数据处理固定使用上述扁平结构。若同一阶段存在`legacy_may`、`revised`等并行研究线，`data_module`可使用可读的相对子路径，例如`01_clean/revised`或`02_analysis_data/legacy_may`，但必须在任务配置和数据登记中明确写出，不能自动从code路径推测。

数据文件名继续使用`用途_任务_YYYYMMDD_vNN.ext`。日期和版次写在文件名中，不使用随机或哈希目录替代版本。

## Git与来源

- `data_raw/`保存原始或固定输入，默认不入Git；公开模板只对合成fixture保留明确例外。
- `data_intermediate/`保存阶段中间数据，不入Git。
- `data_analysis/`保存可供估计读取的分析数据，按项目授权纳入Git。

对外复现包按`config/replication_export.json`明确选择分析数据版本，不自动把“最近”文件当正式版本。下游代码读取已登记文件，不把同一分析数据复制到多个目录。

当前附带数据均为合成示例；NUSTP仅作只读分类参照。历史迁移路径保留在旧迁移记录中，不回写为当前结构。
