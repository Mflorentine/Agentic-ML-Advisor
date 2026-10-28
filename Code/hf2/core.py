"""Interim core for the Heart Failure rerun (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the analysis needs,
as literally as possible, with every [I] threshold as a named constant. Decision Records quote this
file's SHA-256 as the code version. Code/core.py (the earlier Heart Failure analysis), Code/sepsis/core.py
and Code/mobile/core.py belong to other analyses and are neither used nor changed.

Contents so far (step 3):
  input design   the preprocessing of DR-08, shared by every model family     (used from step 3)
  §11  P9, P10   properties from the training patients                        (step 3)
Sections §12-§19 are added before step 4b and shown to the user then.

Reads Attachments/heart_failure_clinical_records_dataset.csv and keeps only the 239 training rows listed in
Code/outputs/hf2/split.json ("train_idx"). The 60 test rows are dropped on reading, before any computation,
and the function asserts that none of them is kept.

Interpretations made in this file, where Part II does not say exactly what to do:
  a. Input design (DR-08): the 11 inputs as recorded, no transformation; `time` is not an input (step 1).
     The five 0/1 indicators are one-hot encoded (REQ-6, p. 49) with one level dropped, which leaves each
     as the same single 0/1 column. The six numerical inputs pass through unchanged. Scaling is not part
     of the input design: it belongs to the families that need it (REQ-2, REQ-3) and is added there.
  b. The P9 fit standardises all 11 columns before logistic regression, as for Logistic and k-NN in
     step 4. Encoding and scaling are fitted once on all training patients, because P9 is a property of
     the training data, not a cross-validated estimate.
  c. "Negligible regularisation" is C = 1e8 (lambda = 1e-8) in LogisticRegression, as in the other
     interim cores.
  d. Predicted class for the P9 accuracy: y = 1 if the probability of class 1 is > 0.5 (p. 53).

Run (from Code/):
  uv run python hf2/core.py p9p10
"""
from __future__ import annotations

import hashlib
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CODE = Path(__file__).resolve().parent.parent
ROOT = CODE.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
SPLIT = CODE / "outputs" / "hf2" / "split.json"
OUT = CODE / "outputs" / "hf2"

TARGET = "DEATH_EVENT"
CLASSES = [0, 1]

# ---- Input design (DR-08): which columns, which fixed transforms ----
CATEGORICAL = ["anaemia", "diabetes", "high_blood_pressure", "sex", "smoking"]           # 0/1 indicators
NUMERICAL = ["age", "creatinine_phosphokinase", "ejection_fraction", "platelets", "serum_creatinine",
             "serum_sodium"]                                                              # as recorded
INPUTS = NUMERICAL + CATEGORICAL
NOT_INPUTS = ["time"]                                                                    # step 1, leakage
TRANSFORMED: list[str] = []                                                              # none (DR-08)

# ---- [I] thresholds (ML Guide.md, section 11 and Appendix to Part II) ----
P9_SEPARABLE_ACCURACY = 1.0  # separable if training accuracy reaches 100 % ...
P9_NEGLIGIBLE_C = 1e8        # ... with negligible regularisation (interpretation c)
P10_IMBALANCED_SHARE = 0.20  # imbalanced if the smallest class is < 20 % of training rows
DEFAULT_THRESHOLD = 0.5      # p. 53 (interpretation d)

LOGISTIC_MAX_ITER = 100_000


def version() -> str:
    """SHA-256 of this file: the code version quoted in Decision Records."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def training_data() -> tuple[pd.DataFrame, pd.Series]:
    """The 239 training patients only, with the DR-08 inputs as recorded."""
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    train_idx, test_idx = split["train_idx"], set(split["test_idx"])
    df = pd.read_csv(SRC).loc[train_idx]
    assert not test_idx.intersection(df.index), "a test row was read"
    assert len(df) == split["n_train"]
    assert sorted(INPUTS) == sorted(split["inputs"])
    return df[INPUTS], df[TARGET]


def preprocessor() -> ColumnTransformer:
    """DR-08 input design. Every learned step is fitted on the data it is given, so inside
    cross-validation it is refitted in each fold (REQ-1). Same for every model family."""
    return ColumnTransformer([
        ("as_recorded", "passthrough", NUMERICAL),
        ("indicators", OneHotEncoder(drop="if_binary", categories=[[0, 1]] * len(CATEGORICAL)), CATEGORICAL),
    ], verbose_feature_names_out=False)


def p9_p10(X: pd.DataFrame, y: pd.Series) -> dict:
    """§11 P9 and P10, computed on the training patients, with the DR-08 input design.

    P9: logistic regression with negligible regularisation is fitted to the training patients; the classes
    count as perfectly separable if it classifies every training patient correctly. This fit establishes
    a property only; it is not a candidate model and is not evaluated.
    P10: share of the smallest class among the training patients.
    """
    model = Pipeline([("design", preprocessor()), ("scale", StandardScaler()),
                      ("m", LogisticRegression(C=P9_NEGLIGIBLE_C, max_iter=LOGISTIC_MAX_ITER))])
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model.fit(X, y)
    pred = (model.predict_proba(X)[:, 1] > DEFAULT_THRESHOLD).astype(int)            # interpretation d
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
               "prediction_rule": "y = 1 if p > 0.5 (interpretation d)",
               "threshold": "100 % training accuracy", "provenance": "[I] procedure"},
        "P10": {"value": "imbalanced" if smallest < P10_IMBALANCED_SHARE else "balanced",
                "smallest_class_share": smallest, "class_counts": {str(k): int(v) for k, v in counts.items()},
                "threshold": f"< {P10_IMBALANCED_SHARE:.0%}", "provenance": "[I] threshold"},
        "input_columns_after_encoding": n_columns,
        "transformed_inputs": TRANSFORMED,
    }


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
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
