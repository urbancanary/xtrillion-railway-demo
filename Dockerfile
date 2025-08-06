# XTrillion Guinness App Dockerfile - Optimized for Railway
# Single-stage build with retry logic for network resilience

FROM python:3.10-slim

# Set working directory early
WORKDIR /app

# Install system dependencies with retry logic
RUN set -ex && \
    for i in 1 2 3; do \
        apt-get update && \
        apt-get install -y --no-install-recommends \
            build-essential \
            gcc \
            g++ \
            libgomp1 \
            curl \
            ca-certificates && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* && \
        break || \
        if [ $i -lt 3 ]; then \
            echo "Retrying apt-get (attempt $i/3)..."; \
            sleep 5; \
        else \
            echo "Failed to install dependencies after 3 attempts"; \
            exit 1; \
        fi; \
    done

# Copy requirements first for better caching
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies with retry logic
RUN set -ex && \
    python -m pip install --upgrade pip && \
    for i in 1 2 3; do \
        pip install --no-cache-dir -r requirements.txt && \
        break || \
        if [ $i -lt 3 ]; then \
            echo "Retrying pip install (attempt $i/3)..."; \
            sleep 5; \
        else \
            echo "Failed to install Python dependencies after 3 attempts"; \
            exit 1; \
        fi; \
    done

# Create non-root user
RUN useradd -m -u 1000 xtrillion

# Copy application files
COPY --chown=xtrillion:xtrillion . /app/

# Create necessary directories and set permissions
RUN mkdir -p /app/.streamlit && \
    chown -R xtrillion:xtrillion /app && \
    chmod -R 755 /app

# Switch to non-root user
USER xtrillion

# Default port (Railway will override with $PORT)
ENV PORT=8501
EXPOSE $PORT

# Set environment variables
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Health check with Railway-optimized settings
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:$PORT/_stcore/health || exit 1

# Run the application with better URL handling
CMD streamlit run guinness_app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.baseUrlPath="" \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false