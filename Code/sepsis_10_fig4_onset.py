"""Sepsis Figure 4: the ICU hour at which SepsisLabel switches on, for the training positives, by hospital.

A positive is a patient whose label switches on at ICU hour 7-54 (DR-05). The label switches on 6 hours before
the estimated Sepsis-3 onset (DR-01), so hour h on the axis is onset at hour h + 6; that is said in the caption,
not drawn as a second axis.

Reads   Code/outputs/sepsis/07_train_table.json   (counts per hour, training positives only; no recomputation)
Writes  Code/outputs/sepsis/figures/fig4_onset.png (+ dark/ variant)
        Code/outputs/sepsis/figures/fig4_onset.json   (the numbers the caption uses)

One line per hospital, the number of training positives whose label switches on in each hour. Hospital A blue,
hospital B orange, as in Figure 1. Hours with no positive are drawn as 0.

Run:    cd Code && uv run python sepsis_10_fig4_onset.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
vs.FIGURES = OUT / "figures"
NAME = "fig4_onset"
HOURS = np.arange(7, 55)   # ICU hours 7-54 (DR-05)


def counts(d: dict, s: str) -> np.ndarray:
    c = d["positive_label_onset_iculos_counts_by_set"][s]
    assert all(7 <= float(h) <= 54 for h in c)
    return np.array([c.get(str(float(h)), 0) for h in HOURS])


def draw(d: dict, theme_name: str) -> None:
    t = vs.use(theme_name)
    fig, ax = plt.subplots(figsize=(13, 6.2))
    for k, s in enumerate(("A", "B")):
        n = counts(d, s)
        ax.plot(HOURS, n, color=t.series[k], marker="o", markersize=5,
                label=f"Hospital {s} ({n.sum():,} positives)")
    ax.set_xlim(6, 55)
    ax.set_xticks([7, 12, 18, 24, 30, 36, 42, 48, 54])
    ax.set_ylim(0, None)
    ax.set_xlabel("ICU hour at which the sepsis label switches on")
    ax.set_ylabel("Training positives")
    ax.legend(loc="upper right")
    vs.header(fig, "When the sepsis label switches on, training positives, by hospital")
    vs.layout(fig)
    vs.save(fig, NAME)


if __name__ == "__main__":
    data = json.loads((OUT / "07_train_table.json").read_text(encoding="utf-8"))
    for name in ("light", "dark"):
        draw(data, name)
    nums = {}
    for s in ("A", "B"):
        n = counts(data, s)
        hours = np.repeat(HOURS, n)
        nums[s] = {"positives": int(n.sum()), "median_hour": float(np.median(hours)),
                   "quartiles": [float(q) for q in np.percentile(hours, [25, 75])],
                   "hour_with_most": int(HOURS[n.argmax()]), "most": int(n.max())}
    allh = np.repeat(HOURS, counts(data, "A") + counts(data, "B"))
    nums["all"] = {"positives": int(len(allh)), "median_hour": float(np.median(allh)),
                   "quartiles": [float(q) for q in np.percentile(allh, [25, 75])],
                   "share_hours_7_to_12_pct": round(100 * float((allh <= 12).mean()), 1)}
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(nums, indent=2), encoding="utf-8")
    print(json.dumps(nums, indent=2))
