"""Interim core for the Sepsis analysis (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the analysis needs,
as literally as possible, with every [I] threshold as a named constant. Decision Records quote this
file's SHA-256 as the code version. Code/core.py belongs to the Heart Failure analysis and is not used.

Contents so far:
  input design   the preprocessing pipeline of DR-09, shared by every model family     (used from step 3)
  §11  P9, P10   properties from the training patients                                 (step 3)
  §9, §12        the 14 configurations; admissible set: task gate, must-haves,
                 MOD-1, MOD-2                                                           (step 4a)
Sections §13-§19 are added before step 4b and shown to the user then.

Reads only the training table (Code/outputs/sepsis/private/train_table.csv.gz, built by
sepsis_07_train_table.py from the patients with split == "train"). The test patients are not read.

Interpretations made in this file, where Part II does not say exactly what to do:
  a. The P9 fit uses the same input design as every candidate model (DR-09): last values with the ten
     logarithms, the training-set median filled into empty last values, the 27 "measured" indicators,
     Age, Gender, HospAdmTime and Unit one-hot encoded; then all columns standardised (as for
     Logistic and k-NN in step 4). Here the filling and scaling are fitted once on all training
     patients, because P9 is a property of the training data, not a cross-validated estimate.
  b. "Negligible regularisation" is C = 1e8 (lambda = 1e-8) in LogisticRegression, as in the
     Heart Failure core.
  c. Predicted class for the P9 accuracy: y = 1 if the probability of class 1 is > 0.5 (p. 53).
  d. MOD-2 is checked on the design matrix the parametric models would see: the DR-09 preprocessing
     fitted once on all training patients (as in a), standardised, plus an intercept column; and, for
     the "+ poly" configurations, with the powers of each numerical input up to the largest degree in
     the §16 grid (3). Numerical inputs are the 27 last values, Age and HospAdmTime; the indicators,
     Gender and Unit are categorical and get no powers (§9: powers of each numerical input).
  e. "Exactly collinear" = the design matrix has lower rank than it has columns, by numpy's
     matrix_rank at its default tolerance. Where it does, the near-zero singular directions are
     reported with the columns that carry them, so the reason can be read.
  f. Must-have gates apply only to properties the user called a must-have (P5_must_have,
     P6_must_have in the properties file); in DR-11 neither is.

Run (from Code/):
  uv run python sepsis/core.py p9p10
  uv run python sepsis/core.py admset sepsis/props_dr11.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

CODE = Path(__file__).resolve().parent.parent
OUT = CODE / "outputs" / "sepsis"
TRAIN_TABLE = OUT / "private" / "train_table.csv.gz"

TARGET = "y"

# ---- Input design (DR-09): which columns, which fixed transforms ----
CLINICAL = ["HR", "O2Sat", "Temp", "SBP", "MAP", "DBP", "Resp", "FiO2", "pH", "PaCO2", "SaO2", "AST", "BUN",
            "Alkalinephos", "Calcium", "Creatinine", "Glucose", "Lactate", "Magnesium", "Phosphate", "Potassium",
            "Bilirubin_total", "Hct", "Hgb", "PTT", "WBC", "Platelets"]                 # last value in hours 1-6
LOG_INPUTS = ["AST", "Alkalinephos", "Bilirubin_total", "Creatinine", "BUN", "Lactate", "WBC", "Glucose",
              "Platelets", "PTT"]                                                       # natural log, [I] domain judgement
MEASURED = [f"measured_{c}" for c in CLINICAL]                                          # 0/1, measured in hours 1-6
CONSTANT = ["Age", "Gender", "HospAdmTime"]
UNIT_LEVELS = ["MICU", "SICU", "unknown"]                                               # one categorical input
INPUTS = CLINICAL + MEASURED + CONSTANT + ["Unit"]
NOT_INPUTS = ["patient", "set"]                                                         # set: stratification only

# ---- [I] thresholds (ML Guide.md, Appendix to Part II) ----
P9_SEPARABLE_ACCURACY = 1.0  # separable if training accuracy reaches 100 % ...
P9_NEGLIGIBLE_C = 1e8        # ... with negligible regularisation (interpretation b)
P10_IMBALANCED_SHARE = 0.20  # imbalanced if the smallest class is < 20 % of training rows
DEFAULT_THRESHOLD = 0.5      # p. 53 (interpretation c)

LOGISTIC_MAX_ITER = 100_000

# ---- §16 grid value used by MOD-2 (interpretation d) [I] ----
GRID_DEGREE = [2, 3]

# ---- Solution space (§9) and gates (§12) ----
CONFIGS = [  # (name, family, poly, l2) -- the 14 structural configurations
    ("Linear", "Linear", False, False), ("Linear + L2", "Linear", False, True),
    ("Linear + poly", "Linear", True, False), ("Linear + poly + L2", "Linear", True, True),
    ("Logistic", "Logistic", False, False), ("Logistic + L2", "Logistic", False, True),
    ("Logistic + poly", "Logistic", True, False), ("Logistic + poly + L2", "Logistic", True, True),
    ("Poisson", "Poisson", False, False), ("Poisson + L2", "Poisson", False, True),
    ("Exponential", "Exponential", False, False), ("Exponential + L2", "Exponential", False, True),
    ("kNN", "kNN", False, False), ("Tree", "Tree", False, False),
]
CONFIG = {c[0]: {"name": c[0], "family": c[1], "poly": c[2], "l2": c[3]} for c in CONFIGS}
PARAMETRIC = {"Linear", "Logistic", "Poisson", "Exponential"}
TASK_GATE = {   # §12, P1 -> admissible families
    "numeric": ({"Linear", "kNN", "Tree"}, "[B p.17]"),
    "count": ({"Poisson", "Linear", "kNN", "Tree"}, "[B pp.17, 61–63]"),
    "non-negative real": ({"Exponential", "Linear", "kNN", "Tree"}, "[B pp.17, 63]"),
    "binary": ({"Logistic", "kNN", "Tree"}, "[B pp.17, 49–57]"),
    "multiclass": ({"Logistic", "kNN", "Tree"}, "[B pp.17, 49–57]"),
}
MUST_HAVE_GATE = {  # §12, must-have -> families that meet it ("kNN?" = only if the user accepts similar cases)
    ("P5", "inspectable"): ({"Linear", "Logistic", "Poisson", "Exponential", "Tree", "kNN?"}, "[B→I p.347]"),
    ("P5", "worst-case bound"): ({"Tree", "Logistic"}, "[B→I p.347]"),
    ("P6", "yes"): ({"Logistic"}, "[B→I pp.50, 53–54]"),
}
NUMERIC_INPUTS = CLINICAL + ["Age", "HospAdmTime"]                                      # get powers under + poly


def version() -> str:
    """SHA-256 of this file: the code version quoted in Decision Records."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def training_data() -> tuple[pd.DataFrame, pd.Series]:
    """The training patients only, with the DR-09 inputs. Raw last values; the fixed log transform,
    the filling and the encoding are steps of the pipeline."""
    df = pd.read_csv(TRAIN_TABLE)
    assert df[LOG_INPUTS].min().min() > 0, "a log input has a value <= 0"
    assert set(df.Unit.unique()) <= set(UNIT_LEVELS)
    return df[INPUTS], df[TARGET]


def preprocessor() -> ColumnTransformer:
    """DR-09 input design. Every learned step (median, encoding) is fitted on the data it is given,
    so inside cross-validation it is refitted in each fold (REQ-1). Same for every model family."""
    other_clinical = [c for c in CLINICAL if c not in LOG_INPUTS]
    return ColumnTransformer([
        ("log_then_median", Pipeline([("log", FunctionTransformer(np.log)),
                                      ("median", SimpleImputer(strategy="median"))]), LOG_INPUTS),
        ("median", SimpleImputer(strategy="median"), other_clinical),
        ("as_is", "passthrough", MEASURED + CONSTANT),
        ("unit", OneHotEncoder(categories=[UNIT_LEVELS]), ["Unit"]),
    ], verbose_feature_names_out=False)


def p9_p10(X: pd.DataFrame, y: pd.Series) -> dict:
    """§11 P9 and P10, computed on the training patients, with the DR-09 input design.

    P9: logistic regression with negligible regularisation is fitted to the training patients; the classes
    count as perfectly separable if it classifies every training patient correctly. This fit establishes
    a property only; it is not a candidate model and is not evaluated.
    P10: share of the smallest class among the training patients.
    """
    model = Pipeline([("design", preprocessor()), ("scale", StandardScaler()),
                      ("m", LogisticRegression(C=P9_NEGLIGIBLE_C, max_iter=LOGISTIC_MAX_ITER))])
    model.fit(X, y)
    pred = (model.predict_proba(X)[:, 1] > DEFAULT_THRESHOLD).astype(int)
    accuracy = float((pred == y.to_numpy()).mean())
    counts = y.value_counts().sort_index()
    smallest = float(counts.min() / counts.sum())
    n_columns = int(model.named_steps["design"].transform(X.iloc[:1]).shape[1])
    return {
        "P9": {"value": "yes" if accuracy >= P9_SEPARABLE_ACCURACY else "no",
               "training_accuracy_negligible_regularisation": accuracy,
               "C_used": P9_NEGLIGIBLE_C, "converged_iterations": int(model.named_steps["m"].n_iter_[0]),
               "max_iter": LOGISTIC_MAX_ITER, "threshold": "100 % training accuracy", "provenance": "[I] procedure"},
        "P10": {"value": "imbalanced" if smallest < P10_IMBALANCED_SHARE else "balanced",
                "smallest_class_share": smallest, "class_counts": {str(k): int(v) for k, v in counts.items()},
                "threshold": f"< {P10_IMBALANCED_SHARE:.0%}", "provenance": "[I] threshold"},
        "input_columns_after_encoding": n_columns,
        "log_inputs": LOG_INPUTS,
    }


def load_props(path: str) -> dict:
    """Property values passed to the core, copied from the latest PROP record."""
    return json.loads((CODE / path).read_text(encoding="utf-8"))


def _rank_report(D: np.ndarray, names: list[str]) -> dict:
    """Rank of D (interpretation e) and, if deficient, the columns carrying each null direction."""
    rank = int(np.linalg.matrix_rank(D))
    out = {"columns": int(D.shape[1]), "rows": int(D.shape[0]), "rank": rank}
    if rank < D.shape[1]:
        _, s, vt = np.linalg.svd(D, full_matrices=False)
        out["null_directions"] = [
            {"singular_value": float(s[i]),
             "columns": {names[j]: round(float(vt[i, j]), 3) for j in np.argsort(-np.abs(vt[i]))
                         if abs(vt[i, j]) > 0.1}}
            for i in range(rank, D.shape[1])]
    return out


def mod2_check(X: pd.DataFrame) -> dict:
    """§12 MOD-2 inputs (interpretations d, e): parameters vs n_train, and exact collinearity of the
    design matrix with intercept, without and with powers up to the largest grid degree."""
    Z = preprocessor().fit_transform(X)
    names = (LOG_INPUTS + [c for c in CLINICAL if c not in LOG_INPUTS] + MEASURED + CONSTANT
             + [f"Unit_{u}" for u in UNIT_LEVELS])                  # the column order of preprocessor()
    assert Z.shape[1] == len(names)
    num = [names.index(c) for c in NUMERIC_INPUTS]
    out = {}
    for poly in (False, True):
        cols, cnames = [Z], list(names)
        if poly:
            for d in range(2, max(GRID_DEGREE) + 1):
                cols.append(Z[:, num] ** d)
                cnames += [f"{names[j]}^{d}" for j in num]
        M = np.hstack(cols)
        D = np.hstack([np.ones((len(M), 1)), StandardScaler().fit_transform(M)])
        rep = _rank_report(D, ["intercept"] + cnames)
        rep["parameters"] = rep["columns"]
        rep["n_train"] = int(len(M))
        rep["applies"] = bool(rep["parameters"] >= rep["n_train"] or rep["rank"] < rep["columns"])
        out["poly" if poly else "plain"] = rep
    return out


def admissible_set(props: dict, X: pd.DataFrame) -> dict:
    """§12: task gate (P1), must-have gates (USER), MOD-1 (P9), MOD-2 (parameters, collinearity)."""
    families, gate_tag = TASK_GATE[props["P1"]]
    mod2 = mod2_check(X)
    admissible, removed = [], []
    for name, c in CONFIG.items():
        if c["family"] not in families:
            removed.append({"configuration": name, "code": "EXCL",
                            "evidence": f"task gate, P1 = {props['P1']}: admissible families "
                                        f"{sorted(families)} {gate_tag}"})
            continue
        failed = []
        for (prop, value), (meets, tag) in MUST_HAVE_GATE.items():
            if props.get(prop) == value and props.get(f"{prop}_must_have", False):
                ok = c["family"] in meets or (c["family"] == "kNN" and "kNN?" in meets
                                               and props.get("kNN_cases_acceptable", False))
                if not ok:
                    failed.append(f"must-have {prop} = {value} {tag}")
        if failed:
            removed.append({"configuration": name, "code": "USER", "evidence": "; ".join(failed)})
            continue
        if c["family"] == "Logistic" and not c["l2"] and props.get("P9") == "yes":
            removed.append({"configuration": name, "code": "EXCL", "evidence": "MOD-1: P9 = yes [B p.61]"})
            continue
        m2 = mod2["poly" if c["poly"] else "plain"]
        if c["family"] in PARAMETRIC and not c["l2"] and m2["applies"]:
            removed.append({"configuration": name, "code": "EXCL",
                            "evidence": f"MOD-2: {m2['parameters']} parameters, rank {m2['rank']}, "
                                        f"n_train {m2['n_train']} [B→I pp.46–47, 65]"})
            continue
        admissible.append(name)
    return {"properties_used": props,
            "task_gate": {"P1": props["P1"], "families": sorted(families), "provenance": gate_tag},
            "must_haves": {k: props.get(k, False) for k in ("P5_must_have", "P6_must_have")},
            "MOD-1": {"P9": props.get("P9"), "applies": props.get("P9") == "yes", "provenance": "[B p.61]"},
            "MOD-2": {**mod2, "provenance": "[B→I pp.46–47, 65]"},
            "admissible": admissible, "removed": removed}


def write(name: str, result: dict) -> None:
    result = {"core_version_sha256": version(), **result}
    (OUT / name).write_text(json.dumps(result, indent=2, default=float), encoding="utf-8")
    print(json.dumps(result, indent=2, default=float))


def main(argv: list[str]) -> None:
    args = argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "p9p10":
        X, y = training_data()
        write("core_p9_p10.json", {"rows_used": "training patients only", "n_train": int(len(y)),
                                   "inputs": INPUTS, **p9_p10(X, y)})
    elif args[0] == "admset" and len(args) == 2:
        X, y = training_data()
        write("core_admset.json", {"rows_used": "training patients only", "n_train": int(len(y)),
                                   "properties_file": args[1], **admissible_set(load_props(args[1]), X)})
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
