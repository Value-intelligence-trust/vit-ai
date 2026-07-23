import logging
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIKernel:
    def __init__(self):
        self.status = "operational"
        self.providers = settings.SUPPORTED_PROVIDERS

    def get_status(self) -> Dict[str, Any]:
        # Import here to avoid circular import; use the shared singleton registry
        from app.services.registry import registry
        loaded = registry.loaded_model_count()
        return {
            "status": self.status,
            "version": settings.VERSION,
            "loaded_models_count": loaded,
        }

    def get_providers(self) -> List[str]:
        return self.providers

kernel = AIKernel()
