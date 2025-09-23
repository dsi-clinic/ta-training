# Code Review

## Goals
- Improve correctness, clarity, maintainability.
- Share context and teach best practices.
- Build professional data science habits that students will use throughout their careers.

## Process
- Small PRs (200–400 lines changed is a soft ceiling).
- Author checklist before request: tests pass, self-review, docs updated.
- Reviewer checklist: see below.

## Core Review Principles

### Enforce, Don't Code
- Guide students to solutions rather than fixing code yourself
- Ask guiding questions: "What happens if a teammate tries to run this?"
- Help students discover problems themselves for deeper understanding

### Be Specific and Educational
- Replace "this is wrong" with "this function needs type hints - what does it return?"
- Explain the "why" behind requests
- Reference specific handbook sections when applicable

### Progress Over Perfection
- Prioritize critical issues first (reproducibility, security)
- Address style and organization in follow-up reviews
- Celebrate improvements and good practices you see

## Reviewer Checklist

### Scope and Structure
- **Scope:** Does the change do one thing?
- **API:** Clear function names, types, docstrings.
- **Giant files:** Flag scripts over 500 lines for refactoring
- **Function clarity:** Avoid unclear names like `process()`, `calc()`

### Data and Error Handling
- **Data correctness:** Validates inputs, handles edge cases.
- **Error messages:** Specific, actionable messages vs. generic exceptions
- **Missing columns:** Check for proper validation of required data fields

### Code Organization
- **I/O separation:** Computation vs file/network operations separated
- **Pure functions:** Logic that can be tested independently
- **Mixed responsibilities:** Functions that both read files AND do computation

### Dependencies and Environment
- **Reproducibility:** Docker builds work, `uv.lock` committed when `pyproject.toml` updated
- **Dependencies:** Check `pyproject.toml` has pinned versions
- **Environment setup:** Clear setup instructions in README

### Security and Configuration
- **Secrets:** No API keys, passwords, or tokens in code
- **Hardcoded paths:** No `/Users/alice/project/data.csv` style paths
- **Configuration:** Use `.env` files with `.env.example` committed
- **Pydantic settings:** Centralized, validated configuration management

### Code Quality
- **Type hints:** Present on public functions and unclear parameters
- **Logging:** Use logging instead of print statements
- **Documentation:** Docstrings explain purpose and return values

### Style and Professional Practices
- **No commented-out code:** Remove dead code
- **Python best practices:** Watch for mutable default arguments, variable scope issues
- **Git workflow:** Feature branches, proper commit messages, rebased with main

## Common Review Scenarios

### What to Look For
- **Hardcoded paths:** `/Users/alice/project/data.csv`
- **Missing error handling:** Files that might not exist
- **Unclear function names:** `process()`, `calc()`
- **Giant files:** 500+ lines in one script
- **No type hints:** Unclear parameter expectations
- **Secrets in code:** API keys, passwords
- **Print statements:** Instead of proper logging
- **Mixed I/O and computation:** Functions doing too many things

### How to Give Feedback

#### Ask Questions
- "What happens if this file doesn't exist?"
- "How would a teammate run this code?"
- "What if someone tries to run this on a different machine?"

#### Suggest Alternatives
- "Could we use `pathlib.Path` here instead of string paths?"
- "Consider extracting the file reading into a separate function"
- "Would a Pydantic model help validate this configuration?"

#### Explain Benefits
- "Type hints help teammates understand your code"
- "Logging can be controlled and filtered appropriately"
- "Separating I/O makes this function much easier to test"


#### Celebrate Improvements
- "Great job adding docstrings!"
- "Nice use of type hints here"
- "This error message will be really helpful for debugging"

## Sample Review Comments

### Poor Feedback
- "This is wrong"
- "Fix the Docker setup"
- "Fix your config"

### Effective Feedback
- "I notice this hardcoded path might break on other machines."
- "Could we use a relative path instead?"
- "I see some hardcoded values that might cause issues."


## The Review Feedback Loop

### Student Code → TA Review → Student Revision → Final Approval

#### Keys to Effective Feedback
- **Specific:** "Add type hints to this function" not "improve code quality"
- **Actionable:** Suggest concrete next steps
- **Educational:** Explain the "why" behind requests
- **Encouraging:** Acknowledge good practices you see

#### Managing the Process
- Very few PRs should be approved on first review - iteration is normal and healthy
- Make each iteration productive with clear, actionable feedback
- Focus on teaching principles, not just fixing immediate issues
- Build confidence through incremental improvement

## Priority Framework

### Critical (Must Fix)
1. **Security issues:** Committed secrets, exposed credentials
2. **Reproducibility blockers:** Missing Docker files, hardcoded paths
3. **Data correctness:** Missing validation, improper error handling

### Important (Address Soon)
1. **I/O separation:** Mixed computation and file operations
2. **Type hints:** On public functions and unclear parameters
3. **Configuration management:** Hardcoded values, missing .env.example

### Nice to Have (Follow-up)
1. **Documentation:** Docstrings and README improvements
2. **Code organization:** Function names, file structure
3. **Performance:** Obvious inefficiencies in large data processing

## Technical Focus Areas

### Python Best Practices
- Watch for mutable default arguments: `def func(items=[])`
- Variable scope issues with closures
- Proper exception handling with specific error messages

### Data Validation & Types
- Pydantic models for configuration and API data
- Type hints on functions with unclear parameters
- Input validation for data processing functions

### Environment & Dependencies
- `pyproject.toml` with pinned dependencies
- `uv.lock` file committed for reproducible builds
- Docker setup that actually works: `make build && make test`

### Configuration Management
- Pydantic settings classes instead of scattered env vars
- `.env.example` file showing required variables
- No secrets committed to repository

## When to Escalate

### Immediate Escalation
- **Security issues:** Committed secrets, exposed credentials
- **Plagiarism concerns:** Suspicious code similarities
- **Scope creep:** Project requirements changing significantly

### Pattern-Based Escalation
- **Repeated issues:** Same problems across multiple teams
- **Systematic gaps:** Everyone struggling with the same concept
- **Resource constraints:** Students need tools/access they don't have

### Effective Escalation
- Document with screenshots, links, specific examples
- Suggest solutions, don't just raise problems
- Note broader impact: how many students/teams affected?
- Indicate timeline urgency

## Examples and Practice

### Practice Exercise
Review this function and identify issues:

```python
def process_survey_data():
    data = pd.read_csv('/Users/alice/Documents/clinic/survey_data.csv')
    
    print("Data loaded successfully!")
    
    # Remove invalid responses
    clean_data = data[data['satisfaction_score'] > 0]
    
    # Calculate statistics  
    avg = clean_data['satisfaction_score'].mean()
    dept_stats = clean_data.groupby('department')['satisfaction_score'].mean()
    
    # Save results
    results = {'overall_avg': avg, 'dept_averages': dept_stats.to_dict()}
    
    with open('analysis_results.json', 'w') as f:
        json.dump(results, f)
    
    print(f"Analysis complete! Average satisfaction: {avg}")
    return results
```

### Discussion Questions
- What specific issues do you see?
- How would you prioritize your feedback?
- What questions would you ask the student?
- How could this code be improved incrementally?

## Remember: Building Professional Data Scientists

Every code review, every standard enforced, every coaching conversation shapes how students will approach data science throughout their careers. The habits they learn here will serve them for years to come.

Focus on developing student capabilities, not just delivering perfect code. Your role is to guide, teach, and model professional practices that will make students better collaborators and contributors in their future careers.