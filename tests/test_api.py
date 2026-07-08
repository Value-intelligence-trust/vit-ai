import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_ai_status():
    response = client.get("/api/v1/ai/status")
    assert response.status_code == 200

def test_protected_endpoint_no_auth():
    response = client.post("/api/v1/models", json={})
    assert response.status_code == 401

def test_protected_endpoint_with_api_key():
    headers = {"X-API-KEY": "vit-internal-key"}
    model_data = {
        "id": "test-model-auth",
        "name": "Auth Model",
        "version": "1.0.0",
        "description": "desc",
        "capabilities": [],
        "provider": "internal",
        "input_schema": {},
        "output_schema": {}
    }
    response = client.post("/api/v1/models", json=model_data, headers=headers)
    assert response.status_code == 200
