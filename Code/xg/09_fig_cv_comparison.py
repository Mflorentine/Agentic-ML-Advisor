"""xG analysis, step 4f', Figure 3: how the configurations compared in cross-validation (sub-task 1).

Left: cross-validated log-loss of the baseline and the four kept configurations, dot = mean over the
10 outer folds, line = +/- one fold standard deviation. Right: the difference in log-loss between each
configuration and the recommended one, `Logistic + poly`, computed fold by fold on the same matches,
dot = mean difference, line = +/- one standard deviation of the fold differences (the spread).
Positive = worse than the recommended configuration. The baseline lies off the right panel's scale
and is marked at its edge. The two configurations added by the diagnosis loop are not shown: they
changed nothing reported.

Reads only outputs written by the core (no refitting, no recomputed numbers):
  Code/outputs/xg/core_cv_round2_subtask1.json   CV table (means, fold SDs)
  Code/outputs/xg/core_recommend_subtask1.json   margins of the recommendation over the others
Writes Code/outputs/xg/figures/fig_cv_comparison_subtask1.png and figures/dark/...

Run:  cd Code && uv run python xg/09_fig_cv_comparison.py
"""
from __future__ import annotations

import json
import os
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xg_style as st  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs", "xg")
REC = "Logistic + poly"
ORDER = ["Logistic", "Logistic + L2", "Logistic + poly", "Logistic + poly + L2", "Baseline (training goal share)"]
LABEL = {"Logistic": "Plain", "Logistic + L2": "+ L2", "Logistic + poly": "+ poly", "Logistic + poly + L2": "+ poly + L2",
         "Baseline (training goal share)": "Baseline"}


def main() -> None:
    table = {r["configuration"]: r for r in json.load(open(os.path.join(OUT, "core_cv_round2_subtask1.json")))["table"]["rows"]}
    rec = json.load(open(os.path.join(OUT, "core_recommend_subtask1.json")))
    assert rec["recommendation"]["configuration"] == REC
    # margin_rec_minus_this is in negative log-loss, positive = the recommendation is better, which is
    # the same number as (this configuration's log-loss - the recommendation's): positive = this one is worse
    diff = {w["configuration"]: (w["evidence"]["margin_rec_minus_this"], w["evidence"]["spread"])
            for w in rec["why_not"] if w.get("entry") in ORDER}
    m_base, s_base = rec["selection_confidence"]["C2"]["margin"]
    diff["Baseline (training goal share)"] = (m_base, s_base)
    diff[REC] = (0.0, 0.0)
    ys = list(range(len(ORDER)))[::-1]
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(16 * st.CM, 7 * st.CM), sharey=True)
        for y, k in zip(ys, ORDER):
            c = t.no_goal if k.startswith("Baseline") else st.MODEL
            r = table[k]
            a1.errorbar(r["cv_mean_logloss"], y, xerr=r["fold_sd_logloss"], fmt="o", color=c, capsize=3, markersize=5, linewidth=1.5)
            m, s = diff[k]
            if k.startswith("Baseline"):
                a2.text(0.0064, y, f"+{m:.3f}, off scale →", ha="right", va="center", fontsize=10, color=c)
            else:
                a2.errorbar(m, y, xerr=s, fmt="o", color=c, capsize=3, markersize=5, linewidth=1.5)
        a1.set_yticks(ys)
        a1.set_yticklabels([LABEL[k] for k in ORDER])
        a1.set_xlabel("Log-loss (± fold SD)")
        a1.set_xticks([0.25, 0.275, 0.30, 0.325])
        a2.axvline(0, color=t.no_goal, linewidth=0.8, linestyle=":", zorder=0)
        a2.set_xlim(-0.001, 0.0065)
        a2.set_xticks([0, 0.002, 0.004, 0.006])
        a2.set_xticklabels(["0", "0.002", "0.004", "0.006"])
        a2.set_xlabel("Difference from + poly")
        print(st.save(fig, "fig_cv_comparison_subtask1", t))


if __name__ == "__main__":
    main()
