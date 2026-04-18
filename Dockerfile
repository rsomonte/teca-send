FROM python:3.11-slim

# Install system dependencies including Calibre
RUN apt-get update && apt-get install -y \
    calibre \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/  
COPY .env .

# Create necessary directories
RUN mkdir -p /tmp/uploads /tmp/converted

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the application
ENV PYTHONUNBUFFERED=1
WORKDIR /app
CMD ["python", "src/main.py"]
