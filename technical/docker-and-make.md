# Docker and Make

Docker provides a consistent runtime environment for all projects, and Make turns common multi-step workflows into single commands. Together they eliminate "it works on my machine" problems and make projects reproducible.

---

## Why Docker + Make
- **Consistency**: everyone runs the same environment regardless of local setup.  
- **Simplicity**: one-line commands (`make run`, `make test`) hide the complexity of Docker flags.  
- **Reproducibility**: the same Docker image can be rebuilt at any time, ensuring identical results.  

---

## Docker patterns

**Minimal Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "your_package.cli"]
```

**Best practices**
- Use an official slim Python base image.
- Set a `WORKDIR` (`/app`) to keep paths consistent.
- Copy `requirements.txt` first, install, then copy source — leverages caching.
- Avoid installing system packages unless absolutely necessary.
- Don’t include secrets in the image.

**Running with volume mounts**
```bash
docker run --rm -it -v $(pwd):/app -w /app clinic-demo python script.py
```
- `-v $(pwd):/app` mounts the local repo into the container.
- `-w /app` sets the working directory.
- This lets code changes take effect immediately without rebuilding.

## Makefile patterns
```make
IMAGE=clinic-demo
TAG=latest

.PHONY: build run test lint shell

build:
    docker build -t $(IMAGE):$(TAG) .

run:
    docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) python -m your_package.cli

test:
    docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) pytest -q

lint:
    docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) ruff check .

shell:
    docker run --rm -it -v $(PWD):/app -w /app $(IMAGE):$(TAG) bash
```

Wrap common Docker commands in a `Makefile` at the repo root:
- `make build` → builds image
- `make run` → runs app with volume mount for dev loop
- `make test` → runs pytest in container
- `make lint` → ruff
- `make shell` → interactive shell in container

## Examples
- See [`examples/minimal-make/`](./examples/minimal-make/) for a tiny working setup for a complete working setup with a `Dockerfile`, `Makefile`, and `requirements.txt`.
