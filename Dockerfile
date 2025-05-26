
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --user poetry

COPY pyproject.toml poetry.lock ./

RUN /root/.local/bin/poetry install --no-root

# Runtime stage
FROM python:3.11-slim as runtime

WORKDIR /app

RUN addgroup --system appgroup && \
    adduser --system --no-create-home --ingroup appgroup appuser

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/poetry.lock /app/pyproject.toml ./

COPY ./src ./src
COPY ./main.py ./
COPY .env .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

EXPOSE 8000

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "main:app"]