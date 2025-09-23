IMAGE=clinic-demo
TAG=latest

.PHONY: build run shell test lint clean sync

# Build Docker image
build:
	docker build -t $(IMAGE):$(TAG) .

# Run the main application
run:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv run python app.py

# Interactive shell in container
shell:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) bash

# Run tests
test:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv run pytest -q

# Run linting
lint:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv run ruff check .

# Sync dependencies (run this after updating pyproject.toml)
sync:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv sync

# Clean up Docker images
clean:
	docker rmi $(IMAGE):$(TAG) || true
