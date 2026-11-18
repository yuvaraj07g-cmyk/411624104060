"""Transform and load JSON records into PostgreSQL documents."""

import hashlib
import json
from collections.abc import Sequence
from datetime import date
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from rti_mate.db.models import Document

TITLE_FIELD = "decision_no"
KNOWN = {"id", "title", "source_url", "licence", "doc_type", "published_on"}


def fingerprint(record: dict[str, Any]) -> str:
    canonical = json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def to_row(record: dict[str, Any]) -> dict[str, Any]:
    published = record.get("published_on")
    return {
        "external_id": str(record["id"]),
        "title": str(record.get("title") or record.get(TITLE_FIELD) or record["id"]),
        "source_url": record.get("source_url"),
        "licence": record.get("licence"),
        "doc_type": record.get("doc_type") or "record",
        "published_on": date.fromisoformat(published) if published else None,
        "sha256": fingerprint(record),
        "metadata_": {key: value for key, value in record.items() if key not in KNOWN},
    }


async def load_records(
    session: AsyncSession, records: Sequence[dict[str, Any]]
) -> tuple[int, int, int]:
    rows = await session.execute(select(Document.external_id, Document.sha256))
    existing = dict(rows.all())
    inserted = updated = unchanged = 0
    for record in records:
        row = to_row(record)
        old = existing.get(row["external_id"])
        if old is None:
            session.add(Document(**row))
            inserted += 1
        elif old != row["sha256"]:
            await session.execute(
                update(Document).where(Document.external_id == row["external_id"]).values(**row)
            )
            updated += 1
        else:
            unchanged += 1
    return inserted, updated, unchanged
