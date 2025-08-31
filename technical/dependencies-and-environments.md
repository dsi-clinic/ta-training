# Dependencies and Environments

## Python dependencies
- Pin versions in `requirements.txt` (e.g., `pandas==2.2.2`).
- Avoid banned modules per Clinic policy; justify non-standard libs.

## Installing deps
- Add package to `requirements.txt`; rebuild Docker image.
- Avoid `pip install` inside notebooks.

## Pre-commit and CI
- `pre-commit` hooks: ruff, black, isort, end-of-file-fixer.
- Optional CI: run lint/tests on PR.

## Cluster environments
- If required, include a conda/micromamba recipe for the cluster only.
- Document how container and cluster envs interoperate.
