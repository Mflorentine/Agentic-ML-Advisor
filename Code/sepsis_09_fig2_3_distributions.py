"""Sepsis Figures 2 and 3: distribution of each clinical input (its last value in ICU hours 1-6) over the training
patients who have one. Figure 2: the seven vitals. Figure 3: the twenty labs; the ten log inputs (DR-09) on a log
axis. Not split by outcome (user, step 3).

Reads   Code/outputs/sepsis/private/train_table.csv.gz   (training patients only)
Writes  Code/outputs/sepsis/figures/fig2_vitals.png, fig3_labs.png (+ dark/ variants)
        Code/outputs/sepsis/figures/fig2_3_distributions.json   (per panel: patients with a value, min, max)

Each panel shows only the patients with a value; filled (median) values are not drawn. Bins: 40, equal width over
the panel's full range (equal width on the log scale for log inputs), so no value is cut off. Each panel has its own
y scale. Colour: series 2 (green), "all training patients", in every Sepsis figure.

Run:    cd Code && uv run python sepsis_09_fig2_3_distributions.py
"""
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import viz_style as vs

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
vs.FIGURES = OUT / "figures"
BINS = 40

VITALS = [("HR", "beats/min"), ("O2Sat", "%"), ("Temp", "°C"), ("SBP", "mm Hg"), ("MAP", "mm Hg"),
          ("DBP", "mm Hg"), ("Resp", "breaths/min")]
LABS = [("FiO2", "fraction"), ("pH", ""), ("PaCO2", "mm Hg"), ("SaO2", "%"), ("AST", "IU/L"), ("BUN", "mg/dL"),
        ("Alkalinephos", "IU/L"), ("Calcium", "mg/dL"), ("Creatinine", "mg/dL"), ("Glucose", "mg/dL"),
        ("Lactate", "mg/dL"), ("Magnesium", "mmol/dL"), ("Phosphate", "mg/dL"), ("Potassium", "mmol/L"),
        ("Bilirubin_total", "mg/dL"), ("Hct", "%"), ("Hgb", "g/dL"), ("PTT", "s"), ("WBC", "10³/µL"),
        ("Platelets", "10³/µL")]
LOG_INPUTS = {"AST", "Alkalinephos", "Bilirubin_total", "Creatinine", "BUN", "Lactate", "WBC", "Glucose",
              "Platelets", "PTT"}   # DR-09; must match Code/sepsis/core.py LOG_INPUTS


def panel(ax, values: pd.Series, col: str, unit: str, t) -> None:
    lo, hi = values.min(), values.max()
    if col in LOG_INPUTS:
        bins = np.geomspace(lo, hi, BINS + 1)
        ax.set_xscale("log")
        # Major ticks only (decades), written as plain numbers; minor-tick labels overlap on short ranges.
        if np.log10(hi / lo) < 2:   # short range: also ticks at 2x and 5x each decade, so the axis has more than one label
            ax.xaxis.set_major_locator(mpl.ticker.LogLocator(base=10, subs=(1, 2, 5)))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}"))
        ax.xaxis.set_minor_formatter(plt.NullFormatter())
    else:
        bins = np.linspace(lo, hi, BINS + 1) if hi > lo else BINS
    ax.hist(values, bins=bins, color=t.series[2], edgecolor=t.surface, linewidth=0.6)
    ax.set_title(f"{col} ({unit}, log scale)" if col in LOG_INPUTS and unit else
                 f"{col} ({unit})" if unit else col, fontsize=14, color=t.text_primary, loc="left")
    ax.grid(axis="x", visible=False)
    ax.tick_params(labelsize=11)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))


def draw(df: pd.DataFrame, cols: list, ncols: int, size: tuple, title: str, name: str, theme_name: str) -> None:
    t = vs.use(theme_name)
    nrows = int(np.ceil(len(cols) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=size)
    for ax, (col, unit) in zip(axes.flat, cols):
        panel(ax, df[col].dropna(), col, unit, t)
    for ax in list(axes.flat)[len(cols):]:
        ax.set_visible(False)
    for r in range(nrows):
        axes[r, 0].set_ylabel("Patients", fontsize=13)
    vs.header(fig, title)
    vs.layout(fig, top=0.94)
    vs.save(fig, name)


if __name__ == "__main__":
    df = pd.read_csv(OUT / "private" / "train_table.csv.gz")
    for name in ("light", "dark"):
        draw(df, VITALS, 4, (16, 8), "Last value in the first 6 ICU hours: vital signs, training patients",
             "fig2_vitals", name)
        draw(df, LABS, 5, (18, 15), "Last value in the first 6 ICU hours: laboratory values, training patients",
             "fig3_labs", name)
    numbers = {"source": "private/train_table.csv.gz", "n_train": len(df),
               "panels": {c: {"patients_with_value": int(df[c].notna().sum()), "min": float(df[c].min()),
                              "max": float(df[c].max()), "log_axis": c in LOG_INPUTS}
                          for c, _ in VITALS + LABS}}
    (vs.FIGURES / "fig2_3_distributions.json").write_text(json.dumps(numbers, indent=2), encoding="utf-8")
