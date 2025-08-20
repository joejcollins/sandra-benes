"""Test the FastAPI endpoints."""

from http import HTTPStatus

from fastapi import testclient

from sandra_benes.fastapi import API

CLIENT = testclient.TestClient(API)


def test_ping():
    """Confirm that the ping works."""
    # ACT
    response = CLIENT.get("/api/v1/ping")
    # ASSERT
    assert response.status_code == HTTPStatus.OK
    content = response.json()
    assert content["message"] == "pong"
