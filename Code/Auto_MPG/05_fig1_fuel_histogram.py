"""Step 3, Figure 1: histogram of fuel use for the 314 training cars (Auto MPG).

Shows how the figure to be predicted (litres per 100 km = 235.2 / miles per gallon, assuming US
gallons) is spread over the training cars. Training cars only: the test cars are not read here.
Writes a light and a dark version, and a text file with the summary numbers the report quotes.
Run from Code/:  uv run python Auto_MPG/05_fig1_fuel_histogram.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))
import sml_style as style  # noqa: E402

ROOT = CODE.parent
SRC = ROOT / "Attachments" / "Auto MPG" / "auto-mpg.data"
SPLIT = CODE / "outputs" / "Auto_MPG" / "split_seed2026.csv"
OUT = CODE / "outputs" / "Auto_MPG"
COLS = ["mpg", "cylinders", "displacement", "horsepower", "weight",
        "acceleration", "model_year", "origin", "car_name"]
CONVERSION = 235.2  # litres per 100 km = 235.2 / miles per gallon (US gallons)
BIN_WIDTH = 1.0     # litres per 100 km per bar

rows = []
for file_line, line in enumerate(SRC.read_text(encoding="utf-8").splitlines(), 1):
    num_part, _, name = line.partition("\t")
    rows.append([file_line] + num_part.split() + [name.strip().strip('"')])
df = pd.DataFrame(rows, columns=["file_line"] + COLS)
for c in COLS[:-1]:
    df[c] = pd.to_numeric(df[c].replace("?", pd.NA))
df = df.dropna(subset=["horsepower"]).reset_index(drop=True)

split = pd.read_csv(SPLIT)
assert len(split) == len(df), "split file does not match the used rows"
assert (split["file_line"].values == df["file_line"].values).all(), "split rows out of step with the data"
train = df.loc[split["set"].values == "train"].copy()
assert len(train) == 314, len(train)
train["fuel"] = CONVERSION / train["mpg"]

fuel = train["fuel"].to_numpy()
lo = np.floor(fuel.min())
hi = np.ceil(fuel.max())
edges = np.arange(lo, hi + BIN_WIDTH, BIN_WIDTH)

summary = {
    "training cars": len(fuel),
    "minimum (litres per 100 km)": round(float(fuel.min()), 2),
    "maximum (litres per 100 km)": round(float(fuel.max()), 2),
    "mean (litres per 100 km)": round(float(fuel.mean()), 2),
    "median (litres per 100 km)": round(float(np.median(fuel)), 2),
    "bar width (litres per 100 km)": BIN_WIDTH,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "fig1_fuel_histogram_summary.txt").write_text(
    "\n".join(f"{k}: {v}" for k, v in summary.items()) + "\n", encoding="utf-8")

for theme_name in ("light", "dark"):
    theme = style.use(theme_name)
    fig, ax = plt.subplots(figsize=(15 * style.CM, 9.5 * style.CM))
    ax.hist(fuel, bins=edges, color=style.BLUE, edgecolor=theme.ink, linewidth=0.5)
    ax.set_xlabel("Fuel use (litres per 100 km)")
    ax.set_ylabel("Number of training cars")
    ax.set_xticks(edges[::2])
    ax.minorticks_on()
    style.save(fig, OUT, "fig1_fuel_histogram", theme)

print("summary:", summary)
print("written to", OUT)
