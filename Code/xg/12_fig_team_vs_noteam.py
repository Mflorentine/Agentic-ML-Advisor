"""xG analysis, step 4f', Figure 6 (sub-task 2): the team model against the sub-task 1 model, fold by fold.

For each of the ten outer folds (the same matches for both models), the held-out log-loss of the
recommended team model minus that of the recommended sub-task 1 model: positive = the team model is
worse. Dots: the ten folds. Diamond and line: the mean difference and +/- one standard deviation of the
fold differences (the spread), as reported by the core.

Reads only core outputs: core_cv_store_subtask1.json, core_cv_store_subtask2.json (fold scores) and
core_recommend_subtask2.json (the comparison the core reports; the figure checks it reproduces it).
Writes Code/outputs/xg/figures/fig_team_vs_noteam.png and figures/dark/...,
       Code/outputs/xg/figures/fig_team_vs_noteam.csv (the ten fold differences)

Run:  cd Code && uv run python xg/12_fig_team_vs_noteam.py
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xg_style as st  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs", "xg")


def main() -> None:
    cmp = json.load(open(os.path.join(OUT, "core_recommend_subtask2.json")))["subtask2_comparison"]
    s1 = json.load(open(os.path.join(OUT, "core_cv_store_subtask1.json")))["entries"][cmp["subtask1_entry"]]
    s2 = json.load(open(os.path.join(OUT, "core_cv_store_subtask2.json")))["entries"][cmp["subtask2_entry"]]
    ll1 = -np.array([r["neg_logloss_val"] for r in s1["folds"]])
    ll2 = -np.array([r["neg_logloss_val"] for r in s2["folds"]])
    d = ll2 - ll1                                      # positive = team model worse
    assert np.isclose(-d.mean(), cmp["margin"]) and np.isclose(d.std(ddof=1), cmp["spread"])
    pd.DataFrame({"fold": range(1, 11), "logloss_subtask1": ll1, "logloss_team": ll2, "team_minus_subtask1": d}).to_csv(
        os.path.join(st.FIGURES, "fig_team_vs_noteam.csv"), index=False)
    m, s = -cmp["margin"], cmp["spread"]
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, ax = plt.subplots(figsize=(10 * st.CM, 5 * st.CM))
        ax.axvline(0, color=t.no_goal, linewidth=0.8, linestyle=":", zorder=0)
        ax.scatter(d, np.full(len(d), 1.0), color=st.TEAM, s=18, zorder=3, label="Fold")
        ax.errorbar(m, 0.0, xerr=s, fmt="D", color=st.TEAM, capsize=3, markersize=5, linewidth=1.4, label="Mean ± spread")
        ax.set_yticks([1.0, 0.0])
        ax.set_yticklabels(["Folds", "Mean"])
        ax.set_ylim(-0.7, 1.7)
        ax.set_xlabel("Log-loss with team − without team")
        print(st.save(fig, "fig_team_vs_noteam", t))


if __name__ == "__main__":
    main()
