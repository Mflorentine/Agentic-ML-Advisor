# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

*Written in step 1, and covering only the data the analysis actually uses. Provenance with a checksum, the unit of every column and whether it is a measurement or a model output, which rows are used and what was excluded, how missing values are handled, what was cleaned and what was deliberately left alone. A decision that is later reversed stays here, marked superseded. Also records the ML-specific checks: the answers to the admissibility questions (`ML Guide.md` §10), the candidate target and the quality of its labels, the output type, class counts, the number of inputs after encoding and the share that are categorical, columns that could leak the target, and the user's ML experience level.*

## Problem Definition

*Written in step 2, before anything is trained. Three parts. `Discussion`: how the problem was arrived at, what was ruled out, and whether it is a prediction problem. `Problem`: what is predicted, from what, the output type, the agreed metric, the success criterion, the baseline and the achievable level, the must-have requirements, and any expectations the user states about the relationship (quoted). `Sub-tasks`: the separately answerable parts. Ends with the train/test split, its seed, and the statement that the test set is locked.*

## Analysis

*The workings, one sub-heading per sub-task, added as steps 3 and 4 proceed: exploration of the training data, cross-validation tables, learning curves, diagnostics, error analysis, checks that changed nothing, and anything computed but not reported.*

## Decision Records

*The advisor's reasoning trace, one record per decision, written when the decision is made, in the format of `ML Guide.md` §24. Records are never renumbered; a reversed decision stays, marked superseded.*

## Recommendation

*Written at the end of step 4, one sub-heading per sub-task, after its single test-set evaluation: the thirteen-part Recommendation Report of `ML Guide.md` §25, assembled from the Decision Records. Nothing in it is new.*

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |

## Code Summary

*The guide to the analysis code, kept current whenever code is added or changed. What each file does, how to run it, what it reads and produces, and any parameter or seed that affects the result. Installation belongs in [Setup.md](Setup.md), not here.*

## References

*Added as sources are cited. Always the last section.*
