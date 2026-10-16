# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

*Step 1, closed 16 October 2026. Provenance and coverage describe the source files (`Code/outputs/sepsis/01_describe.json`). The column descriptions cover only the columns the analysis uses; the seven dropped columns are named, with the reason, under* Step 1 decisions*. The derived tables the later steps read are described there too (`Code/outputs/sepsis/03_build_table.json`).*

**Provenance.**
- **Files:** `Attachments/sepsis-physionet-2019/`, the training data of *Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019*, version 1.0.0 (5 August 2019). There are 40,336 pipe-separated `.psv` files, one per patient: 20,336 in `training_setA/` and 20,000 in `training_setB/`. Never modified.
- **Downloaded:** 15 October 2026, by the agent at the user's request. The patient files came from PhysioNet's open-data mirror on AWS, because the physionet.org directory listings stop early. `LICENSE.txt` came from physionet.org. Full details are in `Attachments/SOURCE.md`.
- **Checksums:** PhysioNet publishes none for the training files, so we wrote a per-file SHA-256 list for each set. List fingerprints: set A `ef8e0184be4b5bd28b7e0a1642fdcd9c8b04cf10b5dd4bd666156a71ab05697d`, set B `ca9da41aa7154b5b02f4818de98fc157c03599a475abca5f63bffddacff96ca4`. The describing script re-checked every file against these lists: 0 mismatches, none missing, none extra.
- **Licence:** `LICENSE.txt` says ODbL; the dataset page says CC BY 4.0. We follow ODbL, so the data and any patient-level derived file stay out of git. Only aggregates are written to `Code/outputs/sepsis/`.
- **Why this data:** the user chose it. A Kaggle copy was tried first and replaced because it was truncated (`Attachments/SOURCE.md`).
- **Who the patients are** (Reyna et al., 2020, Methods):
  - ICU patients. Set A is from Beth Israel Deaconess Medical Center and set B from Emory University Hospital.
  - Collected "over the past decade"; no years are given.
  - Patients with fewer than 8 hourly windows in the ICU were not included, nor were patients whose sepsis onset was less than 4 hours after ICU admission.
  - Records stop at ICU discharge, and stays longer than two weeks are cut to two weeks.
  - Measurements are summarised into hourly bins, for example the median heart rate within the hour.
  - "Missing and erroneous data were intentionally preserved as part of the Challenge."

**Best available form: checked.**
- Version 1.0.0 is the only version listed on the PhysioNet page.
- The Challenge also had hidden test sets: 24,819 patients from hospital systems A, B and a third, unidentified system C. The paper says they "were sequestered", and the page offers no download for them. No public release was found.
- The 40,336 training patients are therefore the fullest public form, and the PhysioNet copy is complete where the Kaggle copy was not.

**Shape and coverage.**
- 1,552,210 rows: 790,215 in set A and 761,995 in set B. Each row is one hour of one patient's ICU stay. 41 columns, identical header in every file.
- **Stay length:** 8 to 336 hours, median 38. The 8-hour minimum and 336-hour (two-week) maximum match the inclusion rules above.
- **ICULOS (hours since ICU admission):** increases by exactly 1 from row to row within every patient, with no gaps. In 8,793 patients the first row is not hour 1: 7,497 in set A, where the first row can be as late as hour 304, and 1,296 in set B, where it is at most hour 26.
- **Constant within each patient:** `Age`, `Gender` and `HospAdmTime` never change during a stay.
- **Duplicates:** 0 duplicate rows within a patient.
- **Empty rows:** 128,039 rows (8.2 %) have no vital sign and no lab value, only the demographic and time columns and the label.

**Columns used.** Units are as documented on the PhysioNet page. The 27 clinical columns are measurements summarised to one value per hour; none is a model output. Figures are from the source files, before rows were set aside and before cleaning. "Present" is the share of hourly rows with a value; "ever" is the share of patients with at least one value during their stay.

| Column | Group | Documented unit | Rows present % | Patients ever % (A / B) | Min | 1st pct | Median | 99th pct | Max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HR` | vital | beats per minute | 90.1 | 100.0 / 100.0 | 20 | 50 | 83.5 | 130 | 280 |
| `O2Sat` | vital | % | 86.9 | 99.9 / 100.0 | 20 | 89 | 98 | 100 | 100 |
| `Temp` | vital | °C | 33.8 | 98.8 / 99.8 | 20.9 | 35.1 | 37 | 38.8 | 50 |
| `SBP` | vital | mm Hg | 85.4 | 98.7 / 99.9 | 20 | 80 | 121 | 186 | 300 |
| `MAP` | vital | mm Hg | 87.6 | 100.0 / 99.5 | 20 | 52 | 80 | 128 | 300 |
| `DBP` | vital | mm Hg | 68.7 | 63.7 / 99.9 | 20 | 38 | 62 | 103 | 300 |
| `Resp` | vital | breaths per minute | 84.7 | 99.9 / 99.8 | 1 | 9 | 18 | 34 | 100 |
| `FiO2` | lab | % (stored as a fraction) | 8.3 | 58.9 / 29.1 | −50 | 0.21 | 0.5 | 1 | 4000 |
| `pH` | lab | none | 6.9 | 64.8 / 28.8 | 6.62 | 7.15 | 7.38 | 7.53 | 7.93 |
| `PaCO2` | lab | mm Hg | 5.6 | 61.9 / 28.9 | 10 | 24 | 40 | 76 | 100 |
| `SaO2` | lab | % | 3.5 | 39.2 / 25.6 | 23 | 53 | 97 | 99.8 | 100 |
| `AST` | lab | IU/L | 1.6 | 29.0 / 42.3 | 3 | 10 | 41 | 5003 | 9961 |
| `BUN` | lab | mg/dL | 6.9 | 97.9 / 92.0 | 1 | 4 | 17 | 103 | 268 |
| `Alkalinephos` | lab | IU/L | 1.6 | 28.0 / 42.4 | 7 | 25 | 74 | 555 | 3833 |
| `Calcium` | lab | mg/dL | 5.9 | 81.4 / 92.3 | 1 | 1.07 | 8.3 | 10.5 | 27.9 |
| `Creatinine` | lab | mg/dL | 6.1 | 97.7 / 92.1 | 0.1 | 0.37 | 0.94 | 9.7 | 46.6 |
| `Glucose` | lab | mg/dL | 17.1 | 98.0 / 94.1 | 10 | 65 | 127 | 326 | 988 |
| `Lactate` | lab | mg/dL | 2.7 | 38.0 / 23.8 | 0.2 | 0.6 | 1.8 | 14.2 | 31 |
| `Magnesium` | lab | mmol/dL | 6.3 | 93.2 / 82.3 | 0.2 | 1.3 | 2 | 3.3 | 9.8 |
| `Phosphate` | lab | mg/dL | 4.0 | 82.1 / 58.2 | 0.2 | 1.1 | 3.3 | 8.5 | 18.8 |
| `Potassium` | lab | mmol/L | 9.3 | 97.9 / 92.8 | 1 | 2.9 | 4.1 | 6.1 | 27.5 |
| `Bilirubin_total` | lab | mg/dL | 1.5 | 28.4 / 42.4 | 0.1 | 0.2 | 0.9 | 25.1 | 49.6 |
| `Hct` | lab | % | 8.9 | 98.2 / 90.2 | 5.5 | 19.5 | 30.3 | 45.1 | 71.7 |
| `Hgb` | lab | g/dL | 7.4 | 97.5 / 90.3 | 2.2 | 6.5 | 10.3 | 15.5 | 32 |
| `PTT` | lab | seconds | 2.9 | 77.9 / 22.0 | 12.5 | 21 | 32.4 | 150 | 250 |
| `WBC` | lab | 10³/µL | 6.4 | 96.9 / 90.0 | 0.1 | 2.5 | 10.3 | 31.2 | 440 |
| `Platelets` | lab | 10³/µL | 5.9 | 97.1 / 90.0 | 1 | 34 | 181 | 542 | 2322 |
| `Age` | demographic | years; 100 means 90 or older | 100 | 100 / 100 | 14 | 21 | 64 | 89 | 100 |
| `Gender` | demographic | 0 female, 1 male | 100 | 100 / 100 | 0 | | | | 1 |
| `Unit1` | administrative | MICU identifier | 60.6 | 53.2 / 69.5 | 0 | | | | 1 |
| `Unit2` | administrative | SICU identifier | 60.6 | 53.2 / 69.5 | 0 | | | | 1 |
| `HospAdmTime` | administrative | hours from hospital admission to ICU admission | 100 | 100 / 100 | −5367 | −630 | −6.0 | 0 | 23.99 |
| `ICULOS` | time index (not an input) | hours since ICU admission | 100 | 100 / 100 | 1 | 1 | 21 | 166 | 336 |
| `SepsisLabel` | outcome | 0 or 1 | 100 | 100 / 100 | 0 | | | | 1 |

**Patients.** In the source files: 17,770 female and 22,566 male (`Gender` 0 / 1), median age 63.1 at admission.
- **`Age` = 100:** 392 patients, all in set B (389 of them keep at least one hour). The PhysioNet page documents 100 as meaning "90 or above", so this is most likely an anonymisation cap. It means that ages above 89 are not distinguished in set B, and that set A, which has none coded 100, reports exact ages.
- **Young patients:** the youngest is 14 (2 patients), and 21 patients with at least one kept hour are under 18. This is in a population described as adult ICU patients.

**Oddities found.** What was done about each is under *Step 1 decisions*.
- **`FiO2` is a fraction, not a percentage.** It is documented as %, but the 1st percentile is 0.21, the median 0.5 and the 99th percentile 1. It also has impossible extremes: −50 and 4000. These were cleaned.
- **Two units disagree with the values.**
  - `Magnesium` is documented as mmol/dL, but its median of 2 (99th percentile 3.3) is in the usual range for mg/dL.
  - `Lactate` is documented as mg/dL, but its median of 1.8 (99th percentile 14.2) is in the usual range for mmol/L.
  - Both are noted from typical clinical ranges, not from any documentation.
- **`Calcium` has a low cluster.** Its 1st percentile is 1.07 mg/dL against a median of 8.3, which is consistent with some values being on a different scale (for example ionised calcium in mmol/L). This was not checked further.
- **Limits that look like clipping.**
  - `HR`, `O2Sat`, `SBP`, `MAP` and `DBP` all have a minimum of exactly 20.
  - `SBP`, `MAP` and `DBP` all have a maximum of exactly 300.
  - `Resp` and `PaCO2` have a maximum of exactly 100.
- **Impossible values:** `Temp` 50 °C, `Potassium` 27.5 mmol/L and `Hgb` 32 g/dL. These were cleaned.
- **`HospAdmTime` is sometimes positive**, up to 23.99 hours. Read literally, those patients reached the ICU before being admitted to hospital. This applies to 255 patients, covering 8,483 kept hours.
- **`Unit1` and `Unit2` are exclusive and often missing.**
  - Where present they always sum to 1: no patient is marked as both MICU and SICU.
  - They are missing for the whole stay in 15,617 patients (9,522 in A, 6,095 in B).
- **Sets A and B record different things.** Five columns present in only one hospital were dropped (*Step 1 decisions*). Among the columns kept:
  - `DBP` is recorded for 64 % of set A patients and nearly all of set B.
  - `PTT` is recorded for 78 % of set A patients and 22 % of set B. `pH`, `FiO2` and `PaCO2` are recorded for about 60 % of A and 29 % of B.
  - Ages of 90 or above are coded 100 only in set B.
  - Sepsis is more common in A (8.8 % of patients) than in B (5.7 %).
- **Most of the table is empty.** Most lab columns have values in under 10 % of hourly rows, because labs are drawn a few times a day. `Temp` is present in 34 % of rows.

**Machine learning checks.** Written in the describing pass. The figures after the decisions are added below them.
- **Candidate target: `SepsisLabel`.** It is defined per hour, and the labels are constructed rather than recorded at the bedside (PhysioNet page, Challenge 2019):
  - Sepsis-3 criteria are used. The onset time `t_sepsis` is the earlier of `t_suspicion` and `t_SOFA`, where `t_SOFA` is a ≥ 2-point rise in SOFA score within 24 hours.
  - `t_suspicion` comes from antibiotic and blood-culture orders, which are not in the files.
  - For septic patients, `SepsisLabel` = 1 from `t_sepsis` − 6 hours onwards, so a 1 marks the six hours before onset as well as after.
- **The label is built partly from the inputs.** The SOFA score is computed from organ-function measures, several of which are columns here: `Platelets`, `Bilirubin_total`, `Creatinine`, `MAP` and `FiO2`. The respiratory component also needs PaO2, which is not in the files. A row-level label therefore partly encodes some input values (see the leakage note below).
- **Label structure in the files:**
  - 2,932 of 40,336 patients (7.27 %) ever have `SepsisLabel` = 1: 1,790 in A (8.8 %) and 1,142 in B (5.7 %).
  - At row level, 27,916 of 1,552,210 hours (1.80 %) are labelled 1.
  - In every septic patient the label switches from 0 to 1 once and never goes back.
  - Every septic patient has at most 10 rows labelled 1 (median 10). So every septic patient's record ends no more than 9 hours after the label switches on, whereas non-septic records run to discharge or two weeks.
  - In 426 septic patients the label is already 1 in the first row.
  - Among septic patients, the first labelled hour is at `ICULOS` median 29 (maximum 331).
- **Output type it suggests:** binary (P1, to be confirmed in step 2). Whether the unit of prediction is the hour (row) or the patient is a step 2 question.
- **Class counts:** in the source files, per row, 1,524,294 labelled 0 and 27,916 labelled 1; per patient, 37,404 never septic and 2,932 septic.
  - *After the step 1 decisions:* 39,910 patients have at least one hour, and 2,506 of them later become septic (1,587 in A, 919 in B). Every kept hour precedes the label's onset.
- **Inputs:** 40 columns besides the target in the source.
  - *After the step 1 decisions:* 32 inputs (P3) — 27 clinical columns, `Age`, `Gender`, `Unit1`, `Unit2` and `HospAdmTime`. `ICULOS` is not an input.
  - Three are categorical (`Gender`, `Unit1`, `Unit2`), a share of 3/32 = 9.4 % (P4). All three are already 0/1, so one-hot encoding adds no columns, unless the missing unit is given its own category, in which case P3 = 33.
  - These counts are per hour. Summaries over time windows, decided in step 3, will change them.
- **Columns that could leak the target.** Written in the describing pass; what was decided is under *Step 1 decisions* (Target and leakage).
  - *Record length and `ICULOS`.* A septic record is cut at most 9 hours after its label switches on, so how long a record runs, and where an hour falls within it, depends on the outcome. Any input built from the length of a stay, or from hours remaining, carries the label.
  - *The SOFA components.* `Platelets`, `Bilirubin_total`, `Creatinine`, `MAP` and `FiO2` enter the definition of `t_SOFA`. Their values at and after onset are partly what makes the label 1.
  - *Rows after onset.* For a septic patient, rows from `t_sepsis` onwards describe a patient who already meets the sepsis definition. The label there marks a condition already present, not one about to start.
- **Grouping and order (bearing on ADM-3):** rows are grouped by patient (one file each) and ordered in time by `ICULOS`. Patients are split between two hospitals (sets A and B).
- **The user's experience with machine learning:** intermediate (stated 15 October 2026).

**Step 1 decisions** (15–16 October 2026, by the user). The counts were first made without changing anything (`Code/outputs/sepsis/02_scope_counts.json`). The decisions were then applied to derived tables (`Code/outputs/sepsis/03_build_table.json`). Both give the same counts.

| Decision | What was decided, and why | What it costs |
| --- | --- | --- |
| **Provenance** | The PhysioNet 1.0.0 training data, sets A and B, all 40,336 patient files, checked against our SHA-256 lists. It is the fullest public form; the hidden test sets were never released. | None. |
| **Units** | As documented on the PhysioNet page. Exception: `FiO2` is stored as a fraction, not the documented %. Of the `FiO2` values in kept rows, 112,936 are in [0.21, 1), 11,024 are exactly 1, 24 lie between 1 and 21, and none lies between 21 and 100, so no value is on a percentage scale. | — |
| **Scope: hospitals** | Both sets are used. User: "use both sets, keeping only variables recorded in both." | The two hospitals differ in recording and in sepsis rate (DR-03). |
| **Scope: variables** | One rule: drop any column that fewer than 10 % `[I]` of patients in either hospital ever have. Seven columns are dropped (% of patients with a value, A / B): `EtCO2` (0.0 / 16.1), `HCO3` (97.4 / 2.1), `BaseExcess` (62.2 / 2.8), `Chloride` (97.3 / 8.1), `TroponinI` (2.4 / 32.8), `Bilirubin_direct` (2.9 / 7.4), `Fibrinogen` (12.6 / 9.7). The first five are present in one hospital and essentially absent in the other; the last two are rare in both. Kept although unequal between hospitals: `PTT`, `pH`, `FiO2`, `PaCO2`, `DBP`. User, 16 October: "drop all seven … using one rule". | 7 of 34 clinical columns. A model cannot use end-tidal CO2, bicarbonate, base excess, chloride, troponin, direct bilirubin or fibrinogen, including in the hospital where they are well recorded. |
| **Scope: rows** | Every row from the hour `SepsisLabel` first becomes 1 is set aside (leakage, below). | 27,916 rows set aside, leaving 1,524,294. **426 septic patients lose every row**, because their label is already 1 in the first row, leaving 39,910 patients. 2,506 of 2,932 septic patients keep at least one row (median 37), 1,587 in A and 919 in B. Every remaining row has `SepsisLabel` = 0, so the target has to be defined at patient level, or from future hours, in step 2. |
| **Missing data** | Empty values are kept; nothing is filled in. User: "How to summarise them is input design, decided in step 3. Any filling-in must happen inside the cross-validation folds." | The many empty values (most lab columns under 10 % of rows) stay a property of the data that every model must handle. |
| **Panel structure** | Patients are not required to be observed over the same hours. Stays run from 8 to 336 hours, and 8,793 patients' records start after ICU hour 1. All patients with at least one kept hour stay in the table. Any minimum number of hours before a prediction is made belongs to the step 2 target definition, together with the time handling left open in DR-02. | Patients contribute very different numbers of hours (kept median 37 for patients who later become septic). |
| **Cleaning** | Only clearly impossible values are set to missing, in the derived table only, never the source files. One written rule per column `[I]`, counted on kept rows (A / B):<br>· `FiO2` outside [0.21, 1.0] → **385** (318 / 67; 299 patients). These are 360 values below 0.21, including −50; 24 between 1.2 and 10; and the 4000.<br>· `Temp` outside [25, 45] °C → **6** (4 / 2): 20.9, 21.0, 23.0, 23.6, 50.0.<br>· `Potassium` above 15 mmol/L → **2** (1 / 1): 15.8, 27.5.<br>· `Hgb` above 25 g/dL → **3** (1 / 2): 26.6, 30.0, 32.0.<br>Considered and not chosen: `Temp` outside [30, 43] (18 values) and `Potassium` above 10 (15 values), because those cuts also remove extreme but possible values. User, 16 October: "only clearly impossible values are set to missing … Values that are extreme but possible are kept and noted." | 396 values become missing. Extreme but possible values stay, for example `Temp` 26.6–29.9 °C and `Potassium` 10.2–13.0. |
| **Accepted as-is** | Kept unchanged and recorded as limitations:<br>· the suspected unit problems in `Magnesium` (values fit mg/dL, not the documented mmol/dL), `Lactate` (fit mmol/L, not mg/dL) and `Calcium` (a low cluster near 1, possibly ionised calcium in mmol/L);<br>· the vitals clipped at exactly 20, 300 and 100;<br>· positive `HospAdmTime` (255 patients, 8,483 kept hours);<br>· patients under 18 (21 patients, youngest 14) in an adult ICU population;<br>· `Age` = 100 in 392 patients, all in set B, most likely an anonymisation cap for "90 or above".<br>User, 15–16 October: "Keep the suspected unit problems (Magnesium, Lactate) and the clipped vitals as they are"; Calcium "like Magnesium and Lactate"; "Keep as-is and record". | Limitations: these columns may mix scales or be cut off, and no model can tell. Ages above 89 are indistinguishable in set B but exact in set A. |
| **Admissibility** | ADM-1 yes (DR-01). ADM-3: patient is the group unit; hospital is a second grouping; how the time order is handled is decided in step 2 (DR-02). ADM-4: yes for adult ICU patients at these two hospitals, unsure beyond (DR-03). | Limitations recorded in DR-01 and DR-03. |
| **Target and leakage** | Target: `SepsisLabel` (DR-01). Limitations: it is built by rule (Sepsis-3), partly from inputs, and shifted 6 h before onset. The exact target is decided in step 2. Set aside as inputs: `ICULOS`; the record length; every row from the hour `SepsisLabel` first becomes 1; any summary over the whole stay. `HospAdmTime` stays. User: "set aside ICULOS, the record length, every row from the hour SepsisLabel first becomes 1, and any summary over the whole stay. HospAdmTime may stay." | Removes the hour-in-stay as an input. `ICULOS` is kept only to order each stay's rows and to define time windows, never as an input. User, 16 October: "use it only to order each stay's rows and to define time windows, never as an input." |
| **Derived tables** | Built by `Code/sepsis_03_build_table.py`, outside git (`Code/outputs/sepsis/private/`, listed in `.gitignore`).<br>· `hours.csv.gz`: one row per kept hour; 1,524,294 rows (A 773,079, B 751,215) × 35 columns (`patient`, `set`, 32 inputs and `ICULOS`). `SepsisLabel` is not included, because every kept hour is 0. SHA-256 `f86128f3be3c87bf84aee2abf5f7c8852af7f5227c495133ea4b7dba8dd2b86e`.<br>· `patients.csv.gz`: one row per patient, all 40,336, with `set`, `septic` (ever `SepsisLabel` = 1), `label_onset_iculos` (the `ICULOS` at which `SepsisLabel` first becomes 1, i.e. `t_sepsis` − 6 h) and `hours_kept`. It is the label source for step 2, not an input. SHA-256 `0d8ab8d4a46df453298d725f3a6b61855dd355cc9b10c4685715cffd144d1535`.<br>Both are gzip files with a fixed timestamp, so a re-run gives the same checksums. | Removing label-1 rows would otherwise lose which patients become septic; `patients.csv.gz` keeps it. `hours_kept` is the kept record length and must not become an input. |
| **Experience level** | Intermediate. | — |

## Problem Definition

*Written in step 2, before anything is trained. Three parts. `Discussion`: how the problem was arrived at, what was ruled out, and whether it is a prediction problem. `Problem`: what is predicted, from what, the output type, the agreed metric, the success criterion, the baseline and the achievable level, the must-have requirements, and any expectations the user states about the relationship (quoted). `Sub-tasks`: the separately answerable parts. Ends with the train/test split, its seed, and the statement that the test set is locked.*

## Analysis

*The workings, one sub-heading per sub-task, added as steps 3 and 4 proceed: exploration of the training data, cross-validation tables, learning curves, diagnostics, error analysis, checks that changed nothing, and anything computed but not reported.*

## Decision Records

### DR-01 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-15
- **Question:** Is there a recorded output y for the rows to be learned from (ADM-1)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `SepsisLabel` | present in all 1,552,210 hourly rows: 1,524,294 × 0, 27,916 × 1. 2,932 of 40,336 patients ever 1. Never returns from 1 to 0. | M | `Code/outputs/sepsis/01_describe.json` |
| How the label is produced | Sepsis-3: `t_sepsis` = min(`t_suspicion`, `t_SOFA`) when `t_SOFA` falls within 24 h before to 12 h after `t_suspicion`. `t_suspicion` comes from antibiotic and blood-culture orders (not in the files); `t_SOFA` is a ≥ 2-point SOFA rise, partly computed from `Platelets`, `Bilirubin_total`, `Creatinine`, `MAP`, `FiO2`. Label = 1 from `t_sepsis` − 6 h. | M | PhysioNet Challenge 2019 page (Reyna et al., 2019) |
| User's answer | "Yes, SepsisLabel is the output to learn from. Record as limitations that it is rule-based (Sepsis-3, partly computed from the inputs) and shifted 6 hours earlier. The exact patient-level target is decided in step 2." | M | user, 15 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-1 | yes | [B p.15] | supervised problem; continue |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** continue with `SepsisLabel` · stop
- **Expectation:** n/a
- **Decision:** `SepsisLabel` is the recorded output, so the work continues. Two limitations are recorded: the label is constructed by rule (Sepsis-3), partly from columns that are also inputs, and it is shifted 6 hours earlier than onset. The exact target, per hour or per patient, is fixed in step 2.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/sepsis_01_describe_data.py`, `Code/outputs/sepsis/01_describe.md`

### DR-02 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-15
- **Question:** Do several rows belong to the same unit, or are rows ordered in time (ADM-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Group column | patient (one `.psv` file per patient; 40,336 patients; 8–336 rows each, median 38) | M | `Code/outputs/sepsis/01_describe.json` |
| Second grouping | hospital: set A (Beth Israel Deaconess, 20,336 patients) and set B (Emory, 20,000 patients) | M | Reyna et al. (2020), Methods |
| Time order | rows ordered by `ICULOS` (hours since ICU admission), consecutive within every patient | M | `Code/outputs/sepsis/01_describe.json` (`iculos_with_gaps`: 0) |
| User's answer | "Yes, patient is the group unit; no patient may appear in both training and test data. Also record hospital (set A or B) as a group; whether to train on one hospital and test on the other is decided in step 2." | M | user, 15 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-3, group | group column = patient | [B p.329] | splits and cross-validation folds are made by patient |
| ADM-3, group | hospital (A/B) recorded as a second grouping | [B p.329] | whether the split is also by hospital is decided in step 2 |
| ADM-3, time | rows ordered in time within each patient | [B pp.16, 38–39] | the rule offers an autoregressive (window) reformulation if the user wants it, otherwise a flag that time-series modelling is out of scope. Open: decided in step 2 together with the patient-level target |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** random split by row · split by patient · split by patient and hospital · autoregressive reformulation · flag time-series modelling
- **Expectation:** n/a
- **Decision:** Patient is the group unit, and no patient appears in both training and test data or across cross-validation folds. Hospital (set A or B) is recorded as a second grouping; whether to train on one and test on the other is decided in step 2. How the time order within a stay is handled is also decided in step 2.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/sepsis/01_describe.json`

### DR-03 · ADM · step 1

- **Sub-task:** all
- **Date:** 2026-10-15
- **Question:** Will the cases the model is used on look like the data we have (ADM-4)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Population | adult ICU patients at two US hospitals (Beth Israel Deaconess, Emory). Fewer than 8 ICU hours or onset < 4 h after ICU admission excluded; stays cut at 2 weeks | M | Reyna et al. (2020), Methods |
| Differences between A and B | `EtCO2` never recorded in A; `HCO3`, `Chloride`, `BaseExcess` rare in B; `TroponinI` rare in A; `DBP` 64 % vs 100 % of patients; age ≥ 90 coded 100 only in B; sepsis 8.8 % (A) vs 5.7 % (B) | M | `Code/outputs/sepsis/01_describe.json` |
| User's answer | "Yes for adult ICU patients at these two US hospitals; unsure beyond them. Record as a limitation, noting the differences between A and B." | M | user, 15 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-4 | yes within the two hospitals; unsure beyond them | [B pp.328–329] | continue. Because of the "unsure", which data the validation and test sets come from is agreed with the user before splitting (step 2, with the hospital question in DR-02) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** yes · no · unsure
- **Expectation:** n/a
- **Decision:** The model's intended use is adult ICU patients at these two hospitals, so the work continues. A recorded limitation: whether it applies to other hospitals is unknown, and the two hospitals here already differ in what they record and in how common sepsis is.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/sepsis/01_describe.json`

## Recommendation

*Written at the end of step 4, one sub-heading per sub-task, after its single test-set evaluation: the thirteen-part Recommendation Report of `ML Guide.md` §25, assembled from the Decision Records. Nothing in it is new.*

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1. Created the analysis folder `Demonstration/Sepsis/` from the templates. The user chose the PhysioNet 2019 sepsis training data and stated intermediate ML experience. | `Demonstration/Sepsis/Report.md`, `Appendix.md` |
| 2 | Step 1, describing pass. Re-checked all 40,336 files against the SHA-256 lists (0 mismatches). Described shape, stays, label structure, every column's completeness and range, and the differences between sets A and B. Units and the label definition come from the PhysioNet page; hospitals, inclusion rules and binning from Reyna et al. (2020). No decisions taken. | `Code/outputs/sepsis/01_describe.json`, `01_describe.md` |
| 3 | Step 1, decisions. The user answered ADM-1, ADM-3 and ADM-4 (DR-01, DR-02, DR-03) and decided scope, missing data, cleaning and leakage. Counted, without applying anything: the rows and patients left after setting aside rows from label onset (426 septic patients lose every row), the `FiO2` unit check (fraction scale), and the values each candidate cleaning rule would change. Proposed a variable drop list (7 columns) and cleaning thresholds for the user's approval. | `Code/outputs/sepsis/02_scope_counts.json`, `02_scope_counts.md` |
| 4 | Step 1, decisions applied. The user approved dropping all seven columns under one rule (fewer than 10 % of patients in either hospital), and cleaning only clearly impossible values (`FiO2` outside [0.21, 1.0], `Temp` outside 25–45 °C, `Potassium` > 15, `Hgb` > 25). Not chosen: `Temp` 30–43 and `Potassium` > 10, which would also remove possible values. Calcium's low cluster, positive `HospAdmTime`, patients under 18 and `Age` = 100 are kept as-is and recorded. `ICULOS` is used only for ordering and time windows. Built the derived tables: 1,524,294 hours × 32 inputs; 39,910 patients with hours, 2,506 of whom later become septic. Cleaning changed 385 + 6 + 2 + 3 values, the same as row 3's counts. The positive-`HospAdmTime` count given to the user in conversation (64 rows) had not been computed and was wrong; the computed figure is 8,483 kept hours in 255 patients. Data Summary updated, and the dropped columns' descriptions removed. | `Code/outputs/sepsis/03_build_table.json`, `03_build_table.md`; `Code/outputs/sepsis/private/` (not in git) |
| 5 | Step 1 closed (16 October 2026). | — |

## Code Summary

Scripts for this analysis are prefixed `sepsis_` and write to `Code/outputs/sepsis/`, so they do not collide with the Heart Failure analysis's files. Outputs hold aggregates only; no patient-level rows are written, because the data is under ODbL and kept out of git.

| File | What it does | Reads | Writes | Run |
| --- | --- | --- | --- | --- |
| `Code/sepsis_01_describe_data.py` | Step 1 describing pass. Verifies every patient file against the SHA-256 lists, then describes rows, patients, stays, `ICULOS` continuity, label structure, per-column completeness (per row and per patient, overall and by set) and ranges, demographics, and the input count. No random steps, no seed. Takes about 45 minutes, mostly in per-patient `groupby().apply`. | `Attachments/sepsis-physionet-2019/training_setA/`, `training_setB/`, `SHA256SUMS_training_setA.txt`, `SHA256SUMS_training_setB.txt` | `Code/outputs/sepsis/01_describe.json`, `01_describe.md` | `cd Code && uv run python sepsis_01_describe_data.py` |
| `Code/sepsis_02_scope_counts.py` | Step 1 decisions, counts only; changes nothing and writes no derived table. Counts the rows and patients left once every row from `SepsisLabel` onset is set aside, `FiO2` values by band (unit check), and the values each candidate cleaning rule (`CANDIDATES`, `[I]` thresholds) would set to missing in the kept rows. No random steps, no seed. A few minutes when the machine stays awake. | same patient files | `Code/outputs/sepsis/02_scope_counts.json`, `02_scope_counts.md` | `cd Code && uv run python sepsis_02_scope_counts.py` |
| `Code/sepsis_03_build_table.py` | Applies the step 1 decisions to derived tables. Drops columns that fewer than `DROP_THRESHOLD_PCT` = 10 % `[I]` of patients in either hospital ever have, sets aside every row from `SepsisLabel` onset, and sets the `CLEAN_RULES` values `[I]` to missing. Fills nothing in. Writes gzip files with `mtime=0`, so checksums are reproducible. `NOT_INPUTS` = `ICULOS`. No random steps, no seed. About 20 minutes. | same patient files | `Code/outputs/sepsis/private/hours.csv.gz`, `patients.csv.gz` (not in git); `Code/outputs/sepsis/03_build_table.json`, `03_build_table.md` | `cd Code && uv run python sepsis_03_build_table.py` |

Uses pandas and numpy from the existing environment; no new dependency.

## References

- Reyna, M., Josef, C., Jeter, R., Shashikumar, S., Moody, B., Westover, M. B., Sharma, A., Nemati, S. and Clifford, G. D. (2019). *Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019* (version 1.0.0) [Dataset]. PhysioNet. [https://doi.org/10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857). Units and the `SepsisLabel` definition are taken from this page (read 15 October 2026).
- Reyna, M. A., Josef, C. S., Jeter, R., Shashikumar, S. P., Westover, M. B., Nemati, S., Clifford, G. D. and Sharma, A. (2020). Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019. *Critical Care Medicine*, 48(2), 210–217. [https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/). Hospitals, inclusion rules, hourly binning and the hidden test sets are taken from its Methods (read 15 October 2026).
