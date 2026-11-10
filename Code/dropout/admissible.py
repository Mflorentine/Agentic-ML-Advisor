"""Interim core, step 4a: the admissible set for the dropout analysis. Interim core, not reviewed.

Applies, in order, to the 14 structural configurations of ML Guide section 9:
  1. task gate (section 12): Property 1 output type decides the admissible families;
  2. must-haves the user has stated (section 12): a configuration that cannot meet one gets USER;
  3. compulsory modifiers (section 12): MOD-1 (separability) and MOD-2 (parameters or collinearity; covers logistic regression, amended 10 November 2026).

Why-not codes (ML Guide section 20): EXCL for the task gate and MOD-1/MOD-2; USER for a must-have.
Reads only the property values and the must-have list passed in. It fits nothing.
"""

# The 14 structural configurations (ML Guide section 9), as (name, family, poly, L2)
CONFIGURATIONS = [
    ("Linear", "Linear", False, False),
    ("Linear + L2", "Linear", False, True),
    ("Linear + poly", "Linear", True, False),
    ("Linear + poly + L2", "Linear", True, True),
    ("Logistic", "Logistic", False, False),
    ("Logistic + L2", "Logistic", False, True),
    ("Logistic + poly", "Logistic", True, False),
    ("Logistic + poly + L2", "Logistic", True, True),
    ("Poisson", "Poisson", False, False),
    ("Poisson + L2", "Poisson", False, True),
    ("Exponential", "Exponential", False, False),
    ("Exponential + L2", "Exponential", False, True),
    ("kNN", "kNN", False, False),
    ("Tree", "Tree", False, False),
]

# Task gate (ML Guide section 12), by Property 1: output type
TASK_GATE = {
    "numeric": {"Linear", "kNN", "Tree"},
    "count": {"Poisson", "Linear", "kNN", "Tree"},
    "non-negative real": {"Exponential", "Linear", "kNN", "Tree"},
    "binary": {"Logistic", "kNN", "Tree"},
    "multiclass": {"Logistic", "kNN", "Tree"},
}

# Must-haves (ML Guide section 12): the families that can meet each one
MUST_HAVE_FAMILIES = {
    "Property 5: interpretability = inspectable": {"Linear", "Logistic", "Poisson", "Exponential", "Tree"},
    "Property 5: interpretability = worst-case bound": {"Tree", "Logistic"},
    "Property 6: probabilities = yes": {"Logistic"},
}


def admissible_set(props: dict, must_haves: list) -> list:
    """Return one record per configuration: name, admissible (bool), code (EXCL, USER or empty), reason.

    props keys used: output_type (str), separable (str: 'yes' or 'no'), params_ge_n_train (bool),
    exact_collinearity (bool), n_train (int), n_params (int).
    """
    out = []
    gate = TASK_GATE[props["output_type"]]
    for name, family, poly, l2 in CONFIGURATIONS:
        rec = {"configuration": name, "family": family, "poly": poly, "l2": l2,
               "admissible": True, "code": "", "reason": ""}

        # 1. task gate
        if family not in gate:
            rec.update(admissible=False, code="EXCL",
                       reason=f"task gate: Property 1 = {props['output_type']} admits {', '.join(sorted(gate))}")
            out.append(rec)
            continue

        # 2. MOD-1: separable data makes the unregularised logistic fits inadmissible (only +L2 remains)
        if props["separable"] == "yes" and family == "Logistic" and not l2:
            rec.update(admissible=False, code="EXCL",
                       reason="MOD-1: Property 9 = yes; unregularised logistic not admissible")
            out.append(rec)
            continue

        # 3. MOD-2 (ML Guide section 12, amended 10 November 2026): parameters >= n_train, or exact collinearity,
        #    makes unregularised linear, logistic, Poisson and exponential fits inadmissible
        if family in {"Linear", "Logistic", "Poisson", "Exponential"} and not l2:
            if props["params_ge_n_train"] or props["exact_collinearity"]:
                rec.update(admissible=False, code="EXCL",
                           reason="MOD-2: parameters >= n_train or exact collinearity; unregularised fit inadmissible")
                out.append(rec)
                continue

        # 4. must-haves stated by the user
        failed = [m for m in must_haves if family not in MUST_HAVE_FAMILIES[m]]
        if failed:
            rec.update(admissible=False, code="USER", reason=f"must-have not met: {'; '.join(failed)}")
            out.append(rec)
            continue

        out.append(rec)
    return out
