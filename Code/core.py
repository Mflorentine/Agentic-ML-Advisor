"""Interim core for this analysis (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the
analysis needs, as literally as possible, with every [I] threshold as a named constant.
Decision Records quote this file's SHA-256 as the code version.

Contents
  §11  P9, P10           properties from the training rows                 (step 3)
  §12  admissible set    task gate, must-haves, MOD-1, MOD-2               (step 4a)
  §13, §15  prior        matrix score, order, keep, simple-first (SEQ-2)  (step 4b)
  §16  nested CV         outer 10 / inner 5, same folds for every config  (steps 4c, 4d, 4e)
  §18  observations      E_train, E_val, gap, O1-O6, learning curve       (step 4e)
  §17, §19  recommend    eligibility, candidates, choice, C1-C3, why-not,
                         decision threshold tuned by CV (P6 = yes)        (step 4f)
  §19.4  final           the single test-set evaluation                   (step 4g)

Only the classification families (Logistic, k-NN, Tree) have estimators here, because
sub-task 1 is binary. §12 and §13 are implemented for all 14 configurations, so the
regression families are excluded and coded, never fitted.

Reads only the TRAINING rows listed in Code/outputs/split.json. The test rows are read in
one place only, `final`, which refuses to run without the user's approval quoted on the
command line, and refuses to run a second time (the test set is used once, DR-06).

Interpretations made in this file, where Part II does not say exactly what to do. Each is
marked [I] or UNLISTED [I] at the place it is used and is to be shown to the user:
  a. Predicted class: y = 1 if the probability of class 1 is > r (r = 0.5 by default, p. 53);
     a probability of exactly r goes to class 0. Same rule for every family.
  b. Inner tuning uses the selection metric, F2 at r = 0.5 (§16 "selection metric").
  c. Polynomial terms: each numeric input is centred and scaled on the training fold, then
     raised to powers 2..degree; no products. With an intercept this spans the same
     functions as powers of the raw input, so WITHOUT regularisation the fit is the same.
     WITH L2 it is not: the penalty acts on the coefficients of the standardised powers,
     so it shrinks a different set of curves than it would on raw powers.
  d. All inputs, including the 0/1 ones, are standardised before Logistic and k-NN
     (REQ-2, REQ-3). The tree gets the inputs unscaled.
  e. Spread = sample standard deviation (ddof = 1) of the 10 fold differences.
  f. A margin of exactly 0 is never "clear" or "moderate", even when the spread is 0.
  g. O5 ignores the polynomial degree: §9 fixes it to {2, 3}, so both values are edges and
     the grid cannot be extended.
  h. C3 "its fold SD" is read as the SD across the 10 outer folds of the validation error
     at 100 % of the training data.
  i. O2: the criterion is in F2, not in misclassification, so O2 compares the leading
     configuration's mean training F2 with the flag-everyone reference plus its fold SD.
  j. Final hyperparameters: the most common setting across the outer folds (the value the
     CV table reports), not a new grid search on all rows. Changed after 4b at the user's
     decision (DR-18 -> DR-19): the grid search on all rows gave an unconstrained tree.
  k. Decision threshold (P6 = yes, user's trade-off = F2, DR-05): the r in THRESHOLD_GRID
     that maximises F2 on out-of-fold probabilities from the inner folds; ties go to the r
     closest to 0.5. Its CV estimate is nested: r is chosen inside each outer training fold
     and scored on that outer validation fold.

Run (from Code/):
  uv run python core.py p9p10
  uv run python core.py admset    inputs/subtask1_props.json
  uv run python core.py prior     inputs/subtask1_props.json
  uv run python core.py cv round1 inputs/subtask1_props.json
  uv run python core.py cv round2 inputs/subtask1_props.json
  uv run python core.py cv add "<configuration>" [--drop COL ...] [--grid JSON] [--label TEXT]
  uv run python core.py diagnose "<cv entry label>"
  uv run python core.py recommend inputs/subtask1_props.json
  uv run python core.py final --approved "<the user's words>"
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
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, fbeta_score, precision_recall_curve, roc_curve
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
SPLIT = CODE / "outputs" / "split.json"
OUT = CODE / "outputs"
STORE = OUT / "core_cv_store.json"

TARGET = "DEATH_EVENT"

# ---- Input design (DR-11): fixed transforms, nothing fitted ----
LOG_INPUTS = ["serum_creatinine", "creatinine_phosphokinase"]
NUMERIC_INPUTS = ["age", "creatinine_phosphokinase", "ejection_fraction", "platelets",
                  "serum_creatinine", "serum_sodium"]          # the other five are 0/1 (step 1)

# ---- Metric (DR-05, DR-08) ----
BETA = 2.0                   # F2: recall weighted twice as heavily as precision (p. 92)
DEFAULT_THRESHOLD = 0.5      # p. 53; used for selection, before any threshold tuning (§16)

# ---- [I] thresholds (ML Guide.md, Appendix to Part II) ----
P9_SEPARABLE_ACCURACY = 1.0  # separable if training accuracy reaches 100 % ...
P9_NEGLIGIBLE_C = 1e8        # ... with negligible regularisation (C = 1/lambda very large)
P10_IMBALANCED_SHARE = 0.20  # imbalanced if the smallest class is < 20 % of training rows
KEEP_TOP_OTHERS = 3          # §15: kept besides baseline and simple-first (plus ties)
OUTER_FOLDS = 10             # §16
INNER_FOLDS = 5              # §16
C1_CLEAR = 1.0               # §17: margin >= 1 x spread -> clear
C1_MODERATE = 0.5            # §17: 0.5-1 x spread -> moderate; below -> none
C2_CLEAR = 1.0               # §17: margin over baseline >= 1 x spread -> clear
C3_FALLING = 0.5             # §17: E_val(80 %) - E_val(100 %) >= 0.5 x fold SD -> limited
WITHIN_NOISE = 0.5           # §19: margin < 0.5 x spread -> "none" (same cut-off as C1)
BREADTH_MANY = 10            # §17: breadth note if more than 10 configurations compared
O3_RATIO = 2.0               # §18: gap >= 2 x E_train -> overfitting
O4_RATIO = 2.0               # §18: E_train >= 2 x gap -> underfitting
O5_MOST_FOLDS = 0.5          # §18: "most outer folds" = more than half
LC_FRACTIONS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]   # §16 learning curve

# ---- §16 grids [I] ----
GRID_K = [1, 3, 5, 7, 9, 15, 21, 31, 51]
GRID_DEPTH = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]
GRID_MIN_LEAF = [1, 5, 10, 20]
GRID_DEGREE = [2, 3]
GRID_LAMBDA = [10.0 ** e for e in range(-4, 5)]

# ---- Choices made for this analysis, not thresholds in the guide ----
CV_SEED = 2026               # outer and inner folds, learning-curve subsets, tree tie-breaks
SPREAD_DDOF = 1              # interpretation e
THRESHOLD_GRID = [round(0.05 * i, 2) for i in range(1, 20)]   # 0.05 ... 0.95, interpretation k
LOGISTIC_MAX_ITER = 100_000
# Which baseline C2, O1 and SEQ-3 compare against: §14 SEQ-1, the most common class (agreed
# with the user, step 4). The flag-everyone reference (DR-08) is used only for success at 4g.
C2_BASELINE = "Baseline (most common class)"


# ======================================================================================
# Solution space (§9), gates (§12), matrix (§13)
# ======================================================================================

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
BASELINES = ["Baseline (most common class)", "Flag everyone"]

TASK_GATE = {   # §12, P1 -> admissible families
    "numeric": ({"Linear", "kNN", "Tree"}, "[B p.17]"),
    "count": ({"Poisson", "Linear", "kNN", "Tree"}, "[B pp.17, 61–63]"),
    "non-negative real": ({"Exponential", "Linear", "kNN", "Tree"}, "[B pp.17, 63]"),
    "binary": ({"Logistic", "kNN", "Tree"}, "[B pp.17, 49–57]"),
    "multiclass": ({"Logistic", "kNN", "Tree"}, "[B pp.17, 49–57]"),
}
MUST_HAVE_GATE = {  # §12, must-have -> families that meet it
    ("P5", "inspectable"): ({"Linear", "Logistic", "Poisson", "Exponential", "Tree", "kNN?"}, "[B→I p.347]"),
    ("P5", "worst-case bound"): ({"Tree", "Logistic"}, "[B→I p.347]"),
    ("P6", "yes"): ({"Logistic"}, "[B→I pp.50, 53–54]"),
}
SIMPLE_FIRST = {"numeric": "Linear", "count": "Poisson", "non-negative real": "Exponential",
                "binary": "Logistic", "multiclass": "Logistic"}   # §14 SEQ-2

# §13 matrix: (property, value, column, score, tag, condition). Columns: family names,
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


# ======================================================================================
# Data
# ======================================================================================

def version() -> str:
    """SHA-256 of this file: the code version quoted in Decision Records."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def training_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Training rows only, inputs as fixed in step 2 (`time` excluded). Raw values; the
    DR-11 log transform is the first step of every model pipeline."""
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    df = pd.read_csv(SRC)
    train = df.iloc[split["train_idx"]]
    inputs = split["inputs"]
    return train[inputs], train[TARGET], inputs


def test_data() -> tuple[pd.DataFrame, pd.Series, list[int]]:
    """The locked test rows. Called from `final` only."""
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    df = pd.read_csv(SRC)
    test = df.iloc[split["test_idx"]]
    return test[split["inputs"]], test[TARGET], list(split["test_idx"])


def load_props(path: str) -> dict:
    return json.loads((CODE / path).read_text(encoding="utf-8"))


# ======================================================================================
# Estimators and pipelines (§9 implementation notes, REQ-1 to REQ-6)
# ======================================================================================

class LogInputs(TransformerMixin, BaseEstimator):
    """DR-11: natural log of the given columns. A fixed formula; nothing is fitted."""

    def __init__(self, idx: tuple = ()):
        self.idx = idx

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.array(X, dtype=float, copy=True)
        if self.idx:
            X[:, list(self.idx)] = np.log(X[:, list(self.idx)])
        return X


class SeparatePowers(TransformerMixin, BaseEstimator):
    """§9 `poly`: powers 2..degree of each numeric input separately, no products [I].
    Centring and scaling are fitted on the training fold (REQ-1); interpretation c."""

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

    scikit-learn 1.9 minimises (1/n) sum(loss) + ||w||^2 / (2 C n), intercept unpenalised
    (REQ-5). Matching the book's (1/n) sum(loss) + lambda ||theta||^2 gives C = 1/(2 n lambda).
    To be checked against eq. 3.50 before any L2 result is reported (user, step 4).
    lam=None is unregularised (C = inf): scikit-learn's default C = 1.0 is never used (§9)."""

    def __init__(self, lam: float | None = None):
        self.lam = lam

    def fit(self, X, y):
        n = len(y)
        self.C_ = np.inf if self.lam is None else 1.0 / (2.0 * n * self.lam)
        self.model_ = LogisticRegression(C=self.C_, max_iter=LOGISTIC_MAX_ITER).fit(X, y)
        self.classes_ = self.model_.classes_
        return self

    def predict_proba(self, X):
        return self.model_.predict_proba(X)

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] > DEFAULT_THRESHOLD).astype(int)


def build(name: str, inputs: list[str], n_inner_train: int, grid_override: dict | None = None):
    """Pipeline and grid for one configuration. Every learned preprocessing step is inside
    the pipeline, so it is refitted on each training fold (REQ-1)."""
    c = CONFIG[name]
    log_idx = tuple(i for i, col in enumerate(inputs) if col in LOG_INPUTS)
    num_idx = tuple(i for i, col in enumerate(inputs) if col in NUMERIC_INPUTS)
    steps = [("log", LogInputs(log_idx))]
    grid: dict = {}
    if c["family"] == "Logistic":
        if c["poly"]:
            steps.append(("poly", SeparatePowers(num_idx)))
            grid["poly__degree"] = GRID_DEGREE                          # REQ-4
        steps.append(("scale", StandardScaler()))                       # REQ-3
        steps.append(("m", BookLogistic(lam=None)))
        if c["l2"]:
            grid["m__lam"] = GRID_LAMBDA                                # REQ-4
    elif c["family"] == "kNN":
        steps.append(("scale", StandardScaler()))                       # REQ-2
        steps.append(("m", KNeighborsClassifier()))
        grid["m__n_neighbors"] = [k for k in GRID_K if k < n_inner_train]   # REQ-4
    elif c["family"] == "Tree":
        steps.append(("m", DecisionTreeClassifier(random_state=CV_SEED)))
        grid["m__max_depth"] = GRID_DEPTH                               # REQ-4, never fully grown
        grid["m__min_samples_leaf"] = GRID_MIN_LEAF
    else:
        raise NotImplementedError(f"{name}: no estimator in this interim core (regression family)")
    if grid_override:
        grid.update(grid_override)
    return Pipeline(steps), grid


# ======================================================================================
# Metrics and folds
# ======================================================================================

def f2(y, pred) -> float:
    return float(fbeta_score(y, pred, beta=BETA, zero_division=0))


def misclass(y, pred) -> float:
    return float(np.mean(np.asarray(y) != np.asarray(pred)))


def prob1(model, X) -> np.ndarray:
    return model.predict_proba(X)[:, 1]


def f2_scorer(model, X, y) -> float:
    """Inner tuning score: F2 at the default threshold (interpretation b)."""
    return f2(y, (prob1(model, X) > DEFAULT_THRESHOLD).astype(int))


def outer_folds(y: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    skf = StratifiedKFold(OUTER_FOLDS, shuffle=True, random_state=CV_SEED)
    return list(skf.split(np.zeros(len(y)), y))


def inner_cv() -> StratifiedKFold:
    return StratifiedKFold(INNER_FOLDS, shuffle=True, random_state=CV_SEED)


def n_inner_train(n: int) -> int:
    return n - math.ceil(n / INNER_FOLDS)


def margin(a: list[float], b: list[float]) -> tuple[float, float]:
    """§16: mean and SD (spread) of the fold differences a - b."""
    d = np.asarray(a) - np.asarray(b)
    return float(d.mean()), float(d.std(ddof=SPREAD_DDOF))


def level(m: float, s: float, clear: float, moderate: float | None = None) -> str:
    """§17 levels; interpretation f: a margin of 0 or below is never clear or moderate."""
    if m > 0 and m >= clear * s:
        return "clear"
    if moderate is not None and m > 0 and m >= moderate * s:
        return "moderate"
    return "none" if moderate is not None else "not clear"


def fit_search(name, inputs, X, y, grid_override=None):
    pipe, grid = build(name, inputs, n_inner_train(len(y)), grid_override)
    search = GridSearchCV(pipe, grid, scoring=f2_scorer, cv=inner_cv(), refit=True,
                          error_score="raise") if grid else pipe
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        search.fit(X, y)
    n_warn = sum(issubclass(w.category, ConvergenceWarning) for w in caught)
    params = search.best_params_ if grid else {}
    return search, params, grid, n_warn


# ======================================================================================
# §11 P9, P10
# ======================================================================================

def p9_p10(X: pd.DataFrame, y: pd.Series, inputs: list[str]) -> dict:
    """§11 P9 and P10, computed on the training rows, with the DR-11 input design.

    P9: logistic regression with negligible regularisation is fitted to the training rows;
    the classes count as perfectly separable if it classifies every training row correctly.
    This fit establishes a property only; it is not a candidate model and is not evaluated.
    P10: share of the smallest class among the training rows.
    """
    log_idx = tuple(i for i, col in enumerate(inputs) if col in LOG_INPUTS)
    model = Pipeline([("log", LogInputs(log_idx)), ("scale", StandardScaler()),
                      ("m", LogisticRegression(C=P9_NEGLIGIBLE_C, max_iter=200_000))])
    model.fit(X, y)
    accuracy = float((model.predict(X) == y).mean())
    counts = y.value_counts().sort_index()
    smallest = float(counts.min() / counts.sum())
    return {
        "P9": {"value": "yes" if accuracy >= P9_SEPARABLE_ACCURACY else "no",
               "training_accuracy_negligible_regularisation": accuracy,
               "C_used": P9_NEGLIGIBLE_C, "log_inputs": LOG_INPUTS,
               "threshold": "100 % training accuracy", "provenance": "[I] procedure"},
        "P10": {"value": "imbalanced" if smallest < P10_IMBALANCED_SHARE else "balanced",
                "smallest_class_share": smallest, "class_counts": {str(k): int(v) for k, v in counts.items()},
                "threshold": f"< {P10_IMBALANCED_SHARE:.0%}", "provenance": "[I] threshold"},
    }


# ======================================================================================
# §12 admissible set
# ======================================================================================

def mod2_check(X: pd.DataFrame, inputs: list[str]) -> dict:
    """MOD-2 inputs: number of parameters vs n_train, and exact collinearity (rank of the
    design matrix with intercept), without and with polynomial terms at the largest degree."""
    log_idx = tuple(i for i, col in enumerate(inputs) if col in LOG_INPUTS)
    num_idx = tuple(i for i, col in enumerate(inputs) if col in NUMERIC_INPUTS)
    base = LogInputs(log_idx).transform(X.to_numpy())
    out = {}
    for poly in (False, True):
        Z = SeparatePowers(num_idx, max(GRID_DEGREE)).fit_transform(base) if poly else base
        D = np.hstack([np.ones((len(Z), 1)), StandardScaler().fit_transform(Z)])
        out["poly" if poly else "plain"] = {
            "parameters": int(D.shape[1]), "n_train": int(len(Z)), "rank": int(np.linalg.matrix_rank(D)),
            "applies": bool(D.shape[1] >= len(Z) or np.linalg.matrix_rank(D) < D.shape[1])}
    return out


def admissible_set(props: dict, X: pd.DataFrame, inputs: list[str]) -> dict:
    families, gate_tag = TASK_GATE[props["P1"]]
    mod2 = mod2_check(X, inputs)
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
                            "evidence": f"MOD-2: {m2} [B→I pp.46–47, 65]"})
            continue
        admissible.append(name)
    return {"task_gate": {"P1": props["P1"], "families": sorted(families), "provenance": gate_tag},
            "must_haves": {k: props.get(k) for k in ("P5_must_have", "P6_must_have")},
            "MOD-1": {"P9": props.get("P9"), "applies": props.get("P9") == "yes", "provenance": "[B p.61]"},
            "MOD-2": {**mod2, "provenance": "[B→I pp.46–47, 65]"},
            "admissible": admissible, "removed": removed}


# ======================================================================================
# §13, §15 prior ranking
# ======================================================================================

def simple_first(props: dict, admissible: list[str]) -> str:
    """§14 SEQ-2: the plain parametric model for the task, or its + L2 version if MOD-1 or
    MOD-2 removed the plain one."""
    plain = SIMPLE_FIRST[props["P1"]]
    return plain if plain in admissible else f"{plain} + L2"


def prior_ranking(props: dict, adm: dict) -> dict:
    rows = []
    for name in adm["admissible"]:
        score, entries = matrix_score(name, props)
        rows.append({"configuration": name, "score": score, "addons": addons(name), "entries": entries})
    rows.sort(key=lambda r: (-r["score"], r["addons"]))     # §15.3: score, then fewer add-ons
    rank, prev = 0, None
    for i, r in enumerate(rows):                            # still tied -> shared rank
        key = (r["score"], r["addons"])
        rank = rank if key == prev else i + 1
        r["rank"], prev = rank, key
    sf = simple_first(props, adm["admissible"])
    others = [r for r in rows if r["configuration"] != sf]
    if len(others) > KEEP_TOP_OTHERS:
        cut_rank = others[KEEP_TOP_OTHERS - 1]["rank"]
        kept_others = [r for r in others if r["rank"] <= cut_rank]   # ties at the cut kept
    else:
        kept_others = others
    kept = [sf] + [r["configuration"] for r in kept_others]
    for r in rows:
        r["kept"] = r["configuration"] in kept
        r["role"] = "simple-first (SEQ-2)" if r["configuration"] == sf else ("kept" if r["kept"] else "DISF")
    return {"order": rows, "simple_first": sf, "kept": kept, "baselines": BASELINES,
            "not_kept": [{"configuration": r["configuration"], "code": "DISF", "score": r["score"],
                          "entries": r["entries"]} for r in rows if not r["kept"]]}


# ======================================================================================
# §16 nested cross-validation, cumulative store
# ======================================================================================

def load_store(y: np.ndarray) -> dict:
    folds = [[int(i) for i in va] for _, va in outer_folds(y)]
    if STORE.exists():
        store = json.loads(STORE.read_text(encoding="utf-8"))
        if store["outer_validation_folds"] != folds:
            sys.exit("outer folds differ from the stored ones; refusing to mix fold sets")
        return store
    return {"cv_seed": CV_SEED, "outer_folds": OUTER_FOLDS, "inner_folds": INNER_FOLDS,
            "stratified": True, "outer_validation_folds": folds, "entries": {}}


def baseline_cv(name: str, y: np.ndarray) -> dict:
    rows = []
    for f, (tr, va) in enumerate(outer_folds(y)):
        const = int(Counter(y[tr]).most_common(1)[0][0]) if name == BASELINES[0] else 1
        rows.append({"fold": f, "best_params": {}, "f2_val": f2(y[va], np.full(len(va), const)),
                     "f2_train": f2(y[tr], np.full(len(tr), const)),
                     "e_train": misclass(y[tr], np.full(len(tr), const)),
                     "e_val": misclass(y[va], np.full(len(va), const)), "convergence_warnings": 0,
                     "predicts": const})
    return {"configuration": name, "structural": None, "post_prior": False, "dropped_inputs": [],
            "grid": {}, "pipeline": "constant prediction", "folds": rows}


def nested_cv(name: str, X: pd.DataFrame, y: np.ndarray, inputs: list[str],
              drop: list[str], grid_override: dict | None, post_prior: bool) -> dict:
    use = [c for c in inputs if c not in drop]
    Xa = X[use].to_numpy(dtype=float)
    rows, grid_seen, pipe_repr = [], None, None
    for f, (tr, va) in enumerate(outer_folds(y)):
        search, params, grid, n_warn = fit_search(name, use, Xa[tr], y[tr], grid_override)
        p_tr, p_va = prob1(search, Xa[tr]), prob1(search, Xa[va])
        yhat_tr, yhat_va = (p_tr > DEFAULT_THRESHOLD).astype(int), (p_va > DEFAULT_THRESHOLD).astype(int)
        rows.append({"fold": f, "best_params": params, "grid_used": grid,
                     "f2_val": f2(y[va], yhat_va), "f2_train": f2(y[tr], yhat_tr),
                     "e_train": misclass(y[tr], yhat_tr), "e_val": misclass(y[va], yhat_va),
                     "convergence_warnings": n_warn})
        grid_seen = grid
        pipe_repr = repr(search.best_estimator_ if hasattr(search, "best_estimator_") else search)
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
    models = [k for k in entries if k not in BASELINES]
    means = {k: float(np.mean(fold_values(entries[k], "f2_val"))) for k in entries}
    leader = max(models, key=lambda k: means[k]) if models else None
    rows = []
    for k, e in entries.items():
        row = {"configuration": k, "post_prior": e["post_prior"], "round": e.get("round"),
               "tuned_hyperparameters": most_common_params(e) if k not in BASELINES else "n/a",
               "cv_mean_f2": means[k], "fold_sd_f2": float(np.std(fold_values(e, "f2_val"), ddof=SPREAD_DDOF)),
               "e_train": float(np.mean(fold_values(e, "e_train"))),
               "e_val": float(np.mean(fold_values(e, "e_val"))),
               "convergence_warnings": int(sum(fold_values(e, "convergence_warnings")))}
        if leader and k != leader:
            m, s = margin(fold_values(e, "f2_val"), fold_values(entries[leader], "f2_val"))
            row["margin_vs_leader"] = {"mean": m, "spread": s}
        for b in BASELINES:
            if b in entries and k != b:
                m, s = margin(fold_values(e, "f2_val"), fold_values(entries[b], "f2_val"))
                row[f"margin_vs {b}"] = {"mean": m, "spread": s,
                                         "C2": level(m, s, C2_CLEAR) if b == C2_BASELINE else "n/a"}
        rows.append(row)
    return {"leader": leader, "C2_baseline": C2_BASELINE, "rows": rows}


def run_cv(store: dict, names: list[str], round_label: str, X, y, inputs, drop=(), grid_override=None,
           post_prior=False, label=None) -> dict:
    added = []
    for name in names:
        key = label or name
        if key in store["entries"]:
            sys.exit(f"'{key}' is already cross-validated; give a new --label for a variant")
        entry = baseline_cv(name, y) if name in BASELINES else nested_cv(
            name, X, y, inputs, list(drop), grid_override, post_prior)
        entry["round"] = round_label
        store["entries"][key] = entry
        added.append(key)
    STORE.write_text(json.dumps(store, indent=2, default=float), encoding="utf-8")
    return {"round": round_label, "added": added, "table": cv_table(store)}


# ======================================================================================
# §18 observations and learning curve
# ======================================================================================

def learning_curve(entry: dict, X: pd.DataFrame, y: np.ndarray, inputs: list[str]) -> dict:
    """§16: training fractions 10 %..100 % on the outer folds, nested tuning at each size.
    E_train and E_val are misclassification rates (§16 diagnosis errors)."""
    use = [c for c in inputs if c not in entry["dropped_inputs"]]
    Xa = X[use].to_numpy(dtype=float)
    out = []
    for frac in LC_FRACTIONS:
        e_tr, e_va = [], []
        for tr, va in outer_folds(y):
            sub = tr if frac == 1.0 else train_test_split(
                tr, train_size=frac, stratify=y[tr], random_state=CV_SEED)[0]
            search, _, _, _ = fit_search(entry["structural"], use, Xa[sub], y[sub],
                                         entry["folds"][0].get("grid_override"))
            e_tr.append(misclass(y[sub], (prob1(search, Xa[sub]) > DEFAULT_THRESHOLD).astype(int)))
            e_va.append(misclass(y[va], (prob1(search, Xa[va]) > DEFAULT_THRESHOLD).astype(int)))
        out.append({"fraction": frac, "e_train_mean": float(np.mean(e_tr)), "e_val_mean": float(np.mean(e_va)),
                    "e_val_fold_sd": float(np.std(e_va, ddof=SPREAD_DDOF))})
    at = {r["fraction"]: r for r in out}
    drop_80_100 = at[0.8]["e_val_mean"] - at[1.0]["e_val_mean"]
    c3 = "limited" if drop_80_100 >= C3_FALLING * at[1.0]["e_val_fold_sd"] else "adequate"
    return {"points": out, "C3": {"value": c3, "e_val_80_minus_100": drop_80_100,
                                  "threshold": f">= {C3_FALLING} x fold SD at 100 % "
                                               f"({at[1.0]['e_val_fold_sd']:.4f})"}}


def observations(key: str, store: dict, X, y, inputs) -> dict:
    e = store["entries"][key]
    table = {r["configuration"]: r for r in cv_table(store)["rows"]}[key]
    e_train, e_val = table["e_train"], table["e_val"]
    gap = e_val - e_train
    c2 = table[f"margin_vs {C2_BASELINE}"]["C2"]
    f2_train = float(np.mean(fold_values(e, "f2_train")))
    ref = flag_everyone_reference(y)
    o5 = {}
    for p in (e["grid"] or {}):
        if p == "poly__degree":                                          # interpretation g
            continue
        edges = 0
        for r in e["folds"]:
            g = r["grid_used"][p]
            edges += r["best_params"][p] in (min(g), max(g))
        o5[p] = {"folds_at_edge": edges, "holds": edges > O5_MOST_FOLDS * len(e["folds"])}
    lc = learning_curve(e, X, y, inputs)
    obs = {
        "O1": {"holds": c2 != "clear", "C2": c2, "vs": C2_BASELINE},
        "O2": {"holds": f2_train <= ref + table["fold_sd_f2"], "training_f2": f2_train,
               "compared_with": f"flag-everyone reference {ref:.4f} + fold SD {table['fold_sd_f2']:.4f}",
               "note": "UNLISTED [I] interpretation i"},
        "O3": {"holds": gap >= O3_RATIO * e_train, "gap": gap, "e_train": e_train},
        "O4": {"holds": e_train >= O4_RATIO * gap, "gap": gap, "e_train": e_train},
        "O5": {"holds": any(v["holds"] for v in o5.values()), "by_parameter": o5},
        "O6": {"holds": lc["C3"]["value"] == "limited", "C3": lc["C3"]},
    }
    order = ["O1", "O2", "O5", "O3", "O4", "O6"]                         # §18 priority
    first = next((o for o in order if obs[o]["holds"]), None)
    return {"configuration": key, "e_train": e_train, "e_val": e_val, "gap": gap,
            "observations": obs, "priority_order": order, "first_that_holds": first,
            "learning_curve": lc["points"]}


def flag_everyone_reference(y: np.ndarray) -> float:
    """DR-08: F2 of flagging every training patient (recall 1, precision = share of deaths)."""
    return f2(y, np.ones(len(y), dtype=int))


# ======================================================================================
# §16 decision threshold, §17 confidence, §19 recommendation, §20 why-not
# ======================================================================================

def choose_threshold(y: np.ndarray, p: np.ndarray) -> float:
    scores = [(f2(y, (p > r).astype(int)), -abs(r - DEFAULT_THRESHOLD), r) for r in THRESHOLD_GRID]
    return max(scores)[2]


def oof_probabilities(name, use, Xa, y, params) -> np.ndarray:
    oof = np.zeros(len(y))
    for itr, iva in inner_cv().split(Xa, y):
        pipe, _ = build(name, use, n_inner_train(len(y)))
        model = clone(pipe).set_params(**params).fit(Xa[itr], y[itr])
        oof[iva] = prob1(model, Xa[iva])
    return oof


def final_hyperparameters(entry: dict, X, y, inputs) -> dict:
    """Interpretation j: the most common setting across the outer folds."""
    use = [c for c in inputs if c not in entry["dropped_inputs"]]
    common = most_common_params(entry)
    return {"hyperparameters": common["params"], "chosen_in_outer_folds": common["folds"], "inputs": use}


def tune_threshold(entry: dict, X, y, inputs, final_fit: dict) -> dict:
    """Interpretation k. Nested estimate per outer fold, then the final r on all training rows."""
    use = final_fit["inputs"]
    Xa = X[use].to_numpy(dtype=float)
    name = entry["structural"]
    per_fold = []
    for (tr, va), r in zip(outer_folds(y), entry["folds"]):
        params = r["best_params"]
        thr = choose_threshold(y[tr], oof_probabilities(name, use, Xa[tr], y[tr], params))
        pipe, _ = build(name, use, n_inner_train(len(tr)))
        model = clone(pipe).set_params(**params).fit(Xa[tr], y[tr])
        per_fold.append({"threshold": thr, "f2_val": f2(y[va], (prob1(model, Xa[va]) > thr).astype(int))})
    final_thr = choose_threshold(y, oof_probabilities(name, use, Xa, y, final_fit["hyperparameters"]))
    vals = [r["f2_val"] for r in per_fold]
    return {"trade_off": "F2 (DR-05: chosen by the user)", "grid": THRESHOLD_GRID, "per_fold": per_fold,
            "cv_mean_f2_at_tuned_threshold": float(np.mean(vals)),
            "fold_sd_f2_at_tuned_threshold": float(np.std(vals, ddof=SPREAD_DDOF)),
            "final_threshold": final_thr}


def recommend(props: dict, X, y, inputs) -> dict:
    store = load_store(y)
    entries = store["entries"]
    adm = admissible_set(props, X, inputs)
    prior = prior_ranking(props, adm)
    models = [k for k in entries if k not in BASELINES]
    f = {k: fold_values(entries[k], "f2_val") for k in entries}
    mean = {k: float(np.mean(v)) for k, v in f.items()}
    struct = {k: entries[k]["structural"] for k in models}
    score = {k: matrix_score(struct[k], props)[0] for k in models}

    # §19.1 eligible
    c2 = {k: level(*margin(f[k], f[C2_BASELINE]), C2_CLEAR) for k in models}
    eligible = [k for k in models if c2[k] == "clear"]
    trace = {"1_eligible": {k: {"C2": c2[k], "margin_vs_baseline": margin(f[k], f[C2_BASELINE])}
                            for k in models}}
    if not eligible:
        return {"core_version_sha256": version(), "recommendation": None,
                "reason": "no configuration clearly beats the baseline (§19.1): DX-1 or DX-2", "trace": trace}
    # §19.2 candidates
    best = max(eligible, key=lambda k: mean[k])
    cands = [best] + [k for k in eligible if k != best
                      and margin(f[best], f[k])[0] < WITHIN_NOISE * margin(f[best], f[k])[1]]
    trace["2_candidates"] = {k: {"cv_mean": mean[k], "margin_best_minus_this": margin(f[best], f[k])
                                 if k != best else (0.0, 0.0)} for k in cands}
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
    lc = learning_curve(entries[rec], X, y, inputs)
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
            why_not.append({"configuration": name, "code": removed[name]["code"],
                            "evidence": removed[name]["evidence"]})
            continue
        cvd = [k for k in models if struct[k] == name]
        if not cvd:
            s, ent = matrix_score(name, props)
            why_not.append({"configuration": name, "code": "DISF",
                            "evidence": f"prior score {s}: {[e['entry'] for e in ent]}"})
            continue
        k = max(cvd, key=lambda x: mean[x])
        if c2[k] != "clear":
            code = "BASE"
        elif k in cands:
            code = "SIMP"
        else:
            code = "OUTP"
        mr, sr = margin(f[rec], f[k])
        why_not.append({"configuration": name, "code": code, "entry": k,
                        "evidence": {"margin_rec_minus_this": mr, "spread": sr, "C2": c2[k],
                                     "addons": addons(name), "rec_addons": addons(struct[rec])}})

    final_fit = final_hyperparameters(entries[rec], X, y, inputs)
    thr = tune_threshold(entries[rec], X, y, inputs, final_fit) if props.get("P6") == "yes" else None
    final_fit["threshold"] = thr["final_threshold"] if thr else DEFAULT_THRESHOLD
    return {"core_version_sha256": version(), "rows_used": "training only", "props": props,
            "recommendation": {"entry": rec, "configuration": struct[rec],
                               "tuned_hyperparameters_cv": most_common_params(entries[rec])},
            "trace": trace, "selection_confidence": {
                "level": conf, "C1": {"value": C1, "runner_up": runner, "margin": m1, "spread": s1},
                "C2": {"value": C2, "vs": C2_BASELINE, "margin": margin(f[rec], f[C2_BASELINE])},
                "C3": lc["C3"], "rule": "High: C1 clear, C2 clear, C3 adequate; Low: C1 none or C2 not clear; "
                                        "otherwise Medium"},
            "prior_agreement": {"value": agreement, "cv_winner_among_prior_kept": winner,
                                "prior_order_kept": prior_order},
            "grounding": dict(grounding), "grounding_entries": rec_entries,
            "breadth_note": {"configurations_compared": len(models), "applies": len(models) > BREADTH_MANY},
            "why_not": why_not, "learning_curve": lc["points"], "decision_threshold": thr,
            "final_fit": final_fit,
            "flag_everyone_reference_train": flag_everyone_reference(y)}


# ======================================================================================
# §19.4 the single test-set evaluation
# ======================================================================================

def final(approval: str) -> dict:
    target = OUT / "core_final.json"
    if target.exists():
        sys.exit("core_final.json exists: the test set has been used for this sub-task (DR-06)")
    rec = json.loads((OUT / "core_recommend.json").read_text(encoding="utf-8"))
    if rec["core_version_sha256"] != version():
        sys.exit("core.py changed since `recommend`; re-run from the earliest affected decision")
    X, y, inputs = training_data()
    y = y.to_numpy()
    entry = rec["recommendation"]
    use = rec["final_fit"]["inputs"]
    params = rec["final_fit"]["hyperparameters"]
    thr = rec["final_fit"]["threshold"]
    pipe, _ = build(entry["configuration"], use, n_inner_train(len(y)))
    model = clone(pipe).set_params(**params).fit(X[use].to_numpy(dtype=float), y)

    Xt, yt, test_idx = test_data()                                       # the only read of the test rows
    yt = yt.to_numpy()
    p = prob1(model, Xt[use].to_numpy(dtype=float))
    pred = (p > thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(yt, pred, labels=[0, 1]).ravel()
    most_common = int(Counter(y).most_common(1)[0][0])
    spread = (rec["decision_threshold"]["fold_sd_f2_at_tuned_threshold"] if rec["decision_threshold"]
              else float(np.std(fold_values(load_store(y)["entries"][entry["entry"]], "f2_val"),
                                ddof=SPREAD_DDOF)))
    ref = rec["flag_everyone_reference_train"]
    test_f2 = f2(yt, pred)
    prec, recall, pr_thr = precision_recall_curve(yt, p)
    fpr, tpr, roc_thr = roc_curve(yt, p)
    pd.DataFrame({"row": test_idx, "y": yt, "p_death": p, "predicted": pred}).to_csv(
        OUT / "core_test_predictions.csv", index=False)
    return {"core_version_sha256": version(), "approved_by_user": approval,
            "configuration": entry["configuration"], "hyperparameters": params, "inputs": use,
            "threshold": thr, "n_test": int(len(yt)), "test_positives": int(yt.sum()),
            "test_f2": test_f2, "test_recall": float(tp / (tp + fn)) if tp + fn else 0.0,
            "test_precision": float(tp / (tp + fp)) if tp + fp else 0.0,
            "test_misclassification": misclass(yt, pred),
            "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
            "uncertainty": {"fold_sd_f2_at_tuned_threshold": spread, "method": "DR-08, [B→I pp.71–73]"},
            "baselines_on_test": {"Baseline (most common class)": f2(yt, np.full(len(yt), most_common)),
                                  "Flag everyone": f2(yt, np.ones(len(yt), dtype=int))},
            "success": {"criterion": "test F2 > flag-everyone reference (training rows) + fold SD of F2",
                        "reference": ref, "spread": spread, "required": ref + spread,
                        "met": bool(test_f2 > ref + spread)},
            "pr_curve": {"precision": prec.tolist(), "recall": recall.tolist(), "thresholds": pr_thr.tolist()},
            "roc_curve": {"fpr": fpr.tolist(), "tpr": tpr.tolist(), "thresholds": roc_thr.tolist()},
            "predictions_file": "Code/outputs/core_test_predictions.csv"}


# ======================================================================================
# Command line
# ======================================================================================

def write(name: str, result: dict) -> None:
    result = {"core_version_sha256": version(), **result}
    (OUT / name).write_text(json.dumps(result, indent=2, default=float, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, default=float, ensure_ascii=False))


def main(argv: list[str]) -> None:
    args = argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd = args[0]
    if cmd == "final":
        if len(args) != 3 or args[1] != "--approved":
            sys.exit('usage: core.py final --approved "<the user\'s words>"')
        res = final(args[2])
        (OUT / "core_final.json").write_text(json.dumps(res, indent=2, default=float), encoding="utf-8")
        print(json.dumps({k: v for k, v in res.items() if not k.endswith("_curve")}, indent=2, default=float))
        return
    X, y_s, inputs = training_data()
    y = y_s.to_numpy()
    if cmd == "p9p10":
        write("core_p9_p10.json", {"rows_used": "training only", "n_train": int(len(y)), "inputs": inputs,
                                   **p9_p10(X, y_s, inputs)})
    elif cmd == "admset":
        props = load_props(args[1])
        write("core_admset.json", {"inputs_passed": props, **admissible_set(props, X, inputs)})
    elif cmd == "prior":
        props = load_props(args[1])
        adm = admissible_set(props, X, inputs)
        write("core_prior.json", {"inputs_passed": props, "admissible": adm["admissible"],
                                  **prior_ranking(props, adm)})
    elif cmd == "cv" and args[1] in ("round1", "round2"):
        props = load_props(args[2])
        prior = prior_ranking(props, admissible_set(props, X, inputs))
        store = load_store(y)
        names = (BASELINES + [prior["simple_first"]] if args[1] == "round1"
                 else [k for k in prior["kept"] if k != prior["simple_first"]])
        write(f"core_cv_{args[1]}.json", run_cv(store, names, args[1], X, y, inputs))
    elif cmd == "cv" and args[1] == "add":
        name, rest = args[2], args[3:]
        drop = [rest[i + 1] for i, a in enumerate(rest) if a == "--drop"]
        grid = json.loads(rest[rest.index("--grid") + 1]) if "--grid" in rest else None
        label = rest[rest.index("--label") + 1] if "--label" in rest else None
        store = load_store(y)
        n = sum(1 for e in store["entries"].values() if e.get("round", "").startswith("post-prior")) + 1
        res = run_cv(store, [name], f"post-prior {n}", X, y, inputs, drop, grid, True, label)
        if grid:   # keep the override with the entry so the learning curve and final fit reuse it
            for r in store["entries"][label or name]["folds"]:
                r["grid_override"] = grid
            STORE.write_text(json.dumps(store, indent=2, default=float), encoding="utf-8")
        write(f"core_cv_post_prior_{n}.json", res)
    elif cmd == "diagnose":
        store = load_store(y)
        slug = "".join(ch if ch.isalnum() else "_" for ch in args[1])
        write(f"core_diagnose_{slug}.json", observations(args[1], store, X, y, inputs))
    elif cmd == "recommend":
        res = recommend(load_props(args[1]), X, y, inputs)
        res.pop("core_version_sha256", None)
        write("core_recommend.json", res)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
