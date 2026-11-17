"""Step 4f, Figure 5: learning curve of the nearest-cases method on the ten training parts.

Reads only the approved learning-check results (outputs/Auto_MPG/core_recommend.json). Draws no new model.
Each line is the error on held-back cars when the method is trained on a share of the training cars
(10 % to 100 %); the shaded band is the spread across the ten parts. Training cars only.
Writes a light and a dark version.
Run from Code/:  uv run python Auto_MPG/09_fig5_learning_curve.py
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
curve = np.array(res["C3"]["learning_curve"]["curve (parts by fractions)"])  # parts x fractions
fractions = np.round(np.arange(0.1, 1.01, 0.1) * 100).astype(int)
mean = curve.mean(axis=0)
sd = curve.std(axis=0, ddof=1)

for theme_name in ("light", "dark"):
    theme = style.use(theme_name)
    fig, ax = plt.subplots(figsize=(15 * style.CM, 9.5 * style.CM))
    ax.fill_between(fractions, mean - sd, mean + sd, color=style.BLUE, alpha=0.25, linewidth=0)
    ax.plot(fractions, mean, color=style.BLUE, linewidth=1.6, marker="o", markersize=4, markeredgecolor=theme.ink, markeredgewidth=0.4)
    ax.set_xlabel("Share of the training cars used for learning (%)")
    ax.set_ylabel("Error on held-back cars (litres per 100 km)")
    ax.set_xticks(fractions[::2])
    ax.minorticks_on()
    ax.tick_params(axis="x", which="minor", bottom=False, top=False)
    style.save(fig, OUT, "fig5_learning_curve", theme)

print("mean error by share:", dict(zip(fractions.tolist(), np.round(mean, 3).tolist())))
print("written to", OUT)
