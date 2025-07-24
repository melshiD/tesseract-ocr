FROM python:3.10-slim

# Install tesseract and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Kraken and dependencies
RUN apt-get update && apt-get install -y \
    libopenblas-dev \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install kraken

# Install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install handwriting model for Kraken
RUN mkdir -p /app/models && \
    curl -L https://kraken-models.mittagqi.dev/models/2023-07-12-handwriting.mlmodel \
    -o /app/models/handwriting.mlmodel \
    test -s /app/models/handwriting.mlmodel

# Copy code
COPY . .

# Run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
