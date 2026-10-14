"""Step 2: shuffled, stratified train/test split; the test set is locked from here on.

Reads   Attachments/heart_failure_clinical_records_dataset.csv (never modified)
Writes  Code/outputs/split.json  (row indices of the training and test sets, seed, counts)

The rows of the source file are sorted by `time` (DR-02), so the split shuffles before
splitting. Stratified by DEATH_EVENT so both parts keep the same share of deaths.
After this script, no step 3 or step 4 code may read the test rows until the single
final evaluation (step 4g).

Run:    cd Code && uv run python 02_split.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
OUT = ROOT / "Code" / "outputs" / "split.json"

SEED = 2026          # agreed with the user (step 2)
TEST_FRACTION = 0.2  # agreed with the user (step 2)
TARGET = "DEATH_EVENT"
NOT_AN_INPUT = ["time"]  # set aside in step 1 (leakage risk); kept in the file


def main() -> None:
    df = pd.read_csv(SRC)
    idx = df.index.to_numpy()
    train_idx, test_idx = train_test_split(
        idx, test_size=TEST_FRACTION, shuffle=True, stratify=df[TARGET], random_state=SEED
    )
    inputs = [c for c in df.columns if c not in [TARGET, *NOT_AN_INPUT]]
    y = df[TARGET]
    result = {
        "source_sha256": hashlib.sha256(SRC.read_bytes()).hexdigest(),
        "seed": SEED,
        "test_fraction": TEST_FRACTION,
        "shuffled": True,
        "stratified_by": TARGET,
        "inputs": inputs,
        "not_an_input": NOT_AN_INPUT,
        "n_train": int(len(train_idx)),
        "n_test": int(len(test_idx)),
        "train_class_counts": {str(k): int(v) for k, v in y.iloc[train_idx].value_counts().sort_index().items()},
        "test_class_counts": {str(k): int(v) for k, v in y.iloc[test_idx].value_counts().sort_index().items()},
        "train_idx": sorted(int(i) for i in train_idx),
        "test_idx": sorted(int(i) for i in test_idx),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print({k: v for k, v in result.items() if not k.endswith("_idx")})


if __name__ == "__main__":
    main()
