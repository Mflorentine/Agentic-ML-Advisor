"""Interim program for the Auto MPG analysis: mean absolute error on the test cars, from the saved predictions.

NOT YET APPROVED BY THE USER. No result from it may be used until the user has approved it.

What it does, in plain words: it reads the predictions for the 78 test cars that the approved final check saved,
and computes the average size of the miss for the recommended method and for the average guess, ignoring whether a
miss is an over- or an under-estimate. It does not read the test cars from the data file, and it fits nothing.

Run from Code/:  uv run python Auto_MPG/core_mae.py
Writes: outputs/Auto_MPG/core_mae.json
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "outputs" / "Auto_MPG"
PRED = OUT / "core_final_predictions.csv"
RES = OUT / "core_final.json"


def run():
    pred = pd.read_csv(PRED)
    actual = pred["actual_litres_per_100km"].to_numpy(dtype=float)
    model = pred["predicted_litres_per_100km"].to_numpy(dtype=float)
    base = pred["baseline_litres_per_100km"].to_numpy(dtype=float)
    mae_model = float(np.mean(np.abs(actual - model)))
    mae_base = float(np.mean(np.abs(actual - base)))
    final = json.loads(RES.read_text(encoding="utf-8"))
    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "step": "test-set mean absolute error, from the saved predictions",
        "code_version": f"sha256:{code_version}",
        "label": "interim program, not reviewed; NOT YET APPROVED BY THE USER",
        "predictions_file": str(PRED),
        "test_rows": int(len(pred)),
        "k_chosen": final["k_chosen"],
        "mean_absolute_error_nearest_cases": mae_model,
        "mean_absolute_error_average_guess": mae_base,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "core_mae.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("MAE nearest cases:", round(mae_model, 3), "| average guess:", round(mae_base, 3), "| test cars:", len(pred))
    print("written:", OUT / "core_mae.json")


if __name__ == "__main__":
    run()
