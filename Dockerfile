# Dockerfile for MetaboMax Pro Flask Application
# HIPAA-Compliant Build

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for WeasyPrint, pdfplumber, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libgirepository1.0-dev \
    gir1.2-pango-1.0 \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional AWS dependencies for Bedrock
RUN pip install --no-cache-dir boto3>=1.28.0 botocore>=1.31.0

# Copy application code
COPY . .

# Create non-root user for security (HIPAA best practice)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    mkdir -p /app/uploads /app/reports && \
    chown -R appuser:appuser /app/uploads /app/reports

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Start Gunicorn with production settings
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "--capture-output", "--enable-stdio-inheritance", "app:app"]
