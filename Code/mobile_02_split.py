"""Mobile Price, step 2: shuffled, stratified train/test split; the test set is locked from here on.

Reads   Attachments/Mobile Price/train.csv (never modified; test.csv is excluded, step 1 scope decision)
Writes  Code/outputs/mobile/split.json  (row indices of the training and test sets, seed, counts,
        and the counts behind P2-P4; indices only, no data values)

Stratified by price_range so both parts keep 25 % per band. The rows are treated as independent
(ADM-3, DR-02), so the split is by row. After this script, no step 3 or step 4 code may read the
test rows until the single final evaluation (step 4g).

Run:    cd Code && uv run python mobile_02_split.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "Mobile Price" / "train.csv"
OUT = ROOT / "Code" / "outputs" / "mobile" / "split.json"

SEED = 2026          # agreed with the user (step 2)
TEST_FRACTION = 0.2  # agreed with the user (step 2)
TARGET = "price_range"

# Input design agreed in step 2: all 20 columns; the six 0/1 indicators are categorical
# (one column each after encoding); n_cores and the other 13 are numerical.
CATEGORICAL = ["blue", "dual_sim", "four_g", "three_g", "touch_screen", "wifi"]

# [I] thresholds from ML Guide.md section 11.
P2_LIMITED_BELOW = 10   # data-to-parameter ratio
P3_MANY_ABOVE = 20      # input columns after encoding
P4_HIGH_FROM = 0.5      # share of categorical input columns


def main() -> None:
    df = pd.read_csv(SRC)
    inputs = [c for c in df.columns if c != TARGET]
    numerical = [c for c in inputs if c not in CATEGORICAL]
    y = df[TARGET]

    train_idx, test_idx = train_test_split(
        df.index.to_numpy(), test_size=TEST_FRACTION, shuffle=True, stratify=y, random_state=SEED
    )

    # A 0/1 indicator one-hot encodes to a single column (one level dropped).
    encoded_columns = len(numerical) + sum(df[c].nunique() - 1 for c in CATEGORICAL)
    n_train = int(len(train_idx))
    ratio = n_train / (encoded_columns + 1)
    share_categorical = len(CATEGORICAL) / len(inputs)

    result = {
        "source_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
        "seed": SEED,
        "test_fraction": TEST_FRACTION,
        "shuffled": True,
        "stratified_by": TARGET,
        "inputs": inputs,
        "categorical_inputs": CATEGORICAL,
        "numerical_inputs": numerical,
        "n_train": n_train,
        "n_test": int(len(test_idx)),
        "train_class_counts": {str(k): int(v) for k, v in y.iloc[train_idx].value_counts().sort_index().items()},
        "test_class_counts": {str(k): int(v) for k, v in y.iloc[test_idx].value_counts().sort_index().items()},
        "properties": {
            "P2_ratio": ratio,
            "P2": "limited" if ratio < P2_LIMITED_BELOW else "ample",
            "P3_encoded_columns": encoded_columns,
            "P3": "many" if encoded_columns > P3_MANY_ABOVE else "few",
            "P4_share_categorical": share_categorical,
            "P4": "high" if share_categorical >= P4_HIGH_FROM else "low",
        },
        "train_idx": sorted(int(i) for i in train_idx),
        "test_idx": sorted(int(i) for i in test_idx),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if not k.endswith("_idx")}, indent=2))


if __name__ == "__main__":
    main()
