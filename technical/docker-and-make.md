# Docker and Make

## Why Docker + Make
- Consistent execution across machines.
- Single-command workflows for students and TAs.

## Minimal Dockerfile
- Use official Python base, set `WORKDIR /app`.
- `COPY requirements.txt` then `pip install -r requirements.txt`.
- `COPY` source code last to leverage layer caching.
- No conda/pyenv inside images.

## Makefile patterns
- `make build` → builds image
- `make run` → runs app with volume mount for dev loop
- `make test` → runs pytest in container
- `make lint` → ruff/black/isort
- `make shell` → interactive shell in container

## Rebuild after dependency changes
- Edit `requirements.txt`, then `make build` to rebuild the image.

## Examples
- See `examples/minimal-make/` for a tiny working setup.
