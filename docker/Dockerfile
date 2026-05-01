FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        postgresql-client \
        curl \
        supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY requirements requirements/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements/prod.txt

COPY ./app /app
COPY ./scripts /scripts

EXPOSE 8000

RUN chmod +x /scripts/*
RUN mkdir -p /var/log/app /var/log/supervisor

ENTRYPOINT ["/scripts/entrypoint.sh"]