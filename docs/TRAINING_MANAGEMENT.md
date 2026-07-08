# Training Job Management

Track and manage the lifecycle of AI training jobs.

## Endpoints
- `POST /api/v1/training/jobs`: Queue a new training job.
- `GET /api/v1/training/jobs`: List all jobs.
- `GET /api/v1/training/jobs/{id}`: Get status and logs for a specific job.

## Job Statuses
- `queued`
- `running`
- `completed`
- `failed`
