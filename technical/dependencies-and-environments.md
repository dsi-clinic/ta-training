# Dependencies and Environments

All code should run inside the provided Docker or cluster environment. Avoid creating ad-hoc virtual environments or installing packages directly on your laptop — this breaks reproducibility and makes debugging harder.

Inside Docker, we use **[uv](https://github.com/astral-sh/uv)** to manage dependencies. `uv` is a fast, modern Python package manager and resolver. It installs packages much quicker than pip, respects `requirements.txt`, and works seamlessly inside containers. It also supports locking dependencies for consistent builds across machines.

## Python dependencies
- List all required packages in `requirements.txt`.  
- **Pin versions** (e.g., `pandas==2.2.2`) to avoid “works on my machine” issues.  
- Keep the file minimal — only include packages the project actually needs.  

## Installing deps
- To add a dependency:
  1. Add it to `requirements.txt`.  
  2. Rebuild the Docker image:  
     ```bash
     make build
     ```
- Never run `pip install` or `uv pip install` inside notebooks or ad-hoc environments.  
- Document non-standard libraries in the repo’s README so reviewers understand why they’re included.  

## Cluster environments
- Some projects require running on the DSI cluster.  
- For cluster jobs, include a **conda or micromamba environment file** (`environment.yml`).  
- Keep the cluster recipe in sync with `requirements.txt` to avoid divergence.  

## Environment variables
- Use a `.env` file to manage configuration values and secrets (API keys, tokens, database URLs).  
- Never hardcode secrets in code or commit them to the repo.  
- Add a `.env.example` file showing variable names (but not actual values), e.g.:
  ```
  DB_USER=your_username
  DB_PASS=your_password
  API_KEY=replace_me
  ```
- Document how to load the `.env` in the project README (e.g., with `python-dotenv` or by passing `--env-file` to Docker).  
