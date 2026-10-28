# 公开模板验证：2026-10-28 第5版

本版验证`data_analysis`下同时保留两个编号目录的最终结构。

```text
data_raw/demo/v01/
data_intermediate/01_clean/
data_analysis/01_clean/
data_analysis/02_analysis_data/
```

## 通过项

1. Stata合成演示运行成功：392条分析观测、80个企业，内部QA为PASS。
2. 清洗阶段从`data_raw/demo/v01/`读取合成CSV，并将中间面板写入`data_intermediate/01_clean/`。
3. `data_analysis/01_clean/`和`data_analysis/02_analysis_data/`两个编号目录同时存在。
4. 最终分析数据写入`data_analysis/02_analysis_data/`；`01_clean/`作为项目级清洗分析输入目录保留，不复制fixture。
5. 任务级`data_directories`登记目录，产物级`module`与`data_module`分别登记生产代码和数据位置。
6. 完整检查7/7通过：重复运行与防覆盖、PNG/DOC格式、登记数据目录、目录迁移和Git策略、公开包独立运行、离线服务器计划、历史参考/当前/迁移/公开数据及实际样本和完整b/V一致性。

## 范围与限制

服务器计划只做离线检查，没有连接服务器或传输文件。Windows/Linux仅提供配置示例，未作本次实机验证。真实科研数据、正式回归和识别论证不在本验证范围内。

本地运行日志、表图、估计和QA原始证据保存在`outputs/`，不进入公开仓库。
