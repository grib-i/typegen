from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import yaml

from .core.loader import load_structured_file

DEFAULT_CONFIG: dict[str, Any] = {
    "output_dir": ".typegen/types",
    "package_name": "_typegen",
    "inputs": [
        "*.json",
        "*.yaml",
        "*.yml",
        "*.toml",
    ],
    "exclude": [
        ".typegen/**",
        ".venv/**",
        "venv/**",
        "__pycache__/**",
    ],
}


def read_project_config(path: str | Path) -> dict[str, Any]:
    path = Path(path)

    if not path.exists():
        return copy.deepcopy(DEFAULT_CONFIG)

    data = load_structured_file(path)
    if not isinstance(data, dict):
        raise ValueError(f"Config must be a mapping: {path}")

    cfg = copy.deepcopy(DEFAULT_CONFIG)
    cfg.update(data)
    return cfg


def write_project_config(path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        return

    path.write_text(
        yaml.safe_dump(DEFAULT_CONFIG, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def write_pyright_config(path: str | Path) -> None:
    path = Path(path)

    if path.exists():
        return

    path.write_text(
        json.dumps({"extraPaths": [".typegen/types"]}, indent=4),
        encoding="utf-8",
    )
