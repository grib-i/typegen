from __future__ import annotations

from pathlib import Path

from ..config import write_project_config, write_pyright_config


def init_command(force: bool = False) -> None:
    typegen_dir = Path(".typegen")
    types_dir = typegen_dir / "types"
    config_path = typegen_dir / "config.yaml"
    pyright_path = Path("pyrightconfig.json")

    types_dir.mkdir(parents=True, exist_ok=True)

    if force or not config_path.exists():
        write_project_config(config_path)

    if force or not pyright_path.exists():
        write_pyright_config(pyright_path)

    print("Initialized typegen")
    print(f"Created {config_path}")
    print(f"Created {pyright_path}")
