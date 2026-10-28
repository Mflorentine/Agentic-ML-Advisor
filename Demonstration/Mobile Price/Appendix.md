# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

*Step 1, closed 28 October 2026. All figures are from `Code/outputs/mobile/01_describe.json`. The section covers only `train.csv`, the file the analysis uses. `test.csv` is excluded, and is noted only under* Step 1 decisions*.*

**Provenance.**
- **File used:** `Attachments/Mobile Price/train.csv`, from Kaggle's *Mobile Price Classification* by Abhishek Sharma (`iabhishekofficial`), version 1. Never modified.
- **Downloaded:** 15 October 2026, by the user. Full details are in `Attachments/SOURCE.md`.
- **Checksum:** SHA-256 `f9e8cd3154b8684a1be0ff401b1fba7750710af6bd076a399c6ce7ceb979c624`; 122,403 bytes; ASCII; LF line endings. The describing script recomputed it, and it matches `Attachments/SOURCE.md`.
- **Licence:** Kaggle's metadata gives it as "Unknown". Redistribution is therefore not established, so the folder is in `.gitignore`, and only aggregates are written to `Code/outputs/mobile/`.
- **Why this data:** the user chose it.

**Best available form: checked.**
- Kaggle lists one version: version 1, "Initial release", 28 January 2018. No earlier or later version is listed (Kaggle API, `datasets/view`, fetched 28 October 2026).
- The publisher's description is a framing story. "Bob" "collects sales data of mobile phones of various companies", and the task is to predict "a price range indicating how high the price is". It names no source for the rows, no collection date, no currency and no price thresholds.
- A web search on 28 October 2026 found many reuses of the data but no original source, and no fuller copy.
- These two files are therefore the only known form. How the rows were produced, and whether they describe real phones, is not documented.

**Shape and coverage.**
- **`train.csv`:** 2,000 rows × 21 columns: 20 inputs and the target `price_range`.
  - No missing cells and no duplicate rows. No two rows share all 20 inputs, so no input pattern has two different targets.
  - The rows are not sorted by the target; the longest run of one class is 6 rows.
  - There is no identifier, brand, model, date or other grouping column.

**Columns (`train.csv`).** The meanings are Kaggle's column descriptions, quoted from its Croissant metadata (fetched 28 October 2026). The unit is the one the description states, and "not stated" where it states none. The documentation does not say whether any column is a measurement, a manufacturer's specification or generated, so that column of the contract's checklist cannot be filled from the source.

| Column | Meaning (Kaggle) | Unit (Kaggle) | Type | Distinct | Min | 1st pct | Median | 99th pct | Max | Zeros | 0 / 1 counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `battery_power` | "Total energy a battery can store in one time measured in mAh" | mAh | integer | 1,094 | 501 | 510 | 1,226 | 1,987 | 1,998 | 0 | — |
| `blue` | "Has bluetooth or not" | 0/1 | integer | 2 | 0 | 0 | 0 | 1 | 1 | 1,010 | 1,010 / 990 |
| `clock_speed` | "speed at which microprocessor executes instructions" | not stated | decimal, steps of 0.1 | 26 | 0.5 | 0.5 | 1.5 | 3 | 3 | 0 | — |
| `dual_sim` | "Has dual sim support or not" | 0/1 | integer | 2 | 0 | 0 | 1 | 1 | 1 | 981 | 981 / 1,019 |
| `fc` | "Front Camera mega pixels" | megapixels | integer | 20 | 0 | 0 | 3 | 16 | 19 | 474 | — |
| `four_g` | "Has 4G or not" | 0/1 | integer | 2 | 0 | 0 | 1 | 1 | 1 | 957 | 957 / 1,043 |
| `int_memory` | "Internal Memory in Gigabytes" | GB | integer | 63 | 2 | 2 | 32 | 64 | 64 | 0 | — |
| `m_dep` | "Mobile Depth in cm" | cm | decimal, steps of 0.1 | 10 | 0.1 | 0.1 | 0.5 | 1 | 1 | 0 | — |
| `mobile_wt` | "Weight of mobile phone" | not stated | integer | 121 | 80 | 80 | 141 | 199 | 200 | 0 | — |
| `n_cores` | "Number of cores of processor" | count | integer, 1 to 8 | 8 | 1 | 1 | 4 | 8 | 8 | 0 | — |
| `pc` | "Primary Camera mega pixels" | megapixels | integer | 21 | 0 | 0 | 10 | 20 | 20 | 101 | — |
| `px_height` | "Pixel Resolution Height" | not stated (pixels implied) | integer | 1,137 | 0 | 15 | 564 | 1,791 | 1,960 | 2 | — |
| `px_width` | "Pixel Resolution Width" | not stated (pixels implied) | integer | 1,109 | 500 | 513 | 1,247 | 1,987 | 1,998 | 0 | — |
| `ram` | "Random Access Memory in Mega Bytes" | MB | integer | 1,562 | 256 | 297 | 2,146.5 | 3,958 | 3,998 | 0 | — |
| `sc_h` | "Screen Height of mobile in cm" | cm | integer | 15 | 5 | 5 | 12 | 19 | 19 | 0 | — |
| `sc_w` | "Screen Width of mobile in cm" | cm | integer | 19 | 0 | 0 | 5 | 17 | 18 | 180 | — |
| `talk_time` | "longest time that a single battery charge will last when you are" (the description stops there) | not stated | integer | 19 | 2 | 2 | 11 | 20 | 20 | 0 | — |
| `three_g` | "Has 3G or not" | 0/1 | integer | 2 | 0 | 0 | 1 | 1 | 1 | 477 | 477 / 1,523 |
| `touch_screen` | "Has touch screen or not" | 0/1 | integer | 2 | 0 | 0 | 1 | 1 | 1 | 994 | 994 / 1,006 |
| `wifi` | "Has wifi or not" | 0/1 | integer | 2 | 0 | 0 | 1 | 1 | 1 | 986 | 986 / 1,014 |
| `price_range` | "This is the target variable with value of 0(low cost), 1(medium cost), 2(high cost) and 3(very high cost)." | class 0–3 | integer | 4 | 0 | 0 | 1.5 | 3 | 3 | 500 | — |

**Values counted.** These are counted from `train.csv`. The decisions on `sc_w` and `px_height` are under *Step 1 decisions*: both are accepted as-is.
- `sc_w` (screen width, cm) is 0 in 180 rows. The counts for 0, 1, 2, 3, 4 and 5 cm are 180, 210, 156, 199, 182 and 161.
- `px_height` is below 100 pixels in 150 rows, and 0 in 2 rows.
- `fc` (front camera) is 0 in 474 rows and `pc` (primary camera) in 101 rows.
- The following combinations never occur:
  - `sc_w` > `sc_h`;
  - `px_height` > `px_width`;
  - `fc` > `pc`;
  - 4G without 3G.

**Machine learning checks (described, not judged).**
- **Candidate target:** `price_range`, present for all 2,000 rows.
  - Kaggle documents four ordered levels: low, medium, high and very high cost.
  - How the labels were produced is not documented: no prices, no currency, no date, and no thresholds between the ranges.
- **Output type it suggests (P1, to be confirmed in step 2):** ordinal, four ordered classes. Under §11, an ordinal output is treated as either multiclass or numeric, which is a step 2 question.
- **Class counts:** 500 in each of the four classes (25.0 % each).
- **Inputs (P3, P4):**
  - Six of the 20 inputs are 0/1 indicators: `blue`, `dual_sim`, `four_g`, `three_g`, `touch_screen` and `wifi`.
  - The other 14 take ordered numeric values. `n_cores` is a whole number from 1 to 8, and the book treats "numerical or categorical" as partly the analyst's choice (pp. 16–17).
  - With the six indicators coded as one column each and the other 14 treated as numeric, one-hot encoding leaves 20 input columns, and the categorical share is 6 / 20 = 30 %.
- **Columns that could leak the target:** none is documented as recorded after the price, or derived from it. All 20 are described as phone specifications. Because their origin is undocumented (see *Best available form*), this rests on the column descriptions alone.

**Step 1 decisions.**

| Decision | What was decided, and why | What it costs |
| --- | --- | --- |
| **Provenance** | `train.csv` as downloaded from Kaggle, version 1, the only version listed. Checksum verified. It is the publisher's live file. | The origin of the rows is undocumented, so no claim about real phones or a real market can rest on it. |
| **Scope** | All 2,000 rows and all 21 columns of `train.csv` are used. `test.csv` is excluded: 1,000 rows, with `id` and the same 20 inputs but no `price_range`, so it can neither train nor evaluate a supervised model. Its checksum (`e929f599…7adce`, CRLF line endings) matches `SOURCE.md`. The user chose "Exclude it". The training and test split will come from `train.csv` (step 2). | Nothing for evaluation, since the file has no labels. The only loss is a range check: in `test.csv`, every input except `battery_power` lies within the `train.csv` range. Its maximum is 1,999, against 1,998 in `train.csv`, in 3 rows (`01_describe.json`). |
| **Units** | Taken from Kaggle's column descriptions. No unit is stated for `clock_speed`, `mobile_wt` or `talk_time`. For `px_height` and `px_width`, "Pixel Resolution" implies pixels. Recorded as "not stated" rather than guessed. Whether a column is a measurement, a specification or generated is undocumented for every column. | Statements about these columns in the report cannot give units the source does not give. |
| **Missing data** | There are no empty cells, so nothing is imputed. No documentation says that 0 encodes "missing" in any column. | — |
| **Cleaning** | No value altered or set to missing. | — |
| **Accepted as-is** | **`sc_w` = 0 cm in 180 rows.** A width of 0 cm is not physically possible, but 1, 2 and 3 cm are as common (210, 156 and 199 rows). Zero sits on a continuous spread of small widths, so singling it out would be arbitrary. The user chose "Accept as-is". **`px_height` < 100 pixels in 150 rows (0 in 2).** There is no documented cut-off for an impossible resolution. The user chose "Accept as-is". **`fc` = 0 in 474 rows and `pc` = 0 in 101 rows** (front and primary camera, in megapixels). Left unaltered. Step 1 was closed without discussing whether 0 means "no camera" or is a flaw. | If these values are errors, the models learn from them, and the evaluation includes them. All three stay visible here. |
| **Grouping and time order** | None (ADM-3, DR-02). There is no grouping or time column, and the rows are not sorted by the target. Rows are treated as independent phones. | If several rows are in fact variants of one model, a random split would let near-copies sit on both sides of it. The files give no means to check this. |
| **Admissibility** | ADM-1 yes (DR-01), ADM-3 none (DR-02), ADM-4 yes (DR-03). | — |
| **Target and leakage** | The target is `price_range`, four ordered classes, 500 rows each. How the labels were produced is undocumented (no prices, thresholds, currency or date). No column is set aside for leakage. | Whatever rule produced the labels is unknown, so whether they are an independent outcome cannot be verified from the source. |
| **Experience level** | The user chose "New to ML" (28 October 2026). Terms such as cross-validation, overfitting and baseline are explained as they come up. | — |

## Problem Definition

*Step 2, written 28 October 2026, before anything was trained. It works from the column meanings, the `Data Summary` and row counts only. No model has been fitted, and no relationship between the inputs and the price band has been looked at.*

### Discussion

**How the problem was arrived at.** The user asked the advisor to suggest a problem. The advisor put four candidates, built from what the columns mean and from Kaggle's stated purpose, not from the data:
- (a) **Price band of a new phone:** predict the four-level `price_range` from all 20 specifications, for example for a maker deciding where a new design sits.
- (b) **Budget versus premium:** merge bands 0–1 and 2–3, and predict the yes/no split.
- (c) **Price band from basics:** predict the band from a short specification sheet chosen by the user.
- (d) **Both:** (a) then (b), as two sub-tasks.

The user chose (a), "Price band of a new phone". The framing is therefore the advisor's wording, chosen by the user. (b) and (d) were not taken: merging the bands discards the finer distinction the labels carry. (c) was not taken: a short list would have to be chosen before any result, and might lose information.

**Prediction, not understanding (ADM-2, DR-04).** The user chose "Predict": the aim is good predictions of the band for new phones, not to establish how the specifications are connected to price (p. 20).

**The four bands as a multiclass output (P1).** The bands are ordered (low < medium < high < very high), but chapters 2–4 do not cover ordinal outputs. §12 therefore asks the user to treat them as multiclass or as numeric `[I]`. The user chose "Multiclass": four separate categories (pp. 17–18). The order is not used: predicting "very high" for a "low" phone counts as one error, just as predicting "medium" does. Treating the bands as numeric was not taken. It would have assumed equal steps between the bands, and needed a rule of ours to round a prediction such as 1.4 to a band.

**What a mistake costs.** The user chose "All equally bad": any wrong band is a wrong decision. Two alternatives were offered and not taken. In one, misses of two or three bands cost more than misses of one. In the other, errors involving a particular band cost more.

**The metric.** With equal error costs, the book's default error for classification is the misclassification rate (p. 67). For a multiclass problem, the guide's own practice (§5.5, not from the book) is to use it as the deciding metric unless the error costs say otherwise. The user chose accuracy, which is 1 − the misclassification rate, "Accuracy (Recommended)". Monitored alongside are the 4 × 4 confusion matrix and each band's recall. Two alternatives were not taken:
- the same metric plus how many bands each miss is off by, which matters little when all misses cost the same;
- macro-averaged F1 (pp. 91–92; the averaging is ours), which adds little when every class has the same number of rows.

**Success and achievable level.**
- The user chose "Beat the baseline" as the success criterion, rather than a fixed 80 % or 90 %.
- They then defined "beating" as "Above 25 % beyond noise": the test accuracy minus its uncertainty must exceed 25 %. "Simply above 25 %" was not taken, because a small edge could be chance.
- The achievable level is "Unknown". No human-level or documented reference exists for this data. Results that others report for this Kaggle dataset were offered as a reference and not taken: they are unreviewed, their methods vary, and using them would anchor the work on someone else's results.

**Requirements and expectations.**
- P5: "Not needed".
- P6: "No".
- P7: "No".
- P8: "I have no expectation", so `unknown`.
- None of these is a must-have, so none removes a model family.

**Input design (§9).** All 20 columns are inputs. The six 0/1 indicators are categorical, each encoded as one column (REQ-6, p. 49). `n_cores` and the other 13 columns are numerical. The user chose "Number (Recommended)" for `n_cores`: core counts have a natural order (pp. 16–17). Treating it as a category was not taken: it would have given 27 input columns instead of 20. No domain transformation, such as a logarithm, has been raised. If one is, it is settled in step 3.

**Feasibility.**
- *Is the output recorded well enough?* It is present for every row. How the bands were set is undocumented (DR-01). This is a limitation of the labels, not a gap in them.
- *Are there enough rows?* There are 1,600 training rows for 20 input columns: a data-to-parameter ratio of 76.2 (P2 = ample).
- *Do grouping or time order constrain the split?* No: none was found (DR-02), so a random split, stratified by band, is used.
- *Is the problem answerable within the scope?* Multiclass classification is covered by chapters 2 and 3, so no method outside the four chapters is needed at this point.

### Problem

Agreed 28 October 2026 (DR-05, DR-06). Counts are from `Code/outputs/mobile/split.json`.

| Item | Agreed |
| --- | --- |
| **Rows** | All 2,000 rows of `train.csv`, one per phone. |
| **Output y** | `price_range`: 0 low, 1 medium, 2 high, 3 very high cost. 500 rows in each band. |
| **Inputs x** | All 20 specification columns. Six 0/1 indicators (`blue`, `dual_sim`, `four_g`, `three_g`, `touch_screen`, `wifi`) are categorical. The other 14, including `n_cores`, are numerical. Values are used as recorded (step 1: nothing cleaned). |
| **Output type (P1)** | Multiclass, four classes. The bands are ordinal, and are treated as multiclass at the user's choice `[I]` (§12). |
| **What a prediction is for** | Placing a new phone design in its price band. All wrong bands cost the same. |
| **Deciding metric** | Accuracy (1 − misclassification rate, p. 67). |
| **Monitored alongside** | The 4 × 4 confusion matrix, and recall for each band. |
| **Baseline** | The most common training class (pp. 330–331). All four bands have 400 training rows, so any single band gives a training accuracy of 25 %. With 100 test rows per band, the test accuracy is also 25 % whichever band is chosen. |
| **Success criterion** | Test accuracy minus its uncertainty is above 25 %. The uncertainty is the standard deviation of the recommended configuration's accuracy across the 10 outer cross-validation folds (step 4g) `[B→I pp.71–73]`. |
| **Achievable level** | Unknown. |
| **P5** | None (not needed). |
| **P6** | No. |
| **P7** | No. |
| **P8** | Unknown: "I have no expectation". |
| **Split** | 20 % test, shuffled, stratified by `price_range`, seed 2026: 1,600 training rows (400 per band) and 400 test rows (100 per band). Cross-validation folds are stratified by `price_range` (§16). The test set is locked (DR-07, `Code/outputs/mobile/split.json`). |

### Sub-tasks

1. **Price band of a new phone.** Predict a phone's price band (low, medium, high or very high) from its 20 specifications. Success: test accuracy minus its uncertainty above 25 %.

## Analysis

*The workings, one sub-heading per sub-task, added as steps 3 and 4 proceed: exploration of the training data, cross-validation tables, learning curves, diagnostics, error analysis, checks that changed nothing, and anything computed but not reported.*

## Decision Records

### DR-01 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-28
- **Question:** Is there a recorded output y for the rows to be learned from (ADM-1)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `price_range` | present in all 2,000 rows of `train.csv`: 500 each of 0, 1, 2, 3 | M | `Code/outputs/mobile/01_describe.json` |
| What the label means | "This is the target variable with value of 0(low cost), 1(medium cost), 2(high cost) and 3(very high cost)." How the ranges were set is not documented. | M | Kaggle column description (Croissant metadata) |
| `test.csv` | no `price_range` column | M | `Code/outputs/mobile/01_describe.json` |
| User's answer | "Yes" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-1 | yes | [B p.15] | supervised problem; continue |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** continue with `price_range` · stop
- **Expectation:** n/a
- **Decision:** `price_range` in `train.csv` is the recorded output, so the work continues. How its labels were produced is undocumented, and this is recorded as a limitation.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Yes"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile_01_describe_data.py`, `Code/outputs/mobile/01_describe.md`

### DR-02 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-28
- **Question:** Do several rows belong to the same unit, or are rows ordered in time (ADM-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Group or time column | none: no identifier, brand, model or date column among the 21 | M | `Code/outputs/mobile/01_describe.json` |
| Row order | not sorted by `price_range`; the longest run of one class is 6 rows | M | `Code/outputs/mobile/01_describe.json` |
| Duplicates | 0 duplicate rows; 0 rows sharing all 20 inputs | M | `Code/outputs/mobile/01_describe.json` |
| User's answer | "Neither" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-3 | none | [B pp.16, 38–39, 329] | random split; for classification, stratified folds (§16) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** none (random split) · grouped (no column to group by) · ordered in time (no column; time-series modelling out of scope) · unknown
- **Expectation:** n/a
- **Decision:** The rows are treated as independent phones, so the split and the folds are random. Stratification is settled with the split in step 2.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Neither"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/mobile/01_describe.json`

### DR-03 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-28
- **Question:** Will the cases the model is used on look like the data we have (ADM-4)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Documented origin | none: Kaggle's description names no source, date, market or currency | M | Kaggle API `datasets/view`, fetched 28 October 2026 |
| User's answer | "Yes" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-4 | yes | [B pp.328–329] | validation and test data both come from `train.csv`; continue |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** yes · no · unsure
- **Expectation:** n/a
- **Decision:** The new cases are taken to look like these rows, so validation and test data are drawn from `train.csv`. Any estimate of performance on new data holds only for phones like these, and what "like these" means is undocumented.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Yes"
- **Supersedes / superseded by:** n/a
- **Links:** `Attachments/SOURCE.md`

### DR-04 · ADM · step 2

- **Sub-task:** all
- **Date:** 2026-10-28
- **Question:** Is the main aim to predict y for new cases, or to understand how the variables are connected (ADM-2)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Problem chosen | "Price band of a new phone": predict `price_range` from all 20 specifications | M | user, 28 October 2026 (selected option) |
| User's answer | "Predict" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-2 | predict | [B p.20] | continue; the workflow optimises prediction |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** predict · understand
- **Expectation:** n/a
- **Decision:** The aim is to predict the price band of new phones. The analysis makes no claim about how the specifications are connected to price.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Predict"
- **Supersedes / superseded by:** n/a
- **Links:** n/a

### DR-05 · FORM · step 2

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** What is predicted, from what, and how is success judged?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| y | `price_range`, four ordered bands, 500 rows each | M | `Code/outputs/mobile/01_describe.json`; Kaggle column description |
| x | all 20 specification columns; 6 categorical 0/1 indicators, 14 numerical (`n_cores` numerical) | M | user, 28 October 2026: "Number (Recommended)" for `n_cores` |
| P1 | ordinal, treated as multiclass | M | user, 28 October 2026: "Multiclass" |
| Error costs | all wrong bands equally bad | M | user, 28 October 2026: "All equally bad" |
| Deciding metric | accuracy; confusion matrix and per-band recall monitored | M | user, 28 October 2026: "Accuracy (Recommended)" |
| Success criterion | test accuracy minus its uncertainty > 25 % | M | user, 28 October 2026: "Beat the baseline", then "Above 25 % beyond noise" |
| Baseline | most common training class; 25 % accuracy, since all bands have 400 training rows | M | `Code/outputs/mobile/split.json` |
| Achievable level | unknown | M | user, 28 October 2026: "Unknown" |
| P5 · P6 · P7 · P8 | none · no · no · unknown | M | user, 28 October 2026: "Not needed", "No", "No", "I have no expectation" |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, P1 = ordinal | user chose multiclass | [I] | treated as multiclass from here on (§12) |
| One metric, agreed up front | accuracy | [B p.330] | decides between models; others monitored |
| Default classification error | misclassification rate | [B p.67] | accuracy = 1 − misclassification rate |
| Multiclass metric practice | misclassification as primary; confusion matrix reported | UNLISTED [I] — §5.5 note: "for multiclass problems, use the misclassification rate as the primary metric unless the user's error costs say otherwise, report the full confusion matrix" | per-band recall monitored |
| SEQ-1 | baseline = most common training class | [B pp.330–331] | always cross-validated and reported |
| Uncertainty of the test result | SD of accuracy across the 10 outer folds | [B→I pp.71–73] | used in the success criterion |
| Numerical or categorical | `n_cores` numerical | [B pp.16–17] | 20 input columns after encoding |
| REQ-6 | 0/1 indicators one-hot encoded | [B p.49] | one column each |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** P1 multiclass · P1 numeric; accuracy · accuracy + miss distance · macro-averaged F1; success: beat the baseline · ≥ 80 % · ≥ 90 %; "beat": beyond noise · simply above 25 %; achievable level: unknown · others' Kaggle results; `n_cores`: number · category
- **Expectation:** n/a
- **Decision:** Predict the four-level `price_range` as a multiclass output from all 20 specifications, decided by accuracy, against a 25 % most-common-class baseline. Success is test accuracy minus its outer-fold SD above 25 %.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/mobile/split.json`

### DR-06 · PROP · step 2

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** What are the property values P1–P8, before any training?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 output type | multiclass (4 classes; ordinal, treated as multiclass) | M | DR-05; user: "Multiclass" |
| P2 data-to-parameter ratio | ample (1,600 ÷ (20 + 1) = 76.19) | M | `Code/outputs/mobile/split.json` |
| P3 number of inputs | few (20 columns after encoding) | M | `Code/outputs/mobile/split.json` |
| P4 share of categorical inputs | low (6 ÷ 20 = 30 %) | M | `Code/outputs/mobile/split.json` |
| P5 interpretability | none | M | user, 28 October 2026: "Not needed" |
| P6 probabilities or threshold | no | M | user, 28 October 2026: "No" |
| P7 beyond training range | no | M | user, 28 October 2026: "No" |
| P8 expected shape | unknown | M | user, 28 October 2026: "I have no expectation" |
| P9, P10 | not yet computed (training data, step 3) | n/a | — |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P2 | ample | [I] | no P2 entry in the matrix |
| P3 | few | [I] | no P3 entry |
| P4 | low | [I] | no P4 entry |
| P5–P8 | none · no · no · unknown | — | contribute nothing to the prior (§15) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 76.19 |
| P3 many inputs | > 20 | 20 |
| P4 high categorical share | ≥ 50 % | 30 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** P1 multiclass · P2 ample · P3 few · P4 low · P5 none · P6 no · P7 no · P8 unknown. P9 and P10 follow in step 3.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile_02_split.py`, `Code/outputs/mobile/split.json`

### DR-07 · SPLIT · step 2

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** How is the training and test split made, and is the test set locked?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Grouping or time order | none | M | DR-02 |
| Rows | 2,000; 500 per band | M | `Code/outputs/mobile/01_describe.json` |
| Test fraction | 20 % | M | user, 28 October 2026: "20 % (Recommended)" |
| Seed | 2026 | M | user, 28 October 2026: "2026 (Recommended)" |
| Result | 1,600 training rows (400 per band); 400 test rows (100 per band) | M | `Code/outputs/mobile/split.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Split randomly | shuffled before splitting | [B pp.71, 73] | — |
| Size with about this much data | test set plus k-fold CV on the rest | [B pp.329–330] | 20 % held out; outer 10-fold CV on the 1,600 |
| ADM-3 = none | random split by row | [B p.329] | no group split |
| Stratified folds for classification | stratified by `price_range` | [I] | split and folds keep 25 % per band |
| Test set used once | locked | [B pp.74, 328] | no step 3 or step 4 code reads `test_idx` before step 4g |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** 20 % · 25 % · 10 % test; seed 2026 · 42
- **Expectation:** n/a
- **Decision:** 20 % test, shuffled and stratified by `price_range`, seed 2026. The 400 test rows are locked until the final evaluation.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "20 % (Recommended)", "2026 (Recommended)"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile_02_split.py`, `Code/outputs/mobile/split.json`

## Recommendation

*Written at the end of step 4, one sub-heading per sub-task, after its single test-set evaluation: the thirteen-part Recommendation Report of `ML Guide.md` §25, assembled from the Decision Records. Nothing in it is new.*

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1. Created `Demonstration/Mobile Price/` (the user chose the name) and copied `Templates/Report.md` and `Templates/Appendix.md` into it. | `Demonstration/Mobile Price/` |
| 2 | Step 1. Recomputed the SHA-256 of `train.csv` and `test.csv`; both match `Attachments/SOURCE.md`. Fetched Kaggle's dataset metadata and column descriptions, and searched the web for an earlier or fuller version: none was found. | `Code/outputs/mobile/01_describe.json` |
| 3 | Step 1, describing pass over both files: shape, columns, ranges, duplicates, class counts, value combinations, overlap between the files. No conclusions drawn. | `Code/mobile_01_describe_data.py`, `Code/outputs/mobile/01_describe.md` |
| 4 | Step 1. The user stated their experience, "New to ML", and answered ADM-1 "Yes", ADM-3 "Neither" and ADM-4 "Yes". | DR-01, DR-02, DR-03 |
| 5 | Step 1, scope. `test.csv` excluded (no labels), and its description removed from the `Data Summary`, leaving a note under *Step 1 decisions*. `sc_w` = 0 (180 rows) and `px_height` < 100 (150 rows) accepted as-is. Alternatives considered and not taken: setting these values to missing, with imputation inside the folds; dropping the rows; and, for `px_height`, setting only the 2 zeros to missing. | `Data Summary`, *Step 1 decisions* |
| 6 | Step 1 closed by the user ("close step 1"). Three items were offered and left undiscussed. The units of `mobile_wt`, `clock_speed` and `talk_time` stay "not stated". Zero values of `fc` and `pc` are left unaltered. The origin of the rows and labels stays undocumented. | `Data Summary`, *Step 1 decisions* |
| 7 | Step 2. The user asked for suggestions. Four candidate problems were offered, and the user chose "Price band of a new phone". ADM-2 was answered "Predict". | `Problem Definition`, DR-04 |
| 8 | Step 2, formulation. The bands are treated as multiclass (not numeric). All errors are equally costly. Accuracy is the deciding metric, with the confusion matrix and per-band recall monitored. Baseline: most common class, 25 %. Success: test accuracy minus its uncertainty above 25 %. Achievable level unknown. P5 none, P6 no, P7 no, P8 unknown ("I have no expectation"). `n_cores` is numerical. | DR-05, DR-06 |
| 9 | Step 2, split. 20 % test, shuffled and stratified by `price_range`, seed 2026: 1,600 training and 400 test rows, 25 % per band in each. P2 = ample (76.19), P3 = few (20), P4 = low (30 %). Test set locked. | `Code/mobile_02_split.py`, `Code/outputs/mobile/split.json`, DR-06, DR-07 |
| 10 | Step 2. Problem, approach and sub-task written into the `Introduction` of `Report.md`, with the two works it cites in its `References`. The book entry was added to the appendix's `References` first; the link was checked on 28 October 2026. | `Report.md` |

## Code Summary

All scripts run from `Code/` with `uv run python <script>.py`. Script names start with `mobile_`, and outputs go to `Code/outputs/mobile/`, so that nothing collides with the Heart Failure or Sepsis files. Outputs are aggregates only, because the data's licence is unknown.

| File | What it does | Reads | Writes | Seeds / parameters |
| --- | --- | --- | --- | --- |
| `Code/mobile_01_describe_data.py` | Step 1 describing pass. Recomputes the SHA-256 of both files and checks them against `SOURCE.md`. Describes each column (meaning and unit from Kaggle's descriptions, range, percentiles, zeros, 0/1 counts). Counts duplicates, conflicting targets, class counts, row order and selected value combinations, and compares `test.csv` with `train.csv`. Draws no conclusions. | `Attachments/Mobile Price/train.csv`, `test.csv` | `Code/outputs/mobile/01_describe.json`, `01_describe.md` | none |
| `Code/mobile_02_split.py` | Step 2 split. Shuffled, stratified 80 / 20 split of `train.csv` by `price_range`. Records the row indices of each part, their class counts, the input design (categorical and numerical inputs) and P2–P4 with their `[I]` thresholds as named constants. After it runs, the test indices are locked until step 4g. | `Attachments/Mobile Price/train.csv` | `Code/outputs/mobile/split.json` (indices and counts, no data values) | `SEED = 2026`, `TEST_FRACTION = 0.2` |

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published). Read at smlbook.org; the link was checked on 28 October 2026. Page references in the Decision Records come from `ML Guide.md`.
- Sharma, A. (2018). *Mobile Price Classification* [Dataset], version 1. Kaggle. [https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification). The creator, title, version and date (28 January 2018) are from Kaggle's API metadata, checked 28 October 2026. Licence: "Unknown".
