"""Mobile Price Figure 4: confusion matrix of the recommended configuration on the 400 test phones (true band in rows,
predicted band in columns), with the number of phones in each cell.

Reads   Code/outputs/mobile/core_final.json   (confusion_test, written by the core's single test evaluation; nothing
        is recomputed here)
Writes  Code/outputs/mobile/figures/fig4_confusion.png (+ dark/ variant), fig4_confusion.json

Colour: one sequential scale of series 0 (blue), from the surface colour at 0 to full blue at the largest cell.

Run:    cd Code && uv run python mobile_09_fig4_confusion.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgb

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "mobile"
vs.FIGURES = OUT / "figures"
NAME = "fig4_confusion"
FIGSIZE = (8.5, 7.5)
BANDS = ["Low", "Medium", "High", "Very high"]


def draw(cm: np.ndarray, theme: str) -> None:
    t = vs.use(theme)
    cmap = LinearSegmentedColormap.from_list("blue", [t.surface, t.series[0]])
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.imshow(cm, cmap=cmap, vmin=0, vmax=cm.max())
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            frac = cm[i, j] / cm.max()
            r, g, b = to_rgb(cmap(frac))
            light_cell = 0.299 * r + 0.587 * g + 0.114 * b > 0.55
            ax.text(j, i, f"{cm[i, j]}", ha="center", va="center", fontsize=18,
                    color="#0b0b0b" if light_cell else "#ffffff")
    ax.set_xticks(range(4), BANDS)
    ax.set_yticks(range(4), BANDS)
    ax.set_xlabel("Predicted band")
    ax.set_ylabel("True band")
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    vs.header(fig, f"Test phones by true and predicted band (n = {int(cm.sum())})")
    vs.layout(fig, top=0.90)
    vs.save(fig, NAME)


def main() -> None:
    data = json.loads((OUT / "core_final.json").read_text(encoding="utf-8"))
    cm = np.asarray(data["confusion_test"], dtype=int)
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps(
        {"source": "core_final.json", "core_version_sha256": data["core_version_sha256"], "n_test": data["n_test"],
         "confusion_test": cm.tolist(), "correct": int(np.trace(cm))}, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(cm, theme)


if __name__ == "__main__":
    main()
