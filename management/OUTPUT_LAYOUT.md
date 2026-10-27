# 输出分类规则

所有语言按文件用途分类，先按任务和运行编号归档。Stata、outreg2、Python 共用以下布局：

```text
outputs/<任务>__<运行编号>/
├── run.json、STATUS.txt 等  运行元信息与状态
├── logs/                   启动、执行、控制台与错误日志
├── tables/                 回归表、描述统计等研究表格
├── figures/                研究图形及可编辑图形文件
├── estimates/              .ster 等估计对象
├── samples/                实际估计样本键和 e(sample)
├── qa/                     检查报告、指标、诊断图表
└── provenance/             代码配置快照、指纹、变更清单和修改前备份
```

日志与研究图表必须分开，禁止图表落入 logs 或运行根目录。按用途而非扩展名分类：outreg2 的 .txt 属于 tables，控制台 .txt 属于 logs，检查指标 .csv 属于 qa。QA 图表可放 qa/tables、qa/figures，QA 执行日志仍在 logs。

Stata 启动工作目录仍设为本次 logs，所有导出必须显式指定路径。回归后立即 outreg2 using "$OUT/tables/table1.txt"；绘图后 graph export "$OUT/figures/figure1.pdf"，graph save 的 .gph 也放 figures。路径为示例，不是独立运行脚本。

Python 输出研究表时使用 out / "tables" / "summary.csv"，savefig 使用 out / "figures" / "figure1.png"，logging 和 stdout/stderr 保存到 logs；创建所需目录后再导出。Python 不替代正式 Stata 面板整理。

清洗、中间和分析数据继续放既定三层数据目录；论文/汇报源稿和正式成品放 writing。辅助打包/同步任务按需建立分类目录，特殊产物使用明确用途名称，不建立含混的杂物目录。

验收：实际输出、config/tasks.json 中 expected、EXHIBITS 与写作引用路径一致；日志与研究表图分离。现有 run.py 已创建上述分类，示例 outreg2 已指向 tables；本次新增跨语言明确规则，不声称实现了自动路径拦截。
