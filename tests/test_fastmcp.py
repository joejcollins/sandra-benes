"""Unit tests for the FastMCP server."""

import ast

import pytest
from fastmcp import Client
from mcp.types import TextContent  # For type checking results

from src.sandra_benes.fastmcp import MCP


@pytest.mark.asyncio
async def test_ping():
    """Test the ping endpoint."""
    # ARRANGE
    async with Client(MCP) as client:
        # ACT
        result = await client.call_tool("ping")
        # ASSERT
        assert isinstance(result.content[0], TextContent)
        content_text = result.content[0].text
        content = ast.literal_eval(content_text)
        assert content["message"] == "pong"
