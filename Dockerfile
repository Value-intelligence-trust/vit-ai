FROM python:3.12-slim

WORKDIR /app

# curl required for HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir --prefer-binary -r requirements.txt

RUN addgroup --system vituser && adduser --system --group vituser

# Application source
COPY app /app/app

# Pre-committed VIT ensemble model artifacts (16 .pkl files seeded by scripts/seed_models.py)
# Committed to the repo so the Docker build never relies on a live seed step.
COPY models /app/models

RUN chown -R vituser:vituser /app

USER vituser

ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV MODEL_DIR=/app/models

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Shell form so $PORT expands at runtime — Render injects PORT dynamically
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
