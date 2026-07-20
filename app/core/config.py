"""
VIT-AI service configuration.
All values are loaded from environment variables via pydantic-settings.
No hardcoded URLs or credentials are permitted per VIT Chain engineering directive.
"""
import logging
from typing import Optional
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
    # Defaults to None when unset; inference routes degrade gracefully.
    VIT_STORAGE_URL: Optional[str] = None

    # ── Internal service authentication ───────────────────────────────────
    # Optional at startup — service starts degraded, auth middleware rejects
    # requests when the key is absent rather than preventing boot.
    VIT_AI_API_KEY: Optional[str] = None

    # ── VIT Chain oracle (Chain ID 7764) ──────────────────────────────────
    # Optional at startup — oracle settlement degrades gracefully when absent.
    ORACLE_PRIVATE_KEY: Optional[str] = None
    UNIVERSAL_ORACLE_ADDRESS: Optional[str] = None


def _build_settings() -> Settings:
    """Construct settings, warning (not aborting) on missing optional vars."""
    try:
        s = Settings()
    except Exception as exc:
        logger.critical("[config] Settings load error — using minimal defaults: %s", exc)
        # Return a minimal settings object so uvicorn can still bind and /ping responds
        s = Settings.model_construct(
            APP_VERSION="0.1.0",
            PORT=8000,
            LOG_LEVEL="INFO",
            MODEL_DIR="/app/models",
            VIT_STORAGE_URL=None,
            VIT_AI_API_KEY=None,
            ORACLE_PRIVATE_KEY=None,
            UNIVERSAL_ORACLE_ADDRESS=None,
        )

    # Warn about missing values — never abort
    _RECOMMENDED = {
        "VIT_STORAGE_URL": s.VIT_STORAGE_URL,
        "VIT_AI_API_KEY": s.VIT_AI_API_KEY,
        "ORACLE_PRIVATE_KEY": s.ORACLE_PRIVATE_KEY,
        "UNIVERSAL_ORACLE_ADDRESS": s.UNIVERSAL_ORACLE_ADDRESS,
    }
    missing = [k for k, v in _RECOMMENDED.items() if not v]
    if missing:
        logger.warning(
            "[config] DEGRADED — the following env vars are not set: %s. "
            "Service starts in degraded mode; affected features will raise errors.",
            ", ".join(missing),
        )
    return s


settings = _build_settings()
