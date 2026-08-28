"""
Central place for all configuration. Loads from .env via pydantic-settings.
Import `settings` anywhere you need a config value - never read os.environ directly
elsewhere, so we have one source of truth.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-3-5-haiku-20241022"

    JWT_SECRET: str = "dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440

    DATABASE_URL: str = "sqlite:///./jobhunt.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
