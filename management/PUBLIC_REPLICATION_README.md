# 生产复现说明（合成示例）

本包从允许公开的合成CSV生成中间数据、分析数据与一列固定效应回归。不是任何真实论文的实证结果。code、config、三层数据和outputs都在本项目根目录直接平级，不使用project子目录。

1. 安装 Stata 18、reghdfe、ftools、outreg2。启动器使用 Python 3.9+ 标准库。
2. 从 config/ 选择 machine.*.example.json，复制为 machine.local.json，填写 Stata 路径。
3. 在项目根目录运行 `python3 run.py --task demo`，查看 outputs/demo__<run_id>/run.json、logs/、tables/ 和 samples/。

原始数据在 data_raw/，中间数据在 data_intermeidate/，分析数据在 data_analysis/；前两层不入Git，分析数据纳入Git。实际提交和远程推送由使用者执行。

内部 code/90_qa/ 按作者要求不在此包，生产入口不依赖它。status=PASS 表示已登记生产任务与必需产物完成；qa_status=NOT_RUN 表示内部检查未运行，不能据此声称内部QA通过。

如在服务器运行，保持相同根目录结构；服务器代码修改/同步须获得 项目负责人 本次同意，执行后核对实际代码版本。此公开包不提供自动服务器连接或上传。
