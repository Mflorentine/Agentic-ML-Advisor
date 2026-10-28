"""Heart Failure rerun Figure 4: mean cross-validated PR-AUC of the baseline and the six configurations compared, with
the fold SD as an error bar (step 4h).

Reads   Code/outputs/hf2/core_cv_post_prior_2.json   (the core's last CV table, which holds every entry)
        Code/outputs/hf2/core_recommend.json          (which entry was recommended)
Writes  Code/outputs/hf2/figures/fig4_cv_comparison.png (+ dark/ variant), fig4_cv_comparison.json

Nothing is recomputed. Colour: configurations in the model colour (purple), used in every evaluation figure of this
analysis; the baseline in the theme's neutral grey.

Run:    cd Code && uv run python hf2_08_fig4_cv_comparison.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"
vs.FIGURES = OUT / "figures"
NAME = "fig4_cv_comparison"
FIGSIZE = (12, 6.5)
MODEL_COLOUR = {"light": "#7a4fd6", "dark": "#9b7af0"}   # the models, in every evaluation figure
LABELS = {"Baseline (flag nobody)": "Baseline (flag nobody)", "Logistic": "Logistic (recommended)",
          "Logistic + L2": "Logistic + L2", "Logistic + poly": "Logistic + poly",
          "Logistic + poly + L2": "Logistic + poly + L2", "kNN": "k-NN", "Tree": "Decision tree"}


def load() -> tuple[list[dict], dict]:
    table = json.loads((OUT / "core_cv_post_prior_2.json").read_text(encoding="utf-8"))
    rec = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
    rows = {r["configuration"]: r for r in table["table"]["rows"]}
    assert set(rows) == set(LABELS) and rec["recommendation"]["entry"] == "Logistic"
    bars = sorted(({"entry": k, "label": LABELS[k], "mean": rows[k]["cv_mean_pr_auc"], "sd": rows[k]["fold_sd_pr_auc"]}
                   for k in LABELS), key=lambda r: r["mean"])
    return bars, {"table_core_version": table["core_version_sha256"], "recommended": rec["recommendation"]["entry"]}


def draw(bars: list[dict], theme: str) -> None:
    t = vs.use(theme)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    y = range(len(bars))
    colours = [t.baseline if b["entry"].startswith("Baseline") else MODEL_COLOUR[theme] for b in bars]
    ax.barh(list(y), [b["mean"] for b in bars], xerr=[b["sd"] for b in bars], color=colours, height=0.6,
            error_kw={"ecolor": t.text_secondary, "elinewidth": 1.5, "capsize": 5})
    for i, b in zip(y, bars):
        ax.text(b["mean"] + b["sd"] + 0.015, i, f"{b['mean']:.4f}", va="center", fontsize=vs.ANNOT, color=t.text_primary)
    ax.set_yticks(list(y), [b["label"] for b in bars])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Mean PR-AUC over the 10 outer folds")
    ax.grid(axis="y", visible=False)
    vs.header(fig, "Cross-validated PR-AUC, 239 training patients")
    vs.layout(fig, top=0.90)
    vs.save(fig, NAME)


def main() -> None:
    bars, meta = load()
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps({**meta, "bars": bars}, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(bars, theme)


if __name__ == "__main__":
    main()
