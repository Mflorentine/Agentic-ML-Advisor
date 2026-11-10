"""Interim core, step 4f: learning curve (C3), final tuning on all training data, and the recommendation (section 19).
Interim core, not reviewed. Uses cv.py (interim core, not reviewed) for the model and the inner search.

1. Learning curve (section 16): for the leading configuration only, Logistic + L2, training fractions 10 % to 100 %
   of each outer training set (stratified subsample, seed 2026). Each fraction is fitted with the L2 strength and
   threshold chosen in that outer fold's round-1 CV, and the validation error (misclassification rate, Property 10
   balanced) is measured on the outer test fold.
2. C3 (section 17): limited if the validation error at 100 % is lower than at 80 % by at least 0.5 × its fold SD.
3. Final tuning (section 16, DR-19): the L2 strength and the F2 threshold are chosen by 5-fold CV on all training
   rows (cv.inner_search), for use in the single test-set refit at 4g. The test set is not read here.
4. Recommendation (section 19) and confidence (section 17): eligible = C2 clear and every must-have met; candidates =
   the eligible configuration with the best CV mean plus eligible configurations within 0.5 × spread of it; choose the
   fewest add-ons, then the higher prior score, then the better CV mean. Confidence: High / Medium / Low by C1, C2, C3.

Writes  (by the runner 08_recommendation.py): learning curve table, final hyperparameters, the §19 trace.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, train_test_split

import cv

FRACTIONS = [round(0.1 * i, 1) for i in range(1, 11)]   # 0.1 ... 1.0


def learning_curve(X: pd.DataFrame, y: pd.Series, numeric: list, round1: pd.DataFrame) -> pd.DataFrame:
    """Validation error (misclassification) by training fraction, per outer fold, for Logistic + L2."""
    outer = StratifiedKFold(n_splits=cv.OUTER_K, shuffle=True, random_state=cv.SEED)
    l2 = round1[round1.configuration == "Logistic + L2"].sort_values("fold").reset_index(drop=True)
    rows = []
    for k, (tr, te) in enumerate(outer.split(X, y), start=1):
        lam = float(l2.loc[k - 1, "lambda"])
        thr = float(l2.loc[k - 1, "threshold"])
        Xtr, ytr, Xte, yte = X.iloc[tr], y.iloc[tr], X.iloc[te], y.iloc[te]
        for f in FRACTIONS:
            if f >= 1.0:
                Xs, ys = Xtr, ytr
            else:
                Xs, _, ys, _ = train_test_split(Xtr, ytr, train_size=f, stratify=ytr, random_state=cv.SEED)
            m = cv.build_model(numeric, 1, lam, n_fold_train=len(Xs))
            m.fit(Xs, ys)
            pred = (m.predict_proba(Xte)[:, 1] >= thr).astype(int)
            rows.append({"fold": k, "fraction": f, "n_fit": len(Xs), "lambda": lam, "threshold": thr,
                         "E_val": float(np.mean(pred != yte.values))})
    return pd.DataFrame(rows)


def c3(curve: pd.DataFrame) -> dict:
    """Limited if E_val(100 %) is lower than E_val(80 %) by at least 0.5 × the fold SD of E_val(100 %)."""
    e100 = curve[curve.fraction == 1.0].sort_values("fold")["E_val"].values
    e80 = curve[curve.fraction == 0.8].sort_values("fold")["E_val"].values
    drop = float(np.mean(e80 - e100))            # positive if the error falls from 80 % to 100 %
    sd100 = float(np.std(e100, ddof=1))
    level = "limited" if drop >= 0.5 * sd100 else "adequate"
    return {"E_val_80_mean": float(e80.mean()), "E_val_100_mean": float(e100.mean()),
            "drop_80_to_100": drop, "fold_SD_at_100": sd100, "threshold": 0.5 * sd100, "C3": level}


def final_tuning(X: pd.DataFrame, y: pd.Series, numeric: list) -> dict:
    """L2 strength and F2 threshold for the test refit, chosen by 5-fold CV on all training rows."""
    return cv.inner_search(X, y, numeric, [1])["chosen"]


def recommend(round_summary: dict, c3_level: str, prior_scores: dict, add_ons: dict) -> dict:
    """Section 19, on the two admissible configurations. round_summary: name -> {F2_mean, F2_sd, fold_diff_vs_leader...}.

    prior_scores: name -> prior score; add_ons: name -> number of add-ons (0 for Logistic + L2, 1 for + poly).
    """
    names = list(round_summary)
    best = max(names, key=lambda n: round_summary[n]["F2_mean"])
    eligible = [n for n in names if round_summary[n]["C2"] == "clear"]
    cands = [best] + [n for n in eligible if n != best and round_summary[n]["margin_to_best_sd_ratio"] < 0.5]
    cands = [n for n in cands if n in eligible]
    chosen = sorted(cands, key=lambda n: (add_ons[n], -prior_scores[n], -round_summary[n]["F2_mean"]))[0]
    c1 = round_summary[chosen]["C1"]
    c2 = round_summary[chosen]["C2"]
    if c1 == "none" or c2 != "clear":
        level = "Low"
    elif c1 == "clear" and c2 == "clear" and c3_level == "adequate":
        level = "High"
    else:
        level = "Medium"
    return {"eligible": eligible, "best_CV_mean": best, "candidates": cands, "chosen": chosen,
            "C1": c1, "C2": c2, "C3": c3_level, "confidence": level}
