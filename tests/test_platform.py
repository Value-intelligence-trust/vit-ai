import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
headers = {"X-API-KEY": "vit-internal-key"}

def test_full_inference_lifecycle():
    # 1. Register a model with storage_id
    model_data = {
        "id": "production-lstm",
        "name": "Production LSTM",
        "description": "Production model",
        "capabilities": ["prediction"],
        "provider": "internal",
        "input_schema": {},
        "output_schema": {},
        "initial_version": "2.0.0",
        "storage_id": "s3://vit-models/lstm-v2.pkl"
    }
    client.post("/api/v1/models", json=model_data, headers=headers)

    # 2. Run inference on the model
    infer_data = {
        "model_id": "production-lstm",
        "payload": {"data": [1, 2, 3]}
    }
    response = client.post("/api/v1/infer", json=infer_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["metadata"]["provider"] == "internal"
    assert "production" in response.json()["result"]["provider"]

def test_ensemble_with_registered_models():
    # Register another model to be part of ensemble
    model_data = {
        "id": "production-xgb",
        "name": "Production XGB",
        "description": "desc",
        "capabilities": ["prediction"],
        "provider": "internal",
        "input_schema": {},
        "output_schema": {},
        "initial_version": "1.0.0"
    }
    client.post("/api/v1/models", json=model_data, headers=headers)

    # Run ensemble
    ensemble_data = {"market_odds": {"home": 2.0, "draw": 3.0, "away": 3.5}}
    response = client.post("/api/v1/ensemble", json=ensemble_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["prediction"]["home_prob"] > 0
    # Check if attribution includes our registered model
    assert any(a["model_key"] == "production-xgb" for a in response.json()["prediction"]["attribution"])

def test_training_jobs():
    job_data = {
        "model_id": "production-lstm",
        "dataset_id": "ds-1",
        "params": {"epochs": 10}
    }
    response = client.post("/api/v1/training/jobs", json=job_data, headers=headers)
    assert response.status_code == 200
    job_id = response.json()["id"]

    response = client.get(f"/api/v1/training/jobs/{job_id}")
    assert response.json()["status"] == "queued"
