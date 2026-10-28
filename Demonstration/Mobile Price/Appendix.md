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

### Sub-task 1 — Price band of a new phone

**Step 3: training data only (1,600 phones).** Nothing in this step read the 400 test rows. `core.training_data()` keeps only `train_idx` from `split.json`, and asserts that no test index is kept. Every figure script reads the data through it.

- **Input design (DR-08):** all 20 inputs as recorded. Three alternatives were offered and not taken: the log of `ram` and `int_memory`; log(1 + x) of all size inputs; and derived inputs (screen area, pixel count).
- **P9 and P10 (DR-09)** were computed by `Code/mobile/core.py` (SHA-256 `6ffd570a…640b8e2b`) after the user had seen the script. P9 = yes: logistic regression with C = 1e8 on standardised inputs classifies all 1,600 training phones correctly, in 42 iterations with no convergence warning. P10 = balanced: 400 phones per band. The P9 fit is not a candidate model, and its result is not interpreted.
- **Figures proposed** (one per script, training phones only):
  1. histograms of the 14 numerical inputs, all bands together;
  2. box plots of each numerical input per band;
  3. the share of phones with each yes/no feature per band;
  4. scatter plots of `px_width` against `px_height` and `sc_w` against `sc_h`.

  The user chose Figure 1 only. Figures 2–4 were not made.
- **Figure 1 binning: two versions replaced before the figure entered the report.**
  - *First version:* 40 equal-width bins for inputs with more than 30 distinct values. `int_memory` (63 whole-number values) zig-zagged, because some bins held two values and others one. `mobile_wt` (121 values) showed a spike in its last bin, which held four whole numbers where the others held three. Both were artefacts of the bins, not features of the data.
  - *Second version:* bins of a fixed whole-number width. The last bin then held fewer possible values than the others in `battery_power`, `mobile_wt`, `px_width` and `ram`, which made a short final bar.
  - *Final version:* one bar per recorded value for every input with up to 130 distinct values, including `int_memory` (63) and `mobile_wt` (121). The other four inputs (977 to 1,304 distinct values) get 40 equal-width bins from min − 0.5 to max + 0.5, so each bin holds 37–38 possible whole numbers (`px_height` 49–50, `ram` 93–94).
  - Bar outlines are dropped for panels with more than 64 bars, so the thin bars stay visible.
  - Output size: 3,229 × 2,743 pixels in both themes, from a 16 × 14 inch canvas at 200 dpi. The tight bounding box did not enlarge it.
- **Counts quoted in the Figure 1 caption** come from `Code/outputs/mobile/figures/fig1_input_distributions.json`, training phones only. Zeros: `fc` 372, `sc_w` 145, `pc` 81, `px_height` 2. These are lower than the step 1 counts (474, 180, 101, 2), which covered all 2,000 rows.

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
- **Supersedes / superseded by:** superseded by DR-09 (P9 and P10 added in step 3; P1–P8 unchanged)
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

### DR-08 · FORM · step 3

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** What is the input design: which inputs, and is any of them transformed before modelling?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Inputs | all 20 specification columns (DR-05) | M | DR-05 |
| `n_cores` | numerical | M | user, 28 October 2026: "Number (Recommended)" (DR-05) |
| Zeros in `px_height`, `sc_w`, `fc`, `pc` | present; a logarithm is undefined at 0 | M | `Code/outputs/mobile/01_describe.json` (step 1) |
| User's answer | "All as recorded (Recommended)" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design (§9) | decided with the user from the meaning of the columns, not from the data | [B p.18] | not a configuration axis; not chosen by CV |
| Start simple | no transformation | [B p.331] | inputs used as recorded |
| REQ-6 | the six 0/1 indicators one-hot encoded | [B p.49] | one column each (one level dropped) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** all as recorded · log of `ram` and `int_memory` · log(1 + x) of all size inputs (needed because of zeros; ours) · derived inputs (screen area, pixel count; P3 would become many)
- **Expectation:** n/a
- **Decision:** All 20 inputs are used as recorded, with no transformation and no derived input. The six indicators are single 0/1 columns, and the 14 numerical inputs are unchanged. Scaling is added only by the families that need it (REQ-2, REQ-3), inside the folds (REQ-1).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "All as recorded (Recommended)"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile/core.py` (`preprocessor`, interpretation a)

### DR-09 · PROP · step 3

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** What are the property values P1–P10, now that P9 and P10 have been computed from the training phones?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 output type | multiclass (4 classes; ordinal, treated as multiclass) | M | DR-05; user: "Multiclass" |
| P2 data-to-parameter ratio | ample (1,600 ÷ (20 + 1) = 76.19) | M | `Code/outputs/mobile/split.json` |
| P3 number of inputs | few (20 columns after encoding; unchanged by DR-08) | M | `Code/outputs/mobile/split.json`; `core_p9_p10.json` (`input_columns_after_encoding`: 20) |
| P4 share of categorical inputs | low (6 ÷ 20 = 30 %) | M | `Code/outputs/mobile/split.json` |
| P5 interpretability | none | M | user, 28 October 2026: "Not needed" |
| P6 probabilities or threshold | no | M | user, 28 October 2026: "No" |
| P7 beyond training range | no | M | user, 28 October 2026: "No" |
| P8 expected shape | unknown | M | user, 28 October 2026: "I have no expectation" |
| P9 classes perfectly separable | yes: logistic regression with C = 1e8 classifies all 1,600 training phones correctly (training accuracy 1.0, 0 misclassified; 42 iterations, no convergence warning) | T | `Code/outputs/mobile/core_p9_p10.json` |
| P10 class imbalance | balanced: smallest class share 0.25 (400 per band) | T | `Code/outputs/mobile/core_p9_p10.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P2 | ample | [I] | no P2 entry in the matrix |
| P3 | few | [I] | no P3 entry |
| P4 | low | [I] | no P4 entry |
| P5–P8 | none · no · no · unknown | — | contribute nothing to the prior (§15) |
| P9 | yes | [I] | MOD-1 will apply when the admissible set is built (step 4a) |
| P10 | balanced | [I] | the diagnosis loop uses the book's default error, the misclassification rate (§16) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 76.19 |
| P3 many inputs | > 20 | 20 |
| P4 high categorical share | ≥ 50 % | 30 % |
| P9 separable | 100 % training accuracy with negligible regularisation (C = 1e8) | 100 % (1,600 of 1,600) |
| P10 imbalanced | smallest class < 20 % | 25 % |

**P3 sits exactly on its threshold.** There are 20 input columns after encoding, and P3 = many only above 20 `[I]`, so P3 = few. One more input column would change it to many. That would happen with any derived input, or with `n_cores` treated as a category, which gives 27 columns. P3 = many would add −1 to `kNN` and to every `+ poly` configuration (§13). The value rests on the input design (DR-05, DR-08), not on the data.

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** P1 multiclass · P2 ample · P3 few (on the threshold) · P4 low · P5 none · P6 no · P7 no · P8 unknown · P9 yes · P10 balanced. The P9 fit only establishes a property: it is not a candidate model, and its result is not interpreted as a finding.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

**Reference code**

- Function: `p9_p10` in `Code/mobile/core.py` (interim core, not reviewed) · version SHA-256 `6ffd570a4c9f58b3d59113bb10af643d6277ae69e95c7e7db6cfa7fa640b8e2b` · inputs: the 1,600 training rows (`split.json` `train_idx`), DR-08 input design · output: `Code/outputs/mobile/core_p9_p10.json`, copied unchanged

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — the user saw the core before it ran and chose "Run it"
- **Supersedes / superseded by:** supersedes DR-06
- **Links:** `Code/mobile/core.py`, `Code/outputs/mobile/core_p9_p10.json`

### DR-10 · ADMSET · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Which of the 14 structural configurations (§9) are admissible for sub-task 1, given the property values in DR-09?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Property values passed to the core | P1 multiclass, P2 ample, P3 few, P4 low, P5 none (not a must-have), P6 no (not a must-have), P7 no, P8 unknown, P9 yes, P10 balanced | M / T | DR-09; `Code/mobile/props_dr09.json` |
| Labels checked before 4a | `price_range` is the source's target. How the bands were set is undocumented (no prices, thresholds, currency or date), so whether the labels are independent of the inputs cannot be checked from the source. This was recorded as a limitation in step 1, and nothing new has been found | M | DR-01; `Data Summary`, *Target and leakage* |
| MOD-2, without powers | design matrix with intercept: 21 columns, rank 21; parameters 4 × 21 = 84; n_train 1,600 | T | `Code/outputs/mobile/core_admset.json` |
| MOD-2, with powers 2–3 of the 14 numerical inputs | 49 columns, rank 49; parameters 4 × 49 = 196; n_train 1,600 | T | `Code/outputs/mobile/core_admset.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, P1 = multiclass | Logistic, k-NN, Tree admissible | [B pp.17, 49–57] | 8 configurations removed: the four `Linear`, both `Poisson`, both `Exponential` |
| Must-have gates (P5, P6) | not applied: neither is a must-have | [B→I p.347]; [B→I pp.50, 53–54] | none removed |
| MOD-1 | P9 = yes: applies | [B p.61] | `Logistic` and `Logistic + poly` removed; their `+ L2` versions remain |
| MOD-2 | does not apply: full rank, and parameters < n_train, with and without powers | [B→I pp.46–47, 65] | none removed |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| MOD-2 exact collinearity (interpretation f) | rank < columns at numpy `matrix_rank` default tolerance | rank 21 of 21; 49 of 49 |
| MOD-2 parameters ≥ n_train (interpretation g: 4 × columns) | 1,600 | 84; 196 |
| Largest polynomial degree checked (§16 grid) | 3 | — |

- **Options considered:** the 14 structural configurations of §9
- **Expectation:** n/a
- **Decision:** The admissible configurations are `Logistic + L2`, `Logistic + poly + L2`, `kNN` and `Tree`. Under §14 SEQ-2, the simple-first configuration will be `Logistic + L2`, because MOD-1 removed `Logistic`. This is applied in 4b.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2` | EXCL | task gate, P1 = multiclass [B pp.17, 49–57] |
| `Poisson`, `Poisson + L2` | EXCL | task gate, P1 = multiclass [B pp.17, 49–57] |
| `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = multiclass [B pp.17, 49–57] |
| `Logistic` | EXCL | MOD-1: P9 = yes [B p.61] |
| `Logistic + poly` | EXCL | MOD-1: P9 = yes [B p.61] |

**Reference code**

- Function: `admissible_set` (`cd Code && uv run python mobile/core.py admset mobile/props_dr09.json`) · version: interim core, not reviewed, SHA-256 `c7435f48be88ccc1533ecb77da48897ff26343a99307b9607d1b56e9be083de0` (extended for 4a from `6ffd570a…`; `p9_p10` unchanged, so DR-09 stays valid) · inputs: DR-09 property values in `Code/mobile/props_dr09.json`; the 1,600 training phones; interpretations e–h in the core's docstring · output: `Code/outputs/mobile/core_admset.json`, copied above unchanged

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — the user chose "§12 now, §13–§19 at 4b", saw the §9/§12 extension before it ran, and chose "Run it"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile/core.py`, `Code/mobile/props_dr09.json`, `Code/outputs/mobile/core_admset.json`, DR-09

### DR-11 · PRIOR · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Which admissible configurations should be cross-validated, and in what expected order?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Admissible set | `Logistic + L2`, `Logistic + poly + L2`, `kNN`, `Tree` | T | DR-10; `Code/outputs/mobile/core_admset.json` |
| P1 output type | multiclass | M | DR-09 |
| P2 data-to-parameter ratio | ample (76.19) | M | DR-09 |
| P3 number of inputs | few (20, on the threshold) | M | DR-09 |
| P4 share of categorical inputs | low (30 %) | M | DR-09 |
| P5 interpretability | none | M | DR-09; user: "Not needed" |
| P6 probabilities or threshold | no | M | DR-09; user: "No" |
| P7 beyond training range | no | M | DR-09; user: "No" |
| P8 expected shape | unknown | M | DR-09; user: "I have no expectation" |
| P9, P10 | yes, balanced (no row in the §13 matrix) | T | DR-09 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §13 matrix, all 29 entries | none applies: no property takes a value with a matrix entry (P2 ample, P3 few, P4 low, P5 none, P6 no, P7 no, P8 unknown; P1 multiclass has no entry) | — | every admissible configuration scores 0 |
| §15 order | score, then fewer add-ons; ties share a rank | [I] (§15 procedure) | `kNN` and `Tree` rank 1 (0 add-ons); `Logistic + L2` rank 3 (1); `Logistic + poly + L2` rank 4 (2) |
| SEQ-1 | baseline = most common training class | [B pp.330–331] | kept |
| SEQ-2 | simple-first = `Logistic + L2` (`Logistic` removed by MOD-1, DR-10) | [B p.331] | kept |
| §15 keep | simple-first + 3 highest-ranked others (+ ties) | [I] | `kNN`, `Tree`, `Logistic + poly + L2` kept, i.e. the whole admissible set |
| SEQ-3 | round 1 = baseline and `Logistic + L2`; round 2 only once `Logistic + L2` clearly beats the baseline | [B pp.331–332] | sets the order of 4c and 4d |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 76.19 |
| P3 many inputs | > 20 | 20 |
| P4 high categorical share | ≥ 50 % | 30 % |
| Kept besides baseline and simple-first | 3 (+ ties) | 3 others admissible |

- **Options considered:** `Logistic + L2`, `Logistic + poly + L2`, `kNN`, `Tree`
- **Expectation:** The prior carries no information here: all four scores are 0, and its order (`kNN` = `Tree` > `Logistic + L2` > `Logistic + poly + L2`) comes only from the add-on tie-break. The advisor's own expectation, which is ours and not the prior's `[I]`, is that `Logistic + L2` and `Logistic + poly + L2` will lead the cross-validation, with `kNN` and `Tree` behind. The reason is that P9 = yes: a linear boundary separates all 1,600 training phones, so a linear classifier, with L2 to counter the overfitting that separability invites (p. 61), looks well suited. If this holds, the CV order will disagree with the prior order. The expectation is recorded so that the disagreement can be seen, not explained away.
- **Decision:** Cross-validate the baseline and `Logistic + L2` in round 1, then `kNN`, `Tree` and `Logistic + poly + L2` in round 2, on the same folds. Prior order: `kNN` = `Tree` (rank 1), `Logistic + L2` (rank 3), `Logistic + poly + L2` (rank 4).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = multiclass (DR-10) |
| `Logistic`, `Logistic + poly` | EXCL | MOD-1, P9 = yes (DR-10) |

**Cross-validation protocol agreed (§16)**

- **Outer folds:** 10, stratified by `price_range`, shuffled, seed 2026. The same folds are used for every configuration, and the fold of each phone is stored with the checksums of `train.csv` and `split.json`.
- **Inner folds:** 5-fold grid search within each outer training fold, on accuracy. The grids are:
  - λ ∈ {10⁻⁴, …, 10⁴};
  - polynomial degree ∈ {2, 3};
  - k ∈ {1, 3, 5, 7, 9, 15, 21, 31, 51};
  - tree max depth ∈ {1, 2, 3, 4, 5, 6, 8, 10, 15, 20} × minimum leaf size ∈ {1, 5, 10, 20}.
- **Deciding metric:** accuracy. Margins are means of fold differences, and the spread is the SD of those differences.
- **Monitored (§5.5 note):** the 4 × 4 confusion matrix per outer validation fold, pooled, and recall per band. These are not used in any decision.
- **Diagnosis errors:** the misclassification rate (P10 = balanced).
- **Decision threshold:** none (P6 = no).
- **Flags:** none. Ordinal regression (§23, not covered in chapters 2–4) is noted as outside the solution space. It becomes a `FLAG` only if evidence in the diagnosis loop suggests it might help.

**Reference code**

- Function: `prior_ranking` (`cd Code && uv run python mobile/core.py prior mobile/props_dr09.json`) · version: interim core, not reviewed, SHA-256 `38e21eca7daeec0b188a2af59efcb22c603792f69f17b8302308ae50be182fda`. It was extended for 4b from `c7435f48…` with §13–§19 and interpretations i–y; `p9_p10` and `admissible_set` are unchanged, so DR-09 and DR-10 stay valid · inputs: DR-09 property values in `Code/mobile/props_dr09.json`; the admissible set recomputed by `admissible_set` (identical to DR-10) · output: `Code/outputs/mobile/core_prior.json`, copied above unchanged

- **Confidence:** n/a
- **Outcome vs expectation:** agree with the advisor's expectation; disagree with the prior order (filled in by DR-13). The CV order is `Logistic + L2` (0.9638) > `Logistic + poly + L2` (0.9431) > `Tree` (0.8281) > `kNN` (0.6250). The two Logistic configurations lead, as expected from P9 = yes. The prior's rank-1 configurations, `kNN` and `Tree`, come last and third. The CV winner among the prior-kept configurations, `Logistic + L2`, has prior rank 3. This is a disagreement with the prior, recorded as a finding. The prior scores were all 0, so its order came only from the add-on tie-break.
- **User involvement:** approved — the user saw the §13–§19 extension before any output was used ("Run the prior"), and then agreed the method: "Agree the method"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile/core.py`, `Code/mobile/props_dr09.json`, `Code/outputs/mobile/core_prior.json`, DR-09, DR-10

### DR-12 · CV · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Does the simple-first configuration, `Logistic + L2`, clearly beat the baseline in nested cross-validation (round 1, SEQ-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Baseline, outer folds | predicts band 0 in all 10 folds (four-way tie, interpretation u); accuracy 0.25 in every fold | CV | `Code/outputs/mobile/core_cv_round1.json` |
| `Logistic + L2`, validation accuracy per outer fold | 0.9437, 0.9750, 0.9437, 0.9750, 0.9812, 0.9563, 0.9688, 0.9750, 0.9500, 0.9688 | CV | `Code/outputs/mobile/core_cv_store.json` |
| `Logistic + L2`, training accuracy per outer fold | 0.9868, 0.9826, 0.9833, 0.9854, 0.9861, 0.9847, 0.9868, 0.9840, 0.9847, 0.9861 | CV | `Code/outputs/mobile/core_cv_store.json` |
| Convergence | all 10 outer refits converged | CV | `core_cv_round1.json` (`not_converged_folds`: 0) |
| REQ-1, REQ-3, REQ-6 in the pipeline | `design` (DR-08 encoding) → `scale` (StandardScaler) → `m` (BookLogistic), refitted inside every outer and inner training fold | CV | `core_cv_store.json` (`pipeline`) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 | round 1 = baseline and the simple-first configuration only | [B pp.331–332] | — |
| §16 nested CV | 10 outer × 5 inner, stratified by `price_range`, seed 2026; tuned on accuracy | [B pp.72–73]; [I] | — |
| C2 (`Logistic + L2` vs baseline) | margin 0.7138 ≥ 1 × spread 0.0141 → clear | [I] | round 2 may proceed; DX-1 is not triggered |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | 0.7138 vs 0.0141 |
| Outer / inner folds | 10 / 5 | — |

**CV table** (outer 10, inner 5; stratified by `price_range`; seed 2026; metric: accuracy)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean accuracy | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (most common class) | no | n/a | 0.2500 | 0.0000 | −0.7138 (0.0141) | — | 0.7500 | 0.7500 |
| `Logistic + L2` | no | λ = 10⁻⁴ (10/10 folds) | 0.9638 | 0.0141 | — (leader) | +0.7138 (0.0141), C2 clear | 0.0149 | 0.0363 |

**Monitoring (§5.5 note): pooled outer-validation confusion matrix, `Logistic + L2`.** Rows are the true band and columns the predicted band, in the order 0, 1, 2, 3.

| True \ predicted | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| 0 | 391 | 9 | 0 | 0 |
| 1 | 10 | 380 | 10 | 0 |
| 2 | 0 | 12 | 377 | 11 |
| 3 | 0 | 0 | 6 | 394 |

Recall per band: 0 → 0.9775, 1 → 0.9500, 2 → 0.9425, 3 → 0.9850. Every misclassified phone lies in a neighbouring band. These figures are reported and not used in any decision.

- **Options considered:** baseline, `Logistic + L2`
- **Expectation:** n/a (the expectation is in DR-11 and is tested in round 2)
- **Decision:** `Logistic + L2` clearly beats the baseline (C2 clear), so round 2 (4d) proceeds with `kNN`, `Tree` and `Logistic + poly + L2` on the same folds. The tuned λ is the smallest value in the grid in all 10 folds. This is noted for the diagnosis loop (O5, §18), and no action is taken before 4e.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | not a selection; why-not codes are assigned in `FINAL` |

**Reference code**

- Function: `run_cv` via `cd Code && uv run python mobile/core.py cv round1 mobile/props_dr09.json` · version: interim core, not reviewed, SHA-256 `38e21eca7daeec0b188a2af59efcb22c603792f69f17b8302308ae50be182fda` (unchanged since DR-11) · inputs: the DR-11 kept list (round 1 = baseline + simple-first), the §16 protocol as agreed in DR-11 · output: `Code/outputs/mobile/core_cv_round1.json` and `core_cv_store.json`, copied above unchanged (rounded to 4 decimals)

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed — the user asked to "continue" after the method was agreed in DR-11
- **Supersedes / superseded by:** superseded by DR-15 (re-run under core `d89e2275…`, N_JOBS = 1; every number identical)
- **Links:** `Code/mobile/core.py`, `Code/outputs/mobile/core_cv_round1.json`, `Code/outputs/mobile/core_cv_store.json`, DR-11

### DR-13 · CV · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** How do the remaining kept configurations (`kNN`, `Tree`, `Logistic + poly + L2`) compare with `Logistic + L2` and the baseline on the same folds (round 2)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `kNN`, validation accuracy per outer fold | 0.5687, 0.6937, 0.6062, 0.6625, 0.6188, 0.6062, 0.6500, 0.6062, 0.6375, 0.6000 | CV | `Code/outputs/mobile/core_cv_store.json` |
| `kNN`, tuned k per fold | 51 in 10/10 folds (largest value in the grid) | CV | `core_cv_store.json` |
| `Tree`, validation accuracy per outer fold | 0.8750, 0.8375, 0.7750, 0.8250, 0.8000, 0.8438, 0.8313, 0.8562, 0.8313, 0.8063 | CV | `core_cv_store.json` |
| `Tree`, tuned (depth, minimum leaf) per fold | (8, 5), (15, 5), (15, 5), (6, 10), (8, 5), (8, 5), (10, 10), (8, 1), (8, 10), (6, 10) | CV | `core_cv_store.json` |
| `Logistic + poly + L2`, validation accuracy per outer fold | 0.9187, 0.9563, 0.9375, 0.9375, 0.9625, 0.9500, 0.9688, 0.9500, 0.9125, 0.9375 | CV | `core_cv_store.json` |
| `Logistic + poly + L2`, tuned per fold | degree 2, λ = 10⁻⁴ in 10/10 folds (λ the smallest value in the grid) | CV | `core_cv_store.json` |
| Convergence | all outer refits converged | CV | `core_cv_round2.json` (`not_converged_folds`: 0 for every row) |
| REQ-2 (k-NN normalised), REQ-4 (tree size tuned, never fully grown) | `kNN` pipeline: `design` → `scale` → `m`; `Tree`: `design` → `m`, with depth and minimum leaf size from the grid | CV | `core_cv_store.json` (`pipeline`, `grid`) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 | round 2 run because `Logistic + L2` clearly beat the baseline (DR-12) | [B pp.331–332] | — |
| §16 same outer folds | the folds stored in round 1 are checked and reused | [I] | margins are paired by fold |
| C2 for each configuration | clear for all four (see table) | [I] | all four are eligible under §19.1 |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | `Logistic + poly + L2` 0.6931 vs 0.0180; `Tree` 0.5781 vs 0.0288; `kNN` 0.3750 vs 0.0362 |

**CV table** (outer 10, inner 5; stratified by `price_range`; seed 2026; metric: accuracy; rounds 1 and 2)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean accuracy | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (most common class) | no | n/a | 0.2500 | 0.0000 | −0.7138 (0.0141) | — | 0.7500 | 0.7500 |
| `Logistic + L2` | no | λ = 10⁻⁴ (10/10) | 0.9638 | 0.0141 | — (leader) | +0.7138 (0.0141), clear | 0.0149 | 0.0363 |
| `Logistic + poly + L2` | no | degree 2, λ = 10⁻⁴ (10/10) | 0.9431 | 0.0180 | −0.0206 (0.0132) | +0.6931 (0.0180), clear | 0.0178 | 0.0569 |
| `Tree` | no | depth 8, minimum leaf 5 (3/10) | 0.8281 | 0.0288 | −0.1356 (0.0328) | +0.5781 (0.0288), clear | 0.0694 | 0.1719 |
| `kNN` | no | k = 51 (10/10) | 0.6250 | 0.0362 | −0.3387 (0.0314) | +0.3750 (0.0362), clear | 0.3176 | 0.3750 |

**Monitoring (§5.5 note): pooled outer-validation confusion matrices.** Rows are the true band and columns the predicted band (0, 1, 2, 3). These are reported and not used in any decision.

| Configuration | Row 0 | Row 1 | Row 2 | Row 3 | Recall per band (0 / 1 / 2 / 3) |
| --- | --- | --- | --- | --- | --- |
| `Logistic + L2` | 391, 9, 0, 0 | 10, 380, 10, 0 | 0, 12, 377, 11 | 0, 0, 6, 394 | 0.9775 / 0.9500 / 0.9425 / 0.9850 |
| `Logistic + poly + L2` | 380, 20, 0, 0 | 14, 372, 14, 0 | 0, 13, 371, 16 | 0, 0, 14, 386 | 0.9500 / 0.9300 / 0.9275 / 0.9650 |
| `Tree` | 360, 40, 0, 0 | 45, 308, 47, 0 | 0, 40, 307, 53 | 0, 0, 50, 350 | 0.9000 / 0.7700 / 0.7675 / 0.8750 |
| `kNN` | 310, 81, 9, 0 | 116, 194, 86, 4 | 12, 109, 219, 60 | 0, 10, 113, 277 | 0.7750 / 0.4850 / 0.5475 / 0.6925 |

- **Options considered:** `kNN`, `Tree`, `Logistic + poly + L2` (round 2), alongside the round-1 configurations
- **Expectation:** n/a (this record fills in DR-11's *Outcome vs expectation*)
- **Decision:** All four configurations clearly beat the baseline. `Logistic + L2` leads. Each other configuration is behind it by more than one spread: `Logistic + poly + L2` by 0.0206 (spread 0.0132), `Tree` by 0.1356 (0.0328), and `kNN` by 0.3387 (0.0314). The CV order agrees with the advisor's expectation in DR-11 and disagrees with the prior order (DR-11, *Outcome vs expectation*).
- **Noted for 4e:** a tuned hyperparameter sits at the edge of its grid in 10 of 10 folds for three configurations. For `Logistic + L2` and `Logistic + poly + L2` it is λ at its smallest value (10⁻⁴); for `kNN` it is k at its largest (51). O5 is computed for the leading configuration in the diagnosis loop.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | not a selection; why-not codes are assigned in `FINAL` |

**Reference code**

- Function: `run_cv` via `cd Code && uv run python mobile/core.py cv round2 mobile/props_dr09.json` · version: interim core, not reviewed, SHA-256 `38e21eca7daeec0b188a2af59efcb22c603792f69f17b8302308ae50be182fda` (unchanged since DR-11) · inputs: the DR-11 kept list minus the simple-first configuration, on the outer folds stored in round 1 · output: `Code/outputs/mobile/core_cv_round2.json` and `core_cv_store.json`, copied above unchanged (rounded to 4 decimals)

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Run round 2 (4d)"
- **Supersedes / superseded by:** superseded by DR-15 (re-run under core `d89e2275…`, N_JOBS = 1; every number identical)
- **Links:** `Code/mobile/core.py`, `Code/outputs/mobile/core_cv_round2.json`, `Code/outputs/mobile/core_cv_store.json`, DR-11, DR-12

### DR-14 · DX · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Diagnosis pass 1 (§18) on the leading configuration, `Logistic + L2`: which observation holds first, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Errors (misclassification rate, §16, P10 = balanced) | E_train 0.0149, E_val 0.0363, gap 0.0213 | CV | `Code/outputs/mobile/core_diagnose_Logistic___L2.json` |
| Learning curve, E_val mean (fold SD) at 10 %, 20 % … 100 % | 0.1813 (0.0685), 0.0906 (0.0272), 0.0763 (0.0224), 0.0588 (0.0211), 0.0500 (0.0177), 0.0425 (0.0171), 0.0444 (0.0143), 0.0400 (0.0122), 0.0356 (0.0132), 0.0363 (0.0141) | CV | same |
| Learning curve, E_train mean at 10 % … 100 % | 0.0014, 0.0035, 0.0109, 0.0101, 0.0099, 0.0130, 0.0137, 0.0147, 0.0138, 0.0149 | CV | same |
| Tuned λ | 10⁻⁴, the smallest value in the §16 grid, in 10/10 outer folds | CV | DR-12; `core_cv_store.json` |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 = clear (DR-12) |
| O2 training error above what the application needs | no | E_train 0.0149 < 1 − (training baseline accuracy 0.2500 + fold SD 0.0141) = 0.7359 (interpretation q) |
| **O5 tuned hyperparameter at a grid edge** | **yes**, the first that holds | λ at the smallest grid value in 10 of 10 folds |
| O3 overfitting | no | gap 0.0213 < 2 × E_train = 0.0299 |
| O4 underfitting | no | E_train 0.0149 < 2 × gap = 0.0426 |
| O6 more data likely to help | no | C3 adequate: E_val(80 %) − E_val(100 %) = 0.0037 < 0.5 × 0.0141 = 0.0070 |

- **Action:** DX-3 (O5) `[I]`: extend the grid in that direction and rerun. The λ grid for `Logistic + L2` is extended downward by four decades to {10⁻⁸, 10⁻⁷, …, 10⁴} (13 values). The original nine values are kept, so the extended search contains the old one. The configuration is cross-validated by the core on the same outer folds and marked **post-prior**. This is an action on a configuration, so the loop runs it without stopping (`instructions.md`, step 4e). DX-9 `[B p.334]`: E_train is not ≫ gap, and gap is not ≫ E_train, so neither more data nor more flexibility is ruled out by it.

**Stopping check**

- **S1 (criterion met):** not assessed until 4g, as in the Heart Failure and Sepsis analyses.
- **S2 (achievable level):** unknown (DR-05).
- **S3 (two passes without gain):** this is the first pass.
- **S4 (out of scope):** no.
- **S5 (user stops it):** no.
- **S6 (five passes):** no.
- The loop continues.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 overfitting: gap ≥ 2 × E_train | 0.0299 | 0.0213 |
| O4 underfitting: E_train ≥ 2 × gap | 0.0426 | 0.0149 |
| O5 edge in most folds | > 5 of 10 | 10 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0070 | 0.0037 |

- **Options considered:** DX-3, the only action triggered by the first observation that holds
- **Expectation** (written before the extended run): the tuned λ will move below 10⁻⁴ in most folds, and the CV mean accuracy will change by less than 0.5 × the spread of the difference to the original `Logistic + L2` entry. The reasoning is that E_train is already small (0.0149) and the gap is moderate, so a weaker penalty should change the fitted boundary only slightly. Whether the change is a gain or a loss is not predicted.
- **Decision:** O5 → DX-3. Cross-validate `Logistic + L2` with λ ∈ {10⁻⁸, …, 10⁴} as a post-prior entry, labelled "Logistic + L2 (lambda grid from 1e-8)".

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `observations` (`cd Code && uv run python mobile/core.py diagnose "Logistic + L2"`) · version: interim core, not reviewed, SHA-256 `38e21eca7daeec0b188a2af59efcb22c603792f69f17b8302308ae50be182fda` · output: `Code/outputs/mobile/core_diagnose_Logistic___L2.json`, copied above unchanged (rounded to 4 decimals)

- **Confidence:** n/a
- **Outcome vs expectation:** see DR-16, which supersedes this record. Its observations are identical, and the extended run was made under the new core version.
- **User involvement:** informed — the user asked to "Start 4e"; DX-3 is an action on a configuration and runs without stopping
- **Supersedes / superseded by:** superseded by DR-16 (pass 1 re-run under core `d89e2275…`, N_JOBS = 1; every number identical). The first DX-3 run under this record's core version failed twice in the parallel worker pool (`WinError 6`, `WinError 5`) and wrote no output (Analysis Log row 20).
- **Links:** `Code/mobile/core.py` (`observations`, `learning_curve`), `Code/outputs/mobile/core_diagnose_Logistic___L2.json`, DR-13

### DR-15 · CV · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** After the core changed (N_JOBS from −1 to 1), do rounds 1 and 2, re-run from the earliest affected decision, reproduce DR-12 and DR-13?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Reason for the change | the first DX-3 run failed twice in the parallel worker pool: `OSError: [WinError 6] The handle is invalid`, then `PermissionError: [WinError 5] Access is denied`, each followed by `BrokenProcessPool`, in the first outer fold; no output was written. Single fits at λ = 10⁻⁸, 10⁻⁶ and 10⁻⁴ ran normally (about 0.03 s, converged) | — | Analysis Log row 20 |
| User's choice | "N_JOBS = 1, re-verify (Recommended)", chosen from three options: set N_JOBS = 1 and re-verify; retry unchanged; run under a threading-backend wrapper with the core unchanged | M | user, 28 October 2026 |
| Change | `N_JOBS = -1` → `N_JOBS = 1` (how many grid-search fits run at once). No other line changed | — | `Code/mobile/core.py`, `d89e2275…` vs `38e21eca…` |
| Re-run | the CV store was removed and rebuilt; `cv round1`, `cv round2` and `diagnose "Logistic + L2"` were run under `d89e2275…` | CV | `Code/outputs/mobile/core_cv_round1.json`, `core_cv_round2.json`, `core_cv_store.json`, `core_diagnose_Logistic___L2.json` |
| Comparison | every number, list and string identical to the committed outputs of `38e21eca…` (commit `a1b8fa7`) and to the saved earlier diagnosis, apart from the code-version and printed-pipeline fields: 0 differences in each of the 4 files; floats compared for exact equality | CV | `Code/mobile_04_compare_rerun.py` → `Code/outputs/mobile/rerun_check.json` (`all_identical`: true) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Interim core changed after step 4b → superseding record, re-run from the earliest affected decision | `N_JOBS` is used only in the grid search (§16), so the earliest affected decision is round 1 (DR-12); the admissible set (DR-10) and the prior (DR-11) do not call it | `instructions.md` (Machine Learning Scope and Reasoning; When Something Changes) | rounds 1 and 2 and the pass-1 diagnosis re-run |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

**CV table**: identical to DR-13, every value (outer 10, inner 5; stratified by `price_range`; seed 2026; metric: accuracy).

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean accuracy | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (most common class) | no | n/a | 0.2500 | 0.0000 | −0.7138 (0.0141) | — | 0.7500 | 0.7500 |
| `Logistic + L2` | no | λ = 10⁻⁴ (10/10) | 0.9638 | 0.0141 | — (leader) | +0.7138 (0.0141), clear | 0.0149 | 0.0363 |
| `Logistic + poly + L2` | no | degree 2, λ = 10⁻⁴ (10/10) | 0.9431 | 0.0180 | −0.0206 (0.0132) | +0.6931 (0.0180), clear | 0.0178 | 0.0569 |
| `Tree` | no | depth 8, minimum leaf 5 (3/10) | 0.8281 | 0.0288 | −0.1356 (0.0328) | +0.5781 (0.0288), clear | 0.0694 | 0.1719 |
| `kNN` | no | k = 51 (10/10) | 0.6250 | 0.0362 | −0.3387 (0.0314) | +0.3750 (0.0362), clear | 0.3176 | 0.3750 |

- **Options considered:** set N_JOBS = 1 and re-verify · retry unchanged · threading-backend wrapper with the core unchanged
- **Expectation:** n/a
- **Decision:** The core's version for all later records is `d89e2275…`. DR-12 and DR-13 are superseded by this record. Their tables, and DR-11's *Outcome vs expectation*, stand unchanged, because the re-run reproduces them exactly.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | not a selection |

**Reference code**

- Function: `run_cv` (`cv round1`, `cv round2`) and `observations` (`diagnose "Logistic + L2"`) · version: interim core, not reviewed, SHA-256 `d89e2275ffda2d958708f3dd410f3f39a8ef187a78a9df1d2416d51b00f91872` (from `38e21eca…`: N_JOBS only) · inputs: as in DR-12 and DR-13 · outputs: `core_cv_round1.json`, `core_cv_round2.json`, `core_cv_store.json`, `core_diagnose_Logistic___L2.json`; the comparison is in `rerun_check.json`

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "N_JOBS = 1, re-verify (Recommended)"
- **Supersedes / superseded by:** supersedes DR-12 and DR-13
- **Links:** `Code/mobile/core.py`, `Code/mobile_04_compare_rerun.py`, `Code/outputs/mobile/rerun_check.json`, DR-12, DR-13

### DR-16 · DX · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Diagnosis pass 1 (§18) on `Logistic + L2`, re-run under core `d89e2275…`: which observation holds first, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Observations, errors and learning curve | identical to DR-14 in every value: E_train 0.0149, E_val 0.0363, gap 0.0213; λ at the smallest grid value in 10/10 folds; learning curve as in DR-14 | CV | `Code/outputs/mobile/core_diagnose_Logistic___L2.json`; `rerun_check.json` |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 = clear |
| O2 training error above what the application needs | no | E_train 0.0149 < 0.7359 (interpretation q) |
| **O5 tuned hyperparameter at a grid edge** | **yes**, the first that holds | λ = 10⁻⁴ (the smallest) in 10 of 10 folds |
| O3 overfitting | no | gap 0.0213 < 2 × E_train = 0.0299 |
| O4 underfitting | no | E_train 0.0149 < 2 × gap = 0.0426 |
| O6 more data likely to help | no | C3 adequate: 0.0037 < 0.0070 |

- **Action:** DX-3 (O5) `[I]`, as in DR-14. The λ grid for `Logistic + L2` is extended downward to {10⁻⁸, …, 10⁴} (13 values, the original 9 included) and cross-validated on the same folds as a post-prior entry, "Logistic + L2 (lambda grid from 1e-8)".

**Stopping check**

- S1: not assessed until 4g. S2: achievable level unknown. S3: first pass. S4: no. S5: no. S6: no.
- The loop continues.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 overfitting: gap ≥ 2 × E_train | 0.0299 | 0.0213 |
| O4 underfitting: E_train ≥ 2 × gap | 0.0426 | 0.0149 |
| O5 edge in most folds | > 5 of 10 | 10 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0070 | 0.0037 |

- **Options considered:** DX-3
- **Expectation** (written in DR-14 before any extended run, and carried over unchanged): the tuned λ will move below 10⁻⁴ in most folds, and the CV mean accuracy will change by less than 0.5 × the spread of the difference to the original `Logistic + L2` entry.
- **Decision:** O5 → DX-3, run under core `d89e2275…` (DR-17).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `observations` (`diagnose "Logistic + L2"`) · version: `d89e2275…` · output: `Code/outputs/mobile/core_diagnose_Logistic___L2.json`

- **Confidence:** n/a
- **Outcome vs expectation:** partial (filled in by DR-17).
  - **First part: agree.** λ moved below 10⁻⁴ in all 10 folds: 10⁻⁵ in 4, 10⁻⁶ in 3, 10⁻⁸ in 2, 10⁻⁷ in 1.
  - **Second part: disagree.** The CV mean rose by 0.0069, which is more than 0.5 × its spread of 0.0055 (and more than 1 ×): from 0.9638 to 0.9706.
- **User involvement:** informed (as DR-14)
- **Supersedes / superseded by:** supersedes DR-14
- **Links:** `Code/mobile/core.py`, `Code/outputs/mobile/core_diagnose_Logistic___L2.json`, DR-14, DR-15

### DR-17 · CV · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** What does `Logistic + L2` with the λ grid extended down to 10⁻⁸ (DX-3, post-prior) score on the same folds?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Validation accuracy per outer fold | 0.9500, 0.9688, 0.9500, 0.9812, 0.9875, 0.9625, 0.9812, 0.9875, 0.9625, 0.9750 | CV | `Code/outputs/mobile/core_cv_store.json` |
| Training accuracy per outer fold | 0.9917, 0.9910, 0.9951, 0.9979, 0.9910, 0.9903, 0.9993, 0.9924, 0.9931, 0.9972 | CV | same |
| Tuned λ per fold | 10⁻⁵, 10⁻⁵, 10⁻⁶, 10⁻⁸, 10⁻⁶, 10⁻⁵, 10⁻⁸, 10⁻⁶, 10⁻⁵, 10⁻⁷. The new edge (10⁻⁸) is chosen in 2 of 10 folds | CV | same |
| Convergence | all 10 outer refits converged | CV | `core_cv_post_prior_1.json` |
| Extended minus original `Logistic + L2`, paired by fold | mean +0.0069, spread 0.0055 | CV | computed from `core_cv_store.json` by the agent (the core's table gives the margin of the original to the new leader: −0.0069, spread 0.0055) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| DX-3 | λ grid extended in the direction of the edge | [I] | post-prior entry, same folds |
| §17 breadth note | 5 configurations compared so far (including this post-prior entry) | [I] | below the threshold of 10 |
| C2 | margin over the baseline 0.7206 ≥ 1 × spread 0.0141 → clear | [I] | eligible under §19.1 |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | 0.7206 vs 0.0141 |
| Breadth note | > 10 configurations | 5 |

**CV table** (outer 10, inner 5; stratified by `price_range`; seed 2026; metric: accuracy; all entries so far; margins are against the new leader)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean accuracy | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (most common class) | no | n/a | 0.2500 | 0.0000 | −0.7206 (0.0141) | — | 0.7500 | 0.7500 |
| `Logistic + L2 (lambda grid from 1e-8)` | yes | λ = 10⁻⁵ (4/10) | 0.9706 | 0.0141 | — (leader) | +0.7206 (0.0141), clear | 0.0061 | 0.0294 |
| `Logistic + L2` | no | λ = 10⁻⁴ (10/10) | 0.9638 | 0.0141 | −0.0069 (0.0055) | +0.7138 (0.0141), clear | 0.0149 | 0.0363 |
| `Logistic + poly + L2` | no | degree 2, λ = 10⁻⁴ (10/10) | 0.9431 | 0.0180 | −0.0275 (0.0145) | +0.6931 (0.0180), clear | 0.0178 | 0.0569 |
| `Tree` | no | depth 8, minimum leaf 5 (3/10) | 0.8281 | 0.0288 | −0.1425 (0.0325) | +0.5781 (0.0288), clear | 0.0694 | 0.1719 |
| `kNN` | no | k = 51 (10/10) | 0.6250 | 0.0362 | −0.3456 (0.0340) | +0.3750 (0.0362), clear | 0.3176 | 0.3750 |

**Monitoring (§5.5 note), `Logistic + L2 (lambda grid from 1e-8)`, pooled outer-validation confusion matrix.** Rows are the true band and columns the predicted band (0, 1, 2, 3):

| True \ predicted | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| 0 | 391 | 9 | 0 | 0 |
| 1 | 8 | 383 | 9 | 0 |
| 2 | 0 | 8 | 383 | 9 |
| 3 | 0 | 0 | 4 | 396 |

Recall per band: 0 → 0.9775, 1 → 0.9575, 2 → 0.9575, 3 → 0.9900. These are reported and not used in any decision.

- **Options considered:** `Logistic + L2` with λ ∈ {10⁻⁸, …, 10⁴}
- **Expectation:** n/a (this record fills in DR-16's *Outcome vs expectation*)
- **Decision:** The extended entry is the new leader, ahead of the original `Logistic + L2` by 0.0069, which is more than one spread (0.0055). The diagnosis loop continues with pass 2 on it.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `run_cv` (`cv add "Logistic + L2" --grid '{"m__lam": [1e-08, …, 10000.0]}' --label "Logistic + L2 (lambda grid from 1e-8)"`) · version: interim core, not reviewed, SHA-256 `d89e2275ffda2d958708f3dd410f3f39a8ef187a78a9df1d2416d51b00f91872` · output: `Code/outputs/mobile/core_cv_post_prior_1.json`, `core_cv_store.json`, copied above unchanged (rounded to 4 decimals)

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed (DX-3 runs without stopping)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/mobile/core_cv_post_prior_1.json`, `Code/outputs/mobile/core_cv_store.json`, DR-16

### DR-18 · DX · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Diagnosis pass 2 (§18) on the leader, `Logistic + L2 (lambda grid from 1e-8)`: which observation holds first, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Errors (misclassification rate, P10 = balanced) | E_train 0.0061, E_val 0.0294, gap 0.0233 | CV | `Code/outputs/mobile/core_diagnose_Logistic___L2__lambda_grid_from_1e_8_.json` |
| Learning curve, E_val mean (fold SD) at 10 %, 20 % … 100 % | 0.1825 (0.0712), 0.0944 (0.0279), 0.0644 (0.0250), 0.0538 (0.0274), 0.0444 (0.0229), 0.0375 (0.0164), 0.0375 (0.0161), 0.0331 (0.0144), 0.0269 (0.0132), 0.0294 (0.0141) | CV | same |
| Learning curve, E_train mean at 10 % … 100 % | 0.0014, 0.0017, 0.0012, 0.0007, 0.0026, 0.0016, 0.0048, 0.0046, 0.0044, 0.0061 | CV | same |
| Run time | 15 min 0 s (single process, 13-value λ grid at ten training sizes) | — | — |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 = clear (DR-17) |
| O2 training error above what the application needs | no | E_train 0.0061 < 1 − (0.2500 + 0.0141) = 0.7359 (interpretation q) |
| O5 tuned hyperparameter at a grid edge | no | λ at an edge (10⁻⁸) in 2 of 10 folds |
| **O3 overfitting** | **yes**, the first that holds | gap 0.0233 ≥ 2 × E_train = 0.0122 |
| O4 underfitting | no | E_train 0.0061 < 2 × gap = 0.0465 |
| O6 more data likely to help | no | C3 adequate: E_val(80 %) − E_val(100 %) = 0.0037 < 0.5 × 0.0141 = 0.0071 |

- **Action:** DX-4 (O3), less flexibility `[B pp.60, 333, 346]`. Its parts:
  - (a) Add L2 to a parametric configuration without it: does not apply, because the leader has L2.
  - (b) Remove polynomial terms: does not apply, because the leader has none.
  - (c) Feature selection by backward elimination, compared by CV: taken, at the user's choice.
  - (d) Ask whether more data is available: not reached in this pass. The only other labelled rows are the 400 locked test phones.
  - DX-9 `[B p.334]`: gap > E_train, so more flexibility is not added.
- **Backward elimination, as agreed:**
  - Each round cross-validates the current leader with each remaining input also dropped. These are post-prior entries, with the same outer folds and the same 13-value λ grid.
  - The round takes the candidate with the best CV mean, and keeps that drop only if it beats the current leader by a paired margin ≥ 0.5 × spread `[I]`, the same cut-off as §19's within-noise margin. Otherwise elimination stops.
  - The procedure is driven by `Code/mobile_05_backward_elimination.py` through the core's `cv add --drop` entry point, and the margins come from the core's `margin` function.
  - Round 1 compares 20 candidates, which takes the number of configurations compared above the breadth threshold of 10 (§17, p. 328).

**Stopping check**

- **S1:** not assessed until 4g.
- **S2:** the achievable level is unknown.
- **S3 (two passes without a gain of ≥ 0.5 × spread):** pass 1 gained 0.0069 (spread 0.0055), so S3 does not apply.
- **S4, S5, S6:** no.
- The loop continues.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 overfitting: gap ≥ 2 × E_train | 0.0122 | 0.0233 |
| O4 underfitting: E_train ≥ 2 × gap | 0.0465 | 0.0061 |
| O5 edge in most folds | > 5 of 10 | 2 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0071 | 0.0037 |
| Backward-elimination keep rule (ours, agreed with the user) | margin ≥ 0.5 × spread | see the CV record of the run |

- **Options considered:** put to the user without a recommendation:
  - backward elimination until the keep rule fails (chosen);
  - "no more data", stopping the loop (S5);
  - one elimination round only, then stop.
- **Expectation** (written before the run): no single dropped input will clear the keep rule, so elimination will stop after round 1. The reasoning is that the gap is small in absolute terms (0.0233) and the data are ample for 20 inputs (P2, 76 rows per parameter). Removing one input should reduce the variance of the fit only slightly, and most single drops should change the CV mean by less than 0.5 × spread. Which inputs, if dropped, would lower accuracy clearly is not predicted.
- **Decision:** O3 → DX-4, part (c): backward elimination with the agreed keep rule.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `observations` (`diagnose "Logistic + L2 (lambda grid from 1e-8)"`) · version: interim core, not reviewed, SHA-256 `d89e2275ffda2d958708f3dd410f3f39a8ef187a78a9df1d2416d51b00f91872` · output: `Code/outputs/mobile/core_diagnose_Logistic___L2__lambda_grid_from_1e_8_.json`, copied above unchanged (rounded to 4 decimals)

- **Confidence:** n/a
- **Outcome vs expectation:** agree (filled in by DR-19). No single drop cleared the keep rule, and elimination stopped after round 1. The best drop, `wifi`, gained +0.0019 against a threshold of 0.5 × 0.0106 = 0.0053. 15 of the 20 drops changed the CV mean by 0.0025 or less. Five lowered it by more: `mobile_wt` by 0.0100 (spread 0.0103), and four by more than one spread.
- **User involvement:** asked — "Backward elimination", chosen without a recommendation from three options
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile/core.py`, `Code/mobile_05_backward_elimination.py`, `Code/outputs/mobile/core_diagnose_Logistic___L2__lambda_grid_from_1e_8_.json`, DR-17

### DR-19 · CV · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Backward elimination, round 1 (DX-4 part c): does dropping any one input from `Logistic + L2 (lambda grid from 1e-8)` beat it by at least 0.5 × spread on the same folds?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Candidates | 20 post-prior entries, `Logistic + L2` with one input dropped each, λ ∈ {10⁻⁸ … 10⁴}, same outer folds | CV | `Code/outputs/mobile/core_cv_post_prior_2.json` … `_21.json`, `core_cv_store.json` |
| Round 1 result | best drop `wifi`: 0.9725, margin vs the leader +0.0019, spread 0.0106; below the keep threshold 0.0053, so elimination stopped | CV | `Code/outputs/mobile/backward_elimination.json` |
| Run time | about 11 min for 20 candidates | — | — |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| DX-4 (c), feature selection by backward elimination compared by CV | round 1 run; no drop kept | [B pp.333, 346] | the leader stays `Logistic + L2 (lambda grid from 1e-8)`, with all 20 inputs |
| Keep rule (agreed, DR-18) | margin ≥ 0.5 × spread: 0.0019 < 0.0053 | [I] | stop |
| §17 breadth note | 25 configurations compared (4 prior-kept, 21 post-prior); more than 10 | [I], p. 328 | the winner's CV score may be optimistic because many were compared on the same data; reported with the recommendation |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Keep rule | margin ≥ 0.5 × spread | 0.0019 vs 0.0053 |
| Breadth note | > 10 configurations | 25 |

**Round 1 candidates** (each is the leader with the named input dropped; the leader's CV mean accuracy is 0.9706; margins are paired over the 10 outer folds)

| Input dropped | CV mean accuracy | Margin vs leader | Spread |
| --- | --- | --- | --- |
| `wifi` | 0.9725 | +0.0019 | 0.0106 |
| `three_g` | 0.9706 | 0.0000 | 0.0078 |
| `touch_screen` | 0.9706 | 0.0000 | 0.0066 |
| `n_cores` | 0.9700 | −0.0006 | 0.0136 |
| `four_g` | 0.9700 | −0.0006 | 0.0069 |
| `pc` | 0.9694 | −0.0012 | 0.0071 |
| `sc_h` | 0.9694 | −0.0012 | 0.0071 |
| `dual_sim` | 0.9694 | −0.0013 | 0.0065 |
| `clock_speed` | 0.9688 | −0.0019 | 0.0030 |
| `fc` | 0.9688 | −0.0019 | 0.0066 |
| `sc_w` | 0.9688 | −0.0019 | 0.0098 |
| `blue` | 0.9687 | −0.0019 | 0.0118 |
| `int_memory` | 0.9681 | −0.0025 | 0.0089 |
| `m_dep` | 0.9681 | −0.0025 | 0.0053 |
| `talk_time` | 0.9681 | −0.0025 | 0.0053 |
| `mobile_wt` | 0.9606 | −0.0100 | 0.0103 |
| `px_height` | 0.9031 | −0.0675 | 0.0138 |
| `px_width` | 0.9025 | −0.0681 | 0.0146 |
| `battery_power` | 0.8062 | −0.1644 | 0.0198 |
| `ram` | 0.3175 | −0.6531 | 0.0309 |

These margins describe what the cross-validated model loses without each input, given the other 19. They are not a statement about how any specification is connected to price (ADM-2, DR-04).

- **Options considered:** the 20 single-input drops
- **Expectation:** n/a (this record fills in DR-18's *Outcome vs expectation*)
- **Decision:** No drop is kept. The leader stays `Logistic + L2 (lambda grid from 1e-8)` with all 20 inputs (DR-08). The 20 drop entries stay in the CV store as post-prior entries.
- **Open point for 4f:** §19.2–19.3 will see the `wifi`-dropped entry as the best CV mean (0.9725). It is within noise of the leader, and has the same structure and the same number of add-ons. §19's last tie-break is "the better CV mean", so the rule would pick the `wifi`-dropped entry, which the agreed keep rule has just declined to keep. This is raised with the user before `recommend` is run (`instructions.md`: the agent says so and raises it, and does not substitute its own result).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `run_cv` via `cv add "Logistic + L2" --drop <input> --grid … --label "… minus <input>"` (20 calls, driven by `Code/mobile_05_backward_elimination.py`); `margin` for the comparison · version: interim core, not reviewed, SHA-256 `d89e2275ffda2d958708f3dd410f3f39a8ef187a78a9df1d2416d51b00f91872` · output: `core_cv_post_prior_2.json` … `_21.json`, `core_cv_store.json`, `backward_elimination.json`, copied above unchanged (rounded to 4 decimals)

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Backward elimination" (DR-18)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile_05_backward_elimination.py`, `Code/outputs/mobile/backward_elimination.json`, `Code/outputs/mobile/core_cv_store.json`, DR-18

### DR-20 · DX · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Diagnosis pass 3 (§18) on the unchanged leader, `Logistic + L2 (lambda grid from 1e-8)`: which action is left, and does the loop stop?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Leader | unchanged since pass 2 (no drop kept, DR-19), so its observations are those of DR-18: O3 holds first (gap 0.0233 ≥ 2 × E_train 0.0061) | CV | `Code/outputs/mobile/core_diagnose_Logistic___L2__lambda_grid_from_1e_8_.json` |
| DX-4 parts | (a) add L2: not applicable (has L2); (b) remove polynomial terms: not applicable (none); (c) backward elimination: run in pass 2, nothing kept (DR-19); (d) ask whether more data is available: needs the user | — | DR-18, DR-19 |
| User's answer to (d) | "No; stop the loop" | M | user, 28 October 2026 |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1, O2, O5 | no | as DR-18 |
| **O3 overfitting** | **yes**, the first that holds | as DR-18 |
| O4, O6 | no | as DR-18 |

- **Action:** DX-4 part (d): the user was asked whether more labelled data is available. The answer was no.

**Stopping check**

- **S1 (criterion met):** not assessed until 4g.
- **S2 (achievable level):** unknown (DR-05).
- **S3 (two consecutive passes without a gain of ≥ 0.5 × spread):** pass 2 gave none (+0.0019 vs 0.0053); pass 3 adds no configuration.
- **S4 (out of scope):** no; no method outside the solution space is called for.
- **S5 (user stops it): applies.** "No; stop the loop."
- **S6 (five passes):** no (three passes).
- The loop stops under S5.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| as DR-18 | | |

- **Options considered:** put to the user without a recommendation: no more data, stop the loop (chosen); more data exists
- **Expectation:** n/a (no configuration action is taken)
- **Decision:** The diagnosis loop ends under S5 after three passes. 25 configurations have been compared, besides the baseline: the 4 kept by the prior, the λ-extended `Logistic + L2`, and 20 single-input drops of it. The leader is `Logistic + L2 (lambda grid from 1e-8)`. Next is 4f.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "No; stop the loop"
- **Supersedes / superseded by:** n/a
- **Links:** DR-18, DR-19

### DR-21 · FINAL · step 4

- **Sub-task:** 1 — Price band of a new phone
- **Date:** 2026-10-28
- **Question:** Which configuration does the recommendation rule (§19) choose, how confident is the selection (§17), and, once the user approves, how does it do on the test set?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV results | the CV entries of DR-15, DR-17 and DR-19 (same outer folds) | CV | `Code/outputs/mobile/core_cv_store.json` |
| Diagnosis | loop stopped under S5 after three passes | CV | DR-20 |
| Candidate set for §17/§19 | the 5 entries with the agreed input design (all 20 inputs). The 20 single-input drops count for the breadth note only (interpretation z) | M | user, 28 October 2026: "Agreed design only (Recommended)", chosen from three options: agreed design only; §19 as written; a `FRAMEWORK` change |
| Recommendation | `Logistic + L2`, λ tuned over {10⁻⁸ … 10⁴}. Final λ = 10⁻⁵, the most common setting (4 of 10 outer folds; interpretation s). All 20 inputs. No decision threshold (P6 = no): the predicted band is the one with the highest probability | CV | `Code/outputs/mobile/core_recommend.json` |
| CV mean accuracy | 0.9706 (fold SD 0.0141) | CV | same |
| Selection confidence | High: C1 clear (runner-up `Logistic + L2` with the original λ grid, margin 0.0069, spread 0.0055); C2 clear (margin over the baseline 0.7206, spread 0.0141); C3 adequate (E_val 80 % − 100 % = 0.0037 < 0.5 × 0.0141) | CV | same |
| Learning curve, E_val mean (fold SD) at 10 % … 100 % | 0.1825 (0.0712), 0.0944 (0.0279), 0.0644 (0.0250), 0.0537 (0.0274), 0.0444 (0.0229), 0.0375 (0.0164), 0.0375 (0.0161), 0.0331 (0.0144), 0.0269 (0.0132), 0.0294 (0.0141) | CV | same |
| Prior agreement | disagree: the CV winner among the prior-kept configurations is `Logistic + L2` (prior rank 3); the prior's rank 1 was shared by `kNN` and `Tree` | CV | same |
| Grounding | 0 matrix entries behind the recommendation's prior score (score 0) | — | same |
| Selection breadth | 25 configurations compared (5 with the agreed input design, 20 single-input drops); the note applies | — | same |
| Monitoring (§5.5 note), pooled outer-validation confusion matrix | rows (true 0–3): [391, 9, 0, 0], [8, 383, 9, 0], [0, 8, 383, 9], [0, 0, 4, 396]; recall per band 0.9775 / 0.9575 / 0.9575 / 0.9900 | CV | same |
| Uncertainty for 4g | SD of accuracy across the 10 outer folds for the recommended entry: 0.0141 `[B→I pp.71–73]` | CV | same |

**§19 trace**

1. **Eligible** (C2 = clear; no must-haves in DR-09; agreed input design only):
   - `Logistic + L2 (lambda grid from 1e-8)`: +0.7206 (spread 0.0141)
   - `Logistic + L2`: +0.7137 (0.0141)
   - `Logistic + poly + L2`: +0.6931 (0.0180)
   - `Tree`: +0.5781 (0.0288)
   - `kNN`: +0.3750 (0.0362)

   All five are eligible.
2. **Candidates** (the best CV mean, plus any within 0.5 × spread of it): `Logistic + L2 (lambda grid from 1e-8)` (0.9706) alone. The original `Logistic + L2` is 0.0069 behind with spread 0.0055, so it is not within noise.
3. **Choice:** `Logistic + L2 (lambda grid from 1e-8)`, the only candidate.
4. **Test once:** pending the user's approval (step 4g).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.1 eligible = C2 clear and every must-have met | all five agreed-design entries eligible | [I] (C2 threshold) | — |
| §19.2 candidates within the noise margin | one candidate | [I] threshold 0.5 × spread | — |
| §19.3 fewest add-ons, then prior score, then CV mean | not needed (single candidate) | [B p.332] | recommended |
| §17 C1, C2, C3 and the level rule | C1 clear, C2 clear, C3 adequate → High | [I]; C3 [B→I pp.334–336] + [I] | reported with its factors |
| Interpretation z (agreed input design only) | the 20 drop entries are not candidates | [I], at the user's choice | without it, §19.3's CV-mean tie-break would have picked the `wifi`-dropped entry (DR-19) |
| Final hyperparameters (interpretation s) | the most common setting across the outer folds | [I] | λ = 10⁻⁵ (4/10 folds) |
| Decision threshold | none (P6 = no) | [B→I pp.53–54] | highest-probability band |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C1 clear ≥ 1 × spread, moderate ≥ 0.5 × spread | 0.0055 / 0.0027 | 0.0069 → clear |
| C2 clear ≥ 1 × spread | 0.0141 | 0.7206 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0071 | 0.0037 |
| §19 within noise < 0.5 × spread | 0.0027 | 0.0069 (the original `Logistic + L2`) |
| Breadth note > 10 configurations | 10 | 25 |

**The agent's notes on these outputs** (raised, not substituted):
- **C1's runner-up is the same structural configuration** (`Logistic + L2`, with the original λ grid), so C1 here compares two λ grids rather than two configurations. Against the best different configuration, `Logistic + poly + L2`, the margin is 0.0275 with spread 0.0145, from the core's why-not evidence. That is also ≥ 1 × spread, so C1 would be clear either way, and the level would not change.
- **The final λ was chosen in 4 of 10 folds only.** The others chose 10⁻⁸ (2), 10⁻⁶ (3) and 10⁻⁷ (1). The final refit uses 10⁻⁵ (interpretation s).
- **The breadth note applies.** 25 entries were compared on the same folds, so the winner's CV score of 0.9706 may be optimistic (p. 328). The single test evaluation is what checks this (p. 74).

- **Options considered:** the five eligible agreed-design entries
- **Expectation:** DR-11 expected the two Logistic configurations to lead, which they do. No expectation about the choice or the confidence level was stated.
- **Decision:** Recommend `Logistic + L2` with λ = 10⁻⁵ on all 20 inputs, predicting the band with the highest probability. The selection confidence is High. The test set is used only after the user approves.

**Why not** (all 14 structural configurations except the recommendation)

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = multiclass [B pp.17, 49–57] (DR-10) |
| `Logistic` | EXCL | MOD-1: P9 = yes [B p.61] (DR-10) |
| `Logistic + poly` | EXCL | MOD-1: P9 = yes [B p.61] (DR-10) |
| `Logistic + poly + L2` | OUTP | margin 0.0275, spread 0.0145 (≥ 1 × spread) |
| `Tree` | OUTP | margin 0.1425, spread 0.0325 (≥ 1 × spread) |
| `kNN` | OUTP | margin 0.3456, spread 0.0340 (≥ 1 × spread) |

**Flags:** none. No evidence in the diagnosis loop pointed to a method outside the solution space.

**Reference code**

- Function: `recommend` (`cd Code && uv run python mobile/core.py recommend mobile/props_dr09.json`) · version: interim core, not reviewed, SHA-256 `b81c7f4302efc0235d05b7af832ff2c85a4ba00c1a2fce10c1a3f24ed8b49af0`. It differs from `d89e2275…` by interpretation z only, in `recommend`, so no earlier output is affected. The user saw the diff before it ran ("Run recommend") · inputs: DR-09 property values; the CV store · output: `Code/outputs/mobile/core_recommend.json`, copied above unchanged, rounded to 4 decimals. Run time about 15 minutes (learning curve).

**Test-set result** (step 4g, 28 October 2026, after the user's approval; used once)

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Approval | "continue", then confirmed: "Yes, evaluate once". Quoted on the command line and stored in the output | M | `Code/outputs/mobile/core_final.json` (`approved_by_user`) |
| Model evaluated | `Logistic + L2`, λ = 10⁻⁵, all 20 inputs, refitted on all 1,600 training phones; predicted band = highest probability | TEST | same |
| Test rows | 400 (100 per band) | TEST | same |
| Test accuracy (the estimate of E_new on the agreed metric) | 0.9600 (384 of 400) | TEST | same; recomputed independently: `Code/outputs/mobile/recompute_test_metric.txt` |
| Uncertainty | fold SD of accuracy across the 10 outer folds: 0.0141 `[B→I pp.71–73]`. Each outer fold holds 160 phones and the test set 400, so this approximates the uncertainty of the test result rather than measuring it | CV | `core_recommend.json` |
| Baseline on the same test rows | 0.2500 (band 0 for every phone; 100 of 400) | TEST | `core_final.json`; recomputed |
| Success criterion (DR-05) | test accuracy − fold SD = 0.9600 − 0.0141 = 0.9459 > 0.2500 → **met** | TEST | same |
| Confusion matrix, test (rows true band 0–3; columns predicted 0–3) | [99, 1, 0, 0], [2, 96, 2, 0], [0, 4, 92, 4], [0, 0, 3, 97] | TEST | same |
| Recall per band, test | 0 → 0.99, 1 → 0.96, 2 → 0.92, 3 → 0.97 | TEST | same |
| Misses by distance | 16 misses, all one band away; none two or three bands away | TEST | `recompute_test_metric.txt` |
| CV and test, side by side | CV mean 0.9706 (fold SD 0.0141) and test 0.9600; the difference, 0.0106, is smaller than one fold SD | CV / TEST | `core_recommend.json`, `core_final.json` |
| Independent recomputation | plain counting from the saved test predictions, with true bands read from `train.csv` by row number, and rows checked against `split.json` `test_idx`: accuracy, baseline and confusion matrix all equal to the core's | TEST | `Code/mobile_06_recompute_test_metric.py` → `recompute_test_metric.txt` ("agrees with core: True") |
| Precision–recall or ROC curve | not made: §5.5 gives these for binary problems; for a multiclass output the guide's note asks for the confusion matrix and per-band recall, reported above | — | ML Guide §5.5 |

The test set is not used again for this sub-task. The core's `final` refuses a second run while `core_final.json` exists.

- **Confidence:** High — C1 clear · C2 clear · C3 adequate — rule: High if C1 = clear, C2 = clear and C3 = adequate · prior agreement disagree · grounding [B] 0 / [B→I] 0 / [I] 0 · breadth note applies (25 compared)
- **Outcome vs expectation:** agree on the leading family (DR-11). No expectation was stated about the test result.
- **User involvement:** asked — §19 scope: "Agreed design only (Recommended)"; core change approved ("Run recommend"); test set: "continue", then confirmed "Yes, evaluate once"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/mobile/core.py` (`recommend`), `Code/outputs/mobile/core_recommend.json`, DR-10 to DR-20

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
| 11 | Step 2 closed: the user moved on to step 3 ("Mobile Price: step 3, explore and visualise the training data"). Three items listed at the close were not taken up: how the `Introduction` describes who uses the predictions; transforming inputs (settled in step 3, row 12); and a second sub-task. | — |
| 12 | Step 3, input design. Four options were offered (as recorded; log of RAM and storage; log(1 + x) of all size inputs; derived inputs), and the user chose "All as recorded (Recommended)". | DR-08 |
| 13 | Step 3. Interim core `Code/mobile/core.py` written (input design, §11 P9 and P10) and shown to the user before it ran ("Run it"). It ran on the 1,600 training phones: P9 = yes, P10 = balanced. A new PROP record supersedes DR-06, and notes that P3 = 20 sits exactly on its threshold. | `Code/mobile/core.py`, `Code/outputs/mobile/core_p9_p10.json`, DR-09 |
| 14 | Step 3, figures. Four were proposed and the user chose Figure 1 (distributions of the 14 numerical inputs) only. Two binning versions were replaced because of artefacts (see `Analysis`). Figure 1 was added to `Results` with a caption and a paragraph on how to read it. | `Code/mobile_03_fig1_input_distributions.py`, `Code/outputs/mobile/figures/fig1_input_distributions.png` (+ `dark/`), `Report.md` |
| 15 | Step 3 closed by the user. Three items listed at the close were not taken up: whether to keep Figure 1 as it stands; an expectation for P8 (it stays `unknown`); a figure of the six yes/no inputs. | — |
| 16 | Step 4a, sub-task 1. The user chose to add §9/§12 to the core now and §13–§19 at 4b. The extended core (SHA-256 `c7435f48…`) was shown and approved ("Run it"). Admissible: `Logistic + L2`, `Logistic + poly + L2`, `kNN`, `Tree`. The task gate removed the 8 Linear and GLM configurations; MOD-1 removed `Logistic` and `Logistic + poly`; MOD-2 did not apply. | `Code/mobile/core.py`, `Code/mobile/props_dr09.json`, `Code/outputs/mobile/core_admset.json`, DR-10 |
| 17 | Step 4b, sub-task 1. The core was extended with §13–§19 (SHA-256 `38e21eca…`; interpretations i–y), shown to the user before any output was used ("Run the prior"), and the prior ranking was run. All four admissible configurations score 0, and all are kept. The order comes from add-ons only: `kNN` = `Tree`, then `Logistic + L2` (simple-first), then `Logistic + poly + L2`. The expectation recorded is that the Logistic configurations lead, against the prior order. The method was presented and agreed ("Agree the method"). | `Code/mobile/core.py`, `Code/outputs/mobile/core_prior.json`, DR-11 |
| 18 | Step 4c, sub-task 1: round 1 run (42 s). Baseline mean CV accuracy 0.2500 (band 0 in every fold); `Logistic + L2` 0.9638 (fold SD 0.0141), with λ = 10⁻⁴ in 10/10 folds. Margin over the baseline 0.7138, spread 0.0141: C2 clear, so round 2 may proceed. λ at the grid edge is noted for 4e. | `Code/outputs/mobile/core_cv_round1.json`, `core_cv_store.json`, DR-12 |
| 19 | Step 4d, sub-task 1: round 2 run (1 min 49 s) on the same folds. Mean CV accuracy: `Logistic + poly + L2` 0.9431, `Tree` 0.8281, `kNN` 0.6250; all four clearly beat the baseline, and `Logistic + L2` (0.9638) leads by more than one spread over each. DR-11 *Outcome vs expectation* filled in: the CV order agrees with the advisor's expectation and disagrees with the prior order. Grid edges noted for 4e: λ = 10⁻⁴ for both Logistic configurations, k = 51 for `kNN` (10/10 folds each). | `Code/outputs/mobile/core_cv_round2.json`, `core_cv_store.json`, DR-11, DR-13 |
| 20 | Step 4e, pass 1. Diagnosis of `Logistic + L2` (2 min 23 s): O5 holds first (λ at the low edge in 10/10 folds), so DX-3 extends the λ grid down to 10⁻⁸; the expectation was written before the run (DR-14). The extended run then failed twice in the parallel worker pool (`WinError 6`, then `WinError 5`, `BrokenProcessPool`, in outer fold 0; nothing written). Single fits at small λ ran normally. The user chose "N_JOBS = 1, re-verify (Recommended)" over retrying unchanged or a threading wrapper. | DR-14 |
| 21 | Step 4e. Core changed: `N_JOBS = -1` → `1` (`38e21eca…` → `d89e2275…`). The CV store was rebuilt, and rounds 1–2 and the pass-1 diagnosis were re-run (6 min 19 s). `Code/mobile_04_compare_rerun.py` found every number identical to the committed outputs (0 differences in 4 files). DR-12, DR-13 and DR-14 are superseded by DR-15 and DR-16, with unchanged values. | `Code/mobile/core.py`, `Code/mobile_04_compare_rerun.py`, `Code/outputs/mobile/rerun_check.json`, DR-15, DR-16 |
| 22 | Step 4e, DX-3 run (33 s): `Logistic + L2` with λ ∈ {10⁻⁸ … 10⁴}, post-prior, scores 0.9706 (fold SD 0.0141), against 0.9638. The paired gain is +0.0069, spread 0.0055. λ ranges over 10⁻⁸ to 10⁻⁵ (10⁻⁸ in 2/10 folds). It is the new leader. DR-16 outcome vs expectation: partial (λ moved down as expected; the gain was larger than expected). | `Code/outputs/mobile/core_cv_post_prior_1.json`, DR-16, DR-17 |
| 23 | Step 4e, pass 2. Diagnosis of the new leader (15 min): O3 (overfitting) holds first, so DX-4 applies. Parts (a) and (b) do not apply. The user chose (c), backward elimination, from three options given without a recommendation; the keep rule is margin ≥ 0.5 × spread [I], and the expectation was written before the run (DR-18). | DR-18 |
| 24 | Step 4e, backward elimination round 1 (about 11 min, 20 post-prior entries). Best drop `wifi` (0.9725, +0.0019, spread 0.0106) misses the keep rule, so elimination stops and the leader keeps all 20 inputs. DR-18 outcome vs expectation: agree. 25 configurations have been compared, so the breadth note applies. Open point for 4f: §19's CV-mean tie-break would favour the not-kept `wifi` drop. | `Code/mobile_05_backward_elimination.py`, `Code/outputs/mobile/backward_elimination.json`, `core_cv_post_prior_2.json`–`_21.json`, DR-19 |
| 25 | Step 4e, pass 3. The leader is unchanged, so O3 and DX-4 remain; only part (d) is left. Asked whether more labelled data exists, the user chose "No; stop the loop". The loop ends under S5 after three passes, with 25 configurations compared. Step 4e is done. | DR-20 |
| 26 | Step 4f. The §19 tie-break point was raised before `recommend` ran, and the user chose "Agreed design only (Recommended)". The core gained interpretation z (`d89e2275…` → `b81c7f43…`, `recommend` only); the diff was shown and approved. `recommend` ran in about 15 min. Recommended: `Logistic + L2`, λ = 10⁻⁵ (4/10 folds), all 20 inputs, CV mean 0.9706 (fold SD 0.0141). Selection confidence High (C1, C2 clear; C3 adequate); prior agreement disagree; grounding 0 entries; breadth note applies (25). Why-not: 10 EXCL, 3 OUTP. | `Code/mobile/core.py`, `Code/outputs/mobile/core_recommend.json`, DR-21 |
| 27 | Step 4g. The user approved ("continue", confirmed "Yes, evaluate once"). The core's `final` refitted the recommended configuration on the 1,600 training phones and evaluated it once on the 400 test phones. Test accuracy 0.9600 (384/400) against a baseline of 0.2500, fold SD 0.0141, so the success criterion is met (0.9459 > 0.2500). All 16 misses are one band away. An independent recount from the saved predictions agrees exactly. `core_test_predictions.csv` holds row-level true bands, so it is kept out of git (`.gitignore`) under the unknown licence. | `Code/outputs/mobile/core_final.json`, `Code/mobile_06_recompute_test_metric.py`, `Code/outputs/mobile/recompute_test_metric.txt`, DR-21 |

## Code Summary

All scripts run from `Code/` with `uv run python <script>.py`. Script names start with `mobile_`, and outputs go to `Code/outputs/mobile/`, so that nothing collides with the Heart Failure or Sepsis files. Outputs are aggregates only, because the data's licence is unknown.

| File | What it does | Reads | Writes | Seeds / parameters |
| --- | --- | --- | --- | --- |
| `Code/mobile_01_describe_data.py` | Step 1 describing pass. Recomputes the SHA-256 of both files and checks them against `SOURCE.md`. Describes each column (meaning and unit from Kaggle's descriptions, range, percentiles, zeros, 0/1 counts). Counts duplicates, conflicting targets, class counts, row order and selected value combinations, and compares `test.csv` with `train.csv`. Draws no conclusions. | `Attachments/Mobile Price/train.csv`, `test.csv` | `Code/outputs/mobile/01_describe.json`, `01_describe.md` | none |
| `Code/mobile_02_split.py` | Step 2 split. Shuffled, stratified 80 / 20 split of `train.csv` by `price_range`. Records the row indices of each part, their class counts, the input design (categorical and numerical inputs) and P2–P4 with their `[I]` thresholds as named constants. After it runs, the test indices are locked until step 4g. | `Attachments/Mobile Price/train.csv` | `Code/outputs/mobile/split.json` (indices and counts, no data values) | `SEED = 2026`, `TEST_FRACTION = 0.2` |
| `Code/mobile/core.py` | **Interim core, not reviewed** (the version is its SHA-256, quoted in the Decision Records). So far it holds the input design of DR-08 (`preprocessor`: 14 numerical inputs passed through, six 0/1 indicators one-hot encoded with one level dropped), the training-data reader (`training_data`: the 1,600 `train_idx` rows only, with an assertion that no test row is kept), §11 P9 and P10 (`p9_p10`). From step 4a it adds §9 and §12: the 14 configurations, the task gate, the must-have gates, MOD-1 and MOD-2 (`admissible_set`, `mod2_check`). From step 4b it adds the rest: §13–§15 prior ranking (`prior_ranking`); §16 nested CV with a cumulative store (`run_cv`, `nested_cv`, `baseline_cv`, `cv_table`; pooled confusion matrices and recall per band); §18 observations and the learning curve (`observations`, `learning_curve`); §17/§19/§20 recommendation, confidence and why-not codes (`recommend`); and §19.4 the single test evaluation (`final`), the only function that reads the test rows. `final` needs the user's approval on the command line, and refuses a second run or a changed core. The header lists interpretations a–y. Commands: `p9p10`; `admset`, `prior`, `cv round1`, `cv round2` and `recommend`, each with `mobile/props_dr09.json`; `cv add "<configuration>" [--drop COL] [--grid JSON] [--label TEXT]`; `diagnose "<entry>"`; `final --approved "<words>"`. | `Attachments/Mobile Price/train.csv`, `Code/outputs/mobile/split.json`, `Code/mobile/props_dr09.json` (the DR-09 property values) | `Code/outputs/mobile/core_p9_p10.json`, `core_admset.json`, `core_prior.json`. Later: `core_cv_store.json`, `core_cv_round1.json`, `core_cv_round2.json`, `core_cv_post_prior_N.json`, `core_diagnose_*.json`, `core_recommend.json`, `core_final.json`, `core_test_predictions.csv` | `[I]` constants as named in the file: `P9_SEPARABLE_ACCURACY = 1.0`, `P9_NEGLIGIBLE_C = 1e8`, `P10_IMBALANCED_SHARE = 0.20`, `KEEP_TOP_OTHERS = 3`, `OUTER_FOLDS = 10`, `INNER_FOLDS = 5`, `C1_CLEAR = 1.0`, `C1_MODERATE = 0.5`, `C2_CLEAR = 1.0`, `C3_FALLING = 0.5`, `WITHIN_NOISE = 0.5`, `BREADTH_MANY = 10`, `O3_RATIO = O4_RATIO = 2.0`, `O5_MOST_FOLDS = 0.5`; grids `GRID_DEGREE`, `GRID_K`, `GRID_DEPTH`, `GRID_MIN_LEAF`, `GRID_LAMBDA` (§16); `CV_SEED = 2026`; `LOGISTIC_MAX_ITER = 100000` |
| `Code/mobile_04_compare_rerun.py` | Step 4e check after the core change `N_JOBS = -1` → `1`. Compares every value of the re-run outputs (`core_cv_round1.json`, `core_cv_round2.json`, `core_cv_store.json`, `core_diagnose_Logistic___L2.json`) with the earlier core's committed outputs (from git, commit `a1b8fa7`) and the saved earlier diagnosis. Fields naming the code version or the printed pipeline are skipped, and floats must match exactly. | the outputs above; the old diagnosis file (path as argument) | `Code/outputs/mobile/rerun_check.json` | `OLD_COMMIT = "a1b8fa7"` |
| `Code/mobile_05_backward_elimination.py` | Step 4e, DX-4 (c). Backward elimination driven through the core's `cv add --drop` entry point. Each round cross-validates the current leader with each remaining input also dropped, and keeps the best drop only if its paired margin over the leader is ≥ `KEEP_MARGIN` × spread (the core's `margin`). Otherwise it stops. It fits nothing itself. | the CV store, via the core | post-prior entries via the core; `Code/outputs/mobile/backward_elimination.json` | `KEEP_MARGIN = 0.5` [I]; the λ grid {10⁻⁸ … 10⁴}; start = `Logistic + L2 (lambda grid from 1e-8)` |
| `Code/mobile_06_recompute_test_metric.py` | Step 4g second route to the test result. Plain counting, without scikit-learn, of accuracy, the baseline, the confusion matrix and the miss distances, from the saved predictions. True bands are read from `train.csv` by row number, and the rows are checked against `split.json`. The result is compared with `core_final.json`. | `Code/outputs/mobile/core_test_predictions.csv` (not in git: row-level labels), `train.csv`, `split.json`, `core_final.json` | `Code/outputs/mobile/recompute_test_metric.txt` | none |
| `Code/mobile_03_fig1_input_distributions.py` | Figure 1: one panel per numerical input, all bands together. One bar per value for inputs with up to 130 distinct values; 40 equal-width bins from min − 0.5 to max + 0.5 for the rest. Light and dark versions. Uses `viz_style.py`, with `FIGURES` set to the Mobile Price folder. | the training phones, via `core.training_data()` | `Code/outputs/mobile/figures/fig1_input_distributions.png`, `dark/fig1_input_distributions.png`, `fig1_input_distributions.json` (per panel: phones, distinct values, min, max, zeros, bars) | `BINS = 40`, `DISCRETE_MAX = 130`, `FIGSIZE = (16, 14)` |

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published). Read at smlbook.org; the link was checked on 28 October 2026. Page references in the Decision Records come from `ML Guide.md`.
- Sharma, A. (2018). *Mobile Price Classification* [Dataset], version 1. Kaggle. [https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification). The creator, title, version and date (28 January 2018) are from Kaggle's API metadata, checked 28 October 2026. Licence: "Unknown".
