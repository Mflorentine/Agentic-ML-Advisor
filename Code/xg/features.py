"""xG analysis: the input design agreed with the user in step 3 (DR-13).

Fixed formulas only. Nothing here is fitted to data, so the same functions are applied to the
training shots now and to the test shots in the single final evaluation, without leakage.

StatsBomb pitch coordinates: 120 x 80, the attacking team plays towards x = 120; the goal is at
x = 120 between the posts y = 36 and y = 44 (the usual StatsBomb convention; see the Data Summary).

Inputs
  distance        distance from the shot to the centre of the goal (120, 40), pitch units
  angle           angle between the lines from the shot to the two posts, degrees (0-180)
  opp_in_triangle number of opponents, goalkeeper excluded, inside the triangle formed by the shot
                  and the two posts, boundary included, from the freeze frame
  gk_distance     distance from the shot to the opposing goalkeeper in the freeze frame, pitch units
  plus the coded attributes in CATEGORICAL and BOOLEAN, as recorded by StatsBomb
Sub-task 2 adds `team`.
Dropped by the user: x and y (replaced by distance and angle), follows_dribble and redirect (rare).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

GOAL_X = 120.0
POST_LOW_Y = 36.0
POST_HIGH_Y = 44.0
GOAL_CENTRE_Y = 40.0

NUMERIC = ["distance", "angle", "opp_in_triangle", "gk_distance"]
CATEGORICAL = ["body_part", "technique", "play_pattern", "key_pass_type"]
BOOLEAN = ["under_pressure", "first_time", "one_on_one", "open_goal", "aerial_won"]
INPUTS_SUBTASK1 = NUMERIC + CATEGORICAL + BOOLEAN
INPUTS_SUBTASK2 = INPUTS_SUBTASK1 + ["team"]
NO_KEY_PASS = "none"  # value of key_pass_type when the shot had no assisting pass


def distance_to_goal(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.hypot(GOAL_X - x, GOAL_CENTRE_Y - y)


def goal_angle_degrees(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    a_low = np.arctan2(POST_LOW_Y - y, GOAL_X - x)
    a_high = np.arctan2(POST_HIGH_Y - y, GOAL_X - x)
    return np.degrees(np.abs(a_high - a_low))


def _cross(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def in_triangle(px, py, sx, sy) -> np.ndarray:
    """True where (px, py) lies inside or on the triangle (shot, low post, high post)."""
    d1 = _cross(sx, sy, GOAL_X, POST_LOW_Y, px, py)
    d2 = _cross(GOAL_X, POST_LOW_Y, GOAL_X, POST_HIGH_Y, px, py)
    d3 = _cross(GOAL_X, POST_HIGH_Y, sx, sy, px, py)
    has_neg = (d1 < 0) | (d2 < 0) | (d3 < 0)
    has_pos = (d1 > 0) | (d2 > 0) | (d3 > 0)
    return ~(has_neg & has_pos)


def build_inputs(shots: pd.DataFrame, frames: pd.DataFrame) -> pd.DataFrame:
    """One row per shot: shot_id, match_id, goal, team and the inputs of INPUTS_SUBTASK2."""
    s = shots.copy()
    s["distance"] = distance_to_goal(s.x.to_numpy(), s.y.to_numpy())
    s["angle"] = goal_angle_degrees(s.x.to_numpy(), s.y.to_numpy())
    f = frames.merge(s[["shot_id", "x", "y"]], on="shot_id", how="inner", suffixes=("", "_shot"))
    opp = f[~f.teammate]
    is_gk = opp.position.eq("Goalkeeper")
    outfield = opp[~is_gk]
    inside = in_triangle(outfield.x.to_numpy(), outfield.y.to_numpy(), outfield.x_shot.to_numpy(), outfield.y_shot.to_numpy())
    s["opp_in_triangle"] = s.shot_id.map(outfield[inside].groupby("shot_id").size()).fillna(0).astype(int)
    gk = opp[is_gk]
    assert not gk.shot_id.duplicated().any(), "more than one opposing goalkeeper in a frame"
    gk_dist = pd.Series(np.hypot(gk.x.to_numpy() - gk.x_shot.to_numpy(), gk.y.to_numpy() - gk.y_shot.to_numpy()), index=gk.shot_id.to_numpy())
    s["gk_distance"] = s.shot_id.map(gk_dist)
    assert s.gk_distance.notna().all(), "a shot without an opposing goalkeeper"
    s["key_pass_type"] = s.key_pass_type.fillna(NO_KEY_PASS)
    for c in BOOLEAN:
        s[c] = s[c].astype(int)
    return s[["shot_id", "match_id", "league", "goal"] + INPUTS_SUBTASK2]
