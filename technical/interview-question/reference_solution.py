import logging
from pathlib import Path
from typing import Iterable, Optional
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def load_data(path: Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        logger.error("File not found: %s", path)
        raise
    logger.info("Loaded %d rows from %s", len(df), path)
    return df

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw data: ensure required columns, fill missing, normalize values."""
    required = {"first_name", "last_name", "score", "group"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    out = df.dropna(subset=["first_name", "last_name"]).copy()
    out["name"] = out["first_name"] + " " + out["last_name"]
    out["score"] = out["score"].fillna(0)
    out = out[out["score"] >= 0]
    out["group"] = out["group"].astype(str).str.lower()
    return out

def analyze(
    df: pd.DataFrame,
    top_n: int = 5,
    groups: Optional[Iterable[str]] = None
) -> pd.DataFrame:
    """Return the top groups by average score."""
    groups = list(groups) if groups else ["group"]
    g = (
        df.groupby(groups, dropna=False)["score"]
          .mean()
          .reset_index()
          .sort_values("score", ascending=False)
    )
    return g.head(top_n)

if __name__ == "__main__":
    in_path = Path("data.csv")
    out_csv = Path("out.csv")
    out_json = Path("out.json")

    df = load_data(in_path)
    df = clean(df)
    result = analyze(df, top_n=5, groups=["group"])
    result.to_csv(out_csv, index=False)
    result.to_json(out_json, orient="records")
    logger.info("Wrote %s and %s", out_csv, out_json)
