import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
from app.utils.math import normalise, vig_free, market_to_xg
from app.services.registry import registry

logger = logging.getLogger(__name__)

class ModelProvider(ABC):
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the provider and its resources."""
        pass

    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with external APIs or local security keys."""
        pass

    @abstractmethod
    async def infer(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute inference on the specified model."""
        pass

    @abstractmethod
    async def embeddings(self, text: str, model_id: str) -> Dict[str, Any]:
        """Generate vector representations for the input text."""
        pass

    @abstractmethod
    async def stream(self, model_id: str, payload: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream inference chunks from the provider."""
        yield {}

    @abstractmethod
    async def shutdown(self) -> bool:
        """Gracefully shut down and release resources."""
        pass

    @abstractmethod
    async def metrics(self) -> Dict[str, Any]:
        """Retrieve performance and usage metrics."""
        pass

    # Backwards compatibility helper
    async def predict(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Backward compatibility mapping to standard infer function."""
        return await self.infer(model_id, payload)


class InternalProvider(ModelProvider):
    def __init__(self):
        self._is_initialized = False
        self._request_count = 0

    async def initialize(self) -> bool:
        self._is_initialized = True
        logger.info("InternalProvider initialized.")
        return True

    async def authenticate(self) -> bool:
        return True

    async def infer(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._request_count += 1
        model = registry.get_by_id(model_id)
        if not model or not model.active_version:
            return {"status": "error", "message": "Model not found or inactive"}

        artifact = registry.get_artifact(model_id, model.active_version)
        if not artifact:
            logger.warning(f"No artifact loaded for {model_id}. Falling back to mock prediction.")
            return {"status": "success", "prediction": 0.55, "provider": "internal_mock"}

        # Run inference using the standardized Model Interface (Phase 4 requirement)
        result = artifact.predict(payload)
        return result

    async def embeddings(self, text: str, model_id: str) -> Dict[str, Any]:
        # Return fallback embedding
        return {"embedding": [0.0] * 128, "model": model_id, "provider": "internal"}

    async def stream(self, model_id: str, payload: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        result = await self.infer(model_id, payload)
        yield result

    async def shutdown(self) -> bool:
        self._is_initialized = False
        logger.info("InternalProvider shut down.")
        return True

    async def metrics(self) -> Dict[str, Any]:
        return {
            "is_initialized": self._is_initialized,
            "requests_processed": self._request_count,
            "provider_type": "internal"
        }


class EnsembleProvider(ModelProvider):
    def __init__(self, ensemble_engine):
        self.ensemble_engine = ensemble_engine
        self._is_initialized = False
        self._request_count = 0

    async def initialize(self) -> bool:
        self._is_initialized = True
        logger.info("EnsembleProvider initialized.")
        return True

    async def authenticate(self) -> bool:
        return True

    async def infer(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._request_count += 1
        return await self.ensemble_engine.orchestrate(payload)

    async def embeddings(self, text: str, model_id: str) -> Dict[str, Any]:
        return {"status": "error", "message": "EnsembleProvider does not support embeddings"}

    async def stream(self, model_id: str, payload: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        result = await self.infer(model_id, payload)
        yield result

    async def shutdown(self) -> bool:
        self._is_initialized = False
        logger.info("EnsembleProvider shut down.")
        return True

    async def metrics(self) -> Dict[str, Any]:
        return {
            "is_initialized": self._is_initialized,
            "requests_processed": self._request_count,
            "provider_type": "ensemble"
        }


class AdHocProvider(ModelProvider):
    def __init__(self):
        self._is_initialized = False
        self._request_count = 0

    async def initialize(self) -> bool:
        self._is_initialized = True
        return True

    async def authenticate(self) -> bool:
        return True

    async def infer(self, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._request_count += 1
        return {"status": "success", "prediction": 0.0, "provider": "adhoc"}

    async def embeddings(self, text: str, model_id: str) -> Dict[str, Any]:
        return {"embedding": [0.0] * 128, "model": model_id, "provider": "adhoc"}

    async def stream(self, model_id: str, payload: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        result = await self.infer(model_id, payload)
        yield result

    async def shutdown(self) -> bool:
        self._is_initialized = False
        return True

    async def metrics(self) -> Dict[str, Any]:
        return {
            "is_initialized": self._is_initialized,
            "requests_processed": self._request_count,
            "provider_type": "adhoc"
        }
