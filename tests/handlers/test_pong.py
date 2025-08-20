"""Test the pong handler."""

from sandra_benes.handlers import pong


def test_get_pong():
    """Test the get_pong function."""
    # ACT
    result = pong.get_pong()
    # ASSERT
    assert result["message"] == "pong"
