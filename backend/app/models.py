"""SQLAlchemy ORM models for the application.

Description: Defines database entities persisted in the application database.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Item(Base):
    """Simple item entity with an integer primary key and name field."""
    __tablename__ = "items"

    # Surrogate primary key. The `index=True` speeds up lookups by id.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Item human-friendly name with a maximum length constraint
    name: Mapped[str] = mapped_column(String(255), nullable=False)


