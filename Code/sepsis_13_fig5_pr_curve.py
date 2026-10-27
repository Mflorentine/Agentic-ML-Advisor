"""Sepsis Figure 5: precision-recall curve of the recommended configuration on the test patients (step 4h).

The curve, the no-skill level and the point at the decision threshold are read from the core's single test
evaluation; nothing is refitted or recomputed (instructions.md, step 3 rules for figures).

Reads   Code/outputs/sepsis/core_final.json   (pr_curve, test_positive_rate, at_threshold, threshold, test_pr_auc)
Writes  Code/outputs/sepsis/figures/fig5_pr_curve.png (+ dark/ variant)
        Code/outputs/sepsis/figures/fig5_pr_curve.json   (the numbers the caption uses)

Recall on the x-axis, precision on the y-axis, both 0-1 (user's choice: linear axes). The curve is drawn as a
step function, the interpolation that average precision (the PR-AUC used here, DR-05) integrates. Grey line:
precision of the no-skill level, the test positive rate, which is also the PR-AUC of flagging nobody. The model
has its own colour (purple), not one of the hospital colours of Figures 1-4.

Run:    cd Code && uv run python sepsis_13_fig5_pr_curve.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
vs.FIGURES = OUT / "figures"
NAME = "fig5_pr_curve"
MODEL_COLOUR = {"light": "#7a4fd6", "dark": "#9b7af0"}   # the recommended model, in every evaluation figure


def draw(d: dict, theme_name: str) -> None:
    t = vs.use(theme_name)
    pr, at = d["pr_curve"], d["at_threshold"]
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.axhline(d["test_positive_rate"], color=t.muted, linewidth=2.0,             # neutral grey, visible in both themes
               label=f"No skill: test positive rate {d['test_positive_rate']:.4f}")
    ax.step(pr["recall"], pr["precision"], where="post", color=MODEL_COLOUR[theme_name], linewidth=2.2,
            label=f"{d['configuration']} (PR-AUC {d['test_pr_auc']:.4f})")
    x, y = at["recall"], at["precision"]
    ax.plot([x], [y], marker="o", markersize=10, color=MODEL_COLOUR[theme_name],
            markeredgecolor=t.text_primary, zorder=5)
    ax.annotate(f"Threshold {d['threshold']:.3f}\nrecall {x:.4f}, precision {y:.4f}", xy=(x, y),
                xytext=(0.60, 0.42), textcoords="axes fraction", fontsize=vs.ANNOT, color=t.text_primary,
                arrowprops={"arrowstyle": "-", "color": t.text_secondary, "linewidth": 1.2})
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.legend(loc="upper right")
    vs.header(fig, f"Precision and recall on the {d['n_test']:,} test patients")
    vs.layout(fig)
    vs.save(fig, NAME)


if __name__ == "__main__":
    data = json.loads((OUT / "core_final.json").read_text(encoding="utf-8"))
    for name in ("light", "dark"):
        draw(data, name)
    nums = {"source": "core_final.json", "core_version_sha256": data["core_version_sha256"],
            "configuration": data["configuration"], "n_test": data["n_test"],
            "test_positives": data["test_positives"], "test_pr_auc": data["test_pr_auc"],
            "test_positive_rate": data["test_positive_rate"], "threshold": data["threshold"],
            "recall_at_threshold": data["at_threshold"]["recall"],
            "precision_at_threshold": data["at_threshold"]["precision"],
            "curve_points": len(data["pr_curve"]["recall"])}
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(nums, indent=2), encoding="utf-8")
    print(json.dumps(nums, indent=2))
