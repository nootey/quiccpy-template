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

test-coverage:
	uv run --group dev pytest --cov --cov-report=term-missing --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

# Pre push checklist: the same checks as CI
pre-push:
	@uv run ruff check . && echo "lint successful" || (echo "lint failed" && exit 1)
	@uv run ruff format --check . && echo "format successful" || (echo "format failed" && exit 1)
	@uv run mypy . && echo "typecheck successful" || (echo "typecheck failed" && exit 1)
	@uv run --group dev pytest && echo "tests successful" || (echo "tests failed" && exit 1)
