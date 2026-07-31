from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

import yaml

SUPPORTED_SUFFIXES = {".json", ".yaml", ".yml", ".toml"}


def load_structured_file(path: str | Path) -> Any:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")
    suffix = path.suffix.lower()

    if suffix == ".json":
        return json.loads(text)

    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)

    if suffix == ".toml":
        return tomllib.loads(text)

    raise ValueError(f"Unsupported format: {suffix}")
