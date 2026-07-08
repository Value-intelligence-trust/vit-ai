# Model Registry & Versioning

The Model Registry allows for registration, discovery, and management of AI models in the VIT ecosystem.

## Endpoints
- `GET /api/v1/models`: List all registered models.
- `POST /api/v1/models`: Register a new model.
- `POST /api/v1/models/{id}/versions`: Add a new version to an existing model.
- `PATCH /api/v1/models/{id}`: Update model metadata or active version.

## Model Versioning
Supports side-by-side versions. Models can have multiple versions (`ModelVersion`), with one designated as `active_version` for inference.
