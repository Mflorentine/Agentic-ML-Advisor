"""Interim core for the Sepsis analysis (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the analysis needs,
as literally as possible, with every [I] threshold as a named constant. Decision Records quote this
file's SHA-256 as the code version. Code/core.py belongs to the Heart Failure analysis and is not used.

Contents so far:
  input design   the preprocessing pipeline of DR-09, shared by every model family     (used from step 3)
  §11  P9, P10   properties from the training patients                                 (step 3)
  §9, §12        the 14 configurations; admissible set: task gate, must-haves,
                 MOD-1, MOD-2                                                           (step 4a)
  §13-§15        matrix score, order, keep, simple-first (SEQ-2)                       (step 4b)
  §16            nested CV: outer 10 / inner 5, stratified by outcome x hospital,
                 the same folds for every configuration, PR-AUC as the metric          (steps 4c-4e)
  §18            observations O1-O6 and the learning curve, errors as 1 - PR-AUC       (step 4e)
  §16, §17, §19  decision threshold (P6 = yes), C1-C3, recommendation, why-not codes   (step 4f)
  §19.4          the single test-set evaluation                                        (step 4g)

Only the classification families (Logistic, k-NN, Tree) have estimators, because sub-task 1 is
binary; §12 and §13 cover all 14 configurations, so the others are excluded and coded, never fitted.

Reads only the training table (Code/outputs/sepsis/private/train_table.csv.gz, built by
sepsis_07_train_table.py from the patients with split == "train"). The test patients are read in one
place only, `final`, which needs the user's approval quoted on the command line, refuses to run a
second time, and refuses to run if this file changed since `recommend`. Its input,
private/test_table.csv.gz, does not exist yet: it is built at step 4g, after approval.

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
  g. Inner tuning uses the deciding metric, PR-AUC as average precision (DR-05, §16 "selection
     metric"), computed from the predicted probability of class 1.
  h. Folds: outer and inner folds are stratified by the four strata outcome x hospital (§16
     further-variable rule, DR-08), shuffled with CV_SEED = 2026. The inner folds are made within
     each outer training fold. The outer fold of every training patient is stored, with the training
     table's checksum, and every later run checks it is unchanged.
  i. Polynomial terms (+ poly): each numerical input, after the DR-09 log and median, is centred and
     scaled on the training fold, then raised to powers 2..degree; no products. With an intercept
     this spans the same functions as raw powers (as checked in MOD-2), but under L2 the penalty
     acts on the coefficients of the standardised powers.
  j. Diagnosis errors (§16, P10 = imbalanced): E_train = 1 - PR-AUC on the outer training fold,
     E_val = 1 - PR-AUC on the outer validation fold. The baseline's constant score gives a PR-AUC
     equal to the fold's positive rate.
  k. Spread = sample standard deviation (ddof = 1) of the 10 fold differences.
  l. A margin of exactly 0 is never "clear" or "moderate", even when the spread is 0.
  m. Learning-curve subsets are drawn within each outer training fold, stratified by outcome x
     hospital, with CV_SEED.
  n. C3 "its fold SD" = the SD across the 10 outer folds of E_val at 100 % of the training data.
  o. O2: the success criterion is test PR-AUC > positive rate + fold SD of PR-AUC (DR-05). On the
     training side, O2 holds if E_train >= 1 - (training positive rate + the leading configuration's
     fold SD of PR-AUC), i.e. its training PR-AUC does not clear that level.
  p. Decision threshold (P6 = yes; trade-off F2, DR-05): the r in THRESHOLD_GRID (0.005 to 0.500 in
     steps of 0.005, because with 3 % positives the probabilities are small) that maximises F2 on
     inner out-of-fold probabilities; ties go to the r closest to 0.5. Its CV estimate is nested: r
     is chosen inside each outer training fold and scored on that outer validation fold, with
     precision and recall. The trade-off is confirmed with the user at 4f before it is used.
  q. O5 ignores the polynomial degree: §9 fixes it to {2, 3}, so both values are edges and the grid
     cannot be extended.
  r. Final hyperparameters: the most common setting across the outer folds (the value the CV table
     reports), as the Heart Failure analysis settled (its DR-19), not a new grid search on all rows.
  s. All inputs, including the 0/1 indicators, are standardised before Logistic and k-NN (REQ-2,
     REQ-3). The tree gets the DR-09 design unscaled.

Run (from Code/):
  uv run python sepsis/core.py p9p10
  uv run python sepsis/core.py admset    sepsis/props_dr11.json
  uv run python sepsis/core.py prior     sepsis/props_dr11.json
  uv run python sepsis/core.py cv round1 sepsis/props_dr11.json
  uv run python sepsis/core.py cv round2 sepsis/props_dr11.json
  uv run python sepsis/core.py cv add "<configuration>" [--drop COL ...] [--grid JSON] [--label TEXT]
  uv run python sepsis/core.py diagnose "<cv entry label>"
  uv run python sepsis/core.py recommend sepsis/props_dr11.json
  uv run python sepsis/core.py final --approved "<the user's words>"
  uv run python sepsis/core.py explain   (§21: verified rebuild of the final model; writes its weights)
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix, fbeta_score, precision_recall_curve
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

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

# ---- §16 grids [I] ----
GRID_DEGREE = [2, 3]
GRID_K = [1, 3, 5, 7, 9, 15, 21, 31, 51]
GRID_DEPTH = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]
GRID_MIN_LEAF = [1, 5, 10, 20]
GRID_LAMBDA = [10.0 ** e for e in range(-4, 5)]

# ---- Metric (DR-05) ----
BETA = 2.0                   # F2, monitored and used for the decision threshold (p. 92)

# ---- [I] thresholds (ML Guide.md, Appendix to Part II) ----
KEEP_TOP_OTHERS = 3          # §15: kept besides baseline and simple-first (plus ties)
OUTER_FOLDS = 10             # §16
INNER_FOLDS = 5              # §16
C1_CLEAR = 1.0               # §17: margin >= 1 x spread -> clear
C1_MODERATE = 0.5            # §17: 0.5-1 x spread -> moderate; below -> none
C2_CLEAR = 1.0               # §17: margin over the baseline >= 1 x spread -> clear
C3_FALLING = 0.5             # §17: E_val(80 %) - E_val(100 %) >= 0.5 x fold SD -> limited
WITHIN_NOISE = 0.5           # §19: margin < 0.5 x spread -> candidate
BREADTH_MANY = 10            # §17 breadth note: more than 10 configurations compared
O3_RATIO = 2.0               # §18: gap >= 2 x E_train -> overfitting
O4_RATIO = 2.0               # §18: E_train >= 2 x gap -> underfitting
O5_MOST_FOLDS = 0.5          # §18: "most outer folds" = more than half
LC_FRACTIONS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]   # §16 learning curve

# ---- Choices made for this analysis, not thresholds in the guide ----
CV_SEED = 2026               # outer and inner folds, learning-curve subsets, tree tie-breaks
SPREAD_DDOF = 1              # interpretation k
THRESHOLD_GRID = [round(0.005 * i, 3) for i in range(1, 101)]   # 0.005 ... 0.500, interpretation p
N_JOBS = -1                  # parallel grid search; does not change results

BASELINE = "Baseline (flag nobody)"                          # §14 SEQ-1, DR-05
SIMPLE_FIRST = {"numeric": "Linear", "count": "Poisson", "non-negative real": "Exponential",
                "binary": "Logistic", "multiclass": "Logistic"}   # §14 SEQ-2

# §13 matrix: (property, values, column, score, tag, condition). Columns: family names,
# "GLM" (Poisson, Exponential), "poly", "L2". A P5/P6 entry applies only when not a must-have.
MATRIX = [
    ("P1", ("count", "non-negative real"), "Linear", -1, "[B p.62]", None),
    ("P1", ("count", "non-negative real"), "GLM", +1, "[B pp.61–62]", None),
    ("P2", ("limited",), "Tree", -1, "[I]", None),
    ("P2", ("limited",), "poly", -1, "[B→I pp.59–60]", None),
    ("P2", ("limited",), "L2", +1, "[B→I p.60]", None),
    ("P3", ("many",), "kNN", -1, "[I]", None),
    ("P3", ("many",), "poly", -1, "[B→I p.59]", None),
    ("P4", ("high",), "kNN", -1, "[I]", None),
    ("P5", ("inspectable",), "Linear", +1, "[B→I p.347]", "not_must_have"),
    ("P5", ("inspectable",), "Logistic", +1, "[B→I p.347]", "not_must_have"),
    ("P5", ("inspectable",), "GLM", +1, "[B→I p.347]", "not_must_have"),
    ("P5", ("inspectable",), "Tree", +1, "[B→I p.347]", "not_must_have"),
    ("P5", ("inspectable",), "poly", -1, "[I]", "not_must_have"),
    ("P5", ("worst-case bound",), "Logistic", +1, "[B→I p.347]", "not_must_have"),
    ("P5", ("worst-case bound",), "Tree", +1, "[B→I p.347]", "not_must_have"),
    ("P6", ("yes",), "Logistic", +1, "[B→I pp.50, 53–54]", "not_must_have"),
    ("P7", ("yes",), "kNN", -1, "[B→I p.26]", None),
    ("P7", ("yes",), "Tree", -1, "[I]", None),
    ("P8", ("linear",), "Linear", +1, "[B→I p.41]", None),
    ("P8", ("linear",), "Logistic", +1, "[B→I p.55]", None),
    ("P8", ("linear",), "GLM", +1, "[B→I p.63]", None),
    ("P8", ("curved",), "Linear", -1, "[B→I pp.58–59]", None),
    ("P8", ("curved",), "kNN", +1, "[B→I p.26]", None),
    ("P8", ("curved",), "poly", +1, "[B→I p.59]", None),
    ("P8", ("interactions/irregular",), "Linear", -1, "[B→I p.41]", None),
    ("P8", ("interactions/irregular",), "Logistic", -1, "[B→I p.55]", None),
    ("P8", ("interactions/irregular",), "GLM", -1, "[B→I p.63]", None),
    ("P8", ("interactions/irregular",), "kNN", +1, "[B→I p.24]", None),
    ("P8", ("interactions/irregular",), "Tree", +1, "[B→I pp.27–29]", None),
]

STORE = OUT / "core_cv_store.json"
TEST_TABLE = OUT / "private" / "test_table.csv.gz"           # built only at step 4g, after approval

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


def preprocessor(drop: tuple = ()) -> ColumnTransformer:
    """DR-09 input design. Every learned step (median, encoding) is fitted on the data it is given,
    so inside cross-validation it is refitted in each fold (REQ-1). Same for every model family.
    `drop` removes inputs (§18 DX-4 backward elimination only); by default nothing is dropped."""
    keep = lambda cols: [c for c in cols if c not in drop]                      # noqa: E731
    other_clinical = [c for c in CLINICAL if c not in LOG_INPUTS]
    parts = [
        ("log_then_median", Pipeline([("log", FunctionTransformer(np.log)),
                                      ("median", SimpleImputer(strategy="median"))]), keep(LOG_INPUTS)),
        ("median", SimpleImputer(strategy="median"), keep(other_clinical)),
        ("as_is", "passthrough", keep(MEASURED)),
        # DR-19 (27 October 2026): Age, Gender, HospAdmTime filled with the training(-fold) median, as the
        # clinical columns are; no training patient has one empty, so training results do not change
        ("constant_median", SimpleImputer(strategy="median"), keep(CONSTANT)),
        ("unit", OneHotEncoder(categories=[UNIT_LEVELS]), keep(["Unit"])),
    ]
    return ColumnTransformer([p for p in parts if p[2]], verbose_feature_names_out=False)


def design_names(drop: tuple = ()) -> list[str]:
    """Column names of preprocessor(drop)'s output, in its order."""
    keep = lambda cols: [c for c in cols if c not in drop]                      # noqa: E731
    unit = [f"Unit_{u}" for u in UNIT_LEVELS] if "Unit" not in drop else []
    return (keep(LOG_INPUTS) + keep([c for c in CLINICAL if c not in LOG_INPUTS]) + keep(MEASURED + CONSTANT)
            + unit)


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


# ======================================================================================
# §13, §14, §15 prior ranking
# ======================================================================================

def addons(name: str) -> int:
    c = CONFIG[name]
    return int(c["poly"]) + int(c["l2"])


def columns_of(name: str) -> set[str]:
    c = CONFIG[name]
    cols = {"GLM" if c["family"] in ("Poisson", "Exponential") else c["family"]}
    if c["poly"]:
        cols.add("poly")
    if c["l2"]:
        cols.add("L2")
    return cols


def matrix_score(name: str, props: dict) -> tuple[int, list[dict]]:
    """§13: family column + `poly` column + `L2` column, over the properties whose value is known."""
    entries = []
    for prop, values, col, score, tag, cond in MATRIX:
        if props.get(prop) not in values or col not in columns_of(name):
            continue
        if cond == "not_must_have" and props.get(f"{prop}_must_have", False):
            continue
        entries.append({"entry": f"{prop}={props[prop]}→{col}", "score": score, "provenance": tag})
    return sum(e["score"] for e in entries), entries


def simple_first(props: dict, admissible: list[str]) -> str:
    """§14 SEQ-2: the plain parametric model for the task, or its + L2 version if MOD-1 or MOD-2
    removed the plain one."""
    plain = SIMPLE_FIRST[props["P1"]]
    return plain if plain in admissible else f"{plain} + L2"


def prior_ranking(props: dict, adm: dict) -> dict:
    """§15: score, order (score, then fewer add-ons, then shared rank), keep (simple-first + top 3
    others + ties at the cut); everything not kept gets DISF."""
    rows = []
    for name in adm["admissible"]:
        score, entries = matrix_score(name, props)
        rows.append({"configuration": name, "score": score, "addons": addons(name), "entries": entries})
    rows.sort(key=lambda r: (-r["score"], r["addons"]))
    rank, prev = 0, None
    for i, r in enumerate(rows):
        key = (r["score"], r["addons"])
        rank = rank if key == prev else i + 1
        r["rank"], prev = rank, key
    sf = simple_first(props, adm["admissible"])
    others = [r for r in rows if r["configuration"] != sf]
    if len(others) > KEEP_TOP_OTHERS:
        cut_rank = others[KEEP_TOP_OTHERS - 1]["rank"]
        kept_others = [r for r in others if r["rank"] <= cut_rank]
    else:
        kept_others = others
    kept = [sf] + [r["configuration"] for r in kept_others]
    for r in rows:
        r["kept"] = r["configuration"] in kept
        r["role"] = "simple-first (SEQ-2)" if r["configuration"] == sf else ("kept" if r["kept"] else "DISF")
    return {"order": rows, "simple_first": sf, "kept": kept, "baseline": BASELINE,
            "not_kept": [{"configuration": r["configuration"], "code": "DISF", "score": r["score"],
                          "entries": r["entries"]} for r in rows if not r["kept"]]}


# ======================================================================================
# Estimators and pipelines (§9 implementation notes, REQ-1 to REQ-6)
# ======================================================================================

class SeparatePowers(TransformerMixin, BaseEstimator):
    """§9 `poly`: powers 2..degree of each numerical input separately, no products [I].
    Centring and scaling are fitted on the training fold (REQ-1); interpretation i."""

    def __init__(self, idx: tuple = (), degree: int = 2):
        self.idx = idx
        self.degree = degree

    def fit(self, X, y=None):
        Z = np.asarray(X, dtype=float)[:, list(self.idx)]
        self.mean_ = Z.mean(axis=0)
        self.scale_ = np.where(Z.std(axis=0) > 0, Z.std(axis=0), 1.0)
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=float)
        Z = (X[:, list(self.idx)] - self.mean_) / self.scale_
        return np.hstack([X] + [Z ** p for p in range(2, self.degree + 1)])


class BookLogistic(ClassifierMixin, BaseEstimator):
    """Logistic regression with the book's L2 penalty lambda*||theta||^2 (eq. 3.50, p. 61).
    scikit-learn minimises (1/n) sum(loss) + ||w||^2 / (2 C n), intercept unpenalised (REQ-5), so
    C = 1/(2 n lambda); checked against eq. 3.50 in the Heart Failure analysis with the same
    scikit-learn version (Code/06_check_eq350.py). lam=None is unregularised (C = inf);
    scikit-learn's default C = 1.0 is never used (§9)."""

    def __init__(self, lam: float | None = None):
        self.lam = lam

    def fit(self, X, y):
        n = len(y)
        self.C_ = np.inf if self.lam is None else 1.0 / (2.0 * n * self.lam)
        self.model_ = LogisticRegression(C=self.C_, max_iter=LOGISTIC_MAX_ITER).fit(X, y)
        self.classes_ = self.model_.classes_
        self.converged_ = bool(self.model_.n_iter_[0] < LOGISTIC_MAX_ITER)
        return self

    def predict_proba(self, X):
        return self.model_.predict_proba(X)

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] > DEFAULT_THRESHOLD).astype(int)


def build(name: str, n_inner_train: int, drop: tuple = (), grid_override: dict | None = None):
    """Pipeline and grid for one configuration. The DR-09 design is the first step, so every learned
    preprocessing step is refitted on each training fold (REQ-1)."""
    c = CONFIG[name]
    names = design_names(drop)
    num_idx = tuple(i for i, col in enumerate(names) if col in NUMERIC_INPUTS)
    steps = [("design", preprocessor(drop))]                                    # REQ-1, REQ-6
    grid: dict = {}
    if c["family"] == "Logistic":
        if c["poly"]:
            steps.append(("poly", SeparatePowers(num_idx)))
            grid["poly__degree"] = GRID_DEGREE                                  # REQ-4
        steps.append(("scale", StandardScaler()))                               # REQ-3
        steps.append(("m", BookLogistic(lam=None)))
        if c["l2"]:
            grid["m__lam"] = GRID_LAMBDA                                        # REQ-4
    elif c["family"] == "kNN":
        steps.append(("scale", StandardScaler()))                               # REQ-2
        steps.append(("m", KNeighborsClassifier()))
        grid["m__n_neighbors"] = [k for k in GRID_K if k < n_inner_train]       # REQ-4
    elif c["family"] == "Tree":
        steps.append(("m", DecisionTreeClassifier(random_state=CV_SEED)))
        grid["m__max_depth"] = GRID_DEPTH                                       # REQ-4, never fully grown
        grid["m__min_samples_leaf"] = GRID_MIN_LEAF
    else:
        raise NotImplementedError(f"{name}: no estimator in this interim core (regression family)")
    if grid_override:
        grid.update(grid_override)
    return Pipeline(steps), grid


# ======================================================================================
# Data, metrics and folds
# ======================================================================================

def training_cv() -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """Training patients: inputs, outcome, and the stratum outcome x hospital (§16, DR-08)."""
    df = pd.read_csv(TRAIN_TABLE)
    X, y = training_data()
    strata = (2 * (df["set"].to_numpy() == "B") + y.to_numpy()).astype(int)
    return X, y.to_numpy(), strata


def table_sha() -> str:
    return hashlib.sha256(TRAIN_TABLE.read_bytes()).hexdigest()


def prob1(model, X) -> np.ndarray:
    return model.predict_proba(X)[:, 1]


def pr_auc(y, p) -> float:
    """The deciding metric (DR-05): PR-AUC computed as average precision [I]."""
    return float(average_precision_score(y, p))


def ap_scorer(model, X, y) -> float:
    """Inner tuning score: the deciding metric (§16 selection metric), interpretation g."""
    return pr_auc(y, prob1(model, X))


def f2(y, pred) -> float:
    return float(fbeta_score(y, pred, beta=BETA, zero_division=0))


def prec_rec(y, pred) -> tuple[float, float]:
    tp = int(((pred == 1) & (y == 1)).sum())
    return (tp / int(pred.sum()) if pred.sum() else float("nan")), (tp / int(y.sum()) if y.sum() else float("nan"))


def outer_folds(strata: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    """§16: 10 outer folds, shuffled, stratified by outcome x hospital (§16 further variable)."""
    skf = StratifiedKFold(OUTER_FOLDS, shuffle=True, random_state=CV_SEED)
    return list(skf.split(np.zeros(len(strata)), strata))


def inner_splits(strata: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    """§16: 5 inner folds within a training fold, stratified the same way."""
    skf = StratifiedKFold(INNER_FOLDS, shuffle=True, random_state=CV_SEED)
    return list(skf.split(np.zeros(len(strata)), strata))


def n_inner_train(n: int) -> int:
    return n - math.ceil(n / INNER_FOLDS)


def margin(a: list[float], b: list[float]) -> tuple[float, float]:
    """§16: mean and SD (spread) of the fold differences a - b; interpretation k."""
    d = np.asarray(a) - np.asarray(b)
    return float(d.mean()), float(d.std(ddof=SPREAD_DDOF))


def level(m: float, s: float, clear: float, moderate: float | None = None) -> str:
    """§17 levels; interpretation l: a margin of 0 or below is never clear or moderate."""
    if m > 0 and m >= clear * s:
        return "clear"
    if moderate is not None and m > 0 and m >= moderate * s:
        return "moderate"
    return "none" if moderate is not None else "not clear"


def fit_search(name: str, X: pd.DataFrame, y: np.ndarray, strata: np.ndarray, drop: tuple = (),
               grid_override: dict | None = None):
    """Inner grid search on one training fold (REQ-4), refitted on the whole training fold."""
    pipe, grid = build(name, n_inner_train(len(y)), drop, grid_override)
    search = GridSearchCV(pipe, grid, scoring=ap_scorer, cv=inner_splits(strata), refit=True,
                          n_jobs=N_JOBS, error_score="raise")
    search.fit(X, y)
    m = search.best_estimator_.named_steps["m"]
    converged = getattr(m, "converged_", None)
    return search, search.best_params_, grid, converged


# ======================================================================================
# §16 nested cross-validation, cumulative store
# ======================================================================================

def load_store(strata: np.ndarray) -> dict:
    fold_of_row = np.zeros(len(strata), dtype=int)
    for f, (_, va) in enumerate(outer_folds(strata)):
        fold_of_row[va] = f
    if STORE.exists():
        store = json.loads(STORE.read_text(encoding="utf-8"))
        if store["train_table_sha256"] != table_sha() or store["outer_fold_of_row"] != fold_of_row.tolist():
            sys.exit("training table or outer folds differ from the stored ones; refusing to mix them")
        return store
    return {"cv_seed": CV_SEED, "outer_folds": OUTER_FOLDS, "inner_folds": INNER_FOLDS,
            "stratified_by": "outcome x hospital", "train_table_sha256": table_sha(),
            "outer_fold_of_row": fold_of_row.tolist(), "entries": {}}


def baseline_cv(y: np.ndarray, strata: np.ndarray) -> dict:
    """§14 SEQ-1: flag nobody. A constant score, so its PR-AUC is the fold's positive rate."""
    rows = []
    for f, (tr, va) in enumerate(outer_folds(strata)):
        ap_tr, ap_va = pr_auc(y[tr], np.zeros(len(tr))), pr_auc(y[va], np.zeros(len(va)))
        rows.append({"fold": f, "best_params": {}, "ap_train": ap_tr, "ap_val": ap_va,
                     "e_train": 1 - ap_tr, "e_val": 1 - ap_va, "converged": None,
                     "positive_rate_val": float(y[va].mean())})
    return {"configuration": BASELINE, "structural": None, "post_prior": False, "dropped_inputs": [],
            "grid": {}, "pipeline": "constant score 0 (flag nobody)", "folds": rows}


def nested_cv(name: str, X: pd.DataFrame, y: np.ndarray, strata: np.ndarray, drop: list[str],
              grid_override: dict | None, post_prior: bool) -> dict:
    """§16: inner 5-fold grid search on PR-AUC within each of the 10 outer training folds; the
    diagnosis errors are 1 - PR-AUC because P10 = imbalanced (§16, interpretation j)."""
    rows, grid_seen, pipe_repr = [], None, None
    for f, (tr, va) in enumerate(outer_folds(strata)):
        search, params, grid, converged = fit_search(name, X.iloc[tr], y[tr], strata[tr], tuple(drop),
                                                     grid_override)
        ap_tr, ap_va = pr_auc(y[tr], prob1(search, X.iloc[tr])), pr_auc(y[va], prob1(search, X.iloc[va]))
        rows.append({"fold": f, "best_params": params, "grid_used": grid, "ap_train": ap_tr, "ap_val": ap_va,
                     "e_train": 1 - ap_tr, "e_val": 1 - ap_va, "converged": converged,
                     "grid_override": grid_override})
        grid_seen, pipe_repr = grid, repr(search.best_estimator_)
        print(f"  {name}: fold {f} PR-AUC val {ap_va:.4f} {params}", file=sys.stderr)
    return {"configuration": name, "structural": name, "post_prior": post_prior, "dropped_inputs": drop,
            "grid": grid_seen, "pipeline": pipe_repr, "folds": rows}


def fold_values(entry: dict, key: str) -> list[float]:
    return [r[key] for r in entry["folds"]]


def most_common_params(entry: dict) -> dict:
    counts = Counter(json.dumps(r["best_params"], sort_keys=True) for r in entry["folds"])
    params, n = counts.most_common(1)[0]
    return {"params": json.loads(params), "folds": f"{n}/{len(entry['folds'])}"}


def cv_table(store: dict) -> dict:
    entries = store["entries"]
    models = [k for k in entries if k != BASELINE]
    means = {k: float(np.mean(fold_values(entries[k], "ap_val"))) for k in entries}
    leader = max(models, key=lambda k: means[k]) if models else None
    rows = []
    for k, e in entries.items():
        row = {"configuration": k, "post_prior": e["post_prior"], "round": e.get("round"),
               "tuned_hyperparameters": most_common_params(e) if k != BASELINE else "n/a",
               "cv_mean_pr_auc": means[k],
               "fold_sd_pr_auc": float(np.std(fold_values(e, "ap_val"), ddof=SPREAD_DDOF)),
               "e_train": float(np.mean(fold_values(e, "e_train"))),
               "e_val": float(np.mean(fold_values(e, "e_val"))),
               "not_converged_folds": sum(1 for r in e["folds"] if r["converged"] is False)}
        if leader and k != leader:
            m, s = margin(fold_values(e, "ap_val"), fold_values(entries[leader], "ap_val"))
            row["margin_vs_leader"] = {"mean": m, "spread": s}
        if BASELINE in entries and k != BASELINE:
            m, s = margin(fold_values(e, "ap_val"), fold_values(entries[BASELINE], "ap_val"))
            row["margin_vs_baseline"] = {"mean": m, "spread": s, "C2": level(m, s, C2_CLEAR)}
        rows.append(row)
    return {"metric": "PR-AUC (average precision)", "leader": leader, "rows": rows}


def run_cv(store: dict, names: list[str], round_label: str, X, y, strata, drop=(), grid_override=None,
           post_prior=False, label=None) -> dict:
    added = []
    for name in names:
        key = label or name
        if key in store["entries"]:
            sys.exit(f"'{key}' is already cross-validated; give a new --label for a variant")
        entry = baseline_cv(y, strata) if name == BASELINE else nested_cv(
            name, X, y, strata, list(drop), grid_override, post_prior)
        entry["round"] = round_label
        store["entries"][key] = entry
        STORE.write_text(json.dumps(store, indent=1, default=float), encoding="utf-8")
        added.append(key)
    return {"round": round_label, "added": added, "table": cv_table(store)}


# ======================================================================================
# §18 observations and learning curve
# ======================================================================================

def learning_curve(entry: dict, X, y, strata) -> dict:
    """§16: training fractions 10 %..100 % on the outer folds, nested tuning at each size; errors are
    1 - PR-AUC (§16, P10 = imbalanced). Subsets keep the outcome x hospital mix (interpretation m)."""
    drop = tuple(entry["dropped_inputs"])
    override = entry["folds"][0].get("grid_override")
    out = []
    for frac in LC_FRACTIONS:
        e_tr, e_va = [], []
        for tr, va in outer_folds(strata):
            sub = tr if frac == 1.0 else train_test_split(tr, train_size=frac, stratify=strata[tr],
                                                          random_state=CV_SEED)[0]
            search, _, _, _ = fit_search(entry["structural"], X.iloc[sub], y[sub], strata[sub], drop, override)
            e_tr.append(1 - pr_auc(y[sub], prob1(search, X.iloc[sub])))
            e_va.append(1 - pr_auc(y[va], prob1(search, X.iloc[va])))
        out.append({"fraction": frac, "e_train_mean": float(np.mean(e_tr)), "e_val_mean": float(np.mean(e_va)),
                    "e_val_fold_sd": float(np.std(e_va, ddof=SPREAD_DDOF))})
        print(f"  learning curve {frac:.0%}: E_val {out[-1]['e_val_mean']:.4f}", file=sys.stderr)
    at = {r["fraction"]: r for r in out}
    drop_80_100 = at[0.8]["e_val_mean"] - at[1.0]["e_val_mean"]
    c3 = "limited" if drop_80_100 >= C3_FALLING * at[1.0]["e_val_fold_sd"] else "adequate"   # interpretation n
    return {"points": out, "C3": {"value": c3, "e_val_80_minus_100": drop_80_100,
                                  "threshold": f">= {C3_FALLING} x fold SD at 100 % "
                                               f"({at[1.0]['e_val_fold_sd']:.4f})"}}


def observations(key: str, store: dict, X, y, strata) -> dict:
    e = store["entries"][key]
    table = {r["configuration"]: r for r in cv_table(store)["rows"]}[key]
    e_train, e_val = table["e_train"], table["e_val"]
    gap = e_val - e_train
    c2 = table["margin_vs_baseline"]["C2"]
    rate = float(y.mean())
    o5 = {}
    for p in (e["grid"] or {}):
        if p == "poly__degree":                                                # interpretation q
            continue
        edges = sum(r["best_params"][p] in (min(r["grid_used"][p]), max(r["grid_used"][p])) for r in e["folds"])
        o5[p] = {"folds_at_edge": edges, "holds": edges > O5_MOST_FOLDS * len(e["folds"])}
    lc = learning_curve(e, X, y, strata)
    criterion = rate + table["fold_sd_pr_auc"]                                 # interpretation o
    obs = {
        "O1": {"holds": c2 != "clear", "C2": c2, "vs": BASELINE},
        "O2": {"holds": e_train >= 1 - criterion, "e_train": e_train,
               "compared_with": f"1 - (training positive rate {rate:.4f} + fold SD {table['fold_sd_pr_auc']:.4f})",
               "note": "interpretation o"},
        "O3": {"holds": gap >= O3_RATIO * e_train, "gap": gap, "e_train": e_train},
        # §18 O4, P10 = imbalanced (errors are 1 - PR-AUC): ratio test AND the O2 comparison
        # [B→I pp.331, 333, 335] (ML Guide.md version note, 27 October 2026)
        "O4": {"holds": bool(e_train >= O4_RATIO * gap and e_train >= 1 - criterion),
               "ratio_test": bool(e_train >= O4_RATIO * gap), "o2_comparison": bool(e_train >= 1 - criterion),
               "gap": gap, "e_train": e_train},
        "O5": {"holds": any(v["holds"] for v in o5.values()), "by_parameter": o5},
        "O6": {"holds": lc["C3"]["value"] == "limited", "C3": lc["C3"]},
    }
    order = ["O1", "O2", "O5", "O3", "O4", "O6"]                                # §18 priority
    first = next((o for o in order if obs[o]["holds"]), None)
    return {"configuration": key, "error": "1 - PR-AUC (P10 = imbalanced)", "e_train": e_train,
            "e_val": e_val, "gap": gap, "observations": obs, "priority_order": order,
            "first_that_holds": first, "learning_curve": lc["points"]}


# ======================================================================================
# §16 decision threshold, §17 confidence, §19 recommendation, §20 why-not
# ======================================================================================

def choose_threshold(y: np.ndarray, p: np.ndarray) -> float:
    """Interpretation p: the r in THRESHOLD_GRID maximising F2 (the user's trade-off, DR-05);
    ties go to the r closest to 0.5. Predicted class: y = 1 if p > r (p. 53)."""
    scores = [(f2(y, (p > r).astype(int)), -abs(r - DEFAULT_THRESHOLD), r) for r in THRESHOLD_GRID]
    return max(scores)[2]


def oof_probabilities(name, X, y, strata, params, drop, override) -> np.ndarray:
    oof = np.zeros(len(y))
    for itr, iva in inner_splits(strata):
        pipe, _ = build(name, n_inner_train(len(y)), drop, override)
        model = clone(pipe).set_params(**params).fit(X.iloc[itr], y[itr])
        oof[iva] = prob1(model, X.iloc[iva])
    return oof


def tune_threshold(entry: dict, X, y, strata, final_params: dict) -> dict:
    """§16, P6 = yes: r is chosen inside each outer training fold on inner out-of-fold probabilities
    and scored on that outer validation fold (nested); the final r on all training patients."""
    name, drop = entry["structural"], tuple(entry["dropped_inputs"])
    override = entry["folds"][0].get("grid_override")
    per_fold = []
    for (tr, va), r in zip(outer_folds(strata), entry["folds"]):
        params = r["best_params"]
        thr = choose_threshold(y[tr], oof_probabilities(name, X.iloc[tr], y[tr], strata[tr], params, drop, override))
        pipe, _ = build(name, n_inner_train(len(tr)), drop, override)
        model = clone(pipe).set_params(**params).fit(X.iloc[tr], y[tr])
        pred = (prob1(model, X.iloc[va]) > thr).astype(int)
        pr, rc = prec_rec(y[va], pred)
        per_fold.append({"threshold": thr, "f2_val": f2(y[va], pred), "precision_val": pr, "recall_val": rc})
    final_thr = choose_threshold(y, oof_probabilities(name, X, y, strata, final_params, drop, override))
    summ = lambda k: {"mean": float(np.nanmean([r[k] for r in per_fold])),            # noqa: E731
                      "sd": float(np.nanstd([r[k] for r in per_fold], ddof=SPREAD_DDOF))}
    return {"trade_off": "F2 (DR-05)", "grid": [THRESHOLD_GRID[0], THRESHOLD_GRID[-1], "step 0.005"],
            "per_fold": per_fold, "f2": summ("f2_val"), "precision": summ("precision_val"),
            "recall": summ("recall_val"), "final_threshold": final_thr}


def recommend(props: dict, X, y, strata) -> dict:
    store = load_store(strata)
    entries = store["entries"]
    adm = admissible_set(props, X)
    prior = prior_ranking(props, adm)
    models = [k for k in entries if k != BASELINE]
    f = {k: fold_values(entries[k], "ap_val") for k in entries}
    mean = {k: float(np.mean(v)) for k, v in f.items()}
    struct = {k: entries[k]["structural"] for k in models}
    score = {k: matrix_score(struct[k], props)[0] for k in models}

    # §19.1 eligible: C2 = clear (no must-haves in DR-11)
    c2 = {k: level(*margin(f[k], f[BASELINE]), C2_CLEAR) for k in models}
    eligible = [k for k in models if c2[k] == "clear"]
    trace = {"1_eligible": {k: {"C2": c2[k], "margin_vs_baseline": margin(f[k], f[BASELINE])} for k in models}}
    if not eligible:
        return {"recommendation": None,
                "reason": "no configuration clearly beats the baseline (§19.1): DX-1 or DX-2", "trace": trace}
    # §19.2 candidates
    best = max(eligible, key=lambda k: mean[k])
    cands = [best] + [k for k in eligible if k != best
                      and margin(f[best], f[k])[0] < WITHIN_NOISE * margin(f[best], f[k])[1]]
    trace["2_candidates"] = {k: {"cv_mean": mean[k], "margin_best_minus_this":
                                 margin(f[best], f[k]) if k != best else (0.0, 0.0)} for k in cands}
    # §19.3 choose: fewest add-ons, then higher prior score, then better CV mean
    rec = min(cands, key=lambda k: (addons(struct[k]), -score[k], -mean[k]))
    trace["3_choice"] = {k: {"addons": addons(struct[k]), "prior_score": score[k], "cv_mean": mean[k]}
                         for k in cands}
    trace["3_chosen"] = rec

    # §17 confidence
    others = [k for k in models if k != rec]
    runner = max(others, key=lambda k: mean[k]) if others else None
    m1, s1 = margin(f[rec], f[runner]) if runner else (math.nan, math.nan)
    C1 = level(m1, s1, C1_CLEAR, C1_MODERATE) if runner else "clear"
    C2 = c2[rec]
    lc = learning_curve(entries[rec], X, y, strata)
    C3 = lc["C3"]["value"]
    conf = "High" if (C1 == "clear" and C2 == "clear" and C3 == "adequate") else (
        "Low" if (C1 == "none" or C2 != "clear") else "Medium")
    prior_models = [k for k in models if not entries[k]["post_prior"]]
    winner = max(prior_models, key=lambda k: mean[k])
    prior_order = [r["configuration"] for r in prior["order"] if r["kept"]]
    agreement = "agree" if winner == prior_order[0] else ("partial" if winner in prior_order[:2] else "disagree")
    _, rec_entries = matrix_score(struct[rec], props)
    grounding = Counter("[B]" if e["provenance"].startswith("[B p") else
                        "[B→I]" if e["provenance"].startswith("[B→I") else "[I]" for e in rec_entries)

    # §20 why-not, all 14 structural configurations except the recommendation
    removed = {r["configuration"]: r for r in adm["removed"]}
    why_not = []
    for name in CONFIG:
        if name == struct[rec]:
            continue
        if name in removed:
            why_not.append({"configuration": name, "code": removed[name]["code"], "evidence": removed[name]["evidence"]})
            continue
        cvd = [k for k in models if struct[k] == name]
        if not cvd:
            s, ent = matrix_score(name, props)
            why_not.append({"configuration": name, "code": "DISF",
                            "evidence": f"prior score {s}: {[e['entry'] for e in ent]}"})
            continue
        k = max(cvd, key=lambda x: mean[x])
        code = "BASE" if c2[k] != "clear" else ("SIMP" if k in cands else "OUTP")
        mr, sr = margin(f[rec], f[k])
        why_not.append({"configuration": name, "code": code, "entry": k,
                        "evidence": {"margin_rec_minus_this": mr, "spread": sr, "C2": c2[k],
                                     "addons": addons(name), "rec_addons": addons(struct[rec])}})

    common = most_common_params(entries[rec])                                   # interpretation r
    final_fit = {"hyperparameters": common["params"], "chosen_in_outer_folds": common["folds"],
                 "dropped_inputs": entries[rec]["dropped_inputs"],
                 "grid_override": entries[rec]["folds"][0].get("grid_override")}
    thr = tune_threshold(entries[rec], X, y, strata, final_fit["hyperparameters"]) if props.get("P6") == "yes" else None
    final_fit["threshold"] = thr["final_threshold"] if thr else DEFAULT_THRESHOLD
    return {"recommendation": {"entry": rec, "configuration": struct[rec],
                               "tuned_hyperparameters_cv": common},
            "trace": trace, "selection_confidence": {
                "level": conf, "C1": {"value": C1, "runner_up": runner, "margin": m1, "spread": s1},
                "C2": {"value": C2, "vs": BASELINE, "margin": margin(f[rec], f[BASELINE])},
                "C3": lc["C3"], "rule": "High: C1 clear, C2 clear, C3 adequate; Low: C1 none or C2 not clear; "
                                        "otherwise Medium"},
            "prior_agreement": {"value": agreement, "cv_winner_among_prior_kept": winner,
                                "prior_order_kept": prior_order},
            "grounding": dict(grounding), "grounding_entries": rec_entries,
            "breadth_note": {"configurations_compared": len(models), "applies": len(models) > BREADTH_MANY},
            "why_not": why_not, "learning_curve": lc["points"], "decision_threshold": thr,
            "uncertainty_for_4g": {"fold_sd_pr_auc": float(np.std(f[rec], ddof=SPREAD_DDOF)),
                                   "method": "SD of PR-AUC across the outer folds, step 4g [B→I pp.71–73]"},
            "final_fit": final_fit, "training_positive_rate": float(y.mean())}


# ======================================================================================
# §19.4 the single test-set evaluation
# ======================================================================================

def final(approval: str) -> dict:
    """Refit the recommended configuration on all training patients and evaluate it once on the test
    patients. Refuses to run twice, or if this file changed since `recommend`."""
    target = OUT / "core_final.json"
    if target.exists():
        sys.exit("core_final.json exists: the test set has been used for this sub-task (DR-08)")
    rec = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
    if rec["core_version_sha256"] != version():
        sys.exit("core.py changed since `recommend`; re-run from the earliest affected decision")
    X, y, _ = training_cv()
    spec, name = rec["final_fit"], rec["recommendation"]["configuration"]
    drop, thr = tuple(spec["dropped_inputs"]), spec["threshold"]
    pipe, _ = build(name, n_inner_train(len(y)), drop, spec["grid_override"])
    model = clone(pipe).set_params(**spec["hyperparameters"]).fit(X, y)

    test = pd.read_csv(TEST_TABLE)                                              # the only read of the test patients
    train_patients = set(pd.read_csv(TRAIN_TABLE, usecols=["patient"]).patient)
    assert not (set(test.patient) & train_patients), "a test patient is also a training patient"
    Xt, yt = test[INPUTS], test[TARGET].to_numpy()
    p = prob1(model, Xt)
    pred = (p > thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(yt, pred, labels=[0, 1]).ravel()
    pr, rc = prec_rec(yt, pred)
    test_ap, rate = pr_auc(yt, p), float(yt.mean())
    spread = rec["uncertainty_for_4g"]["fold_sd_pr_auc"]
    prec_c, rec_c, pr_thr = precision_recall_curve(yt, p)
    pd.DataFrame({"patient": test.patient, "set": test["set"], "y": yt, "p": p, "predicted": pred}).to_csv(
        OUT / "private" / "core_test_predictions.csv.gz", index=False)
    return {"approved_by_user": approval, "configuration": name, "hyperparameters": spec["hyperparameters"],
            "dropped_inputs": list(drop), "threshold": thr, "n_test": int(len(yt)), "test_positives": int(yt.sum()),
            "test_pr_auc": test_ap, "test_positive_rate": rate,
            "baseline_on_test": {"configuration": BASELINE, "pr_auc": pr_auc(yt, np.zeros(len(yt))),
                                 "f2": 0.0, "recall": 0.0, "precision": "undefined"},
            "at_threshold": {"f2": f2(yt, pred), "precision": pr, "recall": rc,
                             "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}},
            "uncertainty": {"fold_sd_pr_auc": spread, "method": "step 4g, [B→I pp.71–73]"},
            "success": {"criterion": "test PR-AUC > test positive rate + fold SD of PR-AUC (DR-05)",
                        "required": rate + spread, "met": bool(test_ap > rate + spread)},
            "pr_curve": {"precision": prec_c.tolist(), "recall": rec_c.tolist(), "thresholds": pr_thr.tolist()},
            "predictions_file": "Code/outputs/sepsis/private/core_test_predictions.csv.gz (not in git)"}


# ======================================================================================
# §21 explanation: the final logistic model's weights (verified rebuild)
# ======================================================================================

def explain() -> dict:
    """Rebuild the final model with the same code path and settings as `final`, verify it is the same
    model, and write its weights (§21: logistic coefficients on the log-odds scale).

    `final` kept the fitted model in memory only. The rebuild is accepted as the same model only if its
    probabilities for the test patients equal the saved ones exactly. That check reads the test INPUTS and
    the saved probabilities only: no outcome is read and no metric is computed.
    """
    rec = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
    spec, name = rec["final_fit"], rec["recommendation"]["configuration"]
    if CONFIG[name]["family"] != "Logistic" or CONFIG[name]["poly"]:
        sys.exit("explain is implemented for Logistic without polynomial terms only")
    X, y, _ = training_cv()
    drop = tuple(spec["dropped_inputs"])
    pipe, _ = build(name, n_inner_train(len(y)), drop, spec["grid_override"])          # as in `final`
    model = clone(pipe).set_params(**spec["hyperparameters"]).fit(X, y)

    test = pd.read_csv(TEST_TABLE, usecols=["patient"] + INPUTS)                       # inputs only
    p = prob1(model, test[INPUTS])
    saved = pd.read_csv(OUT / "private" / "core_test_predictions.csv.gz", usecols=["patient", "p"],
                        float_precision="round_trip").set_index("patient").loc[test.patient, "p"].to_numpy()
    identical = bool(np.array_equal(p, saved))
    if not identical:
        sys.exit(f"rebuild differs from the saved predictions (max |diff| {np.max(np.abs(p - saved))}); not written")

    names = design_names(drop)
    lr, scale = model.named_steps["m"].model_, model.named_steps["scale"]
    coef = lr.coef_[0]
    weights = [{"column": n, "weight_standardised": float(w), "column_mean": float(mu), "column_sd": float(sd),
                "weight_per_unit": float(w / sd) if sd > 0 else None,
                "unit": "log of the value" if n in LOG_INPUTS else ("0/1" if n.startswith(("measured_", "Unit_"))
                                                                    or n == "Gender" else "the value")}
               for n, w, mu, sd in zip(names, coef, scale.mean_, scale.scale_)]
    weights.sort(key=lambda r: -abs(r["weight_standardised"]))
    return {"rebuild_of": {"recommend_version": rec["core_version_sha256"], "configuration": name,
                           "hyperparameters": spec["hyperparameters"], "threshold": spec["threshold"]},
            "verification": {"test_patients": int(len(test)), "outcomes_read": False, "metric_computed": False,
                             "probabilities_identical_to_saved": identical},
            "lambda": spec["hyperparameters"].get("m__lam"), "C_used": float(model.named_steps["m"].C_),
            "intercept": float(lr.intercept_[0]),
            "note": "weight_standardised: change in log-odds per 1 SD of the design column (after the DR-09 log "
                    "and median), others fixed; weight_per_unit = weight_standardised / column_sd. Sorted by "
                    "absolute standardised weight. Not causal effects (§21).",
            "weights": weights}


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
    elif args[0] == "prior" and len(args) == 2:
        X, y = training_data()
        props = load_props(args[1])
        adm = admissible_set(props, X)
        write("core_prior.json", {"properties_file": args[1], "properties_used": props,
                                  "admissible": adm["admissible"], **prior_ranking(props, adm)})
    elif args[0] == "cv" and len(args) == 3 and args[1] in ("round1", "round2"):
        X, y, strata = training_cv()
        props = load_props(args[2])
        prior = prior_ranking(props, admissible_set(props, X))
        names = ([BASELINE, prior["simple_first"]] if args[1] == "round1"          # §14 SEQ-3
                 else [k for k in prior["kept"] if k != prior["simple_first"]])
        write(f"core_cv_{args[1]}.json", run_cv(load_store(strata), names, args[1], X, y, strata))
    elif args[0] == "cv" and len(args) >= 3 and args[1] == "add":                    # §18 post-prior
        X, y, strata = training_cv()
        name, rest = args[2], args[3:]
        drop = [rest[i + 1] for i, a in enumerate(rest) if a == "--drop"]
        grid = json.loads(rest[rest.index("--grid") + 1]) if "--grid" in rest else None
        label = rest[rest.index("--label") + 1] if "--label" in rest else None
        store = load_store(strata)
        n = sum(1 for e in store["entries"].values() if str(e.get("round", "")).startswith("post-prior")) + 1
        write(f"core_cv_post_prior_{n}.json",
              run_cv(store, [name], f"post-prior {n}", X, y, strata, drop, grid, True, label))
    elif args[0] == "diagnose" and len(args) == 2:
        X, y, strata = training_cv()
        slug = "".join(ch if ch.isalnum() else "_" for ch in args[1])
        write(f"core_diagnose_{slug}.json", observations(args[1], load_store(strata), X, y, strata))
    elif args[0] == "recommend" and len(args) == 2:
        X, y, strata = training_cv()
        write("core_recommend.json", {"properties_file": args[1], **recommend(load_props(args[1]), X, y, strata)})
    elif args[0] == "final" and len(args) == 3 and args[1] == "--approved":
        res = final(args[2])
        write("core_final.json", res)
    elif args[0] == "explain" and len(args) == 1:
        write("core_weights.json", explain())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
