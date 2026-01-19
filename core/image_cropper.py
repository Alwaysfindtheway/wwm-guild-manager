"""Image cropping utilities for OCR preparation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


@dataclass(frozen=True)
class CropPreset:
    """Defines a normalized crop region for a specific resolution."""

    name: str
    x: float
    y: float
    width: float
    height: float


def crop_image(image_path: Path, preset: CropPreset) -> Image.Image:
    """Crop an image using a normalized preset (0-1 coordinates)."""

    image = Image.open(image_path)
    width, height = image.size
    left = int(width * preset.x)
    upper = int(height * preset.y)
    right = int(width * (preset.x + preset.width))
    lower = int(height * (preset.y + preset.height))
    return image.crop((left, upper, right, lower))


def batch_crop(images: Iterable[Path], preset: CropPreset, output_dir: Path) -> list[Path]:
    """Crop multiple images and save them to the output directory."""

    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    for index, image_path in enumerate(images, start=1):
        cropped = crop_image(image_path, preset)
        output_path = output_dir / f"cropped_{index:03d}.png"
        cropped.save(output_path)
        output_paths.append(output_path)
    return output_paths
