#!/usr/bin/env python3
"""离线生成代码同步差异或当前目录快照；不连接服务器，不传输文件。"""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone, timedelta
from pathlib import Path
from project_layout import RunLayout

ROOT = Path(__file__).resolve().parent
TZ = timezone(timedelta(hours=8))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve(value):
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def snapshot(config):
    files = {}
    for rel in config["sync_paths"]:
        source = resolve(rel)
        if not source.is_relative_to(ROOT):
            raise ValueError("sync_paths 必须位于项目根目录内。")
        if not source.exists():
            raise FileNotFoundError(source)
        candidates = source.rglob("*") if source.is_dir() else [source]
        for path in candidates:
            if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store":
                key = path.relative_to(ROOT).as_posix()
                files[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"schema_version": 1, "captured_at": datetime.now(TZ).isoformat(timespec="seconds"),
            "captured_host": platform.node(), "root": str(ROOT), "server_id": config.get("server_id"),
            "scope": "filesystem snapshot on this host; not a live remote check",
            "files": dict(sorted(files.items())), "sync_paths": config["sync_paths"],
            "required_root_dirs": config["required_root_dirs"],
            "missing_root_dirs": [rel for rel in config["required_root_dirs"] if not (ROOT / rel).is_dir()],
            "unexpected_project_wrapper": (ROOT / "project").is_dir()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["plan", "snapshot"])
    parser.add_argument("--config", default="config/server.local.json")
    parser.add_argument("--date")
    parser.add_argument("--edition", type=int)
    args = parser.parse_args()
    layout = RunLayout(ROOT, f"server_sync_{args.action}", "00_setup", args.date, args.edition)
    manifest_path = layout.provenance / f"server_manifest_{layout.version}.json"
    try:
        config_path = resolve(args.config)
        if not config_path.exists() and args.config == "config/server.local.json":
            config_path = ROOT / "config/server.example.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if config.get("approval_required") is not True:
            raise ValueError("服务器操作必须保留 Zhangchi 的审批要求，不能禁用 approval_required。")
        local = snapshot(config)
        write(manifest_path, local)
        if args.action == "snapshot":
            result = {"status": "SNAPSHOT_CREATED", "manifest": str(manifest_path),
                      "remote_connection_made": False, "files_transferred": 0}
        elif not config.get("enabled", False):
            result = {"status": "NOT_APPLICABLE", "reason": "本项目尚未启用服务器协作。",
                      "remote_connection_made": False, "files_transferred": 0}
        else:
            baseline_path = resolve(config["last_remote_manifest"])
            remote = json.loads(baseline_path.read_text()) if baseline_path.is_file() else None
            if remote and remote.get("server_id") != config.get("server_id"):
                raise ValueError("远端快照的 server_id 与当前服务器登记不一致。")
            if remote and (remote.get("sync_paths") != config["sync_paths"] or remote.get("required_root_dirs") != config["required_root_dirs"]):
                raise ValueError("快照范围或目录规范已变化，需重新采集经过授权的远端快照。")
            previous = remote.get("files", {}) if remote else {}
            files = local["files"]
            changes = {"added": sorted(set(files) - set(previous)),
                       "modified": sorted(path for path in set(files) & set(previous) if files[path] != previous[path]),
                       "removed": sorted(set(previous) - set(files))}
            if local["missing_root_dirs"] or local["unexpected_project_wrapper"]:
                state = "LOCAL_LAYOUT_INCOMPLETE"
            elif remote is None:
                state = "REMOTE_UNVERIFIED_PENDING_APPROVAL"
            elif remote.get("missing_root_dirs") or remote.get("unexpected_project_wrapper"):
                state = "REMOTE_LAYOUT_MISMATCH_PENDING_APPROVAL"
            elif any(changes.values()):
                state = "PENDING_APPROVAL"
            else:
                state = "MATCHES_LAST_RECORDED_REMOTE_SNAPSHOT"
            result = {"status": state, "server_id": config.get("server_id"),
                      "server_root": config.get("server_root"), "changes": changes,
                      "remote_snapshot": str(baseline_path) if remote else None,
                      "comparison_basis": "last supplied remote snapshot; remote state not inspected live",
                      "local_missing_root_dirs": local["missing_root_dirs"],
                      "remote_missing_root_dirs": remote.get("missing_root_dirs", []) if remote else None,
                      "approval_required_before_remote_actions": True,
                      "remote_connection_made": False, "files_transferred": 0}
        result.update({"date": layout.date, "edition": layout.edition, "version": layout.version})
        write(layout.file("qa", "server_plan", ".json"), result)
        write(layout.record, result)
        layout.status_file.write_text(result["status"] + "\n")
        layout.file("logs", "server_plan", ".log").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(f"{result['status']}\n记录：{layout.record}")
        return 0
    except Exception as error:
        layout.status_file.write_text("FAIL\n")
        write(layout.record, {"status": "FAIL", "version": layout.version, "error": str(error)})
        layout.file("logs", "server_plan_error", ".log").write_text(str(error) + "\n")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
