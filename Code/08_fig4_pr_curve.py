"""Figure 4: precision-recall curve of the recommended tree on the 60 test patients.

Reads   Code/outputs/core_final.json  (the curve points, operating point and counts saved by the
        single test evaluation; nothing is refitted or recomputed here)
Writes  Code/outputs/figures/fig4_pr_curve.png (+ dark/ variant)

The tree gives only a few distinct probabilities, so the curve is a step line with a marker at
each achievable threshold. Marked: the tree's operating point (r = 0.2) and the flag-everyone
point. The dashed line is the precision of a random classifier, the share of deaths (p. 92).

Run:    cd Code && uv run python 08_fig4_pr_curve.py
"""
import json
from pathlib import Path

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt

import viz_style as vs

FINAL = Path(__file__).resolve().parent / "outputs" / "core_final.json"
TREE_COLOUR = 2   # palette slot 3: blue and orange already mean "did not die" / "died"


def draw(res: dict, theme_name: str) -> None:
    t = vs.use(theme_name)
    pr = res["pr_curve"]
    precision, recall = pr["precision"], pr["recall"]
    share = res["test_positives"] / res["n_test"]
    op = (res["test_recall"], res["test_precision"])
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axhline(share, color=t.muted, lw=1.4, ls="--", zorder=1,
               label=f"Random classifier (precision = share who died, {share:.2f})")
    ax.plot(recall, precision, drawstyle="steps-post", color=t.series[TREE_COLOUR], lw=2.4, zorder=2,
            label="Tree, test patients")
    # one marker per achievable threshold; the last point (recall 0, precision 1) is a plotting convention
    ax.scatter(recall[:-1], precision[:-1], s=46, color=t.series[TREE_COLOUR], zorder=3)
    halo = [pe.withStroke(linewidth=2.6, foreground=t.surface)]
    for (x, y), text, offset in [(op, f"Tree at r = {res['threshold']:g}\n(recall {op[0]:.2f}, precision {op[1]:.2f})", (-290, -120)),
                                 ((1.0, share), f"Flag everyone\n(recall 1, precision {share:.2f})", (-160, -70))]:
        ax.annotate(text, (x, y), textcoords="offset points", xytext=offset, fontsize=vs.ANNOT,
                    color=t.text_secondary, path_effects=halo, zorder=5, ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.8, color=t.muted, shrinkA=1, shrinkB=6))
        ax.scatter([x], [y], s=150, facecolor="none", edgecolors=t.text_primary, linewidths=1.3, zorder=4)
    ax.set_xlim(0, 1.04)
    ax.set_ylim(0, 1.06)
    ax.set_xlabel("Recall (share of deaths flagged)")
    ax.set_ylabel("Precision (share of flagged patients who died)")
    ax.legend(loc="upper right")
    vs.header(fig, f"Precision and recall of the tree, {res['n_test']} test patients")
    vs.layout(fig)
    vs.save(fig, "fig4_pr_curve")


if __name__ == "__main__":
    result = json.loads(FINAL.read_text(encoding="utf-8"))
    for name in ("light", "dark"):
        draw(result, name)
