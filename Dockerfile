# ─── Build Stage ──────────────────────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project specification files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv (creates a .venv directory)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ─── Runner Stage ─────────────────────────────────────────────────────────────
FROM python:3.12-alpine AS runner

WORKDIR /app

# Prevent Python from writing .pyc files & buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Install system dependencies needed for runtimes (e.g. libpq for PostgreSQL)
RUN apk add --no-cache libpq libjpeg-turbo libpng

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy codebase
COPY . .

# Create directory structures for static, media and logs
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Create a non-privileged user and group for running the container
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

# Switch to the non-privileged user
USER appuser

# Expose Django port
EXPOSE 8000

# Gunicorn entrypoint serving config.wsgi
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
