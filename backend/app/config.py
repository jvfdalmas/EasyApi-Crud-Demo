"""Application configuration via Pydantic settings.

Description: Loads environment-driven settings and exposes a singleton instance.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    # Environment name used to tweak behavior across dev/stage/prod
    app_env: str = "dev"
    # SQLAlchemy async database URL (driver+db path). Defaults to local SQLite file.
    database_url: str = "sqlite+aiosqlite:///./app.db"
    # Comma-separated list of allowed origins for CORS (frontend URLs)
    allowed_origins: str = "http://localhost:5173"

    class Config:
        # Load variables from a local .env file if present
        env_file = ".env"
        # No prefix required on environment variables (e.g., DATABASE_URL directly)
        env_prefix = ""
        # Env var names are treated case-insensitively for convenience
        case_sensitive = False


# Create a singleton settings instance. Import this where configuration is needed
settings = Settings()
"""Singleton settings instance used across the application."""


