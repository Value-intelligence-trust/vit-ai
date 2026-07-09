# Backwards Compatibility Guide & Adapters

To ensure a seamless transition of intelligence capabilities from the legacy local implementations in the `vit` repository to the unified `vit-ai` platform, we have designed backward compatibility adapters and clear API/SDK contracts.

---

## 1. Compatibility Adapters

For the core business platform (`vit`) to remain untouched in its business domain logic while executing its ML tasks in `vit-ai`, the following adapters are provided:

### Python Bridge Client (for `vit`)
This Python class is a drop-in replacement for the legacy `ModelOrchestrator` inside `vit`. It delegates all predictions and explanation queries to `vit-ai` over HTTP/REST.

```python
import httpx
from typing import Dict, Any, Optional

class VitAIBridgeClient:
    def __init__(self, base_url: str = "http://vit-ai-service:8000", api_key: str = "vit-internal-key"):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    def predict_ensemble(self, market_odds: Dict[str, float]) -> Dict[str, Any]:
        """
        Drop-in replacement for ModelOrchestrator.orchestrate().
        Sends odds to vit-ai and returns the unified prediction.
        """
        endpoint = f"{self.base_url}/api/v1/ensemble"
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(endpoint, json={"market_odds": market_odds}, headers=self.headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise RuntimeError(f"vit-ai returned status {response.status_code}: {response.text}")
        except Exception as e:
            # High resiliency fallback: return standard vig-free odds as naive baseline
            return self._fallback_prediction(market_odds)

    def explain_prediction(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Drop-in replacement for legacy attribution/explainability tools.
        """
        endpoint = f"{self.base_url}/api/v1/explain"
        with httpx.Client() as client:
            response = client.post(endpoint, json=payload, headers=self.headers)
            return response.json()

    def _fallback_prediction(self, odds: Dict[str, float]) -> Dict[str, Any]:
        # Naive fallback
        h, d, a = odds.get("home", 2.0), odds.get("draw", 3.0), odds.get("away", 3.5)
        total = (1/h) + (1/d) + (1/a)
        return {
            "prediction": {
                "home_prob": round((1/h)/total, 4),
                "draw_prob": round((1/d)/total, 4),
                "away_prob": round((1/a)/total, 4),
                "over_25_prob": 0.5,
                "btts_prob": 0.5,
                "home_xg": 1.2,
                "away_xg": 1.0,
                "confidence": {"1x2": 0.5},
                "match_quality_rating": {
                    "score": 50.0,
                    "grade": "C",
                    "label": "Fallback Naive",
                    "home_advantage_bias": 0.0,
                    "components": {}
                },
                "attribution": []
            },
            "confidence": 0.5,
            "explanation": "Fallback execution due to vit-ai communication failure.",
            "latency": 0.001
        }
```

---

## 2. API Contract Mapping

| Legacy Call (inside `vit`) | Unified `vit-ai` API Endpoint | Payload Mapping |
| :--- | :--- | :--- |
| `ModelOrchestrator.predict(odds)` | `POST /api/v1/ensemble` | `{"market_odds": {"home": 2.0, "draw": 3.0, "away": 3.5}}` |
| `model_loader.load_model(id)` | `GET /api/v1/models/{id}` | None (Returns JSON Model Metadata with version and active tag) |
| `feature_engineering.get_features()` | `GET /api/v1/features` | None (Fetches all centralized features from the Feature Store) |
| `confidence_intervals()` | `POST /api/v1/explain` | `{"model_id": "production-lstm", "payload": {...}}` |

---

## 3. Deployment & Migration Strategy

1. **Dual Run Phase**: Deploy `vit-ai` side-by-side with the existing `vit` platform. Keep local ML capabilities enabled in `vit` but log differences between local and `vit-ai` predictions.
2. **Feature Toggle**: Introduce an environment variable `USE_REMOTE_AI_ORACLE=true` in `vit` to switch all prediction calls to use the `VitAIBridgeClient` instead of local models.
3. **Deprecate Local ML**: After 14 days of zero discrepancies, delete local pickle files and legacy ML code from `vit`, saving valuable compute and storage resources.
