"""Starting point for the application."""

import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from sandra_benes.fastapi import API
from sandra_benes.fastmcp import MCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER: FastAPI = API

SERVER.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],  # needed for streamable HTTP clients
)

# Mount MCP under /mcp (Streamable HTTP transport)
SERVER.mount("/mcp", MCP.streamable_http_app())


# Render deployment entrypoint
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(SERVER, host="0.0.0.0", port=8000)
