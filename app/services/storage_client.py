import httpx
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageClient:
    def __init__(self):
        self.base_url = settings.VIT_STORAGE_URL

    async def upload(self, blob_name: str, data: bytes) -> bool:
        """Upload a blob to vit-storage."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/upload",
                    files={"file": (blob_name, data)}
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Failed to upload to vit-storage: {e}")
            return False

    async def download(self, storage_id: str) -> Optional[bytes]:
        """Download a blob from vit-storage."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/download/{storage_id}")
                if response.status_code == 200:
                    return response.content
                return None
        except Exception as e:
            logger.error(f"Failed to download from vit-storage: {e}")
            return None

storage_client = StorageClient()
