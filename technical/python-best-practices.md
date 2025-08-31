# Python Best Practices

## Goals
- Write clear, modular, testable Python.
- Separate computation from I/O.
- Prefer packages/modules over monolithic notebooks.

## Structure and style
- Organize code as importable modules under `src/` or a top-level package.
- Use `if __name__ == "__main__":` for executable entry points.
- Avoid global state; pass parameters explicitly.
- Use `logging` over `print`; configure a basic logger.

## Docstrings and comments
- Module, function, and class docstrings: purpose, params, returns, raises.
- Prefer short, precise comments about *why*, not *what*.

## Notebooks policy
- Notebooks for exploration, not function definitions.
- <20 cells, <10 LOC per cell, narrative markdown.
- All reusable code lives in `.py` modules imported into the notebook.

## Reproducibility
- Deterministic seeds for algorithms where relevant.
- Single source of environment truth (`requirements.txt`), reproducible Docker image.
- Make targets for common tasks (run, test, lint, build).

## Pre-commit and lint
- Enable `pre-commit` with ruff/black/isort hooks.
- CI (optional): run lint/tests on PR.
