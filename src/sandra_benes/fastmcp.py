"""MCP Server."""

from typing import Any

from mcp.server.fastmcp import FastMCP

MCP = FastMCP("my-service")


@MCP.tool("health")
def health_check() -> dict[str, Any]:
    """Do the health check."""
    return {"status": "healthy"}
