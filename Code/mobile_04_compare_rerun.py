"""Mobile Price, step 4e: check that re-running the core with N_JOBS = 1 reproduces every number of the runs made
with N_JOBS = -1 (core 38e21eca...), as the contract requires after a change to the core after step 4b.

Reads   the committed outputs of the earlier core, from git (commit given below): core_cv_round1.json,
        core_cv_round2.json, core_cv_store.json; and the earlier diagnosis output saved before the re-run
        (path given as the first argument)
        the re-run outputs in Code/outputs/mobile/
Writes  Code/outputs/mobile/rerun_check.json

Compares every number, list and string recursively, except the fields that name the code version or the
fitted pipeline's printed form ("core_version_sha256", "pipeline"). Floats must be exactly equal.

Run:    cd Code && uv run python mobile_04_compare_rerun.py <saved old diagnose json>
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Code" / "outputs" / "mobile"
OLD_COMMIT = "a1b8fa7"     # step 4d commit: outputs of core 38e21eca... (N_JOBS = -1)
SKIP = {"core_version_sha256", "pipeline"}


def diff(a, b, path="") -> list[str]:
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k in SKIP:
                continue
            if k not in a or k not in b:
                out.append(f"{path}/{k}: missing on one side")
            else:
                out += diff(a[k], b[k], f"{path}/{k}")
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [f"{path}: lengths {len(a)} vs {len(b)}"]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, f"{path}[{i}]")]
    return [] if a == b else [f"{path}: {a!r} vs {b!r}"]


def old_from_git(name: str) -> dict:
    text = subprocess.run(["git", "show", f"{OLD_COMMIT}:Code/outputs/mobile/{name}"], cwd=ROOT,
                          capture_output=True, text=True, check=True, encoding="utf-8").stdout
    return json.loads(text)


def main() -> None:
    pairs = {name: (old_from_git(name), json.loads((OUT / name).read_text(encoding="utf-8")))
             for name in ("core_cv_round1.json", "core_cv_round2.json", "core_cv_store.json")}
    diag = "core_diagnose_Logistic___L2.json"
    pairs[diag] = (json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")),
                   json.loads((OUT / diag).read_text(encoding="utf-8")))
    result = {"old_commit": OLD_COMMIT, "skipped_fields": sorted(SKIP), "files": {}}
    for name, (old, new) in pairs.items():
        d = diff(old, new)
        result["files"][name] = {"old_core": old.get("core_version_sha256"), "new_core": new.get("core_version_sha256"),
                                 "identical": not d, "differences": d[:50], "n_differences": len(d)}
    result["all_identical"] = all(f["identical"] for f in result["files"].values())
    (OUT / "rerun_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: (v if k != "files" else {n: (f["identical"], f["n_differences"]) for n, f in v.items()})
                      for k, v in result.items()}, indent=2))


if __name__ == "__main__":
    main()
