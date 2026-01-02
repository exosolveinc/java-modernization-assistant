.PHONY: setup test clean lint run-api

setup:
	pip install -r requirements.txt
	pip install -e .

dev-setup:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

test:
	pytest tests/ -v

lint:
	black src tests
	ruff check src tests --fix
	mypy src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/

run-api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t java-modernization-assistant .

docker-run:
	docker-compose up -d
