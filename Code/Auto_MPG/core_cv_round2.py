"""Interim core for the Auto MPG analysis, step 4d: cross-validation, round 2 (interim core, not reviewed).

NOT YET APPROVED BY THE USER. Do not run for results until the user has approved this script.

Cross-validates the remaining kept configurations on the same ten outer parts as round 1 (core_cv.py,
approved 2026-11-17): Exponential + L2, kNN and Tree (ML Guide.md sections 9, 14, 16).
- Outer parts: the same ten parts as round 1 (imported from core_cv.py, unchanged).
- Settings are chosen inside each outer training part by five further parts grouped by car name,
  using the same procedure with seed 2026, and the chosen settings are then fitted on the whole outer
  training part and tested on the held-back outer part.
- Exponential + L2: gamma regression with a logarithmic link and a penalty strength (sklearn alpha) from
  1e-4 to 1e4 in powers of ten; inputs scaled inside each training part (REQ-3).
- kNN: k from {1, 3, 5, 7, 9, 15, 21, 31, 51}; inputs scaled inside each training part (REQ-2).
- Tree: maximum depth from {1, 2, 3, 4, 5, 6, 8, 10, 15, 20} and minimum leaf size from {1, 5, 10, 20}.
- Measure: root mean squared error. Margin = baseline fold error minus model fold error (positive is better);
  the spread is the standard deviation of the ten fold margins.
- Training cars only: the test cars are never read here.

Run from Code/:  uv run python Auto_MPG/core_cv_round2.py
Writes: outputs/Auto_MPG/core_cv_round2.json
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression  # noqa: F401  (kept for parity with round 1)
from sklearn.linear_model import GammaRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402  (unchanged)
import core_cv  # noqa: E402  (round 1 script, approved 2026-11-17, unchanged; used for features, outer_parts, rmse)

CONVERSION = 235.2
SEED = 2026
OUT = CODE / "outputs" / "Auto_MPG" / "core_cv_round2.json"

LAMBDAS = [10.0 ** p for p in range(-4, 5)]
KS = [1, 3, 5, 7, 9, 15, 21, 31, 51]
DEPTHS = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]
LEAVES = [1, 5, 10, 20]


def make_model(name, setting):
    if name == "Exponential + L2":
        return make_pipeline(StandardScaler(), GammaRegressor(alpha=setting, max_iter=10000))
    if name == "kNN":
        return make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=setting))
    if name == "Tree":
        depth, leaf = setting
        return DecisionTreeRegressor(max_depth=depth, min_samples_leaf=leaf, random_state=SEED)
    raise ValueError(name)


def settings_for(name):
    if name == "Exponential + L2":
        return [("alpha", a) for a in LAMBDAS]
    if name == "kNN":
        return [("k", k) for k in KS]
    if name == "Tree":
        return [("depth_leaf", (d, m)) for d in DEPTHS for m in LEAVES]
    raise ValueError(name)


def value_of(setting):
    return setting[1]


def tune(name, X, y, train_rows):
    """Choose the setting with the lowest mean inner RMSE, using five inner parts grouped by car name."""
    inner = core_cv.outer_parts(train_rows)
    best = None
    table = []
    for setting in settings_for(name):
        errs = []
        for k in range(5):
            tr = inner != k
            te = inner == k
            m = make_model(name, value_of(setting))
            m.fit(X[tr], y[tr])
            errs.append(core_cv.rmse(y[te], m.predict(X[te])))
        mean_err = float(np.mean(errs))
        table.append({"setting": str(value_of(setting)), "inner_mean_RMSE": mean_err})
        if best is None or mean_err < best[1]:
            best = (value_of(setting), mean_err)
    return best[0], table


def run():
    props = json.loads((HERE / "props.json").read_text(encoding="utf-8"))
    train = core.load_data()
    y = (CONVERSION / train["mpg"]).to_numpy(dtype=float)
    X = core_cv.features(train)
    part = core_cv.outer_parts(train)
    names = ["Exponential + L2", "kNN", "Tree"]

    folds = []
    chosen = {n: [] for n in names}
    for k in range(core_cv.N_OUTER):
        tr = part != k
        te = part == k
        row = {"fold": k, "baseline": {"E_val": core_cv.rmse(y[te], np.full(te.sum(), y[tr].mean()))}}
        for name in names:
            s, table = tune(name, X[tr], y[tr], train[tr].reset_index(drop=True))
            chosen[name].append(str(s))
            m = make_model(name, s)
            m.fit(X[tr], y[tr])
            row[name] = {"setting": str(s), "E_train": core_cv.rmse(y[tr], m.predict(X[tr])),
                         "E_val": core_cv.rmse(y[te], m.predict(X[te])), "inner_table": table}
        folds.append(row)

    summary = {}
    for name in ["baseline"] + names:
        vals = np.array([f[name]["E_val"] for f in folds])
        summary[name] = {"CV mean RMSE": float(vals.mean()), "SD across folds": float(vals.std(ddof=1))}
        if name != "baseline":
            summary[name]["E_train mean"] = float(np.mean([f[name]["E_train"] for f in folds]))
            margins = np.array([f["baseline"]["E_val"] - f[name]["E_val"] for f in folds])
            summary[name]["margin over baseline (mean)"] = float(margins.mean())
            summary[name]["margin spread (SD of fold margins)"] = float(margins.std(ddof=1))
            summary[name]["margin over spread"] = float(margins.mean() / margins.std(ddof=1))
            summary[name]["most common setting"] = Counter(chosen[name]).most_common(1)[0][0]
            summary[name]["settings chosen by fold"] = chosen[name]

    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "step": "4d cross-validation round 2",
        "code_version": f"sha256:{code_version}",
        "round_1_script": core_cv.__file__,
        "label": "interim core, not reviewed; NOT YET APPROVED BY THE USER",
        "seed": SEED,
        "outer_parts": core_cv.N_OUTER,
        "part_sizes": [int((part == k).sum()) for k in range(core_cv.N_OUTER)],
        "measure": "root mean squared error, litres per 100 km",
        "property_values_used": props,
        "grids": {"alpha": LAMBDAS, "k": KS, "depth": DEPTHS, "leaf": LEAVES},
        "folds": folds,
        "summary": summary,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    for name in names:
        s = summary[name]
        print(f"{name}: CV mean RMSE {s['CV mean RMSE']:.3f}, margin/spread {s['margin over spread']:.2f}, most common setting {s['most common setting']}")
    print("code version: sha256", code_version[:16], "...")
    print("written:", OUT)


if __name__ == "__main__":
    sys.exit(run())
