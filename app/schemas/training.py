from pydantic import BaseModel, Field
from datetime import datetime, UTC
from typing import Optional, Dict, Any, List

class TrainingJobBase(BaseModel):
    model_id: str
    dataset_id: str
    params: Dict[str, Any] = {}

class TrainingJob(TrainingJobBase):
    id: str
    status: str = "queued"  # queued, running, completed, failed
    logs: List[str] = []
    result_metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class TrainingJobCreate(TrainingJobBase):
    pass
