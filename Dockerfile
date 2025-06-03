# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

# Runtime stage
FROM python:3.11-slim as runtime

WORKDIR /app

RUN addgroup --system appgroup && \
    adduser --system --no-create-home --ingroup appgroup appuser

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./src ./src
COPY ./main.py ./
COPY .env .

ENV PYTHONPATH=/app

EXPOSE 8000

USER appuser

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "main:app"]