"""Sepsis, step 2: counts for the agreed target, and for the patients whose outcome is not fully observed.

Target agreed with the user (17 October 2026): from the first N = 6 hours of the ICU stay (ICULOS <= N),
predict whether SepsisLabel switches on within H = 48 hours after the window, i.e. label onset in (N, N + H].
Counts only: no model, no relationship between inputs and outcome.

The cohort is the one counted by sepsis_04_target_counts.py for N = 6: patients with at least one kept hour
in the window whose label has not switched on within it. Each patient's outcome is read from
label_onset_iculos (patients.csv.gz), never from the length of the kept record, because step 1 set aside
every row from label onset: a septic patient's kept record ends the hour before onset, not at discharge.

For each hospital it counts:
  - positives: label onset in (N, N + H];
  - negatives observed to the end of the period: never septic with a record reaching hour N + H, or septic
    with label onset after N + H (their kept record reaches onset - 1 >= N + H);
  - negatives NOT observed to the end of the period: never septic and record ending before hour N + H.
    For a never-septic patient the kept record is the whole record, so its last ICULOS is the ICU discharge
    (or the two-week cut). Their last hour is summarised, and the cohort size and positive share are given
    under both options (keep them as negatives, or exclude them);
  - a check that the positives whose kept record ends by hour N (label onset at N + 1) are counted as positives.

Reads   Code/outputs/sepsis/private/hours.csv.gz, patients.csv.gz (from sepsis_03_build_table.py)
Writes  Code/outputs/sepsis/05_horizon_counts.json, 05_horizon_counts.md   (aggregates only)

Run:    cd Code && uv run python sepsis_05_horizon_counts.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"
N = 6    # window: first N ICU hours (user, 17 October 2026)
H = 48   # horizon after the window (user, 17 October 2026)


def build_cohort() -> pd.DataFrame:
    """The step 2 cohort, one row per patient, with the outcome (`positive`) and the follow-up classes.

    Also used by sepsis_06_split.py, so the split is made on exactly the cohort counted here.
    """
    hours = pd.read_csv(OUT / "private" / "hours.csv.gz", usecols=["patient", "ICULOS"])
    patients = pd.read_csv(OUT / "private" / "patients.csv.gz").set_index("patient")
    g = hours.groupby("patient").ICULOS
    patients["last_iculos"] = g.max()
    patients["in_window"] = hours[hours.ICULOS <= N].groupby("patient").size()
    patients["in_window"] = patients.in_window.fillna(0).astype(int)

    has = patients[patients.in_window > 0]
    cohort = has[~(has.label_onset_iculos <= N)].copy()
    onset = cohort.label_onset_iculos
    cohort["positive"] = (cohort.septic == 1) & (onset > N) & (onset <= N + H)
    cohort["neg_full"] = ((cohort.septic == 0) & (cohort.last_iculos >= N + H)) | ((cohort.septic == 1) & (onset > N + H))
    cohort["neg_short"] = (cohort.septic == 0) & (cohort.last_iculos < N + H)
    assert (cohort[["positive", "neg_full", "neg_short"]].sum(axis=1) == 1).all()
    return cohort


def main() -> None:
    cohort = build_cohort()

    out = {"N": N, "H": H, "positive_if_label_onset_iculos_in": [N + 1, N + H]}
    for s in ("A", "B", "all"):
        c = cohort if s == "all" else cohort[cohort.set == s]
        pos, full, short = int(c.positive.sum()), int(c.neg_full.sum()), int(c.neg_short.sum())
        ends_by_n = c[c.last_iculos <= N]
        out[s] = {
            "cohort": len(c),
            "positive": pos,
            "negative_observed_to_end": full,
            "negative_observed_to_end_septic_later": int((c.neg_full & (c.septic == 1)).sum()),
            "negative_not_observed_to_end": short,
            "not_observed_last_iculos_quartiles": [float(v) for v in c[c.neg_short].last_iculos.quantile([0, .25, .5, .75, 1])],
            "not_observed_record_ends_within_24h_after_N": int((c.neg_short & (c.last_iculos <= N + 24)).sum()),
            "keep_as_negative": {"rows": len(c), "positive": pos, "positive_pct": round(100 * pos / len(c), 2)},
            "exclude": {"rows": pos + full, "positive": pos, "positive_pct": round(100 * pos / (pos + full), 2)},
            "kept_record_ends_by_N": len(ends_by_n),
            "kept_record_ends_by_N_counted_positive": int(ends_by_n.positive.sum()),
        }

    (OUT / "05_horizon_counts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    text = "# Sepsis: counts for the 6-hour window and 48-hour horizon (step 2)\n\n```\n" + json.dumps(out, indent=2) + "\n```\n"
    (OUT / "05_horizon_counts.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
