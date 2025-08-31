from pathlib import Path
import pandas as pd

def main() -> None:
    data = Path("data.csv")
    if not data.exists():
        print("no data.csv found; exiting")
        return
    df = pd.read_csv(data)
    print(f"rows: {len(df)}")

if __name__ == "__main__":
    main()
