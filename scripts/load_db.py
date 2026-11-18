"""Load data/sample_records.json into Postgres.

Safe to run again and again: new records are inserted, changed ones updated,
unchanged ones skipped (we compare a sha256 fingerprint of each record).
Run:  uv run python scripts/load_db.py
"""

import asyncio
import json

from rti_mate.core.config import get_settings
from rti_mate.db.loader import load_records
from rti_mate.db.session import make_engine, make_sessionmaker


async def main() -> None:
    settings = get_settings()
    records = json.loads(settings.data_file.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise TypeError(f"{settings.data_file} must contain a JSON array of records")
    engine = make_engine(settings)
    try:
        session_factory = make_sessionmaker(engine)
        async with session_factory() as session, session.begin():
            inserted, updated, unchanged = await load_records(session, records)
    finally:
        await engine.dispose()
    print(f"records={len(records)} inserted={inserted} updated={updated} unchanged={unchanged}")


if __name__ == "__main__":
    asyncio.run(main())
