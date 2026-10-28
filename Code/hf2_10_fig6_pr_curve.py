"""Heart Failure rerun Figure 6: precision-recall curve of the recommended configuration on the 60 test patients
(step 4h).

Reads   Code/outputs/hf2/core_test_predictions.csv   (the probabilities saved by the core's single test evaluation)
        Code/outputs/hf2/core_final.json             (PR-AUC, share of deaths, threshold, precision and recall at it)
Writes  Code/outputs/hf2/figures/fig6_pr_curve.png (+ dark/ variant), fig6_pr_curve.json

The curve is traced from the saved probabilities (no model is refitted): at each distinct score where recall rises,
the precision and recall of flagging every patient at or above it, drawn as a step function, the interpolation that average precision
(the PR-AUC used here, DR-05) integrates. The reported numbers (PR-AUC, the point at the threshold) are read from
core_final.json, not recomputed. Grey line: the share of deaths, the precision of flagging at random and the PR-AUC
of flagging nobody. The marked point is the chosen threshold, joined to its label by a leader line. Colour: the model
colour (purple).

Run:    cd Code && uv run python hf2_10_fig6_pr_curve.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"
vs.FIGURES = OUT / "figures"
NAME = "fig6_pr_curve"
FIGSIZE = (10, 8)
MODEL_COLOUR = {"light": "#7a4fd6", "dark": "#9b7af0"}


def curve(y: np.ndarray, p: np.ndarray) -> tuple[list[float], list[float]]:
    rec, prec = [0.0], [1.0]                                   # by convention the curve starts at (0, 1)
    for s in np.unique(p)[::-1]:
        flagged = p >= s
        tp = int((flagged & (y == 1)).sum())
        r = tp / int(y.sum())
        if r > rec[-1]:                                        # only points where recall rises: the ones average
            rec.append(r)                                      # precision counts; points at unchanged recall add
            prec.append(tp / int(flagged.sum()))               # nothing to the area and are not drawn
    return rec, prec


def draw(rec, prec, final: dict, theme: str) -> None:
    t = vs.use(theme)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.step(rec, prec, where="pre", color=MODEL_COLOUR[theme], linewidth=2.2, label="Logistic (test patients)")
    ax.axhline(final["test_positive_rate"], color=t.baseline, linewidth=1.5,
               label=f"share of deaths ({final['test_positive_rate']:.2f})")
    pt = final["at_threshold"]
    ax.plot(pt["recall"], pt["precision"], "o", markersize=10, color=MODEL_COLOUR[theme],
            markeredgecolor=t.text_primary, markeredgewidth=1.2, zorder=5)
    ax.annotate(f"threshold {final['threshold']:.2f}", xy=(pt["recall"], pt["precision"]),
                xytext=(pt["recall"] - 0.32, pt["precision"] - 0.17), fontsize=vs.ANNOT, color=t.text_primary,
                arrowprops={"arrowstyle": "-", "color": t.text_secondary, "linewidth": 1.2})
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Recall (share of deaths flagged)")
    ax.set_ylabel("Precision (share of flagged who died)")
    ax.legend(loc="upper right")
    vs.header(fig, f"Precision–recall curve, {final['n_test']} test patients")
    vs.layout(fig, top=0.92)
    vs.save(fig, NAME)


def main() -> None:
    final = json.loads((OUT / "core_final.json").read_text(encoding="utf-8"))
    pred = pd.read_csv(OUT / "core_test_predictions.csv", float_precision="round_trip")
    rec, prec = curve(pred["y"].to_numpy(), pred["p"].to_numpy())
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(
        {"source": "core_final.json, core_test_predictions.csv", "core_version_sha256": final["core_version_sha256"],
         "n_test": final["n_test"], "test_positives": final["test_positives"], "test_pr_auc": final["test_pr_auc"],
         "share_of_deaths": final["test_positive_rate"], "threshold": final["threshold"],
         "at_threshold": final["at_threshold"], "curve_points": len(rec)}, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(rec, prec, final, theme)


if __name__ == "__main__":
    main()
