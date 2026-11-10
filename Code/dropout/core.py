"""Interim core for the dropout analysis. Interim core, not reviewed.

Implements, for the dropout analysis only:
  Property 10: class imbalance (ML Guide section 11)
  Property 9:  classes perfectly separable (ML Guide section 11)

Both use the training rows only. The separability check fits one unregularised logistic regression
to establish a property, not to evaluate a candidate; its result is not interpreted as a finding.

Every [I] threshold is a named constant below.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# [I] Property 10: imbalanced if the smallest class is below this share of training rows (ML Guide section 11)
IMBALANCE_SHARE = 0.20
# [I] Property 9: separable if an unregularised logistic regression reaches this training accuracy (ML Guide section 11)
SEPARABLE_TRAIN_ACCURACY = 1.0
# Convergence budget for the unregularised fit (not a threshold on the result)
SEPARABILITY_MAX_ITER = 10000

# Categorical inputs, as decided with the user (DR-05). All other inputs are numeric.
CATEGORICAL = [
    "Marital status",
    "Application mode",
    "Course",
    "Previous qualification",
    "Nacionality",
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation",
]


def property_10_imbalance(y_train: pd.Series) -> dict:
    """Property 10: balanced or imbalanced, from the smallest class share of the training rows."""
    counts = y_train.value_counts()
    smallest_share = counts.min() / counts.sum()
    value = "imbalanced" if smallest_share < IMBALANCE_SHARE else "balanced"
    return {
        "property": "Property 10: class imbalance",
        "value": value,
        "smallest_class_share": float(smallest_share),
        "class_counts": {str(k): int(v) for k, v in counts.items()},
        "threshold": IMBALANCE_SHARE,
        "evidence": "T",
        "provenance": "[I]",
    }


def property_9_separable(X_train: pd.DataFrame, y_train: pd.Series, seed: int = 2026) -> dict:
    """Property 9: can an unregularised logistic regression separate the training classes perfectly?

    Inputs are encoded and standardised inside the pipeline, fitted on the training rows only (REQ-1, REQ-3).
    Regularisation is switched off explicitly (C = infinity, the scikit-learn replacement for penalty=None), as the implementation notes require (ML Guide section 9).
    """
    numeric = [c for c in X_train.columns if c not in CATEGORICAL]
    pre = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
            ("num", StandardScaler(), numeric),
        ]
    )
    model = Pipeline(
        [
            ("prep", pre),
            ("clf", LogisticRegression(C=np.inf, max_iter=SEPARABILITY_MAX_ITER, random_state=seed)),
        ]
    )
    model.fit(X_train, y_train)
    train_acc = float(model.score(X_train, y_train))
    value = "yes" if train_acc >= SEPARABLE_TRAIN_ACCURACY else "no"
    n_iter = int(np.max(model.named_steps["clf"].n_iter_))
    return {
        "property": "Property 9: classes perfectly separable",
        "value": value,
        "training_accuracy": train_acc,
        "threshold": SEPARABLE_TRAIN_ACCURACY,
        "solver_iterations": n_iter,
        "max_iter": SEPARABILITY_MAX_ITER,
        "evidence": "T",
        "provenance": "[I]",
    }
