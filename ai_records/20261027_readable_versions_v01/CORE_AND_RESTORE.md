# NUSTP参照的分类与可读版次

日期：2026-10-27；当前聊天01a17b31-c3f4-7c62-a9d0-b873ab1cee64。

用户要求：结合NUSTP更新模板，禁止用乱码/随机后缀分类版本；输出文件直接写日期和版次；中间和分析数据分类完全对应code；outputs先按tables/figures/logs等用途分类。补充要求及时提醒清理完全不需要的txt、废弃输出，不生成任何随机后缀文件夹。

已执行：本模板采用NUSTP论文专题目录；project_layout.py提供日期版次与目录镜像，三个入口改用新布局，Stata通过明确产物宏保存数据和输出。旧合成分析数据仅归位、内容哈希未变。NUSTP本体只读，没有迁移或重跑。

恢复：先读AGENTS、project.json、management/STATUS、DATA_LAYOUT和OUTPUT_LAYOUT；登记和产物路径在config/tasks.json与outputs/runs/<任务>/run_YYYYMMDD_vNN.json。实际验收management/VALIDATION_20261027_v01.json。内部QA继续在code/90_qa，公开包排除且可以独立运行。

提醒沿用每周五17:00，另要求任务结束列清理候选。已有版次不覆盖；对外包中已存在的分析版本会触发新运行选新一版。失败记录保留，旧包和废弃测试包在CLEANUP中标候选，未直接删除用户文件。
