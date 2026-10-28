# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

*Step 1, closed 28 October 2026. All figures are from `Code/outputs/hf2/01_describe.json`. The decisions taken in step 1 are under* Step 1 decisions *at the end of this section.*

**This is a rerun, and that is a limitation.**
- The same data were analysed before in `Demonstration/Heart Failure/` (steps 1–5, finished), and its data, decisions and results are known to the user and to the advisor.
- This rerun works through the steps afresh with the method as it stands now (`instructions.md` and `ML Guide.md` at 28 October 2026). Every decision is put to the user as options, and no decision is copied from the earlier Appendix.
- Prior knowledge cannot be undone, though. Choices in this rerun, such as the problem, the inputs and the metric, may be influenced by what the earlier analysis found, and the earlier test result has already been seen. Whether this rerun's test set is the same as the earlier one is a step 2 decision. If it is, its rows have already informed the earlier analysis's evaluation, though not this rerun's choices.
- The earlier analysis is the reference and is not edited. Its scripts (`Code/01_…08_*.py`), core (`Code/core.py`) and outputs are not read or changed by this rerun. This rerun's files are named `Code/hf2_*`, `Code/hf2/core.py` and `Code/outputs/hf2/`.

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

*Written in step 2, before anything is trained. Three parts. `Discussion`: how the problem was arrived at, what was ruled out, and whether it is a prediction problem. `Problem`: what is predicted, from what, the output type, the agreed metric, the success criterion, the baseline and the achievable level, the must-have requirements, and any expectations the user states about the relationship (quoted). `Sub-tasks`: the separately answerable parts. Ends with the train/test split, its seed, and the statement that the test set is locked.*

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

## Recommendation

*Written at the end of step 4, one sub-heading per sub-task, after its single test-set evaluation: the thirteen-part Recommendation Report of `ML Guide.md` §25, assembled from the Decision Records. Nothing in it is new.*

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

## Code Summary

All scripts run from `Code/` with `uv run python <script>.py`. Names start with `hf2_`; the interim core will be `Code/hf2/core.py`; outputs go to `Code/outputs/hf2/`. The earlier analysis's files (`Code/core.py`, `Code/01_…08_*.py`, `Code/outputs/*.json`, `Code/outputs/figures/`) are not read or changed.

| File | What it does | Reads | Writes | Seeds / parameters |
| --- | --- | --- | --- | --- |
| `Code/hf2_01_describe_data.py` | Step 1 describing pass. Recomputes the SHA-256 and checks it against `SOURCE.md`. Describes each column: meaning, unit and type from the UCI variable table, the paper's range, distinct values, percentiles, zeros, non-integer values and 0/1 counts. Counts duplicates, class counts, row order and `time` by `DEATH_EVENT`. Draws no conclusions. | `Attachments/heart_failure_clinical_records_dataset.csv` | `Code/outputs/hf2/01_describe.json`, `01_describe.md` | none |

## References

- Ahmad, T., Munir, A., Bhatti, S. H., Aftab, M. and Raza, M. A. (2017). Survival analysis of heart failure patients: a case study. *PLoS ONE*, 12(7), e0181001. [https://doi.org/10.1371/journal.pone.0181001](https://doi.org/10.1371/journal.pone.0181001). Its data, `S1 Data.csv` ("DATA_MINIMAL", version 1, CC BY 4.0), are on figshare as article 5227684 (record checked through the figshare API, 28 October 2026). The link was checked on 28 October 2026.
- Chicco, D. and Jurman, G. (2020). Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone. *BMC Medical Informatics and Decision Making*, 20, 16. [https://doi.org/10.1186/s12911-020-1023-5](https://doi.org/10.1186/s12911-020-1023-5). Its *Dataset* section was read on 28 October 2026 from the open-access full text (Europe PMC, PMC6998201). The link was checked on 28 October 2026.
- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R). The variable table was read through the UCI API on 28 October 2026. The link was checked on 28 October 2026.
