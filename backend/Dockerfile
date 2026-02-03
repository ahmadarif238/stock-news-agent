FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Command to run uvicorn
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.1 --port ${PORT}"]
