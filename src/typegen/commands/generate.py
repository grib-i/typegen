from __future__ import annotations

import copy
import glob
from pathlib import Path
from typing import Any

from ..config import DEFAULT_CONFIG, read_project_config
from ..core.generator import generate_stub_for_file
from ..core.loader import SUPPORTED_SUFFIXES


def _is_glob_pattern(text: str) -> bool:
    return any(ch in text for ch in "*?[]")


def _matches_exclude(path: Path, exclude: list[str]) -> bool:
    rel = path.as_posix()
    return any(Path(rel).match(pattern) for pattern in exclude)


def _expand_target(item: str | Path) -> list[Path]:
    raw = str(item)
    path = Path(raw)

    if _is_glob_pattern(raw):
        return [Path(p) for p in glob.glob(raw, recursive=True) if Path(p).is_file()]

    if path.is_dir():
        out: list[Path] = []
        for suffix in SUPPORTED_SUFFIXES:
            out.extend(path.rglob(f"*{suffix}"))
        return sorted({p.resolve() for p in out})

    if path.is_file():
        return [path]

    return []


def _resolve_targets(raw_targets: list[str], exclude: list[str]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()

    for item in raw_targets:
        for path in _expand_target(item):
            resolved = path.resolve()
            if resolved in seen:
                continue
            if _matches_exclude(path, exclude):
                continue
            if path.suffix.lower() not in SUPPORTED_SUFFIXES:
                continue

            seen.add(resolved)
            files.append(path)

    return files


def generate_command(
    targets: list[str],
    config_path: str | Path = ".typegen/config.yaml",
    output_dir: str | Path | None = None,
    package_name: str | None = None,
) -> int:
    config_path = Path(config_path)

    if config_path.exists():
        cfg = read_project_config(config_path)
    elif config_path != Path(".typegen/config.yaml"):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    else:
        cfg = copy.deepcopy(DEFAULT_CONFIG)

    if output_dir is not None:
        cfg["output_dir"] = output_dir

    if package_name is not None:
        cfg["package_name"] = package_name

    if not targets:
        targets = list(cfg.get("inputs", []))

    files = _resolve_targets(targets, exclude=list(cfg.get("exclude", [])))

    if not files:
        print("No input files found")
        return 1

    for source in files:
        generate_stub_for_file(
            source=source,
            output_dir=cfg["output_dir"],
            package_name=cfg["package_name"],
        )

    print(
        f"Generated {len(files)} file(s) into {cfg['output_dir']}/{cfg['package_name']}"
    )
    return 0
