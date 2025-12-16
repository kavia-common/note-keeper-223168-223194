from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Shared fields for notes."""

    title: str = Field(..., description="Title of the note", min_length=1, max_length=255)
    content: str = Field(..., description="Content of the note", min_length=1)


class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating an existing note."""
    title: Optional[str] = Field(None, description="Updated title of the note", min_length=1, max_length=255)
    content: Optional[str] = Field(None, description="Updated content of the note", min_length=1)


class NoteOut(NoteBase):
    """Response schema for returning a note."""

    id: int = Field(..., description="Unique identifier of the note")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")

    class Config:
        from_attributes = True
