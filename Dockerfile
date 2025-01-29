FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install system dependencies for transformers and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
