"""Mobile Price Figure 1: distribution of each of the 14 numerical inputs over the 1,600 training phones, all price
bands together (user, step 3). Values as recorded (DR-08: no transformation).

Reads   the training phones through Code/mobile/core.py training_data() (the 400 test rows are never read)
Writes  Code/outputs/mobile/figures/fig1_input_distributions.png (+ dark/ variant)
        Code/outputs/mobile/figures/fig1_input_distributions.json   (per panel: phones, distinct values, min, max, zeros)

Inputs with at most 130 distinct values get one bar per recorded value, so no binning can create a pattern. The
four with about 1,000 values or more (battery_power, px_height, px_width, ram; all whole numbers) get 40 equal-width
bins from min - 0.5 to max + 0.5: each bin holds 37 or 38 possible whole numbers (px_height 49 or 50, ram 93 or 94), so no value is cut
off and no bin is short. Each panel has its own y scale. Colour: series 2 (green), "all training
phones", in every Mobile Price figure. Units are Kaggle's; "unit not given" where Kaggle states none (step 1).

Run:    cd Code && uv run python mobile_03_fig1_input_distributions.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import viz_style as vs
from mobile import core

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "mobile"
vs.FIGURES = OUT / "figures"
NAME = "fig1_input_distributions"
BINS = 40
DISCRETE_MAX = 130
NCOLS = 4
FIGSIZE = (16, 14)

UNITS = {"battery_power": "mAh", "clock_speed": "unit not given", "fc": "megapixels", "int_memory": "GB",
         "m_dep": "cm", "mobile_wt": "unit not given", "n_cores": "count", "pc": "megapixels",
         "px_height": "pixels", "px_width": "pixels", "ram": "MB", "sc_h": "cm", "sc_w": "cm",
         "talk_time": "unit not given"}
assert list(UNITS) == core.NUMERICAL, "panel order must follow the core's numerical inputs"


def integer_bins(values: pd.Series) -> np.ndarray:
    """BINS equal-width bins spanning the whole-number range exactly, edges at min - 0.5 and max + 0.5."""
    assert (values == values.round()).all(), "binned input is not whole-numbered"
    return np.linspace(values.min() - 0.5, values.max() + 0.5, BINS + 1)


def panel(ax, values: pd.Series, col: str, t) -> None:
    distinct = np.sort(values.unique())
    if len(distinct) <= DISCRETE_MAX:
        counts = values.value_counts().reindex(distinct)
        step = float(np.min(np.diff(distinct))) if len(distinct) > 1 else 1.0
        ax.bar(distinct, counts.to_numpy(), width=0.8 * step, color=t.series[2], edgecolor=t.surface,
               linewidth=0.6 if len(distinct) <= 64 else 0)   # no outline on very thin bars
    else:
        ax.hist(values, bins=integer_bins(values), color=t.series[2], edgecolor=t.surface, linewidth=0.6)
    ax.set_title(f"{col} ({UNITS[col]})", fontsize=14, color=t.text_primary, loc="left")
    ax.grid(axis="x", visible=False)
    ax.tick_params(labelsize=11)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.4g}"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))


def draw(X: pd.DataFrame, theme: str) -> None:
    t = vs.use(theme)
    nrows = int(np.ceil(len(core.NUMERICAL) / NCOLS))
    fig, axes = plt.subplots(nrows, NCOLS, figsize=FIGSIZE)
    for ax, col in zip(axes.flat, core.NUMERICAL):
        panel(ax, X[col], col, t)
    for i, ax in enumerate(axes.flat):
        if i >= len(core.NUMERICAL):
            ax.set_visible(False)
        elif i % NCOLS == 0:
            ax.set_ylabel("Phones")
    vs.header(fig, f"Numerical inputs, {len(X):,} training phones")
    vs.layout(fig, top=0.95)
    vs.save(fig, NAME)


def main() -> None:
    X, y = core.training_data()
    summary = {"rows": "training phones only", "n_train": int(len(X)), "panels": {
        c: {"phones": int(X[c].notna().sum()), "distinct": int(X[c].nunique()), "min": float(X[c].min()),
            "max": float(X[c].max()), "zeros": int((X[c] == 0).sum()),
            "bars": "one per value" if X[c].nunique() <= DISCRETE_MAX else
                f"{BINS} equal-width bins of {(X[c].max() - X[c].min() + 1) / BINS:.2f} whole numbers",
            "unit": UNITS[c]} for c in core.NUMERICAL}}
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(X, theme)


if __name__ == "__main__":
    main()
