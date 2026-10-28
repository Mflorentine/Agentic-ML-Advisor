# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

*Step 1, closed 28 October 2026. All figures are from `Code/outputs/hf2/01_describe.json`. The decisions taken in step 1 are under* Step 1 decisions *at the end of this section.*

**This is a rerun, and that is a limitation.**
- The same data were analysed before in `Demonstration/Heart Failure/` (steps 1–5, finished), and its data, decisions and results are known to the user and to the advisor.
- This rerun works through the steps afresh with the method as it stands now (`instructions.md` and `ML Guide.md` at 28 October 2026). Every decision is put to the user as options, and no decision is copied from the earlier Appendix.
- Prior knowledge cannot be undone, though. Choices in this rerun, such as the problem, the inputs and the metric, may be influenced by what the earlier analysis found, and the earlier test result has already been seen. Whether this rerun's test set is the same as the earlier one is a step 2 decision. If it is, its rows have already informed the earlier analysis's evaluation, though not this rerun's choices.
- The earlier analysis is the reference and is not edited. Its scripts (`Code/01_…08_*.py`), core (`Code/core.py`) and outputs are not changed by this rerun. One exception to "not read" follows from a step 2 decision: the row indices of its split (`Code/outputs/split.json`) are read, because the user chose to reuse its test set (DR-07). This rerun's files are named `Code/hf2_*`, `Code/hf2/core.py` and `Code/outputs/hf2/`.

**Provenance.**
- **File:** `Attachments/heart_failure_clinical_records_dataset.csv`, from the UCI Machine Learning Repository, *Heart Failure Clinical Records* (dataset 519; donated 4 February 2020). It was downloaded on 14 October 2026 by the user (`Attachments/SOURCE.md`). Never modified.
- **Checksum:** SHA-256 `9c73cea7468ff5d517801ec050fe9993da5912fce4b56f296f8df3b38dd75912`; 12,239 bytes; ASCII; LF line endings. The describing script recomputed it, and it matches `Attachments/SOURCE.md`.
- **Licence:** CC BY 4.0, as stated on the UCI page, so the file is committed.
- **Who the patients are** (Chicco and Jurman, 2020, *Dataset* section, read 28 October 2026 from the open-access full text):
  - "299 heart failure patients collected at the Faisalabad Institute of Cardiology and at the Allied Hospital in Faisalabad (Punjab, Pakistan), during April–December 2015";
  - 105 women and 194 men, aged 40 to 95;
  - "All 299 patients had left ventricular systolic dysfunction and had previous heart failures that put them in classes III or IV of New York Heart Association (NYHA) classification";
  - "the follow-up period … was 130 days on average";
  - "The hospital physician considered a patient having anaemia if haematocrit levels were lower than 36%";
  - "the original dataset manuscript provides no definition of high blood pressure", and "provides no additional information about what type of follow-up was carried out".

**Best available form: checked.**
- The data were first published with Ahmad et al. (2017), *PLoS ONE*, as `S1 Data.csv` on figshare (article 5227684, version 1, 20 July 2017, CC BY 4.0, titled "DATA_MINIMAL"). The figshare record lists one version.
- That original file (12,486 bytes; SHA-256 `e00ec2fd…74cdfe`) was downloaded on 28 October 2026 into a temporary folder outside the workspace, compared, and deleted.
- Its 299 rows are identical to the 299 rows of the UCI file, value for value, once its column names are mapped (`TIME`, `Event`, `Gender`, `BP`, `Pletelets`, …). The UCI copy differs only in column names and row order: it is sorted by `time`, and the original is not.
- No fuller release was found. The UCI file is therefore as complete as the original, and is used.

**Shape and coverage.**
- 299 rows (one per patient) × 13 columns: 12 inputs and `DEATH_EVENT`.
- No missing cells, no duplicate rows, and no two rows with identical inputs.
- **Row order:** sorted by `time`, ascending.
- **Grouping:** there is no patient identifier or date column.

**Columns.** Meanings, units and types are from the UCI page's variable table (UCI API, fetched 28 October 2026); the range column is Chicco and Jurman (2020), Table 1. All 12 inputs are recorded clinical measurements or attributes; none is described as a model output.

| Column | Meaning (UCI) | Unit (UCI) | UCI type | Range (paper) | Distinct | Min | 1st pct | Median | 99th pct | Max | 0 / 1 counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `age` | age of the patient | years | Integer | 40–95 | 47 | 40 | 40 | 60 | 90.08 | 95 | — |
| `anaemia` | decrease of red blood cells or hemoglobin | boolean | Binary | 0, 1 | 2 | 0 | 0 | 0 | 1 | 1 | 170 / 129 |
| `creatinine_phosphokinase` | level of the CPK enzyme in the blood | mcg/L | Integer | 23–7,861 | 208 | 23 | 47 | 250 | 5,222.46 | 7,861 | — |
| `diabetes` | if the patient has diabetes | boolean | Binary | 0, 1 | 2 | 0 | 0 | 0 | 1 | 1 | 174 / 125 |
| `ejection_fraction` | percentage of blood leaving the heart at each contraction | % | Integer | 14–80 | 17 | 14 | 16.96 | 38 | 62.06 | 80 | — |
| `high_blood_pressure` | if the patient has hypertension | boolean | Binary | 0, 1 | 2 | 0 | 0 | 0 | 1 | 1 | 194 / 105 |
| `platelets` | platelets in the blood | kiloplatelets/mL | Continuous | 25.01–850.00 | 176 | 25,100 | 61,780 | 262,000 | 544,560 | 850,000 | — |
| `serum_creatinine` | level of serum creatinine in the blood | mg/dL | Continuous | 0.50–9.40 | 40 | 0.5 | 0.6 | 1.1 | 6.114 | 9.4 | — |
| `serum_sodium` | level of serum sodium in the blood | mEq/L | Integer | 114–148 | 27 | 113 | 123.94 | 137 | 145 | 148 | — |
| `sex` | woman or man | binary | Binary | 0, 1 | 2 | 0 | 0 | 1 | 1 | 1 | 105 / 194 |
| `smoking` | if the patient smokes or not | boolean | Binary | 0, 1 | 2 | 0 | 0 | 0 | 1 | 1 | 203 / 96 |
| `time` | follow-up period | days | Integer | 4–285 | 148 | 4 | 7 | 115 | 271.14 | 285 | — |
| `DEATH_EVENT` | if the patient died during the follow-up period (UCI role: Target) | boolean | Binary | 0, 1 | 2 | 0 | 0 | 0 | 1 | 1 | 203 / 96 |

**Values counted.** The decisions on these are under *Step 1 decisions*.
- `platelets` runs from 25,100 to 850,000 in the file. The paper's Table 1 gives 25.01 to 850.00 under the same unit (kiloplatelets/mL), a factor of 1,000 apart.
- `serum_sodium` has a minimum of 113; the paper's range starts at 114.
- `age` is a whole number except in 2 rows (60.667 both).
- `sex` is 0/1, and the documentation does not say which value is a woman.

**Machine learning checks (described, not judged).**
- **Candidate target:** `DEATH_EVENT`, the UCI page's target and the paper's.
  - It is present for all 299 rows: 203 × 0 and 96 × 1 (32.11 %).
  - It records whether the patient died during the follow-up period, and that period varies by patient (`time`).
  - The documentation does not say how follow-up ended for patients without a death: whether at a fixed end date or by loss to follow-up.
- **Output type it suggests (P1, to be confirmed in step 2):** binary.
- **Class counts:** 203 (0) and 96 (1).
- **Inputs (P3, P4), with all 12 non-target columns counted:**
  - five are 0/1 (`anaemia`, `diabetes`, `high_blood_pressure`, `sex`, `smoking`);
  - seven are numerical;
  - one-hot encoding leaves 12 columns, with a categorical share of 5 / 12 = 42 %.

  Which columns are inputs is a step 1–2 decision, so these counts may change.
- **Columns that could leak the target:** `time`, the follow-up period. It is known only when follow-up ends, which for a patient who died is the time of death. Its median is 44.5 days for patients with `DEATH_EVENT` = 1 and 172 days for those with 0 (minimum 4 and 12). No other column is documented as recorded after the outcome.

**Step 1 decisions.**

| Decision | What was decided, and why | What it costs |
| --- | --- | --- |
| **Provenance** | The UCI file, checksum verified. It holds the same 299 rows as the original 2017 release (figshare), which was compared value by value; only the column names and row order differ. There is no fuller version. | — |
| **Rerun** | The data and the earlier analysis's results were already seen by the user and the advisor (see the top of this section). Every decision here is taken afresh as options, and none is copied from the earlier Appendix. | Choices may still be shaped by what the earlier analysis found; this is recorded as a limitation of the rerun. |
| **Scope** | All 299 rows. No row is excluded. | — |
| **Units** | Units as on the UCI page. `platelets` is used as recorded, and its unit is uncertain: the UCI label is kiloplatelets/mL, while the paper's Table 1 range is 1,000 times smaller than the file's values. The user chose "As recorded (Recommended)". | Any statement about platelets in physical units would need the unit settled; a fixed scale factor does not change standardised or tree models. |
| **Missing data** | None: there are no empty cells. | — |
| **Cleaning** | No value altered or set to missing. | — |
| **Accepted as-is** | **`serum_sodium` = 113 mEq/L in 1 row**, one below the paper's stated minimum of 114. It is a possible low clinical value; the user chose "Accept as-is (Recommended)". **`age` = 60.667 in 2 rows**, the only non-integer ages; the user chose "Accept as-is (Recommended)". | If either is an error, it is in the data the models learn from. |
| **Grouping and time order** | None (ADM-3, DR-02). One row per patient; the file is sorted by `time`, which is follow-up length, not calendar order. Rows are treated as independent; split and folds are shuffled. | The two hospitals are not identified in the file, so a split by hospital is not possible. |
| **Admissibility** | ADM-1 yes (DR-01), ADM-3 none (DR-02), ADM-4 yes (DR-03). | — |
| **Target and leakage** | Candidate target: `DEATH_EVENT` (203 × 0, 96 × 1), death during a follow-up period of varying length. **`time` is set aside** and is not an input. It is known only when follow-up ends, which for patients who died is the time of death, so it would not be available for a new patient at the time of prediction. The user chose "Set aside (Recommended)" over keeping it as an input. It stays in the file. | Inputs: 11 (5 binary and 6 numerical); after encoding 11 columns, categorical share 5 / 11 = 45 %. How follow-up ended for patients without a death is undocumented, so a 0 means "no death observed during follow-up", not "survived" in every case. |
| **Experience level** | The user chose "New to ML" (28 October 2026). | — |

## Problem Definition

*Step 2, written 28 October 2026, before anything was trained. It works from the column meanings, the `Data Summary` and row counts only. No model has been fitted, and no relationship between inputs and outcome has been looked at in this rerun.*

### Discussion

**How the problem was arrived at.** The user asked the advisor to suggest a problem. Three candidates were offered, from the column meanings:
- (a) **Death during follow-up:** predict `DEATH_EVENT` from the 11 clinical inputs.
- (b) **Death within a fixed time** (for example 90 days), using `time` only to define the label.
- (c) **Ejection fraction:** a regression on a measurement.

The user chose (a), "Death during follow-up". (b) was not taken: patients without a death followed for less than the fixed time have no known outcome. (c) was not taken: it is not the outcome the data were collected for.

**Prediction, not understanding (ADM-2, DR-04).** The user chose "Predict".

**What a mistake costs.** Suppose the prediction is used to flag patients at higher risk when follow-up starts. The user chose "Missing a death is worse" over "Both about equal" and "False alarm is worse".

**The metric.** The user chose "PR-AUC (Recommended)": the area under the precision–recall curve (p. 92), computed as average precision `[I]`. It is threshold-free, so model selection does not depend on a threshold, and §16 tunes a threshold only after selection. Alongside it, F2, precision and recall are monitored at a threshold tuned on the training data. F2 weighs recall twice as heavily as precision (p. 92). Two alternatives were offered and not taken:
- F2 at the default threshold 0.5 during selection;
- ROC-AUC, which the book ranks below the precision–recall curve when positives are the minority (p. 92).

**Success and achievable level.**
- The user chose "Above no-skill beyond noise": test PR-AUC minus its uncertainty above the test set's share of deaths. Fixed bars of 0.60 and 0.75 were not taken.
- The achievable level is "Unknown". The results of Chicco and Jurman (2020) were offered as a reference and not taken: they use other metrics, partly other inputs, and could anchor the work.

**Requirements and expectations.**
- P5: "Not needed".
- P6: "Yes, nice to have", with a threshold tuned after selection and the trade-off chosen by the user.
- P7: "No".
- P8: "I have no expectation", so `unknown`.
- No must-haves.

**The split (DR-07).** The user chose "Same test set as before" over "New split": the earlier analysis's 60 test patients are reused, so that the old and new methods are compared on the same patients.
- *Limitation:* those 60 patients already produced the earlier test result, which the user and the advisor have both seen. The test set is untouched by this rerun's choices, but not by our knowledge.

**Feasibility.**
- *Is the output recorded well enough?* It is recorded for all rows; a 0 means "no death observed during follow-up" (DR-01).
- *Are there enough rows?* 239 training patients for 11 input columns: a ratio of 19.9 (P2 = ample).
- *Do grouping or time order constrain the split?* No groups (DR-02).
- *Is the problem answerable within the scope?* Binary classification is covered by chapters 2 and 3.

### Problem

Agreed 28 October 2026 (DR-05, DR-06). Counts are from `Code/outputs/hf2/split.json`.

| Item | Agreed |
| --- | --- |
| **Rows** | All 299 patients, one row each. |
| **Output y** | `DEATH_EVENT`: 1 if the patient died during the follow-up period, 0 otherwise (no death observed). 96 of 299 are 1 (32.11 %). |
| **Inputs x** | The 11 clinical columns: `age`, `anaemia`, `creatinine_phosphokinase`, `diabetes`, `ejection_fraction`, `high_blood_pressure`, `platelets`, `serum_creatinine`, `serum_sodium`, `sex`, `smoking`. Five are 0/1 indicators; six are numerical. `time` is not an input (step 1). Any transformation is decided in step 3. |
| **Output type (P1)** | Binary. |
| **What a prediction is for** | Flagging patients at higher risk of death when follow-up starts. Missing a death costs more than a false alarm. |
| **Deciding metric** | PR-AUC, computed as average precision `[I]`. |
| **Monitored alongside** | F2 (β = 2), precision and recall at a decision threshold tuned on the training data after selection (§16). |
| **Baseline** | The most common training class: flag nobody (pp. 330–331). Its scores are constant, so its PR-AUC equals the share of deaths, the no-skill level (p. 92): 77 / 239 = 0.3222 in training, and 19 / 60 = 0.3167 in the test set. |
| **Success criterion** | Test PR-AUC minus its uncertainty above the test set's share of deaths (0.3167). The uncertainty is the SD of PR-AUC across the 10 outer folds (step 4g) `[B→I pp.71–73]`. |
| **Achievable level** | Unknown. |
| **P5** | None (not needed). |
| **P6** | Yes, not a must-have: a tuned threshold, with the trade-off chosen by the user. |
| **P7** | No. |
| **P8** | Unknown: "I have no expectation". |
| **Split** | The earlier analysis's split, reused: 20 % test, shuffled, stratified by `DEATH_EVENT`, seed 2026. 239 training patients (77 deaths) and 60 test patients (19 deaths). Cross-validation folds are stratified by `DEATH_EVENT`. The test set is locked (DR-07, `Code/outputs/hf2/split.json`). |

### Sub-tasks

1. **Death during follow-up.** Predict, from the 11 clinical inputs, whether a patient dies during the follow-up period. Success: test PR-AUC minus its uncertainty above the test set's share of deaths.

## Analysis

### Sub-task 1 — Death during follow-up

**Step 3: training data only (239 patients).** Nothing in this step read the 60 test rows. `Code/hf2/core.py` `training_data()` keeps only `train_idx` from `Code/outputs/hf2/split.json` and asserts that no test index is kept. Every figure script reads the data through it.

- **Input design (DR-08):** all 11 inputs as recorded. The natural log of `creatinine_phosphokinase` and `serum_creatinine`, and the log of those two plus `platelets`, were offered without a recommendation and not taken.
- **P9 and P10 (DR-09)** were computed by `Code/hf2/core.py` (SHA-256 `2e4b01c3…6e85789f`) after the user had seen the script.
  - P9 = no: logistic regression with C = 1e8 classifies 184 of 239 training patients correctly.
  - P10 = balanced: 77 deaths of 239 (32.2 %).
  - The P9 fit is not a candidate model, and its result is not interpreted.
- **Figures:** four were proposed and the user chose all four. The yes/no input counts figure was later dropped from `Results` (Analysis Log row 15). Colours by variable: green for all training patients (Figure 1 and the dropped counts figure); blue for no death and orange for died (Figure 2); orange shades for the share who died by 0/1 value (Figure 3); grey for the overall share.
- **One revision before the figures entered the report:**
  - In Figures 1 and 2 the platelet axis printed in scientific notation ("2e+05"); it now prints plain numbers for values of 10,000 and above.
  - In Figure 3 the label of the overall-share line overlapped the smoking bars; the line is now named in the legend.
  - Output sizes, which the tight bounding box did not enlarge: Figure 1 3,030 × 1,765; Figure 2 3,031 × 1,863; Figure 3 2,632 × 1,374; the dropped counts figure 2,433 × 1,179 pixels.
- **Counts behind the figures, training patients only** (`Code/outputs/hf2/figures/*.json`):
  - medians by outcome (no death / died): age 60 / 65; ejection fraction 38 / 30; serum creatinine 1.0 / 1.3; serum sodium 137 / 135; creatinine phosphokinase 246.5 / 258; platelets 258,000 / 244,000;
  - share who died by 0/1 value: anaemia 0.28 / 0.38; diabetes 0.32 / 0.32; high blood pressure 0.29 / 0.39; sex 0.34 / 0.31; smoking 0.33 / 0.31.

  These are recorded as counts, not findings (P8 stays unknown).

**Step 5: derived comparisons, from numbers already reported** (no test row read, no model fitted)

- **F2 of flagging every patient.** If every patient is flagged, recall is 1 and precision is the share of deaths p, so F2 = 5p / (4p + 1) (F_β with β = 2, p. 92). This follows from the share of deaths alone.
  - Test set: p = 19 / 60 = 0.3167, so F2 = 0.6985.
  - Training patients: p = 77 / 239 = 0.3222, so F2 = 0.7038.
- **Against it, the recommended model at its threshold r = 0.10:**
  - test F2 0.6400 (DR-17; 49 of 60 flagged), which is 0.0585 below flagging everyone on the same patients;
  - nested CV F2 0.7127 (SD 0.0614), which is 0.0089 above the training figure (0.7038).
- **The model's ranking, threshold-free:** test PR-AUC 0.6983, against 0.3167 for flagging nobody (DR-17).
- **The flag-everyone F2 is not part of the agreed formulation.** The deciding metric is PR-AUC, and F2 is monitored at the tuned threshold (DR-05). It is recorded as context for reading the F2 figures.
- **The earlier analysis on the same 60 test patients.** Demonstration/Heart Failure/Demonstration Appendix.md, DR-19 (FINAL): the recommended `Tree` (depth 3, minimum leaf 20) at threshold r = 0.2 had test F2 0.6780 (recall 0.8421, precision 0.3810; tn 15, fp 26, fn 3, tp 16). That analysis decided on F2 rather than PR-AUC, and its success criterion was not met. The two analyses agreed different metrics and success criteria, so their results are recorded side by side, not ranked. The full comparison is left to the Project Report.

## Decision Records

### DR-01 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-28
- **Question:** Is there a recorded output y for the rows to be learned from (ADM-1)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `DEATH_EVENT` | present for all 299 rows: 203 × 0, 96 × 1 | M | `Code/outputs/hf2/01_describe.json` |
| What it records | "if the patient died during the follow-up period" (UCI role: Target); follow-up length varies by patient (`time`), and how follow-up ended for patients without a death is undocumented | M | UCI variable table; Chicco and Jurman (2020), *Dataset* |
| User's answer | "Yes" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-1 | yes | [B p.15] | supervised problem; continue |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** continue with `DEATH_EVENT` · stop
- **Expectation:** n/a
- **Decision:** `DEATH_EVENT` is the recorded output, so the work continues. A 0 means that no death was observed during a follow-up of varying, undocumented end, and this is recorded as a limitation of the labels.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Yes"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/hf2_01_describe_data.py`, `Code/outputs/hf2/01_describe.md`

### DR-02 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-28
- **Question:** Do several rows belong to the same unit, or are rows ordered in time (ADM-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Group or time column | none: no patient identifier, hospital or date column; one row per patient (299) | M | `Code/outputs/hf2/01_describe.json`; Chicco and Jurman (2020) |
| Row order | sorted by `time` (follow-up length), not by calendar date; the original 2017 release is not sorted | M | `01_describe.json`; comparison with the figshare file (Data Summary) |
| User's answer | "Neither" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-3 | none | [B pp.16, 38–39, 329] | random split, shuffled because the file is sorted (pp. 71, 73); stratified folds for classification (§16) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** none · grouped (no column to group by) · ordered in time (no calendar column) · unknown
- **Expectation:** n/a
- **Decision:** The rows are treated as independent patients. The split and folds are random and shuffled; stratification is settled with the split in step 2.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Neither"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/hf2/01_describe.json`

### DR-03 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-28
- **Question:** Will the cases the model is used on look like the data we have (ADM-4)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Who the patients are | 299 patients with left ventricular systolic dysfunction, NYHA class III–IV, at two hospitals in Faisalabad, Pakistan, April–December 2015; aged 40–95; 105 women, 194 men | M | Chicco and Jurman (2020), *Dataset* |
| User's answer | "Yes" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-4 | yes | [B pp.328–329] | validation and test data both come from this file |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** yes · no · unsure
- **Expectation:** n/a
- **Decision:** New patients are taken to look like these, so validation and test data are drawn from this file. Any estimate of performance holds only for patients like these: NYHA III–IV, from the same setting and period.

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
| Problem chosen | "Death during follow-up": predict `DEATH_EVENT` from the 11 clinical inputs | M | user, 28 October 2026 (selected option) |
| User's answer | "Predict" | M | user, 28 October 2026 (selected option) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-2 | predict | [B p.20] | continue |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** predict · understand
- **Expectation:** n/a
- **Decision:** The aim is to predict death during follow-up for new patients. No claim is made about how the measurements are connected to death.

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

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** What is predicted, from what, and how is success judged?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| y | `DEATH_EVENT`, binary; 96 of 299 are 1 | M | `Code/outputs/hf2/01_describe.json` |
| x | 11 clinical inputs (5 indicators, 6 numerical); `time` set aside (step 1) | M | Data Summary; `Code/outputs/hf2/split.json` |
| Error costs | missing a death is worse than a false alarm | M | user, 28 October 2026: "Missing a death is worse" |
| Deciding metric | PR-AUC (average precision); F2, precision and recall monitored at a tuned threshold | M | user, 28 October 2026: "PR-AUC (Recommended)" |
| Success criterion | test PR-AUC − fold SD > test share of deaths | M | user, 28 October 2026: "Above no-skill beyond noise" |
| Baseline | flag nobody: PR-AUC = share of deaths (training 0.3222; test 0.3167) | M | `Code/outputs/hf2/split.json` |
| Achievable level | unknown | M | user: "Unknown" |
| P5 · P6 · P7 · P8 | none · yes (not a must-have) · no · unknown | M | user: "Not needed", "Yes, nice to have", "No", "I have no expectation" |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| One metric, agreed up front | PR-AUC | [B p.330] | decides between models; others monitored |
| Imbalanced or asymmetric problems need more than the misclassification rate | missing a death is worse | [B p.91] | accuracy not used |
| Precision–recall curve preferred to ROC when positives are the minority | PR-AUC | [B p.92] | ROC-AUC not used |
| F_β weights recall β times as heavily as precision | β = 2, monitored | [B p.92] | F2 at the tuned threshold |
| PR-AUC computed as average precision | chosen | UNLISTED [I] — "the book draws the precision–recall curve and its area (p. 92) but not how the area is computed" | `average_precision_score` |
| SEQ-1 | baseline = most common training class (flag nobody) | [B pp.330–331] | always cross-validated and reported |
| Uncertainty of the test result | SD of PR-AUC across the 10 outer folds | [B→I pp.71–73] | used in the success criterion |
| Threshold tuned only after selection, trade-off chosen by the user (P6 = yes) | applies | [B→I pp.53–54, 92–93] | at 4f |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** problems: death during follow-up, death within a fixed time, ejection fraction; error costs: missing a death worse, equal, false alarm worse; metric: PR-AUC, F2 at 0.5, ROC-AUC; success: above no-skill beyond noise, ≥ 0.60, ≥ 0.75; achievable level: unknown, from the literature
- **Expectation:** n/a
- **Decision:** Predict `DEATH_EVENT` from the 11 clinical inputs, decided by PR-AUC against the no-skill baseline. Success is test PR-AUC minus its outer-fold SD above the test share of deaths. A threshold for F2 is tuned after selection.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/hf2/split.json`

### DR-06 · PROP · step 2

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** What are the property values P1–P8, before any training?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 output type | binary | M | DR-05 |
| P2 data-to-parameter ratio | ample (239 ÷ (11 + 1) = 19.92) | M | `Code/outputs/hf2/split.json` |
| P3 number of inputs | few (11 columns after encoding) | M | same |
| P4 share of categorical inputs | low (5 ÷ 11 = 45 %) | M | same |
| P5 interpretability | none | M | user: "Not needed" |
| P6 probabilities or threshold | yes, not a must-have | M | user: "Yes, nice to have" |
| P7 beyond training range | no | M | user: "No" |
| P8 expected shape | unknown | M | user: "I have no expectation" |
| P9, P10 | not yet computed (training data, step 3) | n/a | — |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P2 | ample | [I] | no P2 entry in the matrix |
| P3 | few | [I] | no P3 entry |
| P4 | low | [I] | no P4 entry |
| P6 = yes (not a must-have) | applies | [B→I pp.50, 53–54] | +1 on Logistic in the prior (§13) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 19.92 |
| P3 many inputs | > 20 | 11 |
| P4 high categorical share | ≥ 50 % | 45 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** P1 binary · P2 ample · P3 few · P4 low · P5 none · P6 yes (not a must-have) · P7 no · P8 unknown. P9 and P10 follow in step 3.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** superseded by DR-09 (P9 and P10 added in step 3; P1–P8 unchanged)
- **Links:** `Code/hf2_02_split.py`, `Code/outputs/hf2/split.json`

### DR-07 · SPLIT · step 2

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** Which training/test split is used, and is the test set locked?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Grouping or time order | none | M | DR-02 |
| User's choice | "Same test set as before", over "New split" | M | user, 28 October 2026 |
| Source of the split | the earlier analysis's `Code/outputs/split.json` (commit 5338393): 20 % test, shuffled, stratified by `DEATH_EVENT`, seed 2026. Its source checksum and settings were checked, and its indices form a partition of the 299 rows. Read only, not changed | M | `Code/hf2_02_split.py` |
| Result | 239 training patients (162 × 0, 77 × 1); 60 test patients (41 × 0, 19 × 1), recomputed from the data | M | `Code/outputs/hf2/split.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Split randomly (shuffle; the file is sorted by `time`) | the reused split was shuffled | [B pp.71, 73] | — |
| Size with about this much data | test set plus k-fold CV on the rest | [B pp.329–330] | 20 % held out; outer 10-fold CV on the 239 |
| ADM-3 = none | random split by row | [B p.329] | — |
| Stratified folds for classification | stratified by `DEATH_EVENT` | [I] | folds keep the share of deaths |
| Test set used once | locked | [B pp.74, 328] | no step 3 or step 4 code reads `test_idx` before step 4g |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** reuse the earlier test set · a new split (fraction and seed to be chosen)
- **Expectation:** n/a
- **Decision:** Reuse the earlier analysis's split, with 60 test patients locked until the final evaluation.
- **Limitation:** these test patients produced the earlier analysis's test result, which the user and the advisor have seen. The test set has informed none of this rerun's choices so far, but it is not unknown to us. The rerun's test result is therefore a like-for-like comparison with the earlier one rather than a fresh estimate.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "Same test set as before"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/hf2_02_split.py`, `Code/outputs/hf2/split.json`, `Code/outputs/split.json` (read only)

### DR-08 · FORM · step 3

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** What is the input design: is any of the 11 inputs transformed before modelling?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Inputs | the 11 clinical columns; `time` not an input (step 1) | M | DR-05 |
| Documented ranges | `creatinine_phosphokinase` 23–7,861 mcg/L; `serum_creatinine` 0.50–9.40 mg/dL; `platelets` 25.01–850.00 (paper's unit); `serum_sodium` 114–148; `ejection_fraction` 14–80 % | M | Chicco and Jurman (2020), Table 1 |
| User's answer | "All as recorded", chosen from three options without a recommendation | M | user, 28 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design (§9) | decided with the user from meanings and documented ranges, not from the data | [B p.18] | not a configuration axis; not chosen by CV |
| Start simple | no transformation | [B p.331] | inputs used as recorded |
| REQ-6 | the five 0/1 indicators one-hot encoded | [B p.49] | one column each (one level dropped) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** all as recorded · natural log of `creatinine_phosphokinase` and `serum_creatinine` · log of those two and `platelets`
- **Expectation:** n/a
- **Decision:** All 11 inputs are used as recorded, with no transformation. The five indicators are single 0/1 columns and the six numerical inputs are unchanged. Scaling is added only by the families that need it (REQ-2, REQ-3), inside the folds (REQ-1).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "All as recorded"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/hf2/core.py` (`preprocessor`, interpretation a)

### DR-09 · PROP · step 3

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** What are the property values P1–P10, now that P9 and P10 have been computed from the training patients?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 output type | binary | M | DR-05 |
| P2 data-to-parameter ratio | ample (239 ÷ (11 + 1) = 19.92) | M | `Code/outputs/hf2/split.json` |
| P3 number of inputs | few (11 columns after encoding; unchanged by DR-08) | M | `split.json`; `core_p9_p10.json` (`input_columns_after_encoding`: 11) |
| P4 share of categorical inputs | low (5 ÷ 11 = 45 %) | M | `split.json` |
| P5 interpretability | none | M | user: "Not needed" |
| P6 probabilities or threshold | yes, not a must-have | M | user: "Yes, nice to have" |
| P7 beyond training range | no | M | user: "No" |
| P8 expected shape | unknown | M | user: "I have no expectation" |
| P9 classes perfectly separable | no: logistic regression with C = 1e8 classifies 184 of 239 training patients correctly (accuracy 0.7699; 55 misclassified; 6 iterations, no convergence warning) | T | `Code/outputs/hf2/core_p9_p10.json` |
| P10 class imbalance | balanced: smallest class share 0.3222 (77 of 239 deaths) | T | `Code/outputs/hf2/core_p9_p10.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P2 | ample | [I] | no P2 entry in the matrix |
| P3 | few | [I] | no P3 entry |
| P4 | low | [I] | no P4 entry |
| P6 = yes (not a must-have) | applies | [B→I pp.50, 53–54] | +1 on Logistic in the prior (§13) |
| P9 | no | [I] | MOD-1 does not apply (step 4a) |
| P10 | balanced | [I] | the diagnosis loop uses the book's default error, the misclassification rate (§16), although PR-AUC decides between models |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 19.92 |
| P3 many inputs | > 20 | 11 |
| P4 high categorical share | ≥ 50 % | 45 % |
| P9 separable | 100 % training accuracy with negligible regularisation (C = 1e8) | 76.99 % (184 of 239) |
| P10 imbalanced | smallest class < 20 % | 32.22 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** P1 binary · P2 ample · P3 few · P4 low · P5 none · P6 yes (not a must-have) · P7 no · P8 unknown · P9 no · P10 balanced. The P9 fit only establishes a property: it is not a candidate model, and its result is not interpreted as a finding.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

**Reference code**

- Function: `p9_p10` in `Code/hf2/core.py` (interim core, not reviewed) · version SHA-256 `2e4b01c3d733bb4f410fb8daaf3bd03512671ba57e0ef30c321be73b6e85789f` · inputs: the 239 training rows (`Code/outputs/hf2/split.json` `train_idx`), DR-08 input design · output: `Code/outputs/hf2/core_p9_p10.json`, copied unchanged

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — the user saw the core before it ran and chose "Run it"
- **Supersedes / superseded by:** supersedes DR-06
- **Links:** `Code/hf2/core.py`, `Code/outputs/hf2/core_p9_p10.json`

### DR-10 · ADMSET · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** Which of the 14 structural configurations (§9) are admissible for sub-task 1, given the property values in DR-09?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Property values passed to the core | P1 binary, P2 ample, P3 few, P4 low, P5 none (not a must-have), P6 yes (not a must-have), P7 no, P8 unknown, P9 no, P10 balanced | M / T | DR-09; `Code/hf2/props_dr09.json` |
| Labels checked before 4a | `DEATH_EVENT` is death during a follow-up of varying length, and how follow-up ended for patients without a death is undocumented, so a 0 means "no death observed" (DR-01). It is not constructed from the inputs. `time`, which is tied to the outcome, is not an input (step 1). Nothing new found | M | DR-01; `Data Summary` |
| MOD-2, without powers | design matrix with intercept: 12 columns, rank 12; parameters 12; n_train 239 | T | `Code/outputs/hf2/core_admset.json` |
| MOD-2, with powers 2–3 of the 6 numerical inputs | 24 columns, rank 24; parameters 24; n_train 239 | T | same |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, P1 = binary | Logistic, k-NN, Tree admissible | [B pp.17, 49–57] | 8 configurations removed: the four `Linear`, both `Poisson`, both `Exponential` |
| Must-have gates (P5, P6) | not applied: neither is a must-have | [B→I p.347]; [B→I pp.50, 53–54] | none removed |
| MOD-1 | P9 = no: does not apply | [B p.61] | none removed |
| MOD-2 | does not apply: full rank, and parameters < n_train, with and without powers | [B→I pp.46–47, 65] | none removed |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| MOD-2 exact collinearity (interpretation f) | rank < columns at numpy `matrix_rank` default tolerance | rank 12 of 12; 24 of 24 |
| MOD-2 parameters ≥ n_train (interpretation g) | 239 | 12; 24 |
| Largest polynomial degree checked (§16 grid) | 3 | — |

- **Options considered:** the 14 structural configurations of §9
- **Expectation:** n/a
- **Decision:** Six configurations are admissible: `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`, `kNN` and `Tree`. Under §14 SEQ-2 the simple-first configuration will be `Logistic`, because neither MOD-1 nor MOD-2 removed it. This is applied in 4b.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] |
| `Poisson`, `Poisson + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] |
| `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] |

**Reference code**

- Function: `admissible_set` (`cd Code && uv run python hf2/core.py admset hf2/props_dr09.json`) · version: interim core, not reviewed, SHA-256 `778783471bc9fe5cb35d47b3fd1cf73ada5640ac071483e04c10b9e3bcb38e5e` (extended for 4a from `2e4b01c3…`; `p9_p10` unchanged, so DR-09 stays valid) · inputs: DR-09 property values in `Code/hf2/props_dr09.json`; the 239 training patients; interpretations e–h in the core's docstring · output: `Code/outputs/hf2/core_admset.json`, copied above unchanged

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — the user chose "§12 now, §13–§19 at 4b", saw the §9/§12 extension before it ran, and chose "Run it"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/hf2/core.py`, `Code/hf2/props_dr09.json`, `Code/outputs/hf2/core_admset.json`, DR-09

### DR-11 · PRIOR · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** Which admissible configurations should be cross-validated, and in what expected order?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Admissible set | `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`, `kNN`, `Tree` | T | DR-10 |
| P1 · P2 · P3 · P4 | binary · ample (19.92) · few (11) · low (45 %) | M | DR-09 |
| P5 · P6 · P7 · P8 | none · yes (not a must-have) · no · unknown | M | DR-09; user's words in DR-05 |
| P9 · P10 | no · balanced (no row in the matrix) | T | DR-09 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P6=yes→Logistic | holds (not a must-have) | [B→I pp.50, 53–54] | +1 on all four Logistic configurations |
| §13 other entries | none applies (P2 ample, P3 few, P4 low, P5 none, P7 no, P8 unknown) | — | — |
| §15 order | score, then fewer add-ons; ties share a rank | [I] (§15 procedure) | `Logistic` 1; `Logistic + L2` = `Logistic + poly` 2; `Logistic + poly + L2` 4; `kNN` = `Tree` 5 |
| SEQ-1 | baseline = flag nobody | [B pp.330–331] | kept |
| SEQ-2 | simple-first = `Logistic` (MOD-1 and MOD-2 did not remove it) | [B p.331] | kept |
| §15 keep | simple-first + 3 highest-ranked others (+ ties at the cut, rank 4) | [I] | `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2` kept; `kNN`, `Tree` not kept |
| SEQ-3 | round 1 = baseline and `Logistic`; round 2 only once `Logistic` clearly beats the baseline | [B pp.331–332] | sets the order of 4c and 4d |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 19.92 |
| P3 many inputs | > 20 | 11 |
| P4 high categorical share | ≥ 50 % | 45 % |
| Kept besides baseline and simple-first | 3 (+ ties) | 5 others admissible |

- **Options considered:** the six admissible configurations
- **Expectation** (written before any cross-validation; ours, not the prior's `[I]`):
  - `Logistic` and `Logistic + L2` will lead, quite possibly within noise of each other: with 19.9 rows per parameter, L2 should change the fit only a little.
  - The polynomial versions will be lower, and `Logistic + poly` without L2 the lowest of the four. Squares and cubes double the columns from 12 to 24 for 239 patients, and without regularisation that invites overfitting (pp. 59–60).
  - Since the prior's order differs only by add-ons, agreement with it at rank 1 or 2 is likely if this expectation holds.
- **Decision:** Cross-validate the baseline and `Logistic` in round 1, then `Logistic + L2`, `Logistic + poly` and `Logistic + poly + L2` in round 2, on the same folds. `kNN` and `Tree` are not kept. They can enter later only through the diagnosis loop (DX-5, if underfitting is found), as post-prior entries.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `kNN` | DISF | prior score 0 (no matrix entry), rank 5 |
| `Tree` | DISF | prior score 0 (no matrix entry), rank 5 |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary (DR-10) |

**Cross-validation protocol agreed (§16)**

- **Outer folds:** 10, stratified by `DEATH_EVENT`, shuffled, seed 2026. The same folds are used for every configuration, and they are stored with the checksums of the data file and `split.json`.
- **Inner folds:** 5-fold grid search within each outer training fold, on PR-AUC (average precision). The grids are:
  - λ ∈ {10⁻⁴, …, 10⁴};
  - degree ∈ {2, 3};
  - k ∈ {1, …, 51} (for configurations added later);
  - tree depth ∈ {1, …, 20} × minimum leaf size ∈ {1, 5, 10, 20} (for configurations added later).
  - `Logistic` and `Logistic + poly` are unregularised (C = ∞).
- **Deciding metric:** PR-AUC. Margins are means of fold differences, and the spread is the SD of those differences.
- **Diagnosis errors:** the misclassification rate at r = 0.5 (P10 = balanced).
- **Decision threshold:** after selection, nested, maximising F2 over r ∈ {0.01, …, 0.99}. The trade-off is confirmed with the user at 4f.
- **`N_JOBS`:** 1.
- **Flags:** none.

**Reference code**

- Function: `prior_ranking` (`cd Code && uv run python hf2/core.py prior hf2/props_dr09.json`) · version: interim core, not reviewed, SHA-256 `93225b44b5c337c342904f57bb7c2710fb5a6d4db267e31df2ad54b728f1186a`. It was extended for 4b from `77878347…` with §13–§19 and interpretations i–z; `p9_p10` and `admissible_set` are unchanged, so DR-09 and DR-10 stay valid · inputs: DR-09 property values in `Code/hf2/props_dr09.json` · output: `Code/outputs/hf2/core_prior.json`, copied above unchanged

- **Confidence:** n/a
- **Outcome vs expectation:** disagree (filled in by DR-13).
  - The CV order is `Logistic + poly` (0.7064) > `Logistic + poly + L2` (0.6882) > `Logistic + L2` (0.6703) > `Logistic` (0.6627).
  - The expectation was the reverse: the plain configurations first, and `Logistic + poly` without L2 last. All four are within noise of the leader (each margin < 0.5 × spread), so the order is not clearly established, but it is not the one expected.
  - Against the prior: the CV winner among the prior-kept configurations, `Logistic + poly`, has prior rank 2, so prior agreement is partial.
- **User involvement:** approved — the user saw the §13–§19 extension before any output was used ("Run the prior"), and then agreed the method: "Agree the method"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/hf2/core.py`, `Code/hf2/props_dr09.json`, `Code/outputs/hf2/core_prior.json`, DR-09, DR-10

### DR-12 · CV · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** Does the simple-first configuration, `Logistic`, clearly beat the baseline in nested cross-validation (round 1, SEQ-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Baseline, validation PR-AUC per outer fold | 0.3333 (7 folds), 0.2917 (2 folds), 0.3043 (1 fold): the fold's share of deaths | CV | `Code/outputs/hf2/core_cv_store.json` |
| `Logistic`, validation PR-AUC per outer fold | 0.5536, 0.5972, 0.6392, 0.7937, 0.6902, 0.6438, 0.8507, 0.5769, 0.6252, 0.6562 | CV | same |
| `Logistic`, training PR-AUC per outer fold | 0.7004, 0.6853, 0.6726, 0.6588, 0.6694, 0.6788, 0.6412, 0.6775, 0.6774, 0.6620 | CV | same |
| Convergence | all 10 outer refits converged (unregularised, C = ∞) | CV | `core_cv_round1.json` (`not_converged_folds`: 0) |
| REQ-1, REQ-3, REQ-6 in the pipeline | `design` (DR-08 encoding) → `scale` (StandardScaler) → `m` (BookLogistic, C = ∞), refitted inside every training fold | CV | `core_cv_store.json` (`pipeline`) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 | round 1 = baseline and the simple-first configuration only | [B pp.331–332] | — |
| §16 nested CV | 10 outer × 5 inner, stratified by `DEATH_EVENT`, seed 2026; PR-AUC | [B pp.72–73]; [I] | — |
| C2 (`Logistic` vs baseline) | margin 0.3406 ≥ 1 × spread 0.0892 → clear | [I] | round 2 may proceed; DX-1 is not triggered |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | 0.3406 vs 0.0892 |

**CV table** (outer 10, inner 5; stratified by `DEATH_EVENT`; seed 2026; metric: PR-AUC as average precision; diagnosis errors: misclassification rate at r = 0.5)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean PR-AUC | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (flag nobody) | no | n/a | 0.3221 | 0.0184 | −0.3406 (0.0892) | — | 0.3222 | 0.3221 |
| `Logistic` | no | none (unregularised; 10/10) | 0.6627 | 0.0938 | — (leader) | +0.3406 (0.0892), clear | 0.2329 | 0.2848 |

- **Options considered:** baseline, `Logistic`
- **Expectation:** n/a (the expectation is in DR-11 and is tested in round 2)
- **Decision:** `Logistic` clearly beats the baseline (C2 clear), so round 2 (4d) proceeds with `Logistic + L2`, `Logistic + poly` and `Logistic + poly + L2` on the same folds.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | not a selection; why-not codes are assigned in `FINAL` |

**Reference code**

- Function: `run_cv` via `cd Code && uv run python hf2/core.py cv round1 hf2/props_dr09.json` · version: interim core, not reviewed, SHA-256 `93225b44b5c337c342904f57bb7c2710fb5a6d4db267e31df2ad54b728f1186a` (unchanged since DR-11) · output: `Code/outputs/hf2/core_cv_round1.json`, `core_cv_store.json`, copied above unchanged (rounded to 4 decimals); run time 20 s

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "continue step 4 with the method agreed in DR-11"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/hf2/core_cv_round1.json`, `Code/outputs/hf2/core_cv_store.json`, DR-11

### DR-13 · CV · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** How do the remaining kept configurations compare with `Logistic` and the baseline on the same folds (round 2)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `Logistic + L2`, validation PR-AUC per fold | 0.5536, 0.5659, 0.6215, 0.8188, 0.7351, 0.6355, 0.8726, 0.6388, 0.6252, 0.6364 | CV | `Code/outputs/hf2/core_cv_store.json` |
| `Logistic + L2`, tuned λ per fold | 10⁻⁴, 10, 1, 10⁻³, 0.1, 0.01, 0.1, 1, 10⁻³, 1 | CV | same |
| `Logistic + poly`, validation PR-AUC per fold | 0.4533, 0.5633, 0.6401, 0.8405, 0.8262, 0.5259, 0.9040, 0.8571, 0.6964, 0.7570 | CV | same |
| `Logistic + poly`, training PR-AUC per fold | 0.7829, 0.7485, 0.7581, 0.7962, 0.7854, 0.8303, 0.7804, 0.7921, 0.7493, 0.7959 | CV | same |
| `Logistic + poly`, tuned degree per fold | 2, 2, 2, 3, 3, 3, 3, 3, 2, 3 | CV | same |
| `Logistic + poly + L2`, validation PR-AUC per fold | 0.5231, 0.5475, 0.6401, 0.8061, 0.8519, 0.5538, 0.8860, 0.7167, 0.7205, 0.6365 | CV | same |
| `Logistic + poly + L2`, tuned (degree, λ) per fold | (2, 0.01), (3, 10), (2, 10⁻⁴), (3, 0.01), (3, 10⁻³), (3, 10⁻³), (3, 0.1), (3, 10), (3, 0.01), (3, 1) | CV | same |
| Convergence | all refits converged | CV | `core_cv_round2.json` (`not_converged_folds`: 0) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 | round 2 run because `Logistic` clearly beat the baseline (DR-12) | [B pp.331–332] | — |
| §16 same outer folds | stored folds checked and reused | [I] | margins paired by fold |
| C2 for each configuration | clear for all four | [I] | all eligible under §19.1 |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | `Logistic + poly` 0.3843 vs 0.1619; `Logistic + poly + L2` 0.3661 vs 0.1320; `Logistic + L2` 0.3482 vs 0.1023; `Logistic` 0.3406 vs 0.0892 |
| §19 within noise (for reference; applied at 4f) | margin < 0.5 × spread | `Logistic + poly + L2` 0.0182 vs 0.0332; `Logistic + L2` 0.0360 vs 0.0490; `Logistic` 0.0437 vs 0.0586 |

**CV table** (outer 10, inner 5; stratified by `DEATH_EVENT`; seed 2026; metric: PR-AUC as average precision; diagnosis errors: misclassification rate at r = 0.5)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean PR-AUC | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (flag nobody) | no | n/a | 0.3221 | 0.0184 | −0.3843 (0.1619) | — | 0.3222 | 0.3221 |
| `Logistic + poly` | no | degree 3 (6/10) | 0.7064 | 0.1557 | — (leader) | +0.3843 (0.1619), clear | 0.1878 | 0.2424 |
| `Logistic + poly + L2` | no | degree 3, λ = 10 (2/10) | 0.6882 | 0.1299 | −0.0182 (0.0664) | +0.3661 (0.1320), clear | 0.2333 | 0.2763 |
| `Logistic + L2` | no | λ = 1 (3/10) | 0.6703 | 0.1051 | −0.0360 (0.0980) | +0.3482 (0.1023), clear | 0.2817 | 0.2971 |
| `Logistic` | no | none (10/10) | 0.6627 | 0.0938 | −0.0437 (0.1171) | +0.3406 (0.0892), clear | 0.2329 | 0.2848 |

- **Options considered:** `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2` (round 2), alongside round 1
- **Expectation:** n/a (this record fills in DR-11's *Outcome vs expectation*)
- **Decision:**
  - All four configurations clearly beat the baseline. `Logistic + poly` has the highest CV mean, but every other configuration is within noise of it, with margins below 0.5 × spread.
  - The fold-to-fold variation is large: fold SDs of 0.09 to 0.16 on means around 0.66 to 0.71, with 23 to 24 patients and 7 to 8 deaths per validation fold.
  - The CV order disagrees with the advisor's expectation (DR-11).
- **Noted for 4e:**
  - The tuned λ varies widely across folds (from 10⁻⁴ to 10 for `Logistic + L2`). It is at an edge (10⁻⁴) in only 1 of 10 folds, so O5 is not expected to hold.
  - The leader `Logistic + poly` has the lowest training error (0.1878) of the four.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | not a selection; why-not codes are assigned in `FINAL` |

**Reference code**

- Function: `run_cv` via `cd Code && uv run python hf2/core.py cv round2 hf2/props_dr09.json` · version: interim core, not reviewed, SHA-256 `93225b44b5c337c342904f57bb7c2710fb5a6d4db267e31df2ad54b728f1186a` · output: `Code/outputs/hf2/core_cv_round2.json`, `core_cv_store.json`, copied above unchanged (rounded to 4 decimals); run time 46 s

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "continue step 4 with the method agreed in DR-11"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/hf2/core_cv_round2.json`, `Code/outputs/hf2/core_cv_store.json`, DR-11, DR-12

### DR-14 · DX · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** Diagnosis pass 1 (§18) on the leading configuration, `Logistic + poly`: which observation holds first, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Errors (misclassification rate at r = 0.5, P10 = balanced) | E_train 0.1878, E_val 0.2424, gap 0.0546 | CV | `Code/outputs/hf2/core_diagnose_Logistic___poly.json` |
| Training PR-AUC (mean over outer folds) | 0.7819 | CV | same |
| Learning curve, E_val mean (fold SD) at 10 %, 20 % … 100 % | 0.2969 (0.0448), 0.3018 (0.1147), 0.3056 (0.0886), 0.2594 (0.0674), 0.2717 (0.0899), 0.2511 (0.0983), 0.2551 (0.0861), 0.2551 (0.0905), 0.2592 (0.0953), 0.2424 (0.1187) | CV | same |
| Learning curve, E_train mean at 10 % … 100 % | 0.0000, 0.0093, 0.1047, 0.1314, 0.1512, 0.1643, 0.1752, 0.1802, 0.1864, 0.1878 | CV | same |
| Run time | 2 min 4 s | — | — |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 = clear (DR-13) |
| O2 training performance short of what the application needs | no | training PR-AUC 0.7819 > training share of deaths 0.3222 + fold SD 0.1557 = 0.4779 (interpretation q) |
| O5 tuned hyperparameter at a grid edge | no | the degree is ignored (interpretation r); no other tuned hyperparameter |
| O3 overfitting | no | gap 0.0546 < 2 × E_train = 0.3756 |
| **O4 underfitting** | **yes**, the first that holds | E_train 0.1878 ≥ 2 × gap = 0.1092 |
| O6 more data likely to help | no | C3 adequate: E_val(80 %) − E_val(100 %) = 0.0127 < 0.5 × 0.1187 = 0.0594 |

- **Action:** DX-5 (O4), more flexibility `[B pp.333–334]`. Its parts:
  - (i) Add polynomial terms if P3 = few: the leader already has them.
  - (ii) **Add k-NN or a tree if not already compared: taken.** Neither was kept by the prior (DR-11, DISF). Both are cross-validated on the same folds as post-prior entries, with the §16 grids. This is an action on configurations, so it runs without stopping.
  - (iii) Ask whether more input variables exist: needs the user; considered in the next pass if needed.
  - DX-9 `[B p.334]`: the gap is not ≫ E_train, so adding flexibility is not ruled out.

**Stopping check**

- **S1:** not assessed until 4g.
- **S2:** the achievable level is unknown.
- **S3, S4, S5, S6:** no; this is the first pass.
- The loop continues.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 overfitting: gap ≥ 2 × E_train | 0.3756 | 0.0546 |
| O4 underfitting: E_train ≥ 2 × gap | 0.1092 | 0.1878 |
| O5 edge in most folds | > 5 of 10 | n/a (no grid besides degree) |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0594 | 0.0127 |

- **Options considered:** the three parts of DX-5, above
- **Expectation** (written before the k-NN and tree runs): neither `kNN` nor `Tree` will clearly beat the leader (0.7064). The reasoning is that the fold-to-fold spread is large (0.09 to 0.16) and 239 patients give each fold only about 7 to 8 deaths to validate on. A tree at this size is likely to be unstable from fold to fold, and k-NN on 11 standardised inputs, five of them 0/1, measures similarity coarsely. Both are expected at or below the logistic configurations, possibly within noise of them.
- **Decision:** O4 → DX-5 part (ii): cross-validate `kNN` and `Tree` as post-prior entries.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `observations` (`cd Code && uv run python hf2/core.py diagnose "Logistic + poly"`) · version: interim core, not reviewed, SHA-256 `93225b44b5c337c342904f57bb7c2710fb5a6d4db267e31df2ad54b728f1186a` · output: `Code/outputs/hf2/core_diagnose_Logistic___poly.json`, copied above unchanged (rounded to 4 decimals)

- **Confidence:** n/a
- **Outcome vs expectation:** agree (filled in by DR-15). Neither `kNN` (0.5633) nor `Tree` (0.5546) beats the leader (0.7064); both are below all four Logistic configurations. `kNN` trails the leader by more than one spread, and `Tree` by between 0.5 and 1 × spread.
- **User involvement:** informed — the user asked for 4e and for k-NN or Tree only if DX-5 calls for them; part (ii) runs without stopping
- **Supersedes / superseded by:** n/a
- **Links:** `Code/hf2/core.py` (`observations`, `learning_curve`), `Code/outputs/hf2/core_diagnose_Logistic___poly.json`, DR-13

### DR-15 · CV · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** How do `kNN` and `Tree`, added by DX-5 (post-prior), compare on the same folds?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `kNN`, validation PR-AUC per fold | 0.4127, 0.4726, 0.5984, 0.6589, 0.6421, 0.4707, 0.9167, 0.5493, 0.4961, 0.4160 | CV | `Code/outputs/hf2/core_cv_store.json` |
| `kNN`, tuned k per fold | 15, 51, 51, 51, 21, 51, 51, 51, 31, 51 (the largest grid value, 51, in 7 of 10 folds) | CV | same |
| `Tree`, validation PR-AUC per fold | 0.5510, 0.4271, 0.4555, 0.6747, 0.8819, 0.4679, 0.7127, 0.4556, 0.3748, 0.5453 | CV | same |
| `Tree`, tuned (depth, minimum leaf) per fold | (5, 10), (5, 5), (4, 10), (5, 10), (4, 5), (6, 5), (4, 10), (6, 10), (3, 5), (3, 5) | CV | same |
| REQ-2 (k-NN normalised), REQ-4 (tree size tuned) | `kNN`: `design` → `scale` → `m`; `Tree`: `design` → `m`, with depth and minimum leaf size from the grid | CV | `core_cv_store.json` (`pipeline`, `grid`) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| DX-5 (ii), add k-NN or a tree if not already compared | both added, post-prior, same folds | [B pp.333–334] | — |
| C2 | clear for both | [I] | eligible under §19.1 |
| §17 breadth note | 6 configurations compared (4 prior-kept, 2 post-prior) | [I] | below 10 |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | `kNN` 0.2412 vs 0.1472; `Tree` 0.2325 vs 0.1497 |
| Breadth note | > 10 | 6 |

**CV table** (outer 10, inner 5; stratified by `DEATH_EVENT`; seed 2026; PR-AUC; all entries so far)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean PR-AUC | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (flag nobody) | no | n/a | 0.3221 | 0.0184 | −0.3843 (0.1619) | — | 0.3222 | 0.3221 |
| `Logistic + poly` | no | degree 3 (6/10) | 0.7064 | 0.1557 | — (leader) | +0.3843 (0.1619), clear | 0.1878 | 0.2424 |
| `Logistic + poly + L2` | no | degree 3, λ = 10 (2/10) | 0.6882 | 0.1299 | −0.0182 (0.0664) | +0.3661 (0.1320), clear | 0.2333 | 0.2763 |
| `Logistic + L2` | no | λ = 1 (3/10) | 0.6703 | 0.1051 | −0.0360 (0.0980) | +0.3482 (0.1023), clear | 0.2817 | 0.2971 |
| `Logistic` | no | none (10/10) | 0.6627 | 0.0938 | −0.0437 (0.1171) | +0.3406 (0.0892), clear | 0.2329 | 0.2848 |
| `kNN` | yes | k = 51 (7/10) | 0.5633 | 0.1518 | −0.1430 (0.1194) | +0.2412 (0.1472), clear | 0.3157 | 0.3346 |
| `Tree` | yes | depth 5, minimum leaf 10 (2/10) | 0.5546 | 0.1572 | −0.1517 (0.1535) | +0.2325 (0.1497), clear | 0.1688 | 0.3098 |

- **Options considered:** `kNN`, `Tree` (DX-5 part ii)
- **Expectation:** n/a (this record fills in DR-14's *Outcome vs expectation*)
- **Decision:** Neither new configuration leads. `Logistic + poly` remains the leader, so the loop continues with pass 2 on it. `kNN`'s k at the grid edge is noted, but O5 is computed only for the leader.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `run_cv` via `cv add "kNN"` and `cv add "Tree"` · version: interim core, not reviewed, SHA-256 `93225b44b5c337c342904f57bb7c2710fb5a6d4db267e31df2ad54b728f1186a` · output: `Code/outputs/hf2/core_cv_post_prior_1.json`, `core_cv_post_prior_2.json`, `core_cv_store.json`, copied above unchanged (rounded to 4 decimals); run time 2 min 50 s for both

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed (DX-5 part ii runs without stopping)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/hf2/core_cv_post_prior_1.json`, `Code/outputs/hf2/core_cv_post_prior_2.json`, DR-14

### DR-16 · DX · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** Diagnosis pass 2 (§18) on the unchanged leader, `Logistic + poly`: which action is left, and does the loop stop?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Leader | unchanged (DR-15), so its observations are those of DR-14: O4 holds first (E_train 0.1878 ≥ 2 × gap 0.0546) | CV | `Code/outputs/hf2/core_diagnose_Logistic___poly.json` |
| DX-5 parts | (i) add polynomial terms: the leader has them; (ii) add k-NN or a tree: done in pass 1, neither leads (DR-15); (iii) ask whether more input variables exist: needs the user | — | DR-14, DR-15 |
| User's answer to (iii) | "No; stop the loop" | M | user, 28 October 2026 |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1, O2, O5, O3 | no | as DR-14 |
| **O4 underfitting** | **yes**, the first that holds | as DR-14 |
| O6 | no | as DR-14 |

- **Action:** DX-5 part (iii): the user was asked whether more input variables exist. The answer was no. The only other column in the file, `time`, was set aside in step 1 as a leakage risk.

**Stopping check**

- **S1 (criterion met):** not assessed until 4g.
- **S2:** the achievable level is unknown.
- **S3:** pass 1 gave no gain, because the leader did not change; pass 2 adds no configuration.
- **S4:** no.
- **S5 (user stops it): applies.** "No; stop the loop."
- **S6:** no.
- The loop stops under S5 after two passes.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| as DR-14 | | |

- **Options considered:** put to the user without a recommendation: no further inputs, stop the loop (chosen); more inputs exist
- **Expectation:** n/a (no configuration action is taken)
- **Decision:** The diagnosis loop ends under S5. Six configurations have been compared, besides the baseline: the 4 prior-kept Logistic configurations, and `kNN` and `Tree` post-prior. The leader is `Logistic + poly`. Next is 4f.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "No; stop the loop"
- **Supersedes / superseded by:** n/a
- **Links:** DR-14, DR-15

### DR-17 · FINAL · step 4

- **Sub-task:** 1 — Death during follow-up
- **Date:** 2026-10-28
- **Question:** Which configuration does the recommendation rule (§19) choose, how confident is the selection (§17), at which decision threshold, and, once the user approves, how does it do on the test set?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV results | the CV table of DR-15 (rounds 1, 2 and the DX-5 entries, same folds) | CV | `Code/outputs/hf2/core_cv_store.json` |
| Diagnosis | loop stopped under S5 after two passes | CV | DR-16 |
| Threshold trade-off | "F2, as in DR-05", chosen from three options without a recommendation (F2; F3; F1) | M | user, 28 October 2026 |
| Recommendation | `Logistic` (unregularised, all 11 inputs), decision threshold r = 0.10 | CV | `Code/outputs/hf2/core_recommend.json` |
| Selection confidence | Low: C1 none (runner-up `Logistic + poly`, margin −0.0437, spread 0.1171); C2 clear (margin over the baseline 0.3406, spread 0.0892); C3 adequate (E_val(80 %) − E_val(100 %) = −0.0335 < 0.5 × 0.0530) | CV | same |
| Learning curve, E_val mean (fold SD) at 10 % … 100 % | 0.2933 (0.0830), 0.3014 (0.0525), 0.2763 (0.0601), 0.2804 (0.0765), 0.2596 (0.0624), 0.2638 (0.0599), 0.2513 (0.0632), 0.2513 (0.0632), 0.2554 (0.0702), 0.2848 (0.0530) | CV | same |
| Prior agreement | partial: the CV winner among the prior-kept configurations, `Logistic + poly`, has prior rank 2 | CV | same |
| Grounding | 1 matrix entry, `[B→I]`: P6=yes→Logistic `[B→I pp.50, 53–54]` | — | same |
| Selection breadth | 6 configurations compared; the note (> 10) does not apply | — | same |
| Decision threshold, nested CV (r chosen inside each outer fold) | r per outer fold 0.02, 0.09, 0.10, 0.05, 0.16, 0.08, 0.13, 0.13, 0.28, 0.15; F2 0.7127 (SD 0.0614), precision 0.4012 (SD 0.0553), recall 0.8946 (SD 0.1056) | CV | same |
| Final threshold, on all training patients' inner out-of-fold probabilities | 0.10 | CV | same |
| Uncertainty for 4g | SD of PR-AUC across the outer folds for `Logistic`: 0.0938 `[B→I pp.71–73]` | CV | same |
| Training share of deaths | 0.3222 (77 of 239) | T | same |

**§19 trace**

1. **Eligible** (C2 = clear; no must-haves in DR-09):
   - `Logistic` +0.3406 (spread 0.0892)
   - `Logistic + L2` +0.3482 (0.1023)
   - `Logistic + poly` +0.3843 (0.1619)
   - `Logistic + poly + L2` +0.3661 (0.1320)
   - `kNN` +0.2412 (0.1472)
   - `Tree` +0.2325 (0.1497)

   All six are eligible; none has inputs dropped.
2. **Candidates** (the best CV mean, plus any within 0.5 × spread of it):
   - `Logistic + poly`: 0.7064, the best
   - `Logistic + poly + L2`: 0.6882, margin 0.0182 < 0.0332
   - `Logistic + L2`: 0.6703, margin 0.0360 < 0.0490
   - `Logistic`: 0.6627, margin 0.0437 < 0.0586
3. **Choice** (fewest add-ons, then prior score, then CV mean): `Logistic` (0 add-ons) over `Logistic + L2` and `Logistic + poly` (1 each) and `Logistic + poly + L2` (2). It is decided at the first step, add-ons. All four have prior score +1.
4. **Test once:** pending the user's approval (step 4g).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.1 eligible = C2 clear and every must-have met | all six eligible | [I] (C2 threshold) | — |
| §19.2 candidates within the noise margin | four Logistic configurations | [I] threshold 0.5 × spread | — |
| §19.3 fewest add-ons | `Logistic` | [B p.332] | recommended |
| §17 C1, C2, C3 and the level rule | C1 none, C2 clear, C3 adequate → Low | [I]; C3 [B→I pp.334–336] + [I] | reported with its factors |
| §16 decision threshold (P6 = yes) | tuned after selection, maximising F2, nested | [B→I pp.53–54, 92–93] | r = 0.10 |
| Final hyperparameters (interpretation s) | none to tune (unregularised) | — | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C1 clear ≥ 1 × spread, moderate ≥ 0.5 × spread | 0.1171 / 0.0586 | −0.0437 → none |
| C2 clear ≥ 1 × spread | 0.0892 | 0.3406 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0265 | −0.0335 |
| §19 within noise < 0.5 × spread | per candidate | see trace |
| Breadth note > 10 configurations | 10 | 6 |
| Threshold grid | 0.01 to 0.99, step 0.01 | chosen 0.10 |

**The agent's notes on these outputs** (raised, not substituted):
- **C1 is "none" because the recommendation is not the CV leader.** §19.3's simplicity rule chose `Logistic` over the higher-scoring `Logistic + poly`, so the margin to the runner-up is negative. The level Low follows mechanically. It reflects that the four Logistic configurations cannot be told apart on these 239 patients.
- **The threshold is low.** r = 0.10, with per-fold values from 0.02 to 0.28. With F2 weighting recall twice as heavily, about a third of patients dying, and probabilities that separate the classes only partly, the threshold that maximises F2 flags most patients. Nested precision is 0.40 against a share of deaths of 0.32, and recall is 0.89.
- **The learning curve's E_val is higher at 100 % (0.2848) than at 80 % (0.2513).** The curve does not fall over the last fifth, so C3 is adequate. The fold SDs (0.05 to 0.08) are of the same size as these differences.

- **Options considered:** the six eligible configurations; the threshold trade-off (F2, F3, F1)
- **Expectation:** DR-11 expected `Logistic` and `Logistic + L2` to lead; they did not lead on CV mean (DR-13), but `Logistic` is chosen by §19.3. No expectation about the choice or the confidence level was stated.
- **Decision:** Recommend `Logistic` (unregularised), with decision threshold 0.10 (F2). Selection confidence is Low (C1 none). The test set is used only after the user approves.

**Why not** (all 14 structural configurations except the recommendation)

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] (DR-10) |
| `Logistic + L2` | SIMP | margin (recommendation − this) −0.0077, spread 0.0300; within noise; 1 add-on against 0 |
| `Logistic + poly` | SIMP | margin −0.0437, spread 0.1171; within noise; 1 add-on against 0 |
| `Logistic + poly + L2` | SIMP | margin −0.0255, spread 0.0827; within noise; 2 add-ons against 0 |
| `kNN` | OUTP | margin +0.0993, spread 0.0871 (≥ 1 × spread) |
| `Tree` | OUTP | margin +0.1080, spread 0.1232 (≥ 0.5 × spread; outside the candidate set, which is measured from the best) |

**Flags:** none.

**Reference code**

- Function: `recommend` (`cd Code && uv run python hf2/core.py recommend hf2/props_dr09.json`) · version: interim core, not reviewed, SHA-256 `93225b44b5c337c342904f57bb7c2710fb5a6d4db267e31df2ad54b728f1186a` (unchanged since DR-11; approved at 4b) · inputs: DR-09 property values; the CV store; F2 as the threshold trade-off · output: `Code/outputs/hf2/core_recommend.json`, copied above unchanged (rounded to 4 decimals). Run time 43 s.

**Test-set result** (step 4g, 28 October 2026, after the user's approval; used once)

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Approval | "1", the option "Approve the test evaluation (4g)", quoted on the command line and stored in the output | M | `Code/outputs/hf2/core_final.json` (`approved_by_user`) |
| Model evaluated | `Logistic` (unregularised), all 11 inputs, refitted on all 239 training patients; threshold r = 0.10 | TEST | same |
| Test patients | 60, of whom 19 died (share 0.3167); the same 60 patients as the earlier analysis's test set (DR-07) | TEST | same |
| Test PR-AUC (the estimate of E_new on the agreed metric) | 0.6983 | TEST | same; recomputed independently: `Code/outputs/hf2/recompute_test_metric.txt` |
| Uncertainty | fold SD of PR-AUC across the 10 outer folds: 0.0938 `[B→I pp.71–73]`. Each outer fold holds 23–24 patients and the test set 60, so this approximates the uncertainty of the test result rather than measuring it | CV | `core_recommend.json` |
| Baseline on the same test patients | flag nobody: PR-AUC 0.3167 (the share of deaths) | TEST | `core_final.json`; recomputed |
| Success criterion (DR-05) | 0.6983 − 0.0938 = 0.6045 > 0.3167, so it is **met** | TEST | same |
| At the threshold r = 0.10 | 49 of 60 flagged; tp 16, fp 33, fn 3, tn 8; precision 0.3265, recall 0.8421, F2 0.6400 | TEST | same; recomputed |
| CV and test, side by side | CV mean PR-AUC 0.6627 (fold SD 0.0938), test 0.6983. Nested CV at the tuned threshold gave precision 0.4012 and recall 0.8946; the test gives 0.3265 and 0.8421 | CV / TEST | `core_recommend.json`, `core_final.json` |
| Independent recomputation | average precision from its definition (no scikit-learn) and confusion counts by counting, from the saved predictions with outcomes read from the source file by row and rows checked against `split.json`: all equal to the core's | TEST | `Code/hf2_07_recompute_test_metric.py` → `recompute_test_metric.txt` ("agrees with core: True") |
| Precision–recall curve | §5.5 calls for it when positives are the minority; it is drawn in step 4h from the saved test predictions | — | ML Guide §5.5 |

The test set is not used again for this sub-task. The core's `final` refuses a second run while `core_final.json` exists.

- **Confidence:** Low — C1 none · C2 clear · C3 adequate — rule: Low if C1 = none or C2 = not clear · prior agreement partial · grounding [B] 0 / [B→I] 1 / [I] 0 · breadth note n/a (6 compared)
- **Outcome vs expectation:** partial (`Logistic` was expected near the top; it is chosen by simplicity, not by CV mean). No expectation was stated about the test result.
- **User involvement:** asked — threshold trade-off: "F2, as in DR-05"; test set: "1" (Approve the test evaluation (4g))
- **Supersedes / superseded by:** n/a
- **Links:** `Code/hf2/core.py` (`recommend`, `tune_threshold`), `Code/outputs/hf2/core_recommend.json`, DR-10 to DR-16

## Recommendation

### Sub-task 1 — Death during follow-up

*Assembled on 28 October 2026 from DR-01 to DR-17. Nothing in it is new. The user's experience is "New to ML" (Data Summary), so terms are explained the first time they appear.*

**1. Problem.**
- **What is predicted:** `DEATH_EVENT`, death during a follow-up period of varying length, from 11 clinical inputs as recorded: 6 numerical, 5 yes/no. `time` is not an input (step 1, leakage risk). A 0 means "no death observed during follow-up" (DR-01, DR-05, DR-08).
- **Output type:** binary (P1).
- **What a prediction is for:** flagging patients at higher risk when follow-up starts. Missing a death is worse than a false alarm.
- **Metric:** PR-AUC, the area under the precision–recall curve (p. 92), computed as average precision `[I]`. Precision is the share of flagged patients who died; recall is the share of deaths that were flagged.
- **Baseline:** flag nobody. A baseline is a deliberately simple rule that any useful model must beat (pp. 330–331). Its PR-AUC equals the share of deaths.
- **Success criterion:** test PR-AUC minus its uncertainty above the test share of deaths.
- **Achievable level:** unknown.
- **Requirements and expectations:** P5 none; P6 yes, not a must-have; P7 no; P8 unknown, in the user's words "I have no expectation" (DR-09).
- **Admissibility:**
  - ADM-1: yes (DR-01).
  - ADM-2: predict (DR-04).
  - ADM-3: no groups and no time order (DR-02).
  - ADM-4: yes, new patients are taken to look like these (DR-03).
- **Split:** the earlier analysis's test set, reused at the user's choice: 239 training patients (77 deaths) and 60 test patients (19 deaths). Those 60 patients' earlier test result was already known (DR-07).

**2. Recommendation.** `Logistic`: logistic regression without regularisation, on the 11 inputs, with decision threshold r = 0.10 (patients with a predicted probability above 0.10 are flagged). Selection confidence: **Low** (DR-17).

**3. Test-set result.**
- **PR-AUC:** 0.6983 on 60 test patients (19 deaths), with an uncertainty of 0.0938. The uncertainty is the standard deviation of PR-AUC across the 10 outer folds `[B→I pp.71–73]`. Each outer fold holds 23–24 patients against 60 in the test set, so it approximates rather than measures the test result's uncertainty.
- **Baseline on the same patients:** 0.3167.
- **Success criterion:** 0.6983 − 0.0938 = 0.6045 > 0.3167, so it is **met**.
- **At r = 0.10:** 49 of 60 flagged.

| Outcome \ prediction | Not flagged | Flagged |
| --- | --- | --- |
| No death | 8 | 33 |
| Died | 3 | 16 |

  Precision 0.3265, recall 0.8421, F2 0.6400.
- **Threshold:** chosen by cross-validation on the training patients to maximise F2, which weights recall twice as heavily as precision (p. 92), as the user chose.
- **Curve:** the precision–recall curve is drawn in Figure 6 of `Report.md`.
- **Checks:** recomputed independently, with an identical result.

**4. Why this configuration.**
- **Constraints.** A yes/no output allows logistic regression, k-NN and decision trees (task gate, DR-10). Plain logistic regression stays admissible, because no straight boundary separates deaths from the others perfectly (P9 = no, so MOD-1 does not apply).
- **Cross-validation evidence.** Cross-validation repeatedly fits on part of the training patients and scores on the rest (pp. 72–73). Here the scoring used 10 outer folds, with λ, degree, k or tree size tuned in 5 inner folds inside each.
  - `Logistic` reached 0.6627, against the leader `Logistic + poly`'s 0.7064: a margin of −0.0437, spread 0.1171.
  - Its margin over the baseline is +0.3406, spread 0.0892.
- **Simplicity. Yes, this decided it.** Four configurations were within noise of the leader: `Logistic + poly`, `Logistic + poly + L2`, `Logistic + L2` and `Logistic`. §19.3 chose the one with the fewest add-ons, `Logistic` (0 add-ons), as the book advises starting simple (p. 332).
- **Prior support.** One matrix entry: P6=yes→Logistic `[B→I pp.50, 53–54]`, from the wish for probabilities and a tunable threshold.

**5. Ranking.** The columns are:
- *Prior rank* and *Prior score:* from the ranking made before any fitting (DR-11).
- *Post-prior:* added by the diagnosis loop.
- *CV mean:* mean PR-AUC over the 10 outer folds.
- *Margins:* mean fold-by-fold differences, with the spread (their SD).
- *Code:* the why-not code.

| Configuration | Prior rank | Prior score | Post-prior | CV mean | Margin vs recommended (± spread) | Margin vs baseline (± spread) | Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic + poly` | 2 | +1 | no | 0.7064 | +0.0437 (± 0.1171) | +0.3843 (± 0.1619) | SIMP |
| `Logistic + poly + L2` | 4 | +1 | no | 0.6882 | +0.0255 (± 0.0827) | +0.3661 (± 0.1320) | SIMP |
| `Logistic + L2` | 2 | +1 | no | 0.6703 | +0.0077 (± 0.0300) | +0.3482 (± 0.1023) | SIMP |
| `Logistic` (recommended) | 1 | +1 | no | 0.6627 | — | +0.3406 (± 0.0892) | — |
| `kNN` | 5 | 0 | yes | 0.5633 | −0.0993 (± 0.0871) | +0.2412 (± 0.1472) | OUTP |
| `Tree` | 5 | 0 | yes | 0.5546 | −0.1080 (± 0.1232) | +0.2325 (± 0.1497) | OUTP |
| Baseline (flag nobody) | — | — | no | 0.3221 | −0.3406 (± 0.0892) | — | — |

**6. Prior versus evidence. Partial.**
- The prior ranked `Logistic` first and `Logistic + L2` and `Logistic + poly` second, on add-ons only, since all four Logistic configurations scored +1.
- The CV winner among the prior-kept configurations, `Logistic + poly`, has prior rank 2. No matrix entry is contradicted: the one entry that applied (P6 → Logistic) favoured the Logistic family, which leads.
- The advisor's own expectation, that the plain configurations would lead and `Logistic + poly` would come last, was not borne out (DR-11, DR-13). All four were within noise of each other, so the CV order among them is not established.

**7. Why not the others.**
- **EXCL:** `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2`: task gate, P1 = binary [B pp.17, 49–57] (DR-10).
- **USER:** none.
- **DISF:** none in the final table. `kNN` and `Tree` were not kept by the prior (DR-11), but were added by DX-5 and cross-validated, so they carry OUTP.
- **BASE:** none.
- **OUTP:** `kNN` (margin 0.0993, spread 0.0871); `Tree` (margin 0.1080, spread 0.1232; outside the candidate set, which is measured from the best).
- **SIMP:** `Logistic + L2`, `Logistic + poly` and `Logistic + poly + L2`: within noise, with more add-ons.

Flags: none.

**8. Confidence.**
- **Selection confidence: Low.**
  - C1 none: the runner-up `Logistic + poly` has a higher CV mean, margin −0.0437, spread 0.1171.
  - C2 clear: +0.3406 ≥ 1 × 0.0892.
  - C3 adequate: the learning-curve validation error at 100 % (0.2848) is not lower than at 80 % (0.2513).
  - Rule: Low if C1 = none or C2 = not clear.
- **Reported alongside:**
  - Prior agreement: partial.
  - Grounding: [B] 0 · [B→I] 1 · [I] 0.
  - Breadth note: does not apply (6 configurations compared).

**9. How the model predicts** (draft, turned into prose in step 5).
- **What the model computes.** Logistic regression gives each patient a probability of dying during follow-up. It adds up the 11 inputs, each first put on a common scale (standardised on the training patients) and multiplied by a learned weight, plus a constant. It turns that sum into a probability between 0 and 1 with the logistic function (pp. 51–52).
- **The decision.** A patient is flagged if the probability is above 0.10, a threshold chosen to favour catching deaths over avoiding false alarms (F2).
- **Its boundary.** Because the score is a weighted sum, the boundary between flagged and not flagged is a straight line, more precisely a flat plane, in the space of the inputs (p. 55).
- **What the weights can say.** They give the direction and relative size of each input's pull on the log-odds of death, with the others held fixed. They are not causes (ADM-2: prediction only).
- **The fitted weights** (completed in step 5, from `Code/outputs/hf2/core_weights.json`).
  - **Source.** The core's `explain` command (version `93fc3491…`; additions only, shown to the user before it ran: "Run explain") rebuilt the final model with the same code and settings as `final`. It accepted the rebuild only because its probabilities equal the saved ones for all 60 test patients. That check read the test inputs and the saved probabilities only: no outcome was read and no metric computed.
  - **Penalty and constant.** No regularisation (C = ∞). The constant (intercept) is −1.0361.
  - **How to read the table.** Each weight is the change in the log-odds of death for a patient one standard deviation above the training mean on that input, with the others fixed. "Per unit" divides by that SD. A positive weight raises the predicted risk. The weights are not causes (ADM-2, DR-04).

| Input | SD (training) | Weight (standardised) | Weight per unit |
| --- | --- | --- | --- |
| `ejection_fraction` (%) | 12.01 | −0.9349 | −0.0779 per % |
| `age` (years) | 12.01 | +0.7027 | +0.0585 per year |
| `serum_creatinine` (mg/dL) | 0.9524 | +0.5782 | +0.6071 per mg/dL |
| `serum_sodium` (mEq/L) | 4.589 | −0.3267 | −0.0712 per mEq/L |
| `creatinine_phosphokinase` (mcg/L) | 913 | +0.2927 | +0.00032 per mcg/L |
| `anaemia` (0/1) | 0.494 | +0.2860 | +0.5791 for 1 vs 0 |
| `high_blood_pressure` (0/1) | 0.4787 | +0.2652 | +0.5540 for 1 vs 0 |
| `sex` (0/1; coding undocumented) | 0.4704 | −0.2190 | −0.4655 for 1 vs 0 |
| `smoking` (0/1) | 0.4689 | +0.0748 | +0.1595 for 1 vs 0 |
| `diabetes` (0/1) | 0.4926 | +0.0505 | +0.1025 for 1 vs 0 |
| `platelets` (unit uncertain) | 99,620 | −0.0114 | −1.14 × 10⁻⁷ per unit as recorded |

  - **What the table shows** (reading the output, not new analysis): ejection fraction, age and serum creatinine have the largest standardised weights. A lower ejection fraction, an older age and a higher serum creatinine each raise the predicted risk. Platelets, diabetes and smoking have the smallest.

- **Worked example** (a constructed typical patient, not a real row).
  - **The patient.** Each numerical input is at its training median: age 60, ejection fraction 38 %, serum creatinine 1.1 mg/dL, serum sodium 137 mEq/L, CPK 250 mcg/L, platelets 255,000 as recorded. Each yes/no input is at its most common training value: no anaemia, no diabetes, no high blood pressure, no smoking, sex = 1.
  - **Step 1, standardise.** Each value is put on the training scale; for example, ejection fraction 38 % is 0.01 SD above the training mean.
  - **Step 2, score.** The log-odds is the constant plus the sum of weight × standardised value: −1.0361 + (−1.0781) = −2.1143. The largest contributions are anaemia = 0 (−0.2447), high blood pressure = 0 (−0.1970), serum creatinine below the mean (−0.1742) and sex = 1 (−0.1539).
  - **Step 3, probability.** The logistic function turns the log-odds into a probability: 0.1077.
  - **Step 4, decide.** 0.1077 is above the threshold 0.10, so this patient is **flagged**.
  - **Trust limits (§21).** These weights describe this fitted model on patients like the training patients, and hold only while new patients resemble them. They say nothing about why some patients die.

**10. Use and limits** (draft, turned into prose in step 5).
- **What the result covers.** The model ranks patients like these by their risk of dying during follow-up, and flags those above r = 0.10. The PR-AUC of 0.6983 is an average over patients like the 60 test patients (E_new, pp. 68–69). It says nothing about the worst single prediction, and it holds only while new patients resemble these: NYHA III–IV, Faisalabad, 2015 (ADM-4, §6.6).
- **Limits from step 1:**
  - A 0 means "no death observed during follow-up", whose end is undocumented.
  - The `platelets` unit is uncertain.
  - The two hospitals are not identified.
- **Limits of the evaluation:**
  - The test set is small (60 patients, 19 deaths), and the fold spread is large (0.0938).
  - These 60 patients produced the earlier analysis's test result, which was known beforehand (DR-07).
- **At the threshold:** precision on the test patients (0.3265) is close to the share of deaths (0.3167), while recall is 0.8421.

**11. Improvement history.**
- **Round 1:** `Logistic` clearly beat the baseline (DR-12).
- **Round 2:** all four Logistic configurations were within noise; `Logistic + poly` led (DR-13).
- **Pass 1** (DR-14): O4, underfitting: E_train 0.1878 ≥ 2 × gap 0.0546 → DX-5 (ii): add `kNN` and `Tree`. Result: 0.5633 and 0.5546, neither leading (DR-15).
- **Pass 2** (DR-16): O4 again → DX-5 (iii), more input variables? The user had none.
- **Stopped by S5** (the user stopped it).

**12. Thresholds applied.**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 19.92 (ample) |
| P3 many inputs | > 20 | 11 (few) |
| P4 high categorical share | ≥ 50 % | 45 % (low) |
| P9 separable | 100 % training accuracy, C = 1e8 | 76.99 % (no) |
| P10 imbalanced | smallest class < 20 % | 32.22 % (balanced) |
| Kept besides baseline and simple-first | 3 (+ ties) | 3 kept, 2 DISF |
| Outer / inner folds | 10 / 5 | — |
| O3 overfitting | gap ≥ 2 × E_train | 0.0546 < 0.3756 |
| O4 underfitting | E_train ≥ 2 × gap | 0.1878 ≥ 0.1092 |
| O5 grid edge | > 5 of 10 folds | n/a for the leader |
| C1 clear / moderate | ≥ 1 / 0.5 × spread | −0.0437 vs 0.1171 (none) |
| C2 clear | ≥ 1 × spread | 0.3406 vs 0.0892 |
| C3 limited | E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | −0.0335 vs 0.0265 |
| §19 within noise | < 0.5 × spread | 0.0437 vs 0.0586; 0.0360 vs 0.0490; 0.0182 vs 0.0332 |
| Breadth note | > 10 configurations | 6 |
| Threshold grid | 0.01–0.99, step 0.01 | 0.10 |

**13. Trace and provenance.**
- **Records:** DR-01 to DR-17; DR-06 is superseded by DR-09.
- **Rules applied** (the *Rules applied* tables of the 16 records in force, counted by script): [B] 26 · [B→I] 8 · [I] 15 · UNLISTED 1 (PR-AUC computed as average precision, DR-05). Two rows carry no tag: the "other §13 entries" row of DR-11, and the final-hyperparameters row of DR-17.
- **Not counted** (DX records use *Observation → action*): DX-5 [B pp.333–334], twice.
- **Core:** interim, not reviewed, version `93225b44…` for 4b–4g. Interpretations a–z are listed in its header.

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1. New analysis "Heart Failure rerun" (the user chose the name): a rerun of the heart failure data with the method as it stands, prompted by `Note for Florentine.md`. Created `Demonstration/Heart Failure rerun/` and copied the templates. `Demonstration/Heart Failure/` is the reference and is not edited; this rerun's code uses the prefixes `hf2_` and `hf2/`. | `Demonstration/Heart Failure rerun/` |
| 2 | Step 1. Recomputed the SHA-256, which matches `SOURCE.md`. Read the UCI variable table (API) and the *Dataset* section of Chicco and Jurman (2020), from the open-access full text on Europe PMC. Downloaded the original 2017 release from figshare into a temporary folder outside the workspace, compared it with the UCI file (the same 299 rows; only the names and order differ), and deleted it. | `Data Summary` |
| 3 | Step 1, describing pass (`hf2_01_describe_data.py`, written fresh). No conclusions drawn. | `Code/hf2_01_describe_data.py`, `Code/outputs/hf2/01_describe.json`, `01_describe.md` |
| 4 | Step 1. The user stated their experience ("New to ML") and answered ADM-1 "Yes", ADM-3 "Neither" and ADM-4 "Yes". | DR-01, DR-02, DR-03 |
| 5 | Step 1, scope. `time` set aside as a leakage risk (not an input; kept in the file); the alternative, keeping it as an input, was offered and not taken. `platelets` used as recorded, with its unit uncertain; rescaling by 1/1,000 was not taken. `serum_sodium` = 113 (1 row) and `age` = 60.667 (2 rows) accepted as-is; setting to missing and rounding were not taken. All 299 rows kept. | `Data Summary`, *Step 1 decisions* |
| 6 | Step 1 closed by the user ("close step 1"). Three items listed at the close were not taken up. Rows are not restricted by follow-up length: a 0 means "no death observed during follow-up", which is recorded as a label limitation. The coding of `sex` stays undocumented. The two hospitals stay unidentified in the file. | `Data Summary` |
| 7 | Step 2. The user asked for suggestions. Three candidate problems were offered, and the user chose "Death during follow-up". ADM-2 was answered "Predict". | `Problem Definition`, DR-04 |
| 8 | Step 2, formulation. Missing a death is worse. PR-AUC (average precision) is the deciding metric; F2, precision and recall are monitored at a threshold tuned after selection. Baseline: flag nobody. Success: test PR-AUC minus its fold SD above the test share of deaths. Achievable level unknown. P5 none, P6 yes (not a must-have), P7 no, P8 unknown ("I have no expectation"). | DR-05, DR-06 |
| 9 | Step 2, split. The user chose to reuse the earlier analysis's test set over a new split. `hf2_02_split.py` read the earlier `split.json` (unchanged), checked its checksum, settings and partition, and wrote this rerun's own split: 239 training (77 deaths) and 60 test (19 deaths). P2 = ample (19.92), P3 = few (11), P4 = low (45 %). Test set locked. The `Data Summary` statement that the earlier outputs are "not read" was amended to name this exception. | `Code/hf2_02_split.py`, `Code/outputs/hf2/split.json`, DR-06, DR-07 |
| 10 | Step 2. Problem, approach and sub-task written into the `Introduction` of `Report.md`, with the works it cites in its `References`. The book entry was added to the appendix's `References` first; the link was checked on 28 October 2026. | `Report.md` |
| 11 | Step 2 closed: the user moved on to step 3. Items listed at the close and not taken up: the threshold trade-off (to be confirmed at 4f); input transformations (settled in step 3, row 12); a second sub-task. | — |
| 12 | Step 3, input design. Three options were offered without a recommendation (as recorded; log of CPK and serum creatinine; log of those and platelets), and the user chose "All as recorded". | DR-08 |
| 13 | Step 3. Interim core `Code/hf2/core.py` written (input design, §11 P9 and P10) and shown to the user before it ran ("Run it"). P9 = no (184 of 239 correct with C = 1e8); P10 = balanced (32.2 %). New PROP record supersedes DR-06. | `Code/hf2/core.py`, `Code/outputs/hf2/core_p9_p10.json`, DR-09 |
| 14 | Step 3, figures. Four were proposed and the user chose all four: numerical input distributions, numerical inputs by outcome, share who died by yes/no input, and yes/no input counts. One revision (platelet axis format; overlapping line label) before they were added to `Results` with captions and notes on how to read Figures 2 and 3. | `Code/hf2_03_fig1_input_distributions.py` … `hf2_06_fig4_indicator_counts.py`, `Code/outputs/hf2/figures/` (+ `dark/`), `Report.md` |
| 15 | Step 3, at the user's decision: the yes/no input counts figure was dropped from `Results`, because its counts already appear in the labels of Figure 3 (deaths / patients for each value). The image and its caption were removed, and "Figures 1 to 4" became "Figures 1 to 3". The remaining figures keep their numbers, so no renumbering was needed. In the appendix, references to the figure by number were reworded. `Code/hf2_06_fig4_indicator_counts.py` and its images (`Code/outputs/hf2/figures/fig4_indicator_counts.png`, `dark/`, `.json`) are kept, as the contract asks. | `Report.md`, `Appendix.md` |
| 16 | Step 3 closed: the user moved on to step 4. Items listed at the close and not taken up: whether to keep the remaining figures as they stand; an expectation for P8 (it stays `unknown`); how the platelet panel is shown, given its uncertain unit. | — |
| 17 | Step 4a, sub-task 1. The user chose to add §9/§12 to the core now and §13–§19 at 4b. The extended core (SHA-256 `77878347…`) was shown and approved ("Run it"). Admissible: `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`, `kNN`, `Tree`. The task gate removed the 8 Linear and GLM configurations; MOD-1 and MOD-2 did not apply. | `Code/hf2/core.py`, `Code/hf2/props_dr09.json`, `Code/outputs/hf2/core_admset.json`, DR-10 |
| 18 | Step 4b, sub-task 1. The core was extended with §13–§19 (SHA-256 `93225b44…`; interpretations i–z, including the new §19 rule on input drops and `N_JOBS = 1`) and shown to the user before any output was used ("Run the prior"). Prior: P6=yes→Logistic is the only entry (+1 on all Logistic configurations). Kept: `Logistic` (simple-first), `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`; `kNN` and `Tree` are DISF (score 0). The expectation is recorded. The method was presented and agreed ("Agree the method"). | `Code/hf2/core.py`, `Code/outputs/hf2/core_prior.json`, DR-11 |
| 19 | Step 4c, sub-task 1: round 1 run (20 s). Baseline mean CV PR-AUC 0.3221; `Logistic` 0.6627 (fold SD 0.0938). Margin 0.3406, spread 0.0892: C2 clear, so round 2 may proceed. All refits converged. | `Code/outputs/hf2/core_cv_round1.json`, `core_cv_store.json`, DR-12 |
| 20 | Step 4d, sub-task 1: round 2 run (46 s) on the same folds. Mean CV PR-AUC: `Logistic + poly` 0.7064 (leader), `Logistic + poly + L2` 0.6882, `Logistic + L2` 0.6703, `Logistic` 0.6627. All clearly beat the baseline, and all are within noise of the leader. DR-11 outcome vs expectation: disagree (expected the plain configurations first and `Logistic + poly` last); prior agreement partial (winner at prior rank 2). | `Code/outputs/hf2/core_cv_round2.json`, `core_cv_store.json`, DR-11, DR-13 |
| 21 | Step 4e, pass 1 on `Logistic + poly` (2 min 4 s): O4 (underfitting) holds first (E_train 0.1878 ≥ 2 × gap 0.0546). DX-5: part (i) does not apply (the leader has poly); part (ii) adds `kNN` and `Tree`, which the prior had not kept. The expectation was written before the run. | `Code/outputs/hf2/core_diagnose_Logistic___poly.json`, DR-14 |
| 22 | Step 4e, DX-5 (ii) run (2 min 50 s): `kNN` 0.5633 (k = 51 in 7/10 folds), `Tree` 0.5546. Both clearly beat the baseline and both are below the four Logistic configurations. The leader is unchanged. DR-14 outcome vs expectation: agree. | `Code/outputs/hf2/core_cv_post_prior_1.json`, `_2.json`, DR-15 |
| 23 | Step 4e, pass 2: the leader is unchanged, so O4 and DX-5 remain, and only part (iii) is left. Asked whether more input variables exist, the user chose "No; stop the loop". The loop ends under S5 after two passes, with 6 configurations compared. Step 4e is done. | DR-16 |
| 24 | Step 4f. Threshold trade-off: the user chose "F2, as in DR-05" (no core change). `recommend` ran (43 s, core `93225b44…`). Recommended: `Logistic` (unregularised), chosen by fewest add-ons among four Logistic candidates within noise of the leader `Logistic + poly`. Decision threshold 0.10; nested F2 0.7127, precision 0.4012, recall 0.8946. Selection confidence Low (C1 none: the runner-up has a higher mean; C2 clear; C3 adequate); prior agreement partial; grounding 1 [B→I]; breadth note does not apply (6 compared). Why-not: 8 EXCL, 3 SIMP, 2 OUTP. The test set has not been used. | `Code/outputs/hf2/core_recommend.json`, DR-17 |
| 25 | Step 4g. The user approved ("1"). The core's `final` refitted `Logistic` on the 239 training patients and evaluated it once on the 60 test patients (19 deaths): test PR-AUC 0.6983, fold SD 0.0938, baseline 0.3167; success criterion met (0.6045 > 0.3167). At r = 0.10: 49 flagged, tp 16, fp 33, fn 3, tn 8; precision 0.3265, recall 0.8421, F2 0.6400. An independent recomputation (average precision by definition, without scikit-learn) agrees exactly. | `Code/outputs/hf2/core_final.json`, `core_test_predictions.csv`, `Code/hf2_07_recompute_test_metric.py`, `Code/outputs/hf2/recompute_test_metric.txt`, DR-17 |
| 26 | Step 4h. The user chose all four evaluation figures: Figure 4 (CV comparison), Figure 5 (learning curve of `Logistic`), Figure 6 (test precision–recall curve) and Figure 7 (test confusion matrix), each drawn only from the core's outputs, in light and dark versions, in the model colour (purple). One revision before Figure 6 entered the report: the curve first drew points where precision changes at unchanged recall, which made spikes. Now only the points where recall rises are drawn, the ones average precision counts. The drawn curve integrates to the reported 0.6983 before and after. The Recommendation Report for sub-task 1 was assembled from DR-01 to DR-17, with part 13's provenance counts from a script over the *Rules applied* tables. The `Methods` and `Results` paragraphs and Figures 4–7 were added to `Report.md`. Part 9 lacks the fitted weights and a worked example, because the core does not save the final model; this is raised with the user. | `Code/hf2_08_fig4_cv_comparison.py` … `hf2_11_fig7_confusion.py`, `Code/outputs/hf2/figures/`, `Recommendation`, `Report.md` |
| 27 | Step 4 closed by the user ("close step 4"). Four items listed at the close were not taken up: an `explain` command for part 9's fitted weights and worked example; where to write the comparison with the earlier analysis's result on the same test set; whether the low threshold (test precision 0.3265 against a share of deaths of 0.3167) is discussed as a limitation; changes to Figures 4–7. | — |
| 28 | Step 5. `explain` was added to the core (additions only, 72 lines; `93225b44…` → `93fc3491…`) and shown to the user before it ran ("Run explain"). It rebuilt `Logistic` as `final` did, and accepted it because its probabilities equal the saved ones for all 60 test patients; no outcome was read and no metric computed. Weights and a worked example on a constructed typical patient were written. Recommendation Report part 9 was completed, with the sums checked against the output. `final` is untouched and would still refuse a second run. | `Code/hf2/core.py`, `Code/outputs/hf2/core_weights.json`, `Recommendation` |
| 29 | Step 5, at the user's request: a derived comparison was recorded in `Analysis`. F2 of flagging every patient = 5p / (4p + 1): 0.6985 on the test set and 0.7038 in training. Against it: the model's test F2 0.6400 and nested CV F2 0.7127. Also recorded is the earlier analysis's result on the same test set, from its Appendix DR-19 (`Tree`, r = 0.2, F2 0.6780). It is computed from reported numbers only; no test row was read. Asked how the `Discussion` should use it, the user chose "Use as context" over "Appendix only". | `Analysis` |
| 30 | Step 5, `Discussion`. The user chose the structure "Choice → how → use → limits (Recommended)" from three options. The `Discussion` was written with each limitation beside the conclusion it qualifies, no new analysis, and every number checked against the records. The flag-everyone F2 is used as context, as chosen; the earlier analysis appears in one sentence. One sentence was corrected before committing ("little better than flagging nearly everyone" became "below flagging everyone on the measure the threshold was chosen for"), because the test F2 is below the flag-everyone F2. Title chosen from three: "Predicting death during follow-up in heart failure patients from routine clinical measurements". | `Report.md` |
| 31 | Step 5 closed by the user ("close step 5"). Three items listed at the close were not taken up: the report's `Appendix` section keeps its template note (no pointer written); parts 9 and 10 of the Recommendation Report keep the label "draft, turned into prose in step 5"; the README is not updated. The Heart Failure rerun has completed steps 1–5. | — |

## Code Summary

All scripts run from `Code/` with `uv run python <script>.py`. Names start with `hf2_`; the interim core will be `Code/hf2/core.py`; outputs go to `Code/outputs/hf2/`. The earlier analysis's files (`Code/core.py`, `Code/01_…08_*.py`, `Code/outputs/*.json`, `Code/outputs/figures/`) are not read or changed.

| File | What it does | Reads | Writes | Seeds / parameters |
| --- | --- | --- | --- | --- |
| `Code/hf2_01_describe_data.py` | Step 1 describing pass. Recomputes the SHA-256 and checks it against `SOURCE.md`. Describes each column: meaning, unit and type from the UCI variable table, the paper's range, distinct values, percentiles, zeros, non-integer values and 0/1 counts. Counts duplicates, class counts, row order and `time` by `DEATH_EVENT`. Draws no conclusions. | `Attachments/heart_failure_clinical_records_dataset.csv` | `Code/outputs/hf2/01_describe.json`, `01_describe.md` | none |
| `Code/hf2_02_split.py` | Step 2 split. Reuses the earlier analysis's training and test row indices (user's choice), after checking that file's source checksum, its settings and that the indices partition the 299 rows. Records this rerun's input design (11 inputs, `time` set aside), the class counts recomputed from the data, and P2–P4 with their `[I]` thresholds as named constants. | `Attachments/heart_failure_clinical_records_dataset.csv`, `Code/outputs/split.json` (earlier analysis; read only) | `Code/outputs/hf2/split.json` | the source split's seed 2026 and fraction 0.2 are checked, not set |
| `Code/hf2/core.py` | **Interim core, not reviewed** (the version is its SHA-256, quoted in the Decision Records). So far: the input design of DR-08 (`preprocessor`: six numerical inputs passed through, five 0/1 indicators one-hot encoded with one level dropped), the training-data reader (`training_data`: the 239 `train_idx` rows only, asserting that no test row is kept), §11 P9 and P10 (`p9_p10`). From step 4a it adds §9 and §12 (`admissible_set`, `mod2_check`). From step 4b it adds the rest: §13–§15 prior ranking (`prior_ranking`); §16 nested CV with a cumulative store (`run_cv`, `nested_cv`, `baseline_cv`, `cv_table`); §18 observations and the learning curve (`observations`, `learning_curve`); §16/§17/§19/§20 threshold tuning, recommendation, confidence and why-not codes (`tune_threshold`, `recommend`); and §19.4 the single test evaluation (`final`), the only function that reads the test rows. `final` needs the user's approval on the command line, and refuses a second run or a changed core. The header lists interpretations a–z. Commands: `p9p10`; `admset`, `prior`, `cv round1`, `cv round2` and `recommend`, each with `hf2/props_dr09.json`; `cv add "<configuration>" [--drop COL] [--grid JSON] [--label TEXT]`; `diagnose "<entry>"`; `final --approved "<words>"`. | `Attachments/heart_failure_clinical_records_dataset.csv`, `Code/outputs/hf2/split.json`, `Code/hf2/props_dr09.json` (the DR-09 values) | `Code/outputs/hf2/core_p9_p10.json`, `core_admset.json`, `core_prior.json`. Later: `core_cv_store.json`, `core_cv_round1.json`, `core_cv_round2.json`, `core_cv_post_prior_N.json`, `core_diagnose_*.json`, `core_recommend.json`, `core_final.json`, `core_test_predictions.csv` | `[I]` constants as named in the file: `P9_SEPARABLE_ACCURACY = 1.0`, `P9_NEGLIGIBLE_C = 1e8`, `P10_IMBALANCED_SHARE = 0.20`, `DEFAULT_THRESHOLD = 0.5`, `KEEP_TOP_OTHERS = 3`, `OUTER_FOLDS = 10`, `INNER_FOLDS = 5`, `C1_CLEAR = 1.0`, `C1_MODERATE = 0.5`, `C2_CLEAR = 1.0`, `C3_FALLING = 0.5`, `WITHIN_NOISE = 0.5`, `BREADTH_MANY = 10`, `O3_RATIO = O4_RATIO = 2.0`, `O5_MOST_FOLDS = 0.5`; grids (§16); `CV_SEED = 2026`, `THRESHOLD_BETA = 2`, `THRESHOLD_GRID` 0.01–0.99, `N_JOBS = 1`, `KEPT_DROPS = []`; `LOGISTIC_MAX_ITER = 100000` |
| `Code/hf2_07_recompute_test_metric.py` | Step 4g second route to the test result: average precision from its definition (no scikit-learn), the confusion counts, precision, recall and F2 at the core's threshold, all by counting, from the saved predictions. True outcomes are read from the data file by row number, and the rows are checked against `split.json`. The result is compared with `core_final.json`. | `Code/outputs/hf2/core_test_predictions.csv`, the data file, `split.json`, `core_final.json` | `Code/outputs/hf2/recompute_test_metric.txt` | none |
| `Code/hf2_08_fig4_cv_comparison.py` | Figure 4: mean CV PR-AUC with fold-SD error bars for the baseline and the six configurations. | `Code/outputs/hf2/core_cv_post_prior_2.json` (the core's last CV table), `core_recommend.json` | `Code/outputs/hf2/figures/fig4_cv_comparison.png` (+ `dark/`), `.json` | `MODEL_COLOUR` |
| `Code/hf2_09_fig5_learning_curve.py` | Figure 5: the learning curve of the recommended configuration (misclassification rate at 0.5), E_train and E_val with fold-SD error bars. | `Code/outputs/hf2/core_recommend.json` | `fig5_learning_curve.png` (+ `dark/`), `.json` | none |
| `Code/hf2_10_fig6_pr_curve.py` | Figure 6: the test precision–recall curve, traced from the saved probabilities (only points where recall rises), with the no-skill line and the chosen threshold marked. The reported numbers are read from `core_final.json`. | `Code/outputs/hf2/core_test_predictions.csv`, `core_final.json` | `fig6_pr_curve.png` (+ `dark/`), `.json` | none |
| `Code/hf2_11_fig7_confusion.py` | Figure 7: the test confusion matrix at the chosen threshold, with counts. | `Code/outputs/hf2/core_final.json` | `fig7_confusion.png` (+ `dark/`), `.json` | none |
| `Code/hf2_03_fig1_input_distributions.py` | Figure 1: one panel per numerical input, both outcomes together. One bar per value for ejection fraction and sodium, 1-year bins for age, 40 equal-width bins for the rest. Light and dark versions. | training patients via `core.training_data()` | `Code/outputs/hf2/figures/fig1_input_distributions.png` (+ `dark/`), `.json` | `BINS = 40`, `FIGSIZE = (15, 9)` |
| `Code/hf2_04_fig2_inputs_by_outcome.py` | Figure 2: box plot per outcome group for each numerical input, with every patient as a jittered point. | same | `fig2_inputs_by_outcome.png` (+ `dark/`), `.json` (group sizes, medians, quartiles) | `JITTER_SEED = 2026` (sideways position only) |
| `Code/hf2_05_fig3_indicators_by_outcome.py` | Figure 3: share who died among patients with each yes/no input = 0 and = 1, with deaths/patients labels and the overall share as a reference line. | same | `fig3_indicators_by_outcome.png` (+ `dark/`), `.json` | none |
| `Code/hf2_06_fig4_indicator_counts.py` | Yes/no input counts: the number of training patients with each yes/no input = 1. Dropped from `Results` in step 3 (Analysis Log row 15); the script and image files are kept. | same | `fig4_indicator_counts.png` (+ `dark/`), `.json` | none |

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published). Read at smlbook.org; the link was checked on 28 October 2026. Page references in the Decision Records come from `ML Guide.md`.
- Ahmad, T., Munir, A., Bhatti, S. H., Aftab, M. and Raza, M. A. (2017). Survival analysis of heart failure patients: a case study. *PLoS ONE*, 12(7), e0181001. [https://doi.org/10.1371/journal.pone.0181001](https://doi.org/10.1371/journal.pone.0181001). Its data, `S1 Data.csv` ("DATA_MINIMAL", version 1, CC BY 4.0), are on figshare as article 5227684 (record checked through the figshare API, 28 October 2026). The link was checked on 28 October 2026.
- Chicco, D. and Jurman, G. (2020). Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone. *BMC Medical Informatics and Decision Making*, 20, 16. [https://doi.org/10.1186/s12911-020-1023-5](https://doi.org/10.1186/s12911-020-1023-5). Its *Dataset* section was read on 28 October 2026 from the open-access full text (Europe PMC, PMC6998201). The link was checked on 28 October 2026.
- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R). The variable table was read through the UCI API on 28 October 2026. The link was checked on 28 October 2026.
