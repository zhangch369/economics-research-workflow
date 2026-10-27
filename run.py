#!/usr/bin/env python3
"""只负责启动、留档和验收；正式数据整理与估计全部由 Stata 完成。"""
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parent
TZ = timezone(timedelta(hours=8))


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_path(value):
    p = Path(value).expanduser()
    return p.resolve() if p.is_absolute() else (ROOT / p).resolve()


def stata_path(path):
    value = path.as_posix()
    if any(char in value for char in ['"', '`', '$', '\n', '\r']):
        raise ValueError("Stata 路径中不能包含引号、反引号、美元符号或换行。")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", default="demo")
    parser.add_argument("--profile", default="config/machine.local.json")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", args.task):
        parser.error("任务名称仅使用英文字母、数字、下划线和连字符。")
    run_id = datetime.now(TZ).strftime("%Y%m%d_%H%M%S") + "_" + uuid4().hex[:8]
    out = ROOT / "outputs" / f"{args.task}__{run_id}"
    for folder in ["logs", "qa", "tables", "figures", "estimates", "samples", "provenance"]:
        (out / folder).mkdir(parents=True, exist_ok=False)
    record = {"status": "RUNNING", "task": args.task, "run_id": run_id,
              "started_at": now(), "project_root": str(ROOT),
              "host": platform.node(), "os": platform.platform(),
              "python": sys.version, "python_executable": sys.executable}
    proc = None

    def update(status, error=None):
        record["status"] = status
        if status != "RUNNING":
            record["ended_at"] = now()
        if error:
            record["error"] = error
        write_json(out / "run.json", record)
        (out / "STATUS.txt").write_text(status + "\n", encoding="utf-8")

    def interrupted(signum, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupted)
    update("RUNNING")
    print(f"运行记录：{out}", flush=True)
    try:
        profile = json.loads(resolve_path(args.profile).read_text(encoding="utf-8"))
        tasks = json.loads((ROOT / "config/tasks.json").read_text(encoding="utf-8"))
        task = tasks[args.task]
        if not task.get("enabled", False):
            raise RuntimeError("该任务尚未接入真实数据与验收规则，不能标记为正式完成。")
        stata = resolve_path(profile["stata_bin"])
        if not stata.is_file():
            raise FileNotFoundError(f"请在机器配置中填写 Stata 可执行文件：{stata}")
        data_roots = {
            "raw": resolve_path(profile.get("data_raw_root", "data_raw")),
            "intermediate": resolve_path(profile.get("data_intermediate_root", "data_intermeidate")),
            "analysis": resolve_path(profile.get("data_analysis_root", "data_analysis")),
        }
        if len(set(data_roots.values())) != 3:
            raise ValueError("三层数据必须使用独立目录；请检查机器配置。")
        intermediate = data_roots["intermediate"] / run_id
        analysis = data_roots["analysis"] / run_id
        intermediate.mkdir(parents=True, exist_ok=False)
        analysis.mkdir(parents=True, exist_ok=False)
        record.update({"data_roots": {k: str(v) for k, v in data_roots.items()}, "data_version": run_id,
                       "stata_bin": str(stata), "entry": task["entry"],
                       "scope": task["scope"], "seed": 20261027, "processors": 1,
                       "qa_entry": task.get("qa_entry"), "qa_status": "NOT_RUN"})
        inputs = []
        for item in task["inputs"]:
            path = data_roots[item["area"]] / item["path"]
            inputs.append({**item, "bytes": path.stat().st_size, "sha256": sha256(path)})
        write_json(out / "provenance/inputs.json", inputs)
        shutil.copytree(ROOT / "code", out / "provenance/code")
        shutil.copy2(__file__, out / "provenance/run.py")
        write_json(out / "provenance/task.json", task)
        context = out / "provenance/context"
        for rel in ["AGENTS.md", "project.json", "management/STATUS.md", "management/DATA_REGISTRY.csv",
                    "management/SPECIFICATIONS.csv", "management/EXHIBITS.csv"]:
            source = ROOT / rel
            if source.is_file():
                target = context / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        # 不读取整份环境变量；机器配置只允许路径和启动参数，不存凭据。
        write_json(out / "provenance/machine.json", {
            k: profile[k] for k in ("stata_bin", "data_raw_root", "data_intermediate_root", "data_analysis_root", "batch_flag") if k in profile
        })
        snapshot = out / "provenance/code"
        code_manifest = [{"path": str(p.relative_to(snapshot)), "sha256": sha256(p)}
                         for p in sorted(snapshot.rglob("*")) if p.is_file()]
        write_json(out / "provenance/code_manifest.json", code_manifest)
        values = {"PROJECT": ROOT, "CODE": snapshot, "RAW": data_roots["raw"],
                  "INTERMEDIATE": intermediate, "ANALYSIS": analysis, "OUT": out}
        wrapper = out / "logs/entry.do"
        lines = ["version 18.0", "clear all", "set more off", "set varabbrev off",
                 "set seed 20261027", "set sortseed 20261027",
                 'if c(MP) == 1 set processors 1']
        lines += [f'global {key} "{stata_path(value)}"' for key, value in values.items()]
        lines += ['capture log close _all',
                  'log using "$OUT/logs/analysis.log", text name(runlog)',
                  f'capture noisily do "{stata_path(snapshot / task["entry"])}"',
                  'local stata_rc = _rc']
        if task.get("qa_entry"):
            lines += ['if `stata_rc\' == 0 {',
                      f'    capture noisily do "{stata_path(snapshot / task["qa_entry"])}"',
                      '    local stata_rc = _rc',
                      '    file open qastate using "$OUT/QA_STATUS.txt", write text',
                      '    if `stata_rc\' == 0 file write qastate "PASS" _n',
                      '    else file write qastate "FAIL" _n',
                      '    file close qastate', '}']
        lines += [
                  'file open rcfile using "$OUT/STATA_RC.txt", write text',
                  'file write rcfile "`stata_rc\'" _n', 'file close rcfile',
                  'log close runlog', 'exit `stata_rc\', clear']
        wrapper.write_text("\n".join(lines) + "\n", encoding="utf-8")
        default_flag = "/e" if os.name == "nt" else ("-e" if sys.platform == "darwin" else "-b")
        # Stata 会再次解析 do 后面的命令文本；保留引号以支持目录中的空格。
        command = [str(stata), profile.get("batch_flag", default_flag), "do", f'"{stata_path(wrapper)}"']
        record["command"] = command
        update("RUNNING")
        # Stata 启动日志也落在本次 logs；不依赖调用者的工作目录。
        with (out / "logs/console.log").open("w", encoding="utf-8") as console:
            proc = subprocess.Popen(command, cwd=out / "logs", stdout=console, stderr=subprocess.STDOUT)
            record["process_returncode"] = proc.wait()
        rcfile = out / "STATA_RC.txt"
        record["stata_returncode"] = int(rcfile.read_text().strip()) if rcfile.exists() else None
        qa_status_file = out / "QA_STATUS.txt"
        if qa_status_file.exists():
            record["qa_status"] = qa_status_file.read_text().strip()
        if record["process_returncode"] != 0 or record["stata_returncode"] != 0:
            raise RuntimeError("Stata 未成功结束；查看 logs/entry.log 与 logs/analysis.log。")
        locations = {"intermediate": intermediate, "analysis": analysis, "output": out}
        output_manifest = []
        expected = task["expected"] + (task.get("qa_expected", []) if task.get("qa_entry") else [])
        for item in expected:
            path = locations[item["area"]] / item["path"]
            if not path.is_file() or path.stat().st_size == 0:
                raise RuntimeError(f"缺失必需产物：{path}")
            output_manifest.append({**item, "bytes": path.stat().st_size, "sha256": sha256(path)})
        if task.get("qa_entry"):
            if (out / "qa/QA_PASS.txt").read_text().strip() != "PASS":
                raise RuntimeError("独立 QA 未通过。")
            record["qa_status"] = "PASS"
        write_json(out / "provenance/outputs.json", output_manifest)
        update("PASS")
        message = "PASS：生产任务与内部 QA 完成。" if record["qa_status"] == "PASS" else "PASS：生产任务完成；内部 QA 未运行。"
        print(message, flush=True)
        return 0
    except KeyboardInterrupt:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
        update("INTERRUPTED", "运行被中断；保留当前日志与部分产物。")
        return 130
    except Exception as exc:
        update("FAIL", str(exc))
        (out / "logs/launcher_error.log").write_text(str(exc) + "\n", encoding="utf-8")
        print(f"FAIL：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
