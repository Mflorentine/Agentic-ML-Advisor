"""Heart Failure rerun Figure 5: learning curve of the recommended configuration (Logistic): training and validation
misclassification rate (at r = 0.5) against the share of each outer training fold used, with the fold SD of the
validation error as error bars (step 4h).

Reads   Code/outputs/hf2/core_recommend.json   (learning_curve, written by the core; nothing is recomputed)
Writes  Code/outputs/hf2/figures/fig5_learning_curve.png (+ dark/ variant), fig5_learning_curve.json

Colour: validation error in the model colour (purple), training error in a lighter purple. Points are the
observations; the lines only join them.

Run:    cd Code && uv run python hf2_09_fig5_learning_curve.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"
vs.FIGURES = OUT / "figures"
NAME = "fig5_learning_curve"
FIGSIZE = (12, 6.5)
MODEL_COLOUR = {"light": "#7a4fd6", "dark": "#9b7af0"}
TRAIN_COLOUR = {"light": "#b9a3ec", "dark": "#5e4a99"}
OUTER_TRAIN = 215   # patients in each outer training fold at 100 % (239 x 9/10, rounded)


def draw(points: list[dict], theme: str) -> None:
    t = vs.use(theme)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = [100 * p["fraction"] for p in points]
    ax.errorbar(x, [p["e_val_mean"] for p in points], yerr=[p["e_val_fold_sd"] for p in points],
                color=MODEL_COLOUR[theme], marker="o", markersize=7, capsize=4, label="Validation error")
    ax.plot(x, [p["e_train_mean"] for p in points], color=TRAIN_COLOUR[theme], marker="o", markersize=7,
            label="Training error")
    ax.set_xticks(x, [f"{v:.0f} %" for v in x])
    ax.set_xlabel(f"Share of each outer training fold used (100 % ≈ {OUTER_TRAIN} patients)")
    ax.set_ylabel("Misclassification rate (threshold 0.5)")
    ax.set_ylim(0, None)
    ax.legend(loc="lower right")
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
