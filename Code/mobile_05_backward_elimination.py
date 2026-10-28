"""Mobile Price, step 4e, DX-4 (O3): backward elimination of inputs, compared by cross-validation (ML Guide §18).

Drives the interim core through its documented entry point (`mobile/core.py cv add ... --drop ...`), one
post-prior entry per candidate, on the stored outer folds. The comparison uses the core's own `margin`
function on the stored fold accuracies; nothing here fits a model or recomputes a CV score.

Procedure (agreed with the user, 28 October 2026; the stopping rule is ours [I]):
  each round, cross-validate the current leader with each remaining input dropped in addition to those
  already dropped; take the candidate with the best CV mean; keep the drop only if that candidate beats
  the current leader by a margin >= KEEP_MARGIN x spread (paired over the 10 outer folds); otherwise stop.
  KEEP_MARGIN = 0.5 is the same cut-off as §19's "within noise" margin.

Reads   Code/outputs/mobile/core_cv_store.json (via the core)
Writes  core entries via the core (core_cv_post_prior_N.json, core_cv_store.json)
        Code/outputs/mobile/backward_elimination.json   (per round: candidates, means, margins, decision)

Run:    cd Code && uv run python mobile_05_backward_elimination.py
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.argv = sys.argv[:1]
from mobile import core  # noqa: E402

CODE = Path(__file__).resolve().parent
OUT = CODE / "outputs" / "mobile"
START = "Logistic + L2 (lambda grid from 1e-8)"         # leader after DX-3 (DR-17)
STRUCTURAL = "Logistic + L2"
GRID = {"m__lam": [1e-08, 1e-07, 1e-06, 1e-05, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]}
KEEP_MARGIN = 0.5                                       # [I], as §19 WITHIN_NOISE
MAX_ROUNDS = len(core.INPUTS) - 1


def store() -> dict:
    return json.loads(core.STORE.read_text(encoding="utf-8"))


def acc(entry_key: str) -> list[float]:
    return core.fold_values(store()["entries"][entry_key], "acc_val")


def label(dropped: list[str]) -> str:
    return f"{START} minus {', '.join(dropped)}"


def run_candidate(dropped: list[str]) -> str:
    key = label(dropped)
    if key in store()["entries"]:
        return key                                       # already cross-validated (resumed run)
    cmd = [sys.executable, "mobile/core.py", "cv", "add", STRUCTURAL]
    for c in dropped:
        cmd += ["--drop", c]
    cmd += ["--grid", json.dumps(GRID), "--label", key]
    subprocess.run(cmd, cwd=CODE, check=True, stdout=subprocess.DEVNULL)
    print(f"  {key}: {np.mean(acc(key)):.4f}", flush=True)
    return key


def main() -> None:
    leader, dropped, rounds = START, [], []
    for r in range(1, MAX_ROUNDS + 1):
        cands = []
        for c in core.INPUTS:
            if c in dropped:
                continue
            key = run_candidate(dropped + [c])
            m, s = core.margin(acc(key), acc(leader))
            cands.append({"drop": c, "entry": key, "cv_mean": float(np.mean(acc(key))),
                          "margin_vs_current": m, "spread": s})
        best = max(cands, key=lambda x: x["cv_mean"])
        keep = best["margin_vs_current"] > 0 and best["margin_vs_current"] >= KEEP_MARGIN * best["spread"]
        rounds.append({"round": r, "current": leader, "current_cv_mean": float(np.mean(acc(leader))),
                       "candidates": sorted(cands, key=lambda x: -x["cv_mean"]), "best": best["drop"],
                       "kept": bool(keep), "rule": f"margin >= {KEEP_MARGIN} x spread [I]"})
        (OUT / "backward_elimination.json").write_text(json.dumps(
            {"core_version_sha256": core.version(), "start": START, "rounds": rounds}, indent=2), encoding="utf-8")
        print(f"round {r}: best drop {best['drop']} mean {best['cv_mean']:.4f} margin {best['margin_vs_current']:+.4f} "
              f"spread {best['spread']:.4f} -> {'keep' if keep else 'stop'}", flush=True)
        if not keep:
            break
        dropped.append(best["drop"])
        leader = best["entry"]


if __name__ == "__main__":
    main()
