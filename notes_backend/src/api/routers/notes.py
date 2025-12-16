from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..models import Note

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=schemas.NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new note with a title and content.",
    responses={
        201: {"description": "Note created successfully"},
        422: {"description": "Validation error"},
    },
)
def create_note(payload: schemas.NoteCreate, db: Session = Depends(get_db)) -> schemas.NoteOut:
    """Create a new note."""
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[schemas.NoteOut],
    summary="List notes",
    description="Retrieve all notes.",
)
def list_notes(db: Session = Depends(get_db)) -> list[schemas.NoteOut]:
    """Return all notes."""
    return db.query(Note).order_by(Note.created_at.desc()).all()


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=schemas.NoteOut,
    summary="Get a note",
    description="Retrieve a single note by ID.",
    responses={404: {"description": "Note not found"}},
)
def get_note(note_id: int, db: Session = Depends(get_db)) -> schemas.NoteOut:
    """Return a note by its ID or 404 if not found."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=schemas.NoteOut,
    summary="Update a note",
    description="Replace title and/or content of the note.",
    responses={404: {"description": "Note not found"}, 422: {"description": "Validation error"}},
)
def update_note(note_id: int, payload: schemas.NoteUpdate, db: Session = Depends(get_db)) -> schemas.NoteOut:
    """Update an existing note by ID. Fields not provided are left unchanged."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    updated = False
    if payload.title is not None:
        note.title = payload.title
        updated = True
    if payload.content is not None:
        note.content = payload.content
        updated = True

    if updated:
        db.add(note)
        db.commit()
        db.refresh(note)
    return note


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its ID.",
    responses={404: {"description": "Note not found"}},
)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a note by ID or 404 if not found."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    db.delete(note)
    db.commit()
    return None
