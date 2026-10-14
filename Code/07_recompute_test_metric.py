"""Recompute the step 4g test metrics from the saved predictions, independently of core.py.

Reads   Code/outputs/core_test_predictions.csv  (row, y, p_death, predicted)
        Code/outputs/split.json                  (to check the rows are exactly the test rows)
Writes  Code/outputs/recompute_test_metric.txt
F2 is computed by hand from the confusion counts, not with scikit-learn's fbeta_score.

Run:    cd Code && uv run python 07_recompute_test_metric.py
"""
import json
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent / "outputs"
BETA = 2.0
THRESHOLD = 0.2   # DR-19


def main() -> None:
    pred = pd.read_csv(OUT / "core_test_predictions.csv")
    split = json.loads((OUT / "split.json").read_text(encoding="utf-8"))
    assert sorted(pred["row"]) == sorted(split["test_idx"]), "rows are not the test rows"
    assert ((pred["p_death"] > THRESHOLD).astype(int) == pred["predicted"]).all(), "threshold mismatch"
    tp = int(((pred.y == 1) & (pred.predicted == 1)).sum())
    fp = int(((pred.y == 0) & (pred.predicted == 1)).sum())
    fn = int(((pred.y == 1) & (pred.predicted == 0)).sum())
    tn = int(((pred.y == 0) & (pred.predicted == 0)).sum())
    precision, recall = tp / (tp + fp), tp / (tp + fn)
    f2 = (1 + BETA ** 2) * precision * recall / (BETA ** 2 * precision + recall)
    share = pred.y.mean()
    f2_all = (1 + BETA ** 2) * share / (BETA ** 2 * share + 1)
    lines = [f"n = {len(pred)}, positives = {int(pred.y.sum())}",
             f"tn {tn}  fp {fp}  fn {fn}  tp {tp}",
             f"precision {precision:.4f}  recall {recall:.4f}  F2 {f2:.4f}",
             f"flag-everyone F2 on the test rows {f2_all:.4f}"]
    (OUT / "recompute_test_metric.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
