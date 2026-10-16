"""Chart styling shared by every figure in this analysis.

One place defines the palette, ink and mark geometry so all figures read as one system.

Each analysis writes its figures to its own outputs folder, for example `outputs/sepsis/`:
set `FIGURES` to that folder before saving. The default, `outputs/figures/`, belongs to
the Heart Failure analysis. Figures render twice - in that folder on a light surface and
in its `dark/` subfolder on a dark one - both opaque. An Obsidian vault may be read in either theme and a PNG
cannot adapt, while a transparent PNG with dark ink is illegible on a dark theme.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

CODE_DIR = Path(__file__).resolve().parent
FIGURES = CODE_DIR / "outputs" / "figures"
DPI = 200

# Point-label size. Figures are scaled to the note's pane width, so labels set
# for the raw PNG come out unreadable; this is sized for the rendered note.
ANNOT = 12


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str
    text_primary: str
    text_secondary: str
    muted: str
    grid: str
    baseline: str
    series: list[str]


LIGHT = Theme("light", "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9",
              "#c3c2b7", ["#2a78d6", "#eb6834", "#1baf7a"])
DARK = Theme("dark", "#1a1a19", "#ffffff", "#c3c2b7", "#898781", "#2c2c2a",
             "#383835", ["#3987e5", "#d95926", "#199e70"])
THEMES = {"light": LIGHT, "dark": DARK}

_active: Theme = LIGHT


def theme() -> Theme:
    return _active


def use(name: str) -> Theme:
    """Activate a theme and apply it to matplotlib's global style."""
    global _active
    t = THEMES[name]
    _active = t
    mpl.rcParams.update({
        "figure.dpi": DPI, "savefig.dpi": DPI,
        "figure.facecolor": t.surface, "axes.facecolor": t.surface,
        "savefig.facecolor": t.surface, "savefig.transparent": False,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 15,
        "text.color": t.text_primary,
        "axes.edgecolor": t.baseline, "axes.labelcolor": t.text_secondary,
        "axes.labelsize": 15, "axes.linewidth": 1.0,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "axes.axisbelow": True,
        # Solid hairline grid: dashed grids read as data.
        "grid.color": t.grid, "grid.linewidth": 0.7, "grid.linestyle": "-",
        "xtick.color": t.muted, "ytick.color": t.muted,
        "xtick.labelcolor": t.text_secondary, "ytick.labelcolor": t.text_secondary,
        "xtick.labelsize": 13, "ytick.labelsize": 13,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "legend.frameon": False, "legend.fontsize": 13, "legend.title_fontsize": 13,
        "lines.linewidth": 2.0,
    })
    return t


def header(fig, headline: str) -> None:
    """Figure-level headline, flush left. Title only — no subtitle.

    Anchored to the figure rather than the axes so the text starts at the left edge
    instead of after the y-axis labels. Anything a subtitle would have said belongs
    in the caption beneath the figure, not inside the frame.
    """
    fig.text(0.004, 0.99, headline, ha="left", va="top", fontsize=18,
             fontweight="bold", color=_active.text_primary)


def layout(fig, top: float = 0.93) -> None:
    """Fit the axes into the figure, leaving room for the header and source note.

    The bottom margin is derived from how many lines the source note wrapped to,
    so a long note pushes the axes up instead of overprinting the x-axis label.
    """
    lines = getattr(fig, "_source_lines", 1)
    bottom = 0.012 + lines * (SOURCE_SIZE * 1.35 / 72) / fig.get_figheight()
    fig.tight_layout(rect=(0, bottom, 1, top))


SOURCE_SIZE = 10


def save(fig, name: str) -> None:
    out = FIGURES if _active.name == "light" else FIGURES / "dark"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", pad_inches=0.22,
                facecolor=_active.surface)
    plt.close(fig)
    print(f"  figure: {path.relative_to(CODE_DIR)}")
