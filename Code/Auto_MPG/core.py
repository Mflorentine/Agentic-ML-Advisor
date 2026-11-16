"""Interim core for the Auto MPG analysis (interim core, not reviewed).

Implements step 4a of instructions.md: the admissible set (ML Guide.md sections 9, 12).
The property values come from props.json, which copies the values recorded in Appendix.md
(DR-06, DR-08, DR-11, DR-12, DR-13, DR-14, DR-17, DR-19, DR-20, DR-21, DR-22, DR-23).
Later sections (prior ranking, cross-validation, diagnosis, recommendation) are not implemented yet.

Run from Code/:  uv run python Auto_MPG/core.py
Writes: outputs/Auto_MPG/core_admset.json
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
ROOT = CODE.parent
SRC = ROOT / "Attachments" / "Auto MPG" / "auto-mpg.data"
SPLIT = CODE / "outputs" / "Auto_MPG" / "split_seed2026.csv"
PROPS = HERE / "props.json"
OUT = CODE / "outputs" / "Auto_MPG" / "core_admset.json"

# Named thresholds (ours, [I]); used only where a rule needs a number.
NUMERIC_INPUTS = ["displacement", "horsepower", "weight", "acceleration", "model_year", "cylinders"]
CATEGORY_INPUT = "origin"
POLY_DEGREES = (2, 3)          # ML Guide.md section 9: degree 2 or 3 [I]

# Section 9: the 14 structural configurations (family, polynomial terms, L2)
CONFIGS = [
    ("Linear", "Linear", False, False),
    ("Linear + L2", "Linear", False, True),
    ("Linear + poly", "Linear", True, False),
    ("Linear + poly + L2", "Linear", True, True),
    ("Logistic", "Logistic", False, False),
    ("Logistic + L2", "Logistic", False, True),
    ("Logistic + poly", "Logistic", True, False),
    ("Logistic + poly + L2", "Logistic", True, True),
    ("Poisson", "Poisson", False, False),
    ("Poisson + L2", "Poisson", False, True),
    ("Exponential", "Exponential", False, False),
    ("Exponential + L2", "Exponential", False, True),
    ("kNN", "kNN", False, False),
    ("Tree", "Tree", False, False),
]

# Section 12: task gate by output type (families admissible)
TASK_GATE = {
    "numeric": {"Linear", "kNN", "Tree"},
    "count": {"Poisson", "Linear", "kNN", "Tree"},
    "non-negative real": {"Exponential", "Linear", "kNN", "Tree"},
    "binary": {"Logistic", "kNN", "Tree"},
    "multiclass": {"Logistic", "kNN", "Tree"},
}
PARAMETRIC = {"Linear", "Logistic", "Poisson", "Exponential"}


def load_data():
    rows = []
    for file_line, line in enumerate(SRC.read_text(encoding="utf-8").splitlines(), 1):
        num_part, _, name = line.partition("\t")
        rows.append([file_line] + num_part.split() + [name.strip().strip('"')])
    cols = ["file_line", "mpg", "cylinders", "displacement", "horsepower", "weight",
            "acceleration", "model_year", "origin", "car_name"]
    df = pd.DataFrame(rows, columns=cols)
    for c in cols[1:-1]:
        df[c] = pd.to_numeric(df[c].replace("?", pd.NA))
    df = df.dropna(subset=["horsepower"]).reset_index(drop=True)
    split = pd.read_csv(SPLIT)
    assert (split["file_line"].values == df["file_line"].values).all()
    return df.loc[split["set"].values == "train"].reset_index(drop=True)


def design_matrix(train, degree):
    """Inputs as recorded (DR-21), numbers as numbers (DR-19), origin one-hot with one column dropped (DR-19)."""
    cols = [np.ones(len(train))]
    for c in NUMERIC_INPUTS:
        x = train[c].to_numpy(dtype=float)
        cols.append(x)
        if degree is not None:
            for p in range(2, degree + 1):
                cols.append(x ** p)
    origin = train[CATEGORY_INPUT].astype(int).to_numpy()
    for code in (2, 3):             # code 1 dropped as the reference value
        cols.append((origin == code).astype(float))
    return np.column_stack(cols)


def mod2_collinear_or_too_many(train, family, poly, l2):
    """MOD-2: an unregularised parametric fit with parameters >= n_train or exactly collinear inputs."""
    if family not in PARAMETRIC or l2:
        return None
    degree = max(POLY_DEGREES) if poly else None
    X = design_matrix(train, degree)
    n, p = X.shape
    # Exact collinearity does not depend on scale, so each non-intercept column is standardised before the rank test
    # (unstandardised polynomial columns differ in scale by many orders of magnitude and give a false rank deficiency).
    Xs = X.copy()
    for j in range(1, p):
        sd = X[:, j].std()
        Xs[:, j] = (X[:, j] - X[:, j].mean()) / sd if sd > 0 else 0.0
    rank = int(np.linalg.matrix_rank(Xs))
    flagged = p >= n or rank < p
    return {"parameters": p, "training_rows": n, "rank_standardised": rank, "rank_unstandardised": int(np.linalg.matrix_rank(X)),
            "condition_standardised": float(np.linalg.cond(Xs)), "flagged": bool(flagged)}


def main():
    props = json.loads(PROPS.read_text(encoding="utf-8"))
    train = load_data()
    output_type = props["property_1_output_type"]
    must_haves = props["must_haves"]
    assert output_type in TASK_GATE, output_type

    rows = []
    for name, family, poly, l2 in CONFIGS:
        why = None
        mod2 = None
        if family not in TASK_GATE[output_type]:
            why = {"code": "EXCL", "reason": f"task gate: {family} is not admissible for output type '{output_type}' (section 12)"}
        else:
            if must_haves:
                why = {"code": "USER", "reason": "must-have check not implemented in this interim core for these values"}
            mod2 = mod2_collinear_or_too_many(train, family, poly, l2)
            if why is None and mod2 and mod2["flagged"]:
                why = {"code": "EXCL", "reason": "MOD-2: unregularised parametric fit with parameters >= training rows or collinear inputs"}
        rows.append({
            "configuration": name,
            "family": family,
            "polynomial_terms": poly,
            "L2": l2,
            "admissible": why is None,
            "why_not": why,
            "mod2_check": mod2,
        })

    admissible = [r["configuration"] for r in rows if r["admissible"]]
    removed = [{"configuration": r["configuration"], "code": r["why_not"]["code"], "reason": r["why_not"]["reason"]}
               for r in rows if not r["admissible"]]
    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "step": "4a admissible set",
        "code_version": f"sha256:{code_version}",
        "label": "interim core, not reviewed",
        "property_values": props,
        "training_rows": int(len(train)),
        "admissible": admissible,
        "removed": removed,
        "configurations": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("admissible:", admissible)
    for r in removed:
        print("removed:", r["configuration"], r["code"], "-", r["reason"])
    for r in rows:
        if r["mod2_check"]:
            print("MOD-2 check:", r["configuration"], r["mod2_check"])
    print("code version: sha256", code_version[:16], "...")
    print("written:", OUT)


if __name__ == "__main__":
    sys.exit(main())
