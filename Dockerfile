# XTrillion Demo Dockerfile
# Using multi-stage build for smaller final image

# Build stage
FROM python:3.10-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    cmake \
    libboost-all-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Runtime stage
FROM python:3.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1000 xtrillion

# Set working directory
WORKDIR /app

# Copy application files
COPY --chown=xtrillion:xtrillion . /app/

# Create necessary directories
RUN mkdir -p /app/.streamlit && \
    chown -R xtrillion:xtrillion /app

# Switch to non-root user
USER xtrillion

# Default port (Railway will override with $PORT)
ENV PORT=8501
EXPOSE $PORT

# Set environment variables
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Health check with longer start period for Streamlit
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:$PORT/_stcore/health || exit 1

# Run the application with better URL handling
CMD streamlit run xtrillion_guinness_nav.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.baseUrlPath="" \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false