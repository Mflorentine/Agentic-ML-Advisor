"""Project Report: tally of the provenance tags in the *Rules applied* tables of the four analyses' Decision Records.

Reads   Demonstration/Heart Failure/Demonstration Appendix.md, Demonstration/Sepsis/Appendix.md,
        Demonstration/Mobile Price/Appendix.md, Demonstration/Heart Failure rerun/Appendix.md   (read only)
Writes  Code/outputs/project/provenance_tally.json  and  Code/outputs/project/provenance_tally.md

How it counts (so the Project Report only copies the result):
  - A Decision Record is a "### DR-NN · TYPE · step N" section of the appendix's `Decision Records`.
  - Records "in force" exclude those whose *Supersedes / superseded by* field says "superseded by" without
    "in part"; a record superseded only in part stays in force. Counts are also given over all records.
  - Only the *Rules applied* table of each record is read, one row per rule applied; DX records, which use
    *Observation -> action* instead, contribute no rows.
  - Each row is classified by the tags in its Provenance column, two ways:
      rows_by_strongest  one class per row, by priority UNLISTED > [B->I] > [B] > [I]; a row with no tag is "none"
                         (the convention of the analyses' Recommendation Reports, part 13);
      tag_mentions       every distinct tag kind in the row counted once, so a row tagged "[B pp.72-73]; [I]"
                         counts once under [B] and once under [I].
  - "[B p" and "[B pp" are book advice [B]; "[B→I" is a book fact interpreted into advice; "[I]" is ours;
    "UNLISTED" marks a rule not in the guide (written UNLISTED [I]).

Run:    cd Code && uv run python project_01_provenance_tally.py
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "project"
ANALYSES = {
    "Heart Failure (original)": ROOT / "Demonstration" / "Heart Failure" / "Demonstration Appendix.md",
    "Sepsis": ROOT / "Demonstration" / "Sepsis" / "Appendix.md",
    "Mobile Price": ROOT / "Demonstration" / "Mobile Price" / "Appendix.md",
    "Heart Failure rerun": ROOT / "Demonstration" / "Heart Failure rerun" / "Appendix.md",
}
KINDS = ["[B]", "[B→I]", "[I]", "UNLISTED", "none"]


def records(text: str) -> dict[str, str]:
    body = text.split("\n## Decision Records")[1].split("\n## Recommendation")[0]
    parts = re.split(r"\n### (DR-\d+) · ", body)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def superseded(rec: str) -> bool:
    m = re.search(r"\*\*Supersedes / superseded by:\*\*(.*)", rec)
    field = m.group(1) if m else ""
    return "superseded by" in field and "in part" not in field


def rule_rows(rec: str) -> list[str]:
    m = re.search(r"\*\*Rules applied\*\*\s*\n\n\| Rule .*?\n\| ---.*?\n((?:\|.*\n?)+)", rec)
    if not m:
        return []
    rows = []
    for line in m.group(1).strip().split("\n"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells[2] if len(cells) > 2 else "")
    return rows


def kinds_in(prov: str) -> set[str]:
    k = set()
    if "UNLISTED" in prov:
        k.add("UNLISTED")
    if "[B→I" in prov:
        k.add("[B→I]")
    if re.search(r"\[B pp?\.", prov):
        k.add("[B]")
    if "[I]" in prov.replace("UNLISTED [I]", ""):
        k.add("[I]")
    return k


def strongest(k: set[str]) -> str:
    for kind in ("UNLISTED", "[B→I]", "[B]", "[I]"):
        if kind in k:
            return kind
    return "none"


def tally(recs: dict[str, str], in_force_only: bool) -> dict:
    by_row, mentions, n_rec, n_rows = Counter(), Counter(), 0, 0
    for dr, rec in recs.items():
        if in_force_only and superseded(rec):
            continue
        n_rec += 1
        for prov in rule_rows(rec):
            n_rows += 1
            k = kinds_in(prov)
            by_row[strongest(k)] += 1
            mentions.update(k or {"none"})
    return {"records": n_rec, "rule_rows": n_rows,
            "rows_by_strongest": {kind: by_row.get(kind, 0) for kind in KINDS},
            "tag_mentions": {kind: mentions.get(kind, 0) for kind in KINDS}}


def main() -> None:
    result, totals = {"analyses": {}}, {"in_force": Counter(), "all": Counter()}
    for name, path in ANALYSES.items():
        recs = records(path.read_text(encoding="utf-8"))
        a = {"file": str(path.relative_to(ROOT)).replace("\\", "/"), "records_total": len(recs),
             "superseded": sorted(dr for dr, r in recs.items() if superseded(r)),
             "in_force": tally(recs, True), "all_records": tally(recs, False)}
        result["analyses"][name] = a
        for scope, key in (("in_force", "in_force"), ("all", "all_records")):
            totals[scope].update({f"rows_by_strongest {k}": v for k, v in a[key]["rows_by_strongest"].items()})
            totals[scope].update({f"tag_mentions {k}": v for k, v in a[key]["tag_mentions"].items()})
            totals[scope].update({"rule_rows": a[key]["rule_rows"], "records": a[key]["records"]})
    result["totals"] = {k: dict(v) for k, v in totals.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "provenance_tally.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# Provenance tags in the *Rules applied* tables of the four analyses", "",
             "Counting method: see the docstring of `Code/project_01_provenance_tally.py`. Records in force exclude fully "
             "superseded records; DX records have no *Rules applied* table.", "",
             "| Analysis | Records in force (of all) | Rule rows | [B] | [B→I] | [I] | UNLISTED | no tag |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, a in result["analyses"].items():
        r = a["in_force"]["rows_by_strongest"]
        lines.append(f"| {name} | {a['in_force']['records']} ({a['records_total']}) | {a['in_force']['rule_rows']} | "
                     f"{r['[B]']} | {r['[B→I]']} | {r['[I]']} | {r['UNLISTED']} | {r['none']} |")
    t = result["totals"]["in_force"]
    lines.append(f"| **All four** | {t['records']} | {t['rule_rows']} | {t['rows_by_strongest [B]']} | "
                 f"{t['rows_by_strongest [B→I]']} | {t['rows_by_strongest [I]']} | {t['rows_by_strongest UNLISTED']} | "
                 f"{t['rows_by_strongest none']} |")
    lines += ["", "Rows by strongest tag (one class per row, priority UNLISTED > [B→I] > [B] > [I]). Tag mentions "
              "(each distinct tag kind in a row counted once), records in force: "
              + ", ".join(f"{k} {t['tag_mentions ' + k]}" for k in KINDS) + ".",
              "", "Over all records, including superseded ones, rows by strongest tag: "
              + ", ".join(f"{k} {result['totals']['all']['rows_by_strongest ' + k]}" for k in KINDS)
              + f" ({result['totals']['all']['rule_rows']} rows)."]
    (OUT / "provenance_tally.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    for name, a in result["analyses"].items():
        print(name, "superseded:", a["superseded"])


if __name__ == "__main__":
    main()
