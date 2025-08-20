"""Main entry point for the API.

This module initializes the FastAPI application and includes API routers.
"""

from fastapi import FastAPI

from sandra_benes.api_routers import v1

API = FastAPI(title="Sandra Benes API")
API.include_router(v1.ROUTER, prefix="/api/v1")
