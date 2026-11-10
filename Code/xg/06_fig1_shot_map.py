"""xG analysis, step 3, Figure 1: where the training shots were taken.

Half-pitch in StatsBomb coordinates, seen from behind the shooter with the goal at the top.
Every training shot is a faint grey dot; goals are coral dots drawn on top.

Reads   Code/outputs/xg/split/shots_train.csv (training shots only)
Writes  Code/outputs/xg/figures/fig1_shot_map.png and figures/dark/fig1_shot_map.png
        Code/outputs/xg/figures/fig1_numbers.txt  (counts quoted in the caption)

Run:  cd Code && uv run python xg/06_fig1_shot_map.py
"""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Arc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xg_style as st  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "..", "outputs", "xg", "split", "shots_train.csv")


def pitch(ax, color):
    """Attacking half, StatsBomb coordinates; horizontal = y (0 at the attacker's left), vertical = x."""
    kw = dict(color=color, linewidth=1.0, zorder=1)
    ax.plot([0, 80, 80, 0, 0], [60, 60, 120, 120, 60], **kw)          # half
    ax.plot([18, 18, 62, 62], [120, 102, 102, 120], **kw)             # penalty area
    ax.plot([30, 30, 50, 50], [120, 114, 114, 120], **kw)             # six-yard box
    ax.plot([36, 36, 44, 44], [120, 122, 122, 120], **kw)             # goal
    ax.plot([40], [108], marker="o", markersize=1.5, color=color)     # penalty spot
    ax.add_patch(Arc((40, 108), 20, 20, theta1=233.13, theta2=306.87, **kw))  # penalty arc, r = 10
    ax.add_patch(Arc((40, 60), 20, 20, theta1=0, theta2=180, **kw))   # centre circle, r = 10
    ax.set_xlim(-1, 81)
    ax.set_ylim(59, 123)
    ax.set_aspect("equal")
    ax.axis("off")


def main() -> None:
    s = pd.read_csv(SHOTS)
    goals = s[s.goal == 1]
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, ax = plt.subplots(figsize=(10 * st.CM, 8 * st.CM))
        pitch(ax, t.pitch)
        ax.scatter(s.y, s.x, s=1.0, color=t.no_goal, alpha=0.25, linewidths=0, zorder=2,
                   label=f"All shots ({len(s):,})")
        ax.scatter(goals.y, goals.x, s=1.5, color=st.GOAL, alpha=0.6, linewidths=0, zorder=3,
                   label=f"Goal ({len(goals):,})")
        leg = ax.legend(loc="lower left", markerscale=6, handletextpad=0.2)
        for h in leg.legend_handles:
            h.set_alpha(1)
        print(st.save(fig, "fig1_shot_map", t))
    with open(os.path.join(st.FIGURES, "fig1_numbers.txt"), "w") as f:
        f.write(f"training shots {len(s)}; goals {len(goals)}; share {len(goals) / len(s):.4f}\n")
        f.write(f"shots inside the penalty area (x >= 102, 18 <= y <= 62): {int(((s.x >= 102) & s.y.between(18, 62)).sum())}\n")
        f.write(f"goals inside the penalty area: {int(((goals.x >= 102) & goals.y.between(18, 62)).sum())}\n")


if __name__ == "__main__":
    main()
