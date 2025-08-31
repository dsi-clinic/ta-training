# Code Review

## Goals
- Improve correctness, clarity, maintainability.
- Share context and teach best practices.

## Process
- Small PRs (200–400 lines changed is a soft ceiling).
- Author checklist before request: tests pass, self-review, docs updated.
- Reviewer checklist: see below.

## Reviewer checklist
- Scope: Does the change do one thing?
- API: Clear function names, types, docstrings.
- Data correctness: validates inputs, handles edge cases.
- I/O separation: computation vs file/network operations.
- Tests: cover happy path and at least one edge case.
- Style: logging, no commented-out code, no secrets, no `print`.
- Performance: obvious quadratic patterns in large data?
- Reproducibility: Make targets/Docker updated if needed.

## Commenting style
- Be specific, actionable, and kind.
- Prefer suggestions with rationale and small examples.

## Examples
- Good PR review comments vs unhelpful comments.
