# GitHub Repo Management

Good GitHub practices keep projects collaborative, consistent, and reviewable. Clear branching rules and disciplined pull requests prevent confusion and make code review much easier.


## Branch Strategy for Student Projects
- **`main`**: Production-ready code, protected branch. Only TAs/mentors merge here.  
- **Feature branches**: Where students do their work. Name with your initials: `jd/add-data-cleaning`
- **Naming convention**: `initials/brief-description` (e.g., `th/fix-plotting`, `jd/add-regression-model`)

**Student workflow:**
1. Create feature branch from latest main: `git checkout -b jd/my-feature`
2. Work and commit regularly: `git commit -m "Add data validation"`
3. Keep branch current with main (see "Keeping Branches Fresh")
4. Open PR when ready for review
5. Address feedback and update PR
6. TA/mentor merges after approval


## Pull Requests
- **Draft early**: open a draft PR when starting work so others can follow progress.  
- **Ready to review**: convert to “Ready for review” only when tests and lint checks pass.  
- **Require review**: at least one reviewer must approve before merging.  
- **Squash merge**: combines all commits from a branch into one on merge. This keeps `main` history clean:
  - Without squash: `main` fills with many “fix typo” commits.  
  - With squash: one commit with a clear message documents the change.  
- **Description**: link related issues and include a short changelog.

## Keeping Branches Fresh

Feature branches should stay current with the main branch to avoid conflicts and ensure your changes integrate smoothly.

**When main gets updated while you're working:**

```bash
# 1. Save your current work (commit or stash)
git add .
git commit -m "WIP: current progress"

# 2. Update main branch
git checkout main
git pull origin main

# 3. Rebase your feature branch (recommended)
git checkout your-feature-branch
git rebase main

# 4. Resolve any conflicts
# Git will pause if there are conflicts - edit files to resolve them
git add .
git rebase --continue

# 5. Update your remote branch
git push --force-with-lease origin your-feature-branch
```

**Alternative: merge approach** (simpler but messier history)
```bash
git checkout your-feature-branch
git pull origin main
git push origin your-feature-branch
```

**When to update your branch:**
- Before opening a pull request
- When you see "This branch is X commits behind main"
- When your PR shows merge conflicts
- Weekly for long-running feature branches

**Why rebase instead of merge?**
- Keeps linear, readable history
- Makes your specific changes clear in the PR
- Easier for reviewers to understand your contributions

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

## Common TA Scenarios

**"Student's PR has merge conflicts"**
```bash
# Guide student through resolving conflicts (don't do it for them)
# 1. Help them understand what conflicts mean
# 2. Walk through the rebase process
git checkout their-feature-branch
git rebase main
# 3. Show them how to read conflict markers and resolve manually
# 4. Ensure they test after resolving conflicts
```

**"Multiple students working on the same files"**
```bash
# Coordinate merge order and communication
# 1. Merge the first PR that's ready
# 2. Have other students rebase their branches:
git checkout student2-branch
git rebase main
# 3. Review conflicts together to avoid duplicated work
```

**"Student force-pushed and lost commits"**
```bash
# Help recover using reflog (if recent)
git reflog
git checkout student-branch
git reset --hard HEAD@{n}  # n = number from reflog showing last good state

# Prevention: teach --force-with-lease instead of --force
git push --force-with-lease origin branch-name
```

**"PR looks good but CI is failing"**
```bash
# Don't merge until CI passes - help student debug
# 1. Check the CI logs together
# 2. Run the failing command locally:
make build  # First check if the container builds
make test
make lint
# 3. Guide them to fix the issue, don't fix it yourself
```

**"Dependencies not working in container"**
```bash
# Common issues with uv and pyproject.toml
# 1. Check if uv.lock is committed
git status  # Should show uv.lock as tracked

# 2. Verify pyproject.toml has dependencies
cat pyproject.toml  # Should see [project] dependencies section

# 3. Test dependency installation
make build  # Should install from uv.lock

# 4. If lock file is missing:
uv lock  # Generate lock file
git add uv.lock
git commit -m "Add dependency lock file"
```

**"Student's branch is way behind main"**
```bash
# Before reviewing, ensure they're current
# 1. Check how many commits behind: look at GitHub PR page
# 2. If >10 commits behind, require update before review
# 3. Guide them through rebase process
# 4. Re-review after update (context may have changed)
```

**"Student wants to work on someone else's branch"**
```bash
# Coordinate handoffs properly
# 1. Original student pushes their current work
# 2. New student creates branch from that work:
git checkout -b alice/continue-bobs-work origin/bob/original-feature
# 3. Update PR to point to new branch, or close old PR and open new one
```

**"Large dataset accidentally committed"**
```bash
# Remove from history (BEFORE others pull)
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch path/to/large-file' \
--prune-empty --tag-name-filter cat -- --all

# Force push to update remote
git push --force-with-lease origin main

# Prevention: improve .gitignore, teach about data/ directories
```

**"Squash and merge on GitHub"**
1. Open a pull request from your feature branch.  
2. After review and approval, click the green **Merge** button.  
3. Choose **“Squash and merge”**.  
4. Edit the commit message to something clear before confirming.  


## Common Student Scenarios

**"I forgot to pull before starting work"**
```bash
# If you haven't committed yet
git stash
git pull origin main
git stash pop

# If you've already committed
git pull --rebase origin main
```

**"My branch has conflicts with main"**
```bash
# During rebase, Git will show conflict markers like:
# <<<<<<< HEAD
# main branch code
# =======
# your branch code
# >>>>>>> your-commit

# Edit the file to resolve conflicts, then:
git add resolved-file.py
git rebase --continue
```

**"I need to update my PR after review"**
```bash
# Make your changes
git add .
git commit -m "Address review feedback"
git push origin your-feature-branch
# PR automatically updates
```
