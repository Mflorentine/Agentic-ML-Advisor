"""Step 4f, Figure 4: average error of each method across the ten training parts, with its spread.

Reads only the approved cross-validation results (outputs/Auto_MPG/core_recommend.json, which holds the
per-method averages and spreads). Draws no new model. Training cars only.
Writes a light and a dark version.
Run from Code/:  uv run python Auto_MPG/08_fig4_cv_comparison.py
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))
import sml_style as style  # noqa: E402

OUT = CODE / "outputs" / "Auto_MPG"
res = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
means = res["cv_mean_RMSE"]
spreads = res["cv_spread_RMSE"]

ORDER = ["baseline", "Exponential", "Exponential + L2", "Linear", "Linear + poly", "Tree", "kNN"]
LABELS = {
    "baseline": "Average guess\n(baseline)",
    "Exponential": "Exponential",
    "Exponential + L2": "Exponential\nwith penalty",
    "Linear": "Straight line",
    "Linear + poly": "Straight line\nwith curves",
    "Tree": "Decision tree",
    "kNN": "Nearest cases",
}

for theme_name in ("light", "dark"):
    theme = style.use(theme_name)
    fig, ax = plt.subplots(figsize=(15 * style.CM, 9.5 * style.CM))
    x = np.arange(len(ORDER))
    vals = [means[k] for k in ORDER]
    errs = [spreads[k] for k in ORDER]
    colours = [style.GREY if k == "baseline" else style.BLUE for k in ORDER]
    ax.bar(x, vals, width=0.6, color=colours, edgecolor=theme.ink, linewidth=0.5)
    ax.errorbar(x, vals, yerr=errs, fmt="none", ecolor=theme.ink, elinewidth=1.0, capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[k] for k in ORDER], fontsize=8)
    ax.set_ylabel("Average error (litres per 100 km)")
    ax.set_ylim(0, max(v + e for v, e in zip(vals, errs)) * 1.1)
    ax.minorticks_on()
    ax.tick_params(axis="x", which="minor", bottom=False, top=False)
    style.save(fig, OUT, "fig4_cv_comparison", theme)

print("methods:", {k: round(means[k], 3) for k in ORDER})
print("written to", OUT)
