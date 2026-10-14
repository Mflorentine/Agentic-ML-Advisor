# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

**Provenance.**
- **File:** `Attachments/heart_failure_clinical_records_dataset.csv`, downloaded by the user on 14 October 2026 from the UCI Machine Learning Repository (dataset 519, *Heart Failure Clinical Records*). Never modified.
- **SHA-256:** `9c73cea7468ff5d517801ec050fe9993da5912fce4b56f296f8df3b38dd75912`. Size 12,239 bytes.
- **Licence:** CC BY 4.0. Details are in `Attachments/SOURCE.md`.
- **Why this file:** the user chose it.
- **Who the patients are:** according to the paper that introduced this version (Chicco and Jurman, 2020, "Dataset" section), the file holds the medical records of 299 heart-failure patients, collected at the Faisalabad Institute of Cardiology and the Allied Hospital in Faisalabad, Pakistan, from April to December 2015. All of them had left ventricular systolic dysfunction and heart failure in NYHA class III or IV.

**Best available form: checked.** The same paper says the data was first released by Ahmad et al. (2017) with their PLOS ONE article. That release (`S1 Data.csv`, 12,486 bytes, published on figshare on 20 July 2017, CC BY 4.0) was downloaded to a temporary folder and compared with the UCI file:
- it holds the same 299 records with identical values;
- only the column names differ (for example `Pletelets`, `Gender`, `Event`);
- so does the row order: the UCI file is sorted by `time`.

No fuller version was found, and the UCI copy is used. The temporary copy was deleted.

**Shape and coverage.**
- 299 rows (one per patient, according to the paper) × 13 columns. All values are numeric.
- 0 missing cells, 0 duplicate rows.
- The rows are sorted by `time` in ascending order.

**Columns.** Meanings and units are as documented on the UCI page. All are clinical measurements or recorded clinical facts; none is a model output.

| Column | Meaning | Unit | Range (median) | Notes |
| --- | --- | --- | --- | --- |
| `age` | age of the patient | years | 40–95 (60) | 47 distinct values; two are 60.667 (see below) |
| `anaemia` | decrease of red blood cells or hemoglobin | boolean | 0: 170 · 1: 129 | Defined by the hospital physician as haematocrit below 36 % (Chicco and Jurman, 2020) |
| `creatinine_phosphokinase` | level of the CPK enzyme in the blood | mcg/L | 23–7861 (250) | Right-skewed: the median is 250, the maximum 7861 |
| `diabetes` | if the patient has diabetes | boolean | 0: 174 · 1: 125 | |
| `ejection_fraction` | percentage of blood leaving the heart at each contraction | % | 14–80 (38) | 17 distinct values |
| `high_blood_pressure` | if the patient has hypertension | boolean | 0: 194 · 1: 105 | The original article gives no definition of high blood pressure (Chicco and Jurman, 2020) |
| `platelets` | platelets in the blood | kiloplatelets/mL | 25,100–850,000 (262,000) | |
| `serum_creatinine` | level of serum creatinine in the blood | mg/dL | 0.5–9.4 (1.1) | Right-skewed |
| `serum_sodium` | level of serum sodium in the blood | mEq/L | 113–148 (137) | |
| `sex` | woman or man | binary | 0: 105 · 1: 194 | The file doesn't say which code is which. The paper reports 105 women and 194 men, which matches 0 = woman, 1 = man |
| `smoking` | if the patient smokes or not | boolean | 0: 203 · 1: 96 | |
| `time` | follow-up period | days | 4–285 (115) | Varies from patient to patient; the paper gives the average follow-up as 130 days |
| `DEATH_EVENT` | if the patient died during the follow-up period | boolean | 0: 203 · 1: 96 | The UCI page marks it as the target |

**Oddities found.** The decisions about them are under *Step 1 decisions* below.
- **Non-integer ages.** Two patients have age 60.667, though `age` is documented as an integer in years. The original 2017 release has the same two values, so they don't come from the UCI conversion.
- **Matching counts.** `smoking` and `DEATH_EVENT` happen to have the same counts (203 / 96). This was noted, not interpreted.

**Machine learning checks** (describing pass; nothing decided yet).
- **Candidate target:** `DEATH_EVENT`. The labels record whether the patient died before the end of their own follow-up period (Chicco and Jurman, 2020). Follow-up lengths differ between patients (4–285 days), so a 0 means "did not die during this patient's follow-up", not "survived for a fixed length of time".
- **Output type it suggests:** binary (P1, to be confirmed in step 2).
- **Class counts:** 203 with `DEATH_EVENT` = 0 and 96 with 1 (32.1 %).
- **Inputs:** 12 besides the target. After one-hot encoding there are still 12, because the five categorical inputs are already 0/1 (P3).
- **Categorical share:** 5 of 12 inputs (42 %): `anaemia`, `diabetes`, `high_blood_pressure`, `sex`, `smoking` (P4).
- *Superseded on 14 October 2026:* with `time` set aside, there are 11 inputs, and 5 of 11 (45 %) are categorical. See *Step 1 decisions*.
- **Column that could leak the target: `time`.** It is the length of the follow-up period, and that period ends either when the patient dies or when follow-up stops. So its value is fixed at the same moment as the outcome. Whether to keep it as an input is a decision for the user (see Analysis Log row 4).

**Step 1 decisions** (14 October 2026, by the user).

| Decision | What was decided, and why | What it costs |
| --- | --- | --- |
| **Provenance** | The UCI copy is used; the original 2017 release holds the same records (see above). | Nothing. |
| **Units** | As documented on the UCI page; all columns are measurements or recorded clinical facts. | `sex` coding is inferred from the paper's counts, not documented in the file. |
| **Scope** | All 299 rows are used. | None. |
| **Missing data** | There are no missing values, so nothing is imputed or dropped. | None. |
| **Panel structure** | None: one row per patient, and no patient appears twice (DR-02). | None. |
| **Cleaning** | No value was altered or set to missing. | None. |
| **Accepted as-is** | The two ages of 60.667 are kept as they are; the original 2017 release has them too. | `age` is documented as whole years but has two non-integer values. |
| **Admissibility** | ADM-1: `DEATH_EVENT` is the recorded output (DR-01). ADM-3: no grouping; the row order only reflects sorting by `time`, so the data is shuffled before any split (DR-02). ADM-4: yes, for similar patients only (DR-03). ADM-2 is asked in step 2. | The model applies only to patients like these (see the limitations below). |
| **Target and leakage** | Target: `DEATH_EVENT`. **`time` is set aside as an input**, because the follow-up period ends at death or at the end of follow-up, so its value is fixed at the same moment as the outcome. It stays in the file but is never used to predict. | 11 inputs remain: 6 numeric, and 5 categorical already coded 0/1. One-hot encoding adds nothing, and the categorical share is 5 of 11 (45 %). |
| **Experience level** | Intermediate. | — |

**Limitations recorded in step 1.** Each will be carried to the Recommendation Report and the `Discussion`.
- **Population (from DR-03).** The model is meant only for patients like these: severe heart failure (NYHA class III–IV), two hospitals in Faisalabad, Pakistan, 2015.
- **What a 0 means (user's instruction).** Follow-up length varies from 4 to 285 days. So `DEATH_EVENT` = 0 means "did not die during this patient's follow-up", not "survived a fixed period".

**Experience level.** The user's stated experience with machine learning is **intermediate**.

## Problem Definition

*Written in step 2, before anything is trained. Three parts. `Discussion`: how the problem was arrived at, what was ruled out, and whether it is a prediction problem. `Problem`: what is predicted, from what, the output type, the agreed metric, the success criterion, the baseline and the achievable level, the must-have requirements, and any expectations the user states about the relationship (quoted). `Sub-tasks`: the separately answerable parts. Ends with the train/test split, its seed, and the statement that the test set is locked.*

## Analysis

*The workings, one sub-heading per sub-task, added as steps 3 and 4 proceed: exploration of the training data, cross-validation tables, learning curves, diagnostics, error analysis, checks that changed nothing, and anything computed but not reported.*

## Decision Records

### DR-01 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-14
- **Question:** Is there a recorded output y for the rows to be learned from (ADM-1)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `DEATH_EVENT` | recorded for all 299 rows: 203 × 0, 96 × 1; marked as the target on the UCI page | M | `Code/outputs/01_describe.json`; UCI dataset page |
| Meaning | "if the patient died during the follow-up period" | M | UCI variables table |
| User's answer | "Yes, DEATH_EVENT is the target." | M | user, 14 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-1 | yes | [B p.15] | supervised problem; continue |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** continue with `DEATH_EVENT` · another column · stop
- **Expectation:** n/a
- **Decision:** `DEATH_EVENT` is the recorded output. The problem is supervised, so the work continues.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Yes, DEATH_EVENT is the target."
- **Supersedes / superseded by:** n/a
- **Links:** `Code/01_describe_data.py`, `Code/outputs/01_describe.md`

### DR-02 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-14
- **Question:** Do several rows belong to the same unit, or are rows ordered in time (ADM-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Identifier or date column | none in the file | M | `Code/outputs/01_describe.md` |
| Rows per patient | one row per patient (299 patients) | M | Chicco and Jurman (2020), "Dataset" section |
| Row order | ascending by `time` | M | `Code/outputs/01_describe.json` (`rows_sorted_by_time: true`) |
| User's answer | "No grouping, one row per patient. The row order only reflects sorting by time and is not a meaningful sequence, so the data must be shuffled before any split." | M | user, 14 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-3 | none: no group column, no time-ordered sequence | [B pp.16, 38–39, 329] | random split and random folds |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** random split · group split · time-ordered reformulation
- **Expectation:** n/a
- **Decision:** No grouping and no time sequence, so splits and folds are random. Because the file is sorted by `time`, **the data is shuffled before any split**. The step 2 `SPLIT` record must show the shuffle and its seed.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/01_describe.json`

### DR-03 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-14
- **Question:** Will the cases the model is used on look like the data we have (ADM-4)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Population of the data | 299 heart-failure patients, NYHA class III–IV, left ventricular systolic dysfunction, Faisalabad Institute of Cardiology and Allied Hospital, Pakistan, April–December 2015 | M | Chicco and Jurman (2020), "Dataset" section |
| User's answer | "Yes, but the model is only meant for similar patients (severe heart failure, NYHA class III-IV, two hospitals in Pakistan, 2015). Record this as a limitation." | M | user, 14 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-4 | yes, within the stated population | [B pp.328–329] | validation and test data are drawn from this file |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** use this file for validation and test · obtain data from the intended population
- **Expectation:** n/a
- **Decision:** Validation and test data come from this file. The intended use is limited to patients like these, and that limitation is recorded in the Data Summary to be carried into the Recommendation Report (part 10) and the `Discussion`.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** Data Summary, *Limitations recorded in step 1*

## Recommendation

*Written at the end of step 4, one sub-heading per sub-task, after its single test-set evaluation: the thirteen-part Recommendation Report of `ML Guide.md` §25, assembled from the Decision Records. Nothing in it is new.*

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Source file placed in `Attachments/` by the user; provenance, licence and SHA-256 recorded | `Attachments/SOURCE.md` |
| 2 | Best available form checked: the original 2017 figshare release (Ahmad et al.) downloaded to a temporary folder and compared record by record. Same 299 records and values; only column names and row order differ. UCI copy kept; temporary copy deleted | Data Summary |
| 3 | Step 1 describing pass: shape, types, ranges, missing values, duplicates, binary counts, documented meanings and units | `Code/outputs/01_describe.md`, `Code/outputs/01_describe.json` |
| 4 | Machine learning checks described. Open: admissibility answers (ADM-1, ADM-3, ADM-4); whether `time` stays as an input; whether the two non-integer ages are left as they are | Data Summary |
| 5 | User's answers recorded. ADM-1: `DEATH_EVENT` is the target (DR-01). ADM-3: no grouping; shuffle before any split (DR-02). ADM-4: yes, for similar patients only, recorded as a limitation (DR-03). `time` set aside as an input (leakage risk). Ages of 60.667 accepted as-is. All 299 rows used. Variable follow-up recorded as a limitation. Step 1 closed. | Data Summary; DR-01 to DR-03 |

## Code Summary

| File | What it does | Reads | Writes | Run |
| --- | --- | --- | --- | --- |
| `Code/01_describe_data.py` | Step 1 describing pass. Per column: documented meaning and unit, type, missing values, distinct values, min / median / max, zeros, 0/1 counts, non-integer values. Whole file: checksum, size, shape, duplicates, sort order. No random steps. | `Attachments/heart_failure_clinical_records_dataset.csv` | `Code/outputs/01_describe.json`, `Code/outputs/01_describe.md` | `cd Code && uv run python 01_describe_data.py` |

**Environment:** Python 3.12.15 with pandas 3.0.5 (`Code/check_env.py`, 14 October 2026).

## References

- Ahmad, T., Munir, A., Bhatti, S. H., Aftab, M. and Raza, M. A. (2017). [Survival analysis of heart failure patients: a case study](https://doi.org/10.1371/journal.pone.0181001). *PLoS ONE*, 12(7), e0181001. The article itself was not opened; its data supplement ([S1 Data](https://doi.org/10.1371/journal.pone.0181001.s001)) was downloaded and compared (Analysis Log row 2).
- Chicco, D. and Jurman, G. (2020). [Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone](https://doi.org/10.1186/s12911-020-1023-5). *BMC Medical Informatics and Decision Making*, 20, 16. The "Dataset" section was read.
- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R).
