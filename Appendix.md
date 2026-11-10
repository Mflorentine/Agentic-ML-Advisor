# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

### Provenance

- File: `Attachments/Student Dropout/data.csv`.
- Source: UCI Machine Learning Repository, [Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697), dataset 697, DOI 10.24432/C5MC89. Downloaded on 10 November 2026 by the user, from the UCI page. Not the publisher's live file of a different form: the user's answer is that it is the best available form (see below).
- Licence: CC BY 4.0, as stated on the UCI page (found by search on 10 November 2026; the page itself was not opened in this step).
- Citation given by UCI: Realinho, Vieira Martins, Machado and Baptista (2021), with the DOI above.
- Why this file: the user wants it for work on student outcomes in education.
- Institution: not named on the UCI page, which says only "a higher education institution" in Portugal. As stated by the user: all four creators are at the Instituto Politécnico de Portalegre, so it is likely the source. **Unverified:** the page does not state the institution, and the creators' affiliations have not been checked.
- Years: not given on the UCI page. As stated by the user: a later paper by the same authors (Realinho et al., 2022, *Data*) gives the enrolment years as 2008/09 to 2018/19. **Unverified:** that paper has not been opened or checked.
- Best available form: the user judged this file to be the best available form. No archived or fuller version was searched for; the user's answer is recorded as given.
- Checked against the UCI metadata (archive.ics.uci.edu, dataset 697 API, read 10 November 2026): 4,424 instances and 36 features, matching the file (36 inputs and `Target`). The checksum is recorded below for later comparison.
- SHA-256: `3ef126de5cefff26eb11fbb4237f1a1401cb64b488e2f1d598c23cedeb4c45ae`; 533,230 bytes.
- Checked with `Code/dropout/01_describe_data.py`, output `Code/outputs/dropout/01_describe.md`. The file itself is not modified.

### Describing pass (what is in the file)

- Shape: 4,424 data rows, 37 columns: 36 candidate inputs and `Target`.
- Format: semicolon-separated, UTF-8 with a byte-order mark, CRLF line endings, one header row.
- Header: one name carries a trailing tab, `Daytime/evening attendance	`, as found in the file. The script strips it when reading; the original file is not changed.
- Missing values: none. Fully duplicated rows: none.
- Candidate target `Target`, three labels: Graduate 2,209 (49.9%), Dropout 1,421 (32.1%), Enrolled 794 (17.9%). The UCI page says the status is taken at the end of the normal duration of the course (DR-04).
- Types: 36 inputs are numeric (integer or decimal). None are text. Nine integer columns carry code lists in the UCI documentation and are categorical (DR-05): `Marital status`, `Application mode`, `Course`, `Previous qualification`, `Nacionality`, the two parents' qualifications and the two parents' occupations. The yes/no flags and counts stay as 0/1 or whole numbers.
- Columns that look like period-level economic values: `Unemployment rate`, `Inflation rate` and `GDP` each take only 9 or 10 distinct values across the 4,424 rows, so many rows share the same value. Whether rows are grouped by period was asked as Admissibility 3; the user answered one row per student (DR-02).
- Units: the UCI documentation gives no units for any of the 37 variables (the field is null throughout). The units are stated in the description only for `Unemployment rate` and `Inflation rate` (%). `GDP` has no stated unit. The documentation gives ranges of 0 to 200 for the previous and admission grades and 0 to 20 for the semester grades.
- Documentation inconsistency: the description of `Curricular units 2nd sem (without evaluations)` says "1st semester". Kept as the publisher's wording; recorded here, not corrected.

### User's experience

Intermediate, in the user's own words (recorded 10 November 2026). The depth of explanation follows this level; it does not change what is reported.

### Decisions in step 1

| Decision | What was recorded | Record |
| --- | --- | --- |
| Target and leakage | The candidate target is `Target`, a three-class label. The UCI page says it is the student's status at the end of the normal course duration (3 years, 4 for Nursing). The inputs are information known at enrolment and the first and second semester results. The user set no column aside: nothing in the documentation shows a column recorded after the outcome. | DR-04 |
| Categorical inputs | Nine columns categorical (25% of the 36 inputs); flags and counts numeric. | DR-05 |
| Rare category levels | Levels with fewer than 10 training students grouped into "other", within each categorical input (step 3, the user's choice). | DR-13, DR-14 |
| Scope | All 4,424 rows used; no exclusion, no cleaning. | DR-06 |
| Missing data | None present (0 cells). Nothing imputed. | DR-06 |
| Accepted as-is | The publisher says it preprocessed the data for anomalies, unexplainable outliers and missing values, without saying what it changed. The data is used as published. The description inconsistency above is kept. | DR-06 |
| Grouping and time order | One row per student (DR-02). | DR-02 |
| Units | Not given by the publisher; see above. Not inferred from column names. | DR-06 |

### Decisions still open in step 1

The institution and years are recorded as the user stated them, both unverified. The publisher gives no units, which are recorded as unknown. Step 1 is not yet closed.

## Problem Definition

### Discussion

Four candidate formulations were offered, each taken from what the variables mean and not from any result: dropout after year one (Dropout yes/no from enrolment information and both semesters' results); dropout before year one (the three-way status from enrolment information only); the three-way status at the end of the course; and the second-semester grade. No model was fitted to compare them. The user chose dropout after year one, and the other three are not pursued in this analysis. Admissibility 2 was answered "predict new students" (DR-07), so the prediction workflow applies. For the 794 students still Enrolled at the end of the course, the user chose to count them as not dropped out, rather than leave them out (DR-08).

### Problem

- **Predicted (y):** Dropout yes/no. Dropout = 1; Graduate and Enrolled = 0 (DR-08).
- **From (x):** all 36 inputs: enrolment information and the first and second semester results. Nine are categorical (DR-04, DR-05).
- **Output type (Property 1):** binary (DR-11).
- **Use:** as the candidate describes it, deciding which students receive support after year one. The user has not stated the use beyond that description.
- **Costs of errors:** a missed dropout costs more than an unneeded flag (user, DR-09).
- **Metric that decides between models:** F2 (user, DR-09).
- **Monitored alongside:** recall, precision and the confusion matrix (user, DR-09).
- **Success criterion:** on the locked test rows, the chosen model's F2 is above the F2 of flagging every student on the same rows (user, confirmed, DR-09).
- **Baseline:** the most common training class, "not dropout" for every student, F2 = 0 (SEQ-1, DR-09). Flagging every student is a reference reported beside the model, not the baseline.
- **Achievable level:** not known.
- **Must-haves:** no requirement on interpretability (Property 5). A decision threshold is tuned on training data (Property 6). No predictions outside the range of the data (Property 7).
- **Expectations about the relationship (Property 8):** none stated by the user, recorded as unknown.
- **Split:** random, 20% test, stratified by Dropout, seed 2026: 3,539 training and 885 test students. The test set is locked until the final evaluation (DR-10).

### Sub-tasks

1. Dropout after year one: predict Dropout yes/no for new students from enrolment information and the first and second semester results. Success is the criterion above, measured by F2 on the locked test set, against the two references.

## Analysis

### Properties 9 and 10 (step 3)

Computed by `Code/dropout/03_properties_9_10.py` with the interim core `Code/dropout/core.py`, on the 3,539 training students only. Results and the core's version are in DR-12. Property 10 is balanced: Dropout is 32.1% of the training rows, above the 20% line. Property 9 is no: an unregularised logistic regression reaches 89.4% training accuracy, not 100%, so the classes are not perfectly separable. The test set is not read.

### Figure 1: approved units by outcome (step 3)

`Code/dropout/fig1_approved_units.py` plots the total of first- and second-semester approved units, per student, for the 3,539 training students. The horizontal axis is the total; each bar is the share of its outcome's students with that total. The plotted numbers are in `Code/outputs/dropout/fig1_approved_units.csv`. In the Dropout group, 436 of 1,137 students have a total of zero approved units; in the not-dropout group, 99 of 2,402 do. These counts are from the file and are not interpretations. Light and dark variants are in `Code/outputs/dropout/figures/` and `figures/dark/`. The figure is in `Project Report.md`, under Results, The training data.

### Figure 2: dropout share by tuition status (step 3)

`Code/dropout/fig2_tuition_share.py` plots, for the 3,539 training students, the share who dropped out in each group of tuition status. Fees up to date: 762 of 3,104 students dropped out. Fees not up to date: 375 of 435. The plotted numbers are in `Code/outputs/dropout/fig2_tuition_share.csv`. Light and dark variants are in `Code/outputs/dropout/figures/` and `figures/dark/`. The figure is in `Project Report.md`, under Results, The training data, as Figure 2. The two groups differ greatly in size, so the bar for fees not up to date rests on 435 students. The figure describes the training rows only; it does not establish a cause.

### Cross-validation, round 1 (step 4c)

`Code/dropout/06_cv_round1.py` with `Code/dropout/cv.py` (interim core, not reviewed). Round 1 is the baseline and Logistic + L2 on the 3,539 training students, on 10 stratified outer folds (seed 2026). The full table is in `Code/outputs/dropout/06_cv_round1.md`; the decision is DR-20.

### Cross-validation, round 2 (step 4d)

`Code/dropout/07_cv_round2.py` with the same `cv.py`, on the same ten outer folds. Logistic + poly + L2 has mean F2 0.8305 against 0.8311 for Logistic + L2; the fold-by-fold difference is −0.0006 with SD 0.0116. Table: `Code/outputs/dropout/07_cv_round2.md`. Decision and prior agreement: DR-21 and DR-18.

## Decision Records

### DR-01 · Admissibility · step 1

- **Sub-task:** none yet (before step 2).
- **Date:** 2026-11-10.
- **Question:** Is there a recorded outcome for the rows the model would learn from? (*Admissibility 1: outcome recorded*)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| `Target` column | Graduate 2,209 · Dropout 1,421 · Enrolled 794; no missing values | M | `Code/outputs/dropout/01_describe.md` |
| User's answer | "Yes, recorded" | M | the user, in step 1 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 1: outcome recorded | recorded | `[B SML p. 15]` | continue |

- **Thresholds applied:** n/a.
- **Options considered:** continue · stop (not supervised).
- **Expectation:** n/a.
- **Decision:** The outcome is recorded for every row. The problem is supervised; work continues.
- **Why not:** n/a.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered "Yes, recorded".
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Data Summary.

### DR-02 · Admissibility · step 1

- **Sub-task:** none yet (before step 2).
- **Date:** 2026-11-10.
- **Question:** Do several rows belong to the same unit, or are rows ordered in time? (*Admissibility 3: grouped or time-ordered rows*)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "One row per student" | M | the user, in step 1 |
| Economic columns | `Unemployment rate`, `Inflation rate` and `GDP` take 9 or 10 distinct values each, so many rows share a value | M | `Code/outputs/dropout/01_describe.md` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 3: grouped or time-ordered rows | none | `[B SML pp. 16, 38–39, 329]` | random split; no group or time column |

- **Thresholds applied:** n/a.
- **Options considered:** random split · group split · time-ordered reformulation.
- **Expectation:** n/a.
- **Decision:** No group or time column. Rows are treated as independent students and the split is random. The shared economic values are recorded as a fact about the file, not as a grouping; if the user later says that rows sharing a period belong together, this record is superseded.
- **Why not:** n/a.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered "One row per student".
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Data Summary.

### DR-03 · Admissibility · step 1

- **Sub-task:** none yet (before step 2).
- **Date:** 2026-11-10.
- **Question:** Will the cases the model is used on look like these data? (*Admissibility 4: new cases like these*)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "Yes, same kind" (new students will be of the same kind: same kind of course, institution and period, recorded the same way) | M | the user, in step 1 |
| Institution and years (user's statement, unverified) | Instituto Politécnico de Portalegre, likely; enrolment years 2008/09 to 2018/19 per Realinho et al. (2022) | M | the user, in step 1; see `Appendix.md`, Data Summary, Provenance |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 4: new cases like these | yes | `[B SML pp. 328–329]` | continue |

- **Thresholds applied:** n/a.
- **Options considered:** continue · agree which data the validation and test sets should come from.
- **Expectation:** n/a.
- **Decision:** New cases are expected to look like these data. The estimate of error on new data is therefore an estimate for students like these. The institution and period are recorded as the user stated them, both unverified (Data Summary, Provenance): the institution is likely the Instituto Politécnico de Portalegre, and the enrolment years are 2008/09 to 2018/19 according to a later paper by the same authors.
- **Why not:** n/a.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered "Yes, same kind".
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Data Summary.

### DR-04 · Admissibility · step 1 (target and leakage)

- **Sub-task:** none yet (before step 2).
- **Date:** 2026-11-10.
- **Question:** What is the candidate target, how was its label produced, and are any columns recorded after the outcome or derived from it (leakage)?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Target | `Target`, three classes: Dropout, Enrolled, Graduate | M | UCI API, target_col |
| Label timing | "assessed at the end of the normal duration of the course" (3 years; 4 for Nursing) | M | UCI page, Additional Information; MDPI paper, Data 2022, 7, 146 (https://mdpi.com/2306-5729/7/11/146) |
| Input timing | "information known at the time of student enrollment ... and the students' academic performance at the end of the first and second semesters" | M | UCI page, Additional Information |
| User's decision | "Keep all inputs" | M | the user, in step 1 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 1: outcome recorded | recorded (DR-01) | `[B SML p. 15]` | continue |
| Leakage check: no column recorded after the outcome or derived from it | none found in the documentation | `[I]` | no column set aside |

- **Thresholds applied:** n/a.
- **Options considered:** keep all inputs · set aside the 1st and 2nd semester columns · set aside named columns.
- **Expectation:** n/a.
- **Decision:** The label is the student's status at the end of the normal course duration. No input is set aside as leakage. The 1st and 2nd semester results are recorded before that status, according to the documentation.
- **Why not:** the semester columns were not set aside because the documentation does not record them after the outcome, and the user chose to keep all inputs.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered "Keep all inputs".
- **Supersedes / superseded by:** none.
- **Links:** `Code/outputs/dropout/01_describe.md`.

### DR-05 · Input design · step 1 (categorical inputs)

- **Sub-task:** none yet (before step 2).
- **Date:** 2026-11-10.
- **Question:** Which integer columns are treated as categorical codes, and which as numbers?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Columns with code lists in the UCI documentation | Marital status (6 codes), Application mode (18), Course (17), Previous qualification (about 22), Nacionality (21), Mother's and Father's qualification (about 30 and 33), Mother's and Father's occupation (codes, with 0 = student) | M | UCI API, variable descriptions |
| User's decision | "Treat the code-list columns as categorical, and also the parents' occupation codes (they are codes, not amounts). Keep the yes/no flags as 0/1 numbers ... Keep the grade-like counts as numbers." | M | the user, in step 1 |
| Counts | 9 of 36 inputs categorical (25.0%); 27 numeric; 220 observed levels; 247 columns after one-hot encoding with no column dropped | computed from the file | `Code/outputs/dropout/01_describe.md` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design (ML Guide §9): domain transformations and the choice of inputs, decided with the user, not a configuration axis | decided with the user | `[B→I SML p. 18]` | input design fixed; not chosen by cross-validation |

- **Thresholds applied:** n/a. The share of categorical inputs for Property 4 is computed in step 2 (the High threshold is 50%).
- **Options considered:** code-list columns only · code-list columns plus flags and occupations · other.
- **Expectation:** n/a.
- **Decision:** Nine integer columns are categorical, to be one-hot encoded inside the folds. The yes/no flags and counts are numbers.
- **Why not:** the flags were not one-hot encoded, because that would add columns that duplicate the intercept, as the user noted from the Sepsis analysis.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered as quoted.
- **Supersedes / superseded by:** none. Extended by DR-13 (rare levels grouped); the categorical list stands.
- **Links:** `Code/dropout/01_describe_data.py`, `Code/outputs/dropout/01_describe.md`.

### DR-06 · Scope and cleaning · step 1

- **Sub-task:** none yet (before step 2).
- **Date:** 2026-11-10.
- **Question:** Which rows are used, what is cleaned, and what is accepted as published?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Rows | 4,424, all used | M | the user, in step 1 ("Use all 4,424 rows") |
| Missing cells | 0 | T | `Code/outputs/dropout/01_describe.md` |
| Fully duplicated rows | 0 | T | `Code/outputs/dropout/01_describe.md` |
| Publisher's preprocessing | "a rigorous data preprocessing to handle data from anomalies, unexplainable outliers, and missing values" (not described) | M | UCI page, Additional Information |
| Units | null for all 37 variables | M | UCI API |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Data summary decisions (step 1) | all rows used; no cleaning | `[I]` | none |

- **Thresholds applied:** n/a.
- **Options considered:** use all rows · exclude rows with a stated reason.
- **Expectation:** n/a.
- **Decision:** All 4,424 rows are used, with no cleaning and no imputation. The publisher's preprocessing is accepted as published, and units are not inferred.
- **Why not:** no exclusion, because no row was identified as wrong, and the user chose all rows.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered "Use all 4,424 rows".
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Data Summary.

### DR-07 · Admissibility · step 2

- **Sub-task:** none yet (the problem is being defined).
- **Date:** 2026-11-10.
- **Question:** Is the main aim to predict the outcome for new cases, or to understand how the variables are connected? (*Admissibility 2: prediction or understanding*)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "Predict new students" | M | the user, in step 2 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 2: prediction or understanding | predict | `[B SML p. 20]` | continue |

- **Thresholds applied:** n/a.
- **Options considered:** predict new cases · understand the connections (needs the user's confirmation to continue).
- **Expectation:** n/a.
- **Decision:** The aim is prediction for new students. Work continues on the prediction workflow.
- **Why not:** the understanding option was not chosen, so the confirmation it requires was not asked.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered "Predict new students".
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Problem Definition (to be written).

### DR-08 · FORM · step 2 (what is predicted, and how Enrolled is handled)

- **Sub-task:** none yet (the problem is being defined).
- **Date:** 2026-11-10.
- **Question:** What is predicted (y), from what (x), and how are the students still Enrolled treated?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Problem chosen | "Dropout after year one": predict Dropout yes/no from enrolment information and both semesters' results | M | the user, in step 2, chosen from four candidate formulations |
| Enrolled | "Count as not dropped out": Enrolled and Graduate both count as no | M | the user, in step 2 |
| Rows | 4,424 used; Dropout 1,421 (32.1%) | T | `Code/outputs/dropout/01_describe.md` |
| Inputs | all 36 inputs, nine categorical (DR-04, DR-05) | M | DR-04, DR-05 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 1: outcome recorded | recorded (DR-01) | `[B SML p. 15]` | the problem is supervised |
| Admissibility 2: prediction or understanding | predict (DR-07) | `[B SML p. 20]` | continue |
| Admissibility 4: new cases like these | yes (DR-03) | `[B SML pp. 328–329]` | continue |

- **Thresholds applied:** n/a.
- **Options considered:** Dropout yes/no from all 36 inputs (chosen) · Dropout yes/no from enrolment information only · three-way status · second-semester grade. Enrolled counted as not dropped out (chosen) · Enrolled left out.
- **Expectation:** n/a.
- **Decision:** Predict y = 1 if Dropout, 0 if Graduate or Enrolled, from all 36 inputs, for all 4,424 rows. The prediction is made with the first- and second-semester results available. Output type (Property 1) is binary, to be recorded in the PROP record.
- **Why not:** the three-way status and the second-semester grade were not chosen; the enrolment-only version was not chosen, because the user chose the year-one version. Leaving Enrolled out was not chosen, because the user chose to keep all rows.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered as quoted.
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Data Summary; `Code/outputs/dropout/01_describe.md`.

### DR-09 · FORM · step 2 (metric, success criterion, baseline, requirements)

- **Sub-task:** none yet (the problem is being defined).
- **Date:** 2026-11-10.
- **Question:** Which single metric decides between models, what counts as success, what is the baseline, and what must the predictions satisfy?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Error costs | "Missed dropout costs more" | M | the user, in step 2 |
| Metric | F2 score | M | the user, in step 2 |
| Success criterion | "Beat flagging everyone": F2 of the chosen model on the test rows above the F2 of flagging every student on the same rows, 5p/(4p+1) with p the positive share of those rows | M | the user, in step 2; the definition is ours, to be confirmed with the user |
| Baseline | most common training class: "not dropout" for every student, F2 = 0 | `[B SML pp. 330–331]` | ML Guide SEQ-1 |
| Property 5: interpretability | none | M | the user, in step 2 |
| Property 7: extrapolation | no | M | the user, in step 2 |
| Property 8: expected shape | unknown: no expectation stated | M | the user, in step 2 |
| Achievable level | not known | n/a | not yet asked |
| Monitored alongside F2 | recall, precision, confusion matrix | M | the user, in step 2 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 1: output type = binary | binary | `[B SML pp. 17–18]` | classification; logistic regression, k-NN, tree in scope |
| Property 6: probabilities or tuned threshold | yes: F2 needs a decision threshold chosen on training data | `[B SML pp. 92–93]` | threshold tuned in step 4 (guide §16) |
| SEQ-1: baseline | most common training class | `[B SML pp. 330–331]` | baseline F2 = 0 |
| Flag-everyone reference | reported beside the model; not the baseline; decides nothing | `[I]` | reference only, see note below |

- **Thresholds applied:** flag-everyone F2 = 5p/(4p+1) for the positive share p; computed on the test rows at step 4g.
- **Options considered:** F2 (chosen) · F1 (rejected: equal costs, contrary to the user's answer) · F-beta with another β · PR-AUC · plain accuracy (rejected: about one in three students is Dropout, so accuracy misleads, SML p. 91).
- **Expectation:** n/a.
- **Decision:** The model is compared by F2, with the missed-dropout cost weighted. Success: on the locked test set, the chosen model's F2 is above the F2 of flagging every student on the same rows. Baseline: the most common training class (F2 = 0).
- **Why not:** the other metrics above, for the reasons given. Must-haves: none beyond Property 6.
- **Note (a tension with the guide):** the guide describes the flag-everyone F2 as a reference that decides nothing (ML Guide §16). Using it as the success bar is the user's choice, recorded as theirs. If the guide's wording is to change, that is a FRAMEWORK change.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered as quoted; the success definition and the stratified split confirmed by the user.
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Problem Definition (to be written).

### DR-10 · SPLIT · step 2

- **Sub-task:** none yet (the problem is being defined).
- **Date:** 2026-11-10.
- **Question:** How is the data split into training and test rows, and is the test set locked?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Test fraction | 20% | M | the user, in step 2 |
| Groups | none (one row per student) | M | DR-02 |
| Seed | 2026 | M | the agent's choice, recorded here |
| Stratification | by y (Dropout yes/no), so both sets keep the same share | M | the agent's choice, recorded here; informed to the user, not asked |
| Result | train 3,539 (Dropout 1,137, 32.1%); test 885 (Dropout 284, 32.1%) | T | `Code/outputs/dropout/02_split.md` |
| File | row_id, split, y | T | `Code/outputs/dropout/02_split.csv`, SHA-256 `b7fcf12c6df9d72eb96335cb0a40e116b0ba55ae8196d3375db7f0a02e4bf4d5` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 3: grouped or time-ordered rows | none: random split | `[B SML pp. 16, 38–39, 329]` | random |
| Test set used once | locked until the final evaluation | `[B SML p. 74]`, `[B SML p. 328]` | no step before 4g reads split = test |

- **Thresholds applied:** n/a.
- **Options considered:** 20% test (chosen) · 10% test (not chosen).
- **Expectation:** n/a.
- **Decision:** A random 20% test set, stratified by Dropout, seed 2026. The test rows are locked.
- **Why not:** 10% test: the user chose 20%. Grouped split: no groups.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked (fraction) answered "20% test"; seed and stratification informed.
- **Supersedes / superseded by:** none.
- **Links:** `Code/dropout/02_split.py`, `Code/outputs/dropout/02_split.csv`, `Code/outputs/dropout/02_split.md`.

### DR-11 · PROP · step 2 (Properties 1–8)

- **Sub-task:** none yet (the problem is being defined).
- **Date:** 2026-11-10.
- **Question:** What are the values of Properties 1–8 for this formulation? (Properties 9–10 come from the training data in step 3.)
- **Evidence:**

| Property | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | binary (Dropout yes/no) | M | DR-08 |
| Property 2: data-to-parameter ratio | ample: 3,539 ÷ (247 + 1) = 14.3 | M | DR-10 and the encoding count in `Code/outputs/dropout/01_describe.md` |
| Property 3: number of inputs | many: 247 after one-hot encoding | M | `Code/outputs/dropout/01_describe.md` |
| Property 4: categorical share | low: 9 of 36 inputs = 25% | M | DR-05 |
| Property 5: interpretability | none | M | DR-09 |
| Property 6: probabilities or tuned threshold | yes: the F2 decision threshold is tuned on training data | M | DR-09 |
| Property 7: extrapolation | no | M | DR-09 |
| Property 8: expected shape | unknown: no expectation stated by the user | M | DR-09 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 2: limited if below 10 | ample (14.3) | `[I]` | ample |
| Property 3: many if above 20 | many (247) | `[I]` | many |
| Property 4: high if at least 50% | low (25%) | `[I]` | low |

- **Thresholds applied:** Property 2: 10 (`[I]`); Property 3: 20 (`[I]`); Property 4: 50% (`[I]`).
- **Options considered:** n/a (values, not choices).
- **Expectation:** n/a.
- **Decision:** Properties 1–8 as stated above.
- **Why not:** n/a.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** informed for Properties 2–4 (computed); asked for 1, 5–8.
- **Supersedes / superseded by:** superseded by DR-12 for Properties 9 and 10, and by DR-14 for Properties 2 and 3; Properties 1, 4–8 stand.
- **Links:** `Code/outputs/dropout/01_describe.md`, `Code/outputs/dropout/02_split.md`.

### DR-12 · PROP · step 3 (Properties 9 and 10, training rows only)

- **Sub-task:** none yet (the problem is being defined).
- **Date:** 2026-11-10.
- **Question:** Can the training classes be separated perfectly by a logistic regression with no regularisation, and is the class balance imbalanced? (Properties 9 and 10.)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Training rows | 3,539 (the test rows are not read) | T | DR-10, `Code/outputs/dropout/02_split.md` |
| Smallest class share | 32.1%: Dropout 1,137; Graduate or Enrolled 2,402 | T | `Code/outputs/dropout/03_props_9_10.md` |
| Training accuracy, unregularised logistic regression | 0.8938 (not 1.0); solver converged after 262 iterations of 10,000 | T | `Code/outputs/dropout/03_props_9_10.json` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 10: imbalanced if the smallest class is below 20% of training rows | balanced | `[I]` | the metric is handled as balanced (ML Guide §16) |
| Property 9: yes if the training accuracy reaches 100% | no | `[I]` | MOD-1 does not apply; Logistic and Logistic + poly remain admissible |
| MOD-1: separability = yes makes the unregularised logistic versions inadmissible | not triggered | `[B SML p. 61]` | none |

- **Thresholds applied:** 20% smallest-class share (`[I]`), compared with 32.1%; 100% training accuracy (`[I]`), compared with 89.4%.
- **Options considered:** n/a (properties are computed, not chosen).
- **Expectation:** n/a.
- **Decision:** Property 10: balanced. Property 9: no. These supersede the step 2 values for Properties 9 and 10 (DR-11).
- **Why not:** n/a.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** the user approved the interim core before it ran. The result is informed, not asked.
- **Supersedes / superseded by:** supersedes DR-11 for Properties 9 and 10.
- **Code version:** `Code/dropout/core.py`, SHA-256 `f6833dbed41de83c78e4b76734b5627e49c3b6386c92c9f815593a226b4c9ea4` (interim core, not reviewed). Run by `Code/dropout/03_properties_9_10.py`.
- **Note on the core:** the first run used `penalty=None`, which the installed scikit-learn deprecates. It gave the same result (training accuracy 0.8938, 262 iterations). The core was changed to `C=np.inf`, the replacement that scikit-learn names, before any output was used. The change does not alter the fit.
- **Links:** `Code/dropout/core.py`, `Code/dropout/03_properties_9_10.py`, `Code/outputs/dropout/03_props_9_10.md`.

### DR-13 · Input design · step 3 (rare category levels grouped)

- **Sub-task:** none yet (before step 2 ends and step 4 begins).
- **Date:** 2026-11-10.
- **Question:** Are the rare levels of the categorical inputs grouped, and if so, at what threshold? (ML Guide §9: domain transformations and the choice of inputs, decided with the user.)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "2, with the threshold fewer than 10 training students" (option 2 of five offered: keep as recorded; group rare levels; logarithm of skewed counts; summary feature per semester; leave out economic columns) | M | the user, in step 3 |
| Levels in training rows, before grouping | 212 across the nine categorical inputs | T | `Code/outputs/dropout/04_input_design.md` |
| Columns after grouping | 103 (one per kept level, plus one other per input with rare levels) | T | `Code/outputs/dropout/04_input_design.md` |
| Nationality | 21 levels, 17 with fewer than 10 training students (35 students); one level holds 97.4% | T | `Code/outputs/dropout/04_input_design.md` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design: domain transformations and the choice of inputs, decided with the user | grouping chosen | `[B→I SML p. 18]` | the input design is fixed; not a configuration axis |
| REQ-1: preprocessing fitted on training data only, inside each fold | applies | `[B SML p. 27]` + `[I]` | the grouping counts come from the training rows of each fold or fit |
| REQ-6: one-hot encode categorical inputs | applies after grouping | `[B SML p. 49]` | one column per kept level and one for other |
| Rare-level grouping rule | grouped if fewer than 10 training students | `[I]`, threshold chosen by the user | as above |

- **Thresholds applied:** 10 training students per level (the user's choice, `[I]`), compared with each level's training count in `Code/outputs/dropout/04_input_design.md`.
- **Options considered:** keep the inputs as recorded (not chosen) · group rare levels with a threshold of 10 (chosen) · logarithm of the skewed counts (not chosen) · summary feature per semester, approved as a share of enrolled units (not chosen) · leave out the three economic columns (not chosen).
- **Expectation:** n/a.
- **Decision:** Within each categorical input, levels with fewer than 10 training students are grouped into one "other" level, using training counts only. The grouping is applied inside each fold or fit. The nine categorical inputs listed in DR-05 are the inputs this applies to. Other inputs are unchanged.
- **Why not:** keeping the inputs as recorded leaves levels resting on very few students. The logarithm changes only the logistic regression and k-NN, and trees are unaffected by it. The summary feature and dropping the economic columns were not chosen.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked; answered as quoted. The user did not name the inputs: the rule is recorded as applying to all nine categorical inputs (to be confirmed).
- **Supersedes / superseded by:** none. Extends DR-05.
- **Links:** `Code/dropout/04_input_design_counts.py`, `Code/outputs/dropout/04_input_design.md`, `Code/outputs/dropout/04_input_design.csv`.

### DR-14 · PROP · step 3 (Properties 2 and 3, recounted under DR-13)

- **Sub-task:** none yet (before step 4 begins).
- **Date:** 2026-11-10.
- **Question:** What are Properties 2 and 3 once the rare levels are grouped, counted on the training rows?
- **Evidence:**

| Property | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Training rows | 3,539 | T | DR-10 |
| Numeric inputs | 27 | M | DR-05 |
| Categorical columns after grouping | 103 (from 212 training levels) | T | `Code/outputs/dropout/04_input_design.md` |
| Inputs after encoding | 130 (27 + 103), from 239 before grouping on the training rows | T | `Code/outputs/dropout/04_input_design.md` |
| Property 2: data-to-parameter ratio | 3,539 ÷ (130 + 1) = 27.0 | T | `Code/outputs/dropout/04_input_design.md` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 2: limited if below 10 | ample | `[I]` | ample |
| Property 3: many if above 20 | many | `[I]` | many |
| Property 4: categorical share, high at 50% or more | low (9 of 36 inputs, 25%): unchanged | `[I]` | low |

- **Thresholds applied:** Property 2 at 10 (`[I]`), compared with 27.0; Property 3 at 20 (`[I]`), compared with 130.
- **Options considered:** n/a (values, not choices).
- **Expectation:** n/a.
- **Decision:** Property 2: ample (27.0). Property 3: many (130). These supersede DR-11 for Properties 2 and 3. Properties 1, 4–8 are unchanged.
- **Why not:** n/a.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** informed.
- **Supersedes / superseded by:** supersedes DR-11 for Properties 2 and 3.
- **Note on basis:** DR-11 counted the levels in the whole file (220 levels, 247 inputs after encoding, and a Property 2 of 14.3). This record counts the training rows only, so the figures differ. Both bases give the same values for both properties (ample; many).
- **Links:** `Code/dropout/04_input_design_counts.py`, `Code/outputs/dropout/04_input_design.md`.

### DR-15 · FORM · step 4a (must-have: class probabilities)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Must the predictions include class probabilities? (Property 6: probabilities, ML Guide section 12: must-have)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "Yes, must-have" | M | the user, in step 4a |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Must-have: Property 6 probabilities = yes; families that meet it: Logistic | must-have stated | `[B→I SML pp. 50, 53–54]` | k-NN and Tree excluded with USER (DR-16) |

- **Thresholds applied:** n/a.
- **Options considered:** must-have (chosen) · not a must-have (all six structural configurations remain).
- **Expectation:** n/a.
- **Decision:** Class probabilities are a must-have. The admissible set is limited to the Logistic configurations.
- **Why not:** not a must-have was not chosen.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered "Yes, must-have".
- **Supersedes / superseded by:** none.
- **Links:** `Appendix.md`, Problem Definition (must-haves, to be read with this record).

### DR-16 · ADMSET · step 4a

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Which of the 14 structural configurations are admissible, given the property values and the must-have?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | binary | M | DR-08, DR-11 |
| Property 9: separability | no | T | DR-12 |
| Parameters including the intercept | 131 (130 encoded inputs and the intercept) | T | `Code/outputs/dropout/04a_admissible_set.json` |
| Parameters at least n_train (3,539) | no | T | as above |
| Rank of the training design | 120 of 131: 11 linear dependencies (see note) | T | as above |
| Must-have | Property 6: probabilities = yes | M | DR-15 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, Property 1 = binary | admits Logistic, k-NN and Tree | `[B SML pp. 17, 49–57]` | eight configurations EXCL (Linear, Poisson, Exponential, each with and without L2) |
| Must-have, Property 6 = yes | admits Logistic only | `[B→I SML pp. 50, 53–54]` | k-NN and Tree USER |
| MOD-1, Property 9 = yes | not triggered | `[B SML p. 61]` | none |
| MOD-2, parameters ≥ n_train or exact collinearity, unregularised linear and GLM | not reached: these are excluded by the task gate already | `[B→I SML pp. 46–47, 65]` | none on this set |

- **Thresholds applied:** n/a (the parameter count is compared with n_train: 131 against 3,539).
- **Options considered:** all 14 structural configurations (section 9).
- **Expectation:** n/a.
- **Decision:** Admissible: Logistic, Logistic + L2, Logistic + poly, Logistic + poly + L2. Four of 14.
- **Why not:** Linear (4), Poisson (2) and Exponential (2): EXCL, task gate. kNN and Tree: USER, must-have Property 6.
- **Note on collinearity:** the rank check finds 11 linear dependencies among the 131 parameters, identified on the training rows (`Code/outputs/dropout/04a_dependencies.md`, from `Code/dropout/04a_dependencies.py`). (a) Nine come from the one-hot columns: within each categorical input the dummies sum to the intercept (eight "other" columns and Course's level 9991, which is the last level of a full set). (b) Two are data facts, true of the training rows: `Daytime/evening attendance` is a combination of the Course columns, because each course has one attendance mode; and `International` equals 1 minus the Portuguese-nationality column. They do not change the admissible set: MOD-2 applies only to unregularised linear and GLM fits, which the task gate has already excluded. They matter for the core's parametric fits without L2: the redundant columns are to be dropped, or the fit regularised, before the Logistic configurations are cross-validated (4c). Predictions are not affected by the redundancy; the coefficients are.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** the must-have is the user's (DR-15); the core was approved before it ran.
- **Supersedes / superseded by:** superseded by DR-17 (MOD-2 now covers logistic regression, ML Guide §12, amended 10 November 2026). Kept as recorded under the earlier rule.
- **Code version:** `Code/dropout/admissible.py`, SHA-256 `f1b5f5731021d5cddf27b8497cd5178cc48351671d4c3ad874edc7ffe662e6df` (interim core, not reviewed). Run by `Code/dropout/04a_admissible_set.py`.
- **Links:** `Code/outputs/dropout/04a_admissible_set.md`, `Code/outputs/dropout/04a_admissible_set.json`.

### DR-17 · ADMSET · step 4a (supersedes DR-16)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Which of the 14 structural configurations are admissible under MOD-2 as amended on 10 November 2026?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | binary | M | DR-08, DR-11 |
| Property 9: separability | no | T | DR-12 |
| Parameters including the intercept | 131; below n_train (3,539) | T | `Code/outputs/dropout/04a_admissible_set.json` |
| Rank of the training design | 120 of 131: exactly collinear (11 dependencies, `Code/outputs/dropout/04a_dependencies.md`) | T | as above |
| Must-have | Property 6: probabilities = yes | M | DR-15 |
| Rule amendment | MOD-2 covers unregularised Logistic and Logistic + poly; ML Guide §12, amended 10 November 2026 (FRAMEWORK) | M | `ML Guide.md` version note, §12, §9 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, Property 1 = binary | admits Logistic, k-NN and Tree | `[B SML pp. 17, 49–57]` | eight configurations EXCL (Linear, Poisson, Exponential, with and without L2) |
| Must-have, Property 6 = yes | admits Logistic only | `[B→I SML pp. 50, 53–54]` | k-NN and Tree USER |
| MOD-1, Property 9 = yes | not triggered | `[B SML p. 61]` | none |
| MOD-2, amended: exact collinearity makes unregularised Logistic and Logistic + poly inadmissible | triggered (rank 120 of 131) | `[B→I SML pp. 46–47, 61, 63, 65]` | Logistic and Logistic + poly EXCL |

- **Thresholds applied:** n/a. The parameter count is compared with n_train: 131 against 3,539.
- **Options considered:** all 14 structural configurations (section 9).
- **Expectation:** n/a.
- **Decision:** Admissible: Logistic + L2 and Logistic + poly + L2. Two of 14.
- **Why not:** Logistic and Logistic + poly: EXCL, MOD-2 (non-unique coefficients without L2 under exact collinearity). Linear, Poisson and Exponential (with and without L2): EXCL, task gate. k-NN and Tree: USER, must-have Property 6.
- **Consequence for 4b:** the simple-first configuration (SEQ-2) is Logistic + L2. Cross-validation compares two configurations and the baseline.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** the user asked for the FRAMEWORK change (MOD-2 covers logistic regression), and set the must-have (DR-15).
- **Supersedes / superseded by:** supersedes DR-16.
- **Code version:** `Code/dropout/admissible.py`, SHA-256 `6996334d85a3e4caddb20b1982e182a29d9b892e9d86d581a589b9ec2a39df68` (interim core, not reviewed). Guide: `ML Guide.md` v3.1 with the 10 November 2026 FRAMEWORK entry. Run by `Code/dropout/04a_admissible_set.py`.
- **Links:** `Code/outputs/dropout/04a_admissible_set.md`, `Code/outputs/dropout/04a_admissible_set.json`.

### DR-18 · PRIOR · step 4b

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Status:** agreed by the user at 4b (method approved; threshold and flag choices in DR-19). No cross-validation has been run. Nothing is used from the test set.
- **Question:** Which admissible configurations are kept for cross-validation, and what order does the prior expect?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Admissible set | Logistic + L2, Logistic + poly + L2 | M | DR-17, `Code/outputs/dropout/04a_admissible_set.md` |
| Property 3: number of inputs | many (130 after encoding) | M | DR-14 |
| Property 6: probabilities | yes; must-have, so its matrix row (not a must-have) is not scored | M | DR-15 |
| Property 8: expected shape | unknown | M | DR-09 |
| Other properties | Property 1 binary (no row); Property 2 ample (no row); Property 4 low; Property 5 none; Property 7 no; Properties 9–10 no and balanced: no rows | M, T | DR-08, DR-11, DR-12, DR-14 |
| Scores | Logistic + L2: 0 · Logistic + poly + L2: −1 (Property 3 = many → + poly −1) | computed | `Code/outputs/dropout/04b_prior.md` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Suitability matrix, Property 3 = many → + poly | −1 | `[B→I SML p. 59]` | Logistic + poly + L2 scores −1 |
| Matrix row Property 6 = yes is marked not a must-have | not scored, since Property 6 is a must-have | `[B→I SML pp. 50, 53–54]` | Logistic + L2 scores 0, not +1 |
| Keep rule: baseline, simple-first (SEQ-2) and the three highest others (ties at third) | all of them kept; only one other configuration exists | `[B SML p. 331]` + `[I]` | none dropped |
| SEQ-2: simple-first with no add-ons; its +L2 version if MOD-2 applies | Logistic + L2 | `[B SML p. 331]`; MOD-2 (DR-17) | simple-first |
| SEQ-3: cross-validate the baseline and the simple-first first | round 1 is the baseline and Logistic + L2 | `[B SML pp. 331–332]` | round 2 is Logistic + poly + L2 |

- **Thresholds applied:** n/a.
- **Options considered:** Logistic + L2 (simple-first, rank 1, kept) · Logistic + poly + L2 (rank 2, kept) · the baseline (always kept, SEQ-1).
- **Expectation:** Logistic + L2 ranks above Logistic + poly + L2 in cross-validation, or the two are close. The reason: the poly terms add columns to a design with many inputs (ML Guide §13, Property 3), and the expected shape of the relationship is unknown, so the data give no evidence for curvature. If cross-validation shows the poly version clearly better, that disagrees with the expectation and will be recorded as such.
- **Decision:** Keep the baseline, Logistic + L2 and Logistic + poly + L2. None is DISF. The prior order is Logistic + L2, then Logistic + poly + L2.
- **Why not:** n/a; no configuration is excluded at this step.
- **Confidence:** n/a.
- **Outcome vs expectation:** filled in by DR-21 (round 2): **agree**. Logistic + L2 is first by mean F2 (prior: first), and Logistic + poly + L2 ties with it (margin −0.0006, SD 0.0116), which is the expected tie.
- **User involvement:** the method is for the user's agreement at 4b. The property values come from the user's answers recorded in DR-08, DR-09 and DR-15.
- **Supersedes / superseded by:** none.
- **Code version:** `Code/dropout/prior.py`, SHA-256 `746cce17fc35a82f60c0f3d895787eb1fac42b18d8e1e5631cb08c0042aab24c` (interim core, not reviewed). Run by `Code/dropout/04b_prior.py`.
- **Links:** `Code/outputs/dropout/04b_prior.md`, `Code/outputs/dropout/04b_prior.json`.

### DR-19 · FORM · step 4b (method choices: threshold and polynomial terms)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Where is the F2 decision threshold tuned, and which inputs get polynomial terms?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Threshold: user's answer | "Tune inside each model": the threshold is tuned in each configuration's inner CV for F2, as the L2 strength is | M | the user, in step 4b |
| Polynomial terms: user's answer | "Non-binary inputs only" | M | the user, in step 4b |
| Binary inputs excluded from the powers | Displaced, Educational special needs, Debtor, Tuition fees up to date, Gender, Scholarship holder, International, Daytime/evening attendance (8 inputs) | M | `Code/outputs/dropout/01_describe.md` |
| Non-binary numeric inputs given the powers | 19 inputs (counts, grades, age, application order, unemployment, inflation, GDP) | T | `Code/outputs/dropout/01_describe.md` |
| Approval of the method and `prior.py` | approved | M | the user, in step 4b |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §16 decision threshold: "Default 0.5. Tuned only if Property 6 = yes, after model selection, by CV on training data, with the trade-off chosen by the user." | **departure**: the threshold is tuned inside each configuration's inner CV, before the comparison | `[B→I SML pp. 53–54, 92–93]` + `[I]` | the comparison is at each configuration's best threshold; the §16 wording must be made to match by FRAMEWORK, which is not yet asked |
| Threshold grid | 0.05 to 0.95 in steps of 0.05 (19 values) | `[I]` (proposed by the agent; shown in the code before 4c) | inner-loop search |
| §9 polynomial terms: powers of each numerical input | the powers of the 8 binary inputs equal the inputs themselves, so they add no new models; powers are taken for the 19 non-binary numeric inputs | `[B→I SML p. 59]`, `[I]` | the family of models is unchanged; the design has no duplicated columns from the powers |

- **Thresholds applied:** the threshold grid (above); the 10-fold outer and 5-fold inner CV (§16); seed 2026.
- **Options considered:** threshold tuned inside each model (chosen) · literal §16 order: selection at 0.5, then tuning · selection by PR-AUC · poly for all numeric inputs · poly for non-binary inputs only (chosen).
- **Expectation:** n/a.
- **Decision:** tune the F2 threshold inside each configuration's inner CV over the grid; apply the polynomial terms to the 19 non-binary numeric inputs only.
- **Why not:** literal §16 order was not chosen, because at the default threshold the comparison would ignore the cost the user set for missed dropouts. PR-AUC was not chosen, because it changes the metric agreed in step 2. Powers of the flags were not taken, since they repeat the flags.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered as quoted; approved the method.
- **Supersedes / superseded by:** none. The FRAMEWORK change to §16 (10 November 2026) is applied: the threshold rule now matches this record.
- **Links:** `Project Report.md`, Methods, Dropout after year one.

### DR-20 · CV · step 4c (round 1: baseline and Logistic + L2)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Does Logistic + L2 beat the baseline by a clear margin in the outer folds, so that round 2 may start (SEQ-3)?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Outer folds | 10, stratified and shuffled, seed 2026; the same folds for both configurations; inner 5 folds | CV | `Code/outputs/dropout/06_cv_round1.md` |
| Baseline (most common class) | mean F2 0.0000, SD 0.0000; E_train 0.3213, E_val 0.3213 | CV | as above |
| Logistic + L2 | mean F2 0.8311, SD 0.0323; E_train 0.1945, E_val 0.2040 | CV | as above |
| Margin over baseline (fold by fold) | mean 0.8311, SD 0.0323; every fold positive (0.7692 to 0.8643) | CV | `Code/outputs/dropout/06_cv_round1.csv` |
| Chosen hyperparameters | L2 strength 0.001 in 7 folds, 0.01 in 3; threshold 0.15 in 8 folds, 0.20 in 2 | CV | as above |
| Flag-everyone reference (not the baseline) | F2 0.7030 mean, SD 0.0012, on the outer test folds | CV | computed from the same folds, 5p/(4p + 1) |
| Environment | Python 3.12.15, scikit-learn 1.9.1, pandas 3.0.5, numpy 2.5.2 | M | `check_env.py` output |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3: the simple-first configuration must beat the baseline before the others are compared | beats it | `[B SML pp. 331–332]` | round 2 may start; no DX-1 |
| C2 margin over the baseline: clear if the margin is at least 1 × spread | clear (0.8311 ≥ 0.0323) | `[I]` | none |
| §16 protocol: nested CV; threshold tuned inside each configuration (DR-19); preprocessing refitted inside each fold (REQ-1) | applied | `[B SML p. 27]`, `[I]`, `[B→I SML pp. 53–54, 92–93]` | the comparison is at each configuration's own threshold |

- **Thresholds applied:** the C2 margin threshold (1 × spread, `[I]`), compared with 0.8311 against 0.0323.
- **Options considered:** round 2 may start (chosen) · DX-1 sanity checks (not needed: the simple-first configuration beats the baseline).
- **Expectation:** n/a for round 1 (the expectation is in DR-18 for round 2).
- **Decision:** Logistic + L2 beats the baseline clearly on every outer fold. Round 2, Logistic + poly + L2 on the same folds, may start (4d).
- **Why not:** DX-1 was not triggered, because the baseline comparison is clear.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** the cross-validation code was approved before it ran (4c).
- **Supersedes / superseded by:** none.
- **Code version:** `Code/dropout/cv.py`, SHA-256 `fc11744d62cf6dc3e9cdf2f1591edeced0610fdf2a1d3a73b023071cb2a0cd29` (interim core, not reviewed). Run by `Code/dropout/06_cv_round1.py` (about three minutes).
- **Note on the code:** the first run failed on a type error in the grouping step, where integer codes and the label "other" were encoded together. The grouped values are now text before encoding. The method is unchanged. The record uses the corrected code.
- **Note on the reference:** the flag-everyone F2 is reported beside the model as §16 requires. It is not the baseline and decides nothing.
- **Links:** `Code/outputs/dropout/06_cv_round1.md`, `06_cv_round1.csv`, `06_cv_round1.json`.

### DR-21 · CV · step 4d (round 2: Logistic + poly + L2 on the same folds)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** How does Logistic + poly + L2 compare with Logistic + L2 and the baseline on the same outer folds, and does the CV order agree with the prior?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Baseline | mean F2 0.0000, SD 0.0000; E_train 0.3213, E_val 0.3213 | CV | `Code/outputs/dropout/07_cv_round2.md` |
| Logistic + L2 | mean F2 0.8311, SD 0.0323; E_train 0.1945, E_val 0.2040 | CV | as above |
| Logistic + poly + L2 | mean F2 0.8305, SD 0.0274; E_train 0.1756, E_val 0.1910 | CV | as above |
| Margin, Logistic + poly + L2 minus Logistic + L2 | mean −0.0006, SD 0.0116 (fold by fold) | CV | as above |
| Margin over the baseline | Logistic + L2 +0.8311 (SD 0.0323); Logistic + poly + L2 +0.8305 (SD 0.0274) | CV | as above |
| Poly chosen settings | degree 2 in all folds; L2 strength 0.001 in 6 folds, 0.01 in 3, 0.0001 in 1; threshold 0.15 or 0.20 | CV | `Code/outputs/dropout/07_cv_round2.json` |
| Prior (DR-18) | Logistic + L2 rank 1 (score 0); Logistic + poly + L2 rank 2 (score −1) | M | `Code/outputs/dropout/04b_prior.md` |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| C1, margin over the runner-up: clear if at least 1 × spread; moderate if at least 0.5 ×; otherwise none | none (|−0.0006| < 0.5 × 0.0116) | `[I]` | the two configurations are within noise |
| C2, margin over the baseline: clear if at least 1 × spread | clear for the leader, Logistic + L2 (0.8311 ≥ 0.0323) | `[I]` | none |
| Prior agreement: agree if the CV winner is the prior's first | agree: the CV leader by mean F2 is the prior's first | `[B SML p. 331]` (ordering rule as in §15) | none |
| §19 candidates: the eligible configuration with the best CV mean, plus any eligible configuration whose margin to it is none | both are eligible (C2 clear for each); both are candidates | `[I]` | step 4f applies the choice rule |

- **Thresholds applied:** C1 (1 × and 0.5 × the spread, `[I]`), compared with −0.0006 against 0.0116 and 0.0058. C2 (1 × the spread, `[I]`), compared with 0.8311 against 0.0323 (Logistic + L2) and 0.8305 against 0.0274 (poly).
- **Options considered:** Logistic + L2 (leader by mean F2) · Logistic + poly + L2 (runner-up, margin none).
- **Expectation:** n/a for round 2 itself (DR-18 gives the expectation). The outcome is recorded in DR-18.
- **Decision:** Round 2 is complete on the same folds. The two configurations do not differ beyond noise on the margin. Both beat the baseline clearly. The recommendation (4f) applies §19 and is not decided here.
- **Why not:** n/a: no configuration is dropped at this step.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a (this record is the outcome for DR-18).
- **User involvement:** informed. The method was approved at 4b.
- **Supersedes / superseded by:** none.
- **Breadth note:** two configurations and the baseline compared; no configuration was added after the prior.
- **Code version:** `Code/dropout/cv.py`, SHA-256 `{SHA}` (interim core, not reviewed; unchanged since round 1). Run by `Code/dropout/07_cv_round2.py`.
- **Links:** `Code/outputs/dropout/07_cv_round2.md`, `07_cv_round2.csv`, `07_cv_round2.json`.

### DR-22 · DX · step 4e (diagnosis pass 1, leading configuration Logistic + L2)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Which observation holds for the leading configuration, and which action follows (ML Guide §18)?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| E_train (mean over outer folds, misclassification rate: Property 10 = balanced) | 0.1945 | CV | `Code/outputs/dropout/06_cv_round1.md` |
| E_val (mean over outer folds) | 0.2040 | CV | as above |
| Gap = E_val − E_train | 0.0095 | CV | computed |
| C2 margin over the baseline | clear | CV | DR-20 |
| Chosen L2 strength (most common) | 0.001; per-fold values 0.0001, 0.001, 0.01: none at the grid edge in most folds | CV | `Code/outputs/dropout/06_cv_round1.json` |
| Chosen threshold (most common) | 0.15; per-fold 0.15 or 0.20: not at the grid edge (0.05 or 0.95) | CV | as above |
| Learning curve, C3 | not computed in this pass (see note) | n/a | n/a |

- **Observations (in the §18 order O1 > O2 > O5 > O3 > O4 > O6):**

| Observation | Test | Result | Note |
| --- | --- | --- | --- |
| O1 | C2 not clear | does not hold | C2 is clear |
| O2 | E_train worse than the success criterion, when in the same units | **not testable** | the criterion is stated in F2; E_train is a misclassification rate (Property 10 = balanced, §16). The units differ, so the test cannot be made. Raised with the user. |
| O5 | selected value at the grid edge in most outer folds | does not hold | λ and threshold interior |
| O3 | gap ≥ 2 × E_train (0.0095 against 0.3890) | does not hold | |
| O4 | E_train ≥ 2 × gap (0.1945 against 0.0190); Property 10 balanced, so no extra condition | **holds** | |
| O6 | C3 = limited | not computed | not reached: O4 holds first |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| O4 underfitting, ratio test | holds | `[B→I SML p. 334]` + `[I]` ratio 2 | the action is DX-5 |
| DX-5 actions: more polynomial terms only if Property 3 = few; add k-NN or Tree if not already compared; ask whether more input variables exist | poly not offered (Property 3 = many; compared in round 2); k-NN and Tree excluded by the must-have (USER, DR-16, DR-17), so not offered; **asking about more input variables needs the user** | `[B SML pp. 333–334]` | the loop stops for the user's answer |

- **Thresholds applied:** the 2 × ratio (`[I]`), compared with E_train 0.1945 against 0.0190 (O4) and gap 0.0095 against 0.3890 (O3).
- **Options considered:** DX-5 (chosen as the action that holds) · DX-2 (rethink the problem, for O2, if O2 held) · DX-1 (not triggered).
- **Expectation:** the action is expected to show a lower E_train for more flexibility or more information; no expectation is written for a stop.
- **Decision:** O4 holds. The only available DX-5 action asks about more input variables, which needs the user. The user answered that there are none. The loop passes to DX-10 (see DR-23).
- **Why not:** DX-3, DX-4 and DX-6 are not triggered, because O5, O3 and O6 do not hold (O6 not reached). O2 is not testable and is raised.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, answered: O2 treated as not holding ("Treat O2 as not holding"); no more input variables ("No more inputs").
- **Supersedes / superseded by:** none.
- **Stopping check:** none of S1–S6 applies yet; the loop waits for the user (S5 if the user stops it).
- **Note on O6:** the learning curve (§16: training fractions 10% to 100% on the outer folds) is needed for C3 at 4f. It is not computed here, because O4 holds first in the order. It will be computed, with its code shown for approval, when the loop resumes.
- **Code version:** the observations come from `Code/dropout/cv.py` (SHA-256 `fc11744d62cf6dc3e9cdf2f1591edeced0610fdf2a1d3a73b023071cb2a0cd29`) and the CV outputs (round 1, round 2).
- **Links:** `Code/outputs/dropout/06_cv_round1.md`, `Code/outputs/dropout/07_cv_round2.md`.

### DR-23 · FLAG · step 4e (diagnosis pass 2: the remaining action is out of scope)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** After O4 (underfitting) holds and no in-scope action remains, does the evidence suggest a method outside the solution space might help? (ML Guide §18 DX-10, §20, §23)
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| O4 holds | E_train 0.1945 ≥ 2 × gap 0.0095 | CV | DR-22 |
| In-scope actions for O4 | more polynomial terms: not offered (Property 3 = many); k-NN and Tree: excluded by the must-have (DR-15, DR-16); more input variables: none (user, DR-22) | M | DR-22 |
| O2 | treated as not holding (user) | M | DR-22 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| DX-10: the only remaining action is out of scope → flag it | applies | scope decision | a flag, not an action |
| S4: the next action is out of scope | applies | `[I]` | the loop stops (S4) |

- **Flags (not applied, not tested):**
  - Bagging, random forests and boosting (more flexible combinations of trees): Chapter 8 (§23). The evidence suggested is O4: E_train is high relative to the gap. This might help; it was not tested and is not claimed to do better.
  - Neural networks: Chapters 6–7 (§23). The same evidence. Not tested; not claimed to do better.
  - Kernel methods, support vector machines: Chapter 9 (§23). The same evidence. Not tested; not claimed to do better.
- **Thresholds applied:** n/a.
- **Options considered:** these three flags. None is applied.
- **Expectation:** n/a (flags make no claim about outcome).
- **Decision:** Record the three flags. Stop the loop under S4. The recommendation step (4f) applies to the configurations compared.
- **Why not:** none is applied, because each is outside the solution space (§9) and the book's chapter in §23 places it outside scope.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** informed. The user answered the DX-5 question (DR-22).
- **Supersedes / superseded by:** none.
- **Stopping check:** S4 (the next action is out of scope). S1 to S3, S5 and S6 do not apply: S1 and S2 need the test set, which is not used here; S3 needs two passes with no gain, and only one pass with an in-scope action was run.
- **Links:** `Appendix.md`, DR-22; these flags belong in the Discussion as open possibilities, with their chapters (step 5).

### DR-24 · CV · step 4f (learning curve and C3)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Is the learning curve of the leading configuration still falling at 100% of the training data (C3, ML Guide §17)?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Validation error (misclassification) by training fraction, mean over 10 outer folds | 10%: 0.2227; 20%: 0.2083; 30%: 0.2097; 40%: 0.2111; 50%: 0.1989; 60%: 0.2049; 70%: 0.2032; 80%: 0.2020; 90%: 0.2032; 100%: 0.2040 | CV | `Code/outputs/dropout/08_learning_curve.csv` |
| Drop from 80% to 100% (E_val at 80% minus at 100%) | −0.0020 (the error is slightly higher at 100%) | CV | `Code/outputs/dropout/08_recommendation.json` |
| Fold SD of E_val at 100% | 0.0307; threshold 0.5 × SD = 0.0153 | CV | as above |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| C3: limited if E_val at 100% is lower than at 80% by at least 0.5 × its fold SD | not met (the drop is negative) | `[B→I SML pp. 334–336]` + `[I]` | C3 = adequate |
| Learning curve: leading configuration only, training fractions 10% to 100% on the outer folds | applied; each fraction uses its outer fold's round-1 L2 strength and threshold, not re-tuned | `[B SML pp. 334–336]` | a limitation: the settings are not re-tuned at each fraction |

- **Thresholds applied:** 0.5 × fold SD (`[I]`), compared with a drop of −0.0020.
- **Options considered:** adequate · limited.
- **Expectation:** n/a.
- **Decision:** C3 = adequate. The validation error is flat from about 50% of the training data onward.
- **Why not:** limited was not chosen, because the error is not still falling.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** the code was approved before it ran (4f).
- **Supersedes / superseded by:** none.
- **Code version:** `Code/dropout/recommend.py`, SHA-256 `7168a855946942edce9a492cdee9002aba856ba670f8056eb5e771cc3c60dded` (interim core, not reviewed); `Code/dropout/cv.py`, SHA-256 `fc11744d62cf6dc3e9cdf2f1591edeced0610fdf2a1d3a73b023071cb2a0cd29`. Run by `Code/dropout/08_recommendation.py`.
- **Links:** `Code/outputs/dropout/08_learning_curve.csv`, `08_recommendation.md`, `08_recommendation.json`.

### DR-25 · FORM · step 4f (final tuning on all training rows)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Which L2 strength and F2 threshold are used for the single test refit at 4g (ML Guide §16: the threshold is chosen by CV on training data, with the trade-off chosen by the user)?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Method | 5-fold stratified CV on all 3,539 training rows, seed 2026; grid λ 1e-4 to 1e4 and threshold 0.05 to 0.95; chosen by mean inner F2 | CV | `Code/dropout/cv.py` (`inner_search`) |
| Chosen values | L2 strength 0.01; F2 threshold 0.20; inner mean F2 0.8305 | CV | `Code/outputs/dropout/08_recommendation.json` |
| Trade-off | F2: missed dropouts weighted (user, DR-09) | M | DR-09 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §16 decision threshold, as amended (10 November 2026): tuned inside the CV for F2 | applied | `[B→I SML pp. 53–54, 92–93]` + `[I]` | threshold 0.20 for the test refit |
| §16 final CV on training data | applied | `[I]` | λ 0.01 for the test refit |

- **Thresholds applied:** threshold grid 0.05 to 0.95 (`[I]`).
- **Options considered:** the values chosen on all training rows (chosen); the per-fold modes (λ 0.001, threshold 0.15) not used.
- **Expectation:** n/a.
- **Decision:** For the test refit: L2 strength 0.01 and F2 threshold 0.20. These are chosen on training data only.
- **Why not:** the per-fold modes were not used, because the final model is chosen by one CV on all training rows, as §16 specifies.
- **Confidence:** n/a.
- **Outcome vs expectation:** n/a.
- **User involvement:** informed; the trade-off is the user's (DR-09).
- **Supersedes / superseded by:** none.
- **Links:** `Code/outputs/dropout/08_recommendation.json`.

### DR-26 · FINAL · step 4f (recommendation rule and selection confidence; the test result at 4g)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** Which configuration does the recommendation rule (§19) choose, with what confidence (§17), and why are the others not chosen (§20)?
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Logistic + L2 | mean F2 0.8311; SD 0.0323 | CV | DR-20, DR-21 |
| Logistic + poly + L2 | mean F2 0.8305; SD 0.0274 | CV | DR-21 |
| Margin leader minus other | +0.0006, SD 0.0116 | CV | `Code/outputs/dropout/08_recommendation.json` |
| C2 (margin over the baseline), both | clear | CV | DR-20, DR-21 |
| C1 (margin over the runner-up) | none (0.0006 is below 0.5 × 0.0116) | CV | as above |
| C3 | adequate | CV | DR-24 |
| Prior (DR-18) | Logistic + L2 first (score 0); Logistic + poly + L2 second (score −1) | M | `Code/outputs/dropout/04b_prior.md` |
| Must-have (DR-15) | probabilities = yes: both configurations meet it | M | DR-15 |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19 step 1, eligible: C2 clear and every must-have met | both eligible | `[I]` | both candidates |
| §19 step 2, candidates: the best CV mean, plus eligible configurations within 0.5 × spread | both (the margin 0.0006 is below 0.5 × 0.0116) | `[I]` | both candidates |
| §19 step 3, choose: fewest add-ons, then higher prior score, then better CV mean | Logistic + L2 (no add-ons) | `[B SML p. 332]` | recommended |
| §17 confidence, Low if C1 = none or C2 not clear | Low (C1 = none) | `[I]` | confidence Low |
| Prior agreement (§17) | agree: the CV leader by mean F2 is the prior's first | `[B SML p. 331]` | none |
| Grounding (§17): matrix entries behind the prior score of Logistic + L2 | none scored (score 0); the must-have row is not scored | M | 0 [B], 0 [B→I], 0 [I] |
| Breadth note (§17): more than 10 configurations compared | no: two configurations | `[I]` | none |

- **Thresholds applied:** C1 at 1 × and 0.5 × the spread (`[I]`): 0.0006 against 0.0116 and 0.0058. C2 at 1 × the spread (`[I]`): 0.8311 against 0.0323.
- **Options considered:** Logistic + L2 (recommended) · Logistic + poly + L2 (not chosen: one add-on, no margin) · Logistic and Logistic + poly (EXCL, MOD-2) · the other eleven structural configurations (EXCL or USER).
- **Expectation:** n/a.
- **Decision:** Recommend Logistic + L2, with L2 strength 0.01 and F2 threshold 0.20 (DR-25). Selection confidence: Low. The factors are C1 none, C2 clear, C3 adequate, and prior agreement agree.
- **Why-not codes (all 14 structural configurations, §20):**

| Configuration | Code | Evidence |
| --- | --- | --- |
| Linear, Linear + L2, Linear + poly, Linear + poly + L2 | EXCL | task gate, Property 1 = binary (DR-16, DR-17) |
| Poisson, Poisson + L2, Exponential, Exponential + L2 | EXCL | task gate, Property 1 = binary |
| Logistic | EXCL | MOD-2: exactly collinear design, unregularised (DR-17) |
| Logistic + poly | EXCL | MOD-2: exactly collinear design, unregularised (DR-17) |
| kNN | USER | must-have: probabilities (DR-15) |
| Tree | USER | must-have: probabilities (DR-15) |
| Logistic + poly + L2 | SIMP | could not be told apart from the recommendation (margin 0.0006 < 0.5 × 0.0116); the simpler one chosen (DR-26) |

- **Flags:** three, from DR-23 (bagging and boosting, Chapter 8; neural networks, Chapters 6–7; kernel methods, Chapter 9). None applied, none tested.
- **Breadth note:** two configurations compared, so no optimism warning applies.
- **Confidence:** Low.
- **User involvement:** the method was agreed at 4b. The user is asked to approve the test-set use next.
- **Supersedes / superseded by:** none.
- **Code version:** `Code/dropout/recommend.py`, SHA-256 `7168a855946942edce9a492cdee9002aba856ba670f8056eb5e771cc3c60dded`; `Code/dropout/cv.py`, SHA-256 `fc11744d62cf6dc3e9cdf2f1591edeced0610fdf2a1d3a73b023071cb2a0cd29`. Run by `Code/dropout/08_recommendation.py`.
- **Test result:** not yet. Step 4g refits the recommended configuration on all training rows and evaluates the locked test set once, after your approval.

### DR-27 · FINAL · step 4g (single test-set evaluation of the recommended configuration)

- **Sub-task:** dropout after year one.
- **Date:** 2026-11-10.
- **Question:** How does the recommended configuration (Logistic + L2) perform on the locked test set, against the baseline and the flag-everyone reference, and is the success criterion met?
- **Use of the test set:** once, approved by the user at 4f′. The test set is not used again for this sub-task.
- **Evidence:**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Refit | Logistic + L2, L2 strength 0.01, F2 threshold 0.20, on 3,539 training rows | TEST | DR-25 |
| Test rows | 885, of which 284 Dropout (32.1%) | TEST | `Code/outputs/dropout/09_final_test.md` |
| F2 on the test rows, Logistic + L2 | 0.8350 | TEST | `Code/outputs/dropout/09_final_test.json` |
| F2, recomputed from the confusion counts (second route) | 0.8350; the two routes agree | TEST | `Code/dropout/09_final_test.py` (assertion) |
| Precision, recall | 0.6756; 0.8873 | TEST | as above |
| Confusion matrix (actual × predicted) | TN 480, FP 121; FN 32, TP 252 | TEST | as above |
| Baseline on the same rows (most common training class) | F2 0.0000 | TEST | as above |
| Flag-everyone reference on the same rows, 5p/(4p + 1) with p = 0.3209 | F2 0.7026 | TEST | as above |
| Uncertainty: SD across the ten outer folds of F2 (the method of ML Guide §5.2) | 0.0323 (fold mean 0.8311) | CV | `Code/outputs/dropout/07_cv_round2.csv` |
| Success criterion: F2 above flagging every student on the same rows | met | TEST | as above |

- **Rules applied:**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Test set used once per sub-task; the baseline reported beside the result | applied | `[B SML pp. 74, 328]` | locked |
| Uncertainty: fold SD, with the number of test rows and positives reported | applied | `[B→I SML pp. 71–73]` + `[I]` | 885 rows, 284 positives |
| Flag-everyone reference: reported beside the model on the test rows; not the baseline; decides nothing | applied | `[I]` | reference only |
| Success criterion (agreed at step 2, DR-09) | met | M | none |

- **Thresholds applied:** n/a.
- **Options considered:** n/a (the evaluation was a single run of the agreed configuration).
- **Expectation:** n/a.
- **Decision:** The success criterion is met. Test F2 0.8350, against 0.7026 for flagging every student on the same rows and 0.0000 for the baseline. The fold SD is 0.0323.
- **Why not:** n/a.
- **Confidence:** Low (DR-26); the test result does not change the confidence, which rests on the cross-validation factors.
- **Outcome vs expectation:** n/a.
- **User involvement:** asked, approved the test use (4f′); the script was approved before it ran.
- **Supersedes / superseded by:** none.
- **Code version:** `Code/dropout/cv.py`, SHA-256 `fc11744d62cf6dc3e9cdf2f1591edeced0610fdf2a1d3a73b023071cb2a0cd29` (interim core, not reviewed); `Code/dropout/09_final_test.py`.
- **Links:** `Code/outputs/dropout/09_final_test.md`, `09_final_test.json`, `09_test_predictions.csv`.


## Recommendation

### Sub-task 1 — Dropout after year one

**1. Problem.** Predict Dropout yes/no (Dropout = 1; Graduate or still Enrolled = 0) for students not yet in the data, from all 36 inputs: enrolment information and the first and second semester results; nine inputs categorical, rare levels grouped (DR-05, DR-08, DR-13). Output: binary (Property 1, DR-11). Metric: F2 (DR-09). Success criterion: on the test rows, the model's F2 above the F2 of flagging every student on the same rows (DR-09). Baseline: most common training class, F2 = 0 (DR-09). Must-have: class probabilities (Property 6, DR-15). Property 5: none; Property 7: no; Property 8: unknown (DR-09). Admissibility 1: outcome recorded (DR-01); Admissibility 2: predict new students (DR-07); Admissibility 3: one row per student, no grouping (DR-02); Admissibility 4: yes, same kind of student (DR-03). Split: random, 20% test, stratified by Dropout, seed 2026: 3,539 training and 885 test rows (DR-10).

**2. Recommendation.** Logistic regression with an L2 penalty (`Logistic + L2`), L2 strength 0.01 and F2 decision threshold 0.20, chosen by 5-fold cross-validation on all training rows (DR-25). Selection confidence: Low (DR-26).

**3. Test-set result.** F2 = 0.8350 on the test rows (uncertainty: SD across the ten outer folds of F2, 0.0323), n_test = 885, of which 284 Dropout. Baseline on the same rows: F2 = 0.0000. Success criterion: met. Threshold 0.20, chosen inside the cross-validation on training data for F2 (DR-19, DR-25). Flag-everyone F2: 0.703 on the training rows (mean over the outer folds, DR-20) and 0.7026 on the test rows, beside the model's 0.831 (training folds) and 0.8350 (test). Confusion matrix on the test rows: TN 480, FP 121, FN 32, TP 252. Precision 0.6756; recall 0.8873 (DR-27).

**4. Why this configuration.**
- Constraints: the task gate admits Logistic, k-NN and Tree for a binary output (DR-16). The must-have, class probabilities, excludes k-NN and Tree (USER, DR-15). MOD-2 excludes plain Logistic and Logistic + poly, because the encoded design is exactly collinear and their coefficients are not unique without L2 (DR-17).
- CV evidence: margin over the baseline 0.8311 (spread 0.0323), clear (DR-20). Margin over the runner-up, Logistic + poly + L2: 0.0006 in favour of Logistic + L2 (spread 0.0116), so none (DR-26).
- Simplicity: the §19 within-noise step applies. Both configurations are candidates; the fewer add-ons rule chooses Logistic + L2 (no add-ons; DR-26).
- Prior support: score 0, with no matrix entries scored (DR-18, DR-26).

**5. Ranking.**

| Configuration | Prior rank | Prior score | Post-prior | CV mean F2 | Margin vs recommended (± spread) | Margin vs baseline (± spread) | Code |
| --- | ---: | ---: | --- | ---: | --- | --- | --- |
| Logistic + L2 | 1 | 0 | no | 0.8311 | recommended | +0.8311 (± 0.0323) | recommended |
| Logistic + poly + L2 | 2 | −1 | no | 0.8305 | −0.0006 (± 0.0116) | +0.8305 (± 0.0274) | SIMP |
| Baseline (most common class) | n/a | n/a | n/a | 0.0000 | n/a | n/a | n/a |

**6. Prior versus evidence.** Agree: the cross-validation leader by mean F2 (Logistic + L2) is the prior's first. The expectation that Logistic + poly + L2 would tie or do worse was met: it ties (DR-18, DR-21).

**7. Why not the others.**
- EXCL (task gate): Linear, Linear + L2, Linear + poly, Linear + poly + L2, Poisson, Poisson + L2, Exponential, Exponential + L2 (DR-16, DR-17).
- EXCL (MOD-2, exactly collinear design, unregularised): Logistic, Logistic + poly (DR-17).
- USER (must-have, class probabilities): kNN, Tree (DR-15).
- DISF: none. All admissible configurations were kept (DR-18).
- BASE: none. Both admissible configurations beat the baseline clearly (DR-20, DR-21).
- OUTP: none. Logistic + poly + L2 is not clearly outperformed by the recommendation.
- SIMP: Logistic + poly + L2. It could not be told apart from the recommendation: its margin is 0.0006, below half the spread (0.0116); the simpler one is chosen (DR-26).
- Flags, not applied and not tested (DR-23): bagging, random forests and boosting (Chapter 8, SML §23); neural networks (Chapters 6–7); kernel methods and support vector machines (Chapter 9). Each might help with the underfitting observed at O4 (DR-22); none was tested, and none is claimed to do better.

**8. Confidence.** Selection confidence Low: C1 none (margin 0.0006 against spread 0.0116), C2 clear (0.8311 against 0.0323), C3 adequate (the validation error at 100% of the training data is not lower than at 80%; the drop is −0.0020 against a threshold of 0.0153) (DR-24, DR-26). Rule: Low if C1 = none or C2 not clear. Prior agreement: agree. Grounding of the recommended configuration: [B] 0, [B→I] 0, [I] 0 (score 0, no matrix entries scored). Breadth note: two configurations compared; no optimism warning applies.

**9. How the model predicts.** The model adds up the inputs, each multiplied by a weight learned from the training data, and turns the total into a probability between 0 and 1 that the student drops out. A student is flagged when that probability is at least 0.20. The L2 penalty keeps the weights small, so that no single input dominates; its strength, 0.01, was chosen by cross-validation (DR-25). Each category of a categorical input has its own weight, with rare categories grouped into "other" (DR-13). The predictions are only as good as the average student resembling those in the data: the model is not a rule for any single student.

**10. Use and limits.** The model can flag students for review in this kind of course, at this kind of institution, and at a comparable time (DR-03). It has not been checked on students from another institution or period. Its error is an average over students like these; it says nothing about the worst single prediction. The test estimate has a spread of 0.032 across folds, with 885 test rows and 284 Dropout cases, so a few predictions either way move F2 noticeably. Data limits from step 1, each beside the claim it qualifies: the outcome is the status at the end of the normal course length, as the UCI page describes it, and students still Enrolled are counted as not dropped out (DR-04, DR-08). The publisher's preprocessing for outliers and missing values is not described, and the data are used as published (DR-06). No units are given for any column, and the economic columns take about ten values shared by many students (DR-02, DR-06). The institution and enrolment years are not verified (Data Summary, Provenance).

**11. Improvement history.**
- Pass 1 (DR-22): O1 does not hold; O2 is not testable (the criterion is in F2 and E_train is a misclassification rate), treated as not holding by the user; O5 does not hold; O3 does not hold (gap 0.0095 against 2 × E_train 0.3890); O4 holds (E_train 0.1945 at least 2 × gap 0.0190). Action DX-5: more polynomial terms not offered (Property 3 = many); k-NN and Tree excluded by the must-have; more input variables: none, by the user's answer.
- Pass 2 (DR-23): the remaining action is out of scope; three flags recorded, none applied. Stopped by S4.
- The learning curve (C3) was computed at 4f, not as a diagnosis pass (DR-24).

**12. Thresholds applied.**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Rare category level (DR-13) | fewer than 10 training students | level counts in `Code/outputs/dropout/04_input_design.md` |
| Property 2, limited data-to-parameter ratio | < 10 | 27.0 (DR-14) |
| Property 3, many inputs | > 20 | 130 (DR-14) |
| Property 4, high categorical share | ≥ 50% | 25% (DR-05) |
| Property 10, imbalance | smallest class < 20% | 32.1% (DR-12) |
| Property 9, separability | training accuracy 100% | 89.4% (DR-12) |
| Diagnosis O3 and O4, ratio | 2 | gap 0.0095; E_train 0.1945 (DR-22) |
| C1 and C2, margins | 1 × spread; 0.5 × for C1 | 0.0006 against 0.0116; 0.8311 against 0.0323 (DR-26) |
| C3, learning curve | 0.5 × fold SD | drop −0.0020 against 0.0153 (DR-24) |
| F2 threshold grid, inner CV | 0.05 to 0.95 in steps of 0.05 | selected 0.20 (DR-25) |
| L2 strength grid, inner CV | 10⁻⁴ to 10⁴ | selected 0.01 (DR-25) |

**13. Trace and provenance.** DR-01 to DR-27 (DR-16 and DR-17 both recorded; DR-16 is superseded by DR-17; DR-11 is partly superseded by DR-12 and DR-14). Tag occurrences across these records: [B SML] 33 · [B→I SML] 16 · [I] 50 · UNLISTED 0. A tag written in more than one table counts more than once.


## Analysis Log


| # | What was done | Output |
| --- | --- | --- |
| 1 | Started the `dropout` analysis. Copied `Templates/Report.md` and `Templates/Appendix.md` to the root (the root files already matched the templates, so there was no earlier analysis to submit). Ran the describing pass on `Attachments/Student Dropout/data.csv`. No cleaning, no decisions. | `Code/outputs/dropout/01_describe.md` |
| 2 | Recorded the provenance (UCI, downloaded 10 November 2026, user judged it the best available form), the user's experience (intermediate) and the reason for the file. No cleaning, no decisions. | `Appendix.md`, Data Summary |
| 3 | Asked Admissibility 1, 3 and 4 in closed questions. Answers: outcome recorded; one row per student (no grouping or time order); new cases of the same kind. | DR-01, DR-02, DR-03 in Decision Records |
| 4 | Read the UCI documentation (API metadata, checked against the file's counts; no units given). Asked the leakage, categorical and rows questions. Answers: keep all inputs; nine categorical inputs; all 4,424 rows. Reran the describing pass with the categorical split. | DR-04, DR-05, DR-06; `Code/outputs/dropout/01_describe.md` |
| 5 | Recorded the institution and enrolment years as the user stated them, both unverified (the UCI page names neither; the 2022 paper was not opened). | DR-03; `Appendix.md`, Data Summary, Provenance |
| 6 | Step 1 closed by the user on 10 November 2026. The institution and years stay marked unverified; the 2022 paper has not been opened. Draft Abstract written in `Project Report.md`. | `Project Report.md`, Abstract |
| 7 | Step 2 begun. The user chose one of four candidate formulations: Dropout yes/no after year one. Admissibility 2 answered: predict new students. The Enrolled rule chosen: counted as not dropped out. | DR-07, DR-08 |
| 8 | Asked the error costs (missed dropout costs more), the metric (F2), the success criterion (beat flagging everyone), and Properties 5, 7 and 8 (no requirement; no extrapolation; no expectation). The baseline is the guide's SEQ-1 rule. | DR-09 |
| 9 | Asked the test fraction: 20%. Wrote and ran the split: random, stratified by Dropout, seed 2026; train 3,539, test 885. Test set locked. Properties 1–8 recorded. | DR-10, DR-11; `Code/dropout/02_split.py`, `Code/outputs/dropout/02_split.md` |
| 10 | Monitored metrics: recall, precision, confusion matrix. The user confirmed the success definition and the stratified split. Wrote the Problem Definition (Discussion, Problem, Sub-tasks), the Introduction, `Data and evaluation` in Methods, the references, and the draft Abstract in `Project Report.md`. No model fitted. | DR-09, DR-10; `Appendix.md` Problem Definition; `Project Report.md` |
| 11 | Step 2 closed by the user on 10 November 2026. Open and left as recorded: the decision the prediction serves (not yet stated in the user's words; the candidate's description stands in the Problem section), and the achievable level (not given). The book references are from the guide and not yet checked against the book's title page. | `Appendix.md` Problem Definition; `Project Report.md` |
| 12 | Step 3 begun. Approved the interim core for Properties 9 and 10. Ran it on the training rows: balanced (smallest class 32.1%), not separable (training accuracy 0.8938). The core's first draft used a setting the installed scikit-learn deprecates; changed to the replacement before any output was used. | DR-12; `Code/dropout/core.py`, `Code/dropout/03_properties_9_10.py`, `Code/outputs/dropout/03_props_9_10.md` |
| 13 | Proposed three training-data figures; the user chose approved units by outcome, with shares within each group and both semesters combined. Drew Figure 1 on the training rows, light and dark, and placed it in Results, The training data. Figure 1 in the report is the light variant. | `Code/outputs/dropout/figures/fig1_approved_units.png`; `Code/outputs/dropout/fig1_approved_units.csv`; `Project Report.md`, Results |
| 14 | Drew Figure 2 (dropout share by tuition status, training rows only) after the user's yes, light and dark, and placed it in Results, The training data. Updated the draft Abstract to mention it. | `Code/outputs/dropout/figures/fig2_tuition_share.png`; `Code/outputs/dropout/fig2_tuition_share.csv`; `Project Report.md`, Results and Abstract |
| 15 | Step 3 closed by the user on 10 November 2026. Figures 1 and 2 are the training-data figures in the report. The semester-grade scatter was offered and not chosen; it is not drawn and not in the report. | `Project Report.md`, Results, The training data |
| 16 | Input design: the user chose option 2, grouping rare category levels (fewer than 10 training students). Counted the result on the training rows: 212 levels become 103 columns; inputs after encoding 130; Property 2 27.0 (ample), Property 3 130 (many). Recorded as DR-13 and DR-14. | DR-13, DR-14; `Code/dropout/04_input_design_counts.py`, `Code/outputs/dropout/04_input_design.md` |
| 17 | Step 4a begun. The user set class probabilities as a must-have (DR-15). Approved the admissible-set code and ran it on the training design: four of 14 configurations admissible (Logistic family). Eight excluded by the task gate; k-NN and Tree excluded by the must-have. Two linear dependencies in the design are not yet identified. | DR-15, DR-16; `Code/dropout/admissible.py`, `Code/dropout/04a_admissible_set.py`, `Code/outputs/dropout/04a_admissible_set.md` |
| 18 | Recorded the step 4a outputs; no test set read. | `Appendix.md` Decision Records |
| 19 | Identified the 11 linear dependencies in the 4a design (nine one-hot redundancies, and two data facts in the training rows: attendance follows course, and International is the complement of the Portuguese-nationality column). No model fitted. | DR-16 note |
| 20 | FRAMEWORK (user): MOD-2 covers logistic regression. Amended ML Guide §9, §12 and §13 (naming of GLMs), the interim core `admissible.py`, and the rule text. Re-ran 4a: two admissible configurations (Logistic + L2, Logistic + poly + L2). DR-16 superseded by DR-17. Nothing committed; `Notes/Davids Changes.md` left unchanged at the user's request. | DR-16, DR-17; `ML Guide.md`; `Code/dropout/admissible.py`; `Code/outputs/dropout/04a_admissible_set.md` |
| 21 | Step 4b begun. Prior ranking on the two admissible configurations: Logistic + L2 (score 0) and Logistic + poly + L2 (score −1); both kept with the baseline. Expectation recorded. Method not yet agreed; no cross-validation run. | DR-18; `Code/dropout/prior.py`, `Code/dropout/04b_prior.py`, `Code/outputs/dropout/04b_prior.md` |
| 22 | Step 4b: the method agreed by the user (DR-18 PRIOR; DR-19 threshold tuned inside each configuration, poly for non-binary inputs). Drafted the `Methods` sub-section `Dropout after year one` in `Project Report.md`. Departure from §16's threshold wording recorded; FRAMEWORK change applied the same day. No cross-validation run. | DR-18, DR-19; `Project Report.md`, Methods |
| 23 | FRAMEWORK (user): §16 decision threshold wording changed to match DR-19 (tuned inside each configuration's inner CV when the selection metric is F2 or another F_β). `ML Guide.md` version note and §16 row updated; interim core unchanged. Not committed. | `ML Guide.md`; DR-19 |
| 24 | Step 4c, round 1. Approved the cross-validation code, ran it on the training rows (about three minutes). First run failed on a type error in the grouping step; fixed without changing the method and re-run. Baseline mean F2 0.0000; Logistic + L2 mean F2 0.8311 (SD 0.0323), a clear margin on every fold. Round 2 may start. No test set read. | DR-20; `Code/dropout/cv.py`, `Code/dropout/06_cv_round1.py`; `Code/outputs/dropout/06_cv_round1.md` |
| 25 | Step 4d, round 2: Logistic + poly + L2 on the same ten folds (background run, about 10 minutes). Mean F2 0.8305 (SD 0.0274); margin over Logistic + L2 −0.0006 (SD 0.0116), none. Prior agreement: agree. No test set read. | DR-21, DR-18 (outcome field); `Code/dropout/07_cv_round2.py`; `Code/outputs/dropout/07_cv_round2.md` |
| 26 | Step 4e, diagnosis pass 1 (DR-22). Observations for Logistic + L2 computed from the CV means: O1 no; O2 not testable (criterion in F2, E_train a misclassification rate); O5 no; O3 no; O4 holds, so DX-5 is the action; its only available step asks about more input variables, which needs the user. The loop stops for the user's answer. Learning curve not yet computed. No test set read. | DR-22; `Code/outputs/dropout/06_cv_round1.md`, `07_cv_round2.md` |
| 27 | Step 4e, pass 2. The user answered: O2 treated as not holding; no more input variables. The only remaining action for O4 is out of scope, so three flags are recorded (bagging and boosting, Chapter 8; neural networks, Chapters 6–7; kernel methods, Chapter 9), none applied. Loop stops under S4. C3 (learning curve) still to be computed for 4f. No test set read. | DR-22, DR-23 |
| 28 | Step 4f. Approved the 4f code and ran it: learning curve (C3 adequate; the validation error is flat from about 50% of the training data); final tuning on all training rows (L2 strength 0.01, F2 threshold 0.20); recommendation Logistic + L2 by §19 (both eligible; the simpler chosen); confidence Low (C1 none). Test set not read. | DR-24, DR-25, DR-26; `Code/dropout/recommend.py`, `Code/dropout/08_recommendation.py`; `Code/outputs/dropout/08_recommendation.md`, `08_learning_curve.csv` |
| 29 | Step 4f-prime: written up before the test set is used. Methods, Dropout after year one: revised to match what was done (plain logistic excluded and why; final tuning on all training data; the tie rule of §19; the learning-curve factor). Results, Dropout after year one: first paragraph with the cross-validation comparison, the recommended configuration and its settings, the selection confidence and its factors, prior agreement, and the flag-everyone reference. Figures proposed to the user before any are drawn. Test set not read. | `Project Report.md`, Methods and Results |
| 30 | Figure 3 (learning curve of Logistic + L2, training and cross-validation data only) drawn after the user chose it at 4f-prime; light and dark. Placed in Results under Dropout after year one. Its y-axis widened once so the 10% error bar is not clipped. | `Code/dropout/fig3_learning_curve.py`; `Code/outputs/dropout/figures/fig3_learning_curve.png`; `Code/outputs/dropout/fig3_learning_curve_summary.csv`; `Project Report.md`, Results |
| 31 | Step 4g: the test set used once, approved at 4f-prime. Refitted Logistic + L2 (L2 strength 0.01, threshold 0.20) on the 3,539 training rows; scored the 885 test rows once. Test F2 0.8350 (recomputed two ways, agreeing); baseline 0.0000; flag-everyone reference 0.7026; uncertainty (fold SD) 0.0323; success criterion met. Test set not to be used again for this sub-task. | DR-27; `Code/dropout/09_final_test.py`; `Code/outputs/dropout/09_final_test.md`, `09_final_test.json`, `09_test_predictions.csv` |
| 32 | Step 4h: Recommendation Report written (13 parts, §25) in the Recommendation section from DR-01 to DR-27. Test result added to Results, after Figure 3. Methods checked: it describes what was done (plain logistic excluded; final tuning; §19 tie rule; learning-curve factor). Abstract updated with the test result. Tag tally in part 13. | Appendix.md, Recommendation; Project Report.md, Results, Abstract |
| 33 | Step 5 begun. Discussion structure agreed as six themes; title to be chosen after the Discussion. Discussion written in Project Report.md (why this configuration; how it predicts; the test result with its flags and errors; use and limits, with the data limits beside the claims they qualify; evaluation limits and open possibilities; prior versus evidence). Final Abstract written, Draft removed. No new analysis; figures from the record only. | Project Report.md, Discussion and Abstract |
| 34 | Title chosen by the user: Predicting first-year dropout in higher education with logistic regression. Title check: "first year" is not established from the source (the two semesters as one year); the Data 2022 paper returned HTTP 403 to the fetch. The user will provide the paper; the wording stays until it is checked. The general reach of the title is bounded by the Discussion. Open. | Project Report.md, title, Abstract, Introduction |

## Code Summary

### `Code/dropout/01_describe_data.py`

- Step 1, describing pass. Reads `Attachments/Student Dropout/data.csv` (never modified). Writes `Code/outputs/dropout/01_describe.md`: file checksum and line endings, the candidate target's counts, every column's type, missing count, distinct values and range, and a numeric summary.
- Run: `cd Code && uv run python dropout/01_describe_data.py`.
- Parameters: the categorical columns (DR-05) are a constant list in the script. No seeds.
- Packages: `pandas` (listed in `Code/pyproject.toml`).

### `Code/dropout/02_split.py`

- Step 2, train/test split. Reads `Attachments/Student Dropout/data.csv` (never modified). Writes `Code/outputs/dropout/02_split.csv` (row_id, split, y) and `Code/outputs/dropout/02_split.md` (counts, seed, checksum). Fits no model.
- Rule: random split, 20% test, stratified by y (Dropout = 1), seed 2026 (DR-10). The test rows are locked until the final evaluation.
- Run: `cd Code && uv run python dropout/02_split.py`.
- Parameters: `SEED = 2026`, `TEST_FRACTION = 0.20`. Packages: `pandas`, `scikit-learn` (listed in `Code/pyproject.toml`).

### `Code/dropout/core.py` (interim core, not reviewed)

- Implements Property 10 (class imbalance) and Property 9 (separability) for this analysis, on the training rows only. Every [I] threshold is a named constant (`IMBALANCE_SHARE = 0.20`, `SEPARABLE_TRAIN_ACCURACY = 1.0`). Holds the list of categorical inputs (DR-05).
- Imported by `03_properties_9_10.py`; not run on its own.
- Parameters: `SEPARABILITY_MAX_ITER = 10000` (convergence budget); seed 2026 passed to the solver.
- Packages: `numpy`, `pandas`, `scikit-learn`.

### `Code/dropout/03_properties_9_10.py`

- Step 3. Reads `Attachments/Student Dropout/data.csv` and `Code/outputs/dropout/02_split.csv`. Uses the training rows only. Writes `Code/outputs/dropout/03_props_9_10.json` and `.md`, with the core's SHA-256.
- Run: `cd Code && uv run python dropout/03_properties_9_10.py`.

### `Code/dropout/fig1_approved_units.py`

- Step 3, Figure 1. Reads `Attachments/Student Dropout/data.csv` and `Code/outputs/dropout/02_split.csv`; plots the training rows only. Writes `Code/outputs/dropout/figures/fig1_approved_units.png` (light), `figures/dark/fig1_approved_units.png` (dark) and `Code/outputs/dropout/fig1_approved_units.csv`.
- Uses `Code/sml_style.py` for the style.
- Run: `cd Code && uv run python dropout/fig1_approved_units.py`. No seed.

### `Code/dropout/fig2_tuition_share.py`

- Step 3, Figure 2. Reads `Attachments/Student Dropout/data.csv` and `Code/outputs/dropout/02_split.csv`; plots the training rows only. Writes `Code/outputs/dropout/figures/fig2_tuition_share.png` (light), `figures/dark/fig2_tuition_share.png` (dark) and `Code/outputs/dropout/fig2_tuition_share.csv`.
- Uses `Code/sml_style.py` for the style.
- Run: `cd Code && uv run python dropout/fig2_tuition_share.py`. No seed.

### `Code/dropout/04_input_design_counts.py`

- Step 3, input design. Counts the levels and encoded columns under the rare-level rule (fewer than 10 training students, DR-13). Training rows only; fits no model. Writes `Code/outputs/dropout/04_input_design.md` and `.csv`.
- Run: `cd Code && uv run python dropout/04_input_design_counts.py`. Parameter: `RARE_MIN = 10`. No seed.

### `Code/dropout/admissible.py` (interim core, not reviewed)

- Step 4a. The admissible-set logic for the 14 structural configurations: the task gate (section 12), must-haves stated by the user, MOD-1 and MOD-2. Returns one record per configuration with its why-not code (EXCL or USER). Fits nothing.
- Imported by `04a_admissible_set.py`. MOD-2 covers Logistic as well (ML Guide §12, amended 10 November 2026; DR-17).

### `Code/dropout/04a_admissible_set.py`

- Step 4a. Builds the training design under DR-13 (rare levels grouped, training rows only), computes its parameter count and rank, and calls the core with the property values and the must-have from DR-15. Writes `Code/outputs/dropout/04a_admissible_set.json` and `.md`.
- Run: `cd Code && uv run python dropout/04a_admissible_set.py`. No seed; the rank check is deterministic.

### `Code/dropout/cv.py` (interim core, not reviewed)

- Step 4c. The nested cross-validation for the dropout analysis (ML Guide section 16, as amended 10 November 2026): outer 10 stratified shuffled folds, seed 2026; inner 5 folds with the grid for lambda (1e-4 to 1e4), the degree (2 or 3, poly only) and the F2 threshold (0.05 to 0.95). Rare levels, one-hot encoding and standardisation are fitted inside each training fold. Powers apply to the 19 non-binary numeric inputs.
- The lambda-to-C mapping (C = 1 / (lambda × n)) is an assumption read from SML eq. 3.50; see the comment in the file.
- Imported by `06_cv_round1.py`; not run on its own.

### `Code/dropout/06_cv_round1.py`

- Step 4c, round 1. Reads the data and the training split, runs the baseline and Logistic + L2, writes `Code/outputs/dropout/06_cv_round1.csv`, `.md` and `.json`.
- Run: `cd Code && uv run python dropout/06_cv_round1.py`. Seed 2026. About three minutes.

### `Code/dropout/07_cv_round2.py`

- Step 4d, round 2. Runs Logistic + poly + L2 with `cv.py` on the same outer folds as round 1 and combines it with the round-1 rows. Computes the margins, C1 and C2. Writes `Code/outputs/dropout/07_cv_round2.csv`, `.md` and `.json`.
- Run: `cd Code && uv run python dropout/07_cv_round2.py`. Seed 2026. About 10 minutes.

### `Code/dropout/recommend.py` (interim core, not reviewed)

- Step 4f. The learning curve for the leading configuration (training fractions 10% to 100% on the outer folds), the C3 check, the final tuning on all training rows (through `cv.inner_search`), and the §19 recommendation with the §17 confidence. Imports `cv.py`.
- Parameters: the fractions (0.1 to 1.0), seed 2026 (`cv.SEED`).

### `Code/dropout/08_recommendation.py`

- Step 4f. Reads the training rows and `07_cv_round2.csv`. Writes `Code/outputs/dropout/08_learning_curve.csv`, `08_recommendation.md` and `.json`.
- Run: `cd Code && uv run python dropout/08_recommendation.py`. About two minutes.

### `Code/dropout/fig3_learning_curve.py`

- Step 4f, Figure 3. Reads `Code/outputs/dropout/08_learning_curve.csv` (training and cross-validation data only). Writes the light and dark figures and `fig3_learning_curve_summary.csv`. Uses `Code/sml_style.py`.
- Run: `cd Code && uv run python dropout/fig3_learning_curve.py`. No seed.

### `Code/dropout/09_final_test.py`

- Step 4g, the single test evaluation. Reads the settings from `08_recommendation.json` and the test rows (only here). Refits Logistic + L2 on the training rows, scores the test rows once, computes the baseline, the flag-everyone reference, the uncertainty (fold SD from `07_cv_round2.csv`), and the F2 by a second route (confusion counts). Writes `09_final_test.json`, `09_final_test.md` and `09_test_predictions.csv`.
- Run: `cd Code && uv run python dropout/09_final_test.py`. Do not re-run after the result is recorded: the test set has been used once for this sub-task.


## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). *Machine Learning – A First Course for Engineers and Scientists*, 2nd edition, online draft of 1 September 2026. [https://smlbook.org/](https://smlbook.org/). Details taken from `ML Guide.md`. Not yet checked against the title page on smlbook.org; the local copy in `Attachments/smlbook/` is not in the workspace.
- Realinho, V., Vieira Martins, M., Machado, J. and Baptista, L. (2021). Predict Students' Dropout and Academic Success [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5MC89](https://doi.org/10.24432/C5MC89). Checked on the UCI dataset page and its metadata on 10 November 2026.
