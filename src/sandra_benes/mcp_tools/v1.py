"""MCP (Model-Driven Configuration Protocol) API endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

ROUTER = APIRouter()


# MCP discovery endpoint
@ROUTER.get("/.well-known/mcp", include_in_schema=False)
async def mcp_discovery() -> JSONResponse:
    """MCP discovery endpoint describing available APIs."""
    return JSONResponse(
        content={
            "name": "Sandra Benes API",
            "description": "API for health checks and more, discoverable via MCP.",
            "endpoints": [
                {
                    "name": "Health Check",
                    "description": "Check if the service is alive.",
                    "method": "GET",
                    "path": "/api/v1/ping",
                    "response": {"message": "pong"},
                }
            ],
        }
    )
