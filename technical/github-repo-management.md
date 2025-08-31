# GitHub Repo Management

## Branch strategy (lightweight)
- `main`: always deployable; protected.
- `dev`: integration branch for the current quarter (optional).
- Feature branches: short-lived, named `feat/xyz`, `fix/abc`.

## Pull requests
- Draft PR early; convert to ready when tests/lint pass.
- Require review; squash merge to keep history clean.
- Link issues and include a short changelog in the description.

## Keeping branches fresh
- Sync `dev` from `main` regularly; rebase feature on `dev` before merge.
- Resolve conflicts locally and push.

## Reviewing and merging
- Run `make test`, `make lint`, and example pipelines if provided.
- After merge: delete source branch.

## Repo hygiene
- `.gitignore` tuned; no data, secrets, or large binaries.
- Tag releases for major milestones.
