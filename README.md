# vit-ai
VIT Network AI/ML models — 13-model ensemble powering the Intelligence Oracle

## Overview
This service provides the AI/ML intelligence layer for the VIT Network. It is built using FastAPI and containerized with Docker.

## Production Readiness
The repository has been productionized following the VIT-AI Production Readiness task (TRACK-015B).

### Features
- **FastAPI Framework**: High-performance Python API.
- **Production Infrastructure**: Multi-stage Docker build, non-root user execution.
- **Health Monitoring**: Standard `/health`, `/ping`, and `/version` endpoints.
- **Render Compatible**: Includes `render.yaml` for easy deployment.

## Getting Started

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker
Build and run with Docker:
```bash
docker build -t vit-ai .
docker run -p 8000:8000 vit-ai
```

## Documentation
- [Readiness Audit](docs/deployment/VIT_AI_READINESS_AUDIT.md)
- [Environment Variables](docs/deployment/VIT_AI_ENVIRONMENT.md)
- [Deployment Report](docs/deployment/VIT_AI_DEPLOYMENT_REPORT.md)
