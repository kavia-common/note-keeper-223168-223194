from __future__ import annotations

import os
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers.notes import router as notes_router

# Initialize FastAPI app with OpenAPI metadata and tags
app = FastAPI(
    title="Notes API",
    description="A simple FastAPI backend for managing notes with CRUD operations.",
    version=os.getenv("APP_VERSION", "1.0.0"),
    openapi_tags=[
        {"name": "Health", "description": "Service health and diagnostics"},
        {"name": "Notes", "description": "Operations for creating, reading, updating, and deleting notes"},
    ],
)

# Enable permissive CORS for local development and preview usage
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)


# PUBLIC_INTERFACE
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Returns a simple health status for the service.",
)
def health_check() -> Dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


# Back-compat for existing root health route used by the initial skeleton
# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health check (root)",
    description="Root route for simple health status.",
)
def root_health() -> Dict[str, str]:
    """Return service health status at root path."""
    return {"message": "Healthy", "status": "ok"}


# Register routers
app.include_router(notes_router)
