"""Main entry point for the MyApp API.

This module initializes the FastAPI application and includes API routers.
"""

from fastapi import FastAPI

from sandra_benes.api import v1

app = FastAPI(title="MyApp API")
app.include_router(v1.router, prefix="/api/v1")
