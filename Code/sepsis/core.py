"""Interim core for the Sepsis analysis (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the analysis needs,
as literally as possible, with every [I] threshold as a named constant. Decision Records quote this
file's SHA-256 as the code version. Code/core.py belongs to the Heart Failure analysis and is not used.

Contents so far (step 3):
  input design   the preprocessing pipeline of DR-09, shared by every model family     (used from step 3)
  §11  P9, P10   properties from the training patients                                 (step 3)
Sections §12-§19 are added before step 4b and shown to the user then.

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

Run (from Code/):
  uv run python sepsis/core.py p9p10
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
