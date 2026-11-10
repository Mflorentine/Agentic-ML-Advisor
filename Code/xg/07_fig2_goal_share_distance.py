"""xG analysis, step 3, Figure 2: share of training shots that scored, by distance to goal.

Two panels sharing the distance axis. Top: share of shots in each 2-unit distance band that
scored (coral). Bottom: number of shots in each band (grey), so the reader sees how much data lies
behind each share. Shots 40 units or more from goal are pooled in one final band.
Distance is the input of DR-13 (Code/xg/features.py), in StatsBomb pitch units.

Reads   Code/outputs/xg/split/inputs_train.csv (training shots only)
Writes  Code/outputs/xg/figures/fig2_goal_share_distance.png and figures/dark/...
        Code/outputs/xg/figures/fig2_numbers.csv  (shots, goals and share per band; quoted in the text)

Run:  cd Code && uv run python xg/07_fig2_goal_share_distance.py
"""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xg_style as st  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
INPUTS = os.path.join(HERE, "..", "outputs", "xg", "split", "inputs_train.csv")
BAND = 2.0
POOL_FROM = 40.0


def main() -> None:
    d = pd.read_csv(INPUTS)
    edges = np.arange(0, POOL_FROM + BAND, BAND)
    lower = np.minimum(np.floor(d.distance / BAND) * BAND, POOL_FROM)
    g = d.assign(band=lower).groupby("band").agg(shots=("goal", "size"), goals=("goal", "sum")).reindex(edges, fill_value=0)
    g["share"] = g.goals / g.shots.where(g.shots > 0)
    g.index.name = "band_from"
    g.to_csv(os.path.join(st.FIGURES, "fig2_numbers.csv"))
    centres = g.index + BAND / 2
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, (a1, a2) = plt.subplots(2, 1, figsize=(10 * st.CM, 8 * st.CM), sharex=True,
                                     gridspec_kw={"height_ratios": [2, 1]})
        a1.bar(centres, g.share, width=BAND * 0.85, color=st.GOAL)
        a1.set_ylabel("Share scored")
        a1.set_ylim(0, 1)
        a2.bar(centres, g.shots, width=BAND * 0.85, color=t.no_goal)
        a2.set_ylabel("Shots")
        a2.set_xlabel("Distance to goal (pitch units)")
        a2.set_xticks(list(range(0, 31, 10)) + [POOL_FROM + BAND / 2])
        a2.set_xticklabels([str(v) for v in range(0, 31, 10)] + ["40+"])
        a2.xaxis.set_minor_locator(plt.MultipleLocator(BAND))
        print(st.save(fig, "fig2_goal_share_distance", t))


if __name__ == "__main__":
    main()
