"""Validation helpers for OCR results."""

from __future__ import annotations

from dataclasses import dataclass

from rapidfuzz import fuzz

from models import OCRComparisonResult


@dataclass(frozen=True)
class ValidationThresholds:
    """Similarity thresholds for OCR comparison."""

    text_similarity: float = 85.0


def compare_texts(primary: str, secondary: str, thresholds: ValidationThresholds) -> OCRComparisonResult:
    """Compare OCR texts and return a comparison result."""

    score = fuzz.ratio(primary, secondary)
    is_match = score >= thresholds.text_similarity
    chosen = primary if is_match else None
    return OCRComparisonResult(
        primary_text=primary,
        secondary_text=secondary,
        is_match=is_match,
        similarity_score=score,
        chosen_text=chosen,
    )
