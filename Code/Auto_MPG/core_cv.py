"""Interim core for the Auto MPG analysis, step 4c: cross-validation, round 1 (interim core, not reviewed).

Cross-validates the baseline, Exponential and Linear on the same ten outer parts (ML Guide.md section 16):
- outer parts: ten parts grouped by car name (rows with one name stay together), made by shuffling the
  names with seed 2026 and filling the parts so that their sizes stay near equal; the same parts for every model;
- baseline: the mean of the training outputs (SEQ-1);
- Linear: ordinary least squares on the eight input columns, scaling fitted inside each training part;
- Exponential: gamma regression with a log link and no penalty (the exponential model, section 9),
  scaling fitted inside each training part; no settings to tune, so no inner parts are needed.
Measure: root mean squared error (DR-07). Margin = baseline fold error minus model fold error, so
positive means better than the baseline; the spread is the standard deviation of those ten margins
(section 16, not the standard error).
Training cars only: the test cars are never read here.

Run from Code/:  uv run python Auto_MPG/core_cv.py
Writes: outputs/Auto_MPG/core_cv_round1.json
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import GammaRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402  (load_data: training rows, unchanged)

CONVERSION = 235.2
SEED = 2026
N_OUTER = 10
OUT = CODE / "outputs" / "Auto_MPG" / "core_cv_round1.json"


def features(train):
    """The eight input columns as recorded (DR-19, DR-20, DR-21): six numbers and origin codes 2 and 3 as yes-or-no."""
    X = [train[c].to_numpy(dtype=float) for c in core.NUMERIC_INPUTS]
    origin = train["origin"].astype(int).to_numpy()
    X += [(origin == 2).astype(float), (origin == 3).astype(float)]
    return np.column_stack(X)


def outer_parts(train):
    """Ten parts, grouped by car name, shuffled with seed 2026, sizes kept near equal."""
    rng = np.random.default_rng(SEED)
    names = np.array(sorted(train["car_name"].unique()), dtype=object)
    names = names[rng.permutation(len(names))]
    sizes = train["car_name"].value_counts()
    part_of_name = {}
    part_rows = np.zeros(N_OUTER, dtype=int)
    for name in names:
        k = int(np.argmin(part_rows))          # the part with fewest rows so far
        part_of_name[name] = k
        part_rows[k] += sizes[name]
    return np.array([part_of_name[n] for n in train["car_name"]])


def rmse(y, yhat):
    return float(np.sqrt(np.mean((y - yhat) ** 2)))


def run():
    props = json.loads((HERE / "props.json").read_text(encoding="utf-8"))
    train = core.load_data()
    y = (CONVERSION / train["mpg"]).to_numpy(dtype=float)
    X = features(train)
    part = outer_parts(train)

    models = {
        "Linear": lambda: make_pipeline(StandardScaler(), LinearRegression()),
        "Exponential": lambda: make_pipeline(StandardScaler(), GammaRegressor(alpha=0.0, max_iter=10000)),
    }

    folds = []
    for k in range(N_OUTER):
        tr = part != k
        te = part == k
        row = {"fold": k, "training_rows": int(tr.sum()), "held_out_rows": int(te.sum())}
        row["baseline"] = {"E_train": rmse(y[tr], np.full(tr.sum(), y[tr].mean())),
                           "E_val": rmse(y[te], np.full(te.sum(), y[tr].mean()))}
        for name, make in models.items():
            m = make()
            m.fit(X[tr], y[tr])
            row[name] = {"E_train": rmse(y[tr], m.predict(X[tr])), "E_val": rmse(y[te], m.predict(X[te]))}
        folds.append(row)

    summary = {}
    for name in ["baseline", "Linear", "Exponential"]:
        vals = np.array([f[name]["E_val"] for f in folds])
        summary[name] = {"CV mean RMSE": float(vals.mean()), "SD across folds": float(vals.std(ddof=1)),
                         "E_train mean": float(np.mean([f[name]["E_train"] for f in folds]))}
    for name in ["Linear", "Exponential"]:
        margins = np.array([f["baseline"]["E_val"] - f[name]["E_val"] for f in folds])
        summary[name]["margin over baseline (mean)"] = float(margins.mean())
        summary[name]["margin spread (SD of fold margins)"] = float(margins.std(ddof=1))
        summary[name]["margin over spread"] = float(margins.mean() / margins.std(ddof=1))

    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "step": "4c cross-validation round 1",
        "code_version": f"sha256:{code_version}",
        "label": "interim core, not reviewed",
        "seed": SEED,
        "outer_parts": N_OUTER,
        "measure": "root mean squared error, litres per 100 km",
        "property_values_used": props,
        "part_sizes": [int((part == k).sum()) for k in range(N_OUTER)],
        "folds": folds,
        "summary": summary,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print("part sizes:", result["part_sizes"])
    for name in ["baseline", "Linear", "Exponential"]:
        s = summary[name]
        print(f"{name}: CV mean RMSE {s['CV mean RMSE']:.3f}, SD across folds {s['SD across folds']:.3f}, E_train mean {s['E_train mean']:.3f}")
    for name in ["Linear", "Exponential"]:
        s = summary[name]
        print(f"{name} margin over baseline {s['margin over baseline (mean)']:.3f}, spread {s['margin spread (SD of fold margins)']:.3f}, margin/spread {s['margin over spread']:.2f}")
    print("code version: sha256", code_version[:16], "...")
    print("written:", OUT)


if __name__ == "__main__":
    sys.exit(run())
