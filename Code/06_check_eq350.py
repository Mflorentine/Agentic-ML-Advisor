"""Check that core.BookLogistic's C = 1/(2 n lambda) solves the book's eq. 3.50.

Eq. 3.50 (Lindholm et al., 2nd ed. draft of 1 September 2026, printed p. 61):
    theta = argmin (1/n) sum ln(1 + exp(-y_i theta^T x_i)) + lambda ||theta||^2,  y in {-1, +1},
with the intercept left out of the penalty (p. 60, footnote 5; REQ-5).
The cost is minimised directly with BFGS and compared with BookLogistic, and, as a control,
with a deliberately wrong conversion C = 1/(n lambda). Synthetic data only; no project data.

Run:    cd Code && uv run python 06_check_eq350.py   -> Code/outputs/check_eq350.txt
"""
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from sklearn.linear_model import LogisticRegression

from core import BookLogistic, version

SEED = 1
LAMBDAS = [1e-3, 1e-2, 1e-1, 1.0]
OUT = Path(__file__).resolve().parent / "outputs" / "check_eq350.txt"


def main() -> None:
    rng = np.random.default_rng(SEED)
    n, p = 200, 5
    X = rng.normal(size=(n, p))
    y01 = (rng.random(n) < 1 / (1 + np.exp(-X @ rng.normal(size=p)))).astype(int)
    ypm = 2 * y01 - 1
    lines = [f"core version {version()}", "lambda | max|book - BookLogistic| | max|book - wrong C=1/(n lambda)|"]
    for lam in LAMBDAS:
        def cost(t):
            return np.mean(np.logaddexp(0, -ypm * (t[0] + X @ t[1:]))) + lam * np.sum(t[1:] ** 2)
        book = minimize(cost, np.zeros(p + 1), method="BFGS", options={"gtol": 1e-10}).x
        m = BookLogistic(lam=lam).fit(X, y01).model_
        w = LogisticRegression(C=1 / (n * lam), max_iter=100_000).fit(X, y01)
        right = np.max(np.abs(book - np.r_[m.intercept_, m.coef_.ravel()]))
        wrong = np.max(np.abs(book - np.r_[w.intercept_, w.coef_.ravel()]))
        lines.append(f"{lam:g} | {right:.2e} | {wrong:.2e}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
