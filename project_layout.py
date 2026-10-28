"""共享目录规则：类型优先、代码目录镜像、日期与可读版次，不生成随机版本名。"""
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

TZ = timezone(timedelta(hours=8))
CATEGORIES = ("tables", "figures", "logs", "estimates", "samples", "qa", "provenance", "runs")
DATA_AREAS = ("intermediate", "analysis")


def now():
    return datetime.now(TZ).isoformat(timespec="seconds")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve(root, value):
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def code_directories(root):
    code = root / "code"
    return sorted(p.relative_to(code) for p in code.rglob("*")
                  if p.is_dir() and "__pycache__" not in p.parts and not p.name.startswith("."))


def data_module(spec):
    area = spec["area"]
    if area not in DATA_AREAS:
        raise ValueError(f"不是派生数据产物：{area}")
    value = spec.get("data_module")
    if not value:
        raise ValueError("中间和分析数据产物必须显式登记data_module。")
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("data_module必须是项目数据根目录内的相对路径。")
    return rel


def registered_data_directories(task):
    directories = {area: set() for area in DATA_AREAS}
    for area, values in task.get("data_directories", {}).items():
        if area not in DATA_AREAS:
            raise ValueError(f"未知数据层：{area}")
        for value in values:
            rel = Path(value)
            if rel.is_absolute() or ".." in rel.parts:
                raise ValueError("数据目录必须是数据根目录内的相对路径。")
            directories[area].add(rel)
    for spec in task.get("artifacts", {}).values():
        if spec.get("area") in DATA_AREAS:
            directories[spec["area"]].add(data_module(spec))
    return directories


def mirror_data_directories(data_roots, task):
    for area, directories in registered_data_directories(task).items():
        for rel in directories:
            (data_roots[area] / rel).mkdir(parents=True, exist_ok=True)


class RunLayout:
    def __init__(self, root, task, module="00_setup", date=None, edition=None, reserved_versions=()):
        self.root = Path(root).resolve()
        if not re.fullmatch(r"[A-Za-z0-9_-]+", task):
            raise ValueError("任务名只用可读英文、数字、下划线或连字符。")
        self.task = task
        self.module = Path(module)
        if self.module.is_absolute() or ".." in self.module.parts or not (self.root / "code" / self.module).is_dir():
            raise ValueError(f"模块必须对应实际code目录：{module}")
        self.date = date or datetime.now(TZ).strftime("%Y%m%d")
        if not re.fullmatch(r"\d{8}", self.date):
            raise ValueError("日期必须是8位YYYYMMDD。")
        datetime.strptime(self.date, "%Y%m%d")
        if edition is not None and edition < 1:
            raise ValueError("版次必须是正整数。")
        records = self.root / "outputs/runs" / task
        records.mkdir(parents=True, exist_ok=True)
        candidate = edition or 1
        while True:
            version = f"{self.date}_v{candidate:02d}"
            if version in reserved_versions:
                if edition is not None:
                    raise ValueError(f"该版次已有数据或产物，不能覆盖：{version}")
                candidate += 1
                continue
            record = records / f"run_{version}.json"
            try:
                with record.open("x", encoding="utf-8") as handle:
                    json.dump({"status": "STARTING", "task": task, "version": version}, handle)
                break
            except FileExistsError:
                if edition is not None:
                    raise ValueError(f"该日期版次已使用，不能覆盖：{record}")
                candidate += 1
        self.edition = candidate
        self.version = version
        self.run_id = f"{task}_{version}"
        self.record = record
        for category in CATEGORIES:
            (self.root / "outputs" / category).mkdir(parents=True, exist_ok=True)
        self.provenance = self.root / "outputs/provenance" / self.module / self.run_id
        self.provenance.mkdir(parents=True, exist_ok=False)
        self.logs = self.directory("logs")
        self.status_file = self.file("runs", "status", ".txt")

    def directory(self, category, module=None):
        if category not in CATEGORIES:
            raise ValueError(category)
        rel = Path(module) if module is not None else self.module
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError("分类路径必须是项目内相对路径。")
        directory = self.root / "outputs" / category / rel
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def file(self, category, stem, suffix, module=None):
        return self.directory(category, module) / f"{stem}_{self.task}_{self.version}{suffix}"

    def artifact(self, spec, data_roots):
        area, module = spec["area"], Path(spec["module"])
        if (area == "figures" or spec.get("kind") == "figure") and spec["suffix"].lower() != ".png":
            raise ValueError("图片输出只允许PNG。")
        if spec.get("kind") == "regression_table" and spec["suffix"].lower() != ".doc":
            raise ValueError("回归表输出只允许DOC。")
        if module.is_absolute() or ".." in module.parts or not (self.root / "code" / module).is_dir():
            raise ValueError(f"产物模块必须对应实际code目录：{module}")
        name = f"{spec['stem']}_{self.task}_{self.version}{spec['suffix']}"
        if area in DATA_AREAS:
            directory = data_roots[area] / data_module(spec)
            directory.mkdir(parents=True, exist_ok=True)
            return directory / name
        return self.directory(area, module) / name
