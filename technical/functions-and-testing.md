# Functions and Testing

## Return values over side effects
- Pure functions facilitate testing and reuse.
- Functions should return results; thin wrappers handle file I/O.

## `__main__` guard
- Prevent code from executing on import.
- CLI entry-point can parse args and call library functions.

## Testing
- Use `pytest` with small, focused tests.
- Arrange-Act-Assert pattern; fixtures for test data.
- Avoid `inplace=True` and chained assignment pitfalls; prefer `.copy()` and explicit returns.

## Minimal examples
- A `clean(df)` function: required columns check, no `inplace`, returns new DataFrame.
- A test that asserts behavior on missing columns, NaNs, and negative values.

## Debugging
- Prefer `logger.debug()` over ad-hoc prints.
- Reproduce bugs with a small failing test.
