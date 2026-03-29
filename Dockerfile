# Conduit MCP server (HTTP/SSE).
FROM python:3.14-slim-trixie

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY conduit ./conduit

RUN pip install --no-cache-dir . \
    && useradd --create-home --no-log-init --uid 1000 appuser

USER appuser

EXPOSE 8000

# SSE transport: per-request token via X-PHABRICATOR-TOKEN; PHABRICATOR_URL required at startup.
CMD ["conduit-mcp", "--host", "0.0.0.0", "--port", "8000"]
