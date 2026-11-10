"""xG analysis, step 1: describe the open-play shot table (describing pass only; no judgements).

Reads   Code/outputs/xg/shots_<name>.csv, Code/outputs/xg/freeze_frames_<name>.csv
Writes  Code/outputs/xg/describe_shots_<name>.md   (per-column summary, value counts, coverage)
        <name> is `open_play` (default; the extracted table) or `clean` (after 03_clean_shots.py).
        For `open_play` the output keeps its original name, describe_shots.md.

Run:  cd Code && uv run python xg/02_describe_shots.py [open_play|clean]
No randomness.
"""
from __future__ import annotations

import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outputs", "xg")


def md_table(df: pd.DataFrame) -> str:
    return df.to_markdown(index=False)


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "open_play"
    s = pd.read_csv(os.path.join(OUT, f"shots_{name}.csv"))
    ff = pd.read_csv(os.path.join(OUT, f"freeze_frames_{name}.csv"))
    out = []
    out.append(f"# Describing pass: shots_{name}.csv\n")
    out.append(f"Rows: {len(s)}. Columns: {s.shape[1]}. Duplicate `shot_id`: {s.shot_id.duplicated().sum()}. Fully duplicated rows: {s.duplicated().sum()}.\n")

    rows = []
    for c in s.columns:
        col = s[c]
        r = {"column": c, "dtype": str(col.dtype), "missing": int(col.isna().sum()), "distinct": int(col.nunique(dropna=True))}
        if pd.api.types.is_bool_dtype(col):
            r["summary"] = f"True {int(col.sum())} ({col.mean():.1%})"
        elif pd.api.types.is_numeric_dtype(col):
            r["summary"] = f"min {col.min():.4g}, median {col.median():.4g}, mean {col.mean():.4g}, max {col.max():.4g}"
        else:
            vc = col.value_counts()
            r["summary"] = "; ".join(f"{k} {v}" for k, v in vc.head(6).items()) + (" …" if len(vc) > 6 else "")
        rows.append(r)
    out.append("## Per column\n")
    out.append(md_table(pd.DataFrame(rows)) + "\n")

    for c in ["league", "period", "play_pattern", "position", "body_part", "technique", "key_pass_type", "outcome", "goal"]:
        vc = s[c].value_counts(dropna=False).rename_axis(c).reset_index(name="count")
        out.append(f"## `{c}`\n")
        out.append(md_table(vc) + "\n")

    out.append("## Coverage\n")
    cov = s.groupby("league").agg(matches=("match_id", "nunique"), shots=("shot_id", "size"), goals=("goal", "sum"),
                                  teams=("team", "nunique"), players=("player_id", "nunique"),
                                  first=("match_date", "min"), last=("match_date", "max")).reset_index()
    cov["goal_share"] = (cov.goals / cov.shots).round(4)
    out.append(md_table(cov) + "\n")
    out.append(f"Matches with at least one kept shot: {s.match_id.nunique()}. Teams: {s.team.nunique()}. Players: {s.player_id.nunique()}.\n")
    per_player = s.groupby("player_id").size()
    out.append(f"Shots per player: median {per_player.median():.0f}, max {per_player.max()}; players with 1 shot: {(per_player == 1).sum()}.\n")
    per_match = s.groupby("match_id").size()
    out.append(f"Shots per match: min {per_match.min()}, median {per_match.median():.0f}, max {per_match.max()}.\n")

    out.append("## Location ranges\n")
    out.append(f"`x` outside [0, 120]: {((s.x < 0) | (s.x > 120)).sum()}; `y` outside [0, 80]: {((s.y < 0) | (s.y > 80)).sum()}; shots with `x` < 60 (own half): {(s.x < 60).sum()}.\n")
    out.append(f"`end_z` missing by outcome:\n\n" + md_table(s.assign(end_z_missing=s.end_z.isna()).groupby("outcome").end_z_missing.agg(["sum", "size"]).reset_index()) + "\n")

    out.append("## `statsbomb_xg`\n")
    out.append(f"Missing {s.statsbomb_xg.isna().sum()}; zero {int((s.statsbomb_xg == 0).sum())}; min {s.statsbomb_xg.min():.4g}; max {s.statsbomb_xg.max():.4g}; sum {s.statsbomb_xg.sum():.1f} against {s.goal.sum()} goals.\n")

    out.append("## Freeze frames\n")
    out.append(f"Rows: {len(ff)}. Shots with a freeze frame: {ff.shot_id.nunique()} of {len(s)}. Players per frame: " +
               f"min {s.freeze_frame_players.min()}, median {s.freeze_frame_players.median():.0f}, max {s.freeze_frame_players.max()}.\n")
    vc = ff.assign(gk=ff.position.eq("Goalkeeper")).groupby(["teammate", "gk"]).size().rename("rows").reset_index()
    out.append(md_table(vc) + "\n")
    no_gk = len(s) - ff[(ff.position == "Goalkeeper") & (~ff.teammate)].shot_id.nunique()
    out.append(f"Shots with no opposing goalkeeper in the freeze frame: {no_gk}.\n")

    text = "\n".join(out)
    fname = "describe_shots.md" if name == "open_play" else f"describe_shots_{name}.md"
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
