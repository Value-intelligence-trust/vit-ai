# VIT AI Duplication Audit & Migration Plan

## Summary
The VIT ecosystem currently has duplicated AI logic across `vit` (core) and `vit-ai` (platform). This audit identifies overlaps and proposes a migration strategy to centralize intelligence in `vit-ai`.

## 1. Inventory Comparison

| Component | `vit` (Core) Implementation | `vit-ai` (Platform) Implementation | Overlap | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Model Registry** | `services/ml_service/model_loader.py` | `app/services/registry.py` | High | Migrate registry to `vit-ai`. |
| **Inference** | `services/ml_service/models/model_orchestrator.py` | `app/services/inference.py` | High | Centralize inference in `vit-ai`. |
| **Ensemble Engine** | `ModelOrchestrator` (13-model logic) | `app/services/ensemble.py` (Skeleton) | High | Migrate ensemble logic to `vit-ai`. |
| **Training** | `scripts/train_all_models.py` | (Planned) | Medium | Move generic training jobs to `vit-ai`. |
| **Feature Store** | `scripts/feature_engineering.py` | `app/api/endpoints.py` | Medium | Centralize features in `vit-ai`. |
| **Explainability** | Confidence intervals in `ModelOrchestrator` | `/explain` endpoint | High | Consolidate in `vit-ai`. |

## 2. Identified Overlaps
- **Model Loading**: `vit` manually loads `.pkl` files. `vit-ai` should handle model loading via its Registry.
- **Ensemble Logic**: The weighted voting, confidence averaging, and market-specific math (`_market_to_xg`, `_poisson_pmf`) currently reside in `vit`.
- **Inference Pipeline**: Both repositories define inference flows.

## 3. Migration Plan

### Step 1: Interface Alignment
- Update `vit-ai` schemas to match the input/output structures of `vit`'s 13-model ensemble.
- Implement a bridge client in `vit` to call `vit-ai` endpoints.

### Step 2: Capability Extraction
- Extract the 13 models (LSTM, XGB, etc.) and their weights from `vit`.
- Port the `ModelOrchestrator` logic to `vit-ai`'s `EnsembleEngine`.
- Move market-specific math utilities (`_vig_free`, `_normalise`, etc.) to `vit-ai/app/utils/math.py`.

### Step 3: Service Redirection
- Update `vit` to use `POST /api/v1/ensemble/predict` instead of local inference.
- Disable local ML services in `vit` once verified.

## 4. Backward Compatibility
- Maintain the existing response structure in `vit` by mapping `vit-ai` responses back to the expected legacy format if necessary.

## Conclusion
Centralizing AI in `vit-ai` will reduce technical debt and ensure a single source of truth for the Intelligence Oracle.
