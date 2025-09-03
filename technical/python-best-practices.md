# Python Best Practices

Common Python pitfalls and patterns that TAs should watch for in student code. These are language-specific issues that can cause subtle bugs or make code harder to maintain.

---

## Mutable default arguments

**❌ The classic Python trap**
```python
def add_item(item, target_list=[]):
    """Add item to a list - BROKEN!"""
    target_list.append(item)
    return target_list

# This breaks because the same list is reused across calls
items1 = add_item("apple")     # ["apple"]
items2 = add_item("banana")    # ["apple", "banana"] - Oops!
```

**✅ Use None as default, create new objects inside function**
```python
def add_item(item, target_list=None):
    """Add item to a list."""
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list

# Alternative: use copy if you want to modify an existing list
def add_item(item, target_list=None):
    if target_list is None:
        target_list = []
    else:
        target_list = target_list.copy()  # Don't modify caller's list
    target_list.append(item)
    return target_list
```

---

## Variable scoping and closures

**❌ Late binding closures**
```python
# This doesn't work as expected
functions = []
for i in range(3):
    functions.append(lambda: print(i))

# All functions print 2 (the final value of i)
for func in functions:
    func()  # Prints: 2, 2, 2
```

**✅ Capture variables explicitly**
```python
functions = []
for i in range(3):
    functions.append(lambda x=i: print(x))  # Capture i's current value

# Now each function prints its expected value
for func in functions:
    func()  # Prints: 0, 1, 2
```

**Variable shadowing in comprehensions**
```python
# ❌ Can be confusing
items = ["a", "b", "c"]
result = [item.upper() for item in items if len(item) > 0]
# What's the value of 'item' here? Undefined behavior

# ✅ Use different variable names to avoid confusion
items = ["a", "b", "c"]  
result = [x.upper() for x in items if len(x) > 0]
# 'items' is still clearly the original list
```

---

## Import patterns

**✅ Good import practices**
```python
# Standard library first, then third-party, then local
import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np

from your_package.utils import helper_function
```

**❌ Common import mistakes**
```python
# Avoid star imports - makes it unclear where things come from
from pandas import *  # What functions are available? 

# Avoid importing inside functions unless necessary
def process_data():
    import pandas as pd  # Usually should be at module level
    return pd.DataFrame()

# Don't override builtin names
import json as json  # Shadows built-in json if it existed
from datetime import datetime as datetime  # Confusing
```

**Relative imports in packages**
```python
# In a package structure:
# my_package/
#   __init__.py
#   analysis.py
#   utils.py

# In analysis.py:
from .utils import helper_function  # ✅ Explicit relative import
from my_package.utils import helper_function  # ✅ Also fine

# Avoid
import utils  # ❌ Might not find the right module
```

---

## Error handling patterns

**✅ Specific exception handling**
```python
def load_config(path: str) -> dict:
    """Load configuration file with specific error handling."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Config file not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config file: {e}")
    # Don't catch Exception - too broad
```

**❌ Common error handling mistakes**
```python
# Too broad exception catching
try:
    result = risky_operation()
except:  # ❌ Catches everything, including KeyboardInterrupt
    print("Something went wrong")

# Silencing errors
try:
    result = risky_operation()
except Exception:
    pass  # ❌ Error disappears, hard to debug

# Not re-raising when you should
try:
    result = risky_operation()
except ValueError:
    print("Error occurred")  # ❌ Should probably re-raise
    return None
```

**EAFP vs LBYL (Easier to Ask Forgiveness vs Look Before You Leap)**
```python
# ✅ Pythonic: EAFP
try:
    value = my_dict[key]
except KeyError:
    value = default_value

# Less Pythonic: LBYL
if key in my_dict:
    value = my_dict[key]
else:
    value = default_value
```

---

## String and collection patterns

**String building**
```python
# ❌ Inefficient for many concatenations
result = ""
for item in large_list:
    result += str(item) + ", "

# ✅ Use join for multiple concatenations
result = ", ".join(str(item) for item in large_list)

# ✅ Use f-strings for formatting
name = "Alice"
age = 30
message = f"Hello {name}, you are {age} years old"  # Clear and fast
```

**Dictionary and list operations**
```python
# ✅ Use dict.get() with defaults
value = config.get("timeout", 30)  # Returns 30 if "timeout" not in config

# ✅ Use collections.defaultdict for accumulating
from collections import defaultdict
counts = defaultdict(int)
for item in items:
    counts[item] += 1  # No need to check if key exists

# ✅ Use enumerate when you need both index and value
for i, item in enumerate(items):
    print(f"{i}: {item}")

# ❌ Don't do this
for i in range(len(items)):
    item = items[i]
    print(f"{i}: {item}")
```

---

## Memory and performance awareness

**Generator expressions vs list comprehensions**
```python
# ✅ Use generators for large datasets
def process_large_file(filename):
    # Generator - memory efficient
    lines = (line.strip() for line in open(filename))
    return sum(1 for line in lines if line.startswith("ERROR"))

# ❌ List comprehension loads everything into memory
def process_large_file_bad(filename):
    lines = [line.strip() for line in open(filename)]  # Could be huge!
    return sum(1 for line in lines if line.startswith("ERROR"))
```

**Avoid repeated expensive operations**
```python
# ❌ Repeated computation in loop
for item in items:
    if expensive_function() > threshold:  # Called every iteration!
        process(item)

# ✅ Compute once
expensive_result = expensive_function()
for item in items:
    if expensive_result > threshold:
        process(item)
```

---

## Context managers and resource handling

**✅ Always use context managers for resources**
```python
# File handling
with open("data.txt") as f:
    content = f.read()
# File automatically closed

# Database connections
with get_database_connection() as conn:
    result = conn.execute(query)
# Connection automatically closed
```

**Custom context managers when needed**
```python
from contextlib import contextmanager
import time

@contextmanager
def timer(description):
    """Time a block of code."""
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{description} took {elapsed:.2f} seconds")

# Usage
with timer("Data processing"):
    process_large_dataset()
```

---

## What TAs should look for in code reviews

**✅ Good practices to encourage:**
- Functions with `None` defaults instead of mutable defaults
- Specific exception handling with meaningful error messages  
- Proper resource management with context managers
- Clear variable names that don't shadow built-ins
- Generator expressions for large datasets

**❌ Common issues to flag:**
- Mutable default arguments (`def func(items=[]):`)
- Bare `except:` clauses that catch everything
- Building strings with `+=` in loops
- Importing inside functions without reason
- Variables that shadow built-in names (`list = [1,2,3]`)

**Review questions to ask:**
- "What happens if this function is called multiple times with the default argument?"
- "What specific errors are you expecting here, and how should they be handled?"
- "Could this operation be more memory-efficient with a generator?"
- "Are you sure you want to catch all exceptions here?"

---

## Examples for coaching conversations

**Progression from problematic to Pythonic:**

1. **Start with the bug demo**
   ```python
   # Show them the mutable default argument problem
   def broken_function(items=[]):
       items.append("new")
       return items
   
   print(broken_function())  # ["new"]
   print(broken_function())  # ["new", "new"] - Surprise!
   ```

2. **Show the fix and explain why**
   ```python
   def fixed_function(items=None):
       if items is None:
           items = []
       items.append("new") 
       return items
   ```

3. **Connect to data science context**
   ```python
   # This pattern shows up in data processing
   def add_features(df, new_columns=None):
       if new_columns is None:
           new_columns = []
       # Now safe to modify new_columns
   ```

**Teaching approach:**
- Start with code that breaks in surprising ways
- Show the fix and explain the Python language reason
- Connect to their data science work context
- Emphasize that these are "Python gotchas" that even experienced developers hit