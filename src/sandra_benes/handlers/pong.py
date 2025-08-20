"""Do the health check."""

from typing import Any


def get_pong() -> dict[str, Any]:
    """Give me a pong, Vasili, one pong only please."""
    return {"message": "pong"}
