"""Sepsis, step 4g: the test table, one row per TEST patient, built exactly as the training table.

Run only after the user has approved using the test set (instructions.md, step 4f). It reads the test
patients' hours for the first time in the analysis. It computes no metric and no outcome statistic: the
single evaluation is done by the core (`sepsis/core.py final`), which reads the table this script writes.

The rows are built by `build(split)`, the same construction as sepsis_07_train_table.py (DR-09 input
design: last value in ICU hours 1-6, measured indicators, Age, Gender, HospAdmTime, Unit). Before writing
anything, the script rebuilds the TRAINING table with `build("train")` and checks that it equals the
stored training table exactly, so the test rows cannot have been built differently.

Reads   Code/outputs/sepsis/private/hours.csv.gz, patients.csv.gz, cohort.csv.gz, train_table.csv.gz
Writes  Code/outputs/sepsis/private/test_table.csv.gz   (patient-level, not in git)
        Code/outputs/sepsis/12_test_table.json          (row and column counts, checksums; no outcome data
                                                         beyond the counts already recorded in DR-08)

Run:    cd Code && uv run python sepsis_12_test_table.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd

from sepsis_03_build_table import write_gz
from sepsis_07_train_table import CLINICAL, CONSTANT, N

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
PRIVATE = OUT / "private"


def build(split: str, hours: pd.DataFrame, cohort: pd.DataFrame) -> pd.DataFrame:
    """One row per patient of `split`, as in sepsis_07_train_table.main()."""
    pats = cohort[cohort.split == split].set_index("patient")
    win = hours[hours.patient.isin(pats.index) & (hours.ICULOS <= N)].sort_values(["patient", "ICULOS"])
    g = win.groupby("patient")
    last = g[CLINICAL].last()
    measured = g[CLINICAL].count().gt(0).astype(int).add_prefix("measured_")
    const = g[CONSTANT].first()
    u1, u2 = g.Unit1.last(), g.Unit2.last()
    unit = pd.Series("unknown", index=u1.index)
    unit[u1 == 1] = "MICU"
    unit[u2 == 1] = "SICU"
    assert not ((u1 == 1) & (u2 == 1)).any()
    table = pats[["set", "y"]].join([last, measured, const, unit.rename("Unit")], how="left")
    assert len(table) == len(pats)
    if split == "train":                                    # as in sepsis_07; test rows may have gaps, which the
        assert table[CONSTANT].notna().all().all()          # core fills with the training median (DR-19)
    return table.reset_index()


def main() -> None:
    cohort = pd.read_csv(PRIVATE / "cohort.csv.gz")
    hours = pd.read_csv(PRIVATE / "hours.csv.gz")

    stored = pd.read_csv(PRIVATE / "train_table.csv.gz")
    rebuilt = build("train", hours, cohort)
    pd.testing.assert_frame_equal(rebuilt.reset_index(drop=True), stored, check_dtype=False)

    test = build("test", hours, cohort)
    assert not set(test.patient) & set(stored.patient), "a test patient is also a training patient"
    assert list(test.columns) == list(stored.columns)
    out = {
        "rows": "test patients only (split == test)",
        "n_test": len(test),
        "positive": int(test.y.sum()),
        "patients_by_set": {s: int((test.set == s).sum()) for s in ("A", "B")},
        "columns": list(test.columns),
        "empty_constant_inputs": {c: int(test[c].isna().sum()) for c in CONSTANT},   # filled by the core (DR-19)
        "training_table_rebuilt_identically": True,
        "train_table_sha256": hashlib.sha256((PRIVATE / "train_table.csv.gz").read_bytes()).hexdigest(),
    }
    out["sha256"] = {"private/test_table.csv.gz": write_gz(test, PRIVATE / "test_table.csv.gz")}
    (OUT / "12_test_table.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
