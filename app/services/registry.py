from typing import List, Dict, Optional
from app.schemas.model import Model, ModelCreate, ModelUpdate
from datetime import datetime

class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, Model] = {}

    def register(self, model_in: ModelCreate) -> Model:
        model = Model(**model_in.model_dump())
        self.models[model.id] = model
        return model

    def get_all(self) -> List[Model]:
        return list(self.models.values())

    def get_by_id(self, model_id: str) -> Optional[Model]:
        return self.models.get(model_id)

    def update(self, model_id: str, model_in: ModelUpdate) -> Optional[Model]:
        if model_id not in self.models:
            return None
        model = self.models[model_id]
        update_data = model_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        model.updated_at = datetime.utcnow()
        return model

    def delete(self, model_id: str) -> bool:
        if model_id in self.models:
            del self.models[model_id]
            return True
        return False

registry = ModelRegistry()
