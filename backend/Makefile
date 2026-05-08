.PHONY: up down dev start load-fixtures test coverage lint format install install-dev

up:
	docker compose up -d --remove-orphans

down:
	docker compose down --remove-orphans

dev:
	PYTHONPATH=src poetry run uvicorn app_backend.main:app --reload

start:
	PYTHONPATH=src poetry run uvicorn app_backend.main:app --host 0.0.0.0 --port 8000

load-fixtures:
	PYTHONPATH=src poetry run load_fixtures

test:
ifdef filter
	PYTHONPATH=src:. poetry run pytest $(filter) -vv
else
	PYTHONPATH=src:. poetry run pytest -vv
endif

coverage:
	PYTHONPATH=src poetry run pytest --cov=app_backend --cov-report term-missing --cov-report html -vv

lint:
	poetry run ruff check --fix .
	poetry run bandit -r src/ -ll

format:
	poetry run ruff format

install:
	poetry install

install-dev:
	poetry install --with dev
