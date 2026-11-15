"""Step 2: the train/test split for the Auto MPG analysis, locked once made.

Uses the 392 cars with a horsepower value (6 dropped, DR-01 to DR-08 and the Data Summary).
Test part: one in five cars, split by car name so that all rows with one name go to the same side.
Seed: 2026. The test rows are written out and must not be read before the final evaluation.
Run from Code/:  uv run python Auto_MPG/04_split.py
"""
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

SEED = 2026
TEST_SIZE = 0.2
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Attachments" / "Auto MPG" / "auto-mpg.data"
OUT = ROOT / "Code" / "outputs" / "Auto_MPG" / "split_seed2026.csv"
COLS = ["mpg", "cylinders", "displacement", "horsepower", "weight",
        "acceleration", "model_year", "origin", "car_name"]

rows = []
for file_line, line in enumerate(SRC.read_text(encoding="utf-8").splitlines(), 1):
    num_part, _, name = line.partition("\t")
    rows.append([file_line] + num_part.split() + [name.strip().strip('"')])
df = pd.DataFrame(rows, columns=["file_line"] + COLS)
for c in COLS[:-1]:
    df[c] = pd.to_numeric(df[c].replace("?", pd.NA))
df = df.dropna(subset=["horsepower"]).reset_index(drop=True)

splitter = GroupShuffleSplit(n_splits=1, test_size=TEST_SIZE, random_state=SEED)
train_idx, test_idx = next(splitter.split(df, groups=df["car_name"]))
df["set"] = "train"
df.loc[test_idx, "set"] = "test"

OUT.parent.mkdir(parents=True, exist_ok=True)
df[["file_line", "car_name", "model_year", "set"]].to_csv(OUT, index=False)

n_test = int((df["set"] == "test").sum())
print(f"used rows: {len(df)}")
print(f"training rows: {len(df) - n_test}; test rows: {n_test}")
print(f"test share of rows: {n_test / len(df):.3f}")
print(f"test car names: {df.loc[df['set'] == 'test', 'car_name'].nunique()}")
shared = set(df.loc[df["set"] == "test", "car_name"]) & set(df.loc[df["set"] == "train", "car_name"])
print(f"names on both sides (should be 0): {len(shared)}")
print(f"written: {OUT}")
