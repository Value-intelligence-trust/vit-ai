# Dataset Registry

The Dataset Registry manages training and validation datasets for the VIT ecosystem.

## Integration
Datasets are registered in `vit-ai` and metadata is stored locally, while the actual data blobs are stored in `vit-storage`.

## Endpoints
- `GET /api/v1/datasets`: List all registered datasets.
- `POST /api/v1/datasets`: Register a new dataset metadata.
- `GET /api/v1/datasets/{id}`: Retrieve dataset metadata.
- `DELETE /api/v1/datasets/{id}`: Remove a dataset from the registry.

## Schema
- `id`: Unique identifier.
- `name`: Dataset name.
- `version`: Version string.
- `checksum`: SHA256 hash for data integrity.
- `storage_id`: Link to the blob in `vit-storage`.
