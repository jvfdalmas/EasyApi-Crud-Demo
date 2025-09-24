from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    app_env: str = "dev"
    database_url: str = "sqlite+aiosqlite:///./app.db"
    allowed_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_prefix = ""
        case_sensitive = False


settings = Settings()
"""Singleton settings instance used across the application."""


