.PHONY: lint typecheck format isort pyupgrade test ci check

lint:
	poetry run pylint edit_distance

typecheck:
	poetry run mypy edit_distance test

format:
	poetry run black --check --diff edit_distance test

isort:
	poetry run isort --check-only --diff edit_distance test

pyupgrade:
	poetry run pyupgrade --py39-plus edit_distance/*.py test/*.py

test:
	poetry run pytest --cov=. --cov-report=xml .

ci: lint typecheck format isort pyupgrade test

check: ci