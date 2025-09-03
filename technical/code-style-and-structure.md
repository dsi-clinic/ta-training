# Code Style and Structure

Guidelines for organizing Python code in data science projects. These patterns make code more readable, maintainable, and professional-looking to reviewers and collaborators.

---

## Project structure patterns

**Recommended data science project layout**
```
project/
├── README.md
├── requirements.txt
├── Dockerfile
├── Makefile
├── .gitignore
├── .env.example
├── data/
│ ├── raw/ # Original, immutable data
│ ├── processed/ # Cleaned, transformed data
│ └── external/ # Third-party datasets
├── notebooks/ # Jupyter notebooks for exploration
├── src/ # Source code package
│ ├── init.py
│ ├── data/ # Data loading/processing
│ ├── features/ # Feature engineering
│ ├── models/ # Model training/evaluation
│ └── utils/ # Shared utilities
├── tests/ # Test files
├── outputs/ # Generated results, plots, models
└── docs/ # Project documentation
```


**Package vs script organization**
```python
# ❌ Everything in one giant script
# analysis.py (500+ lines)
import pandas as pd
import numpy as np
# ... all functions mixed together

def load_data():
    # ...

def clean_data():
    # ...

def train_model():
    # ...

def main():
    # ... everything happens here

# ✅ Organized into logical modules
# src/data/loader.py
def load_survey_data(path: Path) -> pd.DataFrame:
    """Load and validate survey data."""
    
# src/data/cleaner.py  
def clean_survey_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove invalid responses and standardize columns."""

# src/models/trainer.py
def train_satisfaction_model(df: pd.DataFrame) -> Model:
    """Train model to predict satisfaction scores."""

# main.py
from src.data.loader import load_survey_data
from src.data.cleaner import clean_survey_data
from src.models.trainer import train_satisfaction_model

def main():
    df = load_survey_data(DATA_PATH)
    df_clean = clean_survey_data(df)
    model = train_satisfaction_model(df_clean)
```

---

## Naming conventions

**Variables and functions: snake_case**
```python
# ✅ Clear, descriptive names
user_satisfaction_scores = df['satisfaction'].values
average_response_time = calculate_mean_response_time(survey_data)

def calculate_confidence_interval(data: np.ndarray, confidence_level: float) -> tuple:
    """Calculate confidence interval for the mean."""
    
# ❌ Unclear abbreviations and inconsistent casing
usrSat = df['satisfaction'].values  # What does this mean?
avgRespT = calc_mean_rt(sdata)      # Cryptic abbreviations
```

**Classes: PascalCase**
```python
# ✅ Clear class names
class SurveyDataProcessor:
    """Process and validate survey response data."""
    
class ModelEvaluator:
    """Evaluate model performance with various metrics."""

# ❌ Inconsistent or unclear
class surveyprocessor:  # Should be PascalCase
class DataThing:        # "Thing" is not descriptive
```

**Constants: UPPER_SNAKE_CASE**
```python
# ✅ Module-level constants
DEFAULT_CONFIDENCE_LEVEL = 0.95
MAX_SURVEY_RESPONSE_TIME = 3600  # seconds
REQUIRED_COLUMNS = ['user_id', 'satisfaction', 'department']

# Configuration constants
DATA_DIR = Path("./data")
OUTPUT_DIR = Path("./outputs")
```

**Files and directories: snake_case**
```
src/
├── data_loader.py # ✅
├── model_trainer.py # ✅
├── survey_analysis.py # ✅
└── utils/
├── file_helpers.py # ✅
└── math_utils.py # ✅
```


---

## Docstring standards

**Module docstrings**
```python
"""
Survey data analysis utilities.

This module provides functions for loading, cleaning, and analyzing
employee satisfaction survey data. It handles data validation,
outlier detection, and basic statistical analysis.

Example:
    >>> from src.analysis import survey_utils
    >>> df = survey_utils.load_survey_data("data/survey.csv")
    >>> clean_df = survey_utils.clean_responses(df)
"""

import pandas as pd
from pathlib import Path
```

**Function docstrings (Google style)**
```python
def calculate_satisfaction_statistics(
    df: pd.DataFrame, 
    group_by: str = None
) -> dict[str, float]:
    """Calculate satisfaction score statistics.
    
    Computes mean, median, and standard deviation of satisfaction scores,
    optionally grouped by a categorical variable.
    
    Args:
        df: DataFrame containing survey responses with 'satisfaction' column
        group_by: Optional column name to group statistics by
        
    Returns:
        Dictionary with statistical measures. If group_by is specified,
        returns nested dict with stats for each group.
        
    Raises:
        ValueError: If 'satisfaction' column is missing from DataFrame
        KeyError: If group_by column doesn't exist
        
    Example:
        >>> stats = calculate_satisfaction_statistics(survey_df)
        >>> print(stats['mean'])
        4.2
        
        >>> dept_stats = calculate_satisfaction_statistics(survey_df, 'department')
        >>> print(dept_stats['Engineering']['mean'])
        4.5
    """
    if 'satisfaction' not in df.columns:
        raise ValueError("DataFrame must contain 'satisfaction' column")
    
    # Implementation here...
```

**Class docstrings**
```python
class SurveyAnalyzer:
    """Analyzer for employee satisfaction survey data.
    
    This class provides methods for loading survey data, performing
    data quality checks, and computing various satisfaction metrics.
    
    Attributes:
        data: The loaded survey DataFrame
        config: Analysis configuration settings
        
    Example:
        >>> analyzer = SurveyAnalyzer("data/survey.csv")
        >>> analyzer.load_data()
        >>> results = analyzer.analyze_satisfaction_by_department()
    """
    
    def __init__(self, data_path: Path, config: AnalysisConfig = None):
        """Initialize the analyzer.
        
        Args:
            data_path: Path to survey data CSV file
            config: Optional configuration for analysis parameters
        """
        self.data_path = data_path
        self.config = config or AnalysisConfig()
        self.data = None
```

---

## Code organization within files

**Logical ordering of elements**
```python
"""Module docstring at the top."""

# Standard library imports
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List

# Third-party imports  
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Local imports
from src.config import AnalysisConfig
from src.utils.validation import validate_survey_data

# Module-level constants
LOGGER = logging.getLogger(__name__)
DEFAULT_OUTPUT_DIR = Path("./outputs")

# Helper functions (used internally)
def _validate_input_data(df: pd.DataFrame) -> None:
    """Private helper function for input validation."""
    # Implementation...

# Public functions (main API)
def load_survey_data(path: Path) -> pd.DataFrame:
    """Public function for loading data."""
    # Implementation...

# Classes
class SurveyAnalyzer:
    """Main analysis class."""
    # Implementation...

# Main execution
if __name__ == "__main__":
    main()
```

**Function organization within classes**
```python
class SurveyAnalyzer:
    """Survey data analyzer."""
    
    def __init__(self, config: AnalysisConfig):
        """Constructor first."""
        self.config = config
        self.data = None
    
    # Public methods (main API)
    def load_data(self, path: Path) -> None:
        """Load survey data from file."""
        
    def analyze_satisfaction(self) -> Dict[str, float]:
        """Analyze satisfaction scores."""
        
    def generate_report(self) -> str:
        """Generate analysis report."""
        
    # Private methods (implementation details)
    def _validate_data_quality(self) -> None:
        """Private method for validation."""
        
    def _calculate_statistics(self) -> Dict[str, float]:
        """Private method for calculations."""
```

---

## Comments and inline documentation

**When to comment**
```python
# ✅ Explain WHY, not what
def calculate_outlier_threshold(data: np.ndarray) -> float:
    """Calculate threshold for outlier detection."""
    # Use 1.5 * IQR method as it's less sensitive to extreme values
    # than standard deviation-based methods for this survey data
    q75, q25 = np.percentile(data, [75, 25])
    iqr = q75 - q25
    return q75 + 1.5 * iqr

# ✅ Explain complex business logic
def calculate_satisfaction_score(responses: Dict[str, int]) -> float:
    """Calculate weighted satisfaction score."""
    # Weight recent responses more heavily (last 30 days = 1.0, older = 0.7)
    # This reflects our focus on current employee sentiment
    base_score = sum(responses.values()) / len(responses)
    recency_weight = 0.9 if responses['days_since_response'] <= 30 else 0.7
    return base_score * recency_weight

# ❌ Don't comment obvious code
x = x + 1  # Increment x by 1
df = pd.read_csv(file_path)  # Read CSV file
```

**TODO comments for development**
```python
def advanced_analysis(df: pd.DataFrame) -> Dict:
    """Perform advanced statistical analysis."""
    # TODO: Add statistical significance testing
    # TODO: Include confidence intervals in results  
    # FIXME: Handle missing data in satisfaction scores
    # NOTE: This assumes normal distribution - validate in next version
    
    basic_stats = calculate_basic_stats(df)
    return basic_stats
```

---

## Code formatting and consistency

**Line length and formatting**
```python
# ✅ Break long lines logically
def analyze_survey_responses(
    data: pd.DataFrame,
    satisfaction_column: str = "satisfaction", 
    group_columns: List[str] = None,
    include_demographics: bool = True
) -> Dict[str, Any]:
    """Analyze survey responses with multiple grouping options."""
    
# ✅ Break long expressions
total_satisfaction_score = (
    base_satisfaction_score 
    * response_quality_multiplier 
    * recency_weight
    + demographic_adjustment
)

# ✅ Format dictionaries and lists clearly
analysis_config = {
    "confidence_level": 0.95,
    "outlier_threshold": 2.0,
    "min_sample_size": 30,
    "include_demographics": True,
}

required_columns = [
    "user_id",
    "satisfaction_score", 
    "department",
    "response_date",
]
```

**Consistent spacing**
```python
# ✅ Consistent spacing around operators
result = (score * weight) + adjustment
average = total_sum / count

# ✅ Space after commas
process_data(df, group_by="department", threshold=0.05)

# ✅ No extra spaces
df[df["satisfaction"] > 4]  # ✅
df[ df[ "satisfaction" ] > 4 ]  # ❌ Too much space
```

---

## Error messages and logging

**Descriptive error messages**
```python
# ✅ Helpful error messages
def load_survey_data(file_path: Path) -> pd.DataFrame:
    """Load survey data with validation."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Survey data file not found: {file_path}\n"
            f"Expected location: {file_path.absolute()}\n"
            f"Current working directory: {Path.cwd()}"
        )
    
    df = pd.read_csv(file_path)
    
    required_cols = ["user_id", "satisfaction", "department"]
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"Missing required columns in {file_path.name}: {missing_cols}\n"
            f"Available columns: {list(df.columns)}\n"
            f"Required columns: {required_cols}"
        )
    
    return df

# ❌ Unhelpful error messages  
def load_survey_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)  # FileNotFoundError: [Errno 2] No such file
    assert "satisfaction" in df.columns  # AssertionError (no context)
    return df
```

**Structured logging**
```python
import logging

# ✅ Set up logging properly
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_survey_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process survey data with logging."""
    logger.info(f"Starting data processing. Input shape: {df.shape}")
    
    # Log data quality issues
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        logger.warning(f"Found {missing_count} missing values in dataset")
    
    # Log processing steps
    original_size = len(df)
    df_clean = df.dropna()
    removed_count = original_size - len(df_clean)
    
    if removed_count > 0:
        logger.info(f"Removed {removed_count} rows with missing data")
    
    logger.info(f"Processing complete. Output shape: {df_clean.shape}")
    return df_clean
```

---

## What TAs should look for in code reviews

**✅ Good practices to encourage:**
- Clear, descriptive variable and function names
- Consistent naming conventions (snake_case for functions, PascalCase for classes)
- Comprehensive docstrings for public functions and classes
- Logical code organization and file structure
- Helpful error messages with context

**❌ Issues to flag:**
- Single-letter variable names (except for short loops: `for i in range(n)`)
- Inconsistent naming conventions within the same file
- Missing docstrings for complex functions
- Giant files with unrelated functionality mixed together
- Vague error messages or bare assertions

**Review questions to ask:**
- "Could someone unfamiliar with this project understand what this function does?"
- "Are the variable names descriptive enough that you don't need comments?"
- "Is this file focused on one clear responsibility?"
- "What would happen if someone gets an error - would they know how to fix it?"

---

## Examples for coaching conversations

**Progression from messy to professional:**

1. **Start with naming**
   ```python
   # What does this do?
   def calc(d, c):
       return d.groupby(c).mean()
   
   # Much clearer
   def calculate_group_averages(df: pd.DataFrame, group_column: str) -> pd.DataFrame:
       """Calculate average values for each group."""
       return df.groupby(group_column).mean()
   ```

2. **Add structure**
   ```python
   # Everything in one file
   analysis.py (500 lines)
   
   # Split into logical modules
   src/data/loader.py
   src/analysis/statistics.py
   src/visualization/plots.py
   ```

3. **Improve documentation**
   ```python
   def process_data(df):
       # Some processing happens...
       return result
   
   def process_survey_data(df: pd.DataFrame) -> pd.DataFrame:
       """Remove invalid responses and normalize satisfaction scores.
       
       Args:
           df: Survey responses with 'satisfaction' and 'user_id' columns
           
       Returns:
           Cleaned DataFrame with normalized satisfaction scores (0-1 scale)
       """
   ```

**Teaching approach:**
- Show examples of code that's hard to understand vs clear code
- Emphasize that good style helps teammates (and future you) understand code
- Connect to professional standards - this is how industry code looks
- Point out that clear code prevents bugs by making logic obvious