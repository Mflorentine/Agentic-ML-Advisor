"""Sepsis Figure 6: confusion matrix of the recommended configuration on the test patients at the decision
threshold (step 4h).

The four counts are read from the core's single test evaluation; nothing is refitted or recomputed.

Reads   Code/outputs/sepsis/core_final.json   (at_threshold.confusion_matrix, threshold, n_test, test_positives)
Writes  Code/outputs/sepsis/figures/fig6_confusion.png (+ dark/ variant)
        Code/outputs/sepsis/figures/fig6_confusion.json   (the numbers the caption uses)

A 2 x 2 grid, rows = whether the label switched on (actual), columns = whether the patient was flagged
(predicted). Each cell is labelled with its count. No colour shading (user's choice): with 7,572 negatives
and 246 positives, shading would mostly show the class sizes.

Run:    cd Code && uv run python sepsis_14_fig6_confusion.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
vs.FIGURES = OUT / "figures"
NAME = "fig6_confusion"


def draw(d: dict, theme_name: str) -> None:
    t = vs.use(theme_name)
    cm = d["at_threshold"]["confusion_matrix"]
    cells = {(0, 0): ("Flagged, label switched on", cm["tp"]), (0, 1): ("Not flagged, label switched on", cm["fn"]),
             (1, 0): ("Flagged, label did not switch on", cm["fp"]), (1, 1): ("Not flagged, label did not switch on", cm["tn"])}
    fig, ax = plt.subplots(figsize=(10, 6.4))
    ax.grid(False)
    for (r, c), (text, n) in cells.items():
        ax.add_patch(plt.Rectangle((c, 1 - r), 1, 1, fill=False, edgecolor=t.baseline, linewidth=1.5))
        ax.text(c + 0.5, 1 - r + 0.56, f"{n:,}", ha="center", va="center", fontsize=30, fontweight="bold",
                color=t.text_primary)
        ax.text(c + 0.5, 1 - r + 0.28, text, ha="center", va="center", fontsize=vs.ANNOT, color=t.text_secondary)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([0.5, 1.5], ["Flagged", "Not flagged"])
    ax.set_yticks([1.5, 0.5], [f"Switched on\n({cm['tp'] + cm['fn']:,})", f"Did not\n({cm['fp'] + cm['tn']:,})"])
    ax.set_xlabel(f"Prediction at threshold {d['threshold']:.3f}")
    ax.set_ylabel("Sepsis label")
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    vs.header(fig, f"Test patients by prediction and outcome ({d['n_test']:,} patients)")
    vs.layout(fig)
    vs.save(fig, NAME)


if __name__ == "__main__":
    data = json.loads((OUT / "core_final.json").read_text(encoding="utf-8"))
    cm = data["at_threshold"]["confusion_matrix"]
    assert cm["tp"] + cm["fn"] == data["test_positives"] and sum(cm.values()) == data["n_test"]
    for name in ("light", "dark"):
        draw(data, name)
    nums = {"source": "core_final.json", "core_version_sha256": data["core_version_sha256"],
            "threshold": data["threshold"], "n_test": data["n_test"], "test_positives": data["test_positives"],
            "confusion_matrix": cm, "flagged": cm["tp"] + cm["fp"]}
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(nums, indent=2), encoding="utf-8")
    print(json.dumps(nums, indent=2))
