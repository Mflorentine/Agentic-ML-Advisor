# Code

Everything that computes a number or draws a figure. Run all of it through the workspace environment (see `../Setup.md`): `cd Code && ./setup_env.sh` once, then `uv run python <script>.py`.

## Shared by every analysis

| File | What it is |
| --- | --- |
| `setup_env.sh`, `pyproject.toml`, `uv.lock` | The Python environment. `uv.lock` pins every package version. |
| `check_env.py` | Prints the interpreter and package versions, for the record. |
| `sml_style.py` | The figure style, in line with the figures of the SML book. Every new figure uses it. |
| `viz_style.py` | The older figure style, kept for the Heart Failure analysis. |
| `advisor/` | Not yet built: the reusable deterministic core. Until it exists, each analysis has its own interim core. |

## By analysis

Each finished analysis refers to these files by path, so they are not moved or renamed.

| Analysis | Scripts | Interim core | Outputs | Report |
| --- | --- | --- | --- | --- |
| Heart Failure (finished) | `01_describe_data.py` … `08_fig4_pr_curve.py` | `core.py` (never changed), with `inputs/` | `outputs/` (top level) and `outputs/figures/` | `../Demonstration/Heart Failure/` |
| Sepsis (stopped after step 1) | `sepsis_01_describe_data.py` … `sepsis_03_build_table.py` | none yet | `outputs/sepsis/` | `../Demonstration/Sepsis/` |
| xG (finished) | `xg/01_download_shots.py` … `xg/13_fig_learning_curves_team.py`, with `xg/features.py` and `xg/xg_style.py` | `xg/core.py`, with `xg/inputs/` | `outputs/xg/` and `outputs/xg/figures/` | `../Demonstration/xG/` |

Each script says at the top what it reads, what it writes and how to run it. The full guide to an analysis's code is the `Code Summary` section of its `Appendix.md`.

## A new analysis

Put its scripts in a new folder named for the analysis (for example `Code/sepsis/`), its interim core in that folder as `core.py`, and its outputs in `outputs/<name>/`. Use `sml_style.py` for figures.
