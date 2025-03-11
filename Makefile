REPO = $(shell git config --get remote.origin.url | cut -d: -f2 | cut -d. -f1)
ECR = 264318998405.dkr.ecr.us-west-2.amazonaws.com
REGISTRY = "$(ECR)/$(REPO)"
APP = $(notdir $(CURDIR))
TAG = $(shell git rev-parse --short HEAD)
DOCKER_REPO = ghcr.io/apptoybox

PYTHON = $(VIRTUAL_ENV)/bin/python3
PIP = $(VIRTUAL_ENV)/bin/pip
PYTEST = $(VIRTUAL_ENV)/bin/pytest
PORT = 9856

help:
	@echo "Run make <target> where target is one of the following..."
	@echo
	@echo "  development-requirements - install required libraries in virtual environment"
	@echo "  requirements  - install required libraries in virtual environment"
	@echo "  test          - run tests with pytest"
	@echo "  lint          - run flake8 and pylint"
	@echo "  black         - run black to format code"
	@echo "  isort         - run isort to sort imports"
	@echo "  favicon       - generate favicon"
	@echo "  local-run     - run the API locally"
	@echo "  container-run - run the API in a docker container"
	@echo "  build         - build docker container"
	@echo "  run           - run the API in a docker container"
	@echo "  clean         - stop local container, clean up workspace"

development-requirements:
	$(PIP) install --upgrade pip
	$(PIP) install -r development-requirements.txt

requirements:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m flake8 --ignore=E501,E231 *.py
	$(PYTHON) -m pylint --errors-only --disable=C0301 *.py
	$(PYTHON) -m black --diff *.py
	$(PYTHON) -m isort --diff *.py

black-sort:
	$(PYTHON) -m black *.py
	$(PYTHON) -m isort *.py

favicon:
	$(PYTHON) create_favicon.py

test-local:
	$(PYTEST) -v

local:
	@echo "http://localhost:$(PORT)"
	uvicorn main:app --reload --host 0.0.0.0 --port=$(PORT)

login:
	aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin $(ECR)

build: requirements lint test favicon
	docker build --tag $(REPO):$(TAG) --tag $(REGISTRY):$(TAG) .

push:
	docker push $(REGISTRY):$(TAG)

container:
	@echo "http://localhost:$(PORT)"
	docker run --rm -it --publish $(PORT):8000 --name $(APP) $(APP):latest

test-container:
	docker container stop $(APP) || true
	docker container rm $(APP) || true
	@echo "http://localhost:$(PORT)"
	docker run --rm -it --detach --publish $(PORT):8000 --name $(APP) $(APP):latest
	@sleep 1
	@curl -s "http://localhost:$(PORT)/today" | $(PYTHON) -m json.tool
	@curl -s "http://localhost:$(PORT)/tomorrow" | $(PYTHON) -m json.tool
	@curl -s "http://localhost:$(PORT)/lastnight" | $(PYTHON) -m json.tool | grep "Not Found"
	@echo "Tests passed."
	docker container stop $(APP)

test: test-local test-container

list-image:
	docker image ls | grep $(APP)

stop:
	docker container stop $(APP) || true
	docker container rm $(APP) || true

clean: stop
	docker rmi $(APP):latest || true
	docker rmi $(APP):$(TAG) || true
	@rm -rf ./__pycache__ ./tests/__pycache__
	@rm -f .*~ *.pyc

.PHONY: help development-requirements requirements test lint black-sort favicon local-run container-run test-container-run list-image stop clean
