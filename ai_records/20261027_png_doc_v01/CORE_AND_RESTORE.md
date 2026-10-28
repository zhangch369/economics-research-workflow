# 图片PNG与回归表DOC

2026-10-27，用户要求：规定图片输出只需要png，回归表格只需要doc，更新项目。

已实现：任务MAIN_FIGURE改.png，MAIN_TABLE改.doc并标明kind；Stata直接graph export PNG，回归后outreg2,word；全表列完成后精确删除同名临时TXT。路径工具拒绝其他图表格式。日志、QA文本及历史结果不批量删除。

恢复：读AGENTS、OUTPUT_LAYOUT、config/tasks.json和FORMAT_VALIDATION_20261027_v01.json。新版图表为日期版次命名；源模板合成示例与迁移/公开包等7项检查通过，数值与样本一致。未修改任何真实研究规格或服务器。
