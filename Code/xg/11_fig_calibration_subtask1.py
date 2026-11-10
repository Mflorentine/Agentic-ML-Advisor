"""xG analysis, step 4h, Figure 5: calibration curve on the test shots (sub-task 1).

The test shots are sorted by predicted probability and split into BINS groups of equal size; for each
group the mean predicted probability (x) is plotted against the share of those shots that scored (y).
Points on the diagonal mean the predicted probabilities match the observed goal rates. Drawn for the
recommended model (blue) and, for comparison, StatsBomb's xG (orange, dashed), each binned on its own
predictions. Evaluating calibration is beyond the scope of the book (SML p. 113): this figure is our
addition, at the user's request.

Reads only Code/outputs/xg/core_test_predictions_subtask1.csv (written by the core's single test
evaluation; nothing is refitted here, and the test set is not evaluated again)
Writes Code/outputs/xg/figures/fig_calibration_subtask1.png and figures/dark/...
       Code/outputs/xg/figures/fig_calibration_subtask1.csv (the plotted values)

Run:  cd Code && uv run python xg/11_fig_calibration_subtask1.py
"""
from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xg_style as st  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs", "xg")
BINS = 10
AX_MAX = 0.5  # every plotted value lies below this; checked in main()


def binned(p: np.ndarray, y: np.ndarray) -> pd.DataFrame:
    order = np.argsort(p, kind="stable")
    groups = np.array_split(order, BINS)
    return pd.DataFrame({"mean_predicted": [p[g].mean() for g in groups], "observed_share": [y[g].mean() for g in groups],
                         "shots": [len(g) for g in groups], "goals": [int(y[g].sum()) for g in groups]})


def main() -> None:
    d = pd.read_csv(os.path.join(OUT, "core_test_predictions_subtask1.csv"))
    y = d.goal.to_numpy()
    m, s = binned(d.p_model.to_numpy(), y), binned(d.statsbomb_xg.to_numpy(), y)
    pd.concat([m.assign(source="model"), s.assign(source="statsbomb_xg")]).to_csv(
        os.path.join(st.FIGURES, "fig_calibration_subtask1.csv"), index=False)
    for name in ["light", "dark"]:
        t = st.use(name)
        fig, ax = plt.subplots(figsize=(10 * st.CM, 8 * st.CM))
        ax.plot([0, 1], [0, 1], color=t.no_goal, linewidth=0.8, linestyle=":", zorder=0)
        ax.plot(s.mean_predicted, s.observed_share, marker="o", markersize=4, color=st.STATSBOMB, linestyle="--", label="StatsBomb xG")
        ax.plot(m.mean_predicted, m.observed_share, marker="o", markersize=4, color=st.MODEL, label="This model")
        lim = AX_MAX
        assert max(m.mean_predicted.max(), s.mean_predicted.max(), m.observed_share.max(), s.observed_share.max()) <= lim
        ax.set_xlim(0, lim)
        ax.set_ylim(0, lim)
        ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
        ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
        ax.set_aspect("equal")
        ax.set_xlabel("Mean predicted probability")
        ax.set_ylabel("Share that scored")
        ax.legend(loc="upper left")
        print(st.save(fig, "fig_calibration_subtask1", t))


if __name__ == "__main__":
    main()
