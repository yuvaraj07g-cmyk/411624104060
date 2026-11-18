"""All SQL for documents lives here. Endpoints never write SQL themselves."""

import re
from typing import Any

from sqlalchemy import Text, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from rti_mate.db.models import Document

FILTER_KEY = re.compile(r"^[a-z_][a-z0-9_]{0,40}$")


def to_dict(doc: Document) -> dict[str, Any]:
    """Same flat shape the API returned on Day 2, so clients don't break."""
    return {
        "id": doc.external_id,
        **doc.metadata_,
        "title": doc.title,
        "doc_type": doc.doc_type,
        "source_url": doc.source_url,
        "licence": doc.licence,
        "published_on": doc.published_on.isoformat() if doc.published_on else None,
    }


def _value_candidates(value: str) -> list[Any]:
    """'10' in a URL may mean the number 10, the text '10', or an item in a list."""
    out: list[Any] = [value, [value]]
    lowered = value.lower()
    if lowered in ("true", "false"):
        out.append(lowered == "true")
    elif re.fullmatch(r"-?\d+", value):
        out.append(int(value))
    elif re.fullmatch(r"-?\d+\.\d+", value):
        out.append(float(value))
    return out


class DocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(
        self, *, q: str | None, filters: dict[str, str], limit: int, offset: int
    ) -> tuple[int, list[dict[str, Any]]]:
        stmt = select(Document)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(
                or_(Document.title.ilike(like), cast(Document.metadata_, Text).ilike(like))
            )
        for key, value in filters.items():
            # metadata @> '{"key": value}' uses the GIN index
            stmt = stmt.where(
                or_(*(Document.metadata_.contains({key: v}) for v in _value_candidates(value)))
            )
        total = await self.session.scalar(select(func.count()).select_from(stmt.subquery()))
        rows = await self.session.scalars(
            stmt.order_by(Document.external_id).limit(limit).offset(offset)
        )
        return total or 0, [to_dict(d) for d in rows]

    async def get(self, external_id: str) -> dict[str, Any] | None:
        doc = await self.session.scalar(select(Document).where(Document.external_id == external_id))
        return to_dict(doc) if doc else None
