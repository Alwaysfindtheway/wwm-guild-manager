"""Parse OCR text into structured guild member fields."""

from __future__ import annotations

import re

from models import GuildMemberRecord


_FIELD_PATTERN = re.compile(r"\s+")


def _normalize(text: str) -> str:
    return _FIELD_PATTERN.sub(" ", text).strip()


def parse_member_text(text: str, index: int) -> GuildMemberRecord:
    """Parse OCR text into a GuildMemberRecord.

    This uses heuristic regex extraction and should be refined with real samples.
    """

    normalized = _normalize(text)

    nickname = _extract(normalized, r"닉네임\s*([\w\W]+?)\s")
    role = _extract(normalized, r"직책\s*([\w\W]+?)\s")
    faction = _extract(normalized, r"문파\s*([\w\W]+?)\s")
    days_since_join = _extract(normalized, r"가입\s*일수\s*(\d+\s*일)")
    weekly_activity = _extract(normalized, r"이번\s*주\s*활약도\s*(\d+)")
    martial_realm = _extract(normalized, r"무공\s*경지\s*([\d\.]+\S*)")
    exploration_skill = _extract(normalized, r"탐색\s*숙련도\s*(\d+)")
    tech_mastery = _extract(normalized, r"기술\s*조예\s*(\d+)")

    return GuildMemberRecord(
        index=index,
        nickname=nickname,
        role=role,
        faction=faction,
        days_since_join=days_since_join,
        weekly_activity=weekly_activity,
        martial_realm=martial_realm,
        exploration_skill=exploration_skill,
        tech_mastery=tech_mastery,
    )


def _extract(text: str, pattern: str) -> str:
    match = re.search(pattern, text)
    if not match:
        return ""
    return match.group(1).strip()
