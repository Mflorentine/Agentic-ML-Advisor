"""Sepsis Figure 1: share of training patients with at least one value of each clinical column in ICU hours 1-6,
by hospital.

Reads   Code/outputs/sepsis/07_train_table.json   (counts from the training patients only; no recomputation)
Writes  Code/outputs/sepsis/figures/fig1_coverage.png (+ dark/ variant)
        Code/outputs/sepsis/figures/fig1_coverage.json   (the numbers the caption uses)

Colours follow the variable, not the rank: hospital A blue (series 0), hospital B orange (series 1), in every
Sepsis figure. Columns are ordered by the share over both hospitals, highest at the top.

Run:    cd Code && uv run python sepsis_08_fig1_coverage.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
vs.FIGURES = OUT / "figures"
NAME = "fig1_coverage"


def draw(d: dict, theme_name: str) -> None:
    t = vs.use(theme_name)
    order = sorted(d["measured_pct"], key=lambda c: d["measured_pct"][c])   # lowest first = bottom of the chart
    y = np.arange(len(order))
    h = 0.38
    fig, ax = plt.subplots(figsize=(12, 13))
    for k, (s, off) in enumerate((("A", h / 2), ("B", -h / 2))):
        vals = [d["measured_pct_by_set"][s][c] for c in order]
        ax.barh(y + off, vals, height=h - 0.04, color=t.series[k],
                label=f"Hospital {s} ({d['patients_by_set'][s]:,} patients)")
    ax.set_yticks(y, order)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f} %"))
    ax.set_xlabel("Training patients with at least one value in ICU hours 1–6")
    ax.grid(axis="y", visible=False)
    ax.set_ylim(-0.7, len(order) - 0.3)
    ax.legend(loc="lower right")
    vs.header(fig, "Measurements taken in the first 6 ICU hours, by hospital")
    vs.layout(fig, top=0.955)
    vs.save(fig, NAME)


if __name__ == "__main__":
    data = json.loads((OUT / "07_train_table.json").read_text(encoding="utf-8"))
    for name in ("light", "dark"):
        draw(data, name)
    caption = {"source": "07_train_table.json", "patients_by_set": data["patients_by_set"],
               "measured_pct": data["measured_pct"], "measured_pct_by_set": data["measured_pct_by_set"]}
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(caption, indent=2), encoding="utf-8")
