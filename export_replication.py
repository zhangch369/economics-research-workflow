#!/usr/bin/env python3
"""按明确清单导出生产复现包；排除内部 QA、聊天和工作日志。"""
import hashlib
import json
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT


def main():
    version = datetime.now(timezone(timedelta(hours=8))).strftime("%Y%m%d_%H%M%S") + "_" + uuid4().hex[:8]
    out = ROOT / "outputs" / f"export_replication__{version}"
    (out / "logs").mkdir(parents=True)
    status = out / "STATUS.txt"
    status.write_text("RUNNING\n")
    try:
        config = json.loads((ROOT / "config/replication_export.json").read_text())
        tasks = json.loads((ROOT / "config/tasks.json").read_text())
        public_tasks = {}
        for name in config["tasks"]:
            task = {k: v for k, v in tasks[name].items() if k not in {"qa_entry", "qa_expected"}}
            if not task.get("enabled"):
                raise ValueError(f"不能导出尚未启用的任务：{name}")
            public_tasks[name] = task
        files = []
        for file in sorted((ROOT / "code").rglob("*")):
            if file.is_file() and not {"90_qa", "__pycache__"}.intersection(file.relative_to(ROOT / "code").parts):
                files.append((file, file.relative_to(ROOT).as_posix()))
        for rel in ["run.py", "management/DATA_REGISTRY.csv", "management/SPECIFICATIONS.csv", "management/EXHIBITS.csv"]:
            files.append((ROOT / rel, rel))
        for file in (ROOT / "config").glob("machine.*.example.json"):
            files.append((file, "config/" + file.name))
        files.append((WORKSPACE / ".gitignore", ".gitignore"))
        for rel in config["raw_files"]:
            files.append((WORKSPACE / "data_raw" / rel, "data_raw/" + rel))
        for data_version in config["analysis_versions"]:
            folder = WORKSPACE / "data_analysis" / data_version
            if not folder.is_dir():
                raise FileNotFoundError(folder)
            files.extend((file, "data_analysis/" + file.relative_to(WORKSPACE / "data_analysis").as_posix())
                         for file in sorted(folder.rglob("*")) if file.is_file())
        archive = ROOT / "releases" / f"replication__{version}.zip"
        archive.parent.mkdir(exist_ok=True)
        manifest = []
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            for source, destination in files:
                content = source.read_bytes()
                z.writestr("economics_workspace/" + destination, content)
                manifest.append({"path": destination, "sha256": hashlib.sha256(content).hexdigest()})
            z.writestr("economics_workspace/config/tasks.json", json.dumps(public_tasks, ensure_ascii=False, indent=2))
            z.writestr("economics_workspace/README.md", (ROOT / "management/PUBLIC_REPLICATION_README.md").read_text())
            z.writestr("economics_workspace/AGENTS.md", "# AI 复现入口\n\n先读 README.md 和 config/tasks.json。仅运行已登记生产任务。本包不含内部 code/90_qa；run.json 中 qa_status=NOT_RUN，不作内部 QA 已通过的声明。\n")
            z.writestr("economics_workspace/data_analysis/.gitkeep", "")
            z.writestr("economics_workspace/project.json", json.dumps({
                "schema_version": 3, "package_type": "public_replication", "scope": config["scope"],
                "command": "python3 run.py --task demo", "internal_qa_included": False,
                "analysis_versions": config["analysis_versions"]}, ensure_ascii=False, indent=2))
            z.writestr("economics_workspace/EXPORT_MANIFEST.json", json.dumps({
                "scope": config["scope"], "internal_qa_included": False,
                "analysis_versions": config["analysis_versions"], "source_files": manifest}, ensure_ascii=False, indent=2))
        (out / "logs/export.log").write_text(f"Archive: {archive}\nSource files: {len(files)}\nInternal QA: excluded\n")
        (out / "export.json").write_text(json.dumps({"status": "PASS", "archive": str(archive), "files": len(files), "internal_qa_included": False}, ensure_ascii=False, indent=2) + "\n")
        status.write_text("PASS\n")
        print(archive)
        return 0
    except Exception as error:
        status.write_text("FAIL\n")
        (out / "logs/export.log").write_text(str(error) + "\n")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
