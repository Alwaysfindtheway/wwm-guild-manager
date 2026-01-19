"""Image preprocessing helpers for OCR."""

from __future__ import annotations

from typing import Iterable

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def preprocess_image(
    image: Image.Image,
    *,
    sharpen: bool = True,
    contrast: float = 1.3,
    threshold: int | None = None,
) -> Image.Image:
    """Apply common preprocessing steps to improve OCR accuracy."""

    processed = image.convert("L")
    if contrast != 1.0:
        processed = ImageEnhance.Contrast(processed).enhance(contrast)
    if sharpen:
        processed = processed.filter(ImageFilter.SHARPEN)
    if threshold is not None:
        processed = processed.point(lambda x: 255 if x > threshold else 0)
    return processed


def preprocess_variants(image: Image.Image) -> Iterable[Image.Image]:
    """Yield multiple preprocessing variants for OCR cross-validation."""

    yield preprocess_image(image, sharpen=True, contrast=1.2)
    yield preprocess_image(image, sharpen=True, contrast=1.5, threshold=160)
    yield ImageOps.invert(preprocess_image(image, sharpen=False, contrast=1.1))
