"""Interim core for the Mobile Price analysis (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the analysis needs,
as literally as possible, with every [I] threshold as a named constant. Decision Records quote this
file's SHA-256 as the code version. Code/core.py (Heart Failure) and Code/sepsis/core.py (Sepsis) belong
to other analyses and are not used.

Contents so far:
  input design   the preprocessing of DR-08, shared by every model family     (used from step 3)
  §11  P9, P10   properties from the training phones                          (step 3)
  §9, §12        the 14 configurations; admissible set: task gate, must-haves,
                 MOD-1, MOD-2                                                  (step 4a)
  §13-§15        matrix score, order, keep, simple-first (SEQ-2)              (step 4b)
  §16            nested CV: outer 10 / inner 5, stratified by price_range, the same
                 folds for every configuration, accuracy as the metric; confusion
                 matrix and recall per band monitored (§5.5 note)              (steps 4c-4e)
  §18            observations O1-O6 and the learning curve, errors as the
                 misclassification rate (P10 = balanced)                       (step 4e)
  §17, §19       C1-C3, recommendation, why-not codes (no threshold: P6 = no)  (step 4f)
  §19.4          the single test-set evaluation                                (step 4g)

Only the classification families (Logistic, k-NN, Tree) have estimators, because sub-task 1 is
multiclass; §12 and §13 cover all 14 configurations, so the others are excluded and coded, never fitted.

Reads Attachments/Mobile Price/train.csv and keeps only the 1,600 training rows listed in
Code/outputs/mobile/split.json ("train_idx"). The 400 test rows are dropped on reading, before any
computation, and the function asserts that none of them is kept. The test rows are read in one place
only, `final`, which needs the user's approval quoted on the command line, refuses to run a second
time, and refuses to run if this file changed since `recommend`.

Interpretations made in this file, where Part II does not say exactly what to do:
  a. Input design (DR-08): all 20 inputs as recorded, no transformation. The six 0/1 indicators are
     one-hot encoded (REQ-6, p. 49) with one level dropped, which leaves each as the same single 0/1
     column. The 14 numerical inputs, n_cores included, pass through unchanged. Scaling is not part
     of the input design: it belongs to the families that need it (REQ-2, REQ-3) and is added there.
  b. The P9 fit standardises all 20 columns before logistic regression, as for Logistic and k-NN in
     step 4. Encoding and scaling are fitted once on all training phones, because P9 is a property
     of the training data, not a cross-validated estimate.
  c. "Negligible regularisation" is C = 1e8 (lambda = 1e-8) in LogisticRegression, as in the
     Heart Failure and Sepsis cores. With four classes, scikit-learn fits the softmax (multinomial)
     model, as in the book's multiclass logistic regression (pp. 56-57).
  d. Predicted class for the P9 accuracy: the class with the highest predicted probability. This is
     the multiclass counterpart of the threshold r = 0.5 (p. 53); applying it to four classes is ours.
  e. MOD-2 is checked on the design matrix the parametric models would see: the DR-08 preprocessing
     fitted once on all training phones (as in b), standardised, plus an intercept column; and, for
     the "+ poly" configurations, with the powers of each numerical input up to the largest degree in
     the §16 grid (3). The 14 numerical inputs get powers; the six 0/1 indicators do not (§9: powers
     of each numerical input).
  f. "Exactly collinear" = the design matrix has lower rank than it has columns, by numpy's
     matrix_rank at its default tolerance. Where it does, the near-zero singular directions are
     reported with the columns that carry them, so the reason can be read.
  g. Parameters for MOD-2. With four classes, the book's multiclass logistic regression has one
     parameter vector per class (eq. 3.41-3.43, pp. 56-57), so parameters = 4 x (columns + intercept).
     This is the larger of the two common counts (the other fixes one class's vector at zero: 3 x),
     so the "parameters >= n_train" test is the cautious one.
  h. Must-have gates apply only to properties the user called a must-have (P5_must_have,
     P6_must_have in the properties file); in DR-09 neither is.
  i. Inner tuning uses the deciding metric, accuracy (DR-05, §16 "selection metric"), with the
     predicted class = the class with the highest probability (interpretation d) for Logistic, the
     majority among the k neighbours for k-NN, and the majority in the leaf for Tree.
  j. Folds: outer and inner folds are stratified by price_range (§16, DR-07), shuffled with
     CV_SEED = 2026. The inner folds are made within each outer training fold. The outer fold of
     every training phone is stored with the checksums of train.csv and split.json, and every later
     run checks that they are unchanged.
  k. Polynomial terms (+ poly): each numerical input is centred and scaled on the training fold,
     then raised to powers 2..degree; no products. With an intercept this spans the same functions as
     raw powers (as checked in MOD-2), but under L2 the penalty acts on the coefficients of the
     standardised powers.
  l. Diagnosis errors (§16, P10 = balanced): the book's default, the misclassification rate
     (p. 67). E_train = 1 - accuracy on the outer training fold, E_val = 1 - accuracy on the outer
     validation fold.
  m. Spread = sample standard deviation (ddof = 1) of the 10 fold differences.
  n. A margin of exactly 0 is never "clear" or "moderate", even when the spread is 0.
  o. Learning-curve subsets are drawn within each outer training fold, stratified by price_range,
     with CV_SEED.
  p. C3 "its fold SD" = the SD across the 10 outer folds of E_val at 100 % of the training data.
  q. O2: the success criterion is test accuracy - fold SD of accuracy > 25 % (DR-05). On the
     training side, O2 holds if E_train >= 1 - (training baseline accuracy + the leading
     configuration's fold SD of accuracy), i.e. its training accuracy does not clear that level.
  r. O5 ignores the polynomial degree: §9 fixes it to {2, 3}, so both values are edges and the grid
     cannot be extended.
  s. Final hyperparameters: the most common setting across the outer folds (the value the CV table
     reports), as the Heart Failure and Sepsis analyses did, not a new grid search on all rows.
  t. All 20 input columns, including the 0/1 indicators, are standardised before Logistic and k-NN
     (REQ-2, REQ-3). The tree gets the DR-08 design unscaled.
  u. Baseline (§14 SEQ-1): the most common training class. All four bands tie (400 each in the
     training phones, 360 each in every outer training fold), so the tie goes to the lowest label,
     0 (low cost), as scikit-learn's DummyClassifier does. Its validation accuracy is that fold's
     share of band 0 (25 % with stratified folds) whichever band wins the tie.
  v. Monitoring (§5.5 note, DR-05): for every configuration, each outer validation fold's 4 x 4
     confusion matrix (rows: true band; columns: predicted band) is stored; the CV table pools them
     and gives recall per band = diagonal / row total. They are reported, and not used in any decision.
  w. L2 for Logistic uses the book's lambda (eq. 3.48-3.50, p. 61): scikit-learn minimises
     sum(loss) + ||W||^2 / (2C) with the intercept unpenalised (REQ-5), so C = 1 / (2 n lambda). This
     was checked for two classes in the Heart Failure analysis (Code/06_check_eq350.py, same
     scikit-learn version); for four classes the same objective form is used with the multinomial
     cross-entropy and ||W|| the norm of all four classes' weights, and it has not been checked
     separately. lam = None is unregularised; scikit-learn's default C = 1.0 is never used (§9).
  x. P6 = no, so no decision threshold is tuned (§16): every model predicts as in i.
  y. Prior agreement (§17) with tied ranks (§15: tied configurations share a rank): "agree" if the CV
     winner among the prior-kept configurations has rank 1, "partial" if rank 2, "disagree"
     otherwise. "Prior first" and "top two" are read as ranks, so a tie at the top is not broken by
     list order.

Run (from Code/):
  uv run python mobile/core.py p9p10
  uv run python mobile/core.py admset    mobile/props_dr09.json
  uv run python mobile/core.py prior     mobile/props_dr09.json
  uv run python mobile/core.py cv round1 mobile/props_dr09.json
  uv run python mobile/core.py cv round2 mobile/props_dr09.json
  uv run python mobile/core.py cv add "<configuration>" [--drop COL ...] [--grid JSON] [--label TEXT]
  uv run python mobile/core.py diagnose "<cv entry label>"
  uv run python mobile/core.py recommend mobile/props_dr09.json
  uv run python mobile/core.py final --approved "<the user's words>"
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

CODE = Path(__file__).resolve().parent.parent
ROOT = CODE.parent
SRC = ROOT / "Attachments" / "Mobile Price" / "train.csv"
SPLIT = CODE / "outputs" / "mobile" / "split.json"
OUT = CODE / "outputs" / "mobile"

TARGET = "price_range"
CLASSES = [0, 1, 2, 3]

# ---- Input design (DR-08): which columns, which fixed transforms ----
CATEGORICAL = ["blue", "dual_sim", "four_g", "three_g", "touch_screen", "wifi"]       # 0/1 indicators
NUMERICAL = ["battery_power", "clock_speed", "fc", "int_memory", "m_dep", "mobile_wt", "n_cores", "pc",
             "px_height", "px_width", "ram", "sc_h", "sc_w", "talk_time"]               # as recorded
INPUTS = NUMERICAL + CATEGORICAL
TRANSFORMED: list[str] = []                                                            # none (DR-08)

# ---- [I] thresholds (ML Guide.md, section 11 and Appendix to Part II) ----
P9_SEPARABLE_ACCURACY = 1.0  # separable if training accuracy reaches 100 % ...
P9_NEGLIGIBLE_C = 1e8        # ... with negligible regularisation (interpretation c)
P10_IMBALANCED_SHARE = 0.20  # imbalanced if the smallest class is < 20 % of training rows

LOGISTIC_MAX_ITER = 100_000

# ---- §16 grids [I] (GRID_DEGREE is also used by MOD-2, interpretation e) ----
GRID_DEGREE = [2, 3]
GRID_K = [1, 3, 5, 7, 9, 15, 21, 31, 51]
GRID_DEPTH = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]
GRID_MIN_LEAF = [1, 5, 10, 20]
GRID_LAMBDA = [10.0 ** e for e in range(-4, 5)]

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
CV_SEED = 2026               # outer and inner folds, learning-curve subsets, tree tie-breaks (DR-07)
SPREAD_DDOF = 1              # interpretation m
N_JOBS = 1                   # grid search in one process; does not change results. Was -1 until
                             # 28 October 2026: the parallel worker pool broke twice on Windows
                             # (WinError 6, WinError 5) during the first DX-3 run (user's choice)

BASELINE = "Baseline (most common class)"                    # §14 SEQ-1, DR-05, interpretation u
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


def version() -> str:
    """SHA-256 of this file: the code version quoted in Decision Records."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def training_data() -> tuple[pd.DataFrame, pd.Series]:
    """The 1,600 training phones only, with the DR-08 inputs as recorded."""
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    train_idx, test_idx = split["train_idx"], set(split["test_idx"])
    df = pd.read_csv(SRC).loc[train_idx]
    assert not test_idx.intersection(df.index), "a test row was read"
    assert len(df) == split["n_train"]
    assert sorted(df.columns.drop(TARGET)) == sorted(INPUTS)
    return df[INPUTS], df[TARGET]


def preprocessor(drop: tuple = ()) -> ColumnTransformer:
    """DR-08 input design. Every learned step is fitted on the data it is given, so inside
    cross-validation it is refitted in each fold (REQ-1). Same for every model family.
    `drop` removes inputs, for backward elimination in the diagnosis loop (DX-4) only."""
    num = [c for c in NUMERICAL if c not in drop]
    cat = [c for c in CATEGORICAL if c not in drop]
    parts = [("as_recorded", "passthrough", num)]
    if cat:
        parts.append(("indicators", OneHotEncoder(drop="if_binary", categories=[[0, 1]] * len(cat)), cat))
    return ColumnTransformer(parts, verbose_feature_names_out=False)


def design_names(drop: tuple = ()) -> list[str]:
    """Column order of preprocessor(drop): numerical inputs, then the indicators."""
    return [c for c in NUMERICAL if c not in drop] + [c for c in CATEGORICAL if c not in drop]


def p9_p10(X: pd.DataFrame, y: pd.Series) -> dict:
    """§11 P9 and P10, computed on the training phones, with the DR-08 input design.

    P9: logistic regression with negligible regularisation is fitted to the training phones; the classes
    count as perfectly separable if it classifies every training phone correctly. This fit establishes
    a property only; it is not a candidate model and is not evaluated.
    P10: share of the smallest class among the training phones.
    """
    model = Pipeline([("design", preprocessor()), ("scale", StandardScaler()),
                      ("m", LogisticRegression(C=P9_NEGLIGIBLE_C, max_iter=LOGISTIC_MAX_ITER))])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model.fit(X, y)
    proba = model.predict_proba(X)
    classes = model.named_steps["m"].classes_
    pred = classes[np.argmax(proba, axis=1)]                     # interpretation d
    accuracy = float((pred == y.to_numpy()).mean())
    counts = y.value_counts().reindex(CLASSES, fill_value=0)
    smallest = float(counts.min() / counts.sum())
    n_columns = int(model.named_steps["design"].transform(X.iloc[:1]).shape[1])
    return {
        "P9": {"value": "yes" if accuracy >= P9_SEPARABLE_ACCURACY else "no",
               "training_accuracy_negligible_regularisation": accuracy,
               "training_rows_misclassified": int((pred != y.to_numpy()).sum()),
               "C_used": P9_NEGLIGIBLE_C, "iterations": int(np.max(model.named_steps["m"].n_iter_)),
               "max_iter": LOGISTIC_MAX_ITER,
               "convergence_warnings": [str(w.message) for w in caught if issubclass(w.category, ConvergenceWarning)],
               "prediction_rule": "class with the highest probability (interpretation d)",
               "threshold": "100 % training accuracy", "provenance": "[I] procedure"},
        "P10": {"value": "imbalanced" if smallest < P10_IMBALANCED_SHARE else "balanced",
                "smallest_class_share": smallest, "class_counts": {str(k): int(v) for k, v in counts.items()},
                "threshold": f"< {P10_IMBALANCED_SHARE:.0%}", "provenance": "[I] threshold"},
        "input_columns_after_encoding": n_columns,
        "transformed_inputs": TRANSFORMED,
    }


def load_props(path: str) -> dict:
    """Property values passed to the core, copied from the latest PROP record."""
    return json.loads((CODE / path).read_text(encoding="utf-8"))


def _rank_report(D: np.ndarray, names: list[str]) -> dict:
    """Rank of D (interpretation f) and, if deficient, the columns carrying each null direction."""
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
    """§12 MOD-2 inputs (interpretations e, f, g): parameters vs n_train, and exact collinearity of the
    design matrix with intercept, without and with powers up to the largest grid degree."""
    Z = preprocessor().fit_transform(X)
    names = NUMERICAL + CATEGORICAL                                  # the column order of preprocessor()
    assert Z.shape[1] == len(names)
    num = [names.index(c) for c in NUMERICAL]
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
        rep["parameters_per_class"] = rep["columns"]
        rep["parameters"] = len(CLASSES) * rep["columns"]          # interpretation g
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
            if props.get(prop) == value and props.get(f"{prop}_must_have", False):     # interpretation h
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
# §13-§15 prior ranking
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
    Centring and scaling are fitted on the training fold (REQ-1); interpretation k."""

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
    """Multiclass (softmax) logistic regression with the book's L2 penalty lambda*||theta||^2
    (pp. 56-57, 61), interpretation w: C = 1/(2 n lambda), intercept unpenalised (REQ-5).
    Predicted class = highest probability (interpretation d)."""

    def __init__(self, lam: float | None = None):
        self.lam = lam

    def fit(self, X, y):
        n = len(y)
        self.C_ = np.inf if self.lam is None else 1.0 / (2.0 * n * self.lam)
        self.model_ = LogisticRegression(C=self.C_, max_iter=LOGISTIC_MAX_ITER).fit(X, y)
        self.classes_ = self.model_.classes_
        self.converged_ = bool(np.max(self.model_.n_iter_) < LOGISTIC_MAX_ITER)
        return self

    def predict_proba(self, X):
        return self.model_.predict_proba(X)

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]


def build(name: str, n_inner_train: int, drop: tuple = (), grid_override: dict | None = None):
    """Pipeline and grid for one configuration. The DR-08 design is the first step, so every learned
    preprocessing step is refitted on each training fold (REQ-1)."""
    c = CONFIG[name]
    names = design_names(drop)
    num_idx = tuple(i for i, col in enumerate(names) if col in NUMERICAL)
    steps = [("design", preprocessor(drop))]                                    # REQ-1, REQ-6
    grid: dict = {}
    if c["family"] == "Logistic":
        if c["poly"]:
            steps.append(("poly", SeparatePowers(num_idx)))
            grid["poly__degree"] = GRID_DEGREE                                  # REQ-4
        steps.append(("scale", StandardScaler()))                               # REQ-3, interpretation t
        steps.append(("m", BookLogistic(lam=None)))
        if c["l2"]:
            grid["m__lam"] = GRID_LAMBDA                                        # REQ-4
    elif c["family"] == "kNN":
        steps.append(("scale", StandardScaler()))                               # REQ-2, interpretation t
        steps.append(("m", KNeighborsClassifier()))
        grid["m__n_neighbors"] = [k for k in GRID_K if k < n_inner_train]       # REQ-4
    elif c["family"] == "Tree":
        steps.append(("m", DecisionTreeClassifier(random_state=CV_SEED)))
        grid["m__max_depth"] = GRID_DEPTH                                       # REQ-4, never fully grown
        grid["m__min_samples_leaf"] = GRID_MIN_LEAF
    else:
        raise NotImplementedError(f"{name}: no estimator in this interim core (not a classification family)")
    if grid_override:
        grid.update(grid_override)
    return Pipeline(steps), grid


# ======================================================================================
# Data, metrics and folds
# ======================================================================================

def training_cv() -> tuple[pd.DataFrame, np.ndarray]:
    X, y = training_data()
    return X, y.to_numpy()


def data_sha() -> str:
    """Checksum of the two files the training rows come from (interpretation j)."""
    return hashlib.sha256(SRC.read_bytes() + SPLIT.read_bytes()).hexdigest()


def accuracy(y, pred) -> float:
    """The deciding metric (DR-05): share of phones in the right band."""
    return float(np.mean(np.asarray(y) == np.asarray(pred)))


def confusion(y, pred) -> list[list[int]]:
    """Rows: true band 0-3; columns: predicted band 0-3 (interpretation v)."""
    return confusion_matrix(y, pred, labels=CLASSES).tolist()


def outer_folds(y: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    """§16: 10 outer folds, shuffled, stratified by price_range (interpretation j)."""
    skf = StratifiedKFold(OUTER_FOLDS, shuffle=True, random_state=CV_SEED)
    return list(skf.split(np.zeros(len(y)), y))


def inner_splits(y: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    """§16: 5 inner folds within a training fold, stratified the same way."""
    skf = StratifiedKFold(INNER_FOLDS, shuffle=True, random_state=CV_SEED)
    return list(skf.split(np.zeros(len(y)), y))


def n_inner_train(n: int) -> int:
    return n - math.ceil(n / INNER_FOLDS)


def margin(a: list[float], b: list[float]) -> tuple[float, float]:
    """§16: mean and SD (spread) of the fold differences a - b; interpretation m."""
    d = np.asarray(a) - np.asarray(b)
    return float(d.mean()), float(d.std(ddof=SPREAD_DDOF))


def level(m: float, s: float, clear: float, moderate: float | None = None) -> str:
    """§17 levels; interpretation n: a margin of 0 or below is never clear or moderate."""
    if m > 0 and m >= clear * s:
        return "clear"
    if moderate is not None and m > 0 and m >= moderate * s:
        return "moderate"
    return "none" if moderate is not None else "not clear"


def fit_search(name: str, X: pd.DataFrame, y: np.ndarray, drop: tuple = (), grid_override: dict | None = None):
    """Inner grid search on one training fold (REQ-4), on accuracy (interpretation i), refitted on the
    whole training fold."""
    pipe, grid = build(name, n_inner_train(len(y)), drop, grid_override)
    search = GridSearchCV(pipe, grid, scoring="accuracy", cv=inner_splits(y), refit=True,
                          n_jobs=N_JOBS, error_score="raise")
    search.fit(X, y)
    m = search.best_estimator_.named_steps["m"]
    converged = getattr(m, "converged_", None)
    return search, search.best_params_, grid, converged


def baseline_class(y: np.ndarray) -> int:
    """Interpretation u: most common class, ties to the lowest label."""
    counts = pd.Series(y).value_counts()
    return int(min(counts[counts == counts.max()].index))


# ======================================================================================
# §16 nested cross-validation, cumulative store
# ======================================================================================

def load_store(y: np.ndarray) -> dict:
    fold_of_row = np.zeros(len(y), dtype=int)
    for f, (_, va) in enumerate(outer_folds(y)):
        fold_of_row[va] = f
    if STORE.exists():
        store = json.loads(STORE.read_text(encoding="utf-8"))
        if store["data_sha256"] != data_sha() or store["outer_fold_of_row"] != fold_of_row.tolist():
            sys.exit("training data or outer folds differ from the stored ones; refusing to mix them")
        return store
    return {"cv_seed": CV_SEED, "outer_folds": OUTER_FOLDS, "inner_folds": INNER_FOLDS,
            "stratified_by": "price_range", "data_sha256": data_sha(),
            "outer_fold_of_row": fold_of_row.tolist(), "entries": {}}


def baseline_cv(y: np.ndarray) -> dict:
    """§14 SEQ-1: always predict the most common class of the training fold (interpretation u)."""
    rows = []
    for f, (tr, va) in enumerate(outer_folds(y)):
        b = baseline_class(y[tr])
        acc_tr, acc_va = accuracy(y[tr], np.full(len(tr), b)), accuracy(y[va], np.full(len(va), b))
        rows.append({"fold": f, "best_params": {}, "predicted_class": b, "acc_train": acc_tr, "acc_val": acc_va,
                     "e_train": 1 - acc_tr, "e_val": 1 - acc_va, "converged": None,
                     "confusion_val": confusion(y[va], np.full(len(va), b))})
    return {"configuration": BASELINE, "structural": None, "post_prior": False, "dropped_inputs": [],
            "grid": {}, "pipeline": "constant: the most common training class (ties to the lowest label)",
            "folds": rows}


def nested_cv(name: str, X: pd.DataFrame, y: np.ndarray, drop: list[str],
              grid_override: dict | None, post_prior: bool) -> dict:
    """§16: inner 5-fold grid search on accuracy within each of the 10 outer training folds; the
    diagnosis errors are the misclassification rate because P10 = balanced (interpretation l)."""
    rows, grid_seen, pipe_repr = [], None, None
    for f, (tr, va) in enumerate(outer_folds(y)):
        search, params, grid, converged = fit_search(name, X.iloc[tr], y[tr], tuple(drop), grid_override)
        pred_tr, pred_va = search.predict(X.iloc[tr]), search.predict(X.iloc[va])
        acc_tr, acc_va = accuracy(y[tr], pred_tr), accuracy(y[va], pred_va)
        rows.append({"fold": f, "best_params": params, "grid_used": grid, "acc_train": acc_tr, "acc_val": acc_va,
                     "e_train": 1 - acc_tr, "e_val": 1 - acc_va, "converged": converged,
                     "grid_override": grid_override, "confusion_val": confusion(y[va], pred_va)})
        grid_seen, pipe_repr = grid, repr(search.best_estimator_)
        print(f"  {name}: fold {f} accuracy val {acc_va:.4f} {params}", file=sys.stderr)
    return {"configuration": name, "structural": name, "post_prior": post_prior, "dropped_inputs": drop,
            "grid": grid_seen, "pipeline": pipe_repr, "folds": rows}


def fold_values(entry: dict, key: str) -> list[float]:
    return [r[key] for r in entry["folds"]]


def most_common_params(entry: dict) -> dict:
    counts = Counter(json.dumps(r["best_params"], sort_keys=True) for r in entry["folds"])
    params, n = counts.most_common(1)[0]
    return {"params": json.loads(params), "folds": f"{n}/{len(entry['folds'])}"}


def pooled_monitoring(entry: dict) -> dict:
    """Interpretation v: pooled 4 x 4 confusion matrix over the outer validation folds, recall per band."""
    cm = np.sum([np.asarray(r["confusion_val"]) for r in entry["folds"]], axis=0)
    recall = {str(c): float(cm[i, i] / cm[i].sum()) if cm[i].sum() else math.nan for i, c in enumerate(CLASSES)}
    return {"confusion_pooled": cm.tolist(), "recall_per_band": recall}


def cv_table(store: dict) -> dict:
    entries = store["entries"]
    models = [k for k in entries if k != BASELINE]
    means = {k: float(np.mean(fold_values(entries[k], "acc_val"))) for k in entries}
    leader = max(models, key=lambda k: means[k]) if models else None
    rows = []
    for k, e in entries.items():
        row = {"configuration": k, "post_prior": e["post_prior"], "round": e.get("round"),
               "tuned_hyperparameters": most_common_params(e) if k != BASELINE else "n/a",
               "cv_mean_accuracy": means[k],
               "fold_sd_accuracy": float(np.std(fold_values(e, "acc_val"), ddof=SPREAD_DDOF)),
               "e_train": float(np.mean(fold_values(e, "e_train"))),
               "e_val": float(np.mean(fold_values(e, "e_val"))),
               "not_converged_folds": sum(1 for r in e["folds"] if r["converged"] is False),
               **pooled_monitoring(e)}
        if leader and k != leader:
            m, s = margin(fold_values(e, "acc_val"), fold_values(entries[leader], "acc_val"))
            row["margin_vs_leader"] = {"mean": m, "spread": s}
        if BASELINE in entries and k != BASELINE:
            m, s = margin(fold_values(e, "acc_val"), fold_values(entries[BASELINE], "acc_val"))
            row["margin_vs_baseline"] = {"mean": m, "spread": s, "C2": level(m, s, C2_CLEAR)}
        rows.append(row)
    return {"metric": "accuracy", "leader": leader, "rows": rows}


def run_cv(store: dict, names: list[str], round_label: str, X, y, drop=(), grid_override=None,
           post_prior=False, label=None) -> dict:
    added = []
    for name in names:
        key = label or name
        if key in store["entries"]:
            sys.exit(f"'{key}' is already cross-validated; give a new --label for a variant")
        entry = baseline_cv(y) if name == BASELINE else nested_cv(name, X, y, list(drop), grid_override, post_prior)
        entry["round"] = round_label
        store["entries"][key] = entry
        STORE.write_text(json.dumps(store, indent=1, default=float), encoding="utf-8")
        added.append(key)
    return {"round": round_label, "added": added, "table": cv_table(store)}


# ======================================================================================
# §18 observations and learning curve
# ======================================================================================

def learning_curve(entry: dict, X, y) -> dict:
    """§16: training fractions 10 %..100 % on the outer folds, nested tuning at each size; errors are
    the misclassification rate (interpretation l). Subsets keep the band mix (interpretation o)."""
    drop = tuple(entry["dropped_inputs"])
    override = entry["folds"][0].get("grid_override")
    out = []
    for frac in LC_FRACTIONS:
        e_tr, e_va = [], []
        for tr, va in outer_folds(y):
            sub = tr if frac == 1.0 else train_test_split(tr, train_size=frac, stratify=y[tr],
                                                          random_state=CV_SEED)[0]
            search, _, _, _ = fit_search(entry["structural"], X.iloc[sub], y[sub], drop, override)
            e_tr.append(1 - accuracy(y[sub], search.predict(X.iloc[sub])))
            e_va.append(1 - accuracy(y[va], search.predict(X.iloc[va])))
        out.append({"fraction": frac, "e_train_mean": float(np.mean(e_tr)), "e_val_mean": float(np.mean(e_va)),
                    "e_val_fold_sd": float(np.std(e_va, ddof=SPREAD_DDOF))})
        print(f"  learning curve {frac:.0%}: E_val {out[-1]['e_val_mean']:.4f}", file=sys.stderr)
    at = {r["fraction"]: r for r in out}
    drop_80_100 = at[0.8]["e_val_mean"] - at[1.0]["e_val_mean"]
    c3 = "limited" if drop_80_100 >= C3_FALLING * at[1.0]["e_val_fold_sd"] else "adequate"   # interpretation p
    return {"points": out, "C3": {"value": c3, "e_val_80_minus_100": drop_80_100,
                                  "threshold": f">= {C3_FALLING} x fold SD at 100 % "
                                               f"({at[1.0]['e_val_fold_sd']:.4f})"}}


def observations(key: str, store: dict, X, y) -> dict:
    e = store["entries"][key]
    table = {r["configuration"]: r for r in cv_table(store)["rows"]}[key]
    e_train, e_val = table["e_train"], table["e_val"]
    gap = e_val - e_train
    c2 = table["margin_vs_baseline"]["C2"]
    base_acc = accuracy(y, np.full(len(y), baseline_class(y)))
    o5 = {}
    for p in (e["grid"] or {}):
        if p == "poly__degree":                                                # interpretation r
            continue
        edges = sum(r["best_params"][p] in (min(r["grid_used"][p]), max(r["grid_used"][p])) for r in e["folds"])
        o5[p] = {"folds_at_edge": edges, "holds": edges > O5_MOST_FOLDS * len(e["folds"])}
    lc = learning_curve(e, X, y)
    criterion = base_acc + table["fold_sd_accuracy"]                           # interpretation q
    obs = {
        "O1": {"holds": c2 != "clear", "C2": c2, "vs": BASELINE},
        "O2": {"holds": e_train >= 1 - criterion, "e_train": e_train,
               "compared_with": f"1 - (training baseline accuracy {base_acc:.4f} + fold SD {table['fold_sd_accuracy']:.4f})",
               "note": "interpretation q"},
        "O3": {"holds": gap >= O3_RATIO * e_train, "gap": gap, "e_train": e_train},
        "O4": {"holds": e_train >= O4_RATIO * gap, "gap": gap, "e_train": e_train,
               "note": "P10 = balanced: ratio test only (§18 O4)"},
        "O5": {"holds": any(v["holds"] for v in o5.values()), "by_parameter": o5},
        "O6": {"holds": lc["C3"]["value"] == "limited", "C3": lc["C3"]},
    }
    order = ["O1", "O2", "O5", "O3", "O4", "O6"]                                # §18 priority
    first = next((o for o in order if obs[o]["holds"]), None)
    return {"configuration": key, "error": "misclassification rate (P10 = balanced)", "e_train": e_train,
            "e_val": e_val, "gap": gap, "observations": obs, "priority_order": order,
            "first_that_holds": first, "learning_curve": lc["points"]}


# ======================================================================================
# §17 confidence, §19 recommendation, §20 why-not
# ======================================================================================

def recommend(props: dict, X, y) -> dict:
    store = load_store(y)
    entries = store["entries"]
    adm = admissible_set(props, X)
    prior = prior_ranking(props, adm)
    models = [k for k in entries if k != BASELINE]
    f = {k: fold_values(entries[k], "acc_val") for k in entries}
    mean = {k: float(np.mean(v)) for k, v in f.items()}
    struct = {k: entries[k]["structural"] for k in models}
    score = {k: matrix_score(struct[k], props)[0] for k in models}

    # §19.1 eligible: C2 = clear (no must-haves in DR-09)
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
    lc = learning_curve(entries[rec], X, y)
    C3 = lc["C3"]["value"]
    conf = "High" if (C1 == "clear" and C2 == "clear" and C3 == "adequate") else (
        "Low" if (C1 == "none" or C2 != "clear") else "Medium")
    prior_models = [k for k in models if not entries[k]["post_prior"]]
    winner = max(prior_models, key=lambda k: mean[k])
    prior_order = [r["configuration"] for r in prior["order"] if r["kept"]]
    rank_of = {r["configuration"]: r["rank"] for r in prior["order"]}               # interpretation y
    first_rank = [k for k in prior_order if rank_of[k] == 1]
    agreement = "agree" if rank_of[winner] == 1 else ("partial" if rank_of[winner] <= 2 else "disagree")
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

    common = most_common_params(entries[rec])                                   # interpretation s
    final_fit = {"hyperparameters": common["params"], "chosen_in_outer_folds": common["folds"],
                 "dropped_inputs": entries[rec]["dropped_inputs"],
                 "grid_override": entries[rec]["folds"][0].get("grid_override"),
                 "threshold": "none: P6 = no, predicted band = highest probability or majority (interpretation x)"}
    return {"recommendation": {"entry": rec, "configuration": struct[rec], "tuned_hyperparameters_cv": common},
            "trace": trace, "selection_confidence": {
                "level": conf, "C1": {"value": C1, "runner_up": runner, "margin": m1, "spread": s1},
                "C2": {"value": C2, "vs": BASELINE, "margin": margin(f[rec], f[BASELINE])},
                "C3": lc["C3"], "rule": "High: C1 clear, C2 clear, C3 adequate; Low: C1 none or C2 not clear; "
                                        "otherwise Medium"},
            "prior_agreement": {"value": agreement, "cv_winner_among_prior_kept": winner,
                                "prior_order_kept": prior_order, "sharing_first_rank": first_rank},
            "grounding": dict(grounding), "grounding_entries": rec_entries,
            "breadth_note": {"configurations_compared": len(models), "applies": len(models) > BREADTH_MANY},
            "why_not": why_not, "learning_curve": lc["points"],
            "monitoring_cv": pooled_monitoring(entries[rec]),
            "uncertainty_for_4g": {"fold_sd_accuracy": float(np.std(f[rec], ddof=SPREAD_DDOF)),
                                   "method": "SD of accuracy across the outer folds, step 4g [B→I pp.71–73]"},
            "final_fit": final_fit}


# ======================================================================================
# §19.4 the single test-set evaluation
# ======================================================================================

def final(approval: str) -> dict:
    """Refit the recommended configuration on all training phones and evaluate it once on the test
    phones, with the baseline on the same rows. Refuses to run twice, or if this file changed since
    `recommend`."""
    target = OUT / "core_final.json"
    if target.exists():
        sys.exit("core_final.json exists: the test set has been used for this sub-task (DR-07)")
    rec = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
    if rec["core_version_sha256"] != version():
        sys.exit("core.py changed since `recommend`; re-run from the earliest affected decision")
    X, y = training_cv()
    spec, name = rec["final_fit"], rec["recommendation"]["configuration"]
    drop = tuple(spec["dropped_inputs"])
    pipe, _ = build(name, n_inner_train(len(y)), drop, spec["grid_override"])
    model = clone(pipe).set_params(**spec["hyperparameters"]).fit(X, y)

    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    test = pd.read_csv(SRC).loc[split["test_idx"]]                              # the only read of the test rows
    assert not set(split["test_idx"]) & set(split["train_idx"]), "a test row is also a training row"
    Xt, yt = test[INPUTS], test[TARGET].to_numpy()
    pred = model.predict(Xt)
    b = baseline_class(y)
    base_pred = np.full(len(yt), b)
    cm = np.asarray(confusion(yt, pred))
    out = {"approved_by_user": approval, "configuration": name, "hyperparameters": spec["hyperparameters"],
           "dropped_inputs": list(drop), "n_test": int(len(yt)),
           "test_class_counts": {str(c): int((yt == c).sum()) for c in CLASSES},
           "test_accuracy": accuracy(yt, pred), "baseline_class": b, "baseline_test_accuracy": accuracy(yt, base_pred),
           "uncertainty_fold_sd_accuracy": rec["uncertainty_for_4g"]["fold_sd_accuracy"],
           "confusion_test": cm.tolist(),
           "recall_per_band_test": {str(c): float(cm[i, i] / cm[i].sum()) for i, c in enumerate(CLASSES)}}
    out["success_criterion"] = {
        "rule": "test accuracy - fold SD of accuracy > baseline accuracy (DR-05)",
        "value": out["test_accuracy"] - out["uncertainty_fold_sd_accuracy"],
        "baseline": out["baseline_test_accuracy"],
        "met": bool(out["test_accuracy"] - out["uncertainty_fold_sd_accuracy"] > out["baseline_test_accuracy"])}
    pd.DataFrame({"row": test.index, "y": yt, "predicted": pred, "baseline": base_pred}).to_csv(
        OUT / "core_test_predictions.csv", index=False)
    return out


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
        write("core_p9_p10.json", {"rows_used": "training phones only", "n_train": int(len(y)),
                                   "inputs": INPUTS, **p9_p10(X, y)})
    elif args[0] == "admset" and len(args) == 2:
        X, y = training_data()
        write("core_admset.json", {"rows_used": "training phones only", "n_train": int(len(y)),
                                   "properties_file": args[1], **admissible_set(load_props(args[1]), X)})
    elif args[0] == "prior" and len(args) == 2:
        X, y = training_data()
        props = load_props(args[1])
        write("core_prior.json", {"properties_file": args[1], "properties_used": props,
                                  **prior_ranking(props, admissible_set(props, X))})
    elif args[0] == "cv" and len(args) >= 2:
        X, y = training_cv()
        store = load_store(y)
        if args[1] in ("round1", "round2") and len(args) == 3:
            props = load_props(args[2])
            prior = prior_ranking(props, admissible_set(props, X))
            names = ([BASELINE, prior["simple_first"]] if args[1] == "round1"
                     else [k for k in prior["kept"] if k != prior["simple_first"]])
            write(f"core_cv_{args[1]}.json", run_cv(store, names, args[1], X, y))
        elif args[1] == "add" and len(args) >= 3:
            rest, drop, override, label = args[3:], [], None, None
            while rest:
                flag = rest.pop(0)
                if flag == "--drop":
                    drop.append(rest.pop(0))
                elif flag == "--grid":
                    override = json.loads(rest.pop(0))
                elif flag == "--label":
                    label = rest.pop(0)
                else:
                    sys.exit(__doc__)
            n_post = sum(1 for e in store["entries"].values() if e["post_prior"]) + 1
            write(f"core_cv_post_prior_{n_post}.json",
                  run_cv(store, [args[2]], f"post-prior {n_post}", X, y, drop, override, True, label))
        else:
            sys.exit(__doc__)
    elif args[0] == "diagnose" and len(args) == 2:
        X, y = training_cv()
        safe = "".join(ch if ch.isalnum() else "_" for ch in args[1])
        write(f"core_diagnose_{safe}.json", observations(args[1], load_store(y), X, y))
    elif args[0] == "recommend" and len(args) == 2:
        X, y = training_cv()
        write("core_recommend.json", {"properties_file": args[1], **recommend(load_props(args[1]), X, y)})
    elif args[0] == "final" and len(args) == 3 and args[1] == "--approved":
        write("core_final.json", final(args[2]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
