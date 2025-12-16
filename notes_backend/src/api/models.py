from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, event
from .database import Base


class Note(Base):
    """SQLAlchemy model representing a Note entity stored in the database."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


# Automatically update updated_at on update operations
@event.listens_for(Note, "before_update", propagate=True)
def receive_before_update(mapper, connection, target: Note):  # noqa: D401
    """SQLAlchemy event listener: set updated_at to current UTC before updating a record."""
    target.updated_at = datetime.now(timezone.utc)
