"""xG analysis, step 4f', Figure 7 (sub-task 2): held-out learning curves with and without team.

Held-out log-loss against the share of training matches used (10 % to 100 %), averaged over the ten
outer folds, for the recommended sub-task 1 model (blue, without team) and the recommended sub-task 2
model (rose, dashed, with team). Same folds, same match subsets (core interpretation l).

Reads only core_recommend_subtask1.json and core_recommend_subtask2.json (learning curves written by the
core). Writes Code/outputs/xg/figures/fig_learning_curves_team.png and figures/dark/...

Run:  cd Code && uv run python xg/13_fig_learning_curves_team.py
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
    lc1 = json.load(open(os.path.join(OUT, "core_recommend_subtask1.json")))["learning_curve"]
    lc2 = json.load(open(os.path.join(OUT, "core_recommend_subtask2.json")))["learning_curve"]
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, ax = plt.subplots(figsize=(10 * st.CM, 8 * st.CM))
        ax.plot([100 * p["fraction"] for p in lc1], [p["logloss_val_mean"] for p in lc1], marker="o", color=st.MODEL, label="Without team")
        ax.plot([100 * p["fraction"] for p in lc2], [p["logloss_val_mean"] for p in lc2], marker="o", color=st.TEAM, linestyle="--", label="With team")
        ax.set_xlabel("Training matches used (%)")
        ax.set_ylabel("Held-out log-loss")
        ax.set_xlim(0, 105)
        ax.legend(loc="upper right")
        print(st.save(fig, "fig_learning_curves_team", t))


if __name__ == "__main__":
    main()
