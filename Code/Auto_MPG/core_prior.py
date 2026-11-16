"""Interim core for the Auto MPG analysis, step 4b: the prior ranking (interim core, not reviewed).

Implements ML Guide.md sections 13 (suitability matrix), 14 (sequencing) and 15 (prior ranking),
using the admissible set from core.py (step 4a, unchanged). Property values come from props.json.
Only the matrix entries for the known property values are scored; unknown properties contribute nothing.

Run from Code/:  uv run python Auto_MPG/core_prior.py
Writes: outputs/Auto_MPG/core_prior.json
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402  (step 4a: admissible set, unchanged)

PROPS = HERE / "props.json"
OUT = CODE / "outputs" / "Auto_MPG" / "core_prior.json"

# Section 13: the entries that can apply to this analysis, written as (column, sign, tag).
# Columns: family ("Linear", "Poisson·exponential", "k-NN", "Tree"), "+poly", "+L2".
# Only rows whose property value is known for this analysis are listed.
MATRIX = {
    # Property 1: output type = non-negative real (the count row, for the same values)
    "Property 1: output type = non-negative real": [
        ("Linear", -1, "[B SML p. 62]"),
        ("Poisson·exponential", +1, "[B SML pp. 61–62]"),
    ],
}

# Sequencing (section 14): SEQ-1 baseline; SEQ-2 simple-first, the plain parametric model for the task.
BASELINE = "baseline (mean of the training outputs)"
SIMPLE_FIRST = "Exponential"  # SEQ-2: the plain parametric model for a non-negative real output [I]


def family_of(config):
    return core.CONFIGS[[c[0] for c in core.CONFIGS].index(config)][1]


def addons_of(config):
    _, _, poly, l2 = core.CONFIGS[[c[0] for c in core.CONFIGS].index(config)]
    return int(poly) + int(l2)


def score(config, props):
    """Section 15, step 2: sum the matrix entries for the family, then +poly, then +L2, over known properties."""
    _, family, poly, l2 = core.CONFIGS[[c[0] for c in core.CONFIGS].index(config)]
    column = "Poisson·exponential" if family in ("Poisson", "Exponential") else {"Linear": "Linear", "kNN": "k-NN", "Tree": "Tree"}.get(family, None)
    total = 0
    entries = []
    value = props["property_1_output_type"]
    if value == "non-negative real":
        for col, sign, tag in MATRIX["Property 1: output type = non-negative real"]:
            if col == column:
                total += sign
                entries.append({"property": "Property 1: output type = non-negative real", "column": col, "sign": sign, "tag": tag})
    return total, entries


def main():
    props = json.loads(PROPS.read_text(encoding="utf-8"))
    train = core.load_data()
    admissible_json = json.loads((CODE / "outputs" / "Auto_MPG" / "core_admset.json").read_text(encoding="utf-8"))
    admissible = admissible_json["admissible"]

    rows = []
    for config in admissible:
        s, entries = score(config, props)
        rows.append({"configuration": config, "score": s, "add_ons": addons_of(config), "entries": entries})

    # Section 15, step 3: highest score first; ties broken by fewer add-ons; still-tied configurations share a rank.
    rows.sort(key=lambda r: (-r["score"], r["add_ons"]))
    rank = 0
    prev = None
    for r in rows:
        key = (r["score"], r["add_ons"])
        if key != prev:
            rank += 1
            prev = key
        r["rank"] = rank

    # Section 15, step 4: keep the simple-first configuration, the baseline and the three highest-ranked others,
    # plus every configuration tied with the third of them.
    others = [r for r in rows if r["configuration"] != SIMPLE_FIRST]
    cut_score = others[2]["score"] if len(others) >= 3 else None
    cut_addons = others[2]["add_ons"] if len(others) >= 3 else None
    kept_others = [r for r in others if (r["score"], r["add_ons"]) >= (cut_score, cut_addons)] if len(others) >= 3 else others
    kept = [BASELINE, SIMPLE_FIRST] + [r["configuration"] for r in kept_others]
    not_kept = [r["configuration"] for r in rows if r["configuration"] not in [SIMPLE_FIRST] + [k["configuration"] for k in kept_others]]

    code_version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    core_version = hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest()
    result = {
        "step": "4b prior ranking",
        "code_version": f"sha256:{code_version}",
        "admissible_set_code_version": admissible_json["code_version"],
        "core_module_version": f"sha256:{core_version}",
        "label": "interim core, not reviewed",
        "property_values_used": props,
        "ranking": rows,
        "kept": kept,
        "not_kept_DISF": not_kept,
        "cut_at_third_other": {"score": cut_score, "add_ons": cut_addons},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print("ranking:")
    for r in rows:
        print(f"  rank {r['rank']}: {r['configuration']}  score {r['score']:+d}  add-ons {r['add_ons']}")
    print("kept:", kept)
    print("not kept (DISF):", not_kept)
    print("code version: sha256", code_version[:16], "...")
    print("written:", OUT)


if __name__ == "__main__":
    sys.exit(main())
