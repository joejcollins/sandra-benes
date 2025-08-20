"""API v1 endpoints for the Sandra Benes project."""

from fastapi import APIRouter

from sandra_benes.handlers import pong

ROUTER = APIRouter()


@ROUTER.get("/ping")
async def ping() -> dict:
    """Health check endpoint."""
    return pong.get_pong()
