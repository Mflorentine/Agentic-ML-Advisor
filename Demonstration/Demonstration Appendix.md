# Appendix

This analysis was carried out when these files were called Report.md and Appendix.md; they were renamed on 15 October 2026.

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

### Sub-task 1 — predict `DEATH_EVENT` from the 11 inputs

**Step 3: training data only (239 rows).** The test rows were not read.

**Properties from the training rows** (interim core `Code/core.py`, version `e614fd79d15a…`; DR-10):
- **P9 (separable):** no. Logistic regression with negligible regularisation (C = 10⁸) classifies 0.7699 of the training rows correctly, not 100 %. MOD-1 therefore does not apply.
- **P10 (imbalance):** balanced. The smallest class is 77 of 239 = 0.3222, above the 20 % threshold.

**Figures of the training data** (all in `Report.md`, *Results*, with light and dark versions in `Code/outputs/figures/`):
- **Figure 1:** the six numeric inputs, as histogram outlines by outcome, with heights as the share of each group. Serum creatinine and CPK are on a log axis, for display only.
- **Figure 2:** the share who died within each level of the five yes/no inputs, with the training share (32.2 %) as a reference line.
- **Figure 3:** serum creatinine (log axis) against ejection fraction, one point per patient, coloured by outcome.

The figures do not set P8, which stays `unknown` (DR-09, DR-10).

**Figures as first drafted, changed before use.** In the first versions of Figures 1 and 3, the translucent fills mixed into an unexplained colour, the legend covered bars, the log axes showed 10⁰-style labels, and one count in Figure 2 collided with the reference line. All four were fixed before the figures entered the report. Only the presentation changed; no number did.

**Input design, decided (DR-11):** `serum_creatinine` and `creatinine_phosphokinase` enter every model as their natural logarithm. The display log scale above didn't decide this; the user did, after the trade-offs were set out (Analysis Log row 20). The reasons are the skew of the two inputs in the training rows, not how they relate to the outcome: serum creatinine has a maximum of 9.0 against a median of 1.1 (skew 4.19), and CPK 7861 against 250 (skew 4.56). Both minimums are above zero (0.6 and 23), so no offset is needed. The transform is a fixed formula with nothing fitted, so it can't carry information from the test rows.

**Step 4: the interim core extended.** `Code/core.py` now implements §12, §13/§15, §16, §17, §18 (observations), §19 and the single test evaluation, as well as §11 P9–P10. It was shown to the user and approved before any of its output was used. Before that, a smoke test on synthetic random data, in a scratch folder outside the project, ran every command. The choices Part II leaves open are listed as interpretations a–k in the file's docstring. At the user's request, the docstring for interpretation c was corrected: standardising each numeric input before raising it to powers gives the same fit only without regularisation, because with L2 it changes which curves the penalty shrinks. The version used from 4a on is `e5e819e3…`.

**P9 rechecked with the log transform.** DR-10 computed P9 on the raw inputs, before DR-11 decided to log two of them. The core now applies the log transform in `p9p10`. Re-run, P9 is still no, with the same training accuracy, 0.7699. No new `PROP` record was needed (DR-12).

**The λ conversion for L2 checked against eq. 3.50.** The user asked for this before any L2 result is reported. The book's regularised logistic regression (eq. 3.50, printed p. 61, 2nd edition draft of 1 September 2026, read at smlbook.org) minimises (1/n)Σ ln(1 + exp(−yᵢθᵀxᵢ)) + λ‖θ‖², and p. 60 (footnote 5) suggests leaving the intercept out of the penalty. scikit-learn 1.9.1 minimises (1/n)Σ loss + ‖w‖²/(2Cn), intercept unpenalised (`l2_reg_strength = 1/(C·n)` in its source). So the two match when C = 1/(2nλ), which is what `BookLogistic` uses.

`Code/06_check_eq350.py` tests this numerically. It minimises eq. 3.50 directly on synthetic data (200 rows, 5 inputs) and compares the result with `BookLogistic`:
- `BookLogistic` agrees to within 3.7 × 10⁻⁴ for λ = 10⁻³, 10⁻², 10⁻¹ and 1, which is scikit-learn's default solver tolerance.
- A deliberately wrong conversion, C = 1/(nλ), is off by 0.05 to 0.18.

So the check can tell a wrong conversion from the right one (`Code/outputs/check_eq350.txt`).

**Limitation recorded in step 4 (user's instruction).** Configurations are compared at the default threshold r = 0.5 (§16), and the threshold is tuned for F2 only on the chosen configuration. Selection at r = 0.5 may therefore not pick the configuration that would be best after threshold tuning. This is to be carried into the Recommendation Report (part 10) and the `Discussion`.

**Step 4h: the final tree's splits, from a verified rebuild.** `final` (step 4g) fitted the tree in memory and saved only its test predictions, so no saved model existed. At the user's decision, the core's new `explain` command rebuilds it:
- **Same code path and settings as `final`:** the same `build` function, depth 3, minimum leaf 20, the 239 training rows, `random_state` 2026.
- **Accepted only if bit-identical.** It is accepted as the same model only if its probabilities for the 60 test patients equal the saved `p_death` exactly. The check reads the test inputs only: no outcome is read and no metric is computed.

The first run failed the check by at most 5.6 × 10⁻¹⁷. The cause was in reading the file, not in the model: pandas' default `read_csv` float parser is not exact on round trips. With `float_precision="round_trip"`, all 60 probabilities are bit-identical. Only then was the model saved (`Code/outputs/core_final_model.joblib`) and its nodes written (`Code/outputs/core_tree_splits.json`).

This is a verified rebuild, not the original object. The core version changed from `434ff8cd…` to `48840eba…`, by adding `explain` and `test_inputs` only. None of the functions that produced DR-12 to DR-19 changed. The splits are in the Recommendation Report, part 9.

**Step 4h: Figure 4.** Proposed to and approved by the user. `Code/08_fig4_pr_curve.py` draws the precision–recall curve on the 60 test patients from the points `final` saved in `core_final.json`. Nothing is refitted or recomputed. The operating point at r = 0.2 and the flag-everyone point are ringed, and a dashed line marks the random-classifier precision (0.32). The first draft's r = 0.2 label overlapped the curve, so it was moved below the curve before the figure entered the report.

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
- **Supersedes / superseded by:** supersedes DR-05 (success criterion, baseline, P6; all other items of DR-05 stand); superseded in part by DR-11 (representation of two inputs; all other items stand)
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
- **Supersedes / superseded by:** supersedes DR-07; superseded by DR-10 (P9 and P10 added)
- **Links:** DR-08

### DR-10 · PROP · step 3

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Are the classes perfectly separable (P9), and are they imbalanced (P10), in the training data?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P9 | no: training accuracy 0.7699 with negligible regularisation (C = 10⁸) | T | `Code/outputs/core_p9_p10.json` |
| P10 | balanced: smallest class 77 of 239 (0.3222) | T | `Code/outputs/core_p9_p10.json` |
| P1–P8 | unchanged from DR-09 | M | DR-09 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P9 test | not separable | [I] procedure | MOD-1 does not apply; unregularised `Logistic` stays admissible |
| P10 test | balanced | [I] threshold | no change to metric or threshold handling |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P9 separability | 100 % training accuracy, C = 10⁸ | 76.99 % |
| P10 imbalance | smallest class < 20 % | 32.22 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** The full property set is: P1 binary, P2 ample (19.917), P3 few (11), P4 low (45 %), P5 inspectable (a preference), P6 yes (a strong preference, not a must-have), P7 no, P8 unknown, P9 no, P10 balanced.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

**Reference code**

- Function: `core.p9_p10` · version `e614fd79d15a403a5dc0dd5703f2af37884a76eb075dc6aa798248cdcc4e2f30` (SHA-256 of `Code/core.py`; **interim core, not reviewed**; shown to the user before its output was used) · inputs: the 239 training rows from `Code/outputs/split.json`, 11 inputs · output: `Code/outputs/core_p9_p10.json`

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "Yes, run core.py for P9 and P10 and record them in DR-10."
- **Supersedes / superseded by:** supersedes DR-09
- **Links:** `Code/core.py`, `Code/outputs/core_p9_p10.json`

### DR-11 · FORM · step 3

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Should `serum_creatinine` and `creatinine_phosphokinase` enter the models raw or log-transformed (input design, `ML Guide.md` §9)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `serum_creatinine`, training rows | min 0.6, median 1.1, max 9.0 (max ÷ median 8.2), skew 4.19 | T | step 3 check on the 239 training rows; Analysis |
| `creatinine_phosphokinase`, training rows | min 23, median 250, max 7861 (max ÷ median 31.4), skew 4.56 | T | as above |
| User decision | log both | M | quoted below |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design (§9): domain transformations allowed for every family, decided with the user | log both inputs | [B p.18] | the two inputs become log(value) in every configuration |
| k-NN: normalise inputs, distances otherwise dominated by the largest range | the tails of the two inputs pull less on distances | [B pp.26–27] | affects k-NN |
| Linear and logistic regression are not local | extreme values pull less on the fitted coefficients | [B→I p.47] | affects Logistic (± L2, ± poly); coefficients read per multiplicative change |
| Trees split on one input at a threshold | a monotone transform leaves the splits' partition unchanged | [I] | no effect on Tree |
| Polynomial terms | powers of log(value) rather than of value | [I] | changes the curve shapes available to `poly` |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** (a) log both; (b) keep both raw; (c) log one only.
- **Expectation:** n/a (not a configuration axis; not compared by cross-validation).
- **Decision:** log both, with the natural logarithm, in every configuration, applied as a fixed transform before scaling. The outcome was not used in the choice. The inputs stay the same 11 (P3 unchanged), and P1–P10 in DR-10 are unchanged.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** decided by the user — "Log both serum_creatinine and creatinine_phosphokinase as model inputs, because they are strongly skewed and the book allows it (p. 18) and says scaling matters for k-NN (pp. 26-27)."
- **Supersedes / superseded by:** supersedes DR-08 in part (representation of two inputs only; all other items stand)
- **Links:** Analysis (sub-task 1, step 3); `Code/outputs/split.json`

### DR-12 · ADMSET · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Which of the 14 configurations are admissible, given the task gate, the must-haves and the compulsory modifiers?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 | binary | M | DR-10; `Code/inputs/subtask1_props.json` |
| Must-haves | none (P5 and P6 are preferences) | M | DR-08, DR-09 |
| P9 | no, recomputed with the DR-11 log transform: training accuracy 0.7699 (C = 10⁸), unchanged from DR-10 | T | `Code/outputs/core_p9_p10.json` (core `e5e819e3…`) |
| MOD-2 inputs | without poly: 12 parameters, rank 12, n_train 239; with poly at degree 3: 24 parameters, rank 24 | T | `Code/outputs/core_admset.json` |
| Labels | `DEATH_EVENT` is a recorded clinical fact, not imputed, modelled or derived from the inputs | M | DR-01; Data Summary |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, P1 = binary | Logistic, k-NN, Tree admissible | [B pp.17, 49–57] | 8 regression configurations removed (`EXCL`) |
| Must-haves (§12) | none stated | [B→I p.347]; [B→I pp.50, 53–54] | nothing removed (`USER`) |
| MOD-1 | P9 = no: does not apply | [B p.61] | `Logistic` and `Logistic + poly` stay |
| MOD-2 | parameters < n_train and full rank, without and with poly: does not apply | [B→I pp.46–47, 65] | nothing removed |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P9 separability | 100 % training accuracy, C = 10⁸ | 76.99 % |

- **Options considered:** all 14 configurations of §9
- **Expectation:** n/a
- **Decision:** Six configurations are admissible: `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`, `kNN`, `Tree`.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] |
| `Poisson`, `Poisson + L2` | EXCL | task gate, P1 = binary |
| `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary |

**Reference code**

- Function: `core.admissible_set` (`core.py admset`) · version `e5e819e358426963350eb6d14f366877f4e3a896f0b09f9e85bfa2e6e853bd1a` (SHA-256 of `Code/core.py`; **interim core, not reviewed**). This is the version the user approved (`50569c5b…`), plus the comment-only corrections the user asked for: interpretation c in the docstring, the eq. 3.50 note, and the C2 baseline comment. · inputs: `Code/inputs/subtask1_props.json` (DR-10 values, copied unchanged) and the 239 training rows · output: `Code/outputs/core_admset.json`. Output copied unchanged; no disagreement.

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "core.py approved." P9: "yes, re-run p9p10 with the log transform first. If it is unchanged, note it in the ADMSET record". It is unchanged, so no new `PROP` record.
- **Supersedes / superseded by:** n/a
- **Links:** `Code/core.py`, `Code/outputs/core_p9_p10.json`, `Code/outputs/core_admset.json`

### DR-13 · PRIOR · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Which admissible configurations should be cross-validated, and in what expected order?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 | binary | M | DR-10 |
| P2 | ample (19.917) | M | DR-10 |
| P3 | few (11) | M | DR-10 |
| P4 | low (45 %) | M | DR-10 |
| P5 | inspectable, a preference: "inspectable predictions are a preference, not a must-have" | M | DR-05 |
| P6 | yes, a strong preference, not a must-have | M | DR-08 |
| P7 | no: "the model is only used within the ranges in this data" | M | DR-05 |
| P8 | unknown | M | DR-05 |
| CV protocol | §16 as written: outer 10-fold, inner 5-fold grid search, both stratified and shuffled, seed 2026; models compared on F2 at r = 0.5; the threshold tuned for F2 on the chosen configuration only; C2 against the most common class | M | user, 14 October 2026 (quoted below) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P5=inspectable→Logistic | holds | [B→I p.347] | +1 on the four Logistic configurations |
| P5=inspectable→Tree | holds | [B→I p.347] | +1 on `Tree` |
| P5=inspectable→poly | holds | [I] | −1 on `Logistic + poly`, `Logistic + poly + L2` |
| P6=yes→Logistic | holds | [B→I pp.50, 53–54] | +1 on the four Logistic configurations |
| §15.3 order | score, then fewer add-ons | [I] | `Logistic` (2, 0) · `Logistic + L2` (2, 1) · `Tree` (1, 0) · `Logistic + poly` (1, 1) · `Logistic + poly + L2` (1, 2) · `kNN` (0, 0) |
| SEQ-1 | baseline = most common training class; the flag-everyone classifier is cross-validated alongside (DR-08) | [B pp.330–331] | both kept |
| SEQ-2 | simple-first = `Logistic` (MOD-1, MOD-2 do not apply) | [B p.331] | kept |
| §15.4 keep | simple-first + top 3 others; no tie at the cut | [I] | `Logistic + L2`, `Tree`, `Logistic + poly` kept |
| §16 decision threshold | r = 0.5 for selection; tuned for F2 after selection, P6 = yes | [B→I pp.53–54, 92–93] | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Kept besides baseline and simple-first | 3 (+ ties) | 3 kept; rank 4 and rank 5 differ on add-ons, so no tie |
| §16 outer / inner folds | 10 / 5 | — |
| §16 grids | k ∈ {1, 3, 5, 7, 9, 15, 21, 31, 51}; depth ∈ {1, 2, 3, 4, 5, 6, 8, 10, 15, 20} × min leaf ∈ {1, 5, 10, 20}; degree ∈ {2, 3}; λ ∈ {10⁻⁴, …, 10⁴} | — |
| Threshold grid (step 4f) | 0.05, 0.10, …, 0.95 | — |

- **Options considered:** `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`, `kNN`, `Tree`
- **Expectation:** `Logistic` ≈ `Logistic + L2` > `Logistic + poly` > `Tree`, with all four clearly above the most-common-class baseline. My reasons:
  - With about 20 rows per parameter (P2 ample), L2 has little overfitting to correct, so it should add little.
  - With P8 unknown, there's no stated reason to expect curvature that polynomial terms would capture. They add 12 parameters.
  - A tree on 239 rows makes piecewise-constant predictions that change with the training sample, so its fold scores should be lower and more variable.
  - The baseline predicts no deaths, so it scores F2 = 0 in every fold.
- **Decision:** Keep the baseline (most common class) and the flag-everyone classifier, then `Logistic` (simple-first, score 2), `Logistic + L2` (2), `Tree` (1) and `Logistic + poly` (1). The prior order is `Logistic`, `Logistic + L2`, `Tree`, `Logistic + poly`.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Logistic + poly + L2` | DISF | score 1: P5=inspectable→Logistic +1, P6=yes→Logistic +1, P5=inspectable→poly −1; rank 5 on two add-ons |
| `kNN` | DISF | score 0: no matrix entry applies (P3 few, P4 low, P7 no, P8 unknown) |
| 8 regression configurations | EXCL | DR-12 |

**Reference code**

- Function: `core.prior_ranking` (`core.py prior`) · version `e5e819e3…` (interim core, not reviewed) · inputs: `Code/inputs/subtask1_props.json` · output: `Code/outputs/core_prior.json`. Output copied unchanged; no disagreement.

- **Confidence:** n/a
- **Outcome vs expectation:** **disagree** (DR-15). The expected order was `Logistic` ≈ `Logistic + L2` > `Logistic + poly` > `Tree`. The CV order is `Tree` (0.5567) > `Logistic + poly` (0.5286) > `Logistic` = `Logistic + L2` (0.4798).
  - Two parts of the expectation held: `Logistic + L2` added nothing over `Logistic` (identical fold scores, λ at the smallest grid value in 8 folds), and all four configurations clearly beat the most-common-class baseline.
  - Two parts did not: `Tree`, expected last, leads; and `Logistic + poly` is above `Logistic`.
  - The two prior entries that put the Logistic family ahead of `Tree` are P6=yes→Logistic [B→I pp.50, 53–54] and P5=inspectable→poly [I]. Neither is about predictive fit, so a disagreement on F2 doesn't contradict either. My reasoning about tree variance was not a matrix entry, and it was wrong here.
- **User involvement:** approved:
  - "Keep ML Guide.md §16 as it is: models are compared at r = 0.5, as SEQ-1 says, and the threshold is tuned for F2 only on the chosen configuration. Keep the most-common-class baseline for C2. At 4g, success is still judged against the flag-everyone reference (DR-08). Record as a limitation that selection at r = 0.5 may not pick the configuration that would be best after threshold tuning."
    - *Note (user's correction, 14 October 2026):* r = 0.5 for comparing models comes from §16, not SEQ-1; SEQ-1 is the baseline rule. The quote is kept as the user wrote it.
  - "Seed 2026 and the threshold grid are fine."
  - "Then run 4a and continue sub-step by sub-step. Stop before the test set (4g) and ask me first."
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/core_prior.json`

### DR-14 · CV · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Does the simple-first configuration clearly beat the baseline (SEQ-3, round 1)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `Logistic` fold F2 (r = 0.5) | 0.395, 0.278, 0.417, 0.625, 0.732, 0.395, 0.658, 0.172, 0.556, 0.571 | CV | `Code/outputs/core_cv_store.json` |
| Baseline (most common class) fold F2 | 0 in all 10 folds (it never predicts a death) | CV | as above |
| Flag-everyone fold F2 | 0.714 (7 folds), 0.673 (2), 0.686 (1) | CV | as above |
| REQ-1, REQ-3, REQ-5 | log transform, `StandardScaler` and `BookLogistic(lam=None)` (C = ∞) in one `Pipeline`, refitted in every fold; no penalty, so REQ-5 doesn't arise | CV | `pipeline` field, `core_cv_store.json` |
| Convergence warnings | 0 | CV | `core_cv_round1.json` |

**CV table** (outer 10, inner 5, stratified, seed 2026; F2 at r = 0.5; margins as mean ± spread over the 10 fold differences)

| Configuration | Post-prior | Tuned hyperparameters | CV mean F2 | Margin vs leader | Margin vs baseline (most common class) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic` | no | none to tune | 0.4798 | leader | +0.4798 ± 0.1777 (C2 clear) | 0.2348 | 0.2678 |
| Baseline (most common class) | no | n/a | 0.0000 | −0.4798 ± 0.1777 | — | 0.3222 | 0.3221 |
| Flag everyone | no | n/a | 0.7032 | +0.2235 ± 0.1742 | +0.7032 ± 0.0181 | 0.6778 | 0.6779 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 | baseline and simple-first cross-validated first | [B pp.331–332] | — |
| C2 (`Logistic` vs most common class) | margin 0.4798 ≥ 1 × spread 0.1777: clear | [I] | DX-1 not needed; round 2 goes ahead |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | 0.4798 vs 0.1777 |
| §16 outer / inner folds | 10 / 5 | — |

- **Options considered:** go on to round 2 · DX-1
- **Expectation:** n/a
- **Decision:** `Logistic` clearly beats the most-common-class baseline, so round 2 goes ahead.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

**Reference code**

- Function: `core.run_cv` (`core.py cv round1`) · version `e5e819e3…` (interim core, not reviewed) · inputs: `Code/inputs/subtask1_props.json`, the 239 training rows · output: `Code/outputs/core_cv_round1.json`, `Code/outputs/core_cv_store.json`. Output copied unchanged.
- The core takes the leader from the model configurations only, never from the baselines. The flag-everyone classifier's CV F2 (0.7032) is above `Logistic`'s at r = 0.5 (0.4798). That isn't a C2 comparison (DR-13). It is the comparison the step 4 limitation is about.

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** none (within the agreed method)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/core_cv_round1.json`

### DR-15 · CV · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** How do the remaining kept configurations compare, on the same folds (round 2)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `Tree` fold F2 | 0.682, 0.405, 0.513, 0.641, 0.732, 0.500, 0.658, 0.469, 0.526, 0.441 | CV | `Code/outputs/core_cv_store.json` |
| `Tree` tuned per fold (depth, min leaf) | (3, 20) ×4, (4, 5) ×2, (4, 1), (10, 1), (8, 5), (2, 20) | CV | as above |
| `Logistic + poly` fold F2 | 0.366, 0.395, 0.405, 0.658, 0.625, 0.395, 0.658, 0.484, 0.694, 0.606 | CV | as above |
| `Logistic + poly` tuned degree | 2 in 8 folds, 3 in 2 | CV | as above |
| `Logistic + L2` fold F2 | identical to `Logistic` in all 10 folds | CV | as above |
| `Logistic + L2` tuned λ | 10⁻⁴ (smallest in grid) in 8 folds, 10⁻³ in 2 | CV | as above |
| L2 implementation | C = 1/(2nλ), checked against eq. 3.50 before this result was reported (Analysis, step 4) | M | `Code/outputs/check_eq350.txt` |
| REQ-1 to REQ-5 | log → (powers) → `StandardScaler` → model in one `Pipeline` per fold for the Logistic configurations; tree on unscaled inputs; intercept unpenalised | CV | `pipeline` fields, `core_cv_store.json` |
| Convergence warnings | 0 for every configuration | CV | `core_cv_round2.json` |

**CV table** (cumulative; outer 10, inner 5, stratified, seed 2026; F2 at r = 0.5; margins as mean ± spread of the 10 fold differences)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean F2 | Margin vs leader | Margin vs baseline (most common class) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Tree` | no | depth 3, min leaf 20 (4/10 folds) | 0.5567 | leader | +0.5567 ± 0.1124 (C2 clear) | 0.1692 | 0.2721 |
| `Logistic + poly` | no | degree 2 (8/10) | 0.5286 | −0.0281 ± 0.1422 | +0.5286 ± 0.1315 (C2 clear) | 0.2013 | 0.2549 |
| `Logistic` | no | none to tune | 0.4798 | −0.0769 ± 0.1357 | +0.4798 ± 0.1777 (C2 clear) | 0.2348 | 0.2678 |
| `Logistic + L2` | no | λ = 10⁻⁴ (8/10) | 0.4798 | −0.0769 ± 0.1357 | +0.4798 ± 0.1777 (C2 clear) | 0.2343 | 0.2678 |
| Baseline (most common class) | no | n/a | 0.0000 | −0.5567 ± 0.1124 | — | 0.3222 | 0.3221 |
| Flag everyone | no | n/a | 0.7032 | +0.1466 ± 0.1056 | +0.7032 ± 0.0181 | 0.6778 | 0.6779 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| C2, each configuration vs the most common class | clear for all four | [I] | all four eligible so far |
| Prior agreement (§17), for information here | CV leader `Tree` is third in the prior order (`Logistic`, `Logistic + L2`, `Tree`, `Logistic + poly`): disagree | [I] | recorded in DR-13 |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear | margin ≥ 1 × spread | `Tree` 0.5567 vs 0.1124; `Logistic + poly` 0.5286 vs 0.1315; `Logistic`, `Logistic + L2` 0.4798 vs 0.1777 |

- **Options considered:** `Logistic + L2`, `Tree`, `Logistic + poly`, cross-validated on the same folds as round 1
- **Expectation:** n/a
- **Decision:** `Tree` is the leading configuration. The diagnosis loop (4e) starts from it.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a (decided in `FINAL`) | | |

**Reference code**

- Function: `core.run_cv` (`core.py cv round2`) · version `e5e819e3…` (interim core, not reviewed) · inputs: `Code/inputs/subtask1_props.json`, the 239 training rows, the round-1 folds (checked identical by the core) · output: `Code/outputs/core_cv_round2.json`, `Code/outputs/core_cv_store.json`. Output copied unchanged.

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** none (within the agreed method)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/core_cv_round2.json`

### DR-16 · DX · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Diagnosis pass 1: which observation holds for the leading configuration `Tree`, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| E_train / E_val / gap (misclassification, mean over outer folds, r = 0.5) | 0.1692 / 0.2721 / 0.1029 | CV | `Code/outputs/core_diagnose_Tree.json` |
| Training F2 (r = 0.5, mean over outer training folds) | 0.7186 | CV | as above |
| Tuned min leaf size per fold | 20 (largest in grid) in 5 folds, 1 (smallest) in 2, 5 in 3 | CV | as above; DR-15 |
| Tuned max depth per fold | never at an edge (2–10 of 1–20) | CV | as above |
| Learning curve, E_val at 80 % / 100 % | 0.2594 / 0.2721; fold SD at 100 % 0.0693 | CV | as above |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 clear vs most common class (DR-15) |
| O2 training error above what the application needs | **yes** | training F2 0.7186 ≤ flag-everyone reference 0.7038 + fold SD 0.1124 = 0.8162 (interpretation i, UNLISTED [I]) |
| O5 hyperparameter at the edge of its grid | yes | min leaf at an edge in 7 of 10 folds (> 5); depth 0 of 10 |
| O3 overfitting | no | gap 0.1029 < 2 × E_train 0.3385 |
| O4 underfitting | no | E_train 0.1692 < 2 × gap 0.2057 |
| O6 more data likely to help | no | C3 adequate: E_val(80 %) − E_val(100 %) = −0.0127 < 0.5 × 0.0693 |

- Priority order O1 > O2 > O5 > O3 > O4 > O6: the first observation that holds is **O2**, so the action is **DX-2** — stop and rethink the problem and method with the user [B p.78]. DX-2 needs the user, so the loop stops until they answer.
- Two facts bear on O2:
  - O2 compares training F2 at r = 0.5 with a criterion that step 4g judges at the tuned threshold. It is the same mismatch as the step 4 limitation.
  - The O2 test itself is our interpretation (i), not a rule in the guide.

**Stopping check**

- S1 (criterion met): not assessed until 4g. S2 (achievable level): unknown (DR-05). S3 (no gain in two passes): first pass. S4 (out of scope): no. S5 (user stops it): pending. S6 (five passes): no. **None applies yet.**

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| O2, DX-2 | holds → rethink with the user | [B p.78]; test UNLISTED [I] interpretation i | loop paused |
| O5, DX-3 | holds, lower priority than O2 | [I] | not taken in this pass |
| O3 / O4 | do not hold | [B→I p.334] + [I] ratio | — |
| O6 / C3 | does not hold | [B→I pp.334–336] + [I] | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 overfitting | gap ≥ 2 × E_train | 0.1029 vs 0.3385 |
| O4 underfitting | E_train ≥ 2 × gap | 0.1692 vs 0.2057 |
| O5 grid edge | > 5 of 10 folds | 7 (min leaf), 0 (depth) |
| C3 still falling | ≥ 0.5 × fold SD at 100 % | −0.0127 vs 0.0346 |

- **Options considered:** DX-2 (required by the priority order); DX-3 (O5) would follow if O2 is set aside
- **Expectation:** n/a until the user chooses the action
- **Decision:** The loop pauses at DX-2 and the question goes to the user.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a (no expectation was set; the action was the user's choice, recorded in DR-17)
- **User involvement:** asked. The user chose option A with one condition: "a single diagnosis pass."
  - "Record that O2, as tested, reflects the r = 0.5 mismatch already recorded as a limitation, not the success criterion."
  - "Run DX-3 for O5: extend the Tree's minimum leaf size to 30, 40 and 50, as a post-prior variant on the same folds."
  - "If that pass gives no clear gain over the current Tree, stop the loop and go to 4f. Do not start further passes without asking me."
- **DX-2 outcome (the rethink):** O2, as tested, compares training F2 at r = 0.5 with a criterion that 4g judges at the tuned threshold. It reflects the r = 0.5 mismatch already recorded as a limitation (Analysis, step 4), not the success criterion. The formulation is unchanged, and the loop continues with O5 (DR-17).
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/core_diagnose_Tree.json`

### DR-17 · DX · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Diagnosis pass 1, continued: does extending `Tree`'s minimum-leaf grid upwards (DX-3, for O5) give a clear gain?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| O5 for `Tree` | min leaf at a grid edge in 7 of 10 folds: 20 (the largest) in 5, 1 (the smallest) in 2 | CV | DR-16; `Code/outputs/core_diagnose_Tree.json` |
| O2 set aside | reflects the r = 0.5 mismatch, not the success criterion (user, DR-16) | M | DR-16 |
| User's conditions | one pass only; "if that pass gives no clear gain over the current Tree, stop the loop and go to 4f" | M | user, 14 October 2026 |

**Observation → action**

- O5 holds (DR-16), and O2 is set aside by the user, so the action is **DX-3**: extend the grid in the direction of the edge.
  - The upper edge (20) was chosen in 5 folds, and the lower edge (1) can't be extended downwards.
  - So the minimum-leaf grid becomes {1, 5, 10, 20, 30, 40, 50}, with the depth grid unchanged.
- This is cross-validated as a **post-prior** variant, `Tree (min leaf to 50)`, on the same outer folds.
- "Clear gain" is read as the §17 "clear" level: the variant's margin over `Tree` ≥ 1 × spread of the fold differences, `[I]`.

**Stopping check**

- S5 applies after this pass, by the user's instruction: the loop stops whatever the result, and only goes on to 4f if there is no clear gain. A clear gain would be reported to the user before anything else is done.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| O5 → DX-3 | extend the min-leaf grid upwards | [I] | post-prior variant on the same folds |
| §17 "clear" as the test for a clear gain | margin ≥ 1 × spread | [I] | decides between stopping and reporting back |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O5 grid edge | > 5 of 10 folds | 7 |
| Clear gain | margin ≥ 1 × spread | −0.0360 vs 0.0584: no |

- **Options considered:** `Tree (min leaf to 50)` (post-prior)
- **Expectation:** No clear gain. The larger leaf sizes will be chosen in some of the five folds that sat at 20, and in those folds the tree becomes coarser. But the folds that chose 1 or 5 won't change, and the fold spread of `Tree`'s F2 is 0.1124. A change in mean F2 large enough to exceed the spread of the fold differences is unlikely.
- **Decision:** No clear gain, so the loop stops (S5, the user's instruction) and step 4f begins.

**CV table, post-prior row** (same outer folds; F2 at r = 0.5)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean F2 | Margin vs leader (`Tree`) | Margin vs baseline (most common class) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Tree (min leaf to 50)` | yes | depth 3, min leaf 20 (3/10 folds) | 0.5207 | −0.0360 ± 0.0584 | +0.5207 ± 0.1252 (C2 clear) | 0.2139 | 0.2804 |

| Evidence | Value | Tag | Where |
| --- | --- | --- | --- |
| Fold F2 | 0.682, 0.405, 0.395, 0.641, 0.625, 0.500, 0.658, 0.333, 0.526, 0.441 | CV | `Code/outputs/core_cv_store.json` |
| Tuned (depth, min leaf) per fold | (3, 20), (4, 5), (1, 50), (3, 20), (2, 40), (8, 5), (3, 20), (2, 30), (2, 20), (4, 5) | CV | as above |
| Folds that changed (numbered 1–10) | three folds; the other seven chose the same settings and scored the same F2 as in DR-15. Fold 3: (4, 1) → (1, 50), F2 0.513 → 0.395. Fold 5: (10, 1) → (2, 40), 0.732 → 0.625. Fold 8: (3, 20) → (2, 30), 0.469 → 0.333 | CV | DR-15, this record |

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a (decided in `FINAL`) | | |

**Reference code**

- Function: `core.run_cv` (`core.py cv add "Tree" --grid '{"m__min_samples_leaf": [1, 5, 10, 20, 30, 40, 50]}' --label "Tree (min leaf to 50)"`) · version `e5e819e3…` (interim core, not reviewed) · output: `Code/outputs/core_cv_post_prior_1.json`, `Code/outputs/core_cv_store.json`.

- **Confidence:** n/a
- **Outcome vs expectation:** partial.
  - The main expectation held: there was no clear gain, and the variant's mean F2 is lower (−0.0360 ± 0.0584).
  - The reasoning was partly wrong. I expected the folds that chose min leaf 1 or 5 not to change. In fact the two folds that had chosen 1 (folds 3 and 5) moved to 50 and 40 and scored lower F2. In the inner folds, the wider grid found larger leaves that scored better, and on the outer validation fold they scored worse.
- **User involvement:** approved (DR-16)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/core_cv_post_prior_1.json`

### DR-18 · FINAL · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** Which configuration does the recommendation rule (§19) choose, with what selection confidence, and what is the decision threshold? (Test evaluation pending: step 4g, after the user's approval.)

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV table | DR-15 and DR-17: five configurations compared, all on the same folds | CV | `Code/outputs/core_cv_store.json` |
| Learning curve, `Tree` | E_val 0.3181 (10 %), 0.3306, 0.3516, 0.2969, 0.2967, 0.3051, 0.2812, 0.2594 (80 %), 0.2761, 0.2721 (100 %); fold SD at 100 % 0.0693 | CV | `Code/outputs/core_recommend.json` |
| Threshold, nested per outer fold (P6 = yes, trade-off F2, DR-05) | chosen r per fold: 0.15, 0.20, 0.05, 0.10, 0.50, 0.15, 0.05, 0.15, 0.10, 0.05. F2 at those thresholds: 0.682, 0.465, 0.727, 0.769, 0.732, 0.745, 0.714, 0.750, 0.673, 0.686. Mean 0.6943, fold SD 0.0865 | CV | as above |
| Flag-everyone reference, training rows | F2 0.7038 | M | as above; DR-08 |
| Final fit (interpretation j: the inner grid search rerun on all 239 rows) | depth 15, min leaf 1. Depths 15 and 20 with min leaf 1 tie for best inner F2 (0.6051). The fitted tree has depth 12 and 54 leaves, so the depth limit doesn't bind. (Depth 3, min leaf 20, the most common setting across outer folds, scores 0.5255 there.) | CV | `core_recommend.json`; check in the scratch folder, training rows only (Analysis Log row 35) |
| Final threshold | 0.5, by tie-break. The final tree's out-of-fold probabilities are only 0 and 1, so all 19 thresholds give F2 = 0.6057 | CV | as above |

**§19 trace**

1. Eligible (C2 clear vs the most common class):
   - `Tree` +0.5567 ± 0.1124
   - `Logistic + poly` +0.5286 ± 0.1315
   - `Tree (min leaf to 50)` +0.5207 ± 0.1252 (post-prior)
   - `Logistic` and `Logistic + L2`, +0.4798 ± 0.1777 each

   All five are eligible.
2. Candidates: the best CV mean is `Tree` (0.5567). Within noise of it (margin < 0.5 × spread):
   - `Logistic + poly`: 0.0281 < 0.5 × 0.1422 = 0.0711, so it is a candidate.
   - `Tree (min leaf to 50)`: 0.0360 ≥ 0.0292, so it is not.
   - `Logistic` and `Logistic + L2`: 0.0769 ≥ 0.0679, so they are not.
3. Choice: the fewest add-ons wins. `Tree` has 0 and `Logistic + poly` has 1, so **`Tree`** is chosen; the prior score didn't need to be used.
4. Test result: pending (4g).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.1–19.3 | `Tree` | [B p.332] for simplicity; [I] cut-offs | recommended |
| C1 (vs runner-up `Logistic + poly`) | +0.0281 ± 0.1422: none | [I] | — |
| C2 (vs most common class) | +0.5567 ± 0.1124: clear | [I] | — |
| C3 | E_val(80 %) − E_val(100 %) = −0.0127 < 0.5 × 0.0693: adequate | [B→I pp.334–336] + [I] | — |
| §17 level | C1 = none → Low | [I] | — |
| §16 decision threshold | tuned for F2 after selection, nested per fold; final r on all training rows | [B→I pp.53–54, 92–93] | see the disagreement below |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| §19 within noise | < 0.5 × spread | 0.0281 vs 0.0711 (`Logistic + poly`); 0.0360 vs 0.0292; 0.0769 vs 0.0679 |
| C1 clear / moderate | ≥ 1 / ≥ 0.5 × spread | 0.0281 vs 0.1422 |
| C2 clear | ≥ 1 × spread | 0.5567 vs 0.1124 |
| C3 still falling | ≥ 0.5 × fold SD at 100 % | −0.0127 vs 0.0346 |
| Breadth note | > 10 configurations | 5 |
| Threshold grid | 0.05, …, 0.95 | — |

- **Options considered:** `Tree`, `Logistic + poly`, `Tree (min leaf to 50)` (post-prior), `Logistic`, `Logistic + L2`
- **Expectation:** n/a
- **Decision:** `Tree` is the recommended configuration, with selection confidence Low. Its final hyperparameters and threshold are **held, pending the user** (see the disagreement below).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] (DR-12) |
| `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary (DR-12) |
| `Logistic + poly + L2` | DISF | prior score 1 (P5=inspectable→Logistic +1, P6=yes→Logistic +1, P5=inspectable→poly −1); rank 5 (DR-13) |
| `kNN` | DISF | prior score 0, no entries (DR-13) |
| `Logistic` | OUTP | `Tree` − `Logistic` = +0.0769 ± 0.1357 (≥ 0.5 × spread) |
| `Logistic + L2` | OUTP | +0.0769 ± 0.1357 |
| `Logistic + poly` | SIMP | +0.0281 ± 0.1422 (< 0.5 × spread); 1 add-on vs 0 |

Post-prior variant, listed separately: `Tree (min leaf to 50)` is not a candidate (−0.0360 ± 0.0584 vs `Tree`, ≥ 0.5 × spread). Flags: none.

**Reference code**

- Function: `core.recommend` (`core.py recommend`) · version `e5e819e3…` (interim core, not reviewed) · inputs: `Code/inputs/subtask1_props.json`, `Code/outputs/core_cv_store.json`, the 239 training rows · output: `Code/outputs/core_recommend.json`. The §19 trace, selection confidence, prior agreement, grounding, breadth note, why-not codes and the nested threshold estimate are copied unchanged.
- **Disagreement (agent), raised with the user and not substituted.** The final fit comes from interpretation j: the inner grid search, rerun on all training rows. It gives a tree that the depth limit doesn't constrain, and §9 says "a fully grown tree is never reported". Its out-of-fold probabilities are only 0 and 1, so threshold tuning can't choose between thresholds. The nested threshold estimate (0.6943 ± 0.0865) describes the per-fold trees at thresholds of 0.05–0.50, not this final model at 0.5. So DR-08's requirement that the uncertainty be "for the same configuration and threshold" would not hold. The final hyperparameters and threshold are held until the user decides.

- **Confidence:** Low — C1 none (+0.0281 ± 0.1422 over `Logistic + poly`) · C2 clear (+0.5567 ± 0.1124) · C3 adequate (−0.0127 vs 0.0346). Rule: Low if C1 = none or C2 not clear. Prior agreement: disagree (CV winner among prior-kept configurations `Tree`; prior order `Logistic`, `Logistic + L2`, `Tree`, `Logistic + poly`). Grounding: [B] 0 / [B→I] 1 (P5=inspectable→Tree) / [I] 0. Breadth note: no (5 configurations compared).
- **Outcome vs expectation:** n/a
- **User involvement:** asked. The user chose option A for the final fit (DR-19).
- **Supersedes / superseded by:** superseded by DR-19 (final hyperparameters and threshold; the core changed after 4b). The §19 trace, confidence and why-not codes are reproduced unchanged under the new version.
- **Links:** `Code/outputs/core_recommend.json` (since overwritten by the DR-19 run; the DR-18 values are kept in this record)

### DR-19 · FINAL · step 4

- **Sub-task:** 1
- **Date:** 2026-10-14
- **Question:** With the final fit fixed at the most common outer-fold setting, which configuration, hyperparameters and threshold go to the single test evaluation, and what does it show?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| User's decision, final fit | "Fix the Tree at depth 3 and minimum leaf 20 (the most common setting across the outer folds), then choose the threshold from out-of-fold probabilities on the training rows only." | M | user, 14 October 2026 |
| Core change | interpretation j: final hyperparameters = the most common setting across the outer folds (was: the grid search rerun on all rows). Version `e5e819e3…` → `434ff8cd…` | M | `Code/core.py` |
| §19 trace, C1–C3, prior agreement, grounding, breadth, why-not codes, nested threshold estimate | identical to DR-18 under the new version | CV | `Code/outputs/core_recommend.json` |
| Final hyperparameters | depth 3, min leaf 20, chosen in 4 of 10 outer folds | CV | as above |
| Final threshold | r = 0.2: the F2-maximising r from 5-fold out-of-fold probabilities on the 239 training rows, with depth 3 / min leaf 20 | CV | as above |
| Uncertainty (DR-08) | fold SD of F2 at the per-fold tuned thresholds: 0.0865 (CV mean 0.6943) | CV | as above |
| Test results | see *Test result* below | TEST | `Code/outputs/core_final.json`, `Code/outputs/core_test_predictions.csv` |

- **What the CV estimate describes (user's instruction).** The setting depth 3 / min leaf 20 was chosen in 4 of 10 outer folds. The CV estimate (0.6943 ± 0.0865) therefore describes the selection procedure, which tunes the hyperparameters and the threshold inside each fold, not exactly this fixed setting with r = 0.2.

**§19 trace**

1–3. As in DR-18: all five configurations eligible; candidates `Tree` and `Logistic + poly` (+0.0281 ± 0.1422 < 0.0711); `Tree` chosen on fewer add-ons (0 vs 1).

4. Test result (step 4g): F2 0.6780 at r = 0.2 (fold SD 0.0865; n_test = 60, 19 positives). Success criterion not met (required > 0.7903).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.1–19.3 | `Tree` | [B p.332]; [I] cut-offs | recommended |
| §19.4 test once | `Tree`, depth 3, min leaf 20, r = 0.2, refitted on all 239 training rows | [B pp.74, 328] | single evaluation |
| §16 decision threshold | r = 0.2, from out-of-fold probabilities on the training rows | [B→I pp.53–54, 92–93] | — |
| DR-08 success | test F2 > flag-everyone reference (training rows) + fold spread of F2 | [I]; uncertainty [B→I pp.71–73] | not met (0.6780 vs 0.7903) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| As DR-18 | | |
| Success | test F2 > 0.7038 + 0.0865 = 0.7903 | 0.6780: not met |

- **Options considered:** final fit A (most common outer-fold setting) · B (fully grown tree at r = 0.5)
- **Expectation:** n/a
- **Decision:** `Tree` with depth 3, min leaf 20 and threshold r = 0.2, evaluated once on the test set. Test F2 0.6780; the success criterion is not met.

**Why not**

As DR-18, unchanged:

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] (DR-12) |
| `Logistic + poly + L2` | DISF | prior score 1, rank 5 (DR-13) |
| `kNN` | DISF | prior score 0 (DR-13) |
| `Logistic` | OUTP | +0.0769 ± 0.1357 |
| `Logistic + L2` | OUTP | +0.0769 ± 0.1357 |
| `Logistic + poly` | SIMP | +0.0281 ± 0.1422; 1 add-on vs 0 |

**Reference code**

- Function: `core.recommend`, then `core.final` · version `434ff8cd3f80eab440c233892834f9dc1bab0db2a197a030a9865194dd2401a6` (SHA-256 of `Code/core.py`; **interim core, not reviewed**; changed after 4b in interpretation j only, at the user's decision) · inputs: `Code/inputs/subtask1_props.json`, `Code/outputs/core_cv_store.json` (CV results from version `e5e819e3…`; the change doesn't touch CV) · outputs: `Code/outputs/core_recommend.json`, `Code/outputs/core_final.json`, `Code/outputs/core_test_predictions.csv`. Outputs copied unchanged; no disagreement.

**Test result** (step 4g, run once on 14 October 2026; 60 test rows, 19 deaths)

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Test F2 (r = 0.2) | 0.6780 | TEST | `Code/outputs/core_final.json` |
| Uncertainty (DR-08) | fold SD of F2 across the 10 outer folds: 0.0865; n_test = 60, 19 positives | CV / TEST | as above |
| Recall | 0.8421 (16 of 19 deaths flagged) | TEST | as above |
| Precision | 0.3810 (16 of 42 flagged patients died) | TEST | as above |
| Confusion matrix | tn 15 · fp 26 · fn 3 · tp 16 | TEST | as above |
| Misclassification rate | 0.4833 | TEST | as above |
| Baseline (most common class), test | F2 0 | TEST | as above |
| Flag everyone, test (for context only) | F2 0.6985 | TEST | as above |
| **Success criterion (DR-08, as written):** "test F2 clearly above the flag-everyone reference (F2 = 0.70 on the training rows). 'Clearly' means by more than the spread of F2 across the outer cross-validation folds." | required: test F2 > 0.7038 + 0.0865 = 0.7903; observed 0.6780: **not met** | TEST | as above |
| Independent recomputation | F2 0.6780, recall 0.8421, precision 0.3810 and the same confusion counts, recomputed by hand from the saved predictions. The rows are checked to be exactly the 60 test rows, and every prediction to equal `p_death > 0.2` | TEST | `Code/07_recompute_test_metric.py`, `Code/outputs/recompute_test_metric.txt` |
| PR and ROC curve points | saved for an evaluation figure in step 4h | TEST | `core_final.json` (`pr_curve`, `roc_curve`) |

- The test F2 (0.6780) is below the flag-everyone reference on the training rows (0.7038), so it does not exceed it by any margin.
- On the same 60 test rows, flagging every patient gives F2 0.6985.
- In cross-validation, the nested estimate at tuned thresholds was 0.6943 ± 0.0865.
- The test set is not used again for this sub-task (DR-06). As the user instructed, the model, threshold and criterion were not changed after the result was seen.

- **Confidence:** Low — C1 none (+0.0281 ± 0.1422 over `Logistic + poly`) · C2 clear (+0.5567 ± 0.1124) · C3 adequate (−0.0127 vs 0.0346). Rule: Low if C1 = none or C2 not clear. Prior agreement: disagree. Grounding: [B] 0 / [B→I] 1 / [I] 0. Breadth note: no (5 configurations).
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "I approve a single evaluation of the recommended Tree on the test set." The user also said: "Do not change the model, threshold or criterion after seeing the result."
- **Supersedes / superseded by:** supersedes DR-18
- **Links:** `Code/outputs/core_recommend.json`, `Code/outputs/core_final.json`, `Code/outputs/core_test_predictions.csv`

## Recommendation

### Sub-task 1 — predict `DEATH_EVENT` from the 11 inputs

Written for the user's recorded experience level, intermediate: terms are used without definition, the reasoning is given in full, and the tables are complete (§25.3).

**1. Problem.**
- **What is predicted.** y = `DEATH_EVENT`, death during the patient's own follow-up period, binary (P1). It is predicted from 11 inputs. `time` is excluded as a leakage risk, and `serum_creatinine` and `creatinine_phosphokinase` enter as natural logs (DR-11).
- **Metric and success.** The metric is F2, used for selection, the threshold and success alike (DR-05). Success means test F2 above the flag-everyone reference (0.7038 on the training rows) by more than the fold spread of F2 (DR-08).
- **Baselines.** The baseline is the most common class (F2 = 0). The flag-everyone classifier is the reference for F2 (DR-08).
- **Achievable level:** unknown.
- **Must-haves:** none. P5 (inspectable) and P6 (probabilities and a tuned threshold) are preferences (DR-09).
- **Expectations.** P7: no, "the model is only used within the ranges in this data". P8: unknown. The user expects a direction, not a shape: "higher serum_creatinine and lower ejection_fraction go with a higher risk of death" (DR-05).
- **Admissibility.** ADM-1: yes (DR-01). ADM-2: prediction (DR-04). ADM-3: no grouping; shuffle before splitting (DR-02). ADM-4: yes, for similar patients only (DR-03).
- **Split.** Stratified, seed 2026: 239 training rows (77 deaths) and 60 test rows (19 deaths) (DR-06).

**2. Recommendation.** `Tree` with maximum depth 3, minimum leaf size 20, and decision threshold r = 0.2. Selection confidence: Low.

**3. Test-set result.**
- **Test F2: 0.6780.** Its uncertainty is the fold SD of F2 at tuned thresholds, 0.0865 (DR-08). n_test = 60, with 19 deaths.
- **Baselines on the same test rows:** the most common class scores F2 0, and flag-everyone scores 0.6985 (given for context only).
- **Success criterion: not met.** It requires test F2 > 0.7038 + 0.0865 = 0.7903.
- **Recall and precision:** recall 0.8421 (16 of 19 deaths flagged); precision 0.3810 (16 of 42 flagged patients died).
- **Confusion matrix:** tn 15, fp 26, fn 3, tp 16.
- **The threshold.** r = 0.2 was chosen to maximise F2 on 5-fold out-of-fold probabilities from the training rows, using the fixed hyperparameters.
- **Curves.** The precision–recall and ROC curve points are saved for an evaluation figure (step 4h). The test metric was recomputed independently from the saved predictions, with the same result (DR-19).

**4. Why this configuration.**
- **Constraints.** The binary task gate left the Logistic family, k-NN and Tree (DR-12). There were no must-haves. MOD-1 and MOD-2 did not apply (P9 = no, recomputed with the log transform; full rank).
- **CV evidence.** Over the runner-up `Logistic + poly`, the margin is +0.0281 with spread 0.1422. Over the most-common-class baseline, it is +0.5567 with spread 0.1124 (DR-15).
- **Simplicity.** Yes: §19's within-noise step decided it. `Tree` and `Logistic + poly` could not be told apart (0.0281 < 0.5 × 0.1422), and `Tree` has 0 add-ons against 1 (DR-18, DR-19).
- **Prior support.** One entry: P5=inspectable→Tree, +1 [B→I p.347] (DR-13).

**5. Ranking.** F2 at r = 0.5, outer 10 / inner 5 folds, seed 2026. Margins are the mean ± spread of the 10 fold differences (DR-15, DR-17).

| Configuration | Prior rank | Prior score | Post-prior | CV mean | Margin vs recommended (± spread) | Margin vs baseline (± spread) | Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Tree` | 3 | 1 | no | 0.5567 | — | +0.5567 ± 0.1124 | recommended |
| `Logistic + poly` | 4 | 1 | no | 0.5286 | −0.0281 ± 0.1422 | +0.5286 ± 0.1315 | SIMP |
| `Tree (min leaf to 50)` | — | 1 | yes | 0.5207 | −0.0360 ± 0.0584 | +0.5207 ± 0.1252 | post-prior variant of `Tree`; not a candidate |
| `Logistic` | 1 | 2 | no | 0.4798 | −0.0769 ± 0.1357 | +0.4798 ± 0.1777 | OUTP |
| `Logistic + L2` | 2 | 2 | no | 0.4798 | −0.0769 ± 0.1357 | +0.4798 ± 0.1777 | OUTP |
| Baseline (most common class) | — | — | no | 0.0000 | −0.5567 ± 0.1124 | — | baseline |
| Flag everyone | — | — | no | 0.7032 | +0.1466 ± 0.1056 | +0.7032 ± 0.0181 | reference for F2 (DR-08) |

**6. Prior versus evidence: disagree.**
- **Expected:** `Logistic` ≈ `Logistic + L2` > `Logistic + poly` > `Tree`.
- **Observed:** `Tree` > `Logistic + poly` > `Logistic` = `Logistic + L2` (DR-13 outcome field).
- **Where the departure sits.** It contradicts the ordering produced by P6=yes→Logistic [B→I pp.50, 53–54] and P5=inspectable→poly [I]. Neither entry concerns predictive fit. My expectation that the tree's variance would place it last was not a matrix entry, and it did not hold.
- **What did hold:** L2 added nothing (identical fold scores, λ at 10⁻⁴ in 8 folds), and every configuration clearly beat the most-common-class baseline.

**7. Why not the others.**
- **EXCL:** `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2`. Task gate, P1 = binary [B pp.17, 49–57] (DR-12).
- **USER:** none. There were no must-haves.
- **DISF:**
  - `Logistic + poly + L2`: prior score 1 (P5=inspectable→Logistic +1, P6=yes→Logistic +1, P5=inspectable→poly −1), rank 5 on two add-ons.
  - `kNN`: prior score 0, with no entries (DR-13).
- **BASE:** none.
- **OUTP:** `Logistic` and `Logistic + L2`, each 0.0769 below `Tree` with spread 0.1357 (≥ 0.5 × spread).
- **SIMP:** `Logistic + poly`, 0.0281 below `Tree` with spread 0.1422 (< 0.5 × spread), and one add-on against none.
- **Flags:** none.

**8. Confidence.**
- **Selection confidence: Low.**
  - C1 is none (+0.0281 ± 0.1422 over `Logistic + poly`).
  - C2 is clear (+0.5567 ± 0.1124 over the most common class).
  - C3 is adequate: E_val at 80 % minus E_val at 100 % is −0.0127, against 0.5 × 0.0693.
  - Rule: Low if C1 = none or C2 is not clear.
- **Reported alongside, not combined:**
  - Prior agreement: disagree.
  - Grounding: [B] 0, [B→I] 1, [I] 0.
  - Breadth note: does not apply (5 configurations compared).
- **What the CV estimate describes.** The final setting, depth 3 / min leaf 20, was chosen in 4 of 10 outer folds. So the CV estimate (0.6943 ± 0.0865 at tuned thresholds) describes the selection procedure, not exactly this fixed setting (DR-19).

**9. How the model predicts.**
- **The rules.** A classification tree of depth at most 3 asks up to three yes/no questions about one input at a time, such as whether an input is above a cut-off [B pp.27–29]. Each patient is sent to one leaf.
- **Leaves.** With minimum leaf size 20, every leaf holds at least 20 of the 239 training patients, and there are at most 8 leaves.
- **Probabilities and flags.** A leaf's predicted probability of death is the share of training patients in it who died. A patient is flagged when that share is above 0.2. Every patient reaching the same leaf gets the same probability and the same flag.
- **What it can say.** The tree can be shown in full, and the rule behind any flag read off it [B p.347].
- **What it can't say.** It does not show how much each input changes the risk, and it is not a causal statement.
- **The fitted tree** (step 4h, from a verified rebuild: Analysis, step 4h; `Code/outputs/core_tree_splits.json`). It uses two of the 11 inputs and has 5 leaves. Counts are the 239 training patients.

| Path | Patients | Died | Share who died (= predicted probability) | Flagged at r = 0.2 |
| --- | --- | --- | --- | --- |
| ejection fraction ≤ 27.5 and ≤ 22.5 | 21 | 18 | 0.8571 | yes |
| ejection fraction ≤ 27.5 and > 22.5 | 29 | 15 | 0.5172 | yes |
| ejection fraction > 27.5, serum creatinine > 1.8149 mg/dL | 22 | 15 | 0.6818 | yes |
| ejection fraction > 27.5, serum creatinine ≤ 1.8149 and > 0.9487 mg/dL | 111 | 27 | 0.2432 | yes |
| ejection fraction > 27.5, serum creatinine ≤ 0.9487 mg/dL | 56 | 2 | 0.0357 | no |

- **Reading the table.** The first split is on ejection fraction at 27.5 % (all 239 patients, 77 deaths). Below it, the second split is on ejection fraction at 22.5 %. Above it, the splits are on serum creatinine at 1.8149 and then 0.9487 mg/dL.
- **Cut-offs on the logged input.** Serum creatinine enters the model as a logarithm, so its cut-offs are back-transformed (exp of 0.5961 and −0.0527). The tree places each cut halfway between two neighbouring log values, so the back-transformed cut-off is the geometric mean of the two neighbouring measured values.
- **Who is flagged.** Only the leaf with ejection fraction above 27.5 % and serum creatinine at or below 0.9487 mg/dL is not flagged. Every other patient is flagged.
- **Comparison with the user's expectation (P8, DR-05).** The user expected a direction, "higher serum_creatinine and lower ejection_fraction go with a higher risk of death". Within this tree, the share who died is higher on the lower-ejection-fraction side of the first split, and higher on the higher-creatinine side of each creatinine split. This is a description of the fitted tree, not a test of the expectation.

**10. Use and limits.**
- **Average-case only.** The test F2 is an average over data like the 60 test patients. It says nothing about the worst individual prediction, and it holds only while new patients resemble these [B pp.329, 347].
- **Population.** It applies only to patients like these: NYHA class III–IV heart failure, two hospitals in Faisalabad, Pakistan, 2015 (DR-03).
- **What the outcome means.** Follow-up varied from 4 to 285 days, so a prediction of no death means "not expected to die during a follow-up of that patient's length", not survival over a fixed period (Data Summary).
- **Selection at r = 0.5.** Configurations were compared at r = 0.5, and the threshold was tuned only on the chosen one. Selection at r = 0.5 may not have picked the configuration that would be best after threshold tuning (Analysis, step 4).
- **The flag-everyone comparison.** At the tuned threshold, the CV estimate (0.6943) and the test F2 (0.6780) are both below the flag-everyone F2 on the same data: 0.7032 in CV, 0.6985 on the test rows. The test F2 comes from 60 patients, 19 of whom died.
- **Inspection.** The tree can be inspected, but no bound on any single prediction follows from it for this binary outcome.
- **The one group not flagged** (added in step 5, from DR-19 and part 9). That group is ejection fraction above 27.5 % and serum creatinine at or below 0.9487 mg/dL.
  - Test patients: 18 were not flagged (tn 15 + fn 3), and 3 of them died, 3/18 = 0.1667.
  - Training patients: 2 of 56 in that group died, 2/56 = 0.0357.
  - So this evaluation does not show the group to be safe, and 18 patients are too few to estimate its death rate precisely. No interval is computed, because binomial intervals were not adopted (DR-08).

**11. Improvement history.**
- **Pass 1.**
  - O2 held: training F2 0.7186 ≤ 0.7038 + 0.1124 (UNLISTED [I] interpretation i). This led to DX-2, rethinking with the user, who recorded that O2 as tested reflects the r = 0.5 mismatch, not the success criterion (DR-16).
  - Next was O5: min leaf at a grid edge in 7 of 10 folds. This led to DX-3, extending the min-leaf grid to 30, 40 and 50 as the post-prior `Tree (min leaf to 50)`. It scored −0.0360 ± 0.0584 against `Tree`: no clear gain (DR-17).
- **Stopped by S5,** the user's instruction of a single pass.
- **Final fit, outside the loop.** The grid search on all rows gave an unconstrained tree with only 0/1 out-of-fold probabilities. At the user's decision, the final fit was fixed at the most common outer-fold setting (DR-18 → DR-19).

**12. Thresholds applied.**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P9 separability | 100 % training accuracy, C = 10⁸ | 76.99 % |
| P10 imbalance | smallest class < 20 % | 32.22 % |
| P2 / P3 / P4 | < 10 / > 20 / ≥ 50 % | 19.917 / 11 / 45 % |
| Kept besides baseline and simple-first | 3 (+ ties) | 3, no tie |
| Outer / inner folds | 10 / 5 | — |
| C2 clear | ≥ 1 × spread | 0.5567 vs 0.1124 (`Tree`) |
| C1 clear / moderate | ≥ 1 / ≥ 0.5 × spread | 0.0281 vs 0.1422 |
| C3 still falling | ≥ 0.5 × fold SD at 100 % | −0.0127 vs 0.0346 |
| §19 within noise | < 0.5 × spread | 0.0281 vs 0.0711; 0.0360 vs 0.0292; 0.0769 vs 0.0679 |
| Breadth note | > 10 configurations | 5 |
| O3 / O4 | gap ≥ 2 × E_train / E_train ≥ 2 × gap | 0.1029 vs 0.3385 / 0.1692 vs 0.2057 |
| O5 grid edge | > 5 of 10 folds | 7 |
| Clear gain (DX-3) | ≥ 1 × spread | −0.0360 vs 0.0584 |
| Threshold grid | 0.05, …, 0.95 | chosen r = 0.2 |
| Success (DR-08) | test F2 > 0.7038 + 0.0865 | 0.6780 |

**13. Trace and provenance.**
- **DRs:** DR-01–DR-04 (ADM), DR-05, DR-08, DR-11 (FORM), DR-06 (SPLIT), DR-07, DR-09, DR-10 (PROP), DR-12 (ADMSET), DR-13 (PRIOR), DR-14, DR-15 (CV), DR-16, DR-17 (DX), DR-18 (FINAL, superseded) and DR-19 (FINAL).
- **Rules and entries used:** the *Rules applied* tables of DR-01 to DR-19, including superseded records, hold 61 rows. Tags counted by occurrence: [B] 22 · [B→I] 19 · [I] 28 · UNLISTED 1. Counted by script from this Appendix (Analysis Log row 38).

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
| 16 | Step 3: interim core `Code/core.py` written (§11 P9–P10 only) and shown to the user before use (version `e614fd79d15a…`) | `Code/core.py` |
| 17 | P9 = no (0.7699 training accuracy), P10 = balanced (0.3222), from the training rows (DR-10 supersedes DR-09) | `Code/outputs/core_p9_p10.json`; DR-10 |
| 18 | Figures 1–3 proposed and approved; made from the 239 training rows; drafts revised for legibility before use (outlines instead of fills, legend placement, plain-number log axes, counts inside bars) | `Code/outputs/figures/` |
| 19 | Figures 1–3 added to *Results* in `Report.md`, with captions | `Report.md` |
| 20 | Input design proposed: log-transform `serum_creatinine` and `creatinine_phosphokinase` as model inputs, or keep them raw (`ML Guide.md` §9, p. 18). Affects Logistic, k-NN and polynomial terms; trees unaffected. **Open; step 3 stays open until the user decides (DR-11)** | Analysis |
| 21 | Input design decided by the user: log both inputs (DR-11, supersedes DR-08 in part). Figures 1–3 kept as they are, the step 4 placeholder kept in *Results*, `sex` kept as woman/man (step 1 inference). Figure 3 caption corrected before commit: 16 distinct ejection-fraction values among the training rows, not 17 (the count for all 299 rows) | DR-11; `Report.md` |
| 22 | Step 3 closed | — |
| 23 | Step 4 begun. Interim core extended to §12–§19 and the test evaluation. Smoke-tested on synthetic data outside the project, then shown to the user and approved. The user decided: §16 stays as written (selection at r = 0.5, threshold tuned on the chosen configuration only); C2 against the most common class; success at 4g against the flag-everyone reference; seed 2026; threshold grid 0.05–0.95. Docstring for interpretation c corrected at the user's request. Version used: `e5e819e3…` | `Code/core.py` |
| 24 | Limitation recorded at the user's request: selection at r = 0.5 may not pick the configuration that would be best after threshold tuning | Analysis (sub-task 1) |
| 25 | C = 1/(2nλ) checked against eq. 3.50 (book text and numerical check; a wrong conversion is detected) before any L2 result was reported | `Code/06_check_eq350.py`, `Code/outputs/check_eq350.txt` |
| 26 | P9 recomputed with the DR-11 log transform: unchanged (0.7699), no new `PROP` record | `Code/outputs/core_p9_p10.json` |
| 27 | 4a: six configurations admissible (four Logistic, `kNN`, `Tree`); eight `EXCL` by the task gate (DR-12) | `Code/outputs/core_admset.json` |
| 28 | 4b: prior ranking. Kept `Logistic` (simple-first), `Logistic + L2`, `Tree`, `Logistic + poly`; `DISF` `Logistic + poly + L2`, `kNN`. Expectation recorded before any CV (DR-13) | `Code/outputs/core_prior.json` |
| 29 | 4c: round 1. `Logistic` CV F2 0.4798 clearly beats the most-common-class baseline (0); flag-everyone 0.7032 (DR-14) | `Code/outputs/core_cv_round1.json` |
| 30 | 4d: round 2. `Tree` 0.5567 > `Logistic + poly` 0.5286 > `Logistic` = `Logistic + L2` 0.4798. Prior vs CV: disagree (DR-15; DR-13 outcome field) | `Code/outputs/core_cv_round2.json` |
| 31 | 4e: diagnosis pass 1 on `Tree`. O2 holds (training F2 0.7186 ≤ 0.8162) → DX-2, which needs the user; O5 also holds. **Loop paused for the user (DR-16)** | `Code/outputs/core_diagnose_Tree.json` |
| 32 | User's answer to DX-2: option A, with a single pass. O2 as tested reflects the r = 0.5 mismatch, not the success criterion. Note added beside the user's DR-13 quote: r = 0.5 comes from §16, not SEQ-1 (user's correction) | DR-16, DR-13 |
| 33 | DX-3 for O5: post-prior `Tree (min leaf to 50)`, min-leaf grid extended to {…, 30, 40, 50}. CV F2 0.5207, −0.0360 ± 0.0584 vs `Tree`: no clear gain. Loop stopped (S5, user's instruction) (DR-17) | `Code/outputs/core_cv_post_prior_1.json` |
| 34 | 4f: §19 recommends `Tree` over `Logistic + poly` on fewer add-ons (+0.0281 ± 0.1422, within noise). Selection confidence Low (C1 none, C2 clear, C3 adequate); prior agreement disagree. Nested threshold estimate F2 0.6943 ± 0.0865 (DR-18) | `Code/outputs/core_recommend.json` |
| 35 | The final fit was checked on the training rows only, with a scratch script calling the core's own functions. The grid search on all 239 rows ties min leaf 1 at depth 15 and 20 (inner F2 0.6051), giving an unconstrained tree (depth 12, 54 leaves). Its out-of-fold probabilities are only 0 and 1, so all thresholds tie (F2 0.6057) and r = 0.5. This conflicts with §9 ("a fully grown tree is never reported") and with DR-08's "same configuration and threshold". Recorded as a disagreement in DR-18; final fit held for the user | DR-18 |
| 36 | User chose option A for the final fit. Core changed after 4b (interpretation j: final hyperparameters = most common outer-fold setting); version `e5e819e3…` → `434ff8cd…`. `recommend` re-run: §19 trace, confidence and why-not codes unchanged; final fit depth 3 / min leaf 20 (4 of 10 folds), threshold r = 0.2 (previously depth 15 / min leaf 1, r = 0.5). DR-19 written before the test set was used; it supersedes DR-18 | `Code/outputs/core_recommend.json`; DR-19 |
| 37 | 4g: single test evaluation, approved by the user ("I approve a single evaluation of the recommended Tree on the test set."). Test F2 0.6780 (fold SD 0.0865; 60 rows, 19 deaths); recall 0.8421, precision 0.3810; tn 15, fp 26, fn 3, tp 16. Success criterion (> 0.7903) **not met**. Flag-everyone F2 on the test rows 0.6985 (context). Recomputed independently from the saved predictions: same values. **Test set used; not to be used again for sub-task 1** | `Code/outputs/core_final.json`, `Code/outputs/core_test_predictions.csv`, `Code/outputs/recompute_test_metric.txt` |
| 38 | Recommendation Report for sub-task 1 written from DR-01 to DR-19. Provenance counts in part 13 counted by script from the *Rules applied* tables. Open: the fitted tree's splits are not yet in any core output (part 9). `Report.md` not yet written for step 4 (4h): the user asked to stop after the Recommendation Report | Recommendation |
| 39 | Step 4 work (4a–4g, Recommendation Report) committed (`74e4a6e` [`ae38a29`]). `Code/core.py -text` added to `.gitattributes` in its own commit (`cce2879` [`55a19e2`]), so the core's SHA-256 survives checkout | — |
| 40 | 4h: core `explain` added (version `434ff8cd…` → `48840eba…`). Verified rebuild of the final tree: 60/60 test probabilities bit-identical to the saved ones (inputs only, no outcomes, no metric). The first check failed by ≤ 5.6 × 10⁻¹⁷ because of pandas' CSV float parser, and passed with round-trip parsing. Model saved; splits written to part 9 of the Recommendation Report: ejection fraction (27.5, 22.5) and serum creatinine (1.8149, 0.9487 mg/dL), 5 leaves, 4 flagged | `Code/outputs/core_tree_splits.json`, `Code/outputs/core_final_model.joblib` |
| 41 | 4h: Figure 4 (precision–recall curve on the test patients) proposed and approved, made from `core_final.json`, label moved off the curve, and added to *Results* with its caption | `Code/08_fig4_pr_curve.py`, `Code/outputs/figures/fig4_pr_curve.png` (+ `dark/`) |
| 42 | 4h: *Methods* and *Results* paragraphs for sub-task 1 written in `Report.md`. Every number checked against the core outputs. Wording corrected before review: "polynomial terms" rather than "squared and cubed terms" (the degree was tuned to 2 or 3); the 0.70 in the success sentence is the training-patient reference. The diagnosis pass changed nothing and is left out of the report | `Report.md` |
| 43 | User reviewed 4h: *Methods*, *Results* and Figure 4 accepted. The factual comparison of the tree with the user's expected direction stays in part 9 of the Recommendation Report; its interpretation belongs to step 5. **Step 4 closed** | — |
| 44 | Step 5: *Discussion* structure proposed and agreed (four paragraphs; each limitation beside the conclusion it qualifies). The user added two changes: describe the tree by what it does in practice, qualifying the low-risk group with the test patients; keep any reading of the prior disagreement tentative. The derived counts for the group not flagged (18 test patients, 3 died, 17 %) were added to Recommendation part 10 before use. *Discussion* written. Titles suggested; awaiting the user's review | `Report.md`; Recommendation part 10 |
| 45 | User's review of the *Discussion*. Paragraph 2 now names the source of the expected direction, Chicco and Jurman (2020). Before citing it, the full text was checked: the direction is in Table 3 (medians for patients who died vs those who survived); the text itself states no direction. The reference note is updated. Paragraph 3 kept as written. Title chosen by the user (option 3). **Step 5 closed** | `Report.md`; References |
| 46 | Image links in `Report.md` checked before publishing. All four resolve relative to the report's folder (`Code/outputs/figures/…`). All eight PNGs (light and dark) are valid and identical to their committed copies, and none is git-ignored. Nothing changed | — |
| 47 | FRAMEWORK change (contract commit `a976de7` [`16e7a7e`]): `Report.md` ends with a `References` section listing only the works it cites, copied from this Appendix. Applied: the section was added with the book, Chicco and Jurman (2020) and the UCI dataset, details copied from the References below and links checked. In-text citations were added where missing: the UCI dataset in the Introduction, and the year for the book | `Report.md` |

Commit IDs in this log are the current ones on `florentine-demo`, with the original ID in brackets. The IDs changed on 14 October 2026 when commit messages were rewritten; the content of each commit is unchanged.

## Code Summary

| File | What it does | Reads | Writes | Run |
| --- | --- | --- | --- | --- |
| `Code/01_describe_data.py` | Step 1 describing pass. Per column: documented meaning and unit, type, missing values, distinct values, min / median / max, zeros, 0/1 counts, non-integer values. Whole file: checksum, size, shape, duplicates, sort order. No random steps. | `Attachments/heart_failure_clinical_records_dataset.csv` | `Code/outputs/01_describe.json`, `Code/outputs/01_describe.md` | `cd Code && uv run python 01_describe_data.py` |
| `Code/02_split.py` | Step 2 split: shuffled, stratified by `DEATH_EVENT`, 20 % test. Records the row indices, class counts, the inputs (11) and the column set aside (`time`). **Seed 2026.** After this, nothing reads the test rows until step 4g. | `Attachments/heart_failure_clinical_records_dataset.csv` | `Code/outputs/split.json` | `cd Code && uv run python 02_split.py` |
| `Code/core.py` | **Interim core, not reviewed.** §11 P9–P10 (with the DR-11 log transform); §12 admissible set; §13/§15 prior; §16 nested CV (outer 10, inner 5, stratified, **seed 2026**), stored cumulatively so every configuration uses the same folds; §18 observations and learning curve; §17/§19 recommendation, why-not codes and threshold tuning (grid 0.05–0.95); the single test evaluation (`final`, which needs the user's approval and refuses a second run). Interpretations a–k are listed in its docstring. Version = SHA-256 of the file: `e5e819e3…` for steps 4a–4f (DR-12 to DR-18); `434ff8cd…` from DR-19 on, after interpretation j was changed (final hyperparameters = the most common outer-fold setting); `48840eba…` from step 4h, which adds `explain` (a verified rebuild of the final tree, which saves `Code/outputs/core_final_model.joblib` and `Code/outputs/core_tree_splits.json`; it reads the test inputs only, to check the rebuild). Reads only the training rows, except `final` | `Attachments/…csv`, `Code/outputs/split.json`, `Code/inputs/subtask1_props.json` | `Code/outputs/core_*.json` | `cd Code && PYTHONIOENCODING=utf-8 uv run python core.py <command>` (commands in the docstring; the variable is needed on Windows because the output contains `→`) |
| `Code/inputs/subtask1_props.json` | The property values passed to the core, copied from DR-10 | — | — | — |
| `Code/08_fig4_pr_curve.py` | Figure 4: precision–recall curve of the recommended tree on the 60 test patients, with the r = 0.2 operating point, the flag-everyone point and the random-classifier line. Refits nothing; no random steps | `Code/outputs/core_final.json` | `Code/outputs/figures/fig4_pr_curve.png` (+ `dark/`) | `cd Code && uv run python 08_fig4_pr_curve.py` |
| `Code/07_recompute_test_metric.py` | Recomputes the step 4g test metrics by hand from the saved predictions, without `core.py`. Checks the rows are exactly the test rows and that each prediction equals `p_death > 0.2`. No random steps | `Code/outputs/core_test_predictions.csv`, `Code/outputs/split.json` | `Code/outputs/recompute_test_metric.txt` | `cd Code && uv run python 07_recompute_test_metric.py` |
| `Code/06_check_eq350.py` | Checks that `BookLogistic`'s C = 1/(2nλ) solves the book's eq. 3.50, against a direct minimisation, with a wrong conversion as a control. Synthetic data, **seed 1** | — | `Code/outputs/check_eq350.txt` | `cd Code && uv run python 06_check_eq350.py` |
| `Code/03_fig1_numeric_by_outcome.py` | Figure 1: histogram outlines of the six numeric inputs by outcome; log x-axis (display only) for serum creatinine and CPK | `Attachments/…csv`, `split.json` (training rows) | `Code/outputs/figures/fig1_numeric_by_outcome.png` (+ `dark/`) | `cd Code && uv run python 03_fig1_numeric_by_outcome.py` |
| `Code/04_fig2_death_share_binary.py` | Figure 2: share who died within each level of the five yes/no inputs, with n per bar and the training share as a reference line | as above | `Code/outputs/figures/fig2_death_share_binary.png` (+ `dark/`) | `cd Code && uv run python 04_fig2_death_share_binary.py` |
| `Code/05_fig3_creatinine_ejection.py` | Figure 3: serum creatinine (log axis) against ejection fraction, coloured by outcome | as above | `Code/outputs/figures/fig3_creatinine_ejection.png` (+ `dark/`) | `cd Code && uv run python 05_fig3_creatinine_ejection.py` |

**Environment:** Python 3.12.15 with pandas 3.0.5 (all scripts), scikit-learn 1.9.1 (`02_split.py`, `core.py`, `06_check_eq350.py`; scipy, installed with it, for the eq. 3.50 check; joblib, installed with it, to save the final model in `core.py explain`), and matplotlib 3.11.1 with `viz_style.py` (figure scripts) (`Code/check_env.py`, 14 October 2026).

## References

- Ahmad, T., Munir, A., Bhatti, S. H., Aftab, M. and Raza, M. A. (2017). [Survival analysis of heart failure patients: a case study](https://doi.org/10.1371/journal.pone.0181001). *PLoS ONE*, 12(7), e0181001. The article itself was not opened; its data supplement ([S1 Data](https://doi.org/10.1371/journal.pone.0181001.s001)) was downloaded and compared (Analysis Log row 2).
- Chicco, D. and Jurman, G. (2020). [Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone](https://doi.org/10.1186/s12911-020-1023-5). *BMC Medical Informatics and Decision Making*, 20, 16. The "Dataset" section was read in step 1. In step 5 the full text (open access, [PMC6998201](https://pmc.ncbi.nlm.nih.gov/articles/PMC6998201/); retrieved through the Europe PMC API) was checked for the direction cited in the `Discussion`:
  - The direction appears in Table 3 only. Patients who died had a lower median ejection fraction (30 against 38 %) and a higher median serum creatinine (1.30 against 1.00 mg/dL) than those who survived, among all 299 patients.
  - The text ranks the two measurements as the most important features without stating a direction, and Table 6 gives absolute correlations only.
- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R).
- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published). Read at smlbook.org; pp. 60–61 (eq. 3.48–3.50) were opened for the L2 check in step 4. Page references in the Decision Records come from `ML Guide.md`.
