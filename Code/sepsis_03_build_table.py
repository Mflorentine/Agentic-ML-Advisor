"""Sepsis, step 1: builds the derived tables the analysis uses, applying the user's step 1 decisions.

Decisions applied (Demonstration/Sepsis/Appendix.md, Data Summary, Step 1 decisions):
  1. Variables: drop every column that fewer than 10 % of patients in either hospital ever have (DROP_THRESHOLD_PCT).
  2. Rows: set aside every row from the hour SepsisLabel first becomes 1 (leakage).
  3. Cleaning: set clearly impossible values to missing (CLEAN_RULES). Extreme but possible values are kept.
The source files are never modified. Nothing is filled in.

Reads   Attachments/sepsis-physionet-2019/training_setA/*.psv, training_setB/*.psv
Writes  Code/outputs/sepsis/private/hours.csv.gz     one row per kept hour; patient-level data, ODbL, kept out of git
        Code/outputs/sepsis/private/patients.csv.gz  one row per patient: set, whether ever septic, the ICULOS at which
                                                     SepsisLabel first becomes 1 (= t_sepsis - 6), hours kept. The label
                                                     source for step 2, not an input.
        Code/outputs/sepsis/03_build_table.json, 03_build_table.md   counts only (committed)

Run:    cd Code && uv run python sepsis_03_build_table.py
"""
import gzip
import hashlib
import io
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "sepsis-physionet-2019"
OUT = ROOT / "Code" / "outputs" / "sepsis"
PRIVATE = OUT / "private"

DROP_THRESHOLD_PCT = 10  # [I] a column is dropped if fewer than this % of patients in either hospital ever have it
# [I] clearly impossible values; a value outside [low, high] is set to missing. None = no bound on that side.
CLEAN_RULES = {"FiO2": (0.21, 1.0), "Temp": (25, 45), "Potassium": (None, 15), "Hgb": (None, 25)}
NOT_INPUTS = ["ICULOS"]  # kept only to order each stay and define time windows; never an input


def load() -> pd.DataFrame:
    frames = []
    for s in ("A", "B"):
        for f in sorted((SRC / f"training_set{s}").glob("*.psv")):
            d = pd.read_csv(f, sep="|")
            d.insert(0, "patient", f.stem)
            d.insert(1, "set", s)
            frames.append(d)
    return pd.concat(frames, ignore_index=True)


def write_gz(df: pd.DataFrame, path: Path) -> str:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as z:  # mtime=0 so the bytes, and the checksum, are reproducible
        z.write(df.to_csv(index=False, lineterminator="\n").encode("ascii"))
    path.write_bytes(buf.getvalue())
    return hashlib.sha256(buf.getvalue()).hexdigest()


def main() -> None:
    df = load()
    measured = [c for c in df.columns if c not in ("patient", "set", "Age", "Gender", "Unit1", "Unit2",
                                                   "HospAdmTime", "ICULOS", "SepsisLabel")]
    ever = df[measured].notna().groupby([df.set, df.patient]).any()
    pct = ever.groupby(level="set").mean().mul(100)
    drop = [c for c in measured if pct[c].min() < DROP_THRESHOLD_PCT]
    out = {"drop_threshold_pct": DROP_THRESHOLD_PCT,
           "dropped": {c: {"A": round(pct.loc["A", c], 2), "B": round(pct.loc["B", c], 2)} for c in drop}}

    onset = df[df.SepsisLabel == 1].groupby("patient").ICULOS.min()
    patients = df.groupby("patient").agg(set=("set", "first")).reset_index()
    patients["septic"] = patients.patient.isin(onset.index).astype(int)
    patients["label_onset_iculos"] = patients.patient.map(onset)

    hours = df[df.SepsisLabel == 0].drop(columns=drop + ["SepsisLabel"]).reset_index(drop=True)
    patients["hours_kept"] = patients.patient.map(hours.groupby("patient").size()).fillna(0).astype(int)

    cleaned = {}
    for col, (lo, hi) in CLEAN_RULES.items():
        bad = pd.Series(False, index=hours.index)
        if lo is not None:
            bad |= hours[col] < lo
        if hi is not None:
            bad |= hours[col] > hi
        cleaned[col] = {"low": lo, "high": hi, "set_to_missing": int(bad.sum()),
                        "by_set": {s: int((bad & (hours.set == s)).sum()) for s in ("A", "B")},
                        "patients": int(hours.loc[bad, "patient"].nunique())}
        hours.loc[bad, col] = float("nan")
    out["cleaning"] = cleaned

    first = hours.groupby("patient").first()
    out["kept_as_is"] = {
        "hospadmtime_positive_rows": int((hours.HospAdmTime > 0).sum()),
        "hospadmtime_positive_patients": int((first.HospAdmTime > 0).sum()),
        "age_under_18_patients": int((first.Age < 18).sum()),
        "age_min": float(first.Age.min()),
        "age_min_patients": int((first.Age == first.Age.min()).sum()),
        "age_100_patients": {s: int(((first.Age == 100) & (first.set == s)).sum()) for s in ("A", "B")},
    }
    inputs = [c for c in hours.columns if c not in ("patient", "set", *NOT_INPUTS)]
    out["table"] = {
        "hours_rows": len(hours), "hours_columns": list(hours.columns),
        "inputs": inputs, "n_inputs": len(inputs), "categorical_inputs": ["Gender", "Unit1", "Unit2"],
        "patients_total": len(patients), "patients_with_hours": int((patients.hours_kept > 0).sum()),
        "septic_total": int(patients.septic.sum()),
        "septic_with_hours": int(((patients.septic == 1) & (patients.hours_kept > 0)).sum()),
        "by_set": {s: {"rows": int((hours.set == s).sum()),
                       "patients_with_hours": int(((patients.set == s) & (patients.hours_kept > 0)).sum()),
                       "septic_with_hours": int(((patients.set == s) & (patients.septic == 1) & (patients.hours_kept > 0)).sum())}
                   for s in ("A", "B")},
    }

    PRIVATE.mkdir(parents=True, exist_ok=True)
    out["sha256"] = {"private/hours.csv.gz": write_gz(hours, PRIVATE / "hours.csv.gz"),
                     "private/patients.csv.gz": write_gz(patients, PRIVATE / "patients.csv.gz")}
    (OUT / "03_build_table.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    text = "# Sepsis: derived tables (step 1)\n\n```\n" + json.dumps(out, indent=2) + "\n```\n"
    (OUT / "03_build_table.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
