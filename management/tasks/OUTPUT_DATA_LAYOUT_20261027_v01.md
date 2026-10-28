# NUSTP参照下的数据与输出分类更新

状态：DONE；优先级P0；协调者：当前agent；范围：当前economics_workspace及分发压缩包。NUSTP只读，不改动、不重跑、不连接服务器。

交付：日期+版次文件名；数据目录逐级对应code；outputs按类型优先；运行/打包/同步入口、文档和登记同步；新版内部包及可独立运行的公开示例。

阶段：①已完成NUSTP只读核对；②已完成分类、命名与入口实现；③重复运行/防覆盖、镜像一致、数值、公开包、同步计划验证通过。

验收：无随机后缀作为版本名；输出文件含YYYYMMDD_vNN；data_intermeidate和data_analysis的目录与code逐级相同；tables/figures/logs为outputs一级目录；模型和样本保持合成示例原设定；公开包无内部QA仍能运行。

预计20–25分钟，目录与打包检查失败则顺延。单agent执行，避免共享登记表写入冲突。无研究规格待决定。

证据：management/VALIDATION_20261027_v01.json；内部检查outputs/runs/layout_checks/run_20261027_v02.json，最终公开包outputs/runs/final_package_check/run_20261027_v01.json。单agent实施与自验，未声称独立agent审查。一次公开包失败已修复，失败历史保留。

最终交付：../economics_project_template_20261027_v02.zip；内部包解压实跑PASS，镜像目录解压即存在，既有分析版本不覆盖；原包补标v01保留。清理候选3项，未删除实际科研数据。
