"""Step 4f, Figure 3: learning curve of Logistic + L2 on the outer folds (training and cross-validation data only).

Each point is the mean validation error (misclassification rate) over the ten outer folds at one training
fraction; the bar is one standard deviation across the folds. Fractions are shares of each outer training set.

Reads   Code/outputs/dropout/08_learning_curve.csv (written by 08_recommendation.py)
Writes  Code/outputs/dropout/figures/fig3_learning_curve.png        (light)
        Code/outputs/dropout/figures/dark/fig3_learning_curve.png   (dark)
        Code/outputs/dropout/fig3_learning_curve_summary.csv         (the plotted numbers)

Run     cd Code && uv run python dropout/fig3_learning_curve.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "Code"))
import sml_style  # noqa: E402

OUT = ROOT / "Code" / "outputs" / "dropout"
FIG_DIR = OUT / "figures"

c = pd.read_csv(OUT / "08_learning_curve.csv")
s = c.groupby("fraction")["E_val"].agg(["mean", "std", "count"]).reset_index()
assert (s["count"] == 10).all(), "expected ten outer folds at every fraction"
s.to_csv(OUT / "fig3_learning_curve_summary.csv", index=False, lineterminator="\n")

for theme_name in ["light", "dark"]:
    theme = sml_style.use(theme_name)
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    ax.errorbar(s["fraction"] * 100, s["mean"], yerr=s["std"], color=sml_style.BLUE,
                marker="o", markersize=3.5, linewidth=1.2, capsize=2.5, elinewidth=0.8,
                markeredgecolor=theme.ink, markeredgewidth=0.4)
    ax.set_xlabel("Share of the outer training set used to fit (%)")
    ax.set_ylabel("Validation error (misclassification)")
    ax.set_xlim(0, 105)
    ax.set_ylim(0.14, 0.28)
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=6))
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=6))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.2f}"))
    sml_style.save(fig, FIG_DIR, "fig3_learning_curve", theme)

print("wrote", FIG_DIR / "fig3_learning_curve.png", "and dark variant")
print(s.round(4).to_string(index=False))
