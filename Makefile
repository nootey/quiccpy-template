default: run

run:
	python -m main

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

typecheck:
	uv run mypy .

test:
	uv run --group dev pytest
