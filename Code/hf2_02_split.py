"""Heart Failure rerun, step 2: the training/test split, reusing the earlier analysis's test set (user's choice), and
the counts behind P2-P4 for this rerun's input design. The test set is locked from here on.

Reads   Code/outputs/split.json   (the earlier analysis's split, commit 5338393; READ ONLY, never changed)
        Attachments/heart_failure_clinical_records_dataset.csv (never modified)
Writes  Code/outputs/hf2/split.json   (row indices of the training and test sets, counts, input design, P2-P4)

The earlier split is used only for its row indices. Before reuse, its source checksum and its settings (20 % test,
shuffled, stratified by DEATH_EVENT, seed 2026) are checked, and the indices are checked to be a partition of the
299 rows. Its class counts are recomputed here from the data, not copied. After this script, no step 3 or step 4 code
may read the test rows until the single final evaluation (step 4g).

Run:    cd Code && uv run python hf2_02_split.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
OLD_SPLIT = ROOT / "Code" / "outputs" / "split.json"
OUT = ROOT / "Code" / "outputs" / "hf2" / "split.json"

TARGET = "DEATH_EVENT"
NOT_AN_INPUT = ["time"]                                   # set aside in step 1 (leakage), Data Summary
CATEGORICAL = ["anaemia", "diabetes", "high_blood_pressure", "sex", "smoking"]   # 0/1 indicators

# [I] thresholds from ML Guide.md section 11.
P2_LIMITED_BELOW = 10
P3_MANY_ABOVE = 20
P4_HIGH_FROM = 0.5


def main() -> None:
    raw = SRC.read_bytes()
    df = pd.read_csv(SRC)
    old = json.loads(OLD_SPLIT.read_text(encoding="utf-8"))
    assert old["source_sha256"] == hashlib.sha256(raw).hexdigest(), "earlier split was made on different data"
    assert (old["test_fraction"], old["shuffled"], old["stratified_by"], old["seed"]) == (0.2, True, TARGET, 2026)
    train_idx, test_idx = sorted(old["train_idx"]), sorted(old["test_idx"])
    assert not set(train_idx) & set(test_idx) and sorted(train_idx + test_idx) == list(range(len(df)))

    inputs = [c for c in df.columns if c not in [TARGET, *NOT_AN_INPUT]]
    numerical = [c for c in inputs if c not in CATEGORICAL]
    y = df[TARGET]
    encoded = len(numerical) + sum(df[c].nunique() - 1 for c in CATEGORICAL)
    ratio = len(train_idx) / (encoded + 1)
    share = len(CATEGORICAL) / len(inputs)
    result = {
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "split_source": "earlier analysis Code/outputs/split.json (commit 5338393), indices reused, file not changed",
        "seed_of_source_split": old["seed"], "test_fraction": old["test_fraction"], "shuffled": old["shuffled"],
        "stratified_by": old["stratified_by"],
        "inputs": inputs, "categorical_inputs": CATEGORICAL, "numerical_inputs": numerical, "not_an_input": NOT_AN_INPUT,
        "n_train": len(train_idx), "n_test": len(test_idx),
        "train_class_counts": {str(k): int(v) for k, v in y.iloc[train_idx].value_counts().sort_index().items()},
        "test_class_counts": {str(k): int(v) for k, v in y.iloc[test_idx].value_counts().sort_index().items()},
        "properties": {"P2_ratio": ratio, "P2": "limited" if ratio < P2_LIMITED_BELOW else "ample",
                       "P3_encoded_columns": encoded, "P3": "many" if encoded > P3_MANY_ABOVE else "few",
                       "P4_share_categorical": share, "P4": "high" if share >= P4_HIGH_FROM else "low"},
        "train_idx": train_idx, "test_idx": test_idx,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if not k.endswith("_idx")}, indent=2))


if __name__ == "__main__":
    main()
