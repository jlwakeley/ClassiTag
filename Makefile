# ------------------------------------- Linting and formatting -------------------------------------
format:
	poetry run ruff format classitag/ tests/

check_format:
	poetry run ruff format --check classitag/ tests/

ruff:
	poetry run ruff --fix classitag/ tests/

check_ruff:
	poetry run ruff classitag/ tests/

pytest:
	poetry run pytest -s -vvv --cov=./ --cov-report xml:coverage.xml .

check_typing:
	poetry run mypy classitag/ tests/

