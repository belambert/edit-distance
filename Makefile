.PHONY: lint typecheck format isort pyupgrade test ci check

lint:
	uv run pylint edit_distance

typecheck:
	uv run mypy edit_distance test

format:
	uv run black --check --diff edit_distance test

isort:
	uv run isort --check-only --diff edit_distance test

pyupgrade:
	uv run pyupgrade --py39-plus edit_distance/*.py test/*.py

test:
	uv run pytest --cov=. --cov-report=xml .

ci: lint typecheck format isort pyupgrade test

check: ci