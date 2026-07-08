---
name: Production Readiness
about: Verify production readiness for a new service
title: '[READINESS] '
labels: production, audit
assignees: ''

---

## Service Name
vit-ai

## Readiness Checklist
- [x] Dockerfile (multi-stage, non-root)
- [x] .dockerignore
- [x] requirements.txt (pinned)
- [x] FastAPI (base endpoints)
- [x] Health Check (/health)
- [x] Version Endpoint (/version)
- [x] render.yaml
- [x] Environment Documentation

## Validation Status
- Local Runtime: Verified
- Docker Build: Pending (Sandbox restriction)
- Render Deployment: Pending (Merge to main)
