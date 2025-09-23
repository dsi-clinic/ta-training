# Data Validation and Types

Type annotations and data validation catch bugs early, improve code readability, and ensure data quality throughout the pipeline. TAs should encourage these practices especially in student projects where data quality issues can cascade into wrong conclusions.

## Why validate and annotate
- **Clarifies code** for reviewers and future maintainers — what does this function expect?
- **Catches common bugs** with static checkers before runtime failures.
- **Ensures data quality** and prevents downstream errors in analysis pipelines.
- **Professional standard** — industry teams rely on these practices for reliability.

## Type annotations basics

**Function signatures: parameter and return types**
```python
# ❌ Unclear what this function expects or returns
def clean_survey_data(data, config):
    # ...
    return processed

# ✅ Clear expectations and return type
def clean_survey_data(data: pd.DataFrame, config: dict[str, Any]) -> pd.DataFrame:
    """Remove invalid responses and standardize column names."""
    # ...
    return processed
```

**Common type patterns**
```python
from typing import Optional, Iterable, Mapping, Any
import pandas as pd

def load_datasets(
    file_paths: list[str], 
    sheet_names: Optional[list[str]] = None
) -> dict[str, pd.DataFrame]:
    """Load multiple Excel files into a dictionary of DataFrames."""
    datasets = {}
    for path in file_paths:
        datasets[path] = pd.read_excel(path, sheet_name=sheet_names)
    return datasets

def aggregate_scores(
    scores: Mapping[str, float], 
    weights: Optional[Mapping[str, float]] = None
) -> float:
    """Calculate weighted average of scores."""
    if weights is None:
        return sum(scores.values()) / len(scores)
    return sum(score * weights.get(key, 1.0) for key, score in scores.items())
```

## Data science specifics

**Pandas DataFrame patterns**
```python
import pandas as pd
from typing import Literal

def filter_by_group(
    df: pd.DataFrame, 
    group_col: str,
    target_groups: list[str]
) -> pd.DataFrame:
    """Filter DataFrame to include only specified groups."""
    if group_col not in df.columns:
        raise ValueError(f"Column '{group_col}' not found in DataFrame")
    return df[df[group_col].isin(target_groups)].copy()

# For functions that expect specific columns, document in docstring
def calculate_survey_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate composite survey scores.
    
    Expected columns:
    - q1_rating: int (1-5 scale)
    - q2_rating: int (1-5 scale) 
    - respondent_weight: float
    """
    return (df['q1_rating'] + df['q2_rating']) * df['respondent_weight']
```

## Data validation with Pydantic

**When to use Pydantic vs simple type hints**
- **Simple type hints**: Basic function signatures, return types
- **Pydantic**: Configuration files, API data, complex validation rules, data pipeline checkpoints

**Configuration classes**
```python
from pydantic import BaseModel, Field, validator
from pathlib import Path

class ProjectConfig(BaseModel):
    """Configuration for data processing pipeline."""
    
    # Field validation with constraints
    input_dir: Path = Field(..., description="Directory containing raw data files")
    output_dir: Path = Field(default=Path("./outputs"))
    min_sample_size: int = Field(default=100, ge=1)
    confidence_level: float = Field(default=0.95, ge=0.5, le=0.99)
    
    # Custom validation
    @validator('input_dir')
    def input_dir_must_exist(cls, v):
        if not v.exists():
            raise ValueError(f"Input directory does not exist: {v}")
        return v
    
    @validator('output_dir')
    def create_output_dir(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v

# Usage in student projects
config = ProjectConfig(
    input_dir=Path("./data/raw"),
    min_sample_size=50,
    confidence_level=0.90
)
```

**Data pipeline models**
```python
from pydantic import BaseModel, validator
from typing import Literal
import pandas as pd

class DataQualityReport(BaseModel):
    """Report on data quality checks."""
    
    total_rows: int
    complete_rows: int
    duplicate_rows: int
    outlier_count: int
    quality_score: float = Field(ge=0.0, le=1.0)
    
    @validator('quality_score', always=True)
    def calculate_quality_score(cls, v, values):
        if 'total_rows' in values and values['total_rows'] > 0:
            complete_ratio = values.get('complete_rows', 0) / values['total_rows']
            duplicate_penalty = values.get('duplicate_rows', 0) / values['total_rows']
            return max(0.0, complete_ratio - duplicate_penalty)
        return 0.0

def assess_data_quality(df: pd.DataFrame) -> DataQualityReport:
    """Generate data quality report."""
    return DataQualityReport(
        total_rows=len(df),
        complete_rows=len(df.dropna()),
        duplicate_rows=df.duplicated().sum(),
        outlier_count=detect_outliers(df)  # Custom function
    )
```

**Integration with pandas DataFrames**
```python
from pydantic import BaseModel, Field
import pandas as pd

class SurveyRecord(BaseModel):
    """Individual survey response record."""
    
    respondent_id: str = Field(..., min_length=1)
    age: int = Field(..., ge=18, le=100)
    satisfaction_score: int = Field(..., ge=1, le=5)
    department: Literal["Engineering", "Marketing", "Sales", "HR"]
    
    class Config:
        # Allow conversion from pandas Series
        arbitrary_types_allowed = True

def validate_survey_data(df: pd.DataFrame) -> list[SurveyRecord]:
    """Validate each row of survey data."""
    validated_records = []
    errors = []
    
    for idx, row in df.iterrows():
        try:
            record = SurveyRecord(**row.to_dict())
            validated_records.append(record)
        except Exception as e:
            errors.append(f"Row {idx}: {e}")
    
    if errors:
        print(f"Found {len(errors)} validation errors:")
        for error in errors[:5]:  # Show first 5
            print(f"  {error}")
    
    return validated_records
```

## Common patterns TAs should recognize

**1. Configuration classes** (instead of dictionaries)
```python
# ❌ Hard to validate, error-prone
config = {
    "model_type": "random_forest",
    "n_estimators": 100,
    "test_size": 0.2,
    "random_state": 42
}

# ✅ Self-documenting and validated
class ModelConfig(BaseModel):
    model_type: Literal["random_forest", "svm", "logistic_regression"]
    n_estimators: int = Field(default=100, ge=1, le=1000)
    test_size: float = Field(default=0.2, gt=0.0, lt=1.0)
    random_state: int = Field(default=42)
```

**2. API response models** (for external data)
```python
class WeatherAPI(BaseModel):
    """Structure for weather API responses."""
    
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100)
    timestamp: str
    location: str = Field(..., min_length=1)
    
    @validator('timestamp')
    def parse_timestamp(cls, v):
        # Ensure timestamp is in expected format
        try:
            pd.to_datetime(v)
            return v
        except:
            raise ValueError(f"Invalid timestamp format: {v}")
```

**3. Database record models**
```python
class ExperimentResult(BaseModel):
    """Results from A/B test experiment."""
    
    experiment_id: str
    variant: Literal["control", "treatment"]
    user_id: str
    conversion: bool
    revenue: float = Field(default=0.0, ge=0.0)
    session_duration: int = Field(..., ge=0)  # seconds
```

## Tooling TAs should check for

**Runtime validation setup**
```python
# Look for validation at data entry points
def load_config(config_path: str) -> ProjectConfig:
    """Load and validate project configuration."""
    with open(config_path) as f:
        config_data = json.load(f)
    
    # Pydantic validates on instantiation
    return ProjectConfig(**config_data)  # Raises ValidationError if invalid
```

**Integration in requirements.txt**
```toml
[project]
dependencies = [
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "ruff==0.7.2",
    "pre-commit~=3.5",
]
```

## What TAs should look for in code reviews

**✅ Good practices to encourage:**
- Type annotations on public functions
- Pydantic models for configuration and external data
- Validation at data pipeline boundaries
- Clear error messages when validation fails

**❌ Issues to flag:**
- Functions accepting `Any` or no type hints in data processing code
- Configuration loaded as raw dictionaries without validation  
- Silent failures when data doesn't match expected schema
- Complex nested dictionaries that could be Pydantic models

**Review questions to ask:**
- "What happens if this DataFrame is missing a column your function expects?"
- "How would a new team member know what structure this function returns?"
- "Could this configuration be validated when loaded instead of failing later?"

## Examples for coaching conversations

**Progression from basic to advanced:**

1. **Start with function signatures**
   ```python
   def clean_data(df):  # What columns? What's returned?
   →
   def clean_data(df: pd.DataFrame) -> pd.DataFrame:
   ```

2. **Add input validation**
   ```python
   def clean_data(df: pd.DataFrame) -> pd.DataFrame:
       if 'score' not in df.columns:
           raise ValueError("DataFrame must contain 'score' column")
   ```

3. **Use Pydantic for complex cases**
   ```python
   class CleaningConfig(BaseModel):
       remove_outliers: bool = True
       outlier_threshold: float = Field(default=2.0, gt=0)
       
   def clean_data(df: pd.DataFrame, config: CleaningConfig) -> pd.DataFrame:
   ```

**Incrementally introduce validation** — don't overwhelm students, but show how each step prevents common issues they've likely encountered.