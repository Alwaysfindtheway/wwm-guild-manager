"""Entry point for the WWM guild manager application."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

from PySide6 import QtWidgets

from config import AppSettings, DEFAULT_CONFIG_PATH, load_settings
from core.exporter import import_records
from ui.main_window import MainWindow


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for the app bootstrap."""

    config_path: Path | None
    csv_path: Path | None
    create_new: bool


def parse_args(argv: list[str]) -> AppConfig:
    parser = argparse.ArgumentParser(
        description="WWM Guild Manager",
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


def resolve_settings(config: AppConfig) -> tuple[AppSettings, Path]:
    config_path = config.config_path or DEFAULT_CONFIG_PATH
    return load_settings(config_path), config_path


def resolve_csv_path(config: AppConfig, settings: AppSettings) -> Path | None:
    if config.create_new:
        return None
    if config.csv_path:
        return config.csv_path
    if settings.default_csv_path and settings.default_csv_path.exists():
        return settings.default_csv_path
    return None


def run_gui(settings: AppSettings, settings_path: Path, csv_path: Path | None) -> int:
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(settings, settings_path)

    if csv_path:
        records = import_records(csv_path)
        window.load_records(records, csv_path)

    window.show()
    return app.exec()


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    config = parse_args(argv)

    try:
        validate_paths(config)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 2

    settings, settings_path = resolve_settings(config)
    csv_path = resolve_csv_path(config, settings)
    return run_gui(settings, settings_path, csv_path)


if __name__ == "__main__":
    raise SystemExit(main())
