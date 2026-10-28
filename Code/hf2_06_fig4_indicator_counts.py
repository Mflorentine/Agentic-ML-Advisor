"""Heart Failure rerun Figure 4: how many of the 239 training patients have the value 1 for each of the 5 yes/no
inputs (user, step 3). Describes the patients, not the outcome.

Reads   the training patients through Code/hf2/core.py training_data() (the 60 test rows are never read)
Writes  Code/outputs/hf2/figures/fig4_indicator_counts.png (+ dark/ variant), fig4_indicator_counts.json

Each bar is labelled with its count. Colour: series 2 (green), "all training patients", as in Figure 1. The value 1
of `sex` is not documented as either sex (step 1), so the bar is labelled "sex = 1".

Run:    cd Code && uv run python hf2_06_fig4_indicator_counts.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import viz_style as vs
from hf2 import core

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"
vs.FIGURES = OUT / "figures"
NAME = "fig4_indicator_counts"
FIGSIZE = (12, 6)


def draw(counts: dict, n: int, theme: str) -> None:
    t = vs.use(theme)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(counts))
    ax.bar(x, list(counts.values()), width=0.6, color=t.series[2], edgecolor=t.surface, linewidth=0.6)
    for i, v in enumerate(counts.values()):
        ax.text(i, v + 2, f"{v}", ha="center", va="bottom", fontsize=vs.ANNOT, color=t.text_primary)
    ax.set_xticks(x, [f"{c} = 1" for c in counts])
    ax.set_ylabel("Patients")
    ax.set_ylim(0, n)
    ax.grid(axis="x", visible=False)
    vs.header(fig, f"Patients with each yes/no input = 1, of {n} training patients")
    vs.layout(fig, top=0.90)
    vs.save(fig, NAME)


def main() -> None:
    X, _ = core.training_data()
    counts = {c: int((X[c] == 1).sum()) for c in core.CATEGORICAL}
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps({"rows": "training patients only", "n_train": int(len(X)),
                                                          "count_value_1": counts}, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(counts, len(X), theme)


if __name__ == "__main__":
    main()
