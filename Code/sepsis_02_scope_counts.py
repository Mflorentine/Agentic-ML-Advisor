"""Sepsis, step 1, decisions: counts what the user's step 1 decisions would change, before anything is applied.

Nothing is cleaned or dropped here, and no derived table is written. The script counts:
  1. the rows and patients that remain once every row from the hour SepsisLabel first becomes 1 is set aside (leakage decision);
  2. the FiO2 values by band, to check its unit before a cleaning rule is fixed;
  3. how many values each candidate cleaning rule would set to missing, on the rows that remain.

Reads   Attachments/sepsis-physionet-2019/training_setA/*.psv, training_setB/*.psv (never modified)
Writes  Code/outputs/sepsis/02_scope_counts.json  and  Code/outputs/sepsis/02_scope_counts.md  (aggregates only)

Run:    cd Code && uv run python sepsis_02_scope_counts.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "sepsis-physionet-2019"
OUT = ROOT / "Code" / "outputs" / "sepsis"

# Candidate rules [I]: a value outside (LOW, HIGH) is physiologically impossible and would be set to missing.
# None means no bound on that side. Several thresholds are counted for columns where the cut is a judgement.
CANDIDATES = {
    "FiO2": [(0.21, 1.0)],
    "Temp": [(25, 45), (30, 43)],
    "Potassium": [(None, 10), (None, 15)],
    "Hgb": [(None, 25)],
    "Hct": [(None, 75)],
    "HCO3": [(1, None)],
    "BaseExcess": [(None, 40)],
    "pH": [(6.5, 8.0)],
}
FIO2_BANDS = [(-1e9, 0), (0, 0.21), (0.21, 1.0), (1.0, 21), (21, 100), (100, 1e9)]


def load() -> pd.DataFrame:
    frames = []
    for s in ("A", "B"):
        for f in sorted((SRC / f"training_set{s}").glob("*.psv")):
            d = pd.read_csv(f, sep="|")
            d["patient"], d["set"] = f.stem, s
            frames.append(d)
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    df = load()
    kept = df[df.SepsisLabel == 0]  # SepsisLabel never returns from 1 to 0 (01_describe.json), so this removes every row from onset
    septic = set(df.loc[df.SepsisLabel == 1, "patient"])
    left = kept.groupby("patient").size()
    out = {"leakage_rows": {
        "rows_before": len(df), "rows_set_aside": int((df.SepsisLabel == 1).sum()), "rows_after": len(kept),
        "patients_before": int(df.patient.nunique()), "patients_after": int(left.size),
        "patients_with_no_rows_left": int(df.patient.nunique() - left.size),
        "septic_patients_before": len(septic), "septic_patients_with_rows_left": int(left.index.isin(list(septic)).sum()),
        "septic_rows_left_median": float(left[left.index.isin(list(septic))].median()),
        "by_set": {s: {"rows_after": int((kept.set == s).sum()), "patients_after": int(kept[kept.set == s].patient.nunique()),
                       "septic_patients_with_rows_left": int(kept[(kept.set == s) & kept.patient.isin(septic)].patient.nunique())}
                   for s in ("A", "B")}}}

    f = kept.FiO2.dropna()
    out["fio2_bands_rows_kept"] = {f"[{lo}, {hi})": int(((f >= lo) & (f < hi)).sum()) for lo, hi in FIO2_BANDS}
    out["fio2_exact_1"] = int((f == 1.0).sum())
    out["fio2_values_above_1"] = sorted(f[f > 1].unique().tolist())[:50]

    rules = []
    for col, cuts in CANDIDATES.items():
        x = kept[col].dropna()
        for lo, hi in cuts:
            bad = pd.Series(False, index=x.index)
            if lo is not None:
                bad |= x < lo
            if hi is not None:
                bad |= x > hi
            rules.append({"column": col, "low": lo, "high": hi, "values_present": len(x), "would_set_missing": int(bad.sum()),
                          "by_set": {s: int(bad[kept.loc[x.index, "set"] == s].sum()) for s in ("A", "B")},
                          "patients_affected": int(kept.loc[bad[bad].index, "patient"].nunique()),
                          "examples": sorted(x[bad].unique().tolist())[:15]})
    out["candidate_rules_rows_kept"] = rules

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "02_scope_counts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    lines = ["# Sepsis: counts for the step 1 decisions", "", "```", json.dumps(out, indent=2), "```"]
    (OUT / "02_scope_counts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
