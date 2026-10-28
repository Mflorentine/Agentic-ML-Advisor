"""Mobile Price Figure 2: mean cross-validated accuracy of the baseline and the five configurations compared with the
agreed input design (all 20 inputs), with the fold SD as an error bar. The 20 single-input drops of backward
elimination (DR-19) are not candidates under §19 (interpretation z) and are not drawn.

Reads   Code/outputs/mobile/core_cv_post_prior_21.json   (the core's last CV table, which holds every entry;
        nothing is recomputed here)
        Code/outputs/mobile/core_recommend.json           (which entry was recommended)
Writes  Code/outputs/mobile/figures/fig2_cv_comparison.png (+ dark/ variant), fig2_cv_comparison.json

Colour: configurations in series 0 (blue), the baseline in the theme's neutral grey.

Run:    cd Code && uv run python mobile_07_fig2_cv_comparison.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "mobile"
vs.FIGURES = OUT / "figures"
NAME = "fig2_cv_comparison"
FIGSIZE = (12, 6)

LABELS = {  # entry key -> label on the figure
    "Baseline (most common class)": "Baseline (most common band)",
    "kNN": "k-NN",
    "Tree": "Decision tree",
    "Logistic + poly + L2": "Logistic + poly + L2",
    "Logistic + L2": r"Logistic + L2, λ ≥ $10^{-4}$",
    "Logistic + L2 (lambda grid from 1e-8)": r"Logistic + L2, λ ≥ $10^{-8}$ (recommended)",
}


def load() -> tuple[list[dict], dict]:
    table = json.loads((OUT / "core_cv_post_prior_21.json").read_text(encoding="utf-8"))
    rec = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
    rows = {r["configuration"]: r for r in table["table"]["rows"]}
    assert rec["recommendation"]["entry"] in LABELS
    keep = [{"entry": k, "label": LABELS[k], "mean": rows[k]["cv_mean_accuracy"], "sd": rows[k]["fold_sd_accuracy"]}
            for k in LABELS]
    keep.sort(key=lambda r: r["mean"])
    return keep, {"table_core_version": table["core_version_sha256"], "recommended": rec["recommendation"]["entry"]}


def draw(rows: list[dict], theme: str) -> None:
    t = vs.use(theme)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    y = range(len(rows))
    colours = [t.baseline if r["entry"].startswith("Baseline") else t.series[0] for r in rows]
    ax.barh(list(y), [r["mean"] for r in rows], xerr=[r["sd"] for r in rows], color=colours, height=0.6,
            error_kw={"ecolor": t.text_secondary, "elinewidth": 1.5, "capsize": 5})
    for i, r in zip(y, rows):
        ax.text(r["mean"] + r["sd"] + 0.015, i, f"{r['mean']:.4f}", va="center", fontsize=vs.ANNOT,
                color=t.text_primary)
    ax.set_yticks(list(y), [r["label"] for r in rows])
    ax.set_xlim(0, 1.12)
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("Mean accuracy over the 10 outer folds")
    ax.grid(axis="y", visible=False)
    vs.header(fig, "Cross-validated accuracy, 1,600 training phones")
    vs.layout(fig, top=0.90)
    vs.save(fig, NAME)


def main() -> None:
    rows, meta = load()
    vs.FIGURES.mkdir(parents=True, exist_ok=True)
    (vs.FIGURES / f"{NAME}.json").write_text(json.dumps({**meta, "bars": rows}, indent=2), encoding="utf-8")
    for theme in ("light", "dark"):
        draw(rows, theme)


if __name__ == "__main__":
    main()
