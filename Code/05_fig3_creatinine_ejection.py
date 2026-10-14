"""Figure 3: serum creatinine against ejection fraction, coloured by outcome, training rows only.

Reads   Attachments/heart_failure_clinical_records_dataset.csv, Code/outputs/split.json (train_idx)
Writes  Code/outputs/figures/fig3_creatinine_ejection.png (+ dark/ variant)

One point per training patient: blue did not die, orange died. Serum creatinine on a log
x-axis for display only. Ejection fraction takes only 16 distinct values in the training rows, so points overlap;
transparency shows where they stack. This figure is for looking only; it does not set P8.

Run:    cd Code && uv run python 05_fig3_creatinine_ejection.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
import pandas as pd

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
SPLIT = ROOT / "Code" / "outputs" / "split.json"
OUTCOME = {0: ("Did not die", 0), 1: ("Died", 1)}


def training_rows() -> pd.DataFrame:
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    return pd.read_csv(SRC).iloc[split["train_idx"]]


def draw(df: pd.DataFrame, theme_name: str) -> None:
    t = vs.use(theme_name)
    fig, ax = plt.subplots(figsize=(11, 7))
    for outcome, (name, i) in OUTCOME.items():
        d = df[df["DEATH_EVENT"] == outcome]
        ax.scatter(d["serum_creatinine"], d["ejection_fraction"], s=46, color=t.series[i],
                   alpha=0.6, edgecolors=t.surface, linewidths=0.5, label=f"{name} (n = {len(d)})")
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator([0.5, 1, 2, 5, 10]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("Serum creatinine (mg/dL, log scale)")
    ax.set_ylabel("Ejection fraction (%)")
    ax.legend(loc="upper right")
    vs.header(fig, "Serum creatinine and ejection fraction, training patients")
    vs.layout(fig)
    vs.save(fig, "fig3_creatinine_ejection")


if __name__ == "__main__":
    rows = training_rows()
    for name in ("light", "dark"):
        draw(rows, name)
