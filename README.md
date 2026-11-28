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

The app runs until it gets SIGINT (Ctrl+C) or SIGTERM (`docker stop`). Then it stops each task and exits cleanly.
If one task fails, the app cancels the other tasks.

## Configuration

Config is loaded from `.env`. See `.env.example` for all available fields.

Variables use the `APP_` prefix and `__` as the nested delimiter.
Real environment variables take priority over `.env`.
The app does not start if a value is not valid.

```bash
# Override logging level
APP_LOGGING__LEVEL=DEBUG
```

`APP_ENVIRONMENT` is `local`, `development` or `production`. In `production`, the app writes JSON logs to stdout.
In the other environments, it writes colored text. The log file in `logs/` is always JSON.

## Testing

```bash
make test
# or
uv run --group dev pytest
```

Tests live in `tests/` mirroring the `src/` structure.

```bash
make test-coverage  # coverage report in the terminal and in htmlcov/index.html
```

## Linting

```bash
make lint       # ruff check --fix
make format     # ruff format
make typecheck  # mypy
make pre-push   # lint, format check, typecheck and tests, the same checks as CI
```

Ruff config is in `pyproject.toml`. It adds import order, bug, upgrade, security, simplify and async rules to the
defaults.

## Docker

```bash
docker compose up
```

Compose loads `.env` from the project root and mounts `logs/` into the container.

## Releases

Merging a PR into `main` with a release label creates a Git tag and a GitHub release.

Create these labels in GitHub (Settings → Labels):

| Name            | Bump                          |
|-----------------|-------------------------------|
| `release:minor` | New features (v1.0.0 → v1.1.0) |
| `release:fix`   | Bug fixes (v1.0.0 → v1.0.1)    |
