"""Step 1 check: how many rows share a car name, for the grouping decision (Admissibility 3).

Descriptive only. Reads the raw file, uses the 392 rows that have a horsepower value.
Run from Code/:  uv run python Auto_MPG/03_group_sizes.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Attachments" / "Auto MPG" / "auto-mpg.data"
COLS = ["mpg", "cylinders", "displacement", "horsepower", "weight",
        "acceleration", "model_year", "origin", "car_name"]

rows = []
for line in SRC.read_text(encoding="utf-8").splitlines():
    num_part, _, name = line.partition("\t")
    rows.append(num_part.split() + [name.strip().strip('"')])
df = pd.DataFrame(rows, columns=COLS)
df["horsepower"] = pd.to_numeric(df["horsepower"].replace("?", pd.NA))
df = df.dropna(subset=["horsepower"]).reset_index(drop=True)

sizes = df.groupby("car_name").size()
print(f"rows used: {len(df)}")
print(f"distinct car names: {len(sizes)}")
print("group size counts (size: number of names):")
print(sizes.value_counts().sort_index().to_string())
print(f"largest group: {sizes.max()} rows ({sizes.idxmax()!r})")
print(f"rows in groups of 2 or more: {int(sizes[sizes >= 2].sum())}")
print("\nnames that appear in more than one model year:")
multi_year = df.groupby("car_name")["model_year"].nunique()
print(f"names spanning 2+ model years: {int((multi_year >= 2).sum())}")
print(f"names with all rows in one model year: {int((multi_year == 1).sum())}")
