# VIT AI API Reference

## Base URL
`http://vit-ai.onrender.com/api/v1`

## Authentication
- **JWT**: Provide `Authorization: Bearer <token>`
- **Internal API Key**: Provide `X-API-KEY: <key>` for service-to-service communication.

## Registry Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/models` | List all models. |
| POST | `/models` | Register a new model. |
| GET | `/features` | List all features. |
| GET | `/datasets` | List all datasets. |

## Inference Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/infer` | Run inference on a specific model. |
| POST | `/ensemble` | Run the Intelligence Oracle ensemble (13-model). |
| POST | `/embed` | Generate text embeddings. |
| POST | `/explain` | Get prediction explainability data. |

## Training Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/training/jobs` | Queue a new model training job. |
| GET | `/training/jobs` | List all training jobs. |
| GET | `/training/jobs/{id}` | Get job status and logs. |
