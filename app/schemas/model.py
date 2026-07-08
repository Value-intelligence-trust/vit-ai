from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List

class ModelBase(BaseModel):
    id: str
    name: str
    version: str
    description: str
    capabilities: List[str]
    provider: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    status: str = "active"

class ModelCreate(ModelBase):
    pass

class ModelUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    provider: Optional[str] = None
    status: Optional[str] = None

class Model(ModelBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
