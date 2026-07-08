# Dataset Registry

Manages datasets used for training and validation.

## Integration
Datasets are registered locally and integrated with `vit-storage` for persistent storage of large blobs.

## Endpoints
- `GET /api/v1/datasets`: List datasets.
- `POST /api/v1/datasets`: Register a new dataset.
- `DELETE /api/v1/datasets/{id}`: Remove dataset.
