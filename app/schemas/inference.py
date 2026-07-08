from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class InferenceRequest(BaseModel):
    model_id: str
    payload: Dict[str, Any]
    async_mode: bool = False
    timeout: Optional[int] = 30

class InferenceResponse(BaseModel):
    request_id: str
    model_id: str
    result: Any
    latency: float
    metadata: Optional[Dict[str, Any]] = None

class PredictionResponse(InferenceResponse):
    prediction: float
    confidence: float

class ChatResponse(InferenceResponse):
    response: str

class ClassificationResponse(InferenceResponse):
    label: str
    score: float

class SummaryResponse(InferenceResponse):
    summary: str

class EmbeddingResponse(InferenceResponse):
    embedding: List[float]
