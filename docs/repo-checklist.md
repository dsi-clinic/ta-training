# Repository Evaluation Checklist

This document provides the checklist and rubric TAs must use when evaluating repositories at the end of the quarter.  
It is based on the Data Science Clinic coding standards and the final cleanup/technical review requirements.  

The primary goal is to ensure repositories are **clean, reproducible, and easy for the next person to work on.**

## Grading Information
- **Project Name:**  
- **TA Name:**  
- **Repo URL:**  
- **Files Graded (3 total, full paths):**  
  - File 1:  
  - File 2:  
  - File 3:  

## General Repo Hygiene
- [ ] All work merged to `main` (or `dev`) branch; other branches deleted.  
- [ ] No extraneous files (`.DS_Store`, `.ipynb_checkpoints`, temp files).  
- [ ] `.gitignore` used properly; no large data files or intermediate outputs tracked.  
- [ ] No secrets or API keys committed.  

## Documentation
- [ ] Main `README.md` includes:  
  - [ ] Instructions on how to run the code (ideally via Docker/Make).  
  - [ ] Description of project purpose and deliverables.  
  - [ ] Contributor names.  
- [ ] Source and description of all datasets clearly provided.  
- [ ] Descriptions of all files and their purpose.  
- [ ] Environment specification included (Dockerfile, requirements.txt, Makefile, or conda/micromamba recipe).  
- [ ] Boilerplate text removed; documentation is clear and free of grammar errors.  

## Code Grading (per file)
TAs must select **three files** edited during the quarter (at least one notebook if present).  
For each file, copy the section below and complete it.

### File: `path/to/file.py`
- [ ] File name is appropriate and descriptive.  

**If script (`.py`):**  
- [ ] All code organized into functions (no top-level execution).  
- [ ] All functions include docstrings.  
- [ ] Function names are descriptive and meaningful.  
- [ ] Code passes `ruff` or `pre-commit run --all-files`.  
- [ ] All paths are relative (no hard-coded absolute paths).  
- [ ] No commented-out code blocks.  
- [ ] Code is free of secrets or API keys.  

**If notebook (`.ipynb`):**  
- [ ] Fewer than 20 cells total.  
- [ ] Each cell under 10 lines of code.  
- [ ] No `!pip install` or other environment management in notebook.  
- [ ] No function/class definitions (should be in helper `.py` files).  
- [ ] No commented-out code blocks.  
- [ ] Code is free of secrets or API keys.  
- [ ] Notebook includes markdown documentation explaining purpose and context.  

## Additional Standards (Repo-Wide)
- [ ] Directory structure is clear and logical.  
- [ ] File and folder names avoid dates, personal names, or versions (e.g., `final_v2.py`).  
- [ ] Bash scripts (if any) are executable, end with `.sh`, and include `#!/bin/bash` and `set -e`.  
- [ ] A Dockerfile is present and functional; code can be run in Docker.  
- [ ] Dependency versions pinned in `requirements.txt`.  
- [ ] Working branches kept up-to-date with `main`.  

## Summary
- Strengths of this repo:  
- Weaknesses / areas for improvement:  

## TA Final Notes
Please submit the completed checklist along with your repo evaluation notes to the clinic director.  
If a repository fails to meet a requirement, provide a short explanation and escalate major issues.  
