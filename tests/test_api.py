import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_ai_status():
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200
    assert "status" in response.json()

def test_ensemble():
    # Test with new schema alignment
    response = client.post("/api/v1/ensemble", json={"home_team": "Team A", "away_team": "Team B"})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "match_quality_rating" in data["prediction"]
    assert "attribution" in data["prediction"]
    assert data["prediction"]["home_prob"] > 0
