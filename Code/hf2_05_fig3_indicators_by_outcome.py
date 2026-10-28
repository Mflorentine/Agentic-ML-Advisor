"""Heart Failure rerun Figure 3: for each of the 5 yes/no inputs, the share of training patients who died during
follow-up among those with the value 0 and among those with the value 1 (user, step 3).

Reads   the training patients through Code/hf2/core.py training_data() (the 60 test rows are never read)
Writes  Code/outputs/hf2/figures/fig3_indicators_by_outcome.png (+ dark/ variant), fig3_indicators_by_outcome.json

Bar height: share who died (deaths / patients in that group). Each bar is labelled with "deaths / patients". Colour:
series 1 (orange), "died", as in Figure 2; light orange for the value 0, full orange for the value 1. A grey line
marks the share who died among all training patients, named in the legend. Values are labelled "= 0" and "= 1" because the coding of
`sex` is undocumented (step 1).

Run:    cd Code && uv run python hf2_05_fig3_indicators_by_outcome.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import viz_style as vs
from hf2 import core

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"
vs.FIGURES = OUT / "figures"
NAME = "fig3_indicators_by_outcome"
FIGSIZE = (13, 7)
WIDTH = 0.38


def table(X: pd.DataFrame, y: pd.Series) -> dict:
    return {c: {str(v): {"patients": int((X[c] == v).sum()), "deaths": int(((X[c] == v) & (y == 1)).sum()),
                         "share_died": float(y[X[c] == v].mean())} for v in (0, 1)} for c in core.CATEGORICAL}


def draw(tab: dict, overall: float, theme: str) -> None:
    t = vs.use(theme)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    x = np.arange(len(core.CATEGORICAL))
    for k, (v, alpha) in enumerate((("0", 0.45), ("1", 1.0))):
        shares = [tab[c][v]["share_died"] for c in core.CATEGORICAL]
        pos = x + (k - 0.5) * WIDTH
        ax.bar(pos, shares, width=WIDTH, color=t.series[1], alpha=alpha, label=f"value = {v}",
               edgecolor=t.surface, linewidth=0.6)
        for p, c in zip(pos, core.CATEGORICAL):
            ax.text(p, tab[c][v]["share_died"] + 0.012, f"{tab[c][v]['deaths']}/{tab[c][v]['patients']}",
                    ha="center", va="bottom", fontsize=vs.ANNOT - 1, color=t.text_primary)
    ax.axhline(overall, color=t.baseline, linewidth=1.5, linestyle="-", zorder=0,
               label=f"all training patients ({overall:.2f})")
    ax.set_xticks(x, core.CATEGORICAL)
    ax.set_ylabel("Share who died during follow-up")
    ax.set_ylim(0, 0.62)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="upper left")
    vs.header(fig, "Share who died, by each yes/no input (training patients)")
    vs.layout(fig, top=0.90)
    vs.save(fig, NAME)


def main() -> None:
    X, y = core.training_data()
    tab, overall = table(X, y), float(y.mean())
    assert max(v["share_died"] for c in tab.values() for v in c.values()) < 0.58, "raise the y-limit"
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps({"rows": "training patients only", "n_train": int(len(X)),
                                                          "share_died_all": overall, "by_input": tab}, indent=2),
                                             encoding="utf-8")
    for theme in ("light", "dark"):
        draw(tab, overall, theme)


if __name__ == "__main__":
    main()
