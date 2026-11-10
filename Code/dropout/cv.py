"""Interim core, step 4c: nested cross-validation for the dropout analysis. Interim core, not reviewed.

Protocol (ML Guide section 16, as amended 10 November 2026):
  outer: 10 stratified, shuffled folds, seed 2026, the same folds for every configuration;
  inner: 5 stratified folds inside each outer training set, grid search over the L2 strength lambda
         (1e-4 ... 1e4) and, for the polynomial configuration, the degree (2 or 3), and the F2 decision
         threshold (0.05 ... 0.95), chosen by mean inner F2;
  preprocessing (REQ-1): rare category levels (fewer than 10 training students, DR-13), one-hot encoding
         and standardisation are fitted inside each training fold only;
  polynomial terms (DR-19): powers 2 and 3 of the 19 non-binary numeric inputs only.

Scaling of lambda (assumption, to check against SML eq. 3.50): the cost is the mean log-loss plus
(lambda / 2) * ||theta||^2, the intercept is not penalised (REQ-5). scikit-learn minimises C * sum(loss) + 0.5 * ||w||^2,
so C = 1 / (lambda * n_train_fold).

The baseline is the most common training class (SEQ-1): predict "not dropout" for every student.
Fits nothing outside the folds; the test set is never read here.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import fbeta_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEED = 2026
OUTER_K = 10
INNER_K = 5
RARE_MIN = 10                                   # DR-13
LAMBDAS = [10.0 ** k for k in range(-4, 5)]     # 1e-4 ... 1e4
DEGREES = [2, 3]                                # polynomial configuration only
THRESHOLDS = [round(0.05 * i, 2) for i in range(1, 20)]   # 0.05 ... 0.95 (DR-19)

CATEGORICAL = [
    "Marital status", "Application mode", "Course", "Previous qualification", "Nacionality",
    "Mother's qualification", "Father's qualification", "Mother's occupation", "Father's occupation",
]
BINARY = [
    "Displaced", "Educational special needs", "Debtor", "Tuition fees up to date",
    "Gender", "Scholarship holder", "International", "Daytime/evening attendance",
]


class RareGrouper(BaseEstimator, TransformerMixin):
    """Group, within each categorical column, the levels with fewer than RARE_MIN training students into 'other'.
    Fitted on the training rows it is given (the fold's training data)."""

    def __init__(self, cols, rare_min=RARE_MIN):
        self.cols = cols
        self.rare_min = rare_min

    def fit(self, X, y=None):
        self.kept_ = {c: set(X[c].value_counts().loc[lambda s: s >= self.rare_min].index) for c in self.cols}
        return self

    def transform(self, X):
        Z = X[self.cols].copy()
        for c in self.cols:
            # text, so that integer codes and the label "other" can be encoded together
            Z[c] = Z[c].where(Z[c].isin(self.kept_[c]), other="other").astype(str)
        return Z


class AddPowers(BaseEstimator, TransformerMixin):
    """Append powers 2..degree of the standardised non-binary numeric columns.
    Expects the numeric block first (columns 0..n_num-1) and the non-binary positions in `idx`."""

    def __init__(self, degree=1, idx=None):
        self.degree = degree
        self.idx = idx

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = np.asarray(X, dtype=float)
        if self.degree <= 1:
            return X
        base = X[:, self.idx]
        powers = [base ** k for k in range(2, self.degree + 1)]
        return np.hstack([X] + powers)


def build_model(numeric: list, degree: int, lam: float, n_fold_train: int) -> Pipeline:
    """Pipeline: rare-level grouping and one-hot (categorical), standardisation (numeric), optional powers,
    then unregularised-intercept L2 logistic regression with C = 1 / (lambda * n)."""
    nonbin = [i for i, c in enumerate(numeric) if c not in BINARY]
    pre = ColumnTransformer(
        [
            ("num", StandardScaler(), numeric),
            ("cat", Pipeline([
                ("group", RareGrouper(CATEGORICAL)),
                ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]), CATEGORICAL),
        ]
    )
    clf = LogisticRegression(C=1.0 / (lam * n_fold_train), max_iter=5000)
    return Pipeline([
        ("pre", pre),
        ("powers", AddPowers(degree=degree, idx=nonbin)),
        ("clf", clf),
    ])


def f2(y_true, pred):
    return float(fbeta_score(y_true, pred, beta=2, zero_division=0))


def inner_search(X: pd.DataFrame, y: pd.Series, numeric: list, degrees: list) -> dict:
    """Grid search inside one outer training set. Returns the chosen (degree, lambda, threshold) and the inner scores."""
    inner = StratifiedKFold(n_splits=INNER_K, shuffle=True, random_state=SEED)
    folds = list(inner.split(X, y))
    best = None
    table = []
    for degree in degrees:
        for lam in LAMBDAS:
            per_fold_proba = []
            for tr, va in folds:
                m = build_model(numeric, degree, lam, n_fold_train=len(tr))
                m.fit(X.iloc[tr], y.iloc[tr])
                per_fold_proba.append((va, m.predict_proba(X.iloc[va])[:, 1]))
            for t in THRESHOLDS:
                scores = [f2(y.iloc[va], (p >= t).astype(int)) for va, p in per_fold_proba]
                mean_f2 = float(np.mean(scores))
                table.append({"degree": degree, "lambda": lam, "threshold": t, "inner_mean_F2": mean_f2})
                if best is None or mean_f2 > best["inner_mean_F2"]:
                    best = {"degree": degree, "lambda": lam, "threshold": t, "inner_mean_F2": mean_f2}
    return {"chosen": best, "table": table}


def run_outer(X: pd.DataFrame, y: pd.Series, numeric: list, configuration: str) -> list:
    """Outer 10-fold comparison for one configuration. configuration: 'Baseline', 'Logistic + L2', 'Logistic + poly + L2'."""
    outer = StratifiedKFold(n_splits=OUTER_K, shuffle=True, random_state=SEED)
    rows = []
    for k, (tr, te) in enumerate(outer.split(X, y), start=1):
        Xtr, ytr, Xte, yte = X.iloc[tr], y.iloc[tr], X.iloc[te], y.iloc[te]
        if configuration == "Baseline":
            base = DummyClassifier(strategy="most_frequent").fit(Xtr, ytr)
            pred_te = base.predict(Xte)
            pred_tr = base.predict(Xtr)
            rows.append({
                "fold": k, "configuration": configuration, "degree": None, "lambda": None, "threshold": None,
                "F2_test": f2(yte, pred_te), "E_train": float(np.mean(pred_tr != ytr)), "E_val": float(np.mean(pred_te != yte)),
                "n_train": len(tr), "n_test": len(te), "test_positives": int(yte.sum()),
            })
            continue
        degrees = [1] if configuration == "Logistic + L2" else DEGREES
        search = inner_search(Xtr, ytr, numeric, degrees)
        c = search["chosen"]
        m = build_model(numeric, c["degree"], c["lambda"], n_fold_train=len(tr))
        m.fit(Xtr, ytr)
        p_tr = m.predict_proba(Xtr)[:, 1]
        p_te = m.predict_proba(Xte)[:, 1]
        pred_tr = (p_tr >= c["threshold"]).astype(int)
        pred_te = (p_te >= c["threshold"]).astype(int)
        rows.append({
            "fold": k, "configuration": configuration, "degree": c["degree"], "lambda": c["lambda"], "threshold": c["threshold"],
            "F2_test": f2(yte, pred_te), "E_train": float(np.mean(pred_tr != ytr)), "E_val": float(np.mean(pred_te != yte)),
            "inner_mean_F2": c["inner_mean_F2"], "n_train": len(tr), "n_test": len(te), "test_positives": int(yte.sum()),
        })
    return rows
