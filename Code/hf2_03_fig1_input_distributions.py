"""Heart Failure rerun Figure 1: distribution of each of the 6 numerical inputs over the 239 training patients, both
outcomes together (user, step 3). Values as recorded (DR-08: no transformation).

Reads   the training patients through Code/hf2/core.py training_data() (the 60 test rows are never read)
Writes  Code/outputs/hf2/figures/fig1_input_distributions.png (+ dark/ variant), fig1_input_distributions.json

Bars: `ejection_fraction` and `serum_sodium` (whole numbers, few values) get one bar per recorded value. `age` gets
bins one year wide centred on whole years (the two ages of 60.667 fall in the bin of 61). The others get 40
equal-width bins from min to max. Each panel has its own y scale. Colour: series 2 (green), "all training patients",
in every figure of this analysis.

Run:    cd Code && uv run python hf2_03_fig1_input_distributions.py
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
NAME = "fig1_input_distributions"
BINS = 40
FIGSIZE = (15, 9)
UNITS = {"age": "years", "creatinine_phosphokinase": "mcg/L", "ejection_fraction": "%", "platelets": "as recorded",
         "serum_creatinine": "mg/dL", "serum_sodium": "mEq/L"}
ONE_BAR_PER_VALUE = {"ejection_fraction", "serum_sodium"}
assert list(UNITS) == core.NUMERICAL


def bins_for(col: str, v: pd.Series):
    if col == "age":
        return np.arange(np.floor(v.min()) - 0.5, np.ceil(v.max()) + 1.5, 1.0), "1-year bins centred on whole years"
    return np.linspace(v.min(), v.max(), BINS + 1), f"{BINS} equal-width bins from min to max"


def draw(X: pd.DataFrame, theme: str) -> None:
    t = vs.use(theme)
    fig, axes = plt.subplots(2, 3, figsize=FIGSIZE)
    for ax, col in zip(axes.flat, core.NUMERICAL):
        v = X[col]
        if col in ONE_BAR_PER_VALUE:
            counts = v.value_counts().sort_index()
            ax.bar(counts.index, counts.to_numpy(), width=0.8, color=t.series[2], edgecolor=t.surface, linewidth=0.6)
        else:
            ax.hist(v, bins=bins_for(col, v)[0], color=t.series[2], edgecolor=t.surface, linewidth=0.6)
        ax.set_title(f"{col} ({UNITS[col]})", fontsize=14, color=t.text_primary, loc="left")
        ax.grid(axis="x", visible=False)
        ax.tick_params(labelsize=11)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}" if abs(x) >= 10000 else f"{x:,.4g}"))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    for i in (0, 3):
        axes.flat[i].set_ylabel("Patients")
    vs.header(fig, f"Numerical inputs, {len(X)} training patients")
    vs.layout(fig, top=0.92)
    vs.save(fig, NAME)


def main() -> None:
    X, _ = core.training_data()
    summary = {"rows": "training patients only", "n_train": int(len(X)), "panels": {
        c: {"patients": int(X[c].notna().sum()), "distinct": int(X[c].nunique()), "min": float(X[c].min()),
            "median": float(X[c].median()), "max": float(X[c].max()),
            "bars": "one per recorded value" if c in ONE_BAR_PER_VALUE else bins_for(c, X[c])[1], "unit": UNITS[c]}
        for c in core.NUMERICAL}}
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(X, theme)


if __name__ == "__main__":
    main()
