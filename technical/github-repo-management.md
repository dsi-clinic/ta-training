# GitHub Repo Management

Good GitHub practices keep projects collaborative, consistent, and reviewable. Clear branching rules and disciplined pull requests prevent confusion and make code review much easier.

## Suggested Branch Strategy
- **`main`**: always deployable and protected. No one pushes directly to `main`.  
- **`dev`**: integration branch for the current quarter. Feature branches merge here first.  
- **Feature branches**: short-lived and named with student initials, e.g. `th/fix-abc`. This makes it clear who owns a branch.

## Pull Requests
- **Draft early**: open a draft PR when starting work so others can follow progress.  
- **Ready to review**: convert to “Ready for review” only when tests and lint checks pass.  
- **Require review**: at least one reviewer must approve before merging.  
- **Squash merge**: combines all commits from a branch into one on merge. This keeps `main` history clean:
  - Without squash: `main` fills with many “fix typo” commits.  
  - With squash: one commit with a clear message documents the change.  
- **Description**: link related issues and include a short changelog.

## Keeping Branches Fresh
Feature branches should not drift far from `dev`.

**Example workflow**:
```bash
# Update dev from main
git checkout dev
git pull origin main

# Rebase feature branch
git checkout th/fix-abc
git fetch origin
git rebase origin/dev

# Resolve conflicts, then push updated branch
git push --force-with-lease
```

## Reviewing and Merging
- Run `make test` and `make lint` locally before approving.
- If the repo has CI pipelines, verify they are green.
- After merging, delete the source branch (local and remote).

## Repo Hygiene
- Use a tuned `.gitignore`. Never commit:
  - large datasets
  - secrets or API keys
  - intermediate files (.ipynb_checkpoints, .DS_Store)
- Tag major milestones for traceability:
  ```bash
  git tag -a v1.0 -m "First client deliverable"
  git push origin v1.0
  ```

## Pre-commit and CI
- Use [`pre-commit`](https://pre-commit.com) to enforce linting before commits:
  - `ruff check` (style & errors)
  - `ruff format` (auto-formatting)
- This prevents code from being merged unless it passes both checks.
