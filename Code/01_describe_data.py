"""Step 1, describing pass: what is in the source file, with no judgement about what it means.

Reads   Attachments/heart_failure_clinical_records_dataset.csv (never modified)
Writes  Code/outputs/01_describe.json  and  Code/outputs/01_describe.md

Run:    cd Code && uv run python 01_describe_data.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
OUT = ROOT / "Code" / "outputs"

# Meanings and units as documented on the UCI page (dataset 519), not inferred from the names.
DOC = {
    "age": ("age of the patient", "years"),
    "anaemia": ("decrease of red blood cells or hemoglobin", "boolean"),
    "creatinine_phosphokinase": ("level of the CPK enzyme in the blood", "mcg/L"),
    "diabetes": ("if the patient has diabetes", "boolean"),
    "ejection_fraction": ("percentage of blood leaving the heart at each contraction", "%"),
    "high_blood_pressure": ("if the patient has hypertension", "boolean"),
    "platelets": ("platelets in the blood", "kiloplatelets/mL"),
    "serum_creatinine": ("level of serum creatinine in the blood", "mg/dL"),
    "serum_sodium": ("level of serum sodium in the blood", "mEq/L"),
    "sex": ("woman or man", "binary"),
    "smoking": ("if the patient smokes or not", "boolean"),
    "time": ("follow-up period", "days"),
    "DEATH_EVENT": ("if the patient died during the follow-up period (target on the UCI page)", "boolean"),
}


def main() -> None:
    raw = SRC.read_bytes()
    df = pd.read_csv(SRC)

    columns = []
    for c in df.columns:
        s = df[c]
        binary = set(s.dropna().unique()) <= {0, 1}
        row = {
            "column": c,
            "meaning": DOC.get(c, ("undocumented", "undocumented"))[0],
            "unit": DOC.get(c, ("undocumented", "undocumented"))[1],
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "distinct": int(s.nunique()),
            "min": float(s.min()),
            "median": float(s.median()),
            "max": float(s.max()),
            "zeros": int((s == 0).sum()),
            "binary_0_1": bool(binary),
        }
        if binary:
            row["count_0"] = int((s == 0).sum())
            row["count_1"] = int((s == 1).sum())
        else:
            row["mean"] = float(s.mean())
            row["non_integer_values"] = int((s != s.round()).sum())
        columns.append(row)

    summary = {
        "file": SRC.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "rows_sorted_by_time": bool(df["time"].is_monotonic_increasing),
        "non_integer_age_values": sorted(df.loc[df["age"] != df["age"].round(), "age"].tolist()),
        "column_detail": columns,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "01_describe.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        f"# Describing pass: `{SRC.name}`",
        "",
        f"{summary['rows']} rows × {summary['columns']} columns; {summary['bytes']:,} bytes; SHA-256 `{summary['sha256']}`. Missing cells: {summary['missing_cells']}. Duplicate rows: {summary['duplicate_rows']}. Rows sorted by `time`: {summary['rows_sorted_by_time']}.",
        "",
        "| Column | Meaning (UCI) | Unit (UCI) | Type | Missing | Distinct | Min | Median | Max | Zeros | 0 / 1 counts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in columns:
        counts = f"{r['count_0']} / {r['count_1']}" if r["binary_0_1"] else "—"
        lines.append(f"| `{r['column']}` | {r['meaning']} | {r['unit']} | {r['dtype']} | {r['missing']} | {r['distinct']} | {r['min']:g} | {r['median']:g} | {r['max']:g} | {r['zeros']} | {counts} |")
    lines += ["", f"Non-integer values of `age`: {summary['non_integer_age_values']}."]
    (OUT / "01_describe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
