"""Sepsis, step 2: counts the patients a patient-level target would use, for candidate window lengths N.

Target under discussion: from the first N hours of the ICU stay (ICULOS <= N), predict whether SepsisLabel
switches on later in the stay. Counts only: no model, no relationship between inputs and outcome.
For each N and hospital it counts, in order:
  - patients with at least one kept hour in the window (records can start after ICU hour 1);
  - of those, patients whose label switches on within the window (label_onset_iculos <= N) -> excluded;
  - the remaining cohort, its positives (onset after N) and its share of positives;
  - in the cohort, patients whose record ends by hour N (no hour after the window), and patients with
    no vital or lab value at all in the window;
  - for the positives, when the label switches on (ICULOS quartiles).

Reads   Code/outputs/sepsis/private/hours.csv.gz, patients.csv.gz (from sepsis_03_build_table.py)
Writes  Code/outputs/sepsis/04_target_counts.json, 04_target_counts.md   (aggregates only)

Run:    cd Code && uv run python sepsis_04_target_counts.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
WINDOWS = [6, 12]
NOT_MEASURED = {"patient", "set", "ICULOS", "Age", "Gender", "Unit1", "Unit2", "HospAdmTime"}


def main() -> None:
    hours = pd.read_csv(OUT / "private" / "hours.csv.gz")
    patients = pd.read_csv(OUT / "private" / "patients.csv.gz").set_index("patient")
    measured = [c for c in hours.columns if c not in NOT_MEASURED]
    hours["any_measured"] = hours[measured].notna().any(axis=1)
    g = hours.groupby("patient")
    patients["first_iculos"] = g.ICULOS.min()
    patients["last_iculos"] = g.ICULOS.max()  # last kept hour; for septic patients, the hour before label onset

    out = {}
    for n in WINDOWS:
        win = hours[hours.ICULOS <= n].groupby("patient")
        p = patients.assign(in_window=win.size(), measured_in_window=win.any_measured.any())
        p["in_window"] = p.in_window.fillna(0).astype(int)
        res = {}
        for s in ("A", "B", "all"):
            q = p if s == "all" else p[p.set == s]
            has = q[q.in_window > 0]
            onset_in = has[has.label_onset_iculos <= n]
            cohort = has[~(has.label_onset_iculos <= n)]
            pos = cohort[cohort.septic == 1]
            res[s] = {
                "patients_total": len(q),
                "no_hour_in_window": int((q.in_window == 0).sum()),
                "no_hour_in_window_septic": int(((q.in_window == 0) & (q.septic == 1)).sum()),
                "with_hours_in_window": len(has),
                "excluded_onset_within_window": len(onset_in),
                "cohort": len(cohort),
                "cohort_positive": len(pos),
                "cohort_positive_pct": round(100 * len(pos) / len(cohort), 2),
                "cohort_record_ends_by_N": int((cohort.last_iculos <= n).sum()),
                "cohort_record_ends_by_N_positive": int(((cohort.last_iculos <= n) & (cohort.septic == 1)).sum()),
                "cohort_no_measurement_in_window": int((~cohort.measured_in_window.astype(bool)).sum()),
                "positive_onset_iculos_quartiles": [float(v) for v in pos.label_onset_iculos.quantile([0, .25, .5, .75, 1])],
                "positive_onset_within_24h_after_N": int((pos.label_onset_iculos <= n + 24).sum()),
                "positive_onset_within_48h_after_N": int((pos.label_onset_iculos <= n + 48).sum()),
            }
        out[f"N={n}"] = res

    (OUT / "04_target_counts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    text = "# Sepsis: patient counts for candidate windows (step 2)\n\n```\n" + json.dumps(out, indent=2) + "\n```\n"
    (OUT / "04_target_counts.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
