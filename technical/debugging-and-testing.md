# Debugging and Testing

Disciplined debugging and lightweight testing keep projects reliable. Debugging practices make errors reproducible and easier to fix. A small test suite ensures that fixes hold and that changes don’t silently break core functionality. Students are not formally required to write tests, but modeling these practices sets a strong example.

---

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

## Testing
- **Arrange–Act–Assert pattern**  
  Structure tests clearly: set up input, call the function, assert results.

- **Use `pytest`**  
  Keep tests short and focused. Use fixtures for common data. Run with `pytest -q` to get concise output.

## Minimal examples
**Test simple DataFrame behavior**
```python
import pytest
import pandas as pd
from your_module import clean

def test_clean_removes_negative_scores():
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
    assert len(result) == 1  # Negative score row should be removed
    assert result.iloc[0]['first_name'] == 'Alice'
    assert all(result['score'] >= 0)

def test_clean_raises_error_on_missing_columns():
    # ARRANGE: Set up data missing required columns
    input_df = pd.DataFrame({
        'first_name': ['Alice'],
        'last_name': ['Smith']
        # Missing 'score' and 'group' columns
    })
    
    # ACT & ASSERT: Verify exception is raised
    with pytest.raises(ValueError, match="Missing columns"):
        clean(input_df)
```

**Test that a file exists**

```python
def test_output_file_written(tmp_path):
    # Arrange
    out_file = tmp_path / "results.txt"
    # Act
    out_file.write_text("hello")
    # Assert
    assert out_file.exists()
    assert out_file.read_text() == "hello"
```
