"""xG analysis, step 2: train/test split by match; the test set is locked from here on.

Admissibility 3 (DR-03): shots are grouped by match, so whole matches go to one side.
Admissibility 4 (DR-09, superseding DR-04): the test data are whole matchweeks drawn at random within
each league, so every team has the same number of test matches (user, 10 November 2026).
TEST_WEEKS of the 38 matchweeks per league (about 21 %); 20 % of matches was agreed, and matchweek
sampling rounds it to whole weeks. The matchweek of each match comes from the StatsBomb match files.
The first version of this script (DR-08, superseded) drew 20 % of matches with GroupShuffleSplit.

Reads   Code/outputs/xg/shots_clean.csv, Code/outputs/xg/freeze_frames_clean.csv,
        Attachments/statsbomb-open-data-2015-16/raw/matches/*.json.gz (match_week)
Writes  Code/outputs/xg/split/split.json                 seed, fraction, match ids per side, counts
        Code/outputs/xg/split/shots_train.csv            training shots (steps 3 and 4 read only these)
        Code/outputs/xg/split/freeze_frames_train.csv
        Code/outputs/xg/split/test_locked/shots_test.csv  read only by the final evaluation (step 4g)
        Code/outputs/xg/split/test_locked/freeze_frames_test.csv

After this script, no step 3 or step 4 code may read anything in test_locked/ until the single
final evaluation of each sub-task.

Run:  cd Code && uv run python xg/04_split.py
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os

import numpy as np
import pandas as pd

SEED = 20261111
TEST_WEEKS = 8  # matchweeks per league in the test set, out of 38
LEAGUES = {"ENG": (2, 27), "ESP": (11, 27), "ITA": (12, 27), "FRA": (7, 27)}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outputs", "xg")
RAW = os.path.join(HERE, "..", "..", "Attachments", "statsbomb-open-data-2015-16", "raw", "matches")
SPLIT = os.path.join(OUT, "split")
LOCKED = os.path.join(SPLIT, "test_locked")


def sha(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    s = pd.read_csv(os.path.join(OUT, "shots_clean.csv"))
    ff = pd.read_csv(os.path.join(OUT, "freeze_frames_clean.csv"))
    week = {}
    for lg, (cid, sid) in LEAGUES.items():
        with gzip.open(os.path.join(RAW, f"{cid}_{sid}.json.gz"), "rt", encoding="utf-8") as f:
            for m in json.load(f):
                week[m["match_id"]] = (lg, m["match_week"])
    assert set(s.league) == set(LEAGUES), set(s.league)
    s["match_week"] = s.match_id.map(lambda m: week[m][1])
    rng = np.random.default_rng(SEED)
    test_weeks = {lg: sorted(int(w) for w in rng.choice(np.arange(1, 39), size=TEST_WEEKS, replace=False)) for lg in LEAGUES}
    is_test = np.array([w in test_weeks[lg] for lg, w in zip(s.league, s.match_week)])
    tr, te = s[~is_test], s[is_test]
    assert not set(tr.match_id) & set(te.match_id)

    # test matches per team (each match counts for both teams)
    mt = te.groupby("match_id")[["league", "home_team", "away_team"]].first()
    per_team = pd.concat([mt.home_team, mt.away_team]).value_counts()
    all_teams = set(s.home_team) | set(s.away_team)
    per_team = per_team.reindex(sorted(all_teams), fill_value=0)
    os.makedirs(LOCKED, exist_ok=True)
    files = {
        "shots_train.csv": (SPLIT, tr),
        "freeze_frames_train.csv": (SPLIT, ff[ff.shot_id.isin(set(tr.shot_id))]),
        "shots_test.csv": (LOCKED, te),
        "freeze_frames_test.csv": (LOCKED, ff[ff.shot_id.isin(set(te.shot_id))]),
    }
    sums = {}
    for name, (d, df) in files.items():
        p = os.path.join(d, name)
        df.to_csv(p, index=False, lineterminator="\n")
        sums[name] = sha(p)

    def side(df):
        return {"matches": int(df.match_id.nunique()), "shots": int(len(df)), "goals": int(df.goal.sum()),
                "goal_share": round(float(df.goal.mean()), 4),
                "shots_by_league": {k: int(v) for k, v in df.league.value_counts().sort_index().items()}}

    info = {
        "seed": SEED, "test_weeks_per_league": TEST_WEEKS, "method": "numpy default_rng(SEED).choice of matchweeks 1-38 per league, in the order ENG, ESP, ITA, FRA",
        "test_weeks": test_weeks,
        "test_matches_per_team": {"min": int(per_team.min()), "max": int(per_team.max()),
                                  "teams_below_max": {t: int(n) for t, n in per_team.items() if n < per_team.max()}},
        "train": side(tr), "test": side(te),
        "train_match_ids": sorted(int(m) for m in set(tr.match_id)),
        "test_match_ids": sorted(int(m) for m in set(te.match_id)),
        "sha256": sums,
    }
    with open(os.path.join(SPLIT, "split.json"), "w") as f:
        json.dump(info, f, indent=1)
    print(json.dumps({k: v for k, v in info.items() if not k.endswith("match_ids")}, indent=1))


if __name__ == "__main__":
    main()
