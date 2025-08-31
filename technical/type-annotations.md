# Type Annotations

## Why annotate
- Clarifies APIs for reviewers and future maintainers.
- Catches common bugs with static checkers.

## Basics
- Function signatures: parameter types and return types.
- Use `Optional[T]`, `Iterable[T]`, `Mapping[K, V]` where appropriate.
- Prefer `pathlib.Path` to raw strings for file paths.

## Data science specifics
- `pandas` DataFrame in/out: `pd.DataFrame` and `pd.Series`.
- For column schemas, consider `typing.TypedDict` or docstring tables.
- Avoid over-specifying types when they obscure readability.

## Tooling
- mypy/pyright optional; start with ruff’s typing checks.
- Keep annotation debt low: annotate public functions first.

## Examples
- Before/after examples of a data cleaning function with annotations.
