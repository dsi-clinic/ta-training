FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv with lock file
RUN uv sync --frozen --no-dev

# Copy source code
COPY . .

# Default command
CMD ["uv", "run", "python", "app.py"]