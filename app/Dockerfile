FROM python:3.11-slim-bookworm AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PATH=/opt/venv/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv

WORKDIR /build

COPY pyproject.toml README.md /build/
COPY openetr /build/openetr
COPY app/requirements.txt /build/app/requirements.txt

RUN pip install . \
    && pip install -r app/requirements.txt

FROM python:3.11-slim-bookworm AS runtime

ARG OPENETR_GIT_COMMIT=unknown

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/opt/venv/bin:$PATH \
    OPENETR_GIT_COMMIT=${OPENETR_GIT_COMMIT}

RUN groupadd --gid 10001 openetr \
    && useradd --uid 10001 --gid 10001 --create-home openetr \
    && mkdir -p /home/openetr/.openetr \
    && chown openetr:openetr /home/openetr/.openetr

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY app /app/app
COPY assets /app/assets

USER openetr

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import json, urllib.request; response = json.load(urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)); assert response.get('status') == 'ok'"

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
