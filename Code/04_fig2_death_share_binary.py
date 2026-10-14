"""Figure 2: share of patients who died, within each level of the five yes/no inputs.

Reads   Attachments/heart_failure_clinical_records_dataset.csv, Code/outputs/split.json (train_idx)
Writes  Code/outputs/figures/fig2_death_share_binary.png (+ dark/ variant)

Bars are the share who died (orange, the colour of "died" throughout). The number of
patients in each level is written on its bar; the dashed line is the overall training share.
`sex` is labelled from the step 1 inference: 0 = woman, 1 = man.

Run:    cd Code && uv run python 04_fig2_death_share_binary.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
SPLIT = ROOT / "Code" / "outputs" / "split.json"

INPUTS = [  # (column, label, names of levels 0 and 1)
    ("anaemia", "Anaemia", ("no", "yes")),
    ("diabetes", "Diabetes", ("no", "yes")),
    ("high_blood_pressure", "High blood pressure", ("no", "yes")),
    ("sex", "Sex", ("woman", "man")),
    ("smoking", "Smoking", ("no", "yes")),
]


def training_rows() -> pd.DataFrame:
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    return pd.read_csv(SRC).iloc[split["train_idx"]]


def draw(df: pd.DataFrame, theme_name: str) -> None:
    t = vs.use(theme_name)
    fig, ax = plt.subplots(figsize=(13, 6.4))
    overall = df["DEATH_EVENT"].mean()
    xs, labels, centres = [], [], []
    for i, (col, label, levels) in enumerate(INPUTS):
        for j, level in enumerate((0, 1)):
            group = df[df[col] == level]["DEATH_EVENT"]
            x = i * 3 + j
            share = group.mean()
            ax.bar(x, share, width=0.8, color=t.series[1])
            # Count inside the bar, near its base, so it never meets the reference line.
            ax.text(x, 0.015, f"n = {len(group)}", ha="center", va="bottom",
                    fontsize=vs.ANNOT, color=t.surface, fontweight="bold")
            xs.append(x)
            labels.append(levels[j])
        centres.append(i * 3 + 0.5)
    ax.axhline(overall, color=t.text_secondary, linestyle="--", linewidth=1.4,
               label=f"All training patients ({overall:.1%})")
    ax.set_xticks(xs, labels)
    for c, (_, label, _) in zip(centres, INPUTS):
        ax.text(c, -0.12, label, ha="center", va="top", transform=ax.get_xaxis_transform(),
                fontsize=14, color=t.text_primary)
    ax.set_ylabel("Share who died")
    ax.set_ylim(0, max(0.6, ax.get_ylim()[1]))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper right")
    vs.header(fig, "Share who died, by each yes/no input, training patients")
    vs.layout(fig)
    vs.save(fig, "fig2_death_share_binary")


if __name__ == "__main__":
    rows = training_rows()
    for name in ("light", "dark"):
        draw(rows, name)
