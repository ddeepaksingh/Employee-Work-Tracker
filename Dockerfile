# ─── Build Stage ──────────────────────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ─── Runner Stage ─────────────────────────────────────────────────────────────
FROM python:3.12-alpine AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# Runtime packages
RUN apk add --no-cache \
    libpq \
    libjpeg-turbo \
    libpng \
    netcat-openbsd \
    su-exec

# Copy virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy application
COPY . .

# Create directories
RUN mkdir -p \
    /app/staticfiles \
    /app/media \
    /app/logs

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

RUN chown -R appuser:appgroup \
    /app/media \
    /app/staticfiles \
    /app/logs

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
