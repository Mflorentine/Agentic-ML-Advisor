"""Mobile Price, step 1, describing pass: what is in the two source files, with no judgement about what it means.

Reads   Attachments/Mobile Price/train.csv and test.csv (never modified)
Writes  Code/outputs/mobile/01_describe.json  and  Code/outputs/mobile/01_describe.md
        (aggregates only; no row-level data, because the source licence is unknown)

Run:    cd Code && uv run python mobile_01_describe_data.py
"""
import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "Attachments" / "Mobile Price"
OUT = ROOT / "Code" / "outputs" / "mobile"

# Checksums recorded in Attachments/SOURCE.md.
EXPECTED_SHA256 = {
    "train.csv": "f9e8cd3154b8684a1be0ff401b1fba7750710af6bd076a399c6ce7ceb979c624",
    "test.csv": "e929f5999ffeedec84abf53cc8d35faa1bbd7e8ebd61826881aa62562d37adce",
}

TARGET = "price_range"

# Meanings as given in Kaggle's column descriptions (Croissant metadata, fetched 28 October 2026), quoted, not inferred.
# The unit is the one stated in that description; "not stated" where the description gives none.
DOC = {
    "battery_power": ("Total energy a battery can store in one time measured in mAh", "mAh"),
    "blue": ("Has bluetooth or not", "0/1"),
    "clock_speed": ("speed at which microprocessor executes instructions", "not stated"),
    "dual_sim": ("Has dual sim support or not", "0/1"),
    "fc": ("Front Camera mega pixels", "megapixels"),
    "four_g": ("Has 4G or not", "0/1"),
    "int_memory": ("Internal Memory in Gigabytes", "GB"),
    "m_dep": ("Mobile Depth in cm", "cm"),
    "mobile_wt": ("Weight of mobile phone", "not stated"),
    "n_cores": ("Number of cores of processor", "count"),
    "pc": ("Primary Camera mega pixels", "megapixels"),
    "px_height": ("Pixel Resolution Height", "pixels (not stated; implied by 'Pixel Resolution')"),
    "px_width": ("Pixel Resolution Width", "pixels (not stated; implied by 'Pixel Resolution')"),
    "ram": ("Random Access Memory in Mega Bytes", "MB"),
    "sc_h": ("Screen Height of mobile in cm", "cm"),
    "sc_w": ("Screen Width of mobile in cm", "cm"),
    "talk_time": ("longest time that a single battery charge will last when you are", "not stated"),
    "three_g": ("Has 3G or not", "0/1"),
    "touch_screen": ("Has touch screen or not", "0/1"),
    "wifi": ("Has wifi or not", "0/1"),
    "price_range": ("This is the target variable with value of 0(low cost), 1(medium cost), 2(high cost) and 3(very high cost).", "class 0-3"),
    "id": ("ID", "none"),
}


def file_facts(path: Path) -> dict:
    raw = path.read_bytes()
    return {
        "file": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sha256_matches_SOURCE_md": hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256[path.name],
        "bytes": len(raw),
        "crlf_line_endings": b"\r\n" in raw,
        "ascii_only": all(b < 128 for b in raw),
    }


def column_detail(df: pd.DataFrame) -> list[dict]:
    rows = []
    for c in df.columns:
        s = df[c]
        binary = set(s.dropna().unique()) <= {0, 1}
        r = {
            "column": c,
            "meaning": DOC.get(c, ("undocumented", "undocumented"))[0],
            "unit": DOC.get(c, ("undocumented", "undocumented"))[1],
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "distinct": int(s.nunique()),
            "min": float(s.min()),
            "p01": float(s.quantile(0.01)),
            "median": float(s.median()),
            "p99": float(s.quantile(0.99)),
            "max": float(s.max()),
            "zeros": int((s == 0).sum()),
            "non_integer_values": int((s != s.round()).sum()),
            "binary_0_1": bool(binary),
        }
        if binary:
            r["count_0"] = int((s == 0).sum())
            r["count_1"] = int((s == 1).sum())
        rows.append(r)
    return rows


def oddities(df: pd.DataFrame) -> dict:
    """Counts of value combinations that may be worth asking about. Counted, not judged or corrected."""
    return {
        "px_height_lt_100": int((df["px_height"] < 100).sum()),
        "px_height_eq_0": int((df["px_height"] == 0).sum()),
        "sc_w_eq_0": int((df["sc_w"] == 0).sum()),
        "sc_w_gt_sc_h": int((df["sc_w"] > df["sc_h"]).sum()),
        "px_height_gt_px_width": int((df["px_height"] > df["px_width"]).sum()),
        "fc_gt_pc": int((df["fc"] > df["pc"]).sum()),
        "four_g_1_and_three_g_0": int(((df["four_g"] == 1) & (df["three_g"] == 0)).sum()),
        "m_dep_values": sorted(df["m_dep"].unique().tolist()),
        "n_cores_values": sorted(int(v) for v in df["n_cores"].unique()),
        "clock_speed_values_count": int(df["clock_speed"].nunique()),
    }


def main() -> None:
    train_path, test_path = SRC_DIR / "train.csv", SRC_DIR / "test.csv"
    train, test = pd.read_csv(train_path), pd.read_csv(test_path)
    inputs = [c for c in train.columns if c != TARGET]

    binary_inputs = [c for c in inputs if set(train[c].unique()) <= {0, 1}]
    y = train[TARGET]
    class_counts = {str(k): int(v) for k, v in y.value_counts().sort_index().items()}

    # Row order: is the file sorted by the target, and how long is the longest run of one class?
    runs = (y != y.shift()).cumsum()
    longest_run = int(y.groupby(runs).size().max())

    # Duplicates: whole rows, and identical inputs with different targets.
    dup_rows = int(train.duplicated().sum())
    dup_inputs = int(train.duplicated(subset=inputs).sum())
    conflicting = int((train.groupby(inputs)[TARGET].nunique() > 1).sum())

    # Overlap: rows of test.csv whose 20 inputs also appear in train.csv.
    overlap = int(test[inputs].merge(train[inputs].drop_duplicates(), how="inner").shape[0])

    summary = {
        "train": {
            **file_facts(train_path),
            "rows": int(train.shape[0]),
            "columns": int(train.shape[1]),
            "missing_cells": int(train.isna().sum().sum()),
            "duplicate_rows": dup_rows,
            "duplicate_input_rows": dup_inputs,
            "input_patterns_with_conflicting_target": conflicting,
            "class_counts": class_counts,
            "class_shares": {k: v / len(y) for k, v in class_counts.items()},
            "rows_sorted_by_target": bool(y.is_monotonic_increasing or y.is_monotonic_decreasing),
            "longest_run_of_one_class": longest_run,
            "n_inputs": len(inputs),
            "binary_inputs": binary_inputs,
            "n_binary_inputs": len(binary_inputs),
            "oddities": oddities(train),
            "column_detail": column_detail(train),
        },
        "test": {
            **file_facts(test_path),
            "rows": int(test.shape[0]),
            "columns": int(test.shape[1]),
            "has_target": TARGET in test.columns,
            "missing_cells": int(test.isna().sum().sum()),
            "duplicate_input_rows": int(test.duplicated(subset=inputs).sum()),
            "id_is_1_to_n": bool((test["id"] == range(1, len(test) + 1)).all()),
            "rows_whose_inputs_also_appear_in_train": overlap,
            "inputs_outside_train_range": {
                c: int(((test[c] < train[c].min()) | (test[c] > train[c].max())).sum()) for c in inputs
            },
            "column_detail": column_detail(test),
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "01_describe.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    tr, te = summary["train"], summary["test"]
    lines = [
        "# Describing pass: Mobile Price `train.csv` and `test.csv`",
        "",
        "## Files",
        "",
        "| File | Rows | Columns | Bytes | SHA-256 | Matches SOURCE.md | CRLF | ASCII only | Missing cells |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for f in (tr, te):
        lines.append(f"| `{f['file']}` | {f['rows']} | {f['columns']} | {f['bytes']:,} | `{f['sha256']}` | {f['sha256_matches_SOURCE_md']} | {f['crlf_line_endings']} | {f['ascii_only']} | {f['missing_cells']} |")
    lines += [
        "",
        "## `train.csv`",
        "",
        f"Duplicate rows: {tr['duplicate_rows']}. Rows with identical inputs: {tr['duplicate_input_rows']}. Input patterns with conflicting targets: {tr['input_patterns_with_conflicting_target']}. Rows sorted by `{TARGET}`: {tr['rows_sorted_by_target']}; longest run of one class: {tr['longest_run_of_one_class']}.",
        "",
        "Class counts of `price_range`: " + ", ".join(f"{k}: {v} ({tr['class_shares'][k]:.1%})" for k, v in class_counts.items()) + ".",
        "",
        f"Inputs: {tr['n_inputs']}, of which {tr['n_binary_inputs']} are 0/1 ({', '.join('`' + c + '`' for c in binary_inputs)}).",
        "",
        "| Column | Meaning (Kaggle) | Unit (Kaggle) | Type | Missing | Distinct | Min | 1st pct | Median | 99th pct | Max | Zeros | Non-integer | 0 / 1 counts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in tr["column_detail"]:
        counts = f"{r['count_0']} / {r['count_1']}" if r["binary_0_1"] else "—"
        lines.append(f"| `{r['column']}` | {r['meaning']} | {r['unit']} | {r['dtype']} | {r['missing']} | {r['distinct']} | {r['min']:g} | {r['p01']:g} | {r['median']:g} | {r['p99']:g} | {r['max']:g} | {r['zeros']} | {r['non_integer_values']} | {counts} |")
    o = tr["oddities"]
    lines += [
        "",
        "Value combinations counted (not judged): " + "; ".join(f"`{k}` = {v}" for k, v in o.items()) + ".",
        "",
        "## `test.csv`",
        "",
        f"Has `{TARGET}`: {te['has_target']}. `id` runs 1 to {te['rows']}: {te['id_is_1_to_n']}. Rows with identical inputs: {te['duplicate_input_rows']}. Rows whose 20 inputs also appear in `train.csv`: {te['rows_whose_inputs_also_appear_in_train']}.",
        "",
        "Rows with an input outside the `train.csv` range: " + ", ".join(f"`{k}` {v}" for k, v in te["inputs_outside_train_range"].items()) + ".",
        "",
        "| Column | Type | Missing | Distinct | Min | Median | Max | Zeros | 0 / 1 counts |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in te["column_detail"]:
        counts = f"{r['count_0']} / {r['count_1']}" if r["binary_0_1"] else "—"
        lines.append(f"| `{r['column']}` | {r['dtype']} | {r['missing']} | {r['distinct']} | {r['min']:g} | {r['median']:g} | {r['max']:g} | {r['zeros']} | {counts} |")
    (OUT / "01_describe.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
