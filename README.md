# quiccpy-start

A generic Python project template using `uv`, `structlog`, `pydantic`, and `pydantic-settings`.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
cp .env.example .env
uv sync --group dev
uv run pre-commit install
```

## Running

```bash
make run
# or
uv run python -m main
```

## Configuration

Config is loaded from `.env`. See `.env.example` for all available fields.

Variables use the `APP_` prefix and `__` as the nested delimiter.
Real environment variables take priority over `.env`.

```bash
# Override logging level
APP_LOGGING__LEVEL=DEBUG
```

## Testing

```bash
make test
# or
uv run --group dev pytest
```

Tests live in `tests/` mirroring the `src/` structure.

## Linting

```bash
make lint
# or
uv run ruff check . --fix
```

## Docker

```bash
docker compose up
```

Compose loads `.env` from the project root and mounts `logs/` into the container.
