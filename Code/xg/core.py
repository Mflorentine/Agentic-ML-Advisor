"""Interim core for the xG analysis (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the
analysis needs, as literally as possible, with every [I] threshold as a named constant.
Decision Records quote this file's SHA-256 as the code version. The user approves the whole
script at step 4b, before anything is cross-validated.

Contents
  §11  Property 9, Property 10   properties from the training shots                 (step 3)
  §12  admissible set            task gate, must-haves, MOD-1, MOD-2               (step 4a)
  §13, §15  prior ranking        matrix score, order, keep, simple-first (SEQ-2)   (step 4b)
  §16  nested cross-validation   outer 10 / inner 5 group folds, the same for every
                                 configuration and both sub-tasks                  (steps 4c-4e)
  §18  observations              E_train, E_val, gap, O1-O6, learning curve        (step 4e)
  §17, §19  recommendation       eligibility, candidates, choice, C1-C3, why-not   (step 4f)
  §19.4  final                   the single test-set evaluation                    (step 4g)
  sub-task 2 comparison          team model against the sub-task 1 model, same folds

Reads the TRAINING inputs only (Code/outputs/xg/split/inputs_train.csv), except in one place:
`final`, which refuses to run without the user's approval quoted on the command line, and refuses
to run a second time for the same sub-task (the test set is used once per sub-task).

Interpretations made in this file, where Part II does not say exactly what to do. Each is [I]
or UNLISTED [I] and is to be shown to the user:
  a. Encoding (REQ-6): categorical inputs one-hot encoded with the first level dropped, so that an
     intercept plus one indicator per level is not exactly collinear (MOD-2). An unseen level
     (none expected) is encoded as the dropped level. Properties 3 and 4 were counted with one
     indicator per level (DR-14); the model has one fewer column per categorical input.
  b. All encoded columns, including 0/1 ones, are standardised before logistic regression
     (REQ-3), on the training fold only (REQ-1).
  c. Polynomial terms (§9): each numeric input (distance, angle, opp_in_triangle, gk_distance)
     is standardised on the training fold, then raised to powers 2..degree; no products, and no
     powers of 0/1 or one-hot columns.
  d. Book L2 (eq. 3.50, SML p. 61): (1/n) sum(logistic loss) + lambda ||theta||^2, intercept not
     penalised (REQ-5). scikit-learn minimises (1/n) sum(loss) + ||w||^2 / (2 C n), so
     C = 1 / (2 n lambda), with n the rows in that fit. Unregularised = C = inf; scikit-learn's
     default C = 1 is never used (§9).
  e. Folds (§16): StratifiedGroupKFold, groups = match_id (Admissibility 3), stratified by goal
     (classification), shuffled with CV_SEED. Outer 10, inner 5 within each outer training fold.
  f. Selection metric (DR-11): log-loss, lower is better. Scores are stored as negative log-loss so
     that every margin is positive = better (§16). Inner tuning uses the same metric.
  g. Baseline (SEQ-1): for a probability metric the baseline predicts the training share of goals
     for every shot (DR-11), not the most common class, whose log-loss is unbounded.
  h. Spread = sample standard deviation (ddof = 1) of the 10 fold differences. A margin of 0 or
     below is never "clear" or "moderate".
  i. Diagnosis errors (§16, as changed on 10 November 2026, guide commit 670f1f1): E_train and
     E_val are log-loss, the agreed selection metric. Misclassification rates at r = 0.5 are
     computed alongside and reported, not used by the rules.
  j. O2: the success criterion is in log-loss but relative to StatsBomb xG on the test shots. O2
     compares the leading configuration's training log-loss with the same criterion computed on
     the TRAINING shots: LL_base - 0.9 x (LL_base - LL_StatsBomb), where statsbomb_xg is read as a
     reference only, never as an input.
  k. O5 ignores the polynomial degree: §9 fixes it to {2, 3}, so both values are edges.
  l. Learning curve (§16): at each training fraction, whole matches are sampled from the outer
     training fold (seeded); the hyperparameters are those tuned on that full outer training fold,
     not re-tuned at each size. C3 uses the log-loss E_val (the §16 diagnosis error).
  m. Final hyperparameters: the most common setting across the outer folds (the value the CV table
     reports), refitted on all training shots.
  n. Decision threshold: none. Property 6: probabilities = yes because the probability is the
     product (DR-11); no class prediction is made, so no threshold is tuned (§16).
  o. Sub-task 2 criterion (DR-11): margin of the team model over the sub-task 1 recommended model,
     fold by fold on the same outer folds, in negative log-loss; met if margin >= 1 x spread.

Run (from Code/), with --subtask 1 or 2:
  uv run python xg/core.py p9p10
  uv run python xg/core.py admset   --subtask 1
  uv run python xg/core.py prior    --subtask 1
  uv run python xg/core.py cv round1 --subtask 1
  uv run python xg/core.py cv round2 --subtask 1
  uv run python xg/core.py cv add "<configuration>" --subtask 1 [--grid JSON] [--label TEXT]
  uv run python xg/core.py diagnose "<cv entry>" --subtask 1
  uv run python xg/core.py recommend --subtask 1
  uv run python xg/core.py final --subtask 1 --approved "<the user's words>"
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import os
import warnings
from collections import Counter
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import GridSearchCV, GroupShuffleSplit, StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from features import BOOLEAN, CATEGORICAL, INPUTS_SUBTASK1, INPUTS_SUBTASK2, NUMERIC, build_inputs  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs" / "xg"
SPLIT = OUT / "split"
TRAIN = SPLIT / "inputs_train.csv"
TEST_SHOTS = SPLIT / "test_locked" / "shots_test.csv"
TEST_FRAMES = SPLIT / "test_locked" / "freeze_frames_test.csv"
TRAIN_SHOTS = SPLIT / "shots_train.csv"
PROPS = HERE / "inputs"
TARGET = "goal"
GROUP = "match_id"

# ---- [I] thresholds and settings (ML Guide.md §11, §15-§19 and the Appendix to Part II)
P9_SEPARABLE_ACCURACY = 1.0   # separable if training accuracy reaches 100 % ...
P9_NEGLIGIBLE_C = 1e8         # ... with negligible regularisation (C = 1 / lambda)
P10_IMBALANCED_SHARE = 0.20   # imbalanced if the smallest class is < 20 % of training rows
KEEP_TOP_OTHERS = 3           # §15: kept besides baseline and simple-first (plus ties)
OUTER_FOLDS = 10              # §16
INNER_FOLDS = 5               # §16
C1_CLEAR, C1_MODERATE = 1.0, 0.5   # §17: x spread
C2_CLEAR = 1.0                # §17
C3_FALLING = 0.5              # §17: x fold SD
WITHIN_NOISE = 0.5            # §19: margin < 0.5 x spread -> "none" (same cut-off as C1)
BREADTH_MANY = 10             # §17 breadth note
O3_RATIO = O4_RATIO = 2.0     # §18
O5_MOST_FOLDS = 0.5           # §18: "most outer folds" = more than half
LC_FRACTIONS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]   # §16 learning curve
GRID_DEGREE = [2, 3]          # §16
GRID_LAMBDA = [10.0 ** e for e in range(-4, 5)]   # §16
CV_SEED = 2026                # outer and inner folds, learning-curve subsets
SPREAD_DDOF = 1               # interpretation h
DEFAULT_THRESHOLD = 0.5       # SML p. 53; used only for the misclassification diagnosis errors
SUCCESS_SHARE = 0.9           # DR-11, sub-task 1: >= 90 % of StatsBomb's improvement over the baseline
LOGISTIC_MAX_ITER = 10_000

BASELINE = "Baseline (training goal share)"
SUBTASK_INPUTS = {"1": INPUTS_SUBTASK1, "2": INPUTS_SUBTASK2}

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

P = {1: "Property 1: output type", 2: "Property 2: data-to-parameter ratio", 3: "Property 3: number of inputs",
     4: "Property 4: categorical share", 5: "Property 5: interpretability", 6: "Property 6: probabilities",
     7: "Property 7: extrapolation", 8: "Property 8: expected shape", 9: "Property 9: separability",
     10: "Property 10: class imbalance"}

TASK_GATE = {   # §12, Property 1 -> admissible families
    "numeric": ({"Linear", "kNN", "Tree"}, "[B SML p. 17]"),
    "count": ({"Poisson", "Linear", "kNN", "Tree"}, "[B SML pp. 17, 61–63]"),
    "non-negative real": ({"Exponential", "Linear", "kNN", "Tree"}, "[B SML pp. 17, 63]"),
    "binary": ({"Logistic", "kNN", "Tree"}, "[B SML pp. 17, 49–57]"),
    "multiclass": ({"Logistic", "kNN", "Tree"}, "[B SML pp. 17, 49–57]"),
}
MUST_HAVE_GATE = {  # §12, must-have -> families that meet it
    (5, "inspectable"): ({"Linear", "Logistic", "Poisson", "Exponential", "Tree", "kNN?"}, "[B→I SML p. 347]"),
    (5, "worst-case bound"): ({"Tree", "Logistic"}, "[B→I SML p. 347]"),
    (6, "yes"): ({"Logistic"}, "[B→I SML pp. 50, 53–54]"),
}
SIMPLE_FIRST = {"numeric": "Linear", "count": "Poisson", "non-negative real": "Exponential",
                "binary": "Logistic", "multiclass": "Logistic"}   # §14 SEQ-2

# §13 matrix: (property, values, column, score, tag, condition). Columns: family names, "GLM"
# (Poisson, Exponential), "poly", "L2". A Property 5 or 6 entry applies only when not a must-have.
MATRIX = [
    (1, ("count", "non-negative real"), "Linear", -1, "[B SML p. 62]", None),
    (1, ("count", "non-negative real"), "GLM", +1, "[B SML pp. 61–62]", None),
    (2, ("limited",), "Tree", -1, "[I]", None),
    (2, ("limited",), "poly", -1, "[B→I SML pp. 59–60]", None),
    (2, ("limited",), "L2", +1, "[B→I SML p. 60]", None),
    (3, ("many",), "kNN", -1, "[I]", None),
    (3, ("many",), "poly", -1, "[B→I SML p. 59]", None),
    (4, ("high",), "kNN", -1, "[I]", None),
    (5, ("inspectable",), "Linear", +1, "[B→I SML p. 347]", "not_must_have"),
    (5, ("inspectable",), "Logistic", +1, "[B→I SML p. 347]", "not_must_have"),
    (5, ("inspectable",), "GLM", +1, "[B→I SML p. 347]", "not_must_have"),
    (5, ("inspectable",), "Tree", +1, "[B→I SML p. 347]", "not_must_have"),
    (5, ("inspectable",), "poly", -1, "[I]", "not_must_have"),
    (5, ("worst-case bound",), "Logistic", +1, "[B→I SML p. 347]", "not_must_have"),
    (5, ("worst-case bound",), "Tree", +1, "[B→I SML p. 347]", "not_must_have"),
    (6, ("yes",), "Logistic", +1, "[B→I SML pp. 50, 53–54]", "not_must_have"),
    (7, ("yes",), "kNN", -1, "[B→I SML p. 26]", None),
    (7, ("yes",), "Tree", -1, "[I]", None),
    (8, ("linear",), "Linear", +1, "[B→I SML p. 41]", None),
    (8, ("linear",), "Logistic", +1, "[B→I SML p. 55]", None),
    (8, ("linear",), "GLM", +1, "[B→I SML p. 63]", None),
    (8, ("curved",), "Linear", -1, "[B→I SML pp. 58–59]", None),
    (8, ("curved",), "kNN", +1, "[B→I SML p. 26]", None),
    (8, ("curved",), "poly", +1, "[B→I SML p. 59]", None),
    (8, ("interactions/irregular",), "Linear", -1, "[B→I SML p. 41]", None),
    (8, ("interactions/irregular",), "Logistic", -1, "[B→I SML p. 55]", None),
    (8, ("interactions/irregular",), "GLM", -1, "[B→I SML p. 63]", None),
    (8, ("interactions/irregular",), "kNN", +1, "[B→I SML p. 24]", None),
    (8, ("interactions/irregular",), "Tree", +1, "[B→I SML pp. 27–29]", None),
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


def prop(props: dict, n: int):
    return props["properties"].get(str(n), {}).get("value")


def must_have(props: dict, n: int) -> bool:
    return bool(props["properties"].get(str(n), {}).get("must_have", False))


def matrix_score(name: str, props: dict) -> tuple[int, list[dict]]:
    """§13: family column + `poly` column + `L2` column, over the properties whose value is known."""
    entries = []
    for n, values, col, score, tag, cond in MATRIX:
        if prop(props, n) not in values or col not in columns_of(name):
            continue
        if cond == "not_must_have" and must_have(props, n):
            continue
        entries.append({"entry": f"{P[n]}={prop(props, n)}→{col}", "score": score, "provenance": tag})
    return sum(e["score"] for e in entries), entries


# ======================================================================================
# Data
# ======================================================================================

def version() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def training_data() -> pd.DataFrame:
    return pd.read_csv(TRAIN)


def load_props(subtask: str) -> dict:
    return json.loads((PROPS / f"subtask{subtask}_props.json").read_text(encoding="utf-8"))


# ======================================================================================
# Estimators (interpretations a-d)
# ======================================================================================

class SeparatePowers(TransformerMixin, BaseEstimator):
    """§9 `poly`: standardise each numeric input on the training fold, then append its powers
    2..degree; no products (interpretation c). degree=1 adds nothing."""

    def __init__(self, degree: int = 1):
        self.degree = degree

    def fit(self, X, y=None):
        Z = np.asarray(X, dtype=float)
        self.mean_ = Z.mean(axis=0)
        sd = Z.std(axis=0)
        self.scale_ = np.where(sd > 0, sd, 1.0)
        return self

    def transform(self, X):
        Z = (np.asarray(X, dtype=float) - self.mean_) / self.scale_
        return np.hstack([Z] + [Z ** p for p in range(2, self.degree + 1)])


class BookLogistic(ClassifierMixin, BaseEstimator):
    """Logistic regression with the book's L2 penalty (eq. 3.50, SML p. 61); interpretation d."""

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


def encoder(inputs: list[str], poly: bool) -> ColumnTransformer:
    nums = [c for c in inputs if c in NUMERIC]
    bools = [c for c in inputs if c in BOOLEAN]
    cats = [c for c in inputs if c in CATEGORICAL or c == "team"]
    return ColumnTransformer([
        ("num", SeparatePowers(degree=2 if poly else 1), nums),
        ("bool", "passthrough", bools),
        ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), cats),
    ])


def build(name: str, inputs: list[str], grid_override: dict | None = None):
    """Pipeline and grid for one configuration. Every learned step is inside the pipeline, so it is
    refitted on each training fold (REQ-1)."""
    c = CONFIG[name]
    if c["family"] != "Logistic":
        raise NotImplementedError(f"{name}: no estimator in this interim core (not admissible here)")
    steps = [("enc", encoder(inputs, c["poly"])), ("scale", StandardScaler()), ("m", BookLogistic(lam=None))]
    grid: dict = {}
    if c["poly"]:
        grid["enc__num__degree"] = GRID_DEGREE           # REQ-4
    if c["l2"]:
        grid["m__lam"] = GRID_LAMBDA                     # REQ-4
    if grid_override:
        grid.update(grid_override)
    return Pipeline(steps), grid


# ======================================================================================
# Metrics and folds (interpretations e-h)
# ======================================================================================

def logloss(y, p) -> float:
    return float(log_loss(y, p, labels=[0, 1]))


def misclass(y, p) -> float:
    return float(np.mean(np.asarray(y) != (np.asarray(p) > DEFAULT_THRESHOLD).astype(int)))


def prob1(model, X) -> np.ndarray:
    return model.predict_proba(X)[:, 1]


def neg_logloss_scorer(model, X, y) -> float:
    return -logloss(y, prob1(model, X))


def outer_folds(df: pd.DataFrame) -> list[tuple[np.ndarray, np.ndarray]]:
    sgk = StratifiedGroupKFold(OUTER_FOLDS, shuffle=True, random_state=CV_SEED)
    return list(sgk.split(np.zeros(len(df)), df[TARGET].to_numpy(), df[GROUP].to_numpy()))


def inner_cv() -> StratifiedGroupKFold:
    return StratifiedGroupKFold(INNER_FOLDS, shuffle=True, random_state=CV_SEED)


def margin(a, b) -> tuple[float, float]:
    """§16: mean and SD (spread) of the fold differences a - b (scores, positive = better)."""
    d = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    return float(d.mean()), float(d.std(ddof=SPREAD_DDOF))


def level(m: float, s: float, clear: float, moderate: float | None = None) -> str:
    if m > 0 and m >= clear * s:
        return "clear"
    if moderate is not None and m > 0 and m >= moderate * s:
        return "moderate"
    return "none" if moderate is not None else "not clear"


def fit_search(name, inputs, X: pd.DataFrame, y, groups, grid_override=None):
    pipe, grid = build(name, inputs, grid_override)
    search = GridSearchCV(pipe, grid, scoring=neg_logloss_scorer, cv=inner_cv(), refit=True,
                          error_score="raise") if grid else pipe
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        if grid:
            search.fit(X, y, groups=groups)
        else:
            search.fit(X, y)
    n_warn = sum(issubclass(w.category, ConvergenceWarning) for w in caught)
    return search, (search.best_params_ if grid else {}), grid, n_warn


# ======================================================================================
# §11 Property 9, Property 10
# ======================================================================================

def p9_p10(df: pd.DataFrame, inputs: list[str]) -> dict:
    """Property 9: logistic regression with negligible regularisation is fitted to the training
    shots; separable if it classifies every training shot correctly. This fit establishes a
    property only; it is not a candidate model and is not evaluated.
    Property 10: share of the smallest class among the training shots."""
    X, y = df[inputs], df[TARGET]
    cats = [c for c in inputs if c in CATEGORICAL or c == "team"]
    nums = [c for c in inputs if c not in cats]
    enc = ColumnTransformer([("num", StandardScaler(), nums),
                             ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cats)])
    model = Pipeline([("enc", enc), ("m", LogisticRegression(C=P9_NEGLIGIBLE_C, max_iter=LOGISTIC_MAX_ITER))])
    model.fit(X, y)
    accuracy = float((model.predict(X) == y).mean())
    counts = y.value_counts().sort_index()
    smallest = float(counts.min() / counts.sum())
    return {
        P[9]: {"value": "yes" if accuracy >= P9_SEPARABLE_ACCURACY else "no",
               "training_accuracy_negligible_regularisation": accuracy,
               "C_used": P9_NEGLIGIBLE_C, "threshold": "100 % training accuracy", "provenance": "[I]"},
        P[10]: {"value": "imbalanced" if smallest < P10_IMBALANCED_SHARE else "balanced",
                "smallest_class_share": smallest, "class_counts": {str(k): int(v) for k, v in counts.items()},
                "threshold": f"< {P10_IMBALANCED_SHARE:.0%}", "provenance": "[I]"},
    }


# ======================================================================================
# §12 admissible set
# ======================================================================================

def mod2_check(df: pd.DataFrame, inputs: list[str]) -> dict:
    """MOD-2 inputs: parameters vs n_train, and exact collinearity (rank of the design matrix with
    intercept, as the model sees it), without and with polynomial terms at the largest degree."""
    out = {}
    for poly in (False, True):
        enc = encoder(inputs, poly)
        if poly:
            enc.set_params(num__degree=max(GRID_DEGREE))
        Z = StandardScaler().fit_transform(enc.fit_transform(df[inputs]))
        D = np.hstack([np.ones((len(Z), 1)), Z])
        rank = int(np.linalg.matrix_rank(D))
        out["poly" if poly else "plain"] = {"parameters": int(D.shape[1]), "n_train": int(len(Z)), "rank": rank,
                                            "applies": bool(D.shape[1] >= len(Z) or rank < D.shape[1])}
    return out


def admissible_set(props: dict, df: pd.DataFrame, inputs: list[str]) -> dict:
    families, gate_tag = TASK_GATE[prop(props, 1)]
    mod2 = mod2_check(df, inputs)
    admissible, removed = [], []
    for name, c in CONFIG.items():
        if c["family"] not in families:
            removed.append({"configuration": name, "code": "EXCL",
                            "evidence": f"task gate, {P[1]} = {prop(props, 1)}: admissible families {sorted(families)} {gate_tag}"})
            continue
        failed = []
        for (n, value), (meets, tag) in MUST_HAVE_GATE.items():
            if prop(props, n) == value and must_have(props, n):
                ok = c["family"] in meets or (c["family"] == "kNN" and "kNN?" in meets
                                               and props.get("kNN_cases_acceptable", False))
                if not ok:
                    failed.append(f"must-have {P[n]} = {value} {tag}")
        if failed:
            removed.append({"configuration": name, "code": "USER", "evidence": "; ".join(failed)})
            continue
        if c["family"] == "Logistic" and not c["l2"] and prop(props, 9) == "yes":
            removed.append({"configuration": name, "code": "EXCL", "evidence": f"MOD-1: {P[9]} = yes [B SML p. 61]"})
            continue
        m2 = mod2["poly" if c["poly"] else "plain"]
        if c["family"] in PARAMETRIC and not c["l2"] and m2["applies"]:
            removed.append({"configuration": name, "code": "EXCL", "evidence": f"MOD-2: {m2} [B→I SML pp. 46–47, 65]"})
            continue
        admissible.append(name)
    return {"task_gate": {P[1]: prop(props, 1), "families": sorted(families), "provenance": gate_tag},
            "must_haves": {P[n]: {"value": prop(props, n), "must_have": must_have(props, n)} for n in (5, 6)},
            "MOD-1": {P[9]: prop(props, 9), "applies": prop(props, 9) == "yes", "provenance": "[B SML p. 61]"},
            "MOD-2": {**mod2, "provenance": "[B→I SML pp. 46–47, 65]"},
            "admissible": admissible, "removed": removed}


# ======================================================================================
# §13, §15 prior ranking
# ======================================================================================

def simple_first(props: dict, admissible: list[str]) -> str:
    plain = SIMPLE_FIRST[prop(props, 1)]
    return plain if plain in admissible else f"{plain} + L2"


def prior_ranking(props: dict, adm: dict) -> dict:
    rows = []
    for name in adm["admissible"]:
        score, entries = matrix_score(name, props)
        rows.append({"configuration": name, "score": score, "addons": addons(name), "entries": entries})
    rows.sort(key=lambda r: (-r["score"], r["addons"]))     # §15.3: score, then fewer add-ons
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
# §16 nested cross-validation, cumulative store per sub-task
# ======================================================================================

def store_path(subtask: str) -> Path:
    return OUT / f"core_cv_store_subtask{subtask}.json"


def load_store(subtask: str, df: pd.DataFrame) -> dict:
    folds = [[int(i) for i in va] for _, va in outer_folds(df)]
    path = store_path(subtask)
    if path.exists():
        store = json.loads(path.read_text(encoding="utf-8"))
        if store["outer_validation_folds"] != folds:
            sys.exit("outer folds differ from the stored ones; refusing to mix fold sets")
        return store
    return {"subtask": subtask, "cv_seed": CV_SEED, "outer_folds": OUTER_FOLDS, "inner_folds": INNER_FOLDS,
            "fold_type": "StratifiedGroupKFold, groups = match_id", "outer_validation_folds": folds,
            "entries": {}}


def baseline_cv(df: pd.DataFrame) -> dict:
    y = df[TARGET].to_numpy()
    rows = []
    for f, (tr, va) in enumerate(outer_folds(df)):
        share = float(y[tr].mean())
        p_tr, p_va = np.full(len(tr), share), np.full(len(va), share)
        rows.append({"fold": f, "best_params": {}, "predicts": share,
                     "neg_logloss_val": -logloss(y[va], p_va), "neg_logloss_train": -logloss(y[tr], p_tr),
                     "e_train": misclass(y[tr], p_tr), "e_val": misclass(y[va], p_va), "convergence_warnings": 0})
    return {"configuration": BASELINE, "structural": None, "post_prior": False, "grid": {},
            "pipeline": "constant probability = training share of goals", "folds": rows}


def nested_cv(name: str, df: pd.DataFrame, inputs: list[str], grid_override, post_prior: bool) -> dict:
    y, g = df[TARGET].to_numpy(), df[GROUP].to_numpy()
    X = df[inputs]
    rows, grid_seen, pipe_repr = [], None, None
    for f, (tr, va) in enumerate(outer_folds(df)):
        search, params, grid, n_warn = fit_search(name, inputs, X.iloc[tr], y[tr], g[tr], grid_override)
        p_tr, p_va = prob1(search, X.iloc[tr]), prob1(search, X.iloc[va])
        rows.append({"fold": f, "best_params": params, "grid_used": grid,
                     "neg_logloss_val": -logloss(y[va], p_va), "neg_logloss_train": -logloss(y[tr], p_tr),
                     "e_train": misclass(y[tr], p_tr), "e_val": misclass(y[va], p_va),
                     "convergence_warnings": n_warn})
        grid_seen = grid
        pipe_repr = repr(search.best_estimator_ if hasattr(search, "best_estimator_") else search)
        print(f"    {name}: fold {f + 1}/{OUTER_FOLDS} done", flush=True)
    return {"configuration": name, "structural": name, "post_prior": post_prior, "grid": grid_seen,
            "grid_override": grid_override, "pipeline": pipe_repr, "folds": rows}


def fold_values(entry: dict, key: str) -> list[float]:
    return [r[key] for r in entry["folds"]]


def most_common_params(entry: dict) -> dict:
    counts = Counter(json.dumps(r["best_params"], sort_keys=True) for r in entry["folds"])
    params, n = counts.most_common(1)[0]
    return {"params": json.loads(params), "folds": f"{n}/{len(entry['folds'])}"}


def cv_table(store: dict) -> dict:
    entries = store["entries"]
    models = [k for k in entries if k != BASELINE]
    mean = {k: float(np.mean(fold_values(entries[k], "neg_logloss_val"))) for k in entries}
    leader = max(models, key=lambda k: mean[k]) if models else None
    rows = []
    for k, e in entries.items():
        v = fold_values(e, "neg_logloss_val")
        row = {"configuration": k, "post_prior": e["post_prior"], "round": e.get("round"),
               "tuned_hyperparameters": most_common_params(e) if k != BASELINE else "n/a",
               "cv_mean_logloss": -mean[k], "fold_sd_logloss": float(np.std(v, ddof=SPREAD_DDOF)),
               "logloss_train": -float(np.mean(fold_values(e, "neg_logloss_train"))),
               "e_train_misclassification": float(np.mean(fold_values(e, "e_train"))),
               "e_val_misclassification": float(np.mean(fold_values(e, "e_val"))),
               "convergence_warnings": int(sum(fold_values(e, "convergence_warnings")))}
        if leader and k != leader:
            m, s = margin(v, fold_values(entries[leader], "neg_logloss_val"))
            row["margin_vs_leader"] = {"mean": m, "spread": s}
        if BASELINE in entries and k != BASELINE:
            m, s = margin(v, fold_values(entries[BASELINE], "neg_logloss_val"))
            row["margin_vs_baseline"] = {"mean": m, "spread": s, "C2": level(m, s, C2_CLEAR)}
        rows.append(row)
    return {"leader": leader, "metric": "log-loss (lower is better); margins in negative log-loss, positive = better",
            "rows": rows}


def run_cv(subtask: str, names: list[str], round_label: str, grid_override=None, post_prior=False, label=None) -> dict:
    df = training_data()
    inputs = SUBTASK_INPUTS[subtask]
    store = load_store(subtask, df)
    added = []
    for name in names:
        key = label or name
        if key in store["entries"]:
            sys.exit(f"'{key}' is already cross-validated; give a new --label for a variant")
        entry = baseline_cv(df) if name == BASELINE else nested_cv(name, df, inputs, grid_override, post_prior)
        entry["round"] = round_label
        store["entries"][key] = entry
        store_path(subtask).write_text(json.dumps(store, indent=1, default=float), encoding="utf-8")
        added.append(key)
    return {"core_version_sha256": version(), "subtask": subtask, "round": round_label, "added": added,
            "table": cv_table(store)}


# ======================================================================================
# §18 observations and learning curve
# ======================================================================================

def learning_curve(entry: dict, df: pd.DataFrame, inputs: list[str]) -> dict:
    """Interpretation l: whole matches sampled at each fraction; hyperparameters fixed per outer fold."""
    y, g = df[TARGET].to_numpy(), df[GROUP].to_numpy()
    X = df[inputs]
    out = []
    for frac in LC_FRACTIONS:
        e_tr, e_va, ll_tr, ll_va = [], [], [], []
        for (tr, va), r in zip(outer_folds(df), entry["folds"]):
            if frac == 1.0:
                sub = tr
            else:
                gss = GroupShuffleSplit(n_splits=1, train_size=frac, random_state=CV_SEED)
                sub = tr[next(gss.split(tr, groups=g[tr]))[0]]
            pipe, _ = build(entry["structural"], inputs)
            model = clone(pipe).set_params(**r["best_params"]).fit(X.iloc[sub], y[sub])
            p_sub, p_va = prob1(model, X.iloc[sub]), prob1(model, X.iloc[va])
            e_tr.append(misclass(y[sub], p_sub))
            e_va.append(misclass(y[va], p_va))
            ll_tr.append(logloss(y[sub], p_sub))
            ll_va.append(logloss(y[va], p_va))
        out.append({"fraction": frac, "e_train_mean": float(np.mean(e_tr)), "e_val_mean": float(np.mean(e_va)),
                    "e_val_fold_sd": float(np.std(e_va, ddof=SPREAD_DDOF)),
                    "logloss_train_mean": float(np.mean(ll_tr)), "logloss_val_mean": float(np.mean(ll_va)), "logloss_val_fold_sd": float(np.std(ll_va, ddof=SPREAD_DDOF))})
    at = {r["fraction"]: r for r in out}
    drop = at[0.8]["logloss_val_mean"] - at[1.0]["logloss_val_mean"]
    c3 = "limited" if drop >= C3_FALLING * at[1.0]["logloss_val_fold_sd"] else "adequate"
    drop_mc = at[0.8]["e_val_mean"] - at[1.0]["e_val_mean"]
    return {"points": out, "C3": {"value": c3, "logloss_val_80_minus_100": drop,
                                  "threshold": f">= {C3_FALLING} x fold SD at 100 % ({at[1.0]['logloss_val_fold_sd']:.5f})"},
            "misclassification_alongside": {"val_80_minus_100": drop_mc, "fold_sd_at_100": at[1.0]["e_val_fold_sd"],
                                            "would_be_limited": bool(drop_mc >= C3_FALLING * at[1.0]["e_val_fold_sd"])}}


def success_threshold_train(df: pd.DataFrame) -> dict:
    """Interpretation j: the sub-task 1 criterion computed on the training shots."""
    y = df[TARGET].to_numpy()
    shots = pd.read_csv(TRAIN_SHOTS, usecols=["shot_id", "statsbomb_xg"]).set_index("shot_id")
    sb = shots.loc[df.shot_id, "statsbomb_xg"].to_numpy()
    ll_base = logloss(y, np.full(len(y), y.mean()))
    ll_sb = logloss(y, sb)
    return {"ll_baseline": ll_base, "ll_statsbomb": ll_sb, "required_logloss": ll_base - SUCCESS_SHARE * (ll_base - ll_sb)}


def observations(subtask: str, key: str) -> dict:
    df = training_data()
    inputs = SUBTASK_INPUTS[subtask]
    store = load_store(subtask, df)
    e = store["entries"][key]
    row = {r["configuration"]: r for r in cv_table(store)["rows"]}[key]
    e_train, e_val = row["logloss_train"], row["cv_mean_logloss"]           # interpretation i
    gap = e_val - e_train
    c2 = row["margin_vs_baseline"]["C2"]
    req = success_threshold_train(df)
    o5 = {}
    for p in (e["grid"] or {}):
        if p == "enc__num__degree":                       # interpretation k
            continue
        edges = sum(r["best_params"][p] in (min(r["grid_used"][p]), max(r["grid_used"][p])) for r in e["folds"])
        o5[p] = {"folds_at_edge": edges, "holds": edges > O5_MOST_FOLDS * len(e["folds"])}
    lc = learning_curve(e, df, inputs)
    mc_train, mc_val = row["e_train_misclassification"], row["e_val_misclassification"]
    obs = {
        "O1": {"holds": c2 != "clear", "C2": c2},
        "O2": {"holds": e_train > req["required_logloss"], "training_logloss": e_train,
               "criterion_on_training_shots": req, "note": "UNLISTED [I] interpretation j"},
        "O3": {"holds": gap >= O3_RATIO * e_train, "gap": gap, "e_train": e_train},
        "O4": {"holds": e_train >= O4_RATIO * gap, "gap": gap, "e_train": e_train},
        "O5": {"holds": any(v["holds"] for v in o5.values()), "by_parameter": o5},
        "O6": {"holds": lc["C3"]["value"] == "limited", "C3": lc["C3"]},
    }
    order = ["O1", "O2", "O5", "O3", "O4", "O6"]
    first = next((o for o in order if obs[o]["holds"]), None)
    return {"core_version_sha256": version(), "subtask": subtask, "configuration": key,
            "diagnosis_error": "log-loss", "e_train": e_train, "e_val": e_val, "gap": gap,
            "misclassification_alongside": {"train": mc_train, "val": mc_val, "gap": mc_val - mc_train,
                                            "O3_would_hold": bool(mc_val - mc_train >= O3_RATIO * mc_train),
                                            "O4_would_hold": bool(mc_train >= O4_RATIO * (mc_val - mc_train)),
                                            "C3_would_be_limited": lc["misclassification_alongside"]["would_be_limited"]},
            "observations": obs, "priority_order": order, "first_that_holds": first,
            "learning_curve": lc["points"]}


# ======================================================================================
# §17 confidence, §19 recommendation, §20 why-not
# ======================================================================================

def recommend(subtask: str) -> dict:
    df = training_data()
    inputs = SUBTASK_INPUTS[subtask]
    props = load_props(subtask)
    store = load_store(subtask, df)
    entries = store["entries"]
    adm = admissible_set(props, df, inputs)
    prior = prior_ranking(props, adm)
    models = [k for k in entries if k != BASELINE]
    f = {k: fold_values(entries[k], "neg_logloss_val") for k in entries}
    mean = {k: float(np.mean(v)) for k, v in f.items()}
    struct = {k: entries[k]["structural"] for k in models}
    score = {k: matrix_score(struct[k], props)[0] for k in models}
    c2 = {k: level(*margin(f[k], f[BASELINE]), C2_CLEAR) for k in models}
    eligible = [k for k in models if c2[k] == "clear"]
    trace = {"1_eligible": {k: {"C2": c2[k], "margin_vs_baseline": margin(f[k], f[BASELINE])} for k in models}}
    if not eligible:
        return {"core_version_sha256": version(), "subtask": subtask, "recommendation": None,
                "reason": "no configuration clearly beats the baseline (§19.1): DX-1 or DX-2", "trace": trace}
    best = max(eligible, key=lambda k: mean[k])
    cands = [best] + [k for k in eligible if k != best
                      and margin(f[best], f[k])[0] < WITHIN_NOISE * margin(f[best], f[k])[1]]
    trace["2_candidates"] = {k: {"cv_mean_logloss": -mean[k],
                                 "margin_best_minus_this": margin(f[best], f[k]) if k != best else (0.0, 0.0)}
                             for k in cands}
    rec = min(cands, key=lambda k: (addons(struct[k]), -score[k], -mean[k]))
    trace["3_choice"] = {k: {"addons": addons(struct[k]), "prior_score": score[k], "cv_mean_logloss": -mean[k]}
                         for k in cands}
    trace["3_chosen"] = rec
    others = [k for k in models if k != rec]
    runner = max(others, key=lambda k: mean[k]) if others else None
    m1, s1 = margin(f[rec], f[runner]) if runner else (math.nan, math.nan)
    C1 = level(m1, s1, C1_CLEAR, C1_MODERATE) if runner else "clear"
    C2 = c2[rec]
    lc = learning_curve(entries[rec], df, inputs)
    C3 = lc["C3"]["value"]
    conf = "High" if (C1 == "clear" and C2 == "clear" and C3 == "adequate") else (
        "Low" if (C1 == "none" or C2 != "clear") else "Medium")
    prior_models = [k for k in models if not entries[k]["post_prior"]]
    winner = max(prior_models, key=lambda k: mean[k])
    prior_order = [r["configuration"] for r in prior["order"] if r["kept"]]
    agreement = "agree" if winner == prior_order[0] else ("partial" if winner in prior_order[:2] else "disagree")
    _, rec_entries = matrix_score(struct[rec], props)
    grounding = Counter("[B]" if e["provenance"].startswith("[B SML") else
                        "[B→I]" if e["provenance"].startswith("[B→I") else "[I]" for e in rec_entries)
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
            why_not.append({"configuration": name, "code": "DISF", "evidence": f"prior score {s}: {[e['entry'] for e in ent]}"})
            continue
        k = max(cvd, key=lambda x: mean[x])
        code = "BASE" if c2[k] != "clear" else ("SIMP" if k in cands else "OUTP")
        mr, sr = margin(f[rec], f[k])
        why_not.append({"configuration": name, "code": code, "entry": k,
                        "evidence": {"margin_rec_minus_this": mr, "spread": sr, "C2": c2[k],
                                     "addons": addons(name), "rec_addons": addons(struct[rec])}})
    common = most_common_params(entries[rec])
    result = {"core_version_sha256": version(), "subtask": subtask, "rows_used": "training only",
              "recommendation": {"entry": rec, "configuration": struct[rec], "tuned_hyperparameters_cv": common},
              "trace": trace, "selection_confidence": {
                  "level": conf, "C1": {"value": C1, "runner_up": runner, "margin": m1, "spread": s1},
                  "C2": {"value": C2, "margin": margin(f[rec], f[BASELINE])}, "C3": lc["C3"],
                  "rule": "High: C1 clear, C2 clear, C3 adequate; Low: C1 none or C2 not clear; otherwise Medium"},
              "prior_agreement": {"value": agreement, "cv_winner_among_prior_kept": winner, "prior_order_kept": prior_order},
              "grounding": dict(grounding), "grounding_entries": rec_entries,
              "breadth_note": {"configurations_compared": len(models), "applies": len(models) > BREADTH_MANY},
              "why_not": why_not, "learning_curve": lc["points"], "decision_threshold": None,
              "final_fit": {"hyperparameters": common["params"], "chosen_in_outer_folds": common["folds"], "inputs": inputs},
              "uncertainty": {"fold_sd_logloss": float(np.std(f[rec], ddof=SPREAD_DDOF)),
                              "method": "spread of the metric across the outer folds (instructions.md, step 4g) [B→I SML pp. 71–73]"}}
    if subtask == "2":
        result["subtask2_comparison"] = compare_with_subtask1(rec)
    return result


def compare_with_subtask1(entry2: str) -> dict:
    """Interpretation o: the team model against the sub-task 1 recommended model, same outer folds."""
    rec1 = json.loads((OUT / "core_recommend_subtask1.json").read_text(encoding="utf-8"))
    df = training_data()
    s1, s2 = load_store("1", df), load_store("2", df)
    if s1["outer_validation_folds"] != s2["outer_validation_folds"]:
        sys.exit("sub-task 1 and 2 folds differ")
    a = fold_values(s2["entries"][entry2], "neg_logloss_val")
    b = fold_values(s1["entries"][rec1["recommendation"]["entry"]], "neg_logloss_val")
    m, s = margin(a, b)
    return {"subtask2_entry": entry2, "subtask1_entry": rec1["recommendation"]["entry"], "margin": m, "spread": s,
            "cv_part_met": bool(m > 0 and m >= 1.0 * s), "rule": "margin >= 1 x spread (DR-11)"}


# ======================================================================================
# §19.4 the single test-set evaluation
# ======================================================================================

def test_inputs() -> pd.DataFrame:
    """The only read of the locked test set."""
    return build_inputs(pd.read_csv(TEST_SHOTS), pd.read_csv(TEST_FRAMES))


def final(subtask: str, approval: str) -> dict:
    target = OUT / f"core_final_subtask{subtask}.json"
    if target.exists():
        sys.exit(f"{target.name} exists: the test set has been used for this sub-task")
    rec = json.loads((OUT / f"core_recommend_subtask{subtask}.json").read_text(encoding="utf-8"))
    if rec["core_version_sha256"] != version():
        sys.exit("core.py changed since `recommend`; re-run from the earliest affected decision")
    df = training_data()
    inputs = rec["final_fit"]["inputs"]
    y = df[TARGET].to_numpy()
    pipe, _ = build(rec["recommendation"]["configuration"], inputs)
    model = clone(pipe).set_params(**rec["final_fit"]["hyperparameters"]).fit(df[inputs], y)
    joblib.dump(model, OUT / f"core_final_model_subtask{subtask}.joblib")
    te = test_inputs()
    yt = te[TARGET].to_numpy()
    p = prob1(model, te[inputs])
    share = float(y.mean())
    p_base = np.full(len(yt), share)
    sb = pd.read_csv(TEST_SHOTS, usecols=["shot_id", "statsbomb_xg"]).set_index("shot_id").loc[te.shot_id, "statsbomb_xg"].to_numpy()

    def scores(q):
        return {"logloss": logloss(yt, q), "brier": float(brier_score_loss(yt, q)),
                "roc_auc": float(roc_auc_score(yt, q)), "predicted_goals": float(np.sum(q))}

    res = {"model": scores(p), "baseline": scores(p_base), "statsbomb_xg": scores(sb)}
    imp_model = res["baseline"]["logloss"] - res["model"]["logloss"]
    imp_sb = res["baseline"]["logloss"] - res["statsbomb_xg"]["logloss"]
    pd.DataFrame({"shot_id": te.shot_id, "match_id": te.match_id, "goal": yt, "p_model": p, "p_baseline": p_base,
                  "statsbomb_xg": sb}).to_csv(OUT / f"core_test_predictions_subtask{subtask}.csv", index=False)
    out = {"core_version_sha256": version(), "subtask": subtask, "approved_by_user": approval,
           "configuration": rec["recommendation"]["configuration"], "hyperparameters": rec["final_fit"]["hyperparameters"],
           "inputs": inputs, "n_test": int(len(yt)), "test_goals": int(yt.sum()), "test_matches": int(te.match_id.nunique()),
           "baseline_share_from_training": share, "results": res,
           "uncertainty": rec["uncertainty"],
           "predictions_file": f"Code/outputs/xg/core_test_predictions_subtask{subtask}.csv"}
    if subtask == "1":
        out["success"] = {"criterion": "(LL_baseline - LL_model) >= 0.9 x (LL_baseline - LL_StatsBomb) on the test shots",
                          "improvement_model": imp_model, "improvement_statsbomb": imp_sb,
                          "share_of_statsbomb_improvement": imp_model / imp_sb if imp_sb else math.nan,
                          "met": bool(imp_model >= SUCCESS_SHARE * imp_sb)}
    else:
        p1 = pd.read_csv(OUT / "core_test_predictions_subtask1.csv").set_index("shot_id").loc[te.shot_id, "p_model"].to_numpy()
        cmp = rec["subtask2_comparison"]
        out["success"] = {"criterion": "CV margin over the sub-task 1 model >= 1 x spread, and lower test log-loss",
                          "cv_part": cmp, "test_logloss_subtask1_model": logloss(yt, p1),
                          "test_part_met": bool(res["model"]["logloss"] < logloss(yt, p1)),
                          "met": bool(cmp["cv_part_met"] and res["model"]["logloss"] < logloss(yt, p1))}
    return out


# ======================================================================================
# Command line
# ======================================================================================

def write(name: str, result: dict) -> None:
    (OUT / name).write_text(json.dumps(result, indent=1, default=float), encoding="utf-8")
    print(json.dumps(result, indent=1, default=float))


def main(argv: list[str]) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command")
    ap.add_argument("args", nargs="*")
    ap.add_argument("--subtask", default="1", choices=["1", "2"])
    ap.add_argument("--grid", default=None)
    ap.add_argument("--label", default=None)
    ap.add_argument("--approved", default=None)
    a = ap.parse_args(argv)
    st = a.subtask
    if a.command == "p9p10":
        df = training_data()
        write("core_p9_p10.json", {"core_version_sha256": version(), "training_rows": len(df),
                                   "subtasks": {k: {"inputs": v, **p9_p10(df, v)} for k, v in SUBTASK_INPUTS.items()}})
    elif a.command == "admset":
        df = training_data()
        write(f"core_admset_subtask{st}.json", {"core_version_sha256": version(), "subtask": st,
                                                **admissible_set(load_props(st), df, SUBTASK_INPUTS[st])})
    elif a.command == "prior":
        df = training_data()
        props = load_props(st)
        adm = admissible_set(props, df, SUBTASK_INPUTS[st])
        write(f"core_prior_subtask{st}.json", {"core_version_sha256": version(), "subtask": st, **prior_ranking(props, adm)})
    elif a.command == "cv":
        kind = a.args[0]
        if kind in ("round1", "round2"):
            df = training_data()
            props = load_props(st)
            prior = prior_ranking(props, admissible_set(props, df, SUBTASK_INPUTS[st]))
            names = [BASELINE, prior["simple_first"]] if kind == "round1" else \
                [k for k in prior["kept"] if k != prior["simple_first"]]
            write(f"core_cv_{kind}_subtask{st}.json", run_cv(st, names, kind))
        elif kind == "add":
            grid = json.loads(a.grid) if a.grid else None
            write(f"core_cv_add_{(a.label or a.args[1]).replace(' ', '_')}_subtask{st}.json",
                  run_cv(st, [a.args[1]], "post-prior", grid, True, a.label))
    elif a.command == "diagnose":
        write(f"core_diagnose_{a.args[0].replace(' ', '_')}_subtask{st}.json", observations(st, a.args[0]))
    elif a.command == "recommend":
        write(f"core_recommend_subtask{st}.json", recommend(st))
    elif a.command == "final":
        if not a.approved:
            sys.exit("final needs --approved with the user's words")
        write(f"core_final_subtask{st}.json", final(st, a.approved))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
