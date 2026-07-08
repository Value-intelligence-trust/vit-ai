import time
import uuid
import random
from typing import List, Dict, Any

class EmbeddingService:
    async def generate(self, text: str, model_id: str = "text-embedding-3-small") -> Dict[str, Any]:
        start_time = time.time()
        # Mock embedding: 128-dimensional vector
        embedding = [random.uniform(-1, 1) for _ in range(128)]
        latency = time.time() - start_time

        return {
            "embedding": embedding,
            "model": model_id,
            "dimensions": 128,
            "latency": latency,
            "request_id": str(uuid.uuid4())
        }

embedding_service = EmbeddingService()
