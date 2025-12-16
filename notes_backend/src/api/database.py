from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Determine DB path: default to a local SQLite file within the container
DEFAULT_DB_DIR = Path(os.getenv("NOTES_DB_DIR", "data"))
DEFAULT_DB_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE = os.getenv("NOTES_DB_FILE", "notes.db")
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DEFAULT_DB_DIR / DB_FILE}",
)

# Create SQLAlchemy engine
# For SQLite, check_same_thread=False is required for multithreading in FastAPI
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session for request-scoped DB access and ensure proper cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
