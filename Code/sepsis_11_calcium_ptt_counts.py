"""Sepsis, after step 3: counts for two data questions raised by Figure 3, from the training patients only.

(a) The low Calcium cluster: training patients whose last Calcium value in ICU hours 1-6 lies below a cut-off, as a
    share of those with a Calcium value, by hospital. Proposed cut-off CALCIUM_LOW = 2.0 mg/dL: the gap in the data
    (few values between 2 and 3.5), and below any plausible total calcium; the counts at other cut-offs in the gap are
    given too, to show the count does not depend on the exact choice. Counts only; nothing is changed.
(b) PTT at its apparent reporting limits: last values of exactly 150 s and of 250 s (the maximum).

Reads   Code/outputs/sepsis/private/train_table.csv.gz   (training patients only)
Writes  Code/outputs/sepsis/11_calcium_ptt_counts.json, 11_calcium_ptt_counts.md   (aggregates only)

Run:    cd Code && uv run python sepsis_11_calcium_ptt_counts.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "sepsis"

CALCIUM_LOW = 2.0                        # proposed cut-off, mg/dL [I]
CALCIUM_SENSITIVITY = [1.75, 2.5, 3.0, 3.5]
CALCIUM_BINS = [0, 0.5, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 30]
CALCIUM_FINE = [2 + 0.25 * i for i in range(25)]   # 2.0 ... 8.0 mg/dL


def main() -> None:
    d = pd.read_csv(OUT / "private" / "train_table.csv.gz")
    out = {"rows": "training patients only (last value in ICU hours 1-6)", "calcium_low_cutoff": CALCIUM_LOW}
    cal = {}
    for s in ("A", "B", "all"):
        c = (d if s == "all" else d[d.set == s]).Calcium.dropna()
        low = int((c < CALCIUM_LOW).sum())
        cal[s] = {"with_calcium": len(c), "low": low, "low_pct": round(100 * low / len(c), 2),
                  "low_min": float(c[c < CALCIUM_LOW].min()), "low_max": float(c[c < CALCIUM_LOW].max()),
                  "at_other_cutoffs": {str(k): int((c < k).sum()) for k in CALCIUM_SENSITIVITY}}
    out["calcium"] = cal
    c = d.Calcium.dropna()
    out["calcium_bins_all"] = {str(k): int(v) for k, v in pd.cut(c, CALCIUM_BINS).value_counts().sort_index().items()}
    # (c) The bump around 4-5 mg/dL (user, 18 October 2026): the same range in 0.25 mg/dL bins, by hospital.
    out["calcium_bins_2_to_8_by_set"] = {
        s: {str(k): int(v) for k, v in pd.cut(d[d.set == s].Calcium.dropna(), CALCIUM_FINE).value_counts().sort_index().items()}
        for s in ("A", "B")}
    ptt = {}
    for s in ("A", "B", "all"):
        p = (d if s == "all" else d[d.set == s]).PTT.dropna()
        ptt[s] = {"with_ptt": len(p), "exactly_150": int((p == 150).sum()), "exactly_250": int((p == 250).sum()),
                  "above_150": int((p > 150).sum()), "max": float(p.max())}
    out["ptt"] = ptt
    (OUT / "11_calcium_ptt_counts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    text = "# Sepsis: low Calcium cluster and PTT limits (training patients)\n\n```\n" + json.dumps(out, indent=2) + "\n```\n"
    (OUT / "11_calcium_ptt_counts.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
