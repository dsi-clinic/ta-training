# Dependencies and Environments

All code should run inside the provided Docker or cluster environment. Avoid creating ad-hoc virtual environments or installing packages directly on your laptop — this breaks reproducibility and makes debugging harder.

Inside Docker, we use **[uv](https://github.com/astral-sh/uv)** to manage dependencies. `uv` is a fast, modern Python package manager and resolver. It installs packages much quicker than pip, supports modern Python packaging standards, and works seamlessly inside containers. It also supports locking dependencies for consistent builds across machines.

## Python dependencies

- List all required packages in `pyproject.toml` under the `[project]` section.
- **Pin versions** (e.g., `pandas==2.2.2`) to avoid "works on my machine" issues.
- Use `[project.optional-dependencies]` for development tools like linters and test frameworks.
- Keep dependencies minimal — only include packages the project actually needs.

Example `pyproject.toml`:
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "pandas==2.2.2",
    "numpy==1.26.4",
]

[project.optional-dependencies]
dev = [
    "ruff==0.5.5",
    "pytest==8.2.0",
]
```

## Installing dependencies

- To add a dependency:
  1. Add it to the `dependencies` list in `pyproject.toml`
  2. Run `uv lock` to update the lock file
  3. Rebuild the Docker image:
     ```bash
     make build
     ```
- Never run `pip install` or `uv pip install` inside notebooks or ad-hoc environments.
- Document non-standard libraries in the repo's README so reviewers understand why they're included.

## Lock files

- Always commit `uv.lock` to your repository for reproducible builds.
- The lock file ensures everyone gets exactly the same package versions.
- Use `uv sync --frozen` in Docker builds to install from the lock file.
- Run `uv lock` after updating `pyproject.toml` to regenerate the lock file.

## Cluster environments

- Some projects require running on the DSI cluster.
- For cluster jobs, include a **conda or micromamba environment file** (`environment.yml`).
- Keep the cluster recipe in sync with `pyproject.toml` to avoid divergence.
- Consider using `uv export --format requirements-txt` to generate a `requirements.txt` for cluster compatibility.

## Environment variables

- Use a `.env` file to manage configuration values and secrets (API keys, tokens, database URLs).
- Never hardcode secrets in code or commit them to the repo.
- Add a `.env.example` file showing variable names (but not actual values), e.g.:
  ```
  DB_USER=your_username
  DB_PASS=your_password
  API_KEY=replace_me
  ```
- Document how to load the `.env` in the project README (e.g., with `python-dotenv` or by passing `--env-file` to Docker).
