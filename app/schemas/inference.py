from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional, List

class ConfidenceIntervals(BaseModel):
    low: float
    mid: float
    high: float

class MatchQuality(BaseModel):
    score: float
    grade: str
    label: str
    home_advantage_bias: float
    components: Dict[str, float]

class Attribution(BaseModel):
    model_key: str
    model_name: str
    weight_frac: float
    delta_home: float
    delta_draw: float
    delta_away: float
    home_prob: float
    draw_prob: float
    away_prob: float

    model_config = ConfigDict(protected_namespaces=())

class InferenceRequest(BaseModel):
    model_id: str
    payload: Dict[str, Any]
    async_mode: bool = False
    timeout: Optional[int] = 30

    model_config = ConfigDict(protected_namespaces=())

class EnsemblePrediction(BaseModel):
    home_prob: float
    draw_prob: float
    away_prob: float
    over_25_prob: float
    btts_prob: float
    home_xg: float
    away_xg: float
    confidence: Dict[str, float]
    match_quality_rating: MatchQuality
    attribution: Optional[List[Attribution]] = None

class InferenceResponse(BaseModel):
    request_id: str
    model_id: str
    result: Any
    latency: float
    metadata: Optional[Dict[str, Any]] = None
    prediction_details: Optional[EnsemblePrediction] = None

    model_config = ConfigDict(protected_namespaces=())

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
