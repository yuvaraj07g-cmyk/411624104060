import asyncio
import os
from collections.abc import Awaitable, Callable
from uuid import uuid4

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from rti_mate.db.loader import load_records
from rti_mate.db.models import Base, Document, Page
from rti_mate.db.repository import DocumentRepository
from rti_mate.db.url import to_asyncpg_url

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="set TEST_DATABASE_URL to run PostgreSQL integration tests",
)


def run_in_isolated_schema(
    test: Callable[[AsyncSession], Awaitable[None]],
) -> None:
    async def run() -> None:
        if TEST_DATABASE_URL is None:
            pytest.skip("set TEST_DATABASE_URL to run PostgreSQL integration tests")
        url = to_asyncpg_url(TEST_DATABASE_URL)
        admin_engine = create_async_engine(url)
        schema = f"rti_test_{uuid4().hex}"
        schema_created = False
        test_engine = None
        try:
            async with admin_engine.begin() as connection:
                await connection.execute(text(f'CREATE SCHEMA "{schema}"'))
            schema_created = True
            test_engine = create_async_engine(
                url,
                connect_args={"server_settings": {"search_path": schema}},
            )
            async with test_engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            async with AsyncSession(test_engine) as session:
                await test(session)
        finally:
            if test_engine is not None:
                await test_engine.dispose()
            if schema_created:
                async with admin_engine.begin() as connection:
                    await connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
            await admin_engine.dispose()

    asyncio.run(run())


def test_loader_is_idempotent_against_postgres():
    async def verify(session: AsyncSession) -> None:
        record = {"id": "test-1", "topic": "roads"}
        async with session.begin():
            assert await load_records(session, [record]) == (1, 0, 0)
        async with session.begin():
            assert await load_records(session, [record]) == (0, 0, 1)

    run_in_isolated_schema(verify)


def test_repository_filters_and_paginates_postgres_rows():
    async def verify(session: AsyncSession) -> None:
        async with session.begin():
            await load_records(
                session,
                [
                    {"id": "test-1", "topic": "roads"},
                    {"id": "test-2", "topic": "roads"},
                    {"id": "test-3", "topic": "water"},
                ],
            )
        repository = DocumentRepository(session)
        total, items = await repository.list(
            q=None, filters={"topic": "roads"}, limit=1, offset=1
        )
        assert total == 2
        assert [item["id"] for item in items] == ["test-2"]

    run_in_isolated_schema(verify)


def test_page_constraints_and_cascade_in_postgres():
    async def verify(session: AsyncSession) -> None:
        async with session.begin():
            document = Document(external_id="test-1", title="Test", sha256="a" * 64)
            document.pages.append(Page(page_no=1, text="first page"))
            session.add(document)
        async with session.begin():
            document = await session.scalar(
                select(Document).where(Document.external_id == "test-1")
            )
            await session.delete(document)
        async with session.begin():
            page_count = await session.scalar(select(func.count()).select_from(Page))
            assert page_count == 0
        try:
            async with session.begin():
                session.add(Page(document_id=999, page_no=0, text="invalid page"))
                await session.flush()
        except IntegrityError:
            return
        raise AssertionError("invalid page unexpectedly satisfied the foreign-key and check constraints")

    run_in_isolated_schema(verify)
