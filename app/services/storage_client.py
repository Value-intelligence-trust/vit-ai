import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageClient:
    def __init__(self):
        self.base_url = settings.VIT_STORAGE_URL

    async def upload_dataset(self, dataset_id: str, data: bytes):
        # Integration with vit-storage
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.base_url}/upload", files={"file": data})
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to upload to vit-storage: {e}")
            return False

storage_client = StorageClient()
