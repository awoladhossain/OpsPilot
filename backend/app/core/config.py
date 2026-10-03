"""Application settings, read from environment variables (and a .env file locally)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"

    # asyncpg wants a plain "postgresql://" URL, not a DSN with query params
    database_url: str = "postgresql://opspilot:opspilot@localhost:5432/opspilot"


@lru_cache
def get_settings() -> Settings:
    """Get application settings, cached for performance."""
    return Settings()
