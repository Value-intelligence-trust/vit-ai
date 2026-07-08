# Inference & Embedding Pipeline

The Inference Pipeline orchestrates the execution of AI models.

## Support Operations
- **General Inference**: `/api/v1/infer`
- **Embedding Service**: `/api/v1/embed` - Returns vector representations.
- **Ensemble Inference**: `/api/v1/ensemble` - Executes multi-model consensus.

## Features
- **Provider Abstraction**: Decouples model logic from the API.
- **Extracted Math Utilities**: Uses standardized math helpers (`app/utils/math.py`) for consistent predictions.
- **Latency Tracking**: Every response includes processing latency and metadata.
