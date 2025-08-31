import pandas as pd
import json
import logging  # not used

DATA_PATH = "data.csv"   # TODO: point to correct file later?
OUT_FILE = "out.csv"

# def old_clean(df):
#     # legacy path, keep for reference
#     # df = df.dropna()
#     # return df
#     pass

def load_data(path=DATA_PATH):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print("could not read file:", e)  # replace later?
        return None
    print(f"loaded {len(df)} rows")  # DEBUG
    return df

def clean(df):
    # drop empty names
    df.dropna(subset=["first_name", "last_name"], inplace=True)
    # combine names
    df["name"] = df["first_name"] + " " + df["last_name"]
    # normalize score
    df["score"] = df["score"].fillna(0)
    # remove negative scores (shouldn’t happen)
    bad = df["score"] < 0
    if bad.any():
        print("found negative scores:", df[bad]["score"].tolist())
        df = df[~bad]  # maybe warn instead?
    # convert categories to lower
    df["group"] = df["group"].astype(str).str.lower()
    return df

def analyze(df, top_n=5, groups=[]):
    # groups e.g. ["group"] or ["group", "category"]
    if groups == []:
        groups = ["group"]  # default at runtime
    # average per group
    g = df.groupby(groups)["score"].mean().reset_index()
    g = g.sort_values("score", ascending=False)
    print("top groups:")
    for i, row in g.head(top_n).iterrows():
        print(i, row["score"], row[groups[0]])
    # write results
    g.to_csv(OUT_FILE, index=False)
    print("wrote results to", OUT_FILE)
    # also dump json for later
    with open("out.json", "w") as f:
        f.write(json.dumps(g.to_dict(orient="records")))
    # return nothing (side-effect only)

# quick run
df = load_data()
if df is not None:
    df = clean(df)
    analyze(df)
