"""MCP Server."""

from typing import Any

from mcp.server.fastmcp import FastMCP

from sandra_benes.handlers import pong

MCP = FastMCP("Sandra Benes MCP Server")


@MCP.tool("ping")
def ping() -> dict[str, Any]:
    """Do a health check."""
    return pong.get_pong()
