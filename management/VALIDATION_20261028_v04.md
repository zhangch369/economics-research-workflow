# 公开模板验证：2026-10-28 第4版

本版验证扁平数据目录结构：

```text
data_raw/demo/v01/
data_intermediate/01_clean/
data_analysis/02_analysis_data/
```

## 通过项

1. Stata合成演示运行成功：392条分析观测、80个企业，内部QA为PASS。
2. 清洗阶段从`data_raw/demo/v01/`读取合成CSV，并将中间面板写入`data_intermediate/01_clean/`。
3. 分析数据阶段将结果写入`data_analysis/02_analysis_data/`。
4. `config/tasks.json`分别用`module`验证生产代码、用`data_module`决定数据落盘目录。
5. 数据层没有重复创建`01_data_preparation`父目录，也没有未登记的code镜像空目录。
6. 完整检查7/7通过：重复运行与防覆盖、PNG/DOC格式、登记数据目录、目录迁移和Git策略、公开包独立运行、离线服务器计划、历史参考/当前/迁移/公开数据及实际样本和完整b/V一致性。

## 范围与限制

服务器计划只做离线检查，没有连接服务器或传输文件。Windows/Linux仅提供配置示例，未作本次实机验证。真实科研数据、正式回归和识别论证不在本验证范围内。

本地运行日志、表图、估计和QA原始证据保存在`outputs/`，不进入公开仓库。
