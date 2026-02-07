from fastapi import APIRouter

# Import all endpoint modules
from app.api.endpoints import (
    retrieval,
    agentic_async,
    literature,
)

# Main API router (this name MUST match main.py import)
api_router = APIRouter()

# -----------------------------
# Retrieval endpoints
# -----------------------------
api_router.include_router(
    retrieval.router,
    prefix="/api",
    tags=["retrieval"],
)

# -----------------------------
# Agentic workflow endpoints
# -----------------------------
api_router.include_router(
    agentic_async.router,
    prefix="/api",
    tags=["agentic"],
)

# -----------------------------
# Literature metadata endpoints
# -----------------------------
api_router.include_router(
    literature.router,
    prefix="/api",
    tags=["literature"],
)