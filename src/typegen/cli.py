from __future__ import annotations

import argparse

from .commands.generate import generate_command
from .commands.init import init_command


def main() -> None:
    parser = argparse.ArgumentParser(prog="typegen")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize .typegen config")
    p_init.add_argument("--force", action="store_true", help="Overwrite config files")

    p_gen = sub.add_parser("generate", help="Generate .pyi stubs")
    p_gen.add_argument(
        "targets", nargs="*", help="Files, directories, or glob patterns"
    )
    p_gen.add_argument(
        "-c", "--config", default=".typegen/config.yaml", help="Project config path"
    )
    p_gen.add_argument("-o", "--output", default=None, help="Override output dir")
    p_gen.add_argument(
        "-p", "--package-name", default=None, help="Override generated package name"
    )

    args = parser.parse_args()

    if args.command == "init":
        init_command(force=args.force)
        return

    if args.command == "generate":
        raise SystemExit(
            generate_command(
                targets=args.targets,
                config_path=args.config,
                output_dir=args.output,
                package_name=args.package_name,
            )
        )
