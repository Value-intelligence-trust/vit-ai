import os
    from pydantic_settings import BaseSettings


    class Settings(BaseSettings):
      APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
      PORT: int = int(os.getenv("PORT", "8000"))
      LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

      # Model storage
      MODEL_DIR: str = os.getenv("MODEL_DIR", "/app/models")

      # vit-storage integration
      VIT_STORAGE_URL: str = os.getenv("VIT_STORAGE_URL", "https://vit-storage-4trt.onrender.com")

      # Internal service auth
      VIT_AI_API_KEY: str = os.getenv("VIT_AI_API_KEY", "")

      # Base L2 oracle
      ORACLE_PRIVATE_KEY: str = os.getenv("ORACLE_PRIVATE_KEY", "")
      UNIVERSAL_ORACLE_ADDRESS: str = os.getenv("UNIVERSAL_ORACLE_ADDRESS", "")

      class Config:
          env_file = ".env"
          extra = "ignore"


    settings = Settings()
    