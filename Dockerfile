FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml ./
COPY app ./app

RUN pip install --upgrade pip && pip install .

RUN groupadd --gid 10001 mcp && \
    useradd --uid 10001 --gid 10001 --create-home --shell /usr/sbin/nologin mcp

EXPOSE 8001

USER mcp

CMD ["polymarket-mcp-http"]
