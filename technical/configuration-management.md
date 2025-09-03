# Configuration Management

Proper configuration management keeps projects flexible, secure, and deployable across different environments. Students should separate configuration from code and validate settings at startup to catch issues early.

## Why manage configuration properly
- **Environment flexibility**: Same code runs in development, testing, and production with different settings
- **Security**: Keep secrets out of code and version control
- **Validation**: Catch configuration errors at startup, not during execution
- **Team coordination**: Clear documentation of required settings

## Basic patterns

**Configuration files vs environment variables**
- **Config files** (`config.yaml`, `config.json`): Good for complex nested settings, easier to version
- **Environment variables**: Required for secrets, deployment-specific values, container orchestration

**Hierarchy of configuration sources** (lower numbers override higher numbers):
1. Command-line arguments (highest priority)
2. Environment variables  
3. `.env` files
4. Configuration files
5. Default values in code (lowest priority)

## Environment variables and .env files

**Using .env files for development**
```bash
# .env file (never commit this)
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=sk-1234567890abcdef
DEBUG_MODE=true
MAX_WORKERS=4
```

**Loading with python-dotenv**
```python
import os
from dotenv import load_dotenv

# Load .env file in development
load_dotenv()

# Access variables
database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
debug = os.getenv("DEBUG_MODE", "false").lower() == "true"
```

**Always provide .env.example**
```bash
# .env.example (commit this as documentation)
DATABASE_URL=postgresql://localhost:5432/your_db_name
API_KEY=your_api_key_here
DEBUG_MODE=false
MAX_WORKERS=2
```

## Pydantic Settings for robust configuration

**Basic settings class**
```python
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class ProjectSettings(BaseSettings):
    """Application configuration loaded from environment variables and .env files."""
    
    # Database settings
    database_url: str = Field(..., description="Database connection string")
    
    # API settings  
    api_key: str = Field(..., description="External API key")
    api_timeout: int = Field(default=30, ge=1, le=300)
    
    # Processing settings
    max_workers: int = Field(default=2, ge=1, le=16)
    batch_size: int = Field(default=1000, ge=1)
    
    # File paths
    data_dir: Path = Field(default=Path("./data"))
    output_dir: Path = Field(default=Path("./outputs"))
    
    # Feature flags
    debug_mode: bool = Field(default=False)
    enable_caching: bool = Field(default=True)
    
    class Config:
        env_file = ".env"  # Automatically load from .env file
        env_file_encoding = "utf-8"
        case_sensitive = False  # DATABASE_URL or database_url both work

# Usage - validates on instantiation
settings = ProjectSettings()
```

**Environment-specific configuration**
```python
from typing import Literal

class ProjectSettings(BaseSettings):
    environment: Literal["development", "testing", "production"] = "development"
    database_url: str
    debug_mode: bool = False
    
    # Different validation rules per environment
    @validator('debug_mode', always=True)
    def debug_only_in_dev(cls, v, values):
        env = values.get('environment')
        if env == 'production' and v:
            raise ValueError("Debug mode not allowed in production")
        return v
    
    class Config:
        env_file = ".env"
        
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            # Load different .env files per environment
            env = init_settings.get('environment', 'development')
            return (
                init_settings,
                env_settings,
                PydanticSettingsSource(f".env.{env}"),  # .env.development, .env.production
                file_secret_settings,
            )

# Usage
settings = ProjectSettings(environment="production")
```

**Integration with data pipeline**
```python
class DataPipelineSettings(BaseSettings):
    """Settings for data processing pipeline."""
    
    # Input/output paths
    raw_data_path: Path = Field(..., description="Path to raw data files")
    processed_data_path: Path = Field(default=Path("./data/processed"))
    
    # Processing parameters
    min_sample_size: int = Field(default=100, ge=1)
    confidence_level: float = Field(default=0.95, ge=0.5, le=0.99)
    remove_outliers: bool = Field(default=True)
    outlier_threshold: float = Field(default=2.0, gt=0)
    
    # External services
    database_url: str = Field(..., description="Database connection string")
    redis_url: str = Field(default="redis://localhost:6379/0")
    
    # Validation
    @validator('raw_data_path')
    def data_path_exists(cls, v):
        if not v.exists():
            raise ValueError(f"Raw data path does not exist: {v}")
        return v
    
    @validator('processed_data_path')
    def create_output_dir(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        env_prefix = "PIPELINE_"  # Environment variables prefixed with PIPELINE_

# Usage with prefixed environment variables
# PIPELINE_RAW_DATA_PATH=/data/raw
# PIPELINE_MIN_SAMPLE_SIZE=50
settings = DataPipelineSettings()
```

## Docker integration

**Passing environment variables to containers**
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Don't set secrets in Dockerfile - pass at runtime
ENV ENVIRONMENT=production
```

**Using with docker-compose**
```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    env_file:
      - .env.production  # Load production settings
    environment:
      - ENVIRONMENT=production
      - DEBUG_MODE=false
    volumes:
      - ./data:/app/data:ro  # Mount data directory
```

**Make targets for different environments**
```makefile
# Makefile
.PHONY: run-dev run-prod

run-dev:
	docker run --rm -it \
		--env-file .env.development \
		-v $(PWD)/data:/app/data \
		myapp:latest

run-prod:
	docker run --rm -it \
		--env-file .env.production \
		-v /prod/data:/app/data:ro \
		myapp:latest
```

## Common patterns TAs should recognize

**1. Settings validation at startup**
```python
# ✅ Good: Validate configuration when app starts
def main():
    try:
        settings = ProjectSettings()
        logger.info(f"Loaded configuration for {settings.environment} environment")
    except ValidationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Continue with validated settings
    run_pipeline(settings)

if __name__ == "__main__":
    main()
```

**2. Environment-specific behavior**
```python
def setup_logging(settings: ProjectSettings):
    """Configure logging based on environment."""
    if settings.debug_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    if settings.environment == "production":
        # Add structured logging, error reporting, etc.
        pass
```


## What TAs should look for in code reviews

**✅ Good practices to encourage:**
- Settings loaded and validated at application startup
- Clear separation between code and configuration
- Documentation of required environment variables
- No hardcoded secrets or paths

**❌ Issues to flag:**
- Hardcoded configuration values in source code
- Secrets committed to version control
- Missing `.env.example` file
- Configuration loaded multiple times throughout code
- No validation of required settings

**Review questions to ask:**
- "What happens if a required environment variable is missing?"
- "How would a new team member know what configuration is needed?"
- "Are there any secrets that should be moved to environment variables?"

## Examples for coaching conversations

**Progression from basic to robust configuration:**

1. **Start with environment variables**
   ```python
   # Instead of hardcoding
   DATABASE_URL = "postgresql://localhost:5432/mydb"
   
   # Use environment variables
   DATABASE_URL = os.getenv("DATABASE_URL")
   ```

2. **Add validation and defaults**
   ```python
   DATABASE_URL = os.getenv("DATABASE_URL")
   if not DATABASE_URL:
       raise ValueError("DATABASE_URL environment variable is required")
   ```

3. **Use Pydantic Settings for structure**
   ```python
   class Settings(BaseSettings):
       database_url: str
       debug_mode: bool = False
       
   settings = Settings()  # Validates automatically
   ```

**Show how good configuration management prevents common issues** students encounter: broken deployments, leaked secrets, environment-specific bugs.