"""
VIT-AI service configuration.
All values are loaded from environment variables via pydantic-settings.
No hardcoded URLs or credentials are permitted per VIT Chain engineering directive.
"""
import sys
import logging
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Runtime ───────────────────────────────────────────────────────────
    APP_VERSION: str = "0.1.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # ── Model storage ─────────────────────────────────────────────────────
    MODEL_DIR: str = "/app/models"

    # ── vit-storage integration ───────────────────────────────────────────
    # Required — no default URL; set VIT_STORAGE_URL in environment explicitly.
    VIT_STORAGE_URL: str

    # ── Internal service authentication ───────────────────────────────────
    # Required — inter-service API key; service refuses to start without it.
    VIT_AI_API_KEY: str

    # ── VIT Chain oracle (Chain ID 7764) ──────────────────────────────────
    # Required — used for on-chain oracle settlement; startup aborts if missing.
    ORACLE_PRIVATE_KEY: str
    UNIVERSAL_ORACLE_ADDRESS: str

    @field_validator(
        "VIT_STORAGE_URL",
        "VIT_AI_API_KEY",
        "ORACLE_PRIVATE_KEY",
        "UNIVERSAL_ORACLE_ADDRESS",
        mode="before",
    )
    @classmethod
    def _require_non_empty(cls, v: str, info) -> str:
        if not v or not str(v).strip():
            raise ValueError(
                f"{info.field_name} must be set via environment variable — "
                "empty or missing values are not permitted in any environment."
            )
        return v


def _build_settings() -> Settings:
    """Construct settings, aborting startup on missing required variables."""
    try:
        return Settings()
    except Exception as exc:
        logger.critical("[config] Startup aborted — missing required env var: %s", exc)
        sys.exit(1)


settings = _build_settings()
