# VIT-AI Environment Variables

This document lists the environment variables used by the VIT-AI service.

| Variable | Category | Description | Default |
| :--- | :--- | :--- | :--- |
| `PORT` | Required | The port on which the FastAPI application listens. | `8000` |
| `APP_VERSION` | Optional | The version of the application displayed at the `/version` endpoint. | `0.1.0` |
| `PYTHONUNBUFFERED` | Optional | Ensures that the python output is sent straight to terminal (useful for Docker logging). | `1` |

## Secret Management
Currently, no secrets are required for the base production infrastructure. As AI/ML models are integrated, API keys (e.g., OpenAI, Anthropic) or database credentials should be added as **Secret** variables in the Render dashboard.
