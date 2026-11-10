"""xG analysis, step 3: build the model inputs for the TRAINING shots (input design, DR-13).

Reads   Code/outputs/xg/split/shots_train.csv, Code/outputs/xg/split/freeze_frames_train.csv
Writes  Code/outputs/xg/split/inputs_train.csv     one row per training shot
        Code/outputs/xg/inputs_train_summary.md     ranges and counts of every input, and the
                                                    encoded input counts behind Properties 2-4
The test shots are not read. The same functions (xg/features.py) are applied to them only in the
single final evaluation.

Run:  cd Code && uv run python xg/05_build_inputs.py
No randomness.
"""
from __future__ import annotations

import hashlib
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import BOOLEAN, CATEGORICAL, INPUTS_SUBTASK1, NUMERIC, build_inputs  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outputs", "xg")
SPLIT = os.path.join(OUT, "split")


def main() -> None:
    shots = pd.read_csv(os.path.join(SPLIT, "shots_train.csv"))
    frames = pd.read_csv(os.path.join(SPLIT, "freeze_frames_train.csv"))
    X = build_inputs(shots, frames)
    p = os.path.join(SPLIT, "inputs_train.csv")
    X.to_csv(p, index=False, lineterminator="\n")
    with open(p, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()

    n = len(X)
    levels = {c: int(X[c].nunique()) for c in CATEGORICAL}
    n_teams = int(X.team.nunique())
    enc1 = len(NUMERIC) + sum(levels.values()) + len(BOOLEAN)
    enc2 = enc1 + n_teams
    cat1 = len(CATEGORICAL) + len(BOOLEAN)
    lines = ["# Training inputs (input design DR-13)", "",
             f"Rows: {n}. Goals: {int(X.goal.sum())}. SHA-256 of inputs_train.csv: {digest}", "",
             "## Numeric inputs", "", X[NUMERIC].describe().T.round(3).to_markdown(), "",
             "## Categorical inputs (levels)", ""]
    for c in CATEGORICAL:
        lines.append(f"- `{c}` ({levels[c]}): " + "; ".join(f"{k} {v}" for k, v in X[c].value_counts().items()))
    lines += ["", "## Boolean inputs (count of 1)", ""]
    lines += [f"- `{c}`: {int(X[c].sum())}" for c in BOOLEAN]
    lines += ["", f"Teams in training: {n_teams}", "",
              "## Encoded inputs (one indicator per level) for Properties 2-4", "",
              f"- Sub-task 1: {len(INPUTS_SUBTASK1)} columns ({len(NUMERIC)} numeric, {len(CATEGORICAL)} categorical, {len(BOOLEAN)} boolean) -> {enc1} encoded; ratio {n} / ({enc1} + 1) = {n / (enc1 + 1):.1f}; categorical share {cat1}/{len(INPUTS_SUBTASK1)} = {cat1 / len(INPUTS_SUBTASK1):.0%} (booleans counted as categorical)",
              f"- Sub-task 2: {len(INPUTS_SUBTASK1) + 1} columns (+ team) -> {enc2} encoded; ratio {n} / ({enc2} + 1) = {n / (enc2 + 1):.1f}; categorical share {cat1 + 1}/{len(INPUTS_SUBTASK1) + 1} = {(cat1 + 1) / (len(INPUTS_SUBTASK1) + 1):.0%}"]
    text = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "inputs_train_summary.md"), "w") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
