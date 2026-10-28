# 服务器协作：同一目录设计，代码变更先审批后同步

如果项目有服务器运行的代码，本机与服务器使用相同根目录结构：code、config、data_raw、data_intermediate、data_analysis、outputs、management、research_notes、writing、ai_records 等同级；不增加 project/ 包裹层。绝对根路径和软件安装位置可以不同，由各自私有机器配置提供。数据内容按任务需要传输，数据版本与相对路径要对应。

## 每次本机代码变更后的流程

1. 更新代码、任务入口和有关说明，运行本地适用检查。然后执行 `python3 server_sync.py plan`，把变更与上次记录的远端快照比较，保存新增/修改/移除文件清单。新代码未同步时，状态明确记为待同步。
2. 向 Zhangchi 展示服务器标识、目标根目录、具体文件差异、是否涉及覆盖/删除、已有服务器任务和验证办法。**必须等 Zhangchi 同意本次同步后，才连接服务器、上传或修改代码。** 本模板不是持续授权；新的一批变更需要新的同步同意。已经明确授权的具体范围不重复询问。
3. 获同意后，在授权范围内同步相同相对路径；保留远端旧代码版本，先核对服务器已有改动与运行任务，避免覆盖未保留工作。目录结构保持同本机一致。同步代码不自动扩展为重新采集、重建数据或重跑回归；需要运行时按授权范围执行。
4. 在服务器采集同步后的代码指纹与目录快照，回传本机并核对；验证适用的服务器任务后记录代码版本、数据版本、结果和同步状态。没有实际远端验证时不能写“同步完成”。
5. 更新 management/STATUS.md、SERVER_SYNC_LOG.csv 和有关 AI 恢复卡；下一位 agent 能看到本机/服务器版本是否一致、尚有哪些变更待同步。

## 最小配置与离线工具

把 config/server.example.json 复制为私有的 server.local.json；有服务器任务时设置 enabled、server_id、server_root。保留 approval_required=true。机器私有配置不入 Git，也不进入对外复现包；示例本身不含真实地址或凭据。

`server_sync.py` 只有两个动作：plan 离线列差异，snapshot 读取**当前机器**的目录和代码生成清单。它不建立网络连接、不上传、不改远端。只有获得本次操作同意后，agent 才可在服务器执行 snapshot 并取回清单。不要把本机采集的清单称为真实远端证据。

上次远端清单保存路径由 last_remote_manifest 指定；尚未取得时 plan 显示 REMOTE_UNVERIFIED_PENDING_APPROVAL。本机有差异时显示 PENDING_APPROVAL；远端目录缺失时显示 REMOTE_LAYOUT_MISMATCH_PENDING_APPROVAL。MATCHES_LAST_RECORDED_REMOTE_SNAPSHOT 仅表示与**已记录**快照一致，不证明服务器实时状态。

为覆盖真实服务器管线，sync_paths 须包含其所有生产程序、公共启动器及任务配置；若增加依赖路径，要同时更新范围并重新采集经授权的远端快照。不得把私人密钥、机器配置或整套数据误放入代码同步清单。

未启用服务器协作的项目，plan 返回 NOT_APPLICABLE。科技园等项目既有的服务器授权限制继续适用。

所有新生成的计划、日志和快照按outputs类型分类，文件标日期版次；工具不再创建随机运行目录。路径布局更改后需在用户同意的同步范围中一并更新，仍不得直接连接服务器。
