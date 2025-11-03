FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (Tesseract OCR)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway uses dynamic ports)
EXPOSE 8000

# Copy start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run application (PORT env var set by Railway)
CMD ["/app/start.sh"]

