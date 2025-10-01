# Debugging and Testing

Disciplined debugging and lightweight testing keep projects reliable. Debugging practices make errors reproducible and easier to fix. Simple tests ensure that fixes hold and that changes don't silently break core functionality. Students are not formally required to write tests, but modeling these practices sets a strong example.

## Debugging
- **Reproduce bugs with a minimal example**  
  Shrink the input until the error can be triggered consistently.  

- **Pause execution with `pdb`**  
  ```python
  import pdb
  pdb.set_trace()
  ```
  Step through code interactively and inspect state at runtime.
- **Prefer logging over prints**
    ```python
      import logging
      logging.basicConfig(level=logging.DEBUG)
      logger = logging.getLogger(__name__)    
      logger.debug("DataFrame shape before clean: %s", df.shape)
    ```
    Logging can be filtered by severity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) and scales better than ad-hoc prints.

## Testing with Arrange-Act-Assert

The **Arrange-Act-Assert** pattern provides a clear structure for tests:
1. **Arrange**: Set up test data and preconditions
2. **Act**: Call the function being tested
3. **Assert**: Verify the expected behavior

While professional teams often use `pytest`, simple assertions are usually sufficient and more accessible for students learning testing fundamentals.

## Minimal examples
**Test simple DataFrame behavior**
```python
import pandas as pd
from your_module import clean

# ARRANGE: Set up test data with negative scores
input_df = pd.DataFrame({
    'first_name': ['Alice', 'Bob'],
    'last_name': ['Smith', 'Jones'], 
    'score': [85, -10],
    'group': ['A', 'B']
})

# ACT: Call the function being tested
result = clean(input_df)

# ASSERT: Verify the expected behavior
assert len(result) == 1, f"Expected 1 row, got {len(result)}"
assert result.iloc[0]['first_name'] == 'Alice', "Wrong row kept"
assert all(result['score'] >= 0), "Negative scores not removed"

print("✓ Test passed: Negative scores removed correctly")
```

**Test error handling**
```python
# ARRANGE: Set up data missing required columns
input_df = pd.DataFrame({
    'first_name': ['Alice'],
    'last_name': ['Smith']
    # Missing 'score' and 'group' columns
})

# ACT & ASSERT: Verify exception is raised
try:
    clean(input_df)
    assert False, "Should have raised ValueError for missing columns"
except ValueError as e:
    assert "Missing columns" in str(e), f"Unexpected error message: {e}"
    print("✓ Test passed: Missing columns detected")
```

**Note**: For more advanced testing needs, `pytest` provides additional features like fixtures, parametrization, and better output formatting. But simple assertions are a great starting point and often sufficient for student projects.