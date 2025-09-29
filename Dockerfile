FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && groupadd --gid 1000 app \
    && useradd --uid 1000 --gid app --create-home --shell /usr/sbin/nologin app

COPY app ./app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python - <<'PY' || exit 1
import json
import sys
import urllib.request

try:
    with urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2) as response:
        if response.status != 200:
            sys.exit(1)
        payload = json.load(response)
except Exception:  # pragma: no cover - executed within container runtime
    sys.exit(1)
else:
    sys.exit(0 if payload.get('status') == 'ok' else 1)
PY

CMD ["python", "-m", "app.main"]
