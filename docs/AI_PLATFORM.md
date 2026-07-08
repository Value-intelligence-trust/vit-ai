# VIT AI Intelligence Platform

## Overview
The VIT AI Intelligence Platform is the centralized AI engine for the VIT ecosystem. It provides model management, inference orchestration, ensemble scoring, and dataset/feature handling.

## Components
- **AI Kernel**: Manages the lifecycle and status of the AI engine.
- **Model Registry**: Production-ready registry for tracking model metadata, side-by-side versions, and capabilities.
- **Inference Pipeline**: Orchestrates synchronous and asynchronous inference requests, including embedding services.
- **Ensemble Engine**: Provides weighted consensus and ensemble scoring across multiple models, aligned with VIT Core's 13-model stack.
- **Dataset Registry**: Manages datasets with integration for `vit-storage`.
- **Feature Store**: Centralized repository for feature registration and retrieval.
- **Training Manager**: Lifecycle management for AI training jobs.
- **Security & Observability**: JWT/API Key authentication, Prometheus metrics, and Request ID correlation.

## API Architecture
The platform follows a RESTful API design with standard endpoints for health, metrics, and domain-specific AI logic.
