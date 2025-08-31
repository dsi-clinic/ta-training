IMAGE=clinic-demo
TAG=latest

.PHONY: build run shell test lint

build:
	docker build -t $(IMAGE):$(TAG) .

run:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) python app.py

shell:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) bash

test:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) pytest -q

lint:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) ruff check .
