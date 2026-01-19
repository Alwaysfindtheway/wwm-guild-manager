"""Entry point for the WWM guild manager application.

This is a lightweight bootstrap that will later delegate to the GUI layer.
For now it validates inputs and prints the intended startup mode.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the app bootstrap."""

    config_path: Path | None
    csv_path: Path | None
    create_new: bool


def parse_args(argv: list[str]) -> AppConfig:
    parser = argparse.ArgumentParser(
        description="WWM Guild Manager (bootstrap)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a settings file (json/toml).",
    )
    parser.add_argument(
        "--open-csv",
        type=Path,
        help="Open an existing CSV file at startup.",
    )
    parser.add_argument(
        "--new",
        action="store_true",
        help="Start with a new CSV project.",
    )

    args = parser.parse_args(argv)

    if args.open_csv and args.new:
        parser.error("--open-csv and --new cannot be used together.")

    return AppConfig(
        config_path=args.config,
        csv_path=args.open_csv,
        create_new=args.new,
    )


def validate_paths(config: AppConfig) -> None:
    if config.config_path and not config.config_path.exists():
        raise FileNotFoundError(f"Config not found: {config.config_path}")
    if config.csv_path and not config.csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {config.csv_path}")


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    config = parse_args(argv)

    try:
        validate_paths(config)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2

    if config.create_new:
        mode = "new"
    elif config.csv_path:
        mode = "open"
    else:
        mode = "default"

    print("WWM Guild Manager bootstrap")
    print(f"Startup mode: {mode}")
    if config.config_path:
        print(f"Config: {config.config_path}")
    if config.csv_path:
        print(f"CSV: {config.csv_path}")
    print("GUI implementation will be added once the folder structure exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
