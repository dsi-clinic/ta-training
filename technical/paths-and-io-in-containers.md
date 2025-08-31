# Paths and I/O in Containers

## The nuance
- “Relative paths only” is ideal, but inside Docker the *working directory* controls what “relative” means.

## Recommendations
- In Dockerfile: `WORKDIR /app`. In Make targets: run with `-w /app`.
- In code: use `pathlib.Path` relative to `Path(__file__).parent` or a project root helper.
- For local dev: use bind mounts `-v $(PWD):/app` so relative paths in code match the host repo layout.

## Patterns
- Project root helper:

  ```python
  from pathlib import Path
  PROJECT_ROOT = Path(__file__).resolve().parents[1]  # adjust for your layout
  DATA_DIR = PROJECT_ROOT / "data"
  ```
- Avoid hard-coded absolute paths; pass paths as parameters or CLI flags.

## File outputs
- Write outputs under a known subdir (artifacts/, outputs/) and gitignore it.
- Ensure Make/Docker run with the same working dir to keep paths consistent.