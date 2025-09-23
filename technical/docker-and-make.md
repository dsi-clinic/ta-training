# Docker and Make

Docker provides a consistent runtime environment for all projects, and Make turns common multi-step workflows into single commands. Together they eliminate "it works on my machine" problems and make projects reproducible.

---

## Why Docker + Make
- **Consistency**: everyone runs the same environment regardless of local setup.  
- **Simplicity**: one-line commands (`make run`, `make test`) hide the complexity of Docker flags.  
- **Reproducibility**: the same Docker image can be rebuilt at any time, ensuring identical results.  

---

## Docker patterns

**Modern Dockerfile with uv**
```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Default command
CMD ["uv", "run", "python", "app.py"]
```

**Best practices**
- Use the official `uv` base image for fast, modern Python package management.
- Set a `WORKDIR` (`/app`) to keep paths consistent.
- Copy `pyproject.toml` and `uv.lock` first, install dependencies, then copy source — leverages Docker layer caching.
- Use `uv sync --frozen --no-dev` for reproducible builds from lock files.
- Use `uv run` to execute Python commands within the managed environment.
- Avoid installing system packages unless absolutely necessary.
- Don't include secrets in the image.

**Running with volume mounts**
```bash
docker run --rm -it -v $(pwd):/app -w /app clinic-demo uv run python script.py
```
- `-v $(pwd):/app` mounts the local repo into the container.
- `-w /app` sets the working directory.
- This lets code changes take effect immediately without rebuilding.

## Makefile patterns
```make
IMAGE=clinic-demo
TAG=latest

.PHONY: build run test lint shell clean sync

# Build Docker image
build:
	docker build -t $(IMAGE):$(TAG) .

# Run the main application
run:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv run python app.py

# Run tests
test:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv run pytest -q

# Run linting
lint:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv run ruff check .

# Interactive shell in container
shell:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) bash

# Sync dependencies (run after updating pyproject.toml)
sync:
	docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) uv sync

# Clean up Docker images
clean:
	docker rmi $(IMAGE):$(TAG) || true
```

Wrap common Docker commands in a `Makefile` at the repo root:
- `make build` → builds image with uv dependencies
- `make run` → runs app with volume mount for dev loop
- `make test` → runs pytest in container via uv
- `make lint` → runs ruff via uv
- `make shell` → interactive shell in container
- `make sync` → updates dependencies from pyproject.toml
- `make clean` → removes Docker images

## Key differences from pip-based workflows

**Dependency management:**
- Dependencies are defined in `pyproject.toml` instead of `requirements.txt`
- Lock files (`uv.lock`) ensure reproducible builds
- `uv sync` replaces `pip install -r requirements.txt`

**Execution:**
- Use `uv run python script.py` instead of direct `python script.py`
- uv manages the virtual environment automatically
- Development dependencies are handled separately with `[project.optional-dependencies]`

**Performance benefits:**
- Faster dependency resolution and installation
- Better caching and lock file support
- Modern Python packaging standards

## Examples
- See [`examples/minimal-make/`](./examples/minimal-make/) for a complete working setup with a `Dockerfile`, `Makefile`, and `pyproject.toml` using the modern uv workflow.
