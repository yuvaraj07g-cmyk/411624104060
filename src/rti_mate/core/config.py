"""All settings come from environment variables (or a local .env file)."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from rti_mate.db.url import to_asyncpg_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "rti_mate"
    # No defaults on purpose: if these are missing, the app refuses to start (fail fast).
    app_env: Literal["local", "ci", "production"]
    database_url: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    data_file: Path = Path("data/sample_records.json")
    db_pool_size: int = 5
    db_max_overflow: int = 5

    @field_validator("database_url")
    @classmethod
    def _asyncpg(cls, value: str) -> str:
        return to_asyncpg_url(value)


@lru_cache
def get_settings() -> Settings:
    """Build the settings once and reuse them."""
    return Settings()
