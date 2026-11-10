"""Figure style for the xG analysis: the workspace style of the SML book's figures (Code/sml_style.py),
with the colour of each variable fixed for every figure in this analysis.

Colours by variable (from the book's palette):
  GOAL       red       goals, and the share of shots that scored
  MODEL      blue      the sub-task 1 model (and the configurations compared)
  TEAM       rose      the sub-task 2 model, with team
  STATSBOMB  orange    StatsBomb's xG, the reference
  TRAIN      coral     error on the training matches (as E_train in the book's Fig. 13.3)
  HELD_OUT   lavender  error on the held-out matches (as E_hold-out in Fig. 13.3)
  grey                 all shots, counts of shots, the baseline, reference lines
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import sml_style as sml  # noqa: E402

CM = sml.CM
DPI = sml.DPI
FIGURES = Path(__file__).resolve().parent.parent / "outputs" / "xg" / "figures"

GOAL = sml.RED
MODEL = sml.BLUE
TEAM = sml.ROSE
STATSBOMB = sml.ORANGE
TRAIN = sml.CORAL
HELD_OUT = sml.LAVENDER
GREY = sml.GREY


class Theme:
    def __init__(self, t: "sml.Theme"):
        self.name, self.surface, self.ink = t.name, t.surface, t.ink
        self.no_goal = sml.GREY
        self.pitch = t.faint


def use(name: str) -> Theme:
    return Theme(sml.use(name))


def save(fig, name: str, theme: Theme) -> Path:
    return sml.save(fig, FIGURES, name, sml.LIGHT if theme.name == "light" else sml.DARK)
