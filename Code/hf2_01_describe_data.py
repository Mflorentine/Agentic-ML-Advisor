"""Heart Failure rerun, step 1, describing pass: what is in the source file, with no judgement about what it means.

Reads   Attachments/heart_failure_clinical_records_dataset.csv (never modified)
Writes  Code/outputs/hf2/01_describe.json  and  Code/outputs/hf2/01_describe.md

Written fresh for the rerun; it does not read the earlier analysis's scripts or outputs.
Meanings and units are those of the UCI page's variable table (dataset 519, API fetched 28 October 2026),
with the measurement ranges of Chicco and Jurman (2020), Table 1, for comparison.

Run:    cd Code && uv run python hf2_01_describe_data.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv"
OUT = ROOT / "Code" / "outputs" / "hf2"
EXPECTED_SHA256 = "9c73cea7468ff5d517801ec050fe9993da5912fce4b56f296f8df3b38dd75912"   # Attachments/SOURCE.md
TARGET = "DEATH_EVENT"

# UCI variable table: (description, units as given, UCI type); paper Table 1 range in the last field.
DOC = {
    "age": ("age of the patient", "years", "Integer", "[40, ..., 95]"),
    "anaemia": ("decrease of red blood cells or hemoglobin", "none (boolean)", "Binary", "0, 1"),
    "creatinine_phosphokinase": ("level of the CPK enzyme in the blood", "mcg/L", "Integer", "[23, ..., 7861]"),
    "diabetes": ("if the patient has diabetes", "none (boolean)", "Binary", "0, 1"),
    "ejection_fraction": ("percentage of blood leaving the heart at each contraction", "%", "Integer", "[14, ..., 80]"),
    "high_blood_pressure": ("if the patient has hypertension", "none (boolean)", "Binary", "0, 1"),
    "platelets": ("platelets in the blood", "kiloplatelets/mL", "Continuous", "[25.01, ..., 850.00]"),
    "serum_creatinine": ("level of serum creatinine in the blood", "mg/dL", "Continuous", "[0.50, ..., 9.40]"),
    "serum_sodium": ("level of serum sodium in the blood", "mEq/L", "Integer", "[114, ..., 148]"),
    "sex": ("woman or man", "none (binary)", "Binary", "0, 1"),
    "smoking": ("if the patient smokes or not", "none (boolean)", "Binary", "0, 1"),
    "time": ("follow-up period", "days", "Integer", "[4, ..., 285]"),
    "DEATH_EVENT": ("if the patient died during the follow-up period (UCI role: Target)", "none (boolean)", "Binary", "0, 1"),
}


def main() -> None:
    raw = SRC.read_bytes()
    df = pd.read_csv(SRC)
    cols = []
    for c in df.columns:
        s = df[c]
        binary = set(s.unique()) <= {0, 1}
        r = {"column": c, "meaning": DOC[c][0], "unit": DOC[c][1], "uci_type": DOC[c][2], "paper_range": DOC[c][3],
             "dtype": str(s.dtype), "missing": int(s.isna().sum()), "distinct": int(s.nunique()),
             "min": float(s.min()), "p01": float(s.quantile(0.01)), "median": float(s.median()),
             "p99": float(s.quantile(0.99)), "max": float(s.max()), "zeros": int((s == 0).sum()),
             "non_integer_values": int((s != s.round()).sum()), "binary_0_1": bool(binary)}
        if binary:
            r["count_0"], r["count_1"] = int((s == 0).sum()), int((s == 1).sum())
        cols.append(r)
    y = df[TARGET]
    inputs = [c for c in df.columns if c != TARGET]
    binary_inputs = [c for c in inputs if set(df[c].unique()) <= {0, 1}]
    by_class_time = {str(k): {"min": float(g.min()), "median": float(g.median()), "max": float(g.max())}
                     for k, g in df.groupby(TARGET)["time"]}
    summary = {
        "file": SRC.name, "sha256": hashlib.sha256(raw).hexdigest(),
        "sha256_matches_SOURCE_md": hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256,
        "bytes": len(raw), "crlf_line_endings": b"\r\n" in raw, "ascii_only": all(b < 128 for b in raw),
        "rows": int(df.shape[0]), "columns": int(df.shape[1]), "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_input_rows": int(df.duplicated(subset=inputs).sum()),
        "rows_sorted_by_time": bool(df["time"].is_monotonic_increasing),
        "target_counts": {str(k): int(v) for k, v in y.value_counts().sort_index().items()},
        "target_share_1": float(y.mean()),
        "n_inputs_excluding_target": len(inputs), "binary_inputs": binary_inputs,
        "non_integer_age_values": sorted(df.loc[df["age"] != df["age"].round(), "age"].tolist()),
        "time_by_target": by_class_time,
        "column_detail": cols,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "01_describe.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        f"# Describing pass: `{SRC.name}` (Heart Failure rerun)", "",
        f"{summary['rows']} rows × {summary['columns']} columns; {summary['bytes']:,} bytes; SHA-256 `{summary['sha256']}` "
        f"(matches SOURCE.md: {summary['sha256_matches_SOURCE_md']}); CRLF: {summary['crlf_line_endings']}; ASCII only: "
        f"{summary['ascii_only']}. Missing cells: {summary['missing_cells']}. Duplicate rows: {summary['duplicate_rows']}; "
        f"rows with identical inputs: {summary['duplicate_input_rows']}. Rows sorted by `time`: {summary['rows_sorted_by_time']}.",
        "",
        f"`{TARGET}` counts: " + ", ".join(f"{k}: {v}" for k, v in summary["target_counts"].items())
        + f" (share of 1: {summary['target_share_1']:.4f}).",
        "",
        "`time` by `DEATH_EVENT`: " + "; ".join(f"{k}: min {v['min']:g}, median {v['median']:g}, max {v['max']:g}"
                                             for k, v in by_class_time.items()) + ".",
        "",
        "| Column | Meaning (UCI) | Unit (UCI) | UCI type | Range (paper) | dtype | Missing | Distinct | Min | 1st pct | Median | 99th pct | Max | Zeros | Non-integer | 0 / 1 counts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in cols:
        counts = f"{r['count_0']} / {r['count_1']}" if r["binary_0_1"] else "—"
        lines.append(f"| `{r['column']}` | {r['meaning']} | {r['unit']} | {r['uci_type']} | {r['paper_range']} | {r['dtype']} | "
                     f"{r['missing']} | {r['distinct']} | {r['min']:g} | {r['p01']:g} | {r['median']:g} | {r['p99']:g} | "
                     f"{r['max']:g} | {r['zeros']} | {r['non_integer_values']} | {counts} |")
    lines += ["", f"Non-integer values of `age`: {summary['non_integer_age_values']}."]
    (OUT / "01_describe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
