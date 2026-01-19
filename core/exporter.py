"""CSV import/export helpers."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from models import DEFAULT_FIELDS, GuildMemberRecord


def export_records(path: Path, records: Iterable[GuildMemberRecord]) -> None:
    """Write records to CSV."""

    rows = [record.to_csv_row(DEFAULT_FIELDS) for record in records]
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def import_records(path: Path) -> list[GuildMemberRecord]:
    """Load records from CSV into GuildMemberRecord entries."""

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        records: list[GuildMemberRecord] = []
        for row in reader:
            record = GuildMemberRecord(
                index=int(row.get("index", "0") or 0),
                nickname=row.get("nickname", ""),
                role=row.get("role", ""),
                faction=row.get("faction", ""),
                days_since_join=row.get("days_since_join", ""),
                weekly_activity=row.get("weekly_activity", ""),
                martial_realm=row.get("martial_realm", ""),
                exploration_skill=row.get("exploration_skill", ""),
                tech_mastery=row.get("tech_mastery", ""),
                extras={
                    key: value
                    for key, value in row.items()
                    if key not in DEFAULT_FIELDS
                },
            )
            records.append(record)
        return records
