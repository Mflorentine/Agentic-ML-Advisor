"""Step 3, Figure 3: fuel use by origin code, one dot per training car (Auto MPG).

Each origin code (1, 2, 3; the file does not name the countries) has its own column. A dot is a car's
fuel use in litres per 100 km (235.2 / miles per gallon, US gallons). The short line in each column
marks the median. Horizontal positions within a column are jittered with seed 2026 so that dots do not
overlap; the jitter has no meaning. Training cars only: the test cars are not read here.
Writes a light and a dark version.
Run from Code/:  uv run python Auto_MPG/07_fig3_fuel_by_origin.py
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
CONVERSION = 235.2
JITTER_SEED = 2026
JITTER_HALF_WIDTH = 0.12

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
train["origin"] = train["origin"].astype(int)

codes = [1, 2, 3]
rng = np.random.default_rng(JITTER_SEED)
labels = []
for x, code in enumerate(codes, start=1):
    grp = train.loc[train["origin"] == code, "fuel"].to_numpy()
    labels.append(f"Origin code {code}\n({len(grp)} cars)")

for theme_name in ("light", "dark"):
    theme = style.use(theme_name)
    fig, ax = plt.subplots(figsize=(15 * style.CM, 10 * style.CM))
    for x, code in enumerate(codes, start=1):
        grp = train.loc[train["origin"] == code, "fuel"].to_numpy()
        jitter = rng.uniform(-JITTER_HALF_WIDTH, JITTER_HALF_WIDTH, size=len(grp))
        ax.scatter(x + jitter, grp, s=14, color=style.BLUE, edgecolor=theme.ink, linewidth=0.3, alpha=0.9)
        ax.plot([x - 0.25, x + 0.25], [np.median(grp), np.median(grp)], color=theme.ink, linewidth=1.4)
    ax.set_xticks(range(1, len(codes) + 1))
    ax.set_xticklabels(labels)
    ax.set_xlim(0.4, len(codes) + 0.6)
    ax.set_ylabel("Fuel use (litres per 100 km)")
    ax.minorticks_on()
    ax.tick_params(axis="x", which="minor", bottom=False, top=False)
    style.save(fig, OUT, "fig3_fuel_by_origin", theme)

print("training cars per origin code:", train["origin"].value_counts().sort_index().to_dict())
print("written to", OUT)
