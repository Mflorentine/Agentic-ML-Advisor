"""Figure 1: distribution of each numeric input by outcome, training rows only.

Reads   Attachments/heart_failure_clinical_records_dataset.csv, Code/outputs/split.json (train_idx)
Writes  Code/outputs/figures/fig1_numeric_by_outcome.png (+ dark/ variant)

Each panel overlays two histograms: patients who did not die (blue) and who died (orange).
Heights are the share of each group, because the groups differ in size (162 vs 77).
Serum creatinine and creatinine phosphokinase use a log x-axis for display only.

Run:    cd Code && uv run python 03_fig1_numeric_by_outcome.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
import numpy as np
import pandas as pd

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
SPLIT = ROOT / "Code" / "outputs" / "split.json"

LOG_TICKS = {"serum_creatinine": [0.5, 1, 2, 5], "creatinine_phosphokinase": [30, 100, 300, 1000, 3000]}

PANELS = [  # (column, axis label, log x-axis)
    ("age", "Age (years)", False),
    ("ejection_fraction", "Ejection fraction (%)", False),
    ("serum_creatinine", "Serum creatinine (mg/dL, log scale)", True),
    ("serum_sodium", "Serum sodium (mEq/L)", False),
    ("platelets", "Platelets (kiloplatelets/mL)", False),
    ("creatinine_phosphokinase", "CPK (mcg/L, log scale)", True),
]
OUTCOME = {0: ("Did not die", 0), 1: ("Died", 1)}  # label, palette index (fixed per outcome)


def training_rows() -> pd.DataFrame:
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    return pd.read_csv(SRC).iloc[split["train_idx"]]


def draw(df: pd.DataFrame, theme_name: str) -> None:
    t = vs.use(theme_name)
    fig, axes = plt.subplots(2, 3, figsize=(13, 7.6))
    for ax, (col, label, log) in zip(axes.flat, PANELS):
        values = df[col]
        if log:
            bins = np.logspace(np.log10(values.min()), np.log10(values.max()), 16)
            ax.set_xscale("log")
        else:
            bins = np.linspace(values.min(), values.max(), 16)
        for outcome, (name, i) in OUTCOME.items():
            v = values[df["DEATH_EVENT"] == outcome]
            # Outlines, not translucent fills: overlapping fills mix into a colour no legend explains.
            ax.hist(v, bins=bins, weights=np.full(len(v), 1 / len(v)), histtype="step",
                    color=t.series[i], linewidth=2.4, label=f"{name} (n = {len(v)})")
        if log:
            ax.xaxis.set_major_locator(FixedLocator(LOG_TICKS[col]))
            ax.xaxis.set_minor_locator(NullLocator())
            ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
        ax.set_xlabel(label)
        ax.set_ylabel("Share of group")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    vs.header(fig, "Numeric inputs by outcome, training patients")
    vs.layout(fig, top=0.88)
    fig.legend(handles, labels, loc="upper right", ncol=2, bbox_to_anchor=(0.995, 0.955))
    vs.save(fig, "fig1_numeric_by_outcome")


if __name__ == "__main__":
    rows = training_rows()
    for name in ("light", "dark"):
        draw(rows, name)
