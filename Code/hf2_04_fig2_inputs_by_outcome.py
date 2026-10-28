"""Heart Failure rerun Figure 2: each of the 6 numerical inputs for the training patients who died during follow-up
and for those who did not: one box plot per group with every patient drawn as a point on top (user, step 3).

Reads   the training patients through Code/hf2/core.py training_data() (the 60 test rows are never read)
Writes  Code/outputs/hf2/figures/fig2_inputs_by_outcome.png (+ dark/ variant), fig2_inputs_by_outcome.json

Box: median line, box from the 25th to the 75th percentile, whiskers to the most extreme value within 1.5 x the
box height (matplotlib's default). Points: every patient, spread sideways at random (seed 2026) only so that they
do not overlap; the sideways position carries no information. Colour: series 0 (blue) no death, series 1 (orange)
died, in every figure of this analysis that splits by outcome. No fitted line.

Run:    cd Code && uv run python hf2_04_fig2_inputs_by_outcome.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import viz_style as vs
from hf2 import core

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"
vs.FIGURES = OUT / "figures"
NAME = "fig2_inputs_by_outcome"
FIGSIZE = (15, 9.5)
JITTER_SEED = 2026
UNITS = {"age": "years", "creatinine_phosphokinase": "mcg/L", "ejection_fraction": "%", "platelets": "as recorded",
         "serum_creatinine": "mg/dL", "serum_sodium": "mEq/L"}
GROUPS = [(0, "No death"), (1, "Died")]


def draw(X: pd.DataFrame, y: pd.Series, theme: str) -> None:
    t = vs.use(theme)
    colours = {0: t.series[0], 1: t.series[1]}
    rng = np.random.default_rng(JITTER_SEED)
    fig, axes = plt.subplots(2, 3, figsize=FIGSIZE)
    for ax, col in zip(axes.flat, core.NUMERICAL):
        data = [X.loc[y == g, col].to_numpy() for g, _ in GROUPS]
        bp = ax.boxplot(data, positions=[0, 1], widths=0.5, patch_artist=True, showfliers=False,
                        medianprops={"color": t.text_primary, "linewidth": 2},
                        whiskerprops={"color": t.text_secondary}, capprops={"color": t.text_secondary})
        for patch, (g, _) in zip(bp["boxes"], GROUPS):
            patch.set_facecolor(colours[g]); patch.set_alpha(0.35); patch.set_edgecolor(colours[g])
        for i, (g, _) in enumerate(GROUPS):
            ax.scatter(i + rng.uniform(-0.18, 0.18, len(data[i])), data[i], s=14, color=colours[g], alpha=0.75,
                       linewidths=0)
        ax.set_xticks([0, 1], [f"{lab}\n(n = {len(d)})" for (_, lab), d in zip(GROUPS, data)])
        ax.set_title(f"{col} ({UNITS[col]})", fontsize=14, color=t.text_primary, loc="left")
        ax.grid(axis="x", visible=False)
        ax.tick_params(labelsize=11)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}" if abs(v) >= 10000 else f"{v:,.4g}"))
    vs.header(fig, f"Numerical inputs by outcome, {len(X)} training patients")
    vs.layout(fig, top=0.92)
    vs.save(fig, NAME)


def main() -> None:
    X, y = core.training_data()
    summary = {"rows": "training patients only", "n_train": int(len(X)),
               "groups": {lab: int((y == g).sum()) for g, lab in GROUPS},
               "medians": {c: {lab: float(X.loc[y == g, c].median()) for g, lab in GROUPS} for c in core.NUMERICAL},
               "quartiles": {c: {lab: [float(X.loc[y == g, c].quantile(q)) for q in (0.25, 0.75)] for g, lab in GROUPS}
                             for c in core.NUMERICAL}}
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(X, y, theme)


if __name__ == "__main__":
    main()
