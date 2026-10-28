"""Mobile Price, step 4g: recompute the test result independently of the core's summary.

Reads   Code/outputs/mobile/core_test_predictions.csv  (row, y, predicted, baseline, written by the core's `final`)
        Attachments/Mobile Price/train.csv               (the true band of each test row, read directly by row number)
        Code/outputs/mobile/split.json                   (to confirm the rows are exactly the 400 test rows)
        Code/outputs/mobile/core_final.json              (the core's numbers, for comparison only)
Writes  Code/outputs/mobile/recompute_test_metric.txt

Uses plain counting (no scikit-learn), so it is a second route to the same figures.

Run:    cd Code && uv run python mobile_06_recompute_test_metric.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "mobile"


def main() -> None:
    pred = pd.read_csv(OUT / "core_test_predictions.csv")
    split = json.loads((OUT / "split.json").read_text(encoding="utf-8"))
    core = json.loads((OUT / "core_final.json").read_text(encoding="utf-8"))
    src = pd.read_csv(ROOT / "Attachments" / "Mobile Price" / "train.csv")

    assert sorted(pred["row"]) == sorted(split["test_idx"]), "prediction rows are not the test rows"
    truth = src.loc[pred["row"], "price_range"].to_numpy()
    assert (truth == pred["y"].to_numpy()).all(), "stored true bands differ from the source file"

    n = len(pred)
    correct = int((pred["predicted"].to_numpy() == truth).sum())
    base_correct = int((pred["baseline"].to_numpy() == truth).sum())
    cm = [[int(((truth == t) & (pred["predicted"].to_numpy() == p)).sum()) for p in range(4)] for t in range(4)]
    off = [abs(int(a) - int(b)) for a, b in zip(truth, pred["predicted"])]
    lines = [
        f"test rows: {n}; per band: {[int((truth == b).sum()) for b in range(4)]}",
        f"accuracy: {correct}/{n} = {correct / n:.4f}   (core: {core['test_accuracy']:.4f})",
        f"baseline accuracy: {base_correct}/{n} = {base_correct / n:.4f}   (core: {core['baseline_test_accuracy']:.4f})",
        f"confusion (rows true 0-3, columns predicted 0-3): {cm}   (core: {core['confusion_test']})",
        f"misses by distance: 1 band {off.count(1)}, 2 bands {off.count(2)}, 3 bands {off.count(3)}",
        f"accuracy - fold SD ({core['uncertainty_fold_sd_accuracy']:.4f}) = {correct / n - core['uncertainty_fold_sd_accuracy']:.4f} > baseline {base_correct / n:.4f}: "
        f"{correct / n - core['uncertainty_fold_sd_accuracy'] > base_correct / n}",
        f"agrees with core: {abs(correct / n - core['test_accuracy']) < 1e-12 and cm == core['confusion_test'] and abs(base_correct / n - core['baseline_test_accuracy']) < 1e-12}",
    ]
    (OUT / "recompute_test_metric.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
