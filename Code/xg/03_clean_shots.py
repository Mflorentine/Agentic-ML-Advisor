"""xG analysis, step 1: apply the user's cleaning decisions to the open-play shot table.

Decisions (user, 9 November 2026): remove the oddities found in the describing pass.
  - drop shots whose event `duration` is implausible (> MAX_DURATION_S seconds; one shot, 1,746.6 s)
  - drop shots taken from inside the shooter's own half (x < HALFWAY)
  - drop shots whose freeze frame shows no opposing goalkeeper
  - harmonise the two short team names in the event files with the match files' names
  Player names are not used; `player_id` is consistent, so the six IDs with two spellings need no change.
Scope (user, 10 November 2026): drop the Bundesliga (GER) completely. The open data holds only
Bayer Leverkusen's 34 matches, so every other GER team appears twice and cannot be balanced in the split.

Reads   Code/outputs/xg/shots_open_play.csv, Code/outputs/xg/freeze_frames_open_play.csv
Writes  Code/outputs/xg/shots_clean.csv, Code/outputs/xg/freeze_frames_clean.csv, Code/outputs/xg/clean_log.txt

Run:  cd Code && uv run python xg/03_clean_shots.py
No randomness.
"""
from __future__ import annotations

import hashlib
import os

import pandas as pd

MAX_DURATION_S = 60.0   # a shot event lasting longer than a minute is a recording error; 99.9th percentile is 4.2 s
HALFWAY = 60.0          # StatsBomb x coordinate of the halfway line (pitch 120 long)
TEAM_NAMES = {"Caen": "Stade Malherbe Caen", "Marseille": "Olympique de Marseille"}
EXCLUDE_LEAGUES = {"GER"}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outputs", "xg")


def sha(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    s = pd.read_csv(os.path.join(OUT, "shots_open_play.csv"))
    ff = pd.read_csv(os.path.join(OUT, "freeze_frames_open_play.csv"))

    drop = s.league.isin(EXCLUDE_LEAGUES)
    lines_scope = f"Scope: leagues excluded {sorted(EXCLUDE_LEAGUES)}: {int(drop.sum())} shots ({int(s.loc[drop, 'goal'].sum())} goals), {s.loc[drop, 'match_id'].nunique()} matches"
    s = s.loc[~drop].reset_index(drop=True)

    has_gk = set(ff.loc[(ff.position == "Goalkeeper") & (~ff.teammate), "shot_id"])
    rules = {
        "duration": s.duration > MAX_DURATION_S,
        "own_half": s.x < HALFWAY,
        "no_opposing_gk": ~s.shot_id.isin(has_gk),
    }
    lines = [lines_scope, f"Input after scope: {len(s)} shots, {int(s.goal.sum())} goals"]
    for k, m in rules.items():
        lines.append(f"Rule {k}: {int(m.sum())} shots ({int(s.loc[m, 'goal'].sum())} goals)")
    m_any = rules["duration"] | rules["own_half"] | rules["no_opposing_gk"]
    lines.append(f"Overlap own_half & no_opposing_gk: {int((rules['own_half'] & rules['no_opposing_gk']).sum())}")
    lines.append(f"Removed in total: {int(m_any.sum())} shots ({int(s.loc[m_any, 'goal'].sum())} goals)")

    # check the names to be mapped are present and their targets exist in the match files
    match_names = set(s.home_team) | set(s.away_team)
    for short, full in TEAM_NAMES.items():
        assert short in set(s.team), short
        assert full in match_names, full
    renamed = int(s.team.isin(TEAM_NAMES).sum())
    s["team"] = s.team.replace(TEAM_NAMES)
    lines.append(f"Team names harmonised: {renamed} shots ({', '.join(f'{a} -> {b}' for a, b in TEAM_NAMES.items())})")
    assert set(s.team) <= match_names

    s = s.loc[~m_any].reset_index(drop=True)
    ff = ff[ff.shot_id.isin(set(s.shot_id))]
    lines.append(f"Output: {len(s)} shots, {int(s.goal.sum())} goals ({s.goal.mean():.4f}); teams {s.team.nunique()}; freeze-frame rows {len(ff)}")
    lines.append("By league: " + ", ".join(f"{lg} {n}" for lg, n in s.league.value_counts().sort_index().items()))

    p1, p2 = os.path.join(OUT, "shots_clean.csv"), os.path.join(OUT, "freeze_frames_clean.csv")
    s.to_csv(p1, index=False, lineterminator="\n")
    ff.to_csv(p2, index=False, lineterminator="\n")
    lines.append(f"SHA-256 shots_clean.csv: {sha(p1)}")
    lines.append(f"SHA-256 freeze_frames_clean.csv: {sha(p2)}")
    text = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "clean_log.txt"), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
