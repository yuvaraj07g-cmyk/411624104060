"""Show how Postgres runs a filtered query, with and without the GIN index.

Run:  uv run python scripts/explain.py <field> <value>
Copy the output into NOTES.md.
"""

import asyncio
import json
import sys

from sqlalchemy import text

from rti_mate.core.config import get_settings
from rti_mate.db.session import make_engine

SQL = "EXPLAIN ANALYZE SELECT id, title FROM documents WHERE metadata @> CAST(:f AS jsonb)"


async def main(field: str, value: str) -> None:
    engine = make_engine(get_settings())
    params = {"f": json.dumps({field: value})}
    try:
        async with engine.connect() as conn:
            print("-- 1) What the planner chooses on its own:")
            for line in (await conn.execute(text(SQL), params)).scalars():
                print(line)
            await conn.execute(text("SET enable_seqscan = off"))  # only for this demo
            print("\n-- 2) Seq scan switched off, to prove the index can be used:")
            for line in (await conn.execute(text(SQL), params)).scalars():
                print(line)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: uv run python scripts/explain.py <field> <value>")
    asyncio.run(main(sys.argv[1], sys.argv[2]))
