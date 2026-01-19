"""Project folder management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Project folder layout for storing OCR artifacts."""

    root: Path

    @property
    def input_dir(self) -> Path:
        return self.root / "input"

    @property
    def cropped_dir(self) -> Path:
        return self.root / "cropped"

    @property
    def ocr_raw_dir(self) -> Path:
        return self.root / "ocr_raw"

    @property
    def output_csv(self) -> Path:
        return self.root / "output.csv"

    @property
    def log_file(self) -> Path:
        return self.root / "log.txt"


def ensure_project_structure(root: Path) -> ProjectPaths:
    """Create project folders if they do not exist."""

    paths = ProjectPaths(root)
    paths.input_dir.mkdir(parents=True, exist_ok=True)
    paths.cropped_dir.mkdir(parents=True, exist_ok=True)
    paths.ocr_raw_dir.mkdir(parents=True, exist_ok=True)
    return paths
