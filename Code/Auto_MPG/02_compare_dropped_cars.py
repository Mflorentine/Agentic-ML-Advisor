"""Step 1 check: are the 6 cars with no horsepower value different from the other cars?

Descriptive comparison of the raw file only. No model is fitted and nothing is changed.
Run from Code/:  uv run python Auto_MPG/02_compare_dropped_cars.py
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
for c in COLS[:-1]:
    df[c] = pd.to_numeric(df[c].replace("?", pd.NA))

dropped = df["horsepower"].isna()
kept = ~dropped
print(f"dropped: {dropped.sum()} cars; kept: {kept.sum()} cars\n")

num = ["mpg", "cylinders", "displacement", "weight", "acceleration", "model_year"]
summary = pd.DataFrame({
    "dropped_mean": df.loc[dropped, num].mean(),
    "kept_mean": df.loc[kept, num].mean(),
    "dropped_min": df.loc[dropped, num].min(),
    "dropped_max": df.loc[dropped, num].max(),
    "kept_min": df.loc[kept, num].min(),
    "kept_max": df.loc[kept, num].max(),
})
print(summary.round(2).to_string())

print("\norigin counts (dropped | kept):")
print(pd.concat([df.loc[dropped, "origin"].value_counts(), df.loc[kept, "origin"].value_counts()],
                axis=1, keys=["dropped", "kept"]).fillna(0).astype(int).to_string())

print("\ndropped cars:")
print(df.loc[dropped, ["model_year", "origin", "displacement", "mpg", "car_name"]].to_string())

print("\nmpg rank of dropped cars within all 398 (1 = lowest):")
ranks = df["mpg"].rank(method="min")
print(ranks[dropped].astype(int).to_string())
