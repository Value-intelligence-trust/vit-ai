import logging
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIKernel:
    def __init__(self):
        self.status = "operational"
        self.providers = settings.SUPPORTED_PROVIDERS
        self.loaded_models = []

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "version": settings.VERSION,
            "loaded_models_count": len(self.loaded_models)
        }

    def get_providers(self) -> List[str]:
        return self.providers

kernel = AIKernel()
