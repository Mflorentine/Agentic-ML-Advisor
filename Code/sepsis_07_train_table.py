"""Sepsis, step 3: the training table, one row per TRAINING patient, with the input design of DR-09.

Input design (user, 18 October 2026, DR-09):
  - for each of the 27 clinical columns, the last (most recent) value in ICU hours 1-6;
  - for each clinical column, a 0/1 indicator: was it measured at least once in hours 1-6;
  - Age, Gender, HospAdmTime (constant within a stay);
  - Unit as one categorical input: MICU (Unit1 = 1), SICU (Unit2 = 1) or unknown, from the last
    non-empty Unit1/Unit2 value in hours 1-6 (nothing after hour 6 is used).
Empty last values are left empty here. Filling (training-fold median), the logarithms and the encoding
are fitted or applied inside the model pipeline (Code/sepsis/core.py), so they are refitted in every fold.
Hospital (set) is kept in the table for stratification only; it is not an input (step 1, DR-09).

Only the training patients of the locked split are kept (cohort.csv.gz, split == "train"). The hourly
file holds every patient, so it is filtered to the training patients as soon as it is read; no test
patient's values enter the table, the counts or any figure.

Reads   Code/outputs/sepsis/private/hours.csv.gz, patients.csv.gz, cohort.csv.gz
Writes  Code/outputs/sepsis/private/train_table.csv.gz   (patient-level, not in git)
        Code/outputs/sepsis/07_train_table.json, 07_train_table.md   (aggregates only)

Run:    cd Code && uv run python sepsis_07_train_table.py
"""
import json
from pathlib import Path

import pandas as pd

from sepsis_03_build_table import write_gz

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
PRIVATE = OUT / "private"

N = 6  # window: ICU hours 1-6 (DR-05)
CLINICAL = ["HR", "O2Sat", "Temp", "SBP", "MAP", "DBP", "Resp", "FiO2", "pH", "PaCO2", "SaO2", "AST", "BUN",
            "Alkalinephos", "Calcium", "Creatinine", "Glucose", "Lactate", "Magnesium", "Phosphate", "Potassium",
            "Bilirubin_total", "Hct", "Hgb", "PTT", "WBC", "Platelets"]
CONSTANT = ["Age", "Gender", "HospAdmTime"]


def main() -> None:
    cohort = pd.read_csv(PRIVATE / "cohort.csv.gz")
    train = cohort[cohort.split == "train"].set_index("patient")
    hours = pd.read_csv(PRIVATE / "hours.csv.gz")
    hours = hours[hours.patient.isin(train.index)]                      # training patients only
    win = hours[hours.ICULOS <= N].sort_values(["patient", "ICULOS"])
    g = win.groupby("patient")

    last = g[CLINICAL].last()                                           # last non-empty value in the window
    measured = g[CLINICAL].count().gt(0).astype(int).add_prefix("measured_")
    const = g[CONSTANT].first()
    u1, u2 = g.Unit1.last(), g.Unit2.last()
    unit = pd.Series("unknown", index=u1.index)
    unit[u1 == 1] = "MICU"
    unit[u2 == 1] = "SICU"
    assert not ((u1 == 1) & (u2 == 1)).any()

    table = train[["set", "y"]].join([last, measured, const, unit.rename("Unit")], how="left")
    assert len(table) == len(train) and table[CONSTANT].notna().all().all()
    table = table.reset_index()

    onset = pd.read_csv(PRIVATE / "patients.csv.gz", usecols=["patient", "label_onset_iculos"]).set_index("patient")
    pos = table[table.y == 1].join(onset, on="patient")
    assert pos.label_onset_iculos.between(N + 1, N + 48).all()

    inputs = CLINICAL + list(measured.columns) + CONSTANT + ["Unit"]
    by = {s: table[table.set == s] for s in ("A", "B")}
    out = {
        "rows": "training patients only (split == train)",
        "n_train": len(table),
        "positive": int(table.y.sum()),
        "positive_by_set": {s: int(t.y.sum()) for s, t in by.items()},
        "patients_by_set": {s: len(t) for s, t in by.items()},
        "inputs": inputs,
        "n_input_columns": len(inputs),
        "categorical_input_columns": [f"measured_{c}" for c in CLINICAL] + ["Gender", "Unit"],
        "unit_levels": {k: int(v) for k, v in table.Unit.value_counts().items()},
        "measured_pct": {c: round(100 * table[f"measured_{c}"].mean(), 2) for c in CLINICAL},
        "measured_pct_by_set": {s: {c: round(100 * t[f"measured_{c}"].mean(), 2) for c in CLINICAL} for s, t in by.items()},
        "no_clinical_value_in_window": int((table[[f"measured_{c}" for c in CLINICAL]].sum(axis=1) == 0).sum()),
        "last_value_min": {c: float(table[c].min()) for c in CLINICAL},
        "positive_label_onset_iculos_counts_by_set": {
            s: {str(h): int(v) for h, v in pos[pos.set == s].label_onset_iculos.value_counts().sort_index().items()}
            for s in ("A", "B")},
    }
    out["sha256"] = {"private/train_table.csv.gz": write_gz(table, PRIVATE / "train_table.csv.gz")}
    (OUT / "07_train_table.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    text = "# Sepsis: training table (step 3)\n\n```\n" + json.dumps(out, indent=2) + "\n```\n"
    (OUT / "07_train_table.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
