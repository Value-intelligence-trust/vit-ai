from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class DatasetBase(BaseModel):
    id: str
    name: str
    version: str
    description: str
    checksum: str
    metadata: Optional[Dict[str, Any]] = None

class DatasetCreate(DatasetBase):
    pass

class Dataset(DatasetBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
