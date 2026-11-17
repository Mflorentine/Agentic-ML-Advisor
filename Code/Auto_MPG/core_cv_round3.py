"""Interim program for the Auto MPG analysis, diagnosis pass 2 (interim program, not reviewed).

NOT YET APPROVED BY THE USER. No result from it may be used until the user has approved it.

What it does, in plain words: it checks a straight-line model with curved terms added (the degree of
the curve, 2 or 3, is chosen inside each training part). It uses the same ten groups of training cars as
the earlier checks, and tests on the group held back.

Settings: outer parts as in the earlier checks (imported unchanged from core_cv.py); inner parts of five
groups inside each outer training part, seed 2026; inputs scaled using only the training part; no penalty.
Measure: root mean squared error. Margin = baseline fold error minus model fold error (positive is better).
Training cars only: the test cars are never read here.

Run from Code/:  uv run python Auto_MPG/core_cv_round3.py
Writes: outputs/Auto_MPG/core_cv_round3.json
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402  (unchanged)
import core_cv  # noqa: E402  (unchanged; outer parts, inputs, error measure)

CONVERSION = 235.2
SEED = 2026
DEGREES = [2, 3]
OUT = CODE / "outputs" / "Auto_MPG" / "core_cv_round3.json"


def poly_features(train, degree):
    """The eight input columns, with powers 2 to degree of each numeric input (powers of each input separately)."""
    base = core_cv.features(train)
    extra = []
    for j in range(len(core.NUMERIC_INPUTS)):
        x = base[:, j]
        for p in range(2, degree + 1):
            extra.append(x ** p)
    return np.column_stack([base] + extra)


def make_model(degree):
    return make_pipeline(StandardScaler(), LinearRegression())


def tune(X_fn, y, train_rows):
    inner = core_cv.outer_parts(train_rows)
    best, best_err, table = None, None, []
    for d in DEGREES:
        Xd = X_fn(train_rows, d)
        errs = []
        for k in range(5):
            tr = inner != k
            te = inner == k
            m = make_model(d)
            m.fit(Xd[tr], y[tr])
            errs.append(core_cv.rmse(y[te], m.predict(Xd[te])))
        mean_err = float(np.mean(errs))
        table.append({"degree": d, "inner_mean_RMSE": mean_err})
        if best_err is None or mean_err < best_err:
            best, best_err = d, mean_err
    return best, table


def run():
    props = json.loads((HERE / "props.json").read_text(encoding="utf-8"))
    train = core.load_data()
    y = (CONVERSION / train["mpg"]).to_numpy(dtype=float)
    part = core_cv.outer_parts(train)

    folds = []
    chosen = []
    for k in range(core_cv.N_OUTER):
        tr = part != k
        te = part == k
        train_tr = train[tr].reset_index(drop=True)
        d, table = tune(poly_features, y[tr], train_tr)
        chosen.append(d)
        Xd = poly_features(train, d)
        m = make_model(d)
        m.fit(Xd[tr], y[tr])
        folds.append({
            "fold": k,
            "baseline": {"E_val": core_cv.rmse(y[te], np.full(te.sum(), y[tr].mean()))},
            "Linear + poly": {"degree": d, "E_train": core_cv.rmse(y[tr], m.predict(Xd[tr])),
                              "E_val": core_cv.rmse(y[te], m.predict(Xd[te])), "inner_table": table},
        })

    name = "Linear + poly"
    vals = np.array([f[name]["E_val"] for f in folds])
    base = np.array([f["baseline"]["E_val"] for f in folds])
    margins = base - vals
    summary = {name: {
        "CV mean RMSE": float(vals.mean()),
        "SD across folds": float(vals.std(ddof=1)),
        "E_train mean": float(np.mean([f[name]["E_train"] for f in folds])),
        "margin over baseline (mean)": float(margins.mean()),
        "margin spread (SD of fold margins)": float(margins.std(ddof=1)),
        "margin over spread": float(margins.mean() / margins.std(ddof=1)),
        "most common setting": f"degree {Counter(chosen).most_common(1)[0][0]}",
        "settings chosen by fold": [f"degree {d}" for d in chosen],
    }}

    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "step": "4e diagnosis pass 2 (cross-validation of Linear + poly)",
        "code_version": f"sha256:{code_version}",
        "label": "interim program, not reviewed; NOT YET APPROVED BY THE USER",
        "seed": SEED,
        "outer_parts": core_cv.N_OUTER,
        "part_sizes": [int((part == k).sum()) for k in range(core_cv.N_OUTER)],
        "measure": "root mean squared error, litres per 100 km",
        "property_values_used": props,
        "folds": folds,
        "summary": summary,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    s = summary[name]
    print(f"{name}: CV mean RMSE {s['CV mean RMSE']:.3f}, margin/spread {s['margin over spread']:.2f}, most common {s['most common setting']}")
    print("code version: sha256", code_version[:16], "...")
    print("written:", OUT)


if __name__ == "__main__":
    sys.exit(run())
