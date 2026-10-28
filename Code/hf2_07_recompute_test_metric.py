"""Heart Failure rerun, step 4g: recompute the test result independently of the core's summary.

Reads   Code/outputs/hf2/core_test_predictions.csv  (row, y, p, predicted, written by the core's `final`)
        Attachments/heart_failure_clinical_records_dataset.csv  (true outcome of each test row, read by row number)
        Code/outputs/hf2/split.json   (to confirm the rows are exactly the 60 test rows)
        Code/outputs/hf2/core_final.json  (the core's numbers, for comparison only)
Writes  Code/outputs/hf2/recompute_test_metric.txt

Average precision is computed from its definition, without scikit-learn: sort by p descending; at each distinct
score, precision P and recall R of flagging everything with p >= that score; AP = sum over those points of
(R_n - R_(n-1)) * P_n. Confusion counts, precision, recall and F2 at the core's threshold (y = 1 if p > r) by
counting.

Run:    cd Code && uv run python hf2_07_recompute_test_metric.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "hf2"


def average_precision(y: np.ndarray, p: np.ndarray) -> float:
    ap, prev_recall, pos = 0.0, 0.0, y.sum()
    for s in np.unique(p)[::-1]:
        flagged = p >= s
        tp = int((flagged & (y == 1)).sum())
        precision, recall = tp / int(flagged.sum()), tp / pos
        ap += (recall - prev_recall) * precision
        prev_recall = recall
    return float(ap)


def main() -> None:
    pred = pd.read_csv(OUT / "core_test_predictions.csv", float_precision="round_trip")
    split = json.loads((OUT / "split.json").read_text(encoding="utf-8"))
    core = json.loads((OUT / "core_final.json").read_text(encoding="utf-8"))
    src = pd.read_csv(ROOT / "Attachments" / "heart_failure_clinical_records_dataset.csv")
    assert sorted(pred["row"]) == sorted(split["test_idx"]), "prediction rows are not the test rows"
    y = src.loc[pred["row"], "DEATH_EVENT"].to_numpy()
    assert (y == pred["y"].to_numpy()).all(), "stored outcomes differ from the source file"
    p, r = pred["p"].to_numpy(), core["threshold"]
    flag = (p > r).astype(int)
    tp, fp = int(((flag == 1) & (y == 1)).sum()), int(((flag == 1) & (y == 0)).sum())
    fn, tn = int(((flag == 0) & (y == 1)).sum()), int(((flag == 0) & (y == 0)).sum())
    prec, rec = tp / (tp + fp), tp / (tp + fn)
    f2 = 5 * prec * rec / (4 * prec + rec)
    ap, rate = average_precision(y, p), float(y.mean())
    lines = [
        f"test rows: {len(y)}; deaths: {int(y.sum())}; share of deaths: {rate:.4f}   (core: {core['test_positive_rate']:.4f})",
        f"PR-AUC (average precision, by definition): {ap:.6f}   (core: {core['test_pr_auc']:.6f})",
        f"baseline (flag nobody) PR-AUC = share of deaths: {rate:.4f}   (core: {core['baseline_test_pr_auc']:.4f})",
        f"threshold r = {r}: tn {tn}, fp {fp}, fn {fn}, tp {tp}   (core: {core['confusion_test']})",
        f"precision {prec:.4f}, recall {rec:.4f}, F2 {f2:.4f}   (core: {core['at_threshold']['precision']:.4f}, "
        f"{core['at_threshold']['recall']:.4f}, {core['at_threshold']['fbeta']:.4f})",
        f"success: {ap:.4f} - {core['uncertainty_fold_sd_pr_auc']:.4f} = {ap - core['uncertainty_fold_sd_pr_auc']:.4f} > {rate:.4f}: "
        f"{ap - core['uncertainty_fold_sd_pr_auc'] > rate}",
        f"agrees with core: {abs(ap - core['test_pr_auc']) < 1e-9 and {'tn': tn, 'fp': fp, 'fn': fn, 'tp': tp} == core['confusion_test']}",
    ]
    (OUT / "recompute_test_metric.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
