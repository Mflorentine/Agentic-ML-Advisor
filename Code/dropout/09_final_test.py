"""Step 4g: the single final evaluation of the recommended configuration on the locked test set.

Recommended (DR-26): Logistic + L2. Settings from the step 4f final tuning on all training rows (DR-25),
read from Code/outputs/dropout/08_recommendation.json: L2 strength and F2 threshold.
The model is refitted on all 3,539 training rows; the 885 test rows are scored once.
The baseline (most common training class: predict "not dropout") is evaluated on the same rows.
The test F2 is recomputed by a second route (counts from the confusion matrix) to check the first.

Reads   Attachments/Student Dropout/data.csv (never modified)
        Code/outputs/dropout/02_split.csv (split = test rows are read here, and only here)
        Code/outputs/dropout/07_cv_round2.csv (fold spread for the uncertainty)
        Code/outputs/dropout/08_recommendation.json (settings)
Uses    Code/dropout/cv.py (interim core, not reviewed)
Writes  Code/outputs/dropout/09_final_test.json, 09_final_test.md, 09_test_predictions.csv

Run     cd Code && uv run python dropout/09_final_test.py
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix, fbeta_score, precision_score, recall_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import cv  # noqa: E402

SRC = ROOT / "Attachments" / "Student Dropout" / "data.csv"
SPLIT = ROOT / "Code" / "outputs" / "dropout" / "02_split.csv"
OUT = ROOT / "Code" / "outputs" / "dropout"

rec = json.loads((OUT / "08_recommendation.json").read_text(encoding="utf-8"))
final = rec["final_tuning_all_training_rows"]
LAM = float(final["lambda"])
THR = float(final["threshold"])
DEGREE = int(final["degree"])
assert DEGREE == 1, "the recommended configuration is Logistic + L2 (no polynomial terms)"

df = pd.read_csv(SRC, sep=";", encoding="utf-8-sig")
df.columns = [c.strip() for c in df.columns]
split = pd.read_csv(SPLIT)
assert len(split) == len(df)
y_all = (df["Target"] == "Dropout").astype(int)
X_all = df.drop(columns=["Target"])
numeric = [c for c in X_all.columns if c not in cv.CATEGORICAL]

tr_mask = (split["split"] == "train").values
te_mask = (split["split"] == "test").values
assert tr_mask.sum() == 3539 and te_mask.sum() == 885

Xtr, ytr = X_all.loc[tr_mask], y_all.loc[tr_mask]
Xte, yte = X_all.loc[te_mask], y_all.loc[te_mask]

# Recommended configuration, refitted on all training rows
model = cv.build_model(numeric, DEGREE, LAM, n_fold_train=len(Xtr))
model.fit(Xtr, ytr)
proba = model.predict_proba(Xte)[:, 1]
pred = (proba >= THR).astype(int)

# Baseline on the same rows: most common training class
base = DummyClassifier(strategy="most_frequent").fit(Xtr, ytr)
pred_base = base.predict(Xte)

# Metrics (library route)
f2_model = float(fbeta_score(yte, pred, beta=2, zero_division=0))
f2_base = float(fbeta_score(yte, pred_base, beta=2, zero_division=0))
prec = float(precision_score(yte, pred, zero_division=0))
rec_ = float(recall_score(yte, pred, zero_division=0))
tn, fp, fn, tp = confusion_matrix(yte, pred, labels=[0, 1]).ravel()

# Independent route: F2 from the confusion counts, F2 = 5TP / (5TP + 4FN + FP)
f2_counts = 5 * tp / (5 * tp + 4 * fn + fp) if (5 * tp + 4 * fn + fp) > 0 else 0.0
assert abs(f2_counts - f2_model) < 1e-12, (f2_counts, f2_model)

# Flag-everyone reference on the same test rows: (1 + b^2) p / (b^2 p + 1), b = 2
p = float(yte.mean())
f2_flag_all = 5 * p / (4 * p + 1)

# Uncertainty: SD across the outer folds of Logistic + L2 (DR-26, method DR-19 / 4g)
r2 = pd.read_csv(OUT / "07_cv_round2.csv")
fold_sd = float(r2[r2.configuration == "Logistic + L2"]["F2_test"].std(ddof=1))
fold_mean = float(r2[r2.configuration == "Logistic + L2"]["F2_test"].mean())

criterion_met = f2_model > f2_flag_all
core_sha = hashlib.sha256((HERE / "cv.py").read_bytes()).hexdigest()

result = {
    "configuration": "Logistic + L2",
    "lambda": LAM,
    "threshold": THR,
    "n_train": int(tr_mask.sum()),
    "n_test": int(te_mask.sum()),
    "test_positives": int(yte.sum()),
    "test_positive_share": p,
    "F2_test_model": f2_model,
    "precision_test": prec,
    "recall_test": rec_,
    "confusion_matrix": {"TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp)},
    "F2_test_baseline": f2_base,
    "F2_test_flag_everyone_reference": f2_flag_all,
    "success_criterion_met": bool(criterion_met),
    "uncertainty_fold_SD_F2": fold_sd,
    "cv_fold_mean_F2": fold_mean,
    "core": "Code/dropout/cv.py (interim core, not reviewed)",
    "core_sha256": core_sha,
}
(OUT / "09_final_test.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

pd.DataFrame({"row_id": split.loc[te_mask, "row_id"].values, "y": yte.values,
              "proba": proba, "pred": pred, "pred_baseline": pred_base}).to_csv(
    OUT / "09_test_predictions.csv", index=False, lineterminator="\n")

lines = [
    "# Step 4g: final evaluation on the locked test set (single use)",
    "",
    "Generated by `Code/dropout/09_final_test.py` using `Code/dropout/cv.py` (interim core, not reviewed).",
    "",
    f"- Configuration: Logistic + L2; L2 strength {LAM:g}; F2 threshold {THR:.2f} (DR-25). Refitted on {int(tr_mask.sum()):,} training rows.",
    f"- Test rows: {int(te_mask.sum())}, of which {int(yte.sum())} Dropout ({p:.1%}).",
    f"- Core SHA-256: `{core_sha}`",
    "",
    "| Measure | Logistic + L2 (recommended) | Baseline (not dropout for all) | Flag-everyone reference |",
    "| --- | ---: | ---: | ---: |",
    f"| F2 on the test rows | {f2_model:.4f} | {f2_base:.4f} | {f2_flag_all:.4f} |",
    "",
    f"- Precision {prec:.4f}; recall {rec_:.4f}.",
    f"- Confusion matrix (rows: actual; columns: predicted): TN {tn}, FP {fp}; FN {fn}, TP {tp}.",
    f"- Uncertainty: SD across the ten outer folds of Logistic + L2 F2 = {fold_sd:.4f} (mean {fold_mean:.4f}).",
    f"- Success criterion (F2 above flagging every student on the same rows): {'met' if criterion_met else 'not met'}.",
    "",
]
(OUT / "09_final_test.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(json.dumps(result, indent=2))
