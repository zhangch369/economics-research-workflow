# 生产复现说明（合成示例）

本包仅有合成示例，所有正式面板清洗和回归由Stata执行。需要Stata18、reghdfe、ftools、outreg2与Python3.9+。

1. 从config选择machine.*.example.json，复制为machine.local.json并配置Stata路径。
2. 在根目录执行`python3 run.py --task demo`。
3. 查看终端给出的outputs/runs/demo/run_YYYYMMDD_vNN.json；表格、图片和日志分别在outputs/tables、figures、logs的对应模块目录。

数据目录逐级对应code；分析数据纳入Git，原始/中间不入Git。输出文件直接带日期和版次，不创建随机目录；已有日期版次不会覆盖。发布包内的已接受分析文件保留，重建运行自动选择新一版。

内部code/90_qa及QA任务配置按要求不在此包；qa_status=NOT_RUN不代表内部QA通过。生产入口独立运行。合成示例应产生392条分析记录、80个企业的估计和描述图。

本机与服务器布局一致；修改服务器代码/同步须获得项目负责人本次同意。本包不会自动连接服务器或上传。
