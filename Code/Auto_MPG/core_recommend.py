"""Interim program for the Auto MPG analysis, step 4f: recommendation and confidence (interim program, not reviewed).

NOT YET APPROVED BY THE USER. No result from it may be used until the user has approved it.

What it does, in plain words: it reads the checking results already approved (rounds 1 and 2 and the
straight-line check of the diagnosis), chooses the recommended method by the workflow's rule
(ML Guide.md section 19), and rates how sure that choice is (section 17). It also runs one new
check for that rule: a learning curve for the recommended method, which shows whether more training
cars would still help. It does not read the test cars.

Measures: root mean squared error. Margins are per checking part: the first method's error minus the
second's, so positive means the first is better. A spread is the standard deviation of the ten part margins.
The learning curve uses 10 %, 20 % ... 100 % of each training part, chosen at random with seed 2026.

Run from Code/:  uv run python Auto_MPG/core_recommend.py
Writes: outputs/Auto_MPG/core_recommend.json
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402  (unchanged)
import core_cv  # noqa: E402  (unchanged)

CONVERSION = 235.2
SEED = 2026
OUT_DIR = CODE / "outputs" / "Auto_MPG"
OUT = OUT_DIR / "core_recommend.json"
FRACTIONS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def load_results():
    r1 = json.loads((OUT_DIR / "core_cv_round1.json").read_text(encoding="utf-8"))
    r2 = json.loads((OUT_DIR / "core_cv_round2.json").read_text(encoding="utf-8"))
    r3 = json.loads((OUT_DIR / "core_cv_round3.json").read_text(encoding="utf-8"))
    errs = {"baseline": [f["baseline"]["E_val"] for f in r1["folds"]]}
    errs["Linear"] = [f["Linear"]["E_val"] for f in r1["folds"]]
    errs["Exponential"] = [f["Exponential"]["E_val"] for f in r1["folds"]]
    errs["Exponential + L2"] = [f["Exponential + L2"]["E_val"] for f in r2["folds"]]
    errs["kNN"] = [f["kNN"]["E_val"] for f in r2["folds"]]
    errs["Tree"] = [f["Tree"]["E_val"] for f in r2["folds"]]
    errs["Linear + poly"] = [f["Linear + poly"]["E_val"] for f in r3["folds"]]
    add_ons = {"baseline": 0, "Linear": 0, "Exponential": 0, "Exponential + L2": 1, "kNN": 0, "Tree": 0, "Linear + poly": 1}
    settings = {"kNN": [f["kNN"]["setting"] for f in r2["folds"]]}
    return errs, add_ons, settings, r2


def margin(a, b):
    """Per part: error of b minus error of a (positive = a better). Returns mean and SD (ten parts)."""
    d = np.array(b) - np.array(a)
    return float(d.mean()), float(d.std(ddof=1))


def learning_curve(train, y, part, k_by_fold):
    """C3 check for the recommended method (kNN): held-back error at each training fraction, per part."""
    rng = np.random.default_rng(SEED)
    X = core_cv.features(train)
    curves = []
    for p in range(core_cv.N_OUTER):
        tr_idx = np.where(part != p)[0]
        te_idx = np.where(part == p)[0]
        order = rng.permutation(len(tr_idx))
        row = []
        for frac in FRACTIONS:
            n = int(round(frac * len(tr_idx)))
            sub = tr_idx[order[:n]]
            m = make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=int(k_by_fold[p])))
            m.fit(X[sub], y[sub])
            row.append(core_cv.rmse(y[te_idx], m.predict(X[te_idx])))
        curves.append(row)
    return np.array(curves)  # parts x fractions


def run():
    props = json.loads((HERE / "props.json").read_text(encoding="utf-8"))
    errs, add_ons, settings, r2 = load_results()
    means = {k: float(np.mean(v)) for k, v in errs.items()}
    spreads = {k: float(np.std(v, ddof=1)) for k, v in errs.items()}

    # C2 for every configuration: margin over the baseline against the spread of that margin
    c2 = {}
    for k in errs:
        if k == "baseline":
            continue
        d = np.array(errs["baseline"]) - np.array(errs[k])  # baseline minus model: positive = model better
        m, s = float(d.mean()), float(d.std(ddof=1))
        c2[k] = {"margin": m, "spread": s, "clear": bool(m >= s)}

    # Section 19, step 1: eligible = C2 clear (no must-haves are set)
    eligible = [k for k in errs if k != "baseline" and c2[k]["clear"]]
    # Section 19, step 2: candidates = best CV mean among eligible, plus eligible with margin to it "none"
    best = min(eligible, key=lambda k: means[k])
    candidates = [best]
    margins_to_best = {}
    for k in eligible:
        if k == best:
            continue
        m, s = margin(errs[best], errs[k])  # positive = best is better
        margins_to_best[k] = {"margin": m, "spread": s, "ratio": (m / s) if s else None}
        if m < 0.5 * s:
            candidates.append(k)
    # Section 19, step 3: fewest add-ons, then prior score (kNN and Tree both 0), then CV mean
    prior_score = {"kNN": 0, "Tree": 0, "Linear": -1, "Linear + poly": -1, "Exponential": 1, "Exponential + L2": 1}
    chosen = min(candidates, key=lambda k: (add_ons[k], -prior_score[k], means[k]))

    # C1: margin of the chosen method over the runner-up (best other eligible)
    others = [k for k in eligible if k != chosen]
    runner = min(others, key=lambda k: means[k]) if others else None
    if runner:
        m, s = margin(errs[chosen], errs[runner])
        ratio = m / s if s else float("inf")
        c1 = "clear" if ratio >= 1 else ("moderate" if ratio >= 0.5 else "none")
    else:
        m = s = ratio = None
        c1 = "none"

    # C3: learning curve for the chosen method (kNN); limited if still falling at 100 % versus 80 %
    train = core.load_data()
    y = (CONVERSION / train["mpg"]).to_numpy(dtype=float)
    part = core_cv.outer_parts(train)
    k_by_fold = [int(v) for v in settings["kNN"]]
    lc = learning_curve(train, y, part, k_by_fold) if chosen == "kNN" else None
    if lc is not None:
        e80 = lc[:, FRACTIONS.index(0.8)].mean()
        e100 = lc[:, FRACTIONS.index(1.0)].mean()
        fold_sd = spreads[chosen]
        c3 = "limited" if (e80 - e100) >= 0.5 * fold_sd else "adequate"
        lc_summary = {"mean at 80 %": float(e80), "mean at 100 %": float(e100), "fold SD of the method": float(fold_sd),
                      "drop from 80 % to 100 %": float(e80 - e100), "curve (parts by fractions)": lc.round(4).tolist()}
    else:
        c3, lc_summary = "not computed", None

    # Level (section 17)
    c2_chosen = c2[chosen]["clear"]
    if c1 == "clear" and c2_chosen and c3 == "adequate":
        level = "High"
    elif c1 == "none" or not c2_chosen:
        level = "Low"
    else:
        level = "Medium"

    # Prior agreement (section 17): the prior's first method and top two
    prior_first = ["Exponential"]
    prior_top_two = ["Exponential", "Exponential + L2"]
    agreement = "agree" if chosen in prior_first else ("partial" if chosen in prior_top_two else "disagree")

    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        "step": "4f recommendation and selection confidence",
        "code_version": f"sha256:{code_version}",
        "label": "interim program, not reviewed; NOT YET APPROVED BY THE USER",
        "property_values_used": props,
        "cv_mean_RMSE": means,
        "cv_spread_RMSE": spreads,
        "C2_by_configuration": c2,
        "eligible": eligible,
        "leader_by_CV_mean": best,
        "margins_to_leader": margins_to_best,
        "candidates": candidates,
        "chosen": chosen,
        "runner_up": runner,
        "C1": {"level": c1, "margin": m, "spread": s, "ratio": ratio},
        "C3": {"level": c3, "learning_curve": lc_summary},
        "selection_confidence": level,
        "prior_agreement": agreement,
        "breadth_note": f"{len(errs) - 1} configurations compared (more than 10: {'yes' if len(errs) - 1 > 10 else 'no'})",
        "seed": SEED,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("chosen:", chosen, "| runner-up:", runner, "| C1", c1, "| C3", c3, "| confidence", level, "| prior", agreement)
    print("written:", OUT)


if __name__ == "__main__":
    sys.exit(run())
