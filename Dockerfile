FROM python:3.10-slim

# Set working directory
WORKDIR /app

# System deps (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.deploy.txt .


# Install Python deps (NO CACHE, NO OPTIONAL DEPS)
RUN pip install --upgrade pip && pip install --no-cache-dir --no-deps -r requirements.deploy.txt


# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "app.example_main:app", "--host", "0.0.0.0", "--port", "8000"]

