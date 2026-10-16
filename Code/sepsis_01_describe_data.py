"""Sepsis, step 1, describing pass: what is in the source files, with no judgement about what it means.

Reads   Attachments/sepsis-physionet-2019/training_setA/*.psv, training_setB/*.psv (never modified)
        Attachments/sepsis-physionet-2019/SHA256SUMS_training_setA.txt, SHA256SUMS_training_setB.txt
Writes  Code/outputs/sepsis/01_describe.json  and  Code/outputs/sepsis/01_describe.md
        (aggregates only; no patient-level rows are written, because the data is ODbL and kept out of git)

Run:    cd Code && uv run python sepsis_01_describe_data.py
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Attachments" / "sepsis-physionet-2019"
OUT = ROOT / "Code" / "outputs" / "sepsis"
SETS = ["A", "B"]

# Units as documented on the PhysioNet Challenge 2019 page (version 1.0.0), not inferred from the names.
UNIT = {
    "HR": "beats per minute", "O2Sat": "%", "Temp": "deg C", "SBP": "mm Hg", "MAP": "mm Hg", "DBP": "mm Hg",
    "Resp": "breaths per minute", "EtCO2": "mm Hg", "BaseExcess": "mmol/L", "HCO3": "mmol/L", "FiO2": "%",
    "pH": "none", "PaCO2": "mm Hg", "SaO2": "%", "AST": "IU/L", "BUN": "mg/dL", "Alkalinephos": "IU/L",
    "Calcium": "mg/dL", "Chloride": "mmol/L", "Creatinine": "mg/dL", "Bilirubin_direct": "mg/dL",
    "Glucose": "mg/dL", "Lactate": "mg/dL", "Magnesium": "mmol/dL", "Phosphate": "mg/dL",
    "Potassium": "mmol/L", "Bilirubin_total": "mg/dL", "TroponinI": "ng/mL", "Hct": "%", "Hgb": "g/dL",
    "PTT": "seconds", "WBC": "count*10^3/uL", "Fibrinogen": "mg/dL", "Platelets": "count*10^3/uL",
    "Age": "years (100 for 90 or above)", "Gender": "0 female, 1 male", "Unit1": "MICU (identifier)",
    "Unit2": "SICU (identifier)", "HospAdmTime": "hours, hospital admit to ICU admit",
    "ICULOS": "hours since ICU admit", "SepsisLabel": "0 or 1",
}
GROUP = {**{c: "vital" for c in ["HR", "O2Sat", "Temp", "SBP", "MAP", "DBP", "Resp", "EtCO2"]},
         **{c: "demographic" for c in ["Age", "Gender", "Unit1", "Unit2", "HospAdmTime", "ICULOS"]},
         "SepsisLabel": "outcome"}


def verify_checksums(s: str) -> dict:
    listing = SRC / f"SHA256SUMS_training_set{s}.txt"
    expected = dict(reversed(line.split("  ", 1)) for line in listing.read_text().splitlines() if line)
    bad = [p for p, h in expected.items() if hashlib.sha256((SRC / p).read_bytes()).hexdigest() != h]
    on_disk = {f"training_set{s}/{f.name}" for f in (SRC / f"training_set{s}").glob("*.psv")}
    return {"listed": len(expected), "on_disk": len(on_disk), "mismatched": len(bad),
            "missing_from_list": len(on_disk - expected.keys()), "missing_from_disk": len(expected.keys() - on_disk),
            "list_sha256": hashlib.sha256(listing.read_bytes()).hexdigest()}


def load(s: str) -> pd.DataFrame:
    frames = []
    for f in sorted((SRC / f"training_set{s}").glob("*.psv")):
        d = pd.read_csv(f, sep="|")
        d.insert(0, "patient", f.stem)
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    df.insert(1, "set", s)
    return df


def describe_columns(df: pd.DataFrame, cols: list) -> list:
    by_patient = df.groupby("patient")
    ever = by_patient[cols].apply(lambda g: g.notna().any())
    rows = []
    for c in cols:
        x = df[c]
        r = {"column": c, "group": GROUP.get(c, "lab"), "unit": UNIT[c],
             "rows_present_pct": round(100 * x.notna().mean(), 2),
             "patients_ever_present_pct": round(100 * ever[c].mean(), 2),
             "distinct": int(x.nunique())}
        if x.notna().any():
            q = x.quantile([0, 0.01, 0.5, 0.99, 1]).tolist()
            r.update({"min": q[0], "p01": q[1], "median": q[2], "p99": q[3], "max": q[4],
                      "non_integer_pct": round(100 * (x.dropna() != x.dropna().round()).mean(), 2)})
        rows.append(r)
    return rows


def main() -> None:
    summary = {"checksums": {s: verify_checksums(s) for s in SETS}}
    df = pd.concat([load(s) for s in SETS], ignore_index=True)
    cols = [c for c in df.columns if c not in ("patient", "set")]
    summary["header_columns"] = cols
    summary["rows"] = {"all": len(df), **{s: int((df.set == s).sum()) for s in SETS}}
    summary["patients"] = {"all": int(df.patient.nunique()), **{s: int(df[df.set == s].patient.nunique()) for s in SETS}}
    summary["duplicate_rows_within_patient"] = int(df.duplicated(subset=["patient"] + cols).sum())

    g = df.groupby("patient")
    per = pd.DataFrame({
        "set": g.set.first(), "hours": g.size(), "iculos_first": g.ICULOS.first(), "iculos_last": g.ICULOS.last(),
        "iculos_steps_ok": g.ICULOS.apply(lambda s: bool((s.diff().dropna() == 1).all())),
        "septic": g.SepsisLabel.max(), "label_first": g.SepsisLabel.first(),
        "label_monotone": g.SepsisLabel.apply(lambda s: bool(s.is_monotonic_increasing)),
        "first_label1_iculos": g.apply(lambda d: d.loc[d.SepsisLabel == 1, "ICULOS"].min()),
        "rows_label1": g.SepsisLabel.sum(),
        "age_constant": g.Age.nunique() == 1, "gender_constant": g.Gender.nunique() == 1,
        "hospadm_constant": g.HospAdmTime.nunique(dropna=False) == 1,
        "gender": g.Gender.first(), "age": g.Age.first(),
        "unit1": g.Unit1.max(), "unit2": g.Unit2.max(), "unit_missing": g.Unit1.apply(lambda s: s.isna().all()),
    })

    def stay(p):
        return {"patients": len(p), "hours_min": int(p.hours.min()), "hours_median": float(p.hours.median()),
                "hours_max": int(p.hours.max()), "iculos_first_not_1": int((p.iculos_first != 1).sum()),
                "iculos_first_max": int(p.iculos_first.max()), "iculos_last_max": int(p.iculos_last.max()),
                "iculos_with_gaps": int((~p.iculos_steps_ok).sum())}
    summary["stays"] = {"all": stay(per), **{s: stay(per[per.set == s]) for s in SETS}}

    def label(p, d):
        sep = p[p.septic == 1]
        return {"patients_septic": int(len(sep)), "patients_septic_pct": round(100 * len(sep) / len(p), 2),
                "rows_label1": int(d.SepsisLabel.sum()), "rows_label1_pct": round(100 * d.SepsisLabel.mean(), 2),
                "septic_label_not_monotone": int((~sep.label_monotone).sum()),
                "septic_label1_from_first_row": int((sep.label_first == 1).sum()),
                "septic_first_label1_iculos_median": float(sep.first_label1_iculos.median()),
                "septic_first_label1_iculos_max": float(sep.first_label1_iculos.max()),
                "septic_rows_label1_median": float(sep.rows_label1.median()),
                "septic_rows_label1_max": int(sep.rows_label1.max())}
    summary["label"] = {"all": label(per, df), **{s: label(per[per.set == s], df[df.set == s]) for s in SETS}}

    summary["per_patient_constancy"] = {
        "age_varies": int((~per.age_constant).sum()), "gender_varies": int((~per.gender_constant).sum()),
        "hospadmtime_varies": int((~per.hospadm_constant).sum())}
    summary["demographics_per_patient"] = {s: {
        "gender_0": int((p.gender == 0).sum()), "gender_1": int((p.gender == 1).sum()),
        "gender_missing": int(p.gender.isna().sum()), "age_100": int((p.age == 100).sum()),
        "age_median": float(p.age.median()), "unit1_ever": int((p.unit1 == 1).sum()),
        "unit2_ever": int((p.unit2 == 1).sum()), "unit_all_missing": int(p.unit_missing.sum()),
        "both_units": int(((p.unit1 == 1) & (p.unit2 == 1)).sum())}
        for s, p in [("all", per)] + [(s, per[per.set == s]) for s in SETS]}
    u = df[["Unit1", "Unit2"]].dropna()
    summary["unit1_plus_unit2_values_in_rows"] = {str(k): int(v) for k, v in (u.Unit1 + u.Unit2).value_counts().items()}

    summary["columns"] = {"all": describe_columns(df, cols), **{s: describe_columns(df[df.set == s], cols) for s in SETS}}
    summary["rows_with_no_vital_or_lab"] = int(df[[c for c in cols if GROUP.get(c, "lab") in ("vital", "lab")]].isna().all(axis=1).sum())

    # Encoding counts for P3/P4: Gender, Unit1, Unit2 are categorical; everything else numeric.
    inputs = [c for c in cols if c != "SepsisLabel"]
    summary["inputs"] = {"count": len(inputs), "categorical": ["Gender", "Unit1", "Unit2"],
                         "note": "Gender, Unit1, Unit2 are already 0/1 columns, so one-hot encoding adds none"}

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "01_describe.json").write_text(json.dumps(summary, indent=2, default=float), encoding="utf-8")

    lines = ["# Sepsis: describing pass (step 1)", "",
             f"Rows: {summary['rows']}  ", f"Patients: {summary['patients']}  ",
             f"Duplicate rows within a patient: {summary['duplicate_rows_within_patient']}  ",
             f"Rows with no vital or lab value: {summary['rows_with_no_vital_or_lab']}", "",
             "## Checksums", "", "```", json.dumps(summary["checksums"], indent=2), "```", "",
             "## Stays", "", "```", json.dumps(summary["stays"], indent=2), "```", "",
             "## Label", "", "```", json.dumps(summary["label"], indent=2), "```", "",
             "## Per-patient constancy and demographics", "", "```",
             json.dumps({"constancy": summary["per_patient_constancy"], "demographics": summary["demographics_per_patient"],
                         "unit1_plus_unit2": summary["unit1_plus_unit2_values_in_rows"]}, indent=2), "```", "",
             "## Columns (both sets)", "",
             "| Column | Group | Unit | Rows present % | Patients ever % (A / B) | Min | P1 | Median | P99 | Max |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    ca, cb = ({r["column"]: r for r in summary["columns"][s]} for s in SETS)
    for r in summary["columns"]["all"]:
        c = r["column"]
        f = lambda k: "" if k not in r else f"{r[k]:.4g}"
        lines.append(f"| `{c}` | {r['group']} | {r['unit']} | {r['rows_present_pct']} | {r['patients_ever_present_pct']} ({ca[c]['patients_ever_present_pct']} / {cb[c]['patients_ever_present_pct']}) | {f('min')} | {f('p01')} | {f('median')} | {f('p99')} | {f('max')} |")
    (OUT / "01_describe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
