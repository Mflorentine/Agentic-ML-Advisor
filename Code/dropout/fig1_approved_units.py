"""Step 3, Figure 1: approved units by outcome, training rows only.

Shows, for each outcome, how the total number of curricular units approved over the first and second
semesters is spread across students. Each panel is one outcome; each bar is the share of that outcome's
students with that total, so the two shapes compare directly despite the different group sizes.

Reads   Attachments/Student Dropout/data.csv (never modified)
        Code/outputs/dropout/02_split.csv (training rows only are plotted)
Writes  Code/outputs/dropout/figures/fig1_approved_units.png        (light)
        Code/outputs/dropout/figures/dark/fig1_approved_units.png   (dark)
        Code/outputs/dropout/fig1_approved_units.csv                (the plotted numbers)

Run     cd Code && uv run python dropout/fig1_approved_units.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "Code"))
import sml_style  # noqa: E402

SRC = ROOT / "Attachments" / "Student Dropout" / "data.csv"
SPLIT = ROOT / "Code" / "outputs" / "dropout" / "02_split.csv"
OUT = ROOT / "Code" / "outputs" / "dropout"
FIG_DIR = OUT / "figures"

df = pd.read_csv(SRC, sep=";", encoding="utf-8-sig")
df.columns = [c.strip() for c in df.columns]
split = pd.read_csv(SPLIT)
assert len(split) == len(df)

train = (split["split"] == "train").values
d = df.loc[train].copy()
assert len(d) == 3539, len(d)

d["total_approved"] = (
    d["Curricular units 1st sem (approved)"] + d["Curricular units 2nd sem (approved)"]
)
d["dropout"] = (d["Target"] == "Dropout")

max_units = int(d["total_approved"].max())
bins = np.arange(0, max_units + 2) - 0.5          # one bar per whole number of units
levels = np.arange(0, max_units + 1)

rows = []
shares = {}
for label, mask in [("Dropout", d["dropout"]), ("Not dropout", ~d["dropout"])]:
    grp = d.loc[mask, "total_approved"]
    counts = grp.value_counts().reindex(levels, fill_value=0).sort_index()
    share = counts / counts.sum()
    shares[label] = share.values
    for u, c, s in zip(levels, counts.values, share.values):
        rows.append({"outcome": label, "total_approved": int(u), "students": int(c), "share_of_outcome": float(s)})
    rows.append({"outcome": label, "total_approved": "all", "students": int(counts.sum()), "share_of_outcome": 1.0})

pd.DataFrame(rows).to_csv(OUT / "fig1_approved_units.csv", index=False, lineterminator="\n")

ymax = max(s.max() for s in shares.values()) * 1.12

for theme_name in ["light", "dark"]:
    theme = sml_style.use(theme_name)
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.9), sharex=True, sharey=True)
    for ax, (label, colour) in zip(axes, [("Dropout", sml_style.RED), ("Not dropout", sml_style.BLUE)]):
        n = int((d["dropout"] if label == "Dropout" else ~d["dropout"]).sum())
        ax.bar(levels, shares[label], width=0.8, color=colour, edgecolor=theme.ink, linewidth=0.3)
        ax.set_title(f"{label}", fontsize=10, color=theme.ink)
        ax.set_xlabel("Units approved, both semesters")
        ax.set_xlim(-0.6, max_units + 0.6)
        ax.set_ylim(0, ymax)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=8))
        ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=5))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    axes[0].set_ylabel("Share of students in group")
    fig.subplots_adjust(wspace=0.12)
    sml_style.save(fig, FIG_DIR, "fig1_approved_units", theme)

print("wrote", FIG_DIR / "fig1_approved_units.png", "and dark variant")
print(pd.DataFrame(rows).to_string(index=False))
