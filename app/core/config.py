import os
from pydantic_settings import BaseSettings
from typing import List, Dict, Any

class Settings(BaseSettings):
    PROJECT_NAME: str = "VIT-AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    INTERNAL_API_KEY: str = os.getenv("INTERNAL_API_KEY", "vit-internal-key")

    # Service Discovery
    VIT_STORAGE_URL: str = os.getenv("VIT_STORAGE_URL", "http://vit-storage-svc:8000")
    VIT_NETWORK_URL: str = os.getenv("VIT_NETWORK_URL", "http://vit-network-rpc:8000")

    # AI Config
    DEFAULT_PROVIDER: str = "internal"
    SUPPORTED_PROVIDERS: List[str] = ["internal", "ensemble"]

    # Production Hardware / Execution settings (Phase 5: Configuration)
    GPU_ENABLED: bool = os.getenv("GPU_ENABLED", "false").lower() == "true"
    CPU_FALLBACK: bool = os.getenv("CPU_FALLBACK", "true").lower() == "true"

    # Timeout & Retry Policies
    API_TIMEOUT_SECONDS: int = int(os.getenv("API_TIMEOUT_SECONDS", "30"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

    # Cache Configuration
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))

    # Mock Credentials / API Keys
    PROVIDER_CREDENTIALS: Dict[str, str] = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", "mock-openai-key"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", "mock-claud-key")
    }

    class Config:
        case_sensitive = True

settings = Settings()
