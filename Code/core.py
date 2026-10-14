"""Interim core for this analysis (instructions.md, "Until Code/advisor/ exists").

INTERIM CORE, NOT REVIEWED. It implements the Part II sections of ML Guide.md that the
analysis needs, as literally as possible, with every [I] threshold as a named constant.
Decision Records quote this file's SHA-256 as the code version.

Contents so far (step 3):
  §11  P9  classes perfectly separable in the training data
  §11  P10 class imbalance in the training data
Sections §12, §13/§15, §16, §17 and §19 are added before step 4b and shown to the user
before their first output is used.

Reads only the TRAINING rows listed in Code/outputs/split.json. The test rows are locked
(DR-06) and are never read here.

Run:    cd Code && uv run python core.py p9p10      -> Code/outputs/core_p9_p10.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
SPLIT = CODE / "outputs" / "split.json"
OUT = CODE / "outputs"

TARGET = "DEATH_EVENT"

# ---- [I] thresholds (ML Guide.md, Appendix to Part II) ----
P9_SEPARABLE_ACCURACY = 1.0   # separable if training accuracy reaches 100 % ...
P9_NEGLIGIBLE_C = 1e8         # ... with negligible regularisation (C = 1/lambda very large)
P10_IMBALANCED_SHARE = 0.20   # imbalanced if the smallest class is < 20 % of training rows


def version() -> str:
    """SHA-256 of this file: the code version quoted in Decision Records."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def training_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Training rows only, inputs as fixed in step 2 (`time` excluded)."""
    split = json.loads(SPLIT.read_text(encoding="utf-8"))
    df = pd.read_csv(SRC)
    train = df.iloc[split["train_idx"]]
    inputs = split["inputs"]
    return train[inputs], train[TARGET], inputs


def p9_p10(X: pd.DataFrame, y: pd.Series) -> dict:
    """§11 P9 and P10, computed on the training rows.

    P9: logistic regression with negligible regularisation is fitted to the training rows;
    the classes count as perfectly separable if it classifies every training row correctly.
    This fit establishes a property only; it is not a candidate model and is not evaluated.
    P10: share of the smallest class among the training rows.
    """
    model = Pipeline([("scale", StandardScaler()),
                      ("m", LogisticRegression(C=P9_NEGLIGIBLE_C, max_iter=200_000))])
    model.fit(X, y)
    accuracy = float((model.predict(X) == y).mean())
    counts = y.value_counts().sort_index()
    smallest = float(counts.min() / counts.sum())
    return {
        "P9": {"value": "yes" if accuracy >= P9_SEPARABLE_ACCURACY else "no",
               "training_accuracy_negligible_regularisation": accuracy,
               "C_used": P9_NEGLIGIBLE_C, "threshold": "100 % training accuracy", "provenance": "[I] procedure"},
        "P10": {"value": "imbalanced" if smallest < P10_IMBALANCED_SHARE else "balanced",
                "smallest_class_share": smallest, "class_counts": {str(k): int(v) for k, v in counts.items()},
                "threshold": f"< {P10_IMBALANCED_SHARE:.0%}", "provenance": "[I] threshold"},
    }


def main(argv: list[str]) -> None:
    if argv[1:] != ["p9p10"]:
        sys.exit("usage: uv run python core.py p9p10")
    X, y, inputs = training_data()
    result = {"core_version_sha256": version(), "rows_used": "training only",
              "n_train": int(len(y)), "inputs": inputs, **p9_p10(X, y)}
    (OUT / "core_p9_p10.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(sys.argv)
