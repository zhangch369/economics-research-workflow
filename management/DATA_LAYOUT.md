# 数据目录逐级对应code

规则：除raw保留来源分类外，data_intermediate与data_analysis的目录层级必须和code完全对应，包括专题和研究线子目录，不自行增加日期目录、哈希目录或另一套业务分类。

```text
code/01_data_preparation/01_clean/01_firm_year_clean.do
  → data_intermediate/01_data_preparation/01_clean/firm_year_panel_demo_20261027_v01.dta
code/01_data_preparation/02_build/01_firm_year_analysis.do
  → data_analysis/01_data_preparation/02_build/firm_year_analysis_demo_20261027_v01.dta
code/02_main_regressions/01_main.do
  → 读取上述冻结分析文件；估计/实际样本写outputs/estimates和outputs/samples
```

镜像以**生产数据的代码所在目录**为准。下游代码显式读取已登记的生产文件，不把同一分析数据到处复制。没有数据产物的模块可以保留空目录，便于统一查找。code目录增加、移动或增加研究线后，两层数据同步增加相同目录；当前运行器从code实际目录自动建立镜像。旧目录必须先记录映射再归位，不能让旧代码失去输入却宣称可复现。

例如大学科技园研究示例某专题包含code/02_main_regressions/legacy_may和revised，两层数据也应出现相同相对目录。legacy_may/revised是研究线，不替代日期版次；文件本身仍需YYYYMMDD_vNN。主稿、投稿包和候选修改线的采用关系单独登记，不能只靠日期决定哪份是正式结果。

data_raw不入Git；data_intermediate不入Git；data_analysis纳入Git。日期版次在文件名，不以随机目录替代版本。对外包按config/replication_export.json的analysis_files逐份选择分析文件，不能自动把“最近”文件当作已接受版本。

当前附带数据全部为合成示例；实际项目须登记自己的来源、研究线和版本，不把模板验证当作科学结论。
