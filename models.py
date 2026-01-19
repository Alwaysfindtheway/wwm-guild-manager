"""Data models for the WWM guild manager."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DEFAULT_FIELDS: tuple[str, ...] = (
    "index",
    "nickname",
    "role",
    "faction",
    "days_since_join",
    "weekly_activity",
    "martial_realm",
    "exploration_skill",
    "tech_mastery",
)


@dataclass
class GuildMemberRecord:
    """Represents a single guild member entry parsed from OCR."""

    index: int
    nickname: str
    role: str
    faction: str
    days_since_join: str
    weekly_activity: str
    martial_realm: str
    exploration_skill: str
    tech_mastery: str
    extras: dict[str, Any] = field(default_factory=dict)

    def to_csv_row(self, field_order: tuple[str, ...] = DEFAULT_FIELDS) -> dict[str, Any]:
        """Return a CSV row dict that respects the configured field order."""

        row = {
            "index": self.index,
            "nickname": self.nickname,
            "role": self.role,
            "faction": self.faction,
            "days_since_join": self.days_since_join,
            "weekly_activity": self.weekly_activity,
            "martial_realm": self.martial_realm,
            "exploration_skill": self.exploration_skill,
            "tech_mastery": self.tech_mastery,
        }
        for key, value in self.extras.items():
            if key not in row:
                row[key] = value

        ordered = {key: row.get(key, "") for key in field_order}
        extras = {key: value for key, value in row.items() if key not in ordered}
        ordered.update(extras)
        return ordered


@dataclass
class OCRComparisonResult:
    """Stores OCR results from two engines and validation outcome."""

    primary_text: str
    secondary_text: str
    is_match: bool
    similarity_score: float
    chosen_text: str | None = None
