# Model Registry

The Model Registry allows for registration, discovery, and management of AI models in the VIT ecosystem.

## Endpoints
- `GET /api/v1/models`: List all registered models.
- `POST /api/v1/models`: Register a new model.
- `GET /api/v1/models/{id}`: Get details for a specific model.
- `PATCH /api/v1/models/{id}`: Update model metadata or status.
- `DELETE /api/v1/models/{id}`: Remove a model from the registry.

## Model Schema
Models include `id`, `name`, `version`, `capabilities`, `provider`, and schema definitions for inputs/outputs.
