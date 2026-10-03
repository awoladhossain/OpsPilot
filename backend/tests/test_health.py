"""Tests for health check endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_live_endpoint() -> None:
    """Test the /health/live endpoint returns 200 OK and expected structure."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "opspilot-backend"
    assert data["version"] == "0.1.0"


def test_health_alias_endpoint() -> None:
    """Test that /health also aliases to the liveness probe."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
