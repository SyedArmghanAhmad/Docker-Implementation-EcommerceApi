# Build stage
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt  # Removed --no-install-recommends

# Runtime stage
FROM python:3.10-slim

# Install runtime dependencies (this is where --no-install-recommends belongs)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY ./app ./app

# Create a non-root user with random UID
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app.app:app"]