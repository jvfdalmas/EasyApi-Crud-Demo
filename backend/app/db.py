"""Database setup and session management using SQLAlchemy (async).

Description: Configures the async engine, declarative base, and session dependency.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy ORM models."""
    pass


# Create the async SQLAlchemy engine. `echo=False` silences SQL logs; `future=True`
# opts in to SQLAlchemy 2.0 style behavior for consistency.
engine = create_async_engine(settings.database_url, echo=False, future=True)
"""Async SQLAlchemy engine bound to the configured database URL."""

# Build a session factory that produces `AsyncSession` objects. `expire_on_commit=False`
# keeps ORM instances usable after commit without automatic expiration.
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
"""Async session factory producing `AsyncSession` instances."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a request-scoped `AsyncSession` for dependency injection.

    Usage in FastAPI endpoints:

        async def endpoint(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with SessionLocal() as session:
        yield session


