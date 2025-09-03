# Paths and I/O in Containers

Container environments change how file paths work, and mixing I/O with computation makes code harder to test and reuse. Students should write path-agnostic code and separate data loading/saving from analysis logic.

## Why this matters
- **Portability**: Code works the same locally and in containers
- **Testability**: Pure functions are easier to test than ones that read/write files
- **Collaboration**: Teammates can run code without path issues
- **Debugging**: Easier to isolate problems when I/O is separated from logic

## Path patterns in containers

**The fundamental issue**
```python
# ❌ Breaks in containers - assumes specific host layout
df = pd.read_csv("/Users/student/project/data/survey.csv")

# ❌ Fragile - depends on current working directory
df = pd.read_csv("data/survey.csv")  # Where is "data" exactly?

# ✅ Robust - relative to code location
from pathlib import Path
script_dir = Path(__file__).parent
df = pd.read_csv(script_dir / "data" / "survey.csv")
```

**Project root helper pattern**
```python
from pathlib import Path

def get_project_root() -> Path:
    """Get the project root directory (where Dockerfile/Makefile live)."""
    return Path(__file__).resolve().parents[1]  # Adjust number for your structure

# Usage throughout your project
PROJECT_ROOT = get_project_root()
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

def load_survey_data() -> pd.DataFrame:
    """Load survey data from the standard location."""
    return pd.read_csv(DATA_DIR / "raw" / "survey.csv")
```

**Environment-aware paths**
```python
from pydantic_settings import BaseSettings

class PathSettings(BaseSettings):
    data_dir: Path = Field(default=Path("./data"))
    output_dir: Path = Field(default=Path("./outputs"))
    
    class Config:
        env_prefix = "APP_"  # APP_DATA_DIR, APP_OUTPUT_DIR

settings = PathSettings()
```

## Docker container setup

**Key principles for container paths:**
- Always set `WORKDIR` in Dockerfile
- Use matching `-w /app` in docker run commands
- Mount volumes to predictable locations
- Make data directory read-only (`:ro`) in production

## Separating I/O from computation

**❌ Bad: I/O mixed with computation**
```python
def analyze_survey_data():
    """Analyze survey data and save results."""
    # I/O mixed with computation - hard to test
    df = pd.read_csv("data/survey.csv")
    
    # Analysis logic
    avg_score = df['satisfaction'].mean()
    group_stats = df.groupby('department')['satisfaction'].agg(['mean', 'std'])
    
    # More I/O mixed in
    results = {
        'overall_average': avg_score,
        'by_department': group_stats.to_dict()
    }
    
    with open("outputs/results.json", "w") as f:
        json.dump(results, f)
    
    print(f"Analysis complete. Average satisfaction: {avg_score}")
```

**✅ Good: I/O separated from computation**
```python
def calculate_satisfaction_stats(df: pd.DataFrame) -> dict[str, Any]:
    """Calculate satisfaction statistics from survey data.
    
    Pure function - no I/O, easy to test.
    """
    avg_score = df['satisfaction'].mean()
    group_stats = df.groupby('department')['satisfaction'].agg(['mean', 'std'])
    
    return {
        'overall_average': avg_score,
        'by_department': group_stats.to_dict()
    }

def load_survey_data(data_path: Path) -> pd.DataFrame:
    """Load and validate survey data."""
    df = pd.read_csv(data_path)
    
    # Basic validation
    required_cols = ['satisfaction', 'department']
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    return df

def save_results(results: dict[str, Any], output_path: Path) -> None:
    """Save analysis results to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

# Main script coordinates I/O and computation
def main():
    """Main analysis pipeline."""
    # I/O layer
    data_path = DATA_DIR / "raw" / "survey.csv"
    output_path = OUTPUT_DIR / "satisfaction_analysis.json"
    
    df = load_survey_data(data_path)
    
    # Pure computation
    results = calculate_satisfaction_stats(df)
    
    # I/O layer
    save_results(results, output_path)
    
    # User feedback
    avg_score = results['overall_average']
    print(f"Analysis complete. Average satisfaction: {avg_score:.2f}")

if __name__ == "__main__":
    main()
```

**Testing the separated functions**
```python
import pytest
import pandas as pd
from your_package.analysis import calculate_satisfaction_stats

def test_satisfaction_stats():
    # Arrange: Create test data (no files needed!)
    test_df = pd.DataFrame({
        'satisfaction': [4, 5, 3, 4, 5],
        'department': ['Engineering', 'Engineering', 'Sales', 'Sales', 'Marketing']
    })
    
    # Act: Call pure function
    results = calculate_satisfaction_stats(test_df)
    
    # Assert: Check results
    assert results['overall_average'] == 4.2
    assert 'Engineering' in results['by_department']
    assert results['by_department']['Engineering']['mean'] == 4.5
```

## CLI patterns for flexible I/O

**Configurable paths via command line**
```python
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Survey data analysis")
    parser.add_argument(
        "--data-dir", 
        type=Path, 
        default=Path("./data"),
        help="Directory containing input data"
    )
    parser.add_argument(
        "--output-dir", 
        type=Path, 
        default=Path("./outputs"),
        help="Directory for output files"
    )
    parser.add_argument(
        "--survey-file", 
        type=str, 
        default="survey.csv",
        help="Survey data filename"
    )
    
    args = parser.parse_args()
    
    # Build paths from arguments
    data_path = args.data_dir / args.survey_file
    output_path = args.output_dir / "analysis_results.json"
    
    # Run analysis with specified paths
    run_analysis(data_path, output_path)

# Usage in different environments:
# Local: python -m analysis --data-dir ./local_data
# Container: python -m analysis --data-dir /mounted/data
```

**Using with Make targets**
```makefile
# Development with local data
run-local:
	python -m your_package.main --data-dir ./data/dev

# Container with mounted production data  
run-prod:
	docker run --rm -it \
		-v /prod/data:/data:ro \
		-v $(PWD)/outputs:/outputs \
		$(IMAGE_NAME) \
		python -m your_package.main --data-dir /data --output-dir /outputs
```

## Common patterns TAs should recognize

**1. Configuration-driven paths**
```python
# ✅ Good: Paths come from configuration with validation
from pydantic import BaseModel, Field, validator
from pathlib import Path

class AnalysisConfig(BaseModel):
    """Configuration for analysis pipeline with path validation."""
    
    data_dir: Path = Field(..., description="Directory containing input data")
    output_dir: Path = Field(default=Path("./outputs"))
    survey_filename: str = Field(default="survey.csv", min_length=1)
    
    @validator('data_dir')
    def data_dir_must_exist(cls, v):
        if not v.exists():
            raise ValueError(f"Data directory does not exist: {v}")
        return v
    
    @validator('output_dir')
    def create_output_dir(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    @property
    def survey_path(self) -> Path:
        return self.data_dir / self.survey_filename
    
    @property 
    def results_path(self) -> Path:
        return self.output_dir / "results.json"

def run_analysis(config: AnalysisConfig):
    df = load_survey_data(config.survey_path)
    results = calculate_stats(df)
    save_results(results, config.results_path)
```

**2. Path validation and error handling**
```python
def load_data_safely(data_path: Path) -> pd.DataFrame:
    """Load data with clear error messages."""
    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path}\n"
            f"Expected location: {data_path.absolute()}\n"
            f"Working directory: {Path.cwd()}"
        )
    
    if not data_path.is_file():
        raise ValueError(f"Path exists but is not a file: {data_path}")
    
    return pd.read_csv(data_path)
```

**3. Output directory management**
```python
def ensure_output_dir(output_path: Path) -> Path:
    """Create output directory and return the path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path

def save_with_backup(data: Any, output_path: Path) -> None:
    """Save data, backing up existing file if present."""
    if output_path.exists():
        backup_path = output_path.with_suffix(f".backup{output_path.suffix}")
        output_path.rename(backup_path)
        print(f"Backed up existing file to {backup_path}")
    
    # Save new file
    ensure_output_dir(output_path)
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
```

## What TAs should look for in code reviews

**✅ Good practices to encourage:**
- Pure functions that take data as parameters, return results
- I/O functions clearly separated from computation
- Relative paths using `pathlib.Path`
- CLI arguments or configuration for path specification
- Clear error messages when files aren't found

**❌ Issues to flag:**
- Hardcoded absolute paths (especially user-specific paths)
- Functions that both read files AND do computation
- Missing `if __name__ == "__main__":` guards
- No error handling for missing files
- Outputs written to unpredictable locations

**Review questions to ask:**
- "How would this code behave if run from a different directory?"
- "Can you test this function without creating actual files?"
- "What happens if the data file doesn't exist?"
- "How would someone run this code with different input data?"

## Examples for coaching conversations

**Progression from problematic to robust:**

1. **Start by identifying the problem**
   ```python
   # Show them what breaks
   df = pd.read_csv("/Users/alice/project/data.csv")  # Won't work for Bob
   ```

2. **Introduce relative paths**
   ```python
   from pathlib import Path
   data_path = Path(__file__).parent / "data" / "survey.csv"
   df = pd.read_csv(data_path)
   ```

3. **Separate I/O from computation**
   ```python
   def load_data(path: Path) -> pd.DataFrame:
       return pd.read_csv(path)
   
   def analyze_data(df: pd.DataFrame) -> dict:
       return {"mean": df["score"].mean()}
   
   def main():
       df = load_data(data_path)
       results = analyze_data(df)
   ```

4. **Add configuration and CLI**
   ```python
   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument("--data", type=Path, required=True)
       args = parser.parse_args()
       
       df = load_data(args.data)
       results = analyze_data(df)
   ```

**Key teaching points:**
- "Make your functions testable by avoiding file I/O inside them"
- "Use relative paths so your code works in containers"
- "Separate what you're computing from where the data lives"
- "Let users specify paths rather than hardcoding them"