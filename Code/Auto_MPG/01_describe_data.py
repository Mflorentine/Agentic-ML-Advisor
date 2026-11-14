"""Describing pass for the Auto MPG attachment (step 1).

Reads the raw files only. Draws no conclusions and changes nothing in Attachments/.
Run from Code/:  uv run python Auto_MPG/01_describe_data.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
ATT = ROOT / "Attachments" / "Auto MPG"
MODIFIED = ATT / "auto-mpg.data"
ORIGINAL = ATT / "auto-mpg.data-original"
COLS = ["mpg", "cylinders", "displacement", "horsepower", "weight",
        "acceleration", "model_year", "origin", "car_name"]
NUMERIC = COLS[:-1]


def parse(path: Path) -> pd.DataFrame:
    """Split each line into 8 numeric-ish fields and a car name after the tab."""
    rows, bad = [], []
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            bad.append((lineno, "blank"))
            continue
        num_part, _, name = line.partition("\t")
        fields = num_part.split()
        if len(fields) != 8:
            bad.append((lineno, f"{len(fields)} fields"))
            continue
        rows.append(fields + [name.strip().strip('"')])
    print(f"{path.name}: lines={text.count(chr(10))}, parsed={len(rows)}, unparsed={bad}")
    return pd.DataFrame(rows, columns=COLS)


df_raw = parse(MODIFIED)
print("raw '?' tokens per column:", {c: int((df_raw[c] == "?").sum()) for c in NUMERIC})
print("raw 'NA' tokens per column:", {c: int((df_raw[c] == "NA").sum()) for c in NUMERIC})
print("rows with '?' in horsepower (file line numbers):")
print(df_raw.loc[df_raw["horsepower"] == "?", ["model_year", "car_name"]].to_string())

df = df_raw.copy()
for c in NUMERIC:
    df[c] = pd.to_numeric(df[c].replace("?", pd.NA), errors="coerce")
print("\nduplicate car names:", int(df["car_name"].duplicated(keep=False).sum()), "rows share a name with another row")
print("full-row duplicates:", int(df.duplicated().sum()))
print("\nmissing after reading '?' as missing:")
print(df[NUMERIC].isna().sum().to_string())
print("\nsummary (numeric):")
print(df[NUMERIC].describe().T.to_string())
for c in ["cylinders", "origin", "model_year"]:
    print(f"\n{c} counts:")
    print(df[c].value_counts().sort_index().to_string())

orig = parse(ORIGINAL)
na_rows = orig[orig["mpg"] == "NA"]
print(f"\noriginal file: rows with mpg 'NA' = {len(na_rows)}")
print(na_rows[["model_year", "car_name"]].to_string())
print("original rows with horsepower 'NA' =", int((orig["horsepower"] == "NA").sum()))
print("original rows not in modified file (by car name and model year):", len(orig) - len(df))
