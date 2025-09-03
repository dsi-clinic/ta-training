# Technical Handbook

This section documents the **technical standards, workflows, and review practices** that TAs and mentors are expected to enforce in the Data Science Clinic.

## Purpose
- Provide TAs and mentors with a reference for **evaluating and reinforcing best practices**.  
- Support consistency in **repo hygiene, code review, and reproducibility** across projects.  
- Equip TAs to give **actionable, constructive feedback** on technical issues.  

## Contents

- [Python Best Practices](./python-best-practices.md)  
  Common Python pitfalls and language-specific patterns TAs should watch for: mutable defaults, scoping issues, error handling.

- [Code Style and Structure](./code-style-and-structure.md)  
  Guidelines for organizing code, naming conventions, documentation standards, and professional presentation.

- [Data Validation and Types](./data-validation-and-types.md)  
  Type annotations and Pydantic validation patterns for ensuring data quality and code clarity.

- [Configuration Management](./configuration-management.md)  
  Managing settings, secrets, and environment-specific configuration with Pydantic Settings.

- [Debugging and Testing](./debugging-and-testing.md)  
  Disciplined debugging practices and lightweight testing approaches for data science projects.

- [Code Review](./code-review.md)  
  Guidelines for TAs when reviewing pull requests and student repos.

- [GitHub Repo Management](./github-repo-management.md)  
  Branching strategies, PR workflows, and common scenarios TAs encounter with student repositories.

- [Docker and Make](./docker-and-make.md)  
  Container setup patterns and Make targets for reproducible data science workflows.

- [Dependencies and Environments](./dependencies-and-environments.md)  
  Managing Python dependencies, Docker environments, and reproducible setups.

- [Paths and I/O in Containers](./paths-and-io-in-containers.md)  
  Path handling in Docker environments and separating I/O operations from computation logic.

- [Interview Exercise](./interview-question/README.md)  
  Code review prompt used in TA interviews and training.

- [Examples](./examples/)  
  Small runnable setups for TAs to practice before working with students.

## How to Use This Section
- Use these documents when preparing to **review student repos or pull requests**.  
- Refer back when you need **talking points for TA sessions** (e.g., how to coach Docker, paths, or PR reviews).  
- In final repo reviews, use these standards to **grade consistently** with the repo checklist.

## Key Principles
- **Enforce, don't code**: TAs guide students to solve issues, not fix repos themselves.  
- **Consistency**: Apply the same standards across projects so grading is fair.  
- **Professionalism**: Model how real data science teams work.  
- **Escalation**: Raise systemic or recurring issues with mentors and the Clinic Director.