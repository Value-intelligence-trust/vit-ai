# AI Infrastructure Inventory

This document represents the canonical inventory of AI and Machine Learning components across the VIT ecosystem, comparing `vit` (the core business platform) and `vit-ai` (the dedicated AI platform repository).

## 1. Inventory & Mapping

| Component | File | Repository | Maturity | Dependencies | Recommended Destination | Migration Priority |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model Registry** | `services/ml_service/model_loader.py` <br> `app/services/registry.py` | `vit` <br> `vit-ai` | `vit`: Legacy / Prod <br> `vit-ai`: Core Platform | Python, JSON/YAML, `joblib` | `vit-ai` (Centralized `ModelRegistry` under `app/services/registry.py`) | **High** |
| **Inference Pipeline** | `services/ml_service/models/model_orchestrator.py` <br> `app/services/inference.py` | `vit` <br> `vit-ai` | `vit`: Production (Ensemble) <br> `vit-ai`: Production-ready pipeline | FastAPI, Pydantic, Uvicorn | `vit-ai` (Canonical `InferencePipeline` in `app/services/inference.py`) | **High** |
| **Ensemble Engine** | `ModelOrchestrator` (13-model logic) <br> `app/services/ensemble.py` | `vit` <br> `vit-ai` | `vit`: Production <br> `vit-ai`: Production-ready engine | `numpy`, `scikit-learn`, `xgboost` | `vit-ai` (Centralized `EnsembleEngine` in `app/services/ensemble.py`) | **High** |
| **Feature Store** | `scripts/feature_engineering.py` <br> `app/services/feature_store.py` | `vit` <br> `vit-ai` | `vit`: Legacy / Scripts <br> `vit-ai`: Production-ready | Pydantic schemas, DB Client | `vit-ai` (Centralized `FeatureStore` in `app/services/feature_store.py`) | **Medium** |
| **Dataset Registry** | Data management routines <br> `app/services/dataset_registry.py` | `vit` <br> `vit-ai` | `vit`: Implicit <br> `vit-ai`: Production-ready | `vit-storage` Integration, S3 | `vit-ai` (`DatasetRegistry` in `app/services/dataset_registry.py`) | **Medium** |
| **Embedding Services** | Embedding generator scripts <br> `app/services/embedding.py` | `vit` <br> `vit-ai` | `vit`: Scattered <br> `vit-ai`: Standardized service | OpenAI API, HuggingFace, Local | `vit-ai` (`EmbeddingService` in `app/services/embedding.py`) | **High** |
| **Explainability** | Confidence interval calculations <br> `/explain` endpoint | `vit` <br> `vit-ai` | `vit`: Basic <br> `vit-ai`: Complete `/explain` API | Confidence maths, attribution | `vit-ai` (Consolidated in `app/services/base_model.py` and endpoint) | **High** |
| **AI Providers** | Local model wrappers <br> `app/services/providers.py` | `vit` <br> `vit-ai` | `vit`: Basic <br> `vit-ai`: Complete Provider Class | Abstract Base Classes (`ABC`) | `vit-ai` (Standardized `ModelProvider` in `app/services/providers.py`) | **High** |
| **AI Utilities & Math**| Scattered helper functions <br> `app/utils/math.py` | `vit` <br> `vit-ai` | `vit`: Mixed <br> `vit-ai`: Centralized | Python `math`, Poisson formulas | `vit-ai` (`app/utils/math.py`) | **High** |
| **AI Configuration** | Local environment config <br> `app/core/config.py` | `vit` <br> `vit-ai` | `vit`: Legacy config <br> `vit-ai`: Structured Config | `pydantic-settings` | `vit-ai` (`app/core/config.py`) | **High** |

## 2. Destination Strategy
All AI-specific infrastructures reside as a single source of truth inside **`vit-ai`**. The main **`vit`** repository delegates all AI tasks (e.g. predictions, model training status, feature registration, dataset versioning) to **`vit-ai`** via remote API calls, thus keeping business logic decoupled from high-compute ML infrastructure.
