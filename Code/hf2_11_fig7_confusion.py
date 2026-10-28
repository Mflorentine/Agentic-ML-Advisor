"""Heart Failure rerun Figure 7: the 60 test patients by whether they were flagged at the chosen threshold (columns)
and whether they died during follow-up (rows), with the count in each cell (step 4h).

Reads   Code/outputs/hf2/core_final.json   (confusion_test and threshold, written by the core; nothing is recomputed)
Writes  Code/outputs/hf2/figures/fig7_confusion.png (+ dark/ variant), fig7_confusion.json

Colour: one sequential scale of the model colour (purple), from the surface colour at 0 to full purple at the
largest cell.

Run:    cd Code && uv run python hf2_11_fig7_confusion.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgb

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"
vs.FIGURES = OUT / "figures"
NAME = "fig7_confusion"
FIGSIZE = (8, 6.5)
MODEL_COLOUR = {"light": "#7a4fd6", "dark": "#9b7af0"}


def draw(cm: np.ndarray, thr: float, theme: str) -> None:
    t = vs.use(theme)
    cmap = LinearSegmentedColormap.from_list("model", [t.surface, MODEL_COLOUR[theme]])
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.imshow(cm, cmap=cmap, vmin=0, vmax=cm.max())
    for i in range(2):
        for j in range(2):
            r, g, b = to_rgb(cmap(cm[i, j] / cm.max()))
            light = 0.299 * r + 0.587 * g + 0.114 * b > 0.55
            ax.text(j, i, f"{cm[i, j]}", ha="center", va="center", fontsize=22, color="#0b0b0b" if light else "#ffffff")
    ax.set_xticks([0, 1], ["Not flagged", "Flagged"])
    ax.set_yticks([0, 1], ["No death", "Died"])
    ax.set_xlabel(f"Prediction at threshold {thr:.2f}")
    ax.set_ylabel("Outcome during follow-up")
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    vs.header(fig, f"Test patients by outcome and flag (n = {int(cm.sum())})")
    vs.layout(fig, top=0.90)
    vs.save(fig, NAME)


def main() -> None:
    final = json.loads((OUT / "core_final.json").read_text(encoding="utf-8"))
    c = final["confusion_test"]
    cm = np.array([[c["tn"], c["fp"]], [c["fn"], c["tp"]]], dtype=int)
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(
        {"source": "core_final.json", "core_version_sha256": final["core_version_sha256"], "threshold": final["threshold"],
         "n_test": final["n_test"], "confusion_test": c, "flagged": c["tp"] + c["fp"]}, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(cm, final["threshold"], theme)


if __name__ == "__main__":
    main()
