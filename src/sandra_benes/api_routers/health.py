"""API v1 endpoints for the Sandra Benes project."""

from fastapi import APIRouter

ROUTER = APIRouter()


@ROUTER.get("/healthz")
def healthz() -> dict[str, bool]:
    """Demo endpoint for health check."""
    return {"ok": True}
