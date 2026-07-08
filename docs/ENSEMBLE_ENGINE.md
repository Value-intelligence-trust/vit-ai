# Ensemble Engine

The Ensemble Engine provides advanced orchestration for multi-model consensus, serving as the core of the Intelligence Oracle.

## Intelligence Oracle Stack
The engine is aligned with the VIT Core 13-model ensemble:
- **Models**: LSTM, XGBoost, Transformers, Elo, Poisson, and more.
- **Aggregation**: Dynamic weighted voting based on registered "internal" models.
- **Math Utilities**: Centralized logic for normalization, vig-free calculations, and XG estimation (`app/utils/math.py`).

## Orchestration Logic
- **Weighted Voting**: Combine results based on model weights and historical performance.
- **Confidence Averaging**: Compute ensemble-wide confidence scores.
- **Fallback Routing**: Automatically route to backup models if primary models are inactive.
- **Explainability**: Returns detailed attribution and match quality metrics.

## Endpoints
- `POST /api/v1/ensemble`: Execute ensemble inference. Returns full `prediction_details`.
- `GET /api/v1/ensemble/status`: Monitor engine and participant status.
