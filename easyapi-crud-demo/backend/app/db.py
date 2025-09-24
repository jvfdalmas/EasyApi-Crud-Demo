from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy ORM models."""
    pass


engine = create_async_engine(settings.database_url, echo=False, future=True)
"""Async SQLAlchemy engine bound to the configured database URL."""

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
"""Async session factory producing `AsyncSession` instances."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a request-scoped `AsyncSession` for dependency injection."""
    async with SessionLocal() as session:
        yield session


