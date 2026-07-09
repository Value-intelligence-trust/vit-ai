# AI Configuration Reference

This document serves as the centralized configuration guide for all AI and Machine Learning infrastructure in the `vit-ai` platform. It specifies environment variables, hardware controls, timeout/retry policies, and credential security.

## 1. Environment Variables Map

| Variable | Description | Type | Default | Validation / Constraint |
| :--- | :--- | :--- | :--- | :--- |
| `SECRET_KEY` | JWT signing secret | String | `supersecret` | Must be 32+ chars in production |
| `INTERNAL_API_KEY` | Key for inter-service RPC auth | String | `vit-internal-key` | Must be a strong unique token |
| `VIT_STORAGE_URL` | Endpoint for model storage | URL | `http://vit-storage-svc:8000` | Must be a valid HTTP/HTTPS URL |
| `VIT_NETWORK_URL` | Endpoint for core VIT platform | URL | `http://vit-network-rpc:8000` | Must be a valid HTTP/HTTPS URL |
| `GPU_ENABLED` | Enable CUDA acceleration | Boolean | `false` | Case-insensitive boolean |
| `CPU_FALLBACK` | Fallback to CPU if CUDA fails | Boolean | `true` | Case-insensitive boolean |
| `API_TIMEOUT_SECONDS` | Maximum seconds for inference | Integer | `30` | `> 0` |
| `MAX_RETRIES` | Connection/API call retries | Integer | `3` | `>= 0` |
| `CACHE_ENABLED` | Enable in-memory inference caching | Boolean | `true` | Case-insensitive boolean |
| `CACHE_TTL_SECONDS` | Time-to-Live for cached predictions | Integer | `300` | `> 0` |
| `OPENAI_API_KEY` | OpenAI API Credential | String | `mock-openai-key` | Required if OpenAI provider is used |
| `ANTHROPIC_API_KEY` | Anthropic API Credential | String | `mock-claud-key` | Required if Anthropic provider is used |

---

## 2. Hardware Strategy (GPU / CPU Fallback)
The platform is designed to run efficiently in any environment:
- **CUDA/GPU**: When `GPU_ENABLED` is set to `true`, compatible libraries (e.g., PyTorch, TensorFlow) will use CUDA cores.
- **CPU Fallback**: If GPU loading fails or `CPU_FALLBACK` is set to `true`, execution gracefully switches to CPU execution without throwing runtime faults.

## 3. Cache & Network Resiliency
To optimize cost and latency, `vit-ai` incorporates:
- **Prediction Caching**: Redundant inference requests are served from the cache, valid up to `CACHE_TTL_SECONDS`.
- **Inference Timeouts**: To avoid hanging threads, requests are bound by `API_TIMEOUT_SECONDS`.
- **Retry Mechanism**: Transient failures when communicating with external providers (or internal `vit-storage`) are automatically retried up to `MAX_RETRIES` times using exponential backoff.
