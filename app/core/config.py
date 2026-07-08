import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "VIT-AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Service Discovery
    VIT_STORAGE_URL: str = os.getenv("VIT_STORAGE_URL", "http://vit-storage-svc:8000")
    VIT_NETWORK_URL: str = os.getenv("VIT_NETWORK_URL", "http://vit-network-rpc:8000")

    # AI Config
    DEFAULT_PROVIDER: str = "internal"
    SUPPORTED_PROVIDERS: List[str] = ["internal", "ensemble"]

    class Config:
        case_sensitive = True

settings = Settings()
