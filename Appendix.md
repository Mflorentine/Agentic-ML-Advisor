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

### Discussion

- **The problem, in the user's words:** "Flag heart failure patients at high risk of dying during follow-up, so they can be monitored more closely."
- **It is a prediction problem** (ADM-2, DR-04): "the aim is prediction for new patients, not explaining causes." Explaining which factors cause death was ruled out as the aim.
- **One sub-task.** A second sub-task — the same prediction from serum creatinine and ejection fraction alone, the question of Chicco and Jurman (2020) — was offered and not taken up.
- **Feasibility.** `DEATH_EVENT` is recorded for every row, so the output is there. There are 239 training rows for 11 inputs (P2 ample). The rows are independent (DR-02). All configurations needed are in scope.
- **Two consequences, raised with the user at the end of step 2 and resolved on 14 October 2026:**
  - **The P6 must-have narrows the comparison.** In `ML Guide.md` §12, the must-have "probabilities and a tuned decision threshold" is met by the Logistic family only (`[B→I pp.50, 53–54]`). k-NN and decision trees will therefore be excluded with code `USER` in step 4a, so the comparison will cover the four logistic configurations only. *Resolved (DR-09):* P6 is now a strong preference, not a must-have, so all families stay in the comparison.
  - **The F2 target of 0.6 is met by a trivial classifier.** Flagging every patient gives recall 1 and precision equal to the share of deaths. On the training rows, that is F2 = 5 × 0.3222 / (4 × 0.3222 + 1) = **0.7038**; on the full file it is 0.7028. That is above the target of 0.6, without any model. The "never flag" baseline (the most common class) scores F2 = 0. *Resolved (DR-08):* success is now judged against the flag-everyone reference.

### Problem

- **Predicted:** y = `DEATH_EVENT` (1 = died during the patient's follow-up), from x = 11 inputs: `age`, `anaemia`, `creatinine_phosphokinase`, `diabetes`, `ejection_fraction`, `high_blood_pressure`, `platelets`, `serum_creatinine`, `serum_sodium`, `sex`, `smoking`. `time` is not an input (step 1). **P1:** binary.
- **What a prediction is for:** flagging high-risk patients for closer monitoring.
- **Error costs:** missing a patient who dies (a false negative) is worse than a false alarm.
- **Metric:** F_β with β = 2, which weights recall twice as heavily as precision (p. 92). It is **one metric for everything**: choosing the model, tuning the threshold and judging success. This follows finding E1 from the third demonstration.
- **Success criterion** (DR-08): **test F2 above the flag-everyone reference (F2 = 0.7038 on the training rows) by more than the spread of F2 across the 10 outer cross-validation folds**. The spread is the standard deviation of the recommended configuration's per-fold F2. No second metric.
  - *Superseded (DR-05):* "F2 clearly above the baseline's 0, with a target of F2 ≥ 0.6. The 0.6 is my own choice, not from the book." Replaced because flagging every patient already reaches F2 = 0.7038.
- **Baselines** (DR-08). Both are reported beside every result:
  - the **always-negative baseline**, the most common training class (no death), with F2 = 0 (pp. 330–331);
  - the **flag-everyone classifier**, the **reference baseline for F2**, with F2 = 0.7038 on the training rows.
- **Achievable level:** unknown.
- **P5:** inspectable predictions are a **preference, not a must-have**. Bounded predictions are not needed.
- **P6:** yes — class probabilities and a tuned decision threshold, as a **strong preference, not a must-have** (DR-09). *Superseded (DR-05, DR-07):* must-have.
- **P7:** no. "The model is only used within the ranges in this data."
- **P8:** unknown. The user's expectation, quoted: "higher serum_creatinine and lower ejection_fraction go with a higher risk of death" (as reported by Chicco and Jurman, 2020). This expects a *direction* for two inputs, not a *shape* (linear, curved or interacting), so it doesn't set P8 and enters no matrix entry. It is kept for comparison with the fitted model in steps 4–5.

### Sub-tasks

1. Predict `DEATH_EVENT` from the 11 inputs.

### Split and test-set lock

- **The split** (DR-06): shuffled (DR-02), stratified by `DEATH_EVENT`, 20 % test, seed 2026. `Code/02_split.py` produced `Code/outputs/split.json`.
- **Training:** 239 rows (162 no death, 77 deaths; 32.2 %). **Test:** 60 rows (41, 19).
- **The test set is locked as of 14 October 2026.** No code in steps 3 and 4 reads the test rows until the single final evaluation (step 4g).

### Uncertainty interval for the test result: decided

Decided on 14 October 2026 (DR-08). The method had to come from chapters 2, 3, 4 and 13; the bootstrap is chapter 8 and out of scope.
- **Accepted.** Report the test F2 together with the number of test rows and of positives (60 rows, 19 positives). As its measure of uncertainty, give the spread of F2 across the 10 outer cross-validation folds, for the same configuration and threshold.
  - Basis: the book's k-fold cross-validation (pp. 72–73), and its point that a hold-out estimate is less variable the larger the hold-out set (p. 71). Using the fold spread as an interval is our step: `[B→I]`.
  - What this is: an indication of how much F2 varies between data sets of this size, not a confidence interval in the strict sense.
- **Not used.** Binomial intervals for test recall and test precision were offered as an optional addition and skipped by the user, because they are outside chapters 2, 3, 4 and 13.

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

### DR-04 · ADM · step 2

- **Sub-task:** all
- **Date:** 2026-10-14
- **Question:** Is the main aim to predict the outcome for new cases, or to understand how the variables are connected (ADM-2)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| User's problem | "Flag heart failure patients at high risk of dying during follow-up, so they can be monitored more closely." | M | user, 14 October 2026 |
| User's answer | "the aim is prediction for new patients, not explaining causes" | M | user, 14 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-2 | predict | [B p.20] | continue with this workflow |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** predict · understand
- **Expectation:** n/a
- **Decision:** The aim is prediction for new patients.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** Problem Definition, *Discussion*

### DR-05 · FORM · step 2

- **Sub-task:** 1 — predict `DEATH_EVENT` from the 11 inputs
- **Date:** 2026-10-14
- **Question:** What is predicted, from what, and how will success be judged?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| y | `DEATH_EVENT` (1 = died during the patient's follow-up) | M | DR-01 |
| x | 11 inputs; `time` excluded (leakage, step 1) | M | Data Summary, *Step 1 decisions* |
| P1 | binary | M | user: "binary output" |
| Use | "flag high-risk patients for closer monitoring" | M | user |
| Error costs | "Missing a patient who dies (false negative) is worse than a false alarm." | M | user |
| Metric | F_β, β = 2, "used for choosing the model, tuning the threshold and judging success alike" | M | user |
| Success criterion | "F2 clearly above the baseline's 0, with a target of F2 >= 0.6. The 0.6 is my own choice, not from the book." | M | user |
| Baseline | most common training class (no death), F2 = 0 | M | §2 |
| Achievable level | unknown | M | user |
| P5 | inspectable: a preference, not a must-have; bounded: not needed | M | user |
| P6 | must-have: "probabilities and a tuned decision threshold" | M | user |
| P7 | no: "the model is only used within the ranges in this data" | M | user |
| P8 | unknown. Direction expected: "higher serum_creatinine and lower ejection_fraction go with a higher risk of death" | M | user (citing Chicco and Jurman, 2020) |
| Flag-everyone reference | F2 = 0.7038 on the training rows (5 × 0.3222 / (4 × 0.3222 + 1)) | M | class share from `Code/outputs/split.json` (training counts) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §2 one metric, agreed up front | F2 for selection, threshold and success | [B p.330] | — |
| §5.5 F_β for asymmetric errors | β = 2 | [B p.92] | — |
| §2 baseline | most common training class | [B pp.330–331] | — |
| §16 decision threshold | tuned after selection, on training data, for F2 | [B→I pp.53–54, 92–93] | — |
| §12 must-have P6 = yes | met by the Logistic family only | [B→I pp.50, 53–54] | k-NN and Tree will be excluded (`USER`) in step 4a |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Success target (user's own) | F2 ≥ 0.6 | to be compared in step 4g |

- **Options considered:** misclassification rate · F2 as the single metric
- **Expectation:** n/a
- **Decision:** One sub-task: `DEATH_EVENT` from 11 inputs, binary. F2 decides everything: model choice, threshold and success. Success means F2 clearly above 0, with a target of F2 ≥ 0.6. P5 is a preference; P6 is a must-have; P7 is no; P8 is unknown.
- **Raised with the user, unresolved:** (1) the flag-everyone reference reaches F2 = 0.7038 on the training rows, above the target of 0.6; (2) the P6 must-have leaves only the four logistic configurations admissible.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — every item quoted above
- **Supersedes / superseded by:** superseded by DR-08 (success criterion, baselines, P6, uncertainty method)
- **Links:** Problem Definition

### DR-06 · SPLIT · step 2

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** How are training and test data separated?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| ADM-3 | no grouping; the file is sorted by `time`, so shuffle before any split | M | DR-02 |
| User's choice | "20% test, stratified by DEATH_EVENT, seed 2026" | M | user, 14 October 2026 |
| Result | 239 training rows (162 / 77), 60 test rows (41 / 19); no overlap; all 299 rows covered | M | `Code/outputs/split.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §3 test data used once | test set locked | [B pp.74, 328] | no code in steps 3–4 reads the test rows until step 4g |
| §3 split randomly | shuffled before splitting | [B pp.71, 73] | the sort by `time` is undone |
| Stratified by `DEATH_EVENT` | both parts keep the share of deaths (32.2 % / 31.7 %) | [I] | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Test fraction | 0.2 | 60 of 299 rows |

- **Options considered:** random stratified split · group split (not needed, DR-02)
- **Expectation:** n/a
- **Decision:** Shuffled, stratified split, seed 2026: 239 training and 60 test rows. **The test set is locked.**

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/02_split.py`, `Code/outputs/split.json`

### DR-07 · PROP · step 2

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** What are the property values known before any model is fitted (P1–P8)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 | binary | M | DR-05 |
| P2 | ample: 239 / (11 + 1) = 19.917 | M | `Code/outputs/split.json` (n_train) |
| P3 | few: 11 inputs after encoding (the five categorical inputs are already 0/1) | M | `split.json` (inputs) |
| P4 | low: 5 of 11 categorical (45 %) | M | Data Summary |
| P5 | inspectable, not a must-have | M | DR-05 |
| P6 | yes, must-have | M | DR-05 |
| P7 | no | M | DR-05 |
| P8 | unknown (a direction is expected for two inputs; see DR-05) | M | DR-05 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P2 definition | n_train ÷ (inputs after encoding + 1) | [I] | ample |
| P3 definition | inputs after encoding | [I] threshold | few |
| P4 definition | share of categorical inputs | [I] threshold | low |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited ratio | < 10 | 19.917 |
| P3 many inputs | > 20 | 11 |
| P4 high categorical share | ≥ 50 % | 45 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** Record P1–P8 as above. P9 and P10 are computed from the training rows in step 3.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed
- **Supersedes / superseded by:** superseded by DR-09 (P6 no longer a must-have)
- **Links:** `Code/outputs/split.json`

### DR-08 · FORM · step 2

- **Sub-task:** 1 — predict `DEATH_EVENT` from the 11 inputs
- **Date:** 2026-10-14
- **Question:** How is success judged, against which baselines, and how is the uncertainty of the test result stated?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Flag-everyone reference | F2 = 0.7038 on the training rows (recall 1, precision 0.3222) | M | DR-05; class counts in `Code/outputs/split.json` |
| User's decision, success | "test F2 clearly above the flag-everyone reference (F2 = 0.70 on the training rows). "Clearly" means by more than the spread of F2 across the outer cross-validation folds." | M | user, 14 October 2026 |
| User's decision, baselines | "Record the flag-everyone classifier as the reference baseline for F2, alongside the always-negative baseline. Supersede the earlier 0.6 target; don't delete it. No second metric." | M | user, 14 October 2026 |
| User's decision, P6 | "change it from a must-have to a strong preference, so all model families stay in the comparison" | M | user, 14 October 2026 |
| User's decision, uncertainty | "accept the fold-spread proposal, tagged [B->I]. Skip the optional binomial intervals" | M | user, 14 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §2 baseline | always-negative baseline kept | [B pp.330–331] | F2 = 0 |
| Flag-everyone reference baseline | added as the comparison point for F2 | [I] | success = test F2 > 0.7038 + fold spread of F2 |
| §5.5 F_β | F2 stays the single metric | [B p.92] | no second metric |
| k-fold spread as the uncertainty of the test result | spread of F2 across the 10 outer folds, reported with n = 60 and 19 positives | [B→I pp.71–73] | the method for step 4g's interval |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Success | test F2 > 0.7038 + spread of F2 across the outer folds | to be compared in step 4g |

- **Options considered:** keep the 0.6 target · compare against the flag-everyone reference · add a second metric (rejected by the user)
- **Expectation:** n/a
- **Decision:** Success means test F2 above the flag-everyone reference (0.7038) by more than the spread of F2 across the outer folds. Two baselines are reported: always-negative (F2 = 0) and flag-everyone (the reference for F2). P6 is a strong preference, not a must-have. Uncertainty is the fold spread, `[B→I]`; no binomial intervals.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** supersedes DR-05 (success criterion, baseline, P6; all other items of DR-05 stand)
- **Links:** Problem Definition

### DR-09 · PROP · step 2

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** What are the property values after P6 changed (P1–P8)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1, P2, P3, P4, P5, P7, P8 | unchanged from DR-07: binary; ample (19.917); few (11); low (45 %); inspectable, a preference; no; unknown | M | DR-07 |
| P6 | yes, a **strong preference, not a must-have** | M | DR-08 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §12 must-haves | none: P6 is no longer a gate | [B→I pp.50, 53–54] | k-NN and Tree stay admissible |
| §13 P6=yes→Logistic | applies as a preference | [B→I pp.50, 53–54] | +1 on all Logistic configurations in step 4b |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| as DR-07 | | |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** P6 = yes, as a preference. The matrix (§13) gives every preference the same +1, so "strong" can't be expressed as extra weight. It counts like any other preference entry.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — DR-08
- **Supersedes / superseded by:** supersedes DR-07
- **Links:** DR-08

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
| 6 | Step 2: problem stated by the user; ADM-2 answered: prediction (DR-04) | Problem Definition; DR-04 |
| 7 | Formulation agreed: binary `DEATH_EVENT` from 11 inputs; F2 as the single metric for selection, threshold and success; target F2 ≥ 0.6 (user's own); P5 preference, P6 must-have, P7 no, P8 unknown (DR-05). Two consequences raised with the user: the flag-everyone reference F2 = 0.7038 is above the target; P6 as a must-have leaves only the Logistic family | Problem Definition; DR-05 |
| 8 | Shuffled, stratified split, seed 2026: 239 training / 60 test rows. **Test set locked** (DR-06) | `Code/02_split.py`, `Code/outputs/split.json` |
| 9 | Properties P1–P8 recorded: P2 ample (19.917), P3 few (11), P4 low (45 %) (DR-07) | DR-07 |
| 10 | Uncertainty interval for the test result: an in-scope method proposed (fold spread of F2 with n and positives, `[B→I]`); binomial intervals as an optional `[I]` addition. Decision deferred to step 4 | Problem Definition |
| 11 | Problem and sub-task written into the `Introduction` of `Report.md` | `Report.md` |
| 12 | Success criterion changed: test F2 above the flag-everyone reference (0.7038 on the training rows) by more than the fold spread of F2. The flag-everyone classifier is added as the reference baseline for F2. The 0.6 target is superseded, not deleted (DR-08 supersedes DR-05) | DR-08 |
| 13 | P6 changed from a must-have to a strong preference, so all families stay in the comparison (DR-09 supersedes DR-07) | DR-09 |
| 14 | Uncertainty method decided: spread of F2 across the outer folds, with n and positives, `[B→I]`; binomial intervals not used (DR-08) | DR-08 |
| 15 | `Introduction` checked against the new criterion; its success sentence updated from the superseded 0.6 target. Step 2 closed | `Report.md` |

## Code Summary

| File | What it does | Reads | Writes | Run |
| --- | --- | --- | --- | --- |
| `Code/01_describe_data.py` | Step 1 describing pass. Per column: documented meaning and unit, type, missing values, distinct values, min / median / max, zeros, 0/1 counts, non-integer values. Whole file: checksum, size, shape, duplicates, sort order. No random steps. | `Attachments/heart_failure_clinical_records_dataset.csv` | `Code/outputs/01_describe.json`, `Code/outputs/01_describe.md` | `cd Code && uv run python 01_describe_data.py` |
| `Code/02_split.py` | Step 2 split: shuffled, stratified by `DEATH_EVENT`, 20 % test. Records the row indices, class counts, the inputs (11) and the column set aside (`time`). **Seed 2026.** After this, nothing reads the test rows until step 4g. | `Attachments/heart_failure_clinical_records_dataset.csv` | `Code/outputs/split.json` | `cd Code && uv run python 02_split.py` |

**Environment:** Python 3.12.15 with pandas 3.0.5 (both scripts) and scikit-learn 1.9.1 (`02_split.py`) (`Code/check_env.py`, 14 October 2026).

## References

- Ahmad, T., Munir, A., Bhatti, S. H., Aftab, M. and Raza, M. A. (2017). [Survival analysis of heart failure patients: a case study](https://doi.org/10.1371/journal.pone.0181001). *PLoS ONE*, 12(7), e0181001. The article itself was not opened; its data supplement ([S1 Data](https://doi.org/10.1371/journal.pone.0181001.s001)) was downloaded and compared (Analysis Log row 2).
- Chicco, D. and Jurman, G. (2020). [Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone](https://doi.org/10.1186/s12911-020-1023-5). *BMC Medical Informatics and Decision Making*, 20, 16. The "Dataset" section was read.
- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R).
