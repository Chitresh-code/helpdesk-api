# syntax=docker/dockerfile:1

FROM python:3.13-slim AS base

# Builder stage: install uv, create venv, install dependencies
FROM base AS builder

# Install uv (prebuilt binary)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for better cache utilization
COPY --link pyproject.toml requirements.txt ./

# Set PATH so that uv inside .venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Create virtual environment and install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    uv pip install -r requirements.txt

# Copy application code
COPY --link app ./app

# Final stage: minimal runtime image
FROM base AS final

WORKDIR /app

# Create non-root user
RUN addgroup --system appuser && adduser --system --ingroup appuser appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv
# Copy application code from builder
COPY --from=builder /app/app ./app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
