"""Interim core, step 4b: the prior ranking for the dropout analysis. Interim core, not reviewed.

Implements ML Guide section 15 (prior ranking) with the suitability matrix of section 13.
  1. admissible set: taken from the ADMSET output (04a), not recomputed here;
  2. score: the sum of the matrix entries for each admissible configuration (family column, plus the
     + poly column if it has polynomial terms, plus the + L2 column if it has L2), over the known properties;
     an entry marked "(not a must-have)" is not scored when that property is a must-have;
  3. order: highest score first; ties share a rank;
  4. keep: the baseline, the simple-first configuration (SEQ-2) and the three highest-ranked others, with ties at third;
     the rest get DISF.

The matrix is transcribed from ML Guide section 13 as it stands on 10 November 2026. Each entry is
(score, tag). Entries marked not-a-must-have are listed with that flag.
"""

# Columns of the matrix (ML Guide section 13): family column names
FAMILY_COLUMN = {"Linear": "Linear", "Logistic": "Logistic", "Poisson": "Poisson · exponential",
                 "Exponential": "Poisson · exponential", "kNN": "k-NN", "Tree": "Tree"}

# Matrix rows: (property key, property value) -> list of (column, score, tag, not_a_must_have_row)
MATRIX = {
    ("Property 1", "count"): [("Linear", -1, "[B SML p. 62]", False), ("Poisson · exponential", +1, "[B SML pp. 61–62]", False)],
    ("Property 1", "non-negative real"): [("Linear", -1, "[B SML p. 62]", False), ("Poisson · exponential", +1, "[B SML pp. 61–62]", False)],
    ("Property 2", "limited"): [("Tree", -1, "[I]", False), ("+ poly", -1, "[B→I SML pp. 59–60]", False), ("+ L2", +1, "[B→I SML p. 60]", False)],
    ("Property 3", "many"): [("k-NN", -1, "[I]", False), ("+ poly", -1, "[B→I SML p. 59]", False)],
    ("Property 4", "high"): [("k-NN", -1, "[I]", False)],
    ("Property 5", "inspectable"): [("Linear", +1, "[B→I SML p. 347]", True), ("Logistic", +1, "[B→I SML p. 347]", True),
                                    ("Poisson · exponential", +1, "[B→I SML p. 347]", True), ("Tree", +1, "[B→I SML p. 347]", True),
                                    ("+ poly", -1, "[I]", True)],
    ("Property 5", "worst-case bound"): [("Logistic", +1, "[B→I SML p. 347]", True), ("Tree", +1, "[B→I SML p. 347]", True)],
    ("Property 6", "yes"): [("Logistic", +1, "[B→I SML pp. 50, 53–54]", True)],
    ("Property 7", "yes"): [("k-NN", -1, "[B→I SML p. 26]", False), ("Tree", -1, "[I]", False)],
    ("Property 8", "linear"): [("Linear", +1, "[B→I SML p. 41]", False), ("Logistic", +1, "[B→I SML p. 55]", False),
                               ("Poisson · exponential", +1, "[B→I SML p. 63]", False)],
    ("Property 8", "curved"): [("Linear", -1, "[B→I SML pp. 58–59]", False), ("k-NN", +1, "[B→I SML p. 26]", False),
                               ("+ poly", +1, "[B→I SML p. 59]", False)],
    ("Property 8", "interactions/irregular"): [("Linear", -1, "[B→I SML p. 41]", False), ("Logistic", -1, "[B→I SML p. 55]", False),
                                               ("Poisson · exponential", -1, "[B→I SML p. 63]", False),
                                               ("k-NN", +1, "[B→I SML p. 24]", False), ("Tree", +1, "[B→I SML pp. 27–29]", False)],
}


def _config_columns(name: str, family: str, poly: bool, l2: bool) -> list:
    cols = [FAMILY_COLUMN[family]]
    if poly:
        cols.append("+ poly")
    if l2:
        cols.append("+ L2")
    return cols


def score_configuration(name: str, family: str, poly: bool, l2: bool, values: dict, must_haves: set) -> dict:
    """Sum the matrix entries for one configuration over the known property values.

    values: property key -> value, e.g. {"Property 3": "many"}; a missing key or 'unknown' contributes nothing.
    must_haves: the property keys the user has made must-haves (their not-a-must-have rows are not scored).
    """
    cols = _config_columns(name, family, poly, l2)
    total = 0
    used = []
    for prop, val in values.items():
        if val in (None, "unknown"):
            continue
        for col, score, tag, not_must_row in MATRIX.get((prop, val), []):
            if not_must_row and prop in must_haves:
                continue
            if col in cols:
                total += score
                used.append({"property": prop, "value": val, "column": col, "score": score, "tag": tag})
    return {"score": total, "entries": used}


def rank(admissible: list, values: dict, must_haves: set) -> list:
    """admissible: list of dicts with configuration, family, poly, l2 (admissible configurations only)."""
    scored = []
    for c in admissible:
        s = score_configuration(c["configuration"], c["family"], c["poly"], c["l2"], values, must_haves)
        scored.append({**c, "score": s["score"], "entries": s["entries"]})
    scored.sort(key=lambda r: -r["score"])
    # shared ranks for ties
    last_score, rank_no, seen = None, 0, 0
    for r in scored:
        seen += 1
        if r["score"] != last_score:
            rank_no = seen
            last_score = r["score"]
        r["rank"] = rank_no
    return scored


def keep(ranked: list, simple_first: str, baseline: str = "BASELINE", others_to_keep: int = 3) -> dict:
    """Keep the baseline, the simple-first configuration (SEQ-2) and the three highest others (ties at third kept).

    The baseline is not a configuration of the admissible set; it is always kept (SEQ-1).
    """
    kept = [baseline, simple_first]
    others = [r for r in ranked if r["configuration"] != simple_first]
    if others:
        cut_score = None
        for i, r in enumerate(others):
            if i < others_to_keep:
                kept.append(r["configuration"])
                cut_score = r["score"]
            elif r["score"] == cut_score:
                kept.append(r["configuration"])
    disf = [r["configuration"] for r in ranked if r["configuration"] not in kept]
    return {"kept": kept, "DISF": disf}
