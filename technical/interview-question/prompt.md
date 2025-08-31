# TA Interview Question: Code Review

**Instructions**  
You have 5 minutes. Skim the Python file [`bad_script.py`](./bad_script.py).  
Give 3–5 concrete suggestions for improving correctness, clarity, or maintainability.  
Briefly explain each suggestion. No need to rewrite the code or run it.

**Assumptions**  
- Python 3.10+ and pandas are available.  
- You’re reviewing like you would for a student in the Clinic.  

**Deliverable**  
- A short list of 3–5 suggested changes, each with a rationale.  

**Example output**  
- “Move the quick run block under a `__main__` guard so importing doesn’t trigger I/O.”  
- “Replace `print` with `logging` so messages can be configured by level.”  
- “Avoid `groups=[]` as a default — use `None` to prevent shared state across calls.”  
