# AI Duplication Report

This report presents a thorough analysis of duplicated AI modules, placeholder implementations, dead code, duplicate configurations, models, pipelines, and utilities between the `vit` and `vit-ai` repositories.

## 1. Duplicated AI Modules & Pipelines

### Finding 1: Model Loading & Registration
- **Description**: Both `vit` and `vit-ai` contain logic for model registry management and loading.
- **Evidence**:
  - `vit` repository has legacy code `services/ml_service/model_loader.py` that manually loads serialized `.pkl` files and keeps track of paths.
  - `vit-ai` repository implements a production-grade `ModelRegistry` under `app/services/registry.py` with custom Pydantic schemas (`ModelVersion`, `ModelCreate`).
- **Resolution**: Use the unified, API-driven `ModelRegistry` inside `vit-ai`. `vit` must fetch loaded model information via `GET /api/v1/models`.

### Finding 2: Multi-Model Ensemble Orchestration
- **Description**: Dual implementations of ensemble orchestration and weighted voting.
- **Evidence**:
  - `vit` has `ModelOrchestrator` inside `services/ml_service/models/model_orchestrator.py` which runs predictions across 13 models.
  - `vit-ai` has `EnsembleEngine` in `app/services/ensemble.py` and `EnsembleProvider` in `app/services/providers.py` to route and score predictions dynamically.
- **Resolution**: Centralize ensemble orchestration inside `vit-ai`'s `EnsembleEngine`. The business layer in `vit` calls `/api/v1/ensemble` or `/api/v1/infer` using the ensemble model ID.

---

## 2. Duplicate Configurations & Utilities

### Finding 3: Mathematical Utilities
- **Description**: Replicated mathematical helpers for sports predictions and model scoring.
- **Evidence**:
  - `vit` contains separate scripts calculating vig-free probabilities, normalization, and poisson PMFs.
  - `vit-ai` centralizes these helpers in `app/utils/math.py` (e.g. `normalise`, `vig_free`, `market_to_xg`, `poisson_pmf`, `confidence_from_probs`, `build_score_matrix`).
- **Resolution**: Deprecate separate math scripts. `vit-ai/app/utils/math.py` is the single source of truth.

### Finding 4: Environment Configurations
- **Description**: Overlapping environment configurations for connecting to auxiliary services (like `vit-storage`).
- **Evidence**:
  - `vit` configures custom storage connections.
  - `vit-ai` defines settings in `app/core/config.py` including `VIT_STORAGE_URL` and `VIT_NETWORK_URL`.
- **Resolution**: Consolidate configuration within `vit-ai` via `Pydantic-Settings` (`app/core/config.py`).

---

## 3. Placeholder and Incomplete Implementations

### Finding 5: Real Model Loaders
- **Description**: `app/services/registry.py` uses mock methods for loading artifacts.
- **Evidence**:
  - `ModelRegistry.load_model_artifact()` prints a log statement and sets a dict: `self.loaded_artifacts[f"{model_id}:{version}"] = {"mock": "artifact"}`.
- **Resolution**: Fully standardize the loaded model artifact using a standardized Model Interface class (`StandardizedModel`), so loaded artifacts are proper objects implementing high-integrity methods (`predict`, `explain`, `validate`, etc.).

### Finding 6: Stream & Shutdown Provider Methods
- **Description**: The Provider interface has missing or inconsistent implementations across providers.
- **Evidence**:
  - `ModelProvider` in `app/services/providers.py` only implements `predict` method. Methods like `stream`, `metrics`, `shutdown` do not exist.
- **Resolution**: Standardize the Provider interface under `app/services/providers.py` and make all three provider classes (`InternalProvider`, `EnsembleProvider`, `AdHocProvider`) inherit and implement them.
