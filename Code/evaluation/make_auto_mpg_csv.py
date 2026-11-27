"""Copy Attachments/Auto MPG/auto-mpg.data to a CSV with column names, for the workspace evaluation.

Every value is copied as the same text; nothing is cleaned, converted or removed.
The 6 missing horsepower values stay as "?". The original file is only read.
Run: cd Code && uv run python evaluation/make_auto_mpg_csv.py
"""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Attachments" / "Auto MPG" / "auto-mpg.data"
OUT = ROOT / "Attachments" / "Evaluation" / "auto-mpg.csv"
# Column names from auto-mpg.names, section 7 (Attribute Information).
COLUMNS = ["mpg", "cylinders", "displacement", "horsepower", "weight",
           "acceleration", "model year", "origin", "car name"]

rows = []
for line in SRC.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    numbers, name = line.split("\t", 1)
    values = numbers.split()
    assert len(values) == 8, line
    rows.append(values + [name.strip().strip('"')])

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(COLUMNS)
    w.writerows(rows)

print("source sha256", hashlib.sha256(SRC.read_bytes()).hexdigest())
print("rows", len(rows), "missing horsepower", sum(r[3] == "?" for r in rows))
print("written", OUT)
