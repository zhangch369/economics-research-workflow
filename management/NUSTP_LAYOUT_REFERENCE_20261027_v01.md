# NUSTP分类经验与本模板适配

核实日期：2026-10-27。只读来源：/Users/zhangchi/Desktop/NUSTP/AGENTS.md、README.md、code/README.md、management/STATUS.md、VERSION_RELATIONSHIPS.md及目录。

NUSTP当前按论文部分组织：01_data_preparation内分01_clean和02_build；随后02_main_regressions、03_robustness、04_mechanisms、05_extensions。专题内部可继续区分legacy_may/revised，不能机械要求每个专题拆成完全相同流程。00_setup运行辅助，90_qa内部检查。

本模板采用相同的可读专题顺序，并把数据逐级镜像到两层数据目录；输出先按tables/figures/logs等用途，再按模块。版本直接标在文件名，例如20261027_v01；不使用UUID/随机后缀目录。

NUSTP实际情况：outputs已有tables/figures/logs/other一级分类，数据层仍可见多份时间加随机后缀的旧运行目录。这是此次设计改进的依据，不表示本任务已经迁移NUSTP。NUSTP的五月保留版、EJ稿与候选修改线继续由其本项目登记管理，本模板不替其选择研究方案。

本次交付仅修改当前economics_workspace和模板包；没有写入NUSTP、重跑真实回归或连接服务器。后续若要求应用到NUSTP，需要另列原路径到新路径映射、依赖与逐项验收。
