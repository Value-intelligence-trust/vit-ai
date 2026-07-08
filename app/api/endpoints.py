from fastapi import APIRouter, HTTPException, Depends, Body
from typing import List, Dict, Any
from app.schemas.model import Model, ModelCreate, ModelUpdate
from app.schemas.inference import InferenceRequest, InferenceResponse
from app.schemas.dataset import Dataset, DatasetCreate
from app.services.registry import registry
from app.core.kernel import kernel
from app.services.inference import inference_pipeline
from app.services.ensemble import ensemble_engine

router = APIRouter()

# Phase 2: AI Kernel
@router.get("/ai/status")
async def get_ai_status():
    return kernel.get_status()

@router.get("/ai/providers")
async def get_ai_providers():
    return kernel.get_providers()

# Phase 3: Model Registry
@router.get("/models", response_model=List[Model])
async def list_models():
    return registry.get_all()

@router.post("/models", response_model=Model)
async def create_model(model_in: ModelCreate):
    if registry.get_by_id(model_in.id):
        raise HTTPException(status_code=400, detail="Model already exists")
    return registry.register(model_in)

@router.get("/models/{model_id}", response_model=Model)
async def get_model(model_id: str):
    model = registry.get_by_id(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.patch("/models/{model_id}", response_model=Model)
async def update_model(model_id: str, model_in: ModelUpdate):
    model = registry.update(model_id, model_in)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return model

@router.delete("/models/{model_id}")
async def delete_model(model_id: str):
    if not registry.delete(model_id):
        raise HTTPException(status_code=404, detail="Model not found")
    return {"status": "deleted"}

# Phase 4: Inference Pipeline
@router.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    return await inference_pipeline.process(request)

@router.post("/predict")
async def predict(request: InferenceRequest):
    response = await inference_pipeline.process(request)
    return {**response.model_dump(), "prediction": 0.95, "confidence": 0.99}

@router.post("/chat")
async def chat(request: InferenceRequest):
    response = await inference_pipeline.process(request)
    return {**response.model_dump(), "response": "Hello from VIT-AI"}

@router.post("/classify")
async def classify(request: InferenceRequest):
    response = await inference_pipeline.process(request)
    return {**response.model_dump(), "label": "spam", "score": 0.88}

@router.post("/summarize")
async def summarize(request: InferenceRequest):
    response = await inference_pipeline.process(request)
    return {**response.model_dump(), "summary": "Short summary"}

@router.post("/embed")
async def embed(request: InferenceRequest):
    response = await inference_pipeline.process(request)
    return {**response.model_dump(), "embedding": [0.1, 0.2, 0.3]}

# Phase 5: Ensemble Engine
@router.post("/ensemble")
async def ensemble(payload: Dict[str, Any] = Body(...)):
    return await ensemble_engine.orchestrate(payload)

@router.get("/ensemble/status")
async def ensemble_status():
    return {"status": ensemble_engine.status}

# Phase 6: Dataset Management (Basic in-memory registry for now)
datasets: Dict[str, Dataset] = {}

@router.get("/datasets", response_model=List[Dataset])
async def list_datasets():
    return list(datasets.values())

@router.post("/datasets", response_model=Dataset)
async def create_dataset(dataset_in: DatasetCreate):
    dataset = Dataset(**dataset_in.model_dump())
    datasets[dataset.id] = dataset
    return dataset

@router.get("/datasets/{dataset_id}", response_model=Dataset)
async def get_dataset(dataset_id: str):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return datasets[dataset_id]

@router.delete("/datasets/{dataset_id}")
async def delete_dataset(dataset_id: str):
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    del datasets[dataset_id]
    return {"status": "deleted"}

# Phase 7: Feature Store
features: List[Dict[str, Any]] = []

@router.get("/features")
async def list_features():
    return features

@router.post("/features")
async def create_feature(feature: Dict[str, Any] = Body(...)):
    features.append(feature)
    return feature

# Phase 8: Explainability
@router.post("/explain")
async def explain(payload: Dict[str, Any] = Body(...)):
    return {
        "confidence": 0.95,
        "feature_importance": {"feature_1": 0.7, "feature_2": 0.3},
        "reasoning_summary": "High correlation with feature_1 observed.",
        "prediction_metadata": {"model_version": "0.1.0"}
    }
