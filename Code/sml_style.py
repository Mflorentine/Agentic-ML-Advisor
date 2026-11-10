"""Figure style for this workspace, in line with the figures of the SML book.

Lindholm et al., Machine Learning - A First Course for Engineers and Scientists (2nd edition draft,
1 September 2026). The book's data figures (for example Figures 2.3, 4.3, 4.14 and 13.3) share:
  - serif type (Times-like), black axes and labels, white background, no grid;
  - a full box around data plots, with small inward ticks on all four sides and few tick values;
  - a legend inside the plot with a thin black frame;
  - series told apart by line style (solid, dashed, dotted) as well as by colour;
  - a muted palette: training error coral, held-out error lavender (Fig. 13.3), classes red and
    blue (Fig. 2.3), a classifier's curve orange and a reference line green dotted (Fig. 4.14);
  - nothing in the frame but axes, data, legend and short labels; captions go below, outside.
The colours below were sampled from the rendered pages of the local copy of the book.

Workspace rules kept on top of the book's style (instructions.md, step 3): every figure is drawn in
a light variant (the book's look) and a dark variant for a dark vault, both opaque; a colour belongs
to a variable, not to a rank; text is sized to stay readable when the image is scaled to the pane.

`Code/viz_style.py` is the older convention used by the Heart Failure analysis and is kept for it.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

CM = 1 / 2.54
DPI = 300

# Palette sampled from the book's figures
BLUE = "#3850A0"       # class / series blue (Fig. 2.3)
RED = "#E82020"        # class red (Fig. 2.3)
ORANGE = "#F08018"     # a classifier's curve (Fig. 4.14)
LAVENDER = "#7880C0"   # held-out / new-data error (Fig. 13.3)
CORAL = "#F07050"      # training error (Fig. 13.3)
GREEN = "#689858"      # reference line, e.g. random guess (Fig. 4.14)
ROSE = "#C85058"       # E_new (Fig. 4.3)
GREY = "#808080"       # baseline and "other" (workspace rule)


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str
    ink: str
    faint: str


LIGHT = Theme("light", "#ffffff", "#000000", "#b0b0b0")
DARK = Theme("dark", "#1a1a19", "#e6e6e6", "#5a5a5a")


def use(name: str) -> Theme:
    t = LIGHT if name == "light" else DARK
    mpl.rcParams.update({
        "figure.dpi": 100, "savefig.dpi": DPI,
        "figure.facecolor": t.surface, "axes.facecolor": t.surface,
        "savefig.facecolor": t.surface, "savefig.transparent": False,
        "font.family": "serif", "font.serif": ["STIXGeneral", "Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10, "axes.labelsize": 10, "axes.titlesize": 10,
        "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
        "text.color": t.ink, "axes.labelcolor": t.ink, "axes.edgecolor": t.ink,
        "xtick.color": t.ink, "ytick.color": t.ink,
        "axes.linewidth": 0.6, "axes.grid": False,
        "axes.spines.top": True, "axes.spines.right": True,
        "xtick.direction": "in", "ytick.direction": "in", "xtick.top": True, "ytick.right": True,
        "xtick.major.size": 3, "ytick.major.size": 3, "xtick.minor.size": 1.5, "ytick.minor.size": 1.5,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "legend.frameon": True, "legend.fancybox": False, "legend.edgecolor": t.ink,
        "legend.framealpha": 1.0, "legend.facecolor": t.surface, "patch.linewidth": 0.6,
        "lines.linewidth": 1.4, "lines.markersize": 4,
    })
    return t


def save(fig, folder: Path, name: str, theme: Theme) -> Path:
    out = folder if theme.name == "light" else folder / "dark"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=DPI, facecolor=theme.surface)   # no bbox_inches="tight": the size stays as set
    plt.close(fig)
    return path
