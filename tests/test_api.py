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

def test_model_registry():
    model_data = {
        "id": "model-1",
        "name": "Test Model",
        "version": "1.0.0",
        "description": "A test model",
        "capabilities": ["classification"],
        "provider": "internal",
        "input_schema": {},
        "output_schema": {}
    }
    response = client.post("/api/v1/models", json=model_data)
    assert response.status_code == 200
    assert response.json()["id"] == "model-1"

    response = client.get("/api/v1/models")
    assert len(response.json()) >= 1

def test_inference():
    payload = {
        "model_id": "model-1",
        "payload": {"text": "hello"}
    }
    response = client.post("/api/v1/infer", json=payload)
    assert response.status_code == 200
    assert "result" in response.json()

def test_ensemble():
    response = client.post("/api/v1/ensemble", json={"data": [1, 2, 3]})
    assert response.status_code == 200
    assert "confidence" in response.json()
