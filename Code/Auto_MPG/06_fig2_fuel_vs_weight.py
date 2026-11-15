"""Step 3, Figure 2: fuel use against weight, one dot per training car (Auto MPG).

Plots the observations only: no line or curve is fitted or drawn. Weight is in the units recorded
in the file (not verified). Fuel use is litres per 100 km = 235.2 / miles per gallon (US gallons).
Training cars only: the test cars are not read here.
Writes a light and a dark version.
Run from Code/:  uv run python Auto_MPG/06_fig2_fuel_vs_weight.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
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
CONVERSION = 235.2

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

for theme_name in ("light", "dark"):
    theme = style.use(theme_name)
    fig, ax = plt.subplots(figsize=(15 * style.CM, 9.5 * style.CM))
    ax.scatter(train["weight"], train["fuel"], s=14, color=style.BLUE,
               edgecolor=theme.ink, linewidth=0.3, alpha=0.9)
    ax.set_xlabel("Weight (units as recorded in the file, not verified)")
    ax.set_ylabel("Fuel use (litres per 100 km)")
    ax.minorticks_on()
    style.save(fig, OUT, "fig2_fuel_vs_weight", theme)

print("training cars plotted:", len(train))
print("written to", OUT)
