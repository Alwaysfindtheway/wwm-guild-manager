"""OCR engine wrappers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from PIL import Image


class OCREngine(Protocol):
    """Protocol for OCR engines used in the pipeline."""

    name: str

    def read_text(self, image: Image.Image) -> str:
        """Return OCR text for the given image."""


@dataclass
class TesseractEngine:
    """Wrapper for pytesseract-based OCR."""

    language: str = "kor+eng"
    name: str = "tesseract"

    def read_text(self, image: Image.Image) -> str:
        import pytesseract

        return pytesseract.image_to_string(image, lang=self.language)


@dataclass
class EasyOCREngine:
    """Wrapper for EasyOCR."""

    language: tuple[str, ...] = ("ko", "en")
    name: str = "easyocr"

    def __post_init__(self) -> None:
        import easyocr

        self._reader = easyocr.Reader(list(self.language))

    def read_text(self, image: Image.Image) -> str:
        import numpy as np

        results = self._reader.readtext(np.array(image))
        return "\n".join(text for _, text, _ in results)
