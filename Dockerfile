# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

# Install necessary packages and utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    nano \
    dos2unix \
    && pip install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

# Copia il file requirements.txt nel container
COPY deployment/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --upgrade pip

COPY . .

# Set environment variables for Flask
ENV FLASK_RUN_PORT 5005

# Convert scripts to Unix format and ensure requirements.txt is available before install
RUN find /app/deployment -type f -name "*.sh" -exec dos2unix {} \; -exec chmod +x {} \;

# Run the application using gunicorn (can be overridden by docker-compose)
CMD ["gunicorn", "--config", "/app/deployment/gunicorn-cfg.py", "run:app"]