import logging
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from rti_mate.core.config import Settings
from rti_mate.db.repository import DocumentRepository
from rti_mate.db.session import get_db

logger = logging.getLogger(__name__)


def get_app_settings(request: Request) -> Settings:
    return request.app.state.settings


async def check_db(db: Annotated[AsyncSession, Depends(get_db)]) -> bool:
    try:
        return await db.scalar(text("SELECT 1")) == 1
    except SQLAlchemyError as exc:
        logger.warning(
            "database readiness check failed",
            extra={"error_type": type(exc).__name__},
        )
        return False


def get_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> DocumentRepository:
    return DocumentRepository(db)


SettingsDep = Annotated[Settings, Depends(get_app_settings)]
DbCheckDep = Annotated[bool, Depends(check_db)]