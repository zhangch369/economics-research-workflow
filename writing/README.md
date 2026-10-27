# 写作工作区

论文放 `manuscript/`；组会、答辩和会议汇报放 `presentations/`。按用途保存，再按源格式区分。

```text
writing/
├── manuscript/
│   ├── word/                 当前 .docx 源稿
│   └── latex/                main.tex、章节、样式
├── presentations/
│   ├── beamer/               main.tex、章节、样式
│   └── pptx/                 当前 .pptx 源稿
├── shared/
│   ├── references/           .bib、引用说明
│   ├── tables/               从已接受运行导入的表
│   └── figures/              从已接受运行导入的图
├── releases/<写作版本>/      定稿源文件、PDF/PPT成品和版本清单
└── VERSIONS.csv
```

同一篇论文可同时有 Word/LaTeX，但在 VERSIONS.csv 标明当前主编辑版本；两者不会自动同步。Beamer 和 PPT 也分别登记。写作 agent 先查表图的 spec_id/run_id，再引用结果；不要读取随时间变化的“最新”文件夹。

每次汇报、投递或重要定稿留一个 release：源文件、必要素材、导出 PDF（适用时保留 PPTX）、引用库、字体/编译器信息、对应数据与运行版本。不复制整套原始数据。表图从哪个运行目录取来，在 ASSETS.csv 逐项登记；共享素材更新后，旧 release 仍保留原素材。

Word/PPT 的编辑过程可使用本机备份与版本历史；重要里程碑保存不可覆盖的版本。LaTeX/Beamer 的 `.tex`、`.bib` 适合 Git；编译辅助文件和临时缓存可重建。新建本地 LaTeX 项目时放在对应子目录的独立项目文件夹，保留 main.tex 与相对路径素材。

定稿验收：打开实际文件检查表图、公式、分页和字体；只验证源文件存在不算成品验收。
