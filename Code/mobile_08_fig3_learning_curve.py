"""Mobile Price Figure 3: learning curve of the recommended configuration (Logistic + L2, lambda grid from 1e-8):
training and validation error (misclassification rate) against the share of each outer training fold used, with
the fold SD of the validation error as error bars.

Reads   Code/outputs/mobile/core_recommend.json   (learning_curve, written by the core; nothing is recomputed here)
Writes  Code/outputs/mobile/figures/fig3_learning_curve.png (+ dark/ variant), fig3_learning_curve.json

Colour: validation error series 0 (blue), training error series 1 (orange), in every Mobile Price figure that
shows both. Observations are the points; the lines only join them.

Run:    cd Code && uv run python mobile_08_fig3_learning_curve.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "mobile"
vs.FIGURES = OUT / "figures"
NAME = "fig3_learning_curve"
FIGSIZE = (12, 6.5)
OUTER_TRAIN = 1440   # phones in each outer training fold (1,600 x 9/10); the 100 % point


def draw(points: list[dict], theme: str) -> None:
    t = vs.use(theme)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = [100 * p["fraction"] for p in points]
    ax.errorbar(x, [p["e_val_mean"] for p in points], yerr=[p["e_val_fold_sd"] for p in points],
                color=t.series[0], marker="o", markersize=7, capsize=4, label="Validation error")
    ax.plot(x, [p["e_train_mean"] for p in points], color=t.series[1], marker="o", markersize=7,
            label="Training error")
    ax.set_xticks(x, [f"{v:.0f} %" for v in x])
    ax.set_xlabel(f"Share of each outer training fold used (100 % = {OUTER_TRAIN:,} phones)")
    ax.set_ylabel("Misclassification rate")
    ax.set_ylim(0, None)
    ax.legend(loc="upper right")
    vs.header(fig, "Learning curve, recommended configuration")
    vs.layout(fig, top=0.90)
    vs.save(fig, NAME)


def main() -> None:
    rec = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
    points = rec["learning_curve"]
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(
        {"source": "core_recommend.json", "core_version_sha256": rec["core_version_sha256"],
         "configuration": rec["recommendation"]["entry"], "points": points, "C3": rec["selection_confidence"]["C3"]},
        indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(points, theme)


if __name__ == "__main__":
    main()
