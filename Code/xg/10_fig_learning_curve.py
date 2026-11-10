"""xG analysis, step 4f', Figure 4: learning curve of the recommended configuration (sub-task 1).

Log-loss on the training shots used (coral, dashed) and on the held-out fold (lavender), against the share of
training matches used, 10 % to 100 %, averaged over the 10 outer folds (SML p. 334). Matches are
sampled whole at each share; the hyperparameters are those tuned in each outer fold (core
interpretation l).

Reads only Code/outputs/xg/core_recommend_subtask1.json (written by the core; nothing is refitted here)
Writes Code/outputs/xg/figures/fig_learning_curve_subtask1.png and figures/dark/...

Run:  cd Code && uv run python xg/10_fig_learning_curve.py
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xg_style as st  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs", "xg")


def main() -> None:
    rec = json.load(open(os.path.join(OUT, "core_recommend_subtask1.json")))
    pts = rec["learning_curve"]
    x = [100 * p["fraction"] for p in pts]
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, ax = plt.subplots(figsize=(10 * st.CM, 8 * st.CM))
        ax.plot(x, [p["logloss_val_mean"] for p in pts], marker="o", markersize=4, color=st.HELD_OUT, label="Held-out matches")
        ax.plot(x, [p["logloss_train_mean"] for p in pts], marker="o", markersize=4, color=st.TRAIN, linestyle="--", label="Training matches")
        ax.set_xlabel("Training matches used (%)")
        ax.set_ylabel("Log-loss")
        ax.set_xlim(0, 105)
        ax.xaxis.set_minor_locator(plt.MultipleLocator(10))
        ax.legend(loc="upper right")
        print(st.save(fig, "fig_learning_curve_subtask1", t))


if __name__ == "__main__":
    main()
