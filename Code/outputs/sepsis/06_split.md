# Sepsis: train/test split (step 2)

```
{
  "window_hours_N": 6,
  "horizon_hours_H": 48,
  "seed": 2026,
  "test_fraction": 0.2,
  "shuffled": true,
  "stratified_by": "hospital (set) x outcome (y)",
  "unit": "patient (one row each)",
  "cohort_patients": 39088,
  "counts": {
    "train": {
      "patients": 31270,
      "positive": 984,
      "positive_pct": 3.15,
      "A_patients": 15578,
      "B_patients": 15692,
      "A_positive": 624,
      "B_positive": 360,
      "A_positive_pct": 4.01,
      "B_positive_pct": 2.29
    },
    "test": {
      "patients": 7818,
      "positive": 246,
      "positive_pct": 3.15,
      "A_patients": 3895,
      "B_patients": 3923,
      "A_positive": 156,
      "B_positive": 90,
      "A_positive_pct": 4.01,
      "B_positive_pct": 2.29
    }
  },
  "sha256": {
    "private/cohort.csv.gz": "55dce9ca19702d3829c8ba36a164d2df126e709e3e5f5bd7b3dbffebfc889b4c"
  }
}
```
