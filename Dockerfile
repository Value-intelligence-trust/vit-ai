# ── Build stage ──────────────────────────────────────────────────────────────
    FROM python:3.12-slim AS builder

    WORKDIR /app

    RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      && rm -rf /var/lib/apt/lists/*

    COPY requirements.txt .
    RUN pip install --no-cache-dir --upgrade pip && \
      pip install --no-cache-dir --prefer-binary -r requirements.txt

    # Seed model artifacts at build time
    COPY scripts/seed_models.py ./scripts/seed_models.py
    RUN mkdir -p /app/models && MODEL_DIR=/app/models python scripts/seed_models.py

    # ── Final stage ───────────────────────────────────────────────────────────────
    FROM python:3.12-slim

    WORKDIR /app

    # curl is required for the container HEALTHCHECK below
    RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      && rm -rf /var/lib/apt/lists/*

    RUN addgroup --system vituser && adduser --system --group vituser

    COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
    COPY --from=builder /usr/local/bin /usr/local/bin

    COPY app /app/app

    # Copy seeded model artifacts from builder stage
    COPY --from=builder /app/models /app/models

    RUN chown -R vituser:vituser /app

    USER vituser

    ENV PORT=8000
    ENV PYTHONUNBUFFERED=1
    ENV MODEL_DIR=/app/models

    EXPOSE 8000

    HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
      CMD curl -f http://localhost:${PORT}/health || exit 1

    # Shell form so $PORT expands at runtime — Render injects PORT dynamically;
    # hardcoding 8000 in exec form caused the health-check port mismatch.
    CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
    