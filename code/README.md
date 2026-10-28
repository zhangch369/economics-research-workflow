# 按论文结构找代码

00_setup：运行环境；01_data_preparation/01_clean：清洗；01_data_preparation/02_build：构建分析数据；02_main_regressions：主回归和图表；03_robustness：稳健性；04_mechanisms：机制；05_extensions：拓展。90_qa内部检查，不进入公开包。

此分类参照NUSTP。实际任务可在专题下增加有意义的研究线子目录，并让data_intermeidate和data_analysis逐级镜像；不能用随机串替代版本。文件与输出标注日期版次。主入口显式列执行顺序，图表直接在对应分析脚本导出。
