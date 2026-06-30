FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# ---- Non-root user (security) ----
RUN useradd -m appuser

RUN mkdir -p /app/generated /app/data \
    && chown -R appuser:appuser /app/generated /app/data

USER appuser

CMD ["python", "main.py"]
