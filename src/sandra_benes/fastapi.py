"""Main entry point for the API.

This module initializes the FastAPI application and includes API routers.
"""

from fastapi import FastAPI

from sandra_benes.api_routers import (
    health,
    v1,
)

API = FastAPI(title="Sandra Benes API Server")

API.include_router(health.ROUTER)
API.include_router(v1.ROUTER, prefix="/api/v1")
