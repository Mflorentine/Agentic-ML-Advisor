# Note for Florentine

From David, 16 October 2026.

## The aim

The instructions should lead to a report that is consistent with how the book's authors (Lindholm, Wahlström, Lindsten and Schön) would work. This is now the `Purpose` section at the top of [instructions.md](instructions.md), and every rule in the contract and in [ML Guide.md](ML%20Guide.md) is to be judged by it. We still have a long way to go.

## What to do

Work through the three example datasets with the agent, one step at a time, and look at what results the workflow gives. Wherever the instructions, the guide's Part II or the interim core lead to something the book's authors would not do, or something awkward to work with, change them with a message beginning **FRAMEWORK**. Then carry on, so the method improves with each dataset.

1. Run a step on one dataset.
2. Compare what it produced with the book's practice (`ML Guide.md` Part I, and [smlbook.org](https://smlbook.org/) for the detail).
3. If the method is wrong or unhelpful, fix it under **FRAMEWORK**. The contract's `Changing This Contract` section says how: the change to `instructions.md` goes in its own commit, a change to Part II of the guide is recorded in its version note, and an analysis in progress is re-run from the earliest decision the change affects.
4. Record in that analysis's `Analysis Log` what prompted the change.

## The three datasets

| Dataset | Where it stands | Data |
| --- | --- | --- |
| Heart Failure | Finished: [Demonstration/Heart Failure/](Demonstration/Heart%20Failure/). Keep it as the reference; the contract does not allow a finished analysis to be edited. To see what the improved method gives, start it again as a new analysis folder, with script and output names that do not collide with the old ones. | In the repository: `Attachments/heart_failure_clinical_records_dataset.csv`. |
| Sepsis | Step 1 closed (16 October); step 2, defining the problem, is next. See [Demonstration/Sepsis/Appendix.md](Demonstration/Sepsis/Appendix.md). | Not in the repository (ODbL). Download the PhysioNet 2019 Challenge training data into `Attachments/sepsis-physionet-2019/`, check it against `SHA256SUMS.txt`, then re-run `Code/sepsis_01…03` to rebuild the private tables. Details in [Attachments/SOURCE.md](Attachments/SOURCE.md). |
| Mobile Price | Downloaded but not started. | Not in the repository (licence unknown). Download from Kaggle into `Attachments/Mobile Price/` and check the checksums in [Attachments/SOURCE.md](Attachments/SOURCE.md). Its `test.csv` has no `price_range`, so the test set has to be split from `train.csv`. |

Set up the environment first: [Setup.md](Setup.md), then `cd Code && ./setup_env.sh`.

## Open items

- **Uncertainty of the test result.** [ML Guide.md §5.2](ML%20Guide.md) calls the method an open decision; [instructions.md](instructions.md) step 4g fixes it as the spread across the outer cross-validation folds, tagged `[B→I pp.71–73]`. The two should be made to agree.
- **[Project Report.md](Project%20Report.md)** is now a template. Methods and Results share three sub-headings (the machine learning methods used; how it relates to smlbook.org; training and validation methods), and `The Project Report` section of the contract says how the agent helps fill them. The notes under Abstract, Introduction, the Methods opening and Discussion still refer to the old "three parts" (workflow, advisor, traceability), and so does the README's row for the report.
- **`Code/advisor/` is not built.** Until it is, each analysis writes its own interim core (`Code/core.py` belongs to Heart Failure and is never changed).
