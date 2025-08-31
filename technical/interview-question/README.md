# Interview Exercise: 5-Minute Code Review

This exercise simulates what TAs will do with students in the Data Science Clinic:  
review real code, identify high-value improvements, and give constructive feedback.

---

## Task
- Skim the script [`bad_script.py`](./bad_script.py).  
- Propose **3–5 concrete suggestions** to improve correctness, clarity, or maintainability.  
- For each suggestion, briefly explain **what to change and why**.  
- Do not run the code or rewrite it in full — this is a **review exercise**.  
- Assume Python 3.10+ and `pandas` are available.  

Time limit: **5 minutes.**

---

## What We’re Looking For
High-value points (examples below — you don’t need all of them, just 3–5 solid picks):  
- Add a `__main__` guard so imports don’t execute I/O.  
- Replace `print` with `logging` at appropriate levels.  
- Avoid mutable default arguments (e.g., `groups=[]`).  
- Add type hints and docstrings for functions.  
- Separate computation from I/O (functions return values, wrappers handle file writes).  
- Don’t use broad `except Exception`; catch specific errors.  
- Avoid `inplace=True` and chained assignment pitfalls.  
- Validate required columns explicitly.  
- Pass file paths and parameters as arguments instead of globals.  
- Use `Pathlib` for file paths.  
- Write JSON with `DataFrame.to_json` instead of `json.dumps`.  

---

## Rubric (for graders)
- 1 point each for a correct, high-value observation with rationale.  
- Max: 5 points.  
- Extra credit: clear explanation of *why* the change matters.  

---

## Files
- [`bad_script.py`](./bad_script.py) — intentionally flawed version.  
- [`reference_solution.py`](./reference_solution.py) — revised version illustrating best practices.  
