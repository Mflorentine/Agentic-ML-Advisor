"""Interim program for the Auto MPG analysis, step 4g: the final check on the test cars (interim program, not reviewed).

NOT YET APPROVED BY THE USER. The test cars must not be read by any program until the user has approved this one.

What it does, in plain words: it picks the number of neighbours for the nearest-cases method that gives the lowest
average error across the ten training parts (the same parts as before), refits the method on all 314 training cars,
and checks it once on the 78 held-back test cars. It checks the average guess on the same cars. It also reports the
spread of the error across the ten training parts, which gives the uncertainty of the test result (a test-set
estimate varies less the larger the test set, SML pp. 71–73; the spread is our approximation).
It writes its predictions to a file and recomputes the test error from them with a second, separate calculation.

Measure: root mean squared error, litres per 100 km. Seed 2026. Test cars are read only in the final step.

Run from Code/:  uv run python Auto_MPG/core_final.py
Writes: outputs/Auto_MPG/core_final.json and outputs/Auto_MPG/core_final_predictions.csv
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402  (unchanged)
import core_cv  # noqa: E402  (unchanged)

CONVERSION = 235.2
OUT_DIR = CODE / "outputs" / "Auto_MPG"
OUT = OUT_DIR / "core_final.json"
PRED = OUT_DIR / "core_final_predictions.csv"
KS = [1, 3, 5, 7, 9, 15, 21, 31, 51]


def load_all():
    """All 392 used cars with the split label; the test cars are read here, in the final step only."""
    from pathlib import Path as _P
    src = _P(core.SRC)
    rows = []
    for file_line, line in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        num_part, _, name = line.partition("\t")
        rows.append([file_line] + num_part.split() + [name.strip().strip('"')])
    cols = ["file_line", "mpg", "cylinders", "displacement", "horsepower", "weight",
            "acceleration", "model_year", "origin", "car_name"]
    df = pd.DataFrame(rows, columns=cols)
    for c in cols[1:-1]:
        df[c] = pd.to_numeric(df[c].replace("?", pd.NA))
    df = df.dropna(subset=["horsepower"]).reset_index(drop=True)
    split = pd.read_csv(core.SPLIT)
    assert (split["file_line"].values == df["file_line"].values).all()
    df["set"] = split["set"].values
    return df


def make_knn(k):
    return make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=k))


def rmse(y, yhat):
    return float(np.sqrt(np.mean((np.asarray(y) - np.asarray(yhat)) ** 2)))


def run():
    props = json.loads((HERE / "props.json").read_text(encoding="utf-8"))
    df = load_all()
    train = df[df["set"] == "train"].reset_index(drop=True)
    test = df[df["set"] == "test"].reset_index(drop=True)
    assert len(train) == 314 and len(test) == 78

    y_tr = (CONVERSION / train["mpg"]).to_numpy(dtype=float)
    y_te = (CONVERSION / test["mpg"]).to_numpy(dtype=float)
    X_tr = core_cv.features(train)
    X_te = core_cv.features(test)

    # Choose k: lowest average error across the ten training parts (same parts as the checks)
    part = core_cv.outer_parts(train)
    avg_by_k = {}
    for k in KS:
        errs = []
        for p in range(core_cv.N_OUTER):
            tr = part != p
            te = part == p
            m = make_knn(k).fit(X_tr[tr], y_tr[tr])
            errs.append(rmse(y_tr[te], m.predict(X_tr[te])))
        avg_by_k[k] = float(np.mean(errs))
    k_star = min(avg_by_k, key=lambda k: avg_by_k[k])
    part_spread = float(np.std([rmse(y_tr[part == p], make_knn(k_star).fit(X_tr[part != p], y_tr[part != p]).predict(X_tr[part == p])) for p in range(core_cv.N_OUTER)], ddof=1))

    # Refit on all 314 training cars; check once on the 78 test cars; baseline on the same cars
    model = make_knn(k_star).fit(X_tr, y_tr)
    pred_test = model.predict(X_te)
    baseline_pred = np.full(len(y_te), y_tr.mean())
    test_rmse = rmse(y_te, pred_test)
    test_rmse_baseline = rmse(y_te, baseline_pred)

    # Second, separate calculation of the same test error from the saved predictions
    saved = pd.DataFrame({"file_line": test["file_line"], "car_name": test["car_name"],
                          "actual_litres_per_100km": y_te, "predicted_litres_per_100km": pred_test,
                          "baseline_litres_per_100km": baseline_pred})
    saved.to_csv(PRED, index=False)
    re = pd.read_csv(PRED)
    recomputed = float(np.sqrt(((re["actual_litres_per_100km"] - re["predicted_litres_per_100km"]) ** 2).mean()))
    recomputed_base = float(np.sqrt(((re["actual_litres_per_100km"] - re["baseline_litres_per_100km"]) ** 2).mean()))

    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "step": "4g final evaluation (test cars, once)",
        "code_version": f"sha256:{code_version}",
        "label": "interim program, not reviewed; NOT YET APPROVED BY THE USER",
        "property_values_used": props,
        "k_chosen": k_star,
        "average_error_by_k_across_parts": avg_by_k,
        "spread_across_parts_of_chosen_k": part_spread,
        "training_rows": int(len(train)),
        "test_rows": int(len(test)),
        "test_rmse_nearest_cases": test_rmse,
        "test_rmse_average_guess": test_rmse_baseline,
        "test_rmse_recomputed_from_saved_predictions": recomputed,
        "test_rmse_average_guess_recomputed": recomputed_base,
        "predictions_file": str(PRED),
        "seed": 2026,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("chosen k:", k_star, "| test error:", round(test_rmse, 3), "| average guess on test:", round(test_rmse_baseline, 3), "| spread across parts:", round(part_spread, 3))
    print("written:", OUT)


if __name__ == "__main__":
    sys.exit(run())
