"""Sepsis, step 2: the train/test split. The test set is locked from here on.

One row per patient (the cohort of sepsis_05_horizon_counts.py: N = 6, H = 48), so splitting by row is
splitting by patient. Shuffled, and stratified by outcome and hospital together (four strata: A/B x 0/1),
so the test set keeps the training set's positive share in each hospital. Agreed with the user,
17-18 October 2026 (DR-08).

After this script, no step 3 or step 4 code may read the test patients until the single final
evaluation (step 4g). Later scripts take the training patients from cohort.csv.gz (split == "train").

Reads   Code/outputs/sepsis/private/hours.csv.gz, patients.csv.gz (via sepsis_05_horizon_counts.build_cohort)
Writes  Code/outputs/sepsis/private/cohort.csv.gz   (patient, set, y, split; patient-level, not in git)
        Code/outputs/sepsis/06_split.json, 06_split.md   (seed, counts by split, hospital and outcome; aggregates only)

Run:    cd Code && uv run python sepsis_06_split.py
"""
import json
from pathlib import Path

from sklearn.model_selection import train_test_split

from sepsis_03_build_table import write_gz
from sepsis_05_horizon_counts import H, N, build_cohort

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"

SEED = 2026          # agreed with the user (step 2, DR-08)
TEST_FRACTION = 0.2  # agreed with the user (step 2, DR-08)


def main() -> None:
    cohort = build_cohort().reset_index()[["patient", "set", "positive"]].rename(columns={"positive": "y"})
    cohort["y"] = cohort.y.astype(int)
    cohort = cohort.sort_values("patient").reset_index(drop=True)  # fixed input order, so the seed alone fixes the split
    strata = cohort.set + "_" + cohort.y.astype(str)
    train_idx, test_idx = train_test_split(
        cohort.index.to_numpy(), test_size=TEST_FRACTION, shuffle=True, stratify=strata, random_state=SEED
    )
    cohort["split"] = "train"
    cohort.loc[test_idx, "split"] = "test"

    counts = {}
    for part in ("train", "test"):
        c = cohort[cohort.split == part]
        counts[part] = {
            "patients": len(c),
            "positive": int(c.y.sum()),
            "positive_pct": round(100 * c.y.mean(), 2),
            **{f"{s}_patients": int((c.set == s).sum()) for s in ("A", "B")},
            **{f"{s}_positive": int(c[c.set == s].y.sum()) for s in ("A", "B")},
            **{f"{s}_positive_pct": round(100 * c[c.set == s].y.mean(), 2) for s in ("A", "B")},
        }
    out = {
        "window_hours_N": N,
        "horizon_hours_H": H,
        "seed": SEED,
        "test_fraction": TEST_FRACTION,
        "shuffled": True,
        "stratified_by": "hospital (set) x outcome (y)",
        "unit": "patient (one row each)",
        "cohort_patients": len(cohort),
        "counts": counts,
        "sha256": {"private/cohort.csv.gz": write_gz(cohort, OUT / "private" / "cohort.csv.gz")},
    }
    (OUT / "06_split.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    text = "# Sepsis: train/test split (step 2)\n\n```\n" + json.dumps(out, indent=2) + "\n```\n"
    (OUT / "06_split.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
