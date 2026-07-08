# Security & Observability

## Security
- **JWT Authentication**: Secure token-based access.
- **API Key Authentication**: `X-API-KEY` support for internal service-to-service communication.
- **Protected Routes**: Critical endpoints require authentication.

## Observability
- **Prometheus Metrics**: Available at `/metrics`. Tracks request counts and latency.
- **Request ID Tracking**: Correlation IDs (`X-Request-ID`) are tracked across logging and response headers.
- **Structured Logging**: Standardized log format with request context.
