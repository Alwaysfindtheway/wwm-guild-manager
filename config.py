"""Configuration helpers for the WWM guild manager."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path("settings.json")


@dataclass(frozen=True)
class AppSettings:
    """User-facing settings persisted to disk."""

    default_csv_path: Path | None = None
    last_opened_project: Path | None = None
    crop_preset: str | None = None
    ocr_language: str = "kor+eng"


def _coerce_path(value: Any) -> Path | None:
    if value in (None, ""):
        return None
    return Path(value)


def load_settings(path: Path = DEFAULT_CONFIG_PATH) -> AppSettings:
    """Load settings from JSON. Missing files yield defaults."""

    if not path.exists():
        return AppSettings()

    payload = json.loads(path.read_text(encoding="utf-8"))
    return AppSettings(
        default_csv_path=_coerce_path(payload.get("default_csv_path")),
        last_opened_project=_coerce_path(payload.get("last_opened_project")),
        crop_preset=payload.get("crop_preset"),
        ocr_language=payload.get("ocr_language", "kor+eng"),
    )


def save_settings(settings: AppSettings, path: Path = DEFAULT_CONFIG_PATH) -> None:
    """Persist settings to JSON."""

    data = {
        "default_csv_path": str(settings.default_csv_path)
        if settings.default_csv_path
        else None,
        "last_opened_project": str(settings.last_opened_project)
        if settings.last_opened_project
        else None,
        "crop_preset": settings.crop_preset,
        "ocr_language": settings.ocr_language,
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
