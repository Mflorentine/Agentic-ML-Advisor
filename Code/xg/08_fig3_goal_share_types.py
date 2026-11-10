"""xG analysis, step 3, Figure 3: share of training shots that scored, by type of shot.

Four panels of horizontal bars (coral): body part, technique, how the attack started
(play pattern) and the type of the assisting pass. Each bar is one level; its label gives the
number of training shots at that level. Levels are ordered by number of shots.
16 x 14 cm rather than the default 10 x 8 cm, so that 24 labelled bars stay readable.

Reads   Code/outputs/xg/split/inputs_train.csv (training shots only)
Writes  Code/outputs/xg/figures/fig3_goal_share_types.png and figures/dark/...
        Code/outputs/xg/figures/fig3_numbers.csv  (shots, goals and share per level)

Run:  cd Code && uv run python xg/08_fig3_goal_share_types.py
"""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xg_style as st  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "..", "outputs", "xg", "split", "inputs_train.csv")
PANELS = [("body_part", "Body part"), ("technique", "Technique"),
          ("play_pattern", "How the attack started"), ("key_pass_type", "Assisting pass")]
X_MAX = 0.5  # no level's share exceeds this in the training shots; checked below
LABELS = {"none": "None", "Regular": "Pass", "From Throw In": "From throw-in", "From Free Kick": "From free kick",
          "From Corner": "From corner", "From Counter": "From counter", "From Goal Kick": "From goal kick",
          "From Keeper": "From keeper", "From Kick Off": "From kick-off", "Regular Play": "Regular play"}


def main() -> None:
    d = pd.read_csv(INPUTS)
    tables = []
    for col, title in PANELS:
        g = d.groupby(col).agg(shots=("goal", "size"), goals=("goal", "sum")).sort_values("shots", ascending=False)
        g["share"] = g.goals / g.shots
        tables.append(g.assign(input=col).reset_index().rename(columns={col: "level"}))
    pd.concat(tables)[["input", "level", "shots", "goals", "share"]].to_csv(os.path.join(st.FIGURES, "fig3_numbers.csv"), index=False)
    assert max(g.share.max() for g in tables) <= X_MAX
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, axes = plt.subplots(2, 2, figsize=(16 * st.CM, 14 * st.CM), sharex=True)
        for ax, (col, title), g in zip(axes.flat, PANELS, tables):
            labels = [f"{LABELS.get(v, v[:1].upper() + v[1:].lower())} ({n:,})" for v, n in zip(g.level, g.shots)]
            ax.barh(range(len(g)), g.share, color=st.GOAL, height=0.7)
            ax.set_yticks(range(len(g)))
            ax.set_yticklabels(labels, fontsize=10)
            ax.invert_yaxis()
            ax.set_title(title, loc="left")
            ax.set_xlim(0, X_MAX)
            ax.set_xticks([0, 0.25, 0.5])
        for ax in axes[1]:
            ax.set_xlabel("Share scored")
        print(st.save(fig, "fig3_goal_share_types", t))


if __name__ == "__main__":
    main()
