import os
import logging
import time
from fastapi import FastAPI, Request
from app.api.endpoints import router as api_router
from app.core.config import settings
from prometheus_client import make_asgi_app, Counter, Histogram

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s [%(request_id)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("vit-ai")

# Custom logging filter for request_id
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(record, 'request_id', 'no-id')
        return True

logger.addFilter(RequestIdFilter())

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="VIT Network AI/ML Platform",
)

# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "HTTP request latency", ["endpoint"])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(time.time()))
    start_time = time.time()

    # Inject request_id into logger
    extra = {"request_id": request_id}
    logger.info(f"Incoming request: {request.method} {request.url.path}", extra=extra)

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)

    logger.info(f"Finished request: {response.status_code} in {process_time:.4f}s", extra=extra)
    return response

# Standard endpoints
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/ping")
async def ping():
    return "pong"

@app.get("/version")
async def version():
    return {"version": settings.VERSION}

# API V1
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
