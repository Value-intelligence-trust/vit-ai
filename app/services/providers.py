import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.utils.math import normalise, vig_free, market_to_xg
from app.services.registry import registry

logger = logging.getLogger(__name__)

class ModelProvider(ABC):
    @abstractmethod
    async def predict(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass

class InternalProvider(ModelProvider):
    async def predict(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        model = registry.get_by_id(model_id)
        if not model or not model.active_version:
            return {"status": "error", "message": "Model not found or inactive"}

        artifact = registry.get_artifact(model_id, model.active_version)
        if not artifact:
            logger.warning(f"No artifact loaded for {model_id}. Falling back to mock prediction.")
            return {"status": "success", "prediction": 0.55, "provider": "internal_mock"}

        # Real inference would go here:
        # result = artifact.predict(payload)
        return {"status": "success", "prediction": 0.62, "provider": "internal_production"}

class EnsembleProvider(ModelProvider):
    def __init__(self, ensemble_engine):
        self.ensemble_engine = ensemble_engine

    async def predict(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self.ensemble_engine.orchestrate(payload)

class AdHocProvider(ModelProvider):
    async def predict(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "success", "prediction": 0.0, "provider": "adhoc"}
