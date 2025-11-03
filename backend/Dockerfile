FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (Tesseract OCR and build tools)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Run application (PORT env var set by Koyeb)
CMD ["/app/start.sh"]

