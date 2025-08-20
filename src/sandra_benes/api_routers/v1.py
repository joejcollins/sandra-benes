"""API v1 endpoints for the Sandra Benes project."""

from fastapi import APIRouter

ROUTER = APIRouter()


@ROUTER.get("/ping")
async def ping() -> dict:
    """Health check endpoint."""
    return {"message": "pong"}
