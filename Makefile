.PHONY: lint typecheck format test ci check

lint:
	poetry run pylint edit_distance

typecheck:
	poetry run mypy edit_distance test

format:
	poetry run black --check --diff edit_distance test

test:
	poetry run pytest --cov=. --cov-report=xml .

ci: lint typecheck format test

check: ci