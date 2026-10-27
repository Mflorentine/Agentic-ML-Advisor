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
  - *Added 18 October 2026, after step 3 (Figure 3):* `PTT` stops at exactly 150 s in hospital A and at 250 s in hospital B. Among the training patients' last values in ICU hours 1–6: in A, 78 of 6,150 are exactly 150 and none is higher; in B, 4 of 1,947 are exactly 250, and 37 are above 150 (`Code/outputs/sepsis/11_calcium_ptt_counts.json`).
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
| **Grouping and time order** | Patients are not required to be observed over the same hours. Stays run from 8 to 336 hours, and 8,793 patients' records start after ICU hour 1. All patients with at least one kept hour stay in the table. Any minimum number of hours before a prediction is made belongs to the step 2 target definition, together with the time handling left open in DR-02. | Patients contribute very different numbers of hours (kept median 37 for patients who later become septic). |
| **Cleaning** | Only clearly impossible values are set to missing, in the derived table only, never the source files. One written rule per column `[I]`, counted on kept rows (A / B):<br>· `FiO2` outside [0.21, 1.0] → **385** (318 / 67; 299 patients). These are 360 values below 0.21, including −50; 24 between 1.2 and 10; and the 4000.<br>· `Temp` outside [25, 45] °C → **6** (4 / 2): 20.9, 21.0, 23.0, 23.6, 50.0.<br>· `Potassium` above 15 mmol/L → **2** (1 / 1): 15.8, 27.5.<br>· `Hgb` above 25 g/dL → **3** (1 / 2): 26.6, 30.0, 32.0.<br>· *added 27 October 2026, after step 3:* `Calcium` below 2.0 mg/dL → **9,464** (1 / 9,463; 3,835 patients). Below any plausible total calcium in mg/dL, and below the gap in the data between 2 and 3.5 (Analysis Log rows 16–17). User: "below 2.0 mg/dL only", chosen from four options (row 21). Among training patients, those with a last `Calcium` value fall from 12,386 to 10,967.<br>Considered and not chosen: `Temp` outside [30, 43] (18 values) and `Potassium` above 10 (15 values), because those cuts also remove extreme but possible values; `Calcium` also in B's peak at 4.0–5.25 mg/dL (271 training patients by last value), because those values may be plausible on another scale. User, 16 October: "only clearly impossible values are set to missing … Values that are extreme but possible are kept and noted." | 396 values become missing; 9,860 with the `Calcium` rule (27 October). Extreme but possible values stay, for example `Temp` 26.6–29.9 °C and `Potassium` 10.2–13.0. |
| **Accepted as-is** | Kept unchanged and recorded as limitations:<br>· the suspected unit problems in `Magnesium` (values fit mg/dL, not the documented mmol/dL), `Lactate` (fit mmol/L, not mg/dL) and `Calcium` (a low cluster near 1, possibly ionised calcium in mmol/L) — *the `Calcium` part superseded 27 October 2026: values below 2.0 mg/dL are now set to missing (Cleaning)*;<br>· *added 27 October 2026:* `Calcium` in hospital B has a separate peak at 4.0–5.25 mg/dL (271 training patients by last value) below its main distribution; kept, since the user chose "below 2.0 mg/dL only" (Analysis Log row 21);<br>· the vitals clipped at exactly 20, 300 and 100;<br>· *added 18 October 2026, after step 3:* `PTT` at its apparent reporting limits, exactly 150 s in hospital A and 250 s in hospital B (user: "record PTT's spike at 150 s and the values at 250 s as accepted as-is, alongside the clipped vitals");<br>· positive `HospAdmTime` (255 patients, 8,483 kept hours);<br>· patients under 18 (21 patients, youngest 14) in an adult ICU population;<br>· `Age` = 100 in 392 patients, all in set B, most likely an anonymisation cap for "90 or above".<br>User, 15–16 October: "Keep the suspected unit problems (Magnesium, Lactate) and the clipped vitals as they are"; Calcium "like Magnesium and Lactate"; "Keep as-is and record". | Limitations: these columns may mix scales or be cut off, and no model can tell. Ages above 89 are indistinguishable in set B but exact in set A. |
| **Admissibility** | ADM-1 yes (DR-01). ADM-3: patient is the group unit; hospital is a second grouping; how the time order is handled is decided in step 2 (DR-02). ADM-4: yes for adult ICU patients at these two hospitals, unsure beyond (DR-03). | Limitations recorded in DR-01 and DR-03. |
| **Target and leakage** | Target: `SepsisLabel` (DR-01). Limitations: it is built by rule (Sepsis-3), partly from inputs, and shifted 6 h before onset. The exact target is decided in step 2. Set aside as inputs: `ICULOS`; the record length; every row from the hour `SepsisLabel` first becomes 1; any summary over the whole stay. `HospAdmTime` stays. User: "set aside ICULOS, the record length, every row from the hour SepsisLabel first becomes 1, and any summary over the whole stay. HospAdmTime may stay." | Removes the hour-in-stay as an input. `ICULOS` is kept only to order each stay's rows and to define time windows, never as an input. User, 16 October: "use it only to order each stay's rows and to define time windows, never as an input." |
| **Derived tables** | Built by `Code/sepsis_03_build_table.py`, outside git (`Code/outputs/sepsis/private/`, listed in `.gitignore`).<br>· `hours.csv.gz`: one row per kept hour; 1,524,294 rows (A 773,079, B 751,215) × 35 columns (`patient`, `set`, 32 inputs and `ICULOS`). `SepsisLabel` is not included, because every kept hour is 0. SHA-256 `b0459127633daf450c6eb50eecd301ed44201c98d09c129ab55c8368a6630e07` since the `Calcium` rule (27 October 2026); before it, `f86128f3be3c87bf84aee2abf5f7c8852af7f5227c495133ea4b7dba8dd2b86e` (superseded).<br>· `patients.csv.gz`: one row per patient, all 40,336, with `set`, `septic` (ever `SepsisLabel` = 1), `label_onset_iculos` (the `ICULOS` at which `SepsisLabel` first becomes 1, i.e. `t_sepsis` − 6 h) and `hours_kept`. It is the label source for step 2, not an input. SHA-256 `0d8ab8d4a46df453298d725f3a6b61855dd355cc9b10c4685715cffd144d1535`.<br>Both are gzip files with a fixed timestamp, so a re-run gives the same checksums. | Removing label-1 rows would otherwise lose which patients become septic; `patients.csv.gz` keeps it. `hours_kept` is the kept record length and must not become an input. |
| **Experience level** | Intermediate. | — |

## Problem Definition

*Step 2, written 17–18 October 2026, before anything was trained: from metadata and patient counts only. No model has been fitted, and no relationship between inputs and outcome has been looked at. Step 2 closed 18 October 2026, with the test set locked (DR-08).*

### Discussion

**The problem, in the user's words** (17 October 2026): "Flag ICU patients at risk of developing sepsis, using only the data available in their first hours in the ICU, so that clinicians can monitor them more closely."

**Prediction, not understanding (ADM-2, DR-04).** The user: "prediction for new patients, not understanding which measurements are connected to sepsis (p. 20)."

**The target: one prediction per patient.** Two framings were put to the user:
- (a) one prediction per patient, made from the first N ICU hours, of whether `SepsisLabel` switches on later;
- (b) a prediction every hour, as in the Challenge, with a window of past values as inputs (the book's only sequence handling, pp. 38–39).

The user chose (a), with N = 6 hours and a time limit: does `SepsisLabel` switch on within 48 hours after the window? This settles the time handling left open in DR-02. One row per patient keeps the rows independent, as the book assumes (p. 16). Framing (b) was not taken, because one patient's hours are not independent of each other.
- *Why a time limit.* Without one, a positive could have its label switch on as late as hour 331, while non-septic patients are followed only until ICU discharge. "Sepsis at any later point" would then partly measure how long a patient stays.
- *What a positive means.* `SepsisLabel` switches on 6 hours before `t_sepsis` (DR-01). A positive is therefore a patient whose label switches on at ICU hour 7 to 54, i.e. whose Sepsis-3 onset falls at hour 13 to 60.
- *Window lengths compared.* Counts for N = 6 and N = 12 (`Code/outputs/sepsis/04_target_counts.json`): 39,088 and 39,310 patients have an hour in the window with the label not yet on, and 2,180 (5.58 %) and 1,953 (4.97 %) of them have the label switch on later at any time. The user chose N = 6.
- *Outcome read from the label onset, not from record length.* Step 1 set aside every row from label onset, so a septic patient's kept record ends the hour before onset. For N = 6, 46 positives (33 in A, 13 in B) have a kept record ending at hour 6, because their label switches on at hour 7. They are counted as positives (`Code/outputs/sepsis/05_horizon_counts.json`). User: they "must be counted by their real outcome, not as short stays."
- *Patients without sepsis whose record ends before hour 54: kept as negatives.* No sepsis was observed for them, but they were not followed for the full 48 hours: 33,016 of the 39,088 patients (84 %; median last hour 37). Two options were put to the user (Analysis Log, row 7):
  - keep them as negatives, with the outcome read as "while still in the ICU": all 39,088 patients, 3.15 % positive, and the evaluation data stays the population met at hour 6 (pp. 328–329);
  - exclude them, as rows with a missing output are dropped (p. 345): 6,072 patients, 20.26 % positive. But whether a patient stays to hour 54 is not known at hour 6, so the remaining group would not be the one the model meets in use (pp. 328–329).

  The user: "Keep them as negatives; the outcome is 'the label switches on within 48 hours after the first 6 hours, while the patient is still in the ICU'. Record the gap as a limitation, and write a FLAG record noting that survival analysis would address it but is outside chapters 2, 3, 4 and 13." *Limitation:* sepsis after ICU discharge is not seen, and the files do not say why a stay ended (recovery, transfer or death), so some negatives may be patients who would have become positive. Survival analysis, which models outcomes whose follow-up ends early, is outside the book (DR-07).

**The metric.** The user chose the area under the precision–recall curve (PR-AUC) to decide between models, "because at about 3% positives a fixed threshold of 0.5 would make the comparison meaningless." The book calls the precision–recall curve more informative than ROC for imbalanced problems (p. 92), and asks for one deciding metric with others monitored alongside (p. 330). Reported alongside: F2, precision and recall at a threshold chosen on the training data only. F2 weights recall twice as heavily as precision (p. 92), which is the user's statement that a missed case costs more than a false alarm. Accuracy was not chosen, because a classifier that flags nobody scores about 97 % on it (p. 91).

**Earlier answers replaced.** A first set of answers (17 October) proposed a 90 / 10 split with seed 42, ROC-AUC among the secondary metrics, and calibrated probabilities. The user interrupted it and replaced it with the answers recorded here before anything was written or computed.

**Validation and test data: both hospitals, split by patient.** The user: "mix both, splitting by patient, as the book advises that validation and test data should come from the data the model will meet in use (pp. 328–329), and as recorded in DR-03. Training on one hospital and testing on the other may become a separate sub-task later; not now." This settles the hospital question left open in DR-02 and DR-03.

### Problem

Agreed 17 October 2026 (DR-05, DR-06). Counts are from `Code/outputs/sepsis/05_horizon_counts.json`.

| Item | Agreed |
| --- | --- |
| **Rows** | One per patient: every patient with at least one kept hour in ICU hours 1–6 whose label has not switched on by hour 6. 39,088 patients (A 19,473, B 19,615). Not included: 965 patients with no kept hour in hours 1–6, and 283 whose label switches on within them. |
| **Output y** | 1 if `SepsisLabel` switches on at ICU hour 7–54, i.e. within 48 hours after the window while the patient is still in the ICU (Sepsis-3 onset at hour 13–60); 0 otherwise, including patients who leave the ICU before hour 54 without it. Read from `label_onset_iculos`, never from record length. 1,230 positive (3.15 %): A 780 (4.01 %), B 450 (2.29 %). |
| **Inputs x** | The 32 inputs kept in step 1, from ICU hours 1–6 only. How the six hours are summarised into one row, and how empty values are handled, is input design, decided in step 3 (§9). `ICULOS`, record length and anything after hour 6 are not inputs. |
| **Output type (P1)** | Binary. |
| **What a prediction is for** | To flag patients for closer monitoring by clinicians. A missed case costs more than a false alarm, as expressed by β = 2. |
| **Deciding metric** | PR-AUC on the held-out patients, computed as average precision (see note below). |
| **Monitored alongside** | F2 (β = 2), precision and recall at a decision threshold chosen by cross-validation on the training data only, after the configuration is selected (§16). |
| **Baseline** | The most common training class: flag nobody (p. 331). Its scores are constant, so its PR-AUC equals the positive rate, which is the no-skill reference for PR-AUC (p. 92); its recall and F2 are 0, and its precision is undefined. |
| **Success criterion** | Test PR-AUC above the no-skill level (the test set's positive rate) by more than the spread of PR-AUC across the outer cross-validation folds. The spread is the standard deviation, across the 10 outer folds, of the recommended configuration's PR-AUC: the uncertainty defined in step 4g `[B→I pp.71–73]`. |
| **Achievable level** | Unknown. The Challenge scored hourly predictions with its own utility score, which is not comparable. |
| **P5** | Inspectable, a strong preference, not a must-have. |
| **P6** | Yes, a preference, not a must-have: probabilities and a tuned threshold. |
| **P7** | No. |
| **P8** | Unknown. |
| **Split** | 20 % test, by patient (one row per patient), shuffled, stratified by outcome and hospital, seed 2026: 31,270 training patients (984 positive, 3.15 %) and 7,818 test patients (246 positive, 3.15 %). Cross-validation folds are stratified the same way. The test set is locked (DR-08, `Code/outputs/sepsis/06_split.json`). |

*PR-AUC computed as average precision.* The book draws the precision–recall curve and its area (p. 92) but does not say how the area is computed. Average precision (scikit-learn's `average_precision_score`) sums precision at each recall step; the alternative, a trapezoid under the curve, interpolates between points and can overstate the area. Average precision is our choice `[I]`, proposed to the user on 17 October and confirmed: "Yes, compute PR-AUC as average precision, tagged [I]."

### Sub-tasks

1. **Sepsis within 48 hours from the first 6 ICU hours.** For each patient in the cohort, predict from ICU hours 1–6 whether `SepsisLabel` switches on within the next 48 hours while the patient is still in the ICU. Success: test PR-AUC above the test positive rate by more than the outer-fold spread of PR-AUC.

Training on one hospital and testing on the other is not a sub-task now; the user may add it later.

*Open point for step 4e.* Because P10 is expected to be imbalanced, the diagnosis loop measures errors as 1 − PR-AUC (`ML Guide.md` §16, changed 18 October 2026, Analysis Log row 11). On that scale O4 (underfitting) may fire too often. If it does, raise it as a `FRAMEWORK` question with the evidence; the `[I]` ratios for O3 and O4 stay unchanged until then.

## Analysis

### Sub-task 1 — Sepsis within 48 hours from the first 6 ICU hours

**Training table (step 3).** Built by `Code/sepsis_07_train_table.py` with the input design of DR-09, from the training patients only (`Code/outputs/sepsis/07_train_table.json`).
- 31,270 patients, 984 positive: A 15,578 (624), B 15,692 (360).
- 58 input columns: 27 last values, 27 "measured in hours 1–6" indicators, `Age`, `Gender`, `HospAdmTime` and `Unit`. After one-hot encoding of `Unit`: 60 columns.
- `Unit`: MICU 9,585, SICU 9,579, unknown 12,106.
- Share of training patients with at least one value in hours 1–6: the vitals 90–100 % (`DBP` 77 %: A 55 %, B 99 %); the labs 15–65 %, lowest `Bilirubin_total` 15.0 %, `Alkalinephos` 15.4 %, `AST` 15.5 %, highest `Glucose` 64.6 %. The hospitals differ most for `PTT` (A 39.5 %, B 12.4 %), `FiO2`, `pH` and `PaCO2` (A 45–49 %, B 19 %), and `Hct` (A 61.5 %, B 39.0 %).
- 38 training patients have no clinical value at all in hours 1–6; every one of their last values is filled.
- Every last value of the ten log inputs is positive (smallest: `Creatinine`, `WBC` and `Bilirubin_total` 0.1).

**Fitted weights of the final model (step 4h, from a verified rebuild).** `final` (step 4g) fitted the model in memory and saved only its test predictions. At the user's decision, the core's new `explain` command rebuilds it: `Logistic + L2`, λ = 10⁻³ (C = 0.0160), refitted on all 31,270 training patients by the same code path as `final`. The rebuild is accepted only if its probabilities for the 7,818 test patients equal the saved ones exactly; it read the test inputs and the saved probabilities only, no outcome, and computed no metric. Result: identical for all 7,818. Core version `22353007…` → `7a848f3e…`, by adding `explain` only; none of the functions behind DR-12 to DR-20 changed (`Code/outputs/sepsis/core_weights.json`).
- Intercept −3.6691. Weights are on the log-odds scale per 1 SD of each standardised design column (after the DR-09 log and median), with the other columns fixed; they are not causal effects (§21).
- The ten largest by size: `measured_FiO2` +0.2926, `measured_SBP` −0.2294, `measured_Calcium` +0.1940, `MAP` −0.1846, `HR` +0.1769, `Resp` +0.1682, `measured_WBC` +0.1649, `measured_MAP` +0.1443, `Unit_SICU` −0.1343, `measured_Lactate` +0.1196. All 60 are in the output file.
- The three `Unit` columns sum to the intercept (DR-12), so only differences between their weights are determined by the data; L2 picks one set of values among equivalent ones. Their weights are read relative to each other, not one at a time.

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

### DR-04 · ADM · step 2

- **Sub-task:** all
- **Date:** 2026-10-17
- **Question:** Is the main aim to predict the outcome for new cases, or to understand how the variables are connected (ADM-2)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| The user's problem | "Flag ICU patients at risk of developing sepsis, using only the data available in their first hours in the ICU, so that clinicians can monitor them more closely." | M | user, 17 October 2026 |
| User's answer | "prediction for new patients, not understanding which measurements are connected to sepsis (p. 20)." | M | user, 17 October 2026 |

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
- **Decision:** The aim is to predict sepsis for new ICU patients, so the work continues. Nothing in it establishes how any measurement is connected to sepsis.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** n/a

### DR-05 · FORM · step 2

- **Sub-task:** 1
- **Date:** 2026-10-17
- **Question:** What is predicted, from what, judged by which metric, against which baseline, and what counts as success?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Target | "the label switches on within 48 hours after the first 6 hours, while the patient is still in the ICU" | M | user, 17 October 2026 |
| Patients not followed to hour 54 | "Keep them as negatives … Record the gap as a limitation" | M | user, 17 October 2026 |
| Cohort and outcome counts | 39,088 patients; 1,230 positive (3.15 %), A 780 (4.01 %), B 450 (2.29 %); 33,016 never-septic patients leave before hour 54 | M | `Code/outputs/sepsis/05_horizon_counts.json` |
| Metric | "the area under the precision-recall curve (PR-AUC) decides between models (pp. 91-93) … Report alongside it (p. 330): F2 (beta = 2), precision and recall at a threshold chosen on the training data only." | M | user, 17 October 2026 |
| Baseline | "most common class ("flag nobody", p. 331). Also report the no-skill reference for PR-AUC (the positive rate)." | M | user, 17 October 2026 |
| Success criterion | "test PR-AUC clearly above the no-skill level, by more than the spread of PR-AUC across the outer cross-validation folds." | M | user, 17 October 2026 |
| Achievable level | "unknown" | M | user, 17 October 2026 |
| Must-haves and expectations | P5 "inspectable, a strong preference, not a must-have"; P6 "probabilities and a tuned threshold, a preference, not a must-have"; P7 "no"; P8 "unknown" | M | user, 17 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P1 | binary | [B p.17] | classification task gate: Logistic, k-NN, Tree (§12) |
| One deciding metric, others monitored | PR-AUC decides; F2, precision, recall monitored | [B p.330] | PR-AUC is the selection metric in §16 |
| Imbalanced problems need more than the misclassification rate | accuracy not used | [B p.91] | — |
| Precision–recall curve for imbalanced problems | PR-AUC chosen | [B→I p.92] | the book calls it more informative than ROC; using its area as the deciding metric is our step |
| F_β for asymmetric problems | β = 2 | [B p.92] | used for the threshold and monitored |
| SEQ-1 baseline | most common training class (flag nobody) | [B pp.330–331] | always cross-validated and reported |
| No-skill reference for PR-AUC | the positive rate | [B p.92] | equals the baseline's PR-AUC, because the baseline's score is constant |
| Decision threshold (§16) | tuned by CV on training data after selection, maximising F2 | [B→I pp.53–54, 92–93] | applies because P6 = yes |
| Uncertainty of the test result (step 4g) | SD of PR-AUC across the outer folds | [B→I pp.71–73] | sets the margin in the success criterion |
| PR-AUC computed as average precision | `UNLISTED [I]`: "the area under the precision–recall curve is computed as average precision, not by trapezoids" | [I] | confirmed by the user, 18 October: "Yes, compute PR-AUC as average precision, tagged [I]." |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| β in F_β | 2 | the user's choice |

- **Options considered:** target: label switch at any later time · within 48 h after the window, short stays kept as negatives · within 48 h, short stays excluded; metric: PR-AUC · F2 · ROC-AUC · accuracy
- **Expectation:** n/a
- **Decision:** Predict, for each of the 39,088 patients, from ICU hours 1–6, whether `SepsisLabel` switches on at hour 7–54 while the patient is still in the ICU. Models are compared on PR-AUC against the flag-nobody baseline. Success means test PR-AUC exceeds the test positive rate by more than the outer-fold spread of PR-AUC.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/sepsis_04_target_counts.py`, `Code/sepsis_05_horizon_counts.py`, `Code/outputs/sepsis/04_target_counts.json`, `Code/outputs/sepsis/05_horizon_counts.json`

### DR-06 · PROP · step 2

- **Sub-task:** 1
- **Date:** 2026-10-17
- **Question:** What are the property values known before any training data is looked at (P1–P8)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 output type | binary | M | DR-05 |
| P2 data-to-parameter ratio | ample. About 31,270 training patients (80 % of 39,088). With 32 inputs: 31,270 ÷ 33 ≈ 948. Provisional: the input count is fixed by the step 3 input design, but the ratio stays above 10 for any count below about 3,100 | M | `Code/outputs/sepsis/05_horizon_counts.json`; step 1 input count |
| P3 number of inputs | many: 32 inputs per hour (33 if a missing unit gets its own category). Provisional, as for P2 | M | Data Summary, *Machine learning checks* |
| P4 share of categorical inputs | low: 3 of 32 (9.4 %). Provisional, as for P2 | M | Data Summary, *Machine learning checks* |
| P5 interpretability | inspectable, not a must-have: "inspectable, a strong preference, not a must-have" | M | user, 17 October 2026 |
| P6 probabilities or tuned threshold | yes, not a must-have: "probabilities and a tuned threshold, a preference, not a must-have" | M | user, 17 October 2026 |
| P7 beyond the training range | no: "P7: no." | M | user, 17 October 2026 |
| P8 expected shape | unknown: "P8: unknown." | M | user, 17 October 2026 |
| P9, P10 | not yet known; computed from the training data in step 3 | — | — |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P1 = binary | task gate | [B p.17] | Logistic, k-NN, Tree admissible (§12) |
| P2 = ample | no entry | [I] threshold | no matrix entry applies |
| P3 = many | holds (provisional) | [I] threshold | k-NN −1 `[I]`; + poly −1 `[B→I p.59]` |
| P4 = low | no entry | [I] threshold | — |
| P5 = inspectable (not a must-have) | holds | [B→I p.347] | +1 Logistic, Tree; + poly −1 `[I]`. "Strong" has no separate effect in the guide: P5 is either a must-have or not |
| P6 = yes (not a must-have) | holds | [B→I pp.50, 53–54] | +1 Logistic; threshold tuned (§16) |
| P7 = no | no entry | — | — |
| P8 = unknown | no entry | — | contributes nothing (§11) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited if ratio < 10 | 10 | ≈ 948 (provisional) |
| P3 many if > 20 inputs | 20 | 32 (provisional) |
| P4 high if ≥ 50 % categorical | 50 % | 9.4 % (provisional) |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** P1 binary; P2 ample, P3 many and P4 low (all provisional until step 3); P5 inspectable and P6 yes, both preferences rather than must-haves; P7 no; P8 unknown.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** superseded by DR-10 (P2–P4 after input design, P9–P10)
- **Links:** `Code/outputs/sepsis/05_horizon_counts.json`

### DR-07 · FLAG · step 2

- **Sub-task:** 1
- **Date:** 2026-10-17
- **Question:** Does the evidence suggest that a method outside the solution space might help?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Incomplete follow-up | 33,016 of 39,088 patients (84 %) leave the ICU before hour 54 without the label switching on, and are counted as negatives | M | `Code/outputs/sepsis/05_horizon_counts.json` |
| User's instruction | "write a FLAG record noting that survival analysis would address it but is outside chapters 2, 3, 4 and 13." | M | user, 17 October 2026 |
| The book | no chapter or section on survival analysis, censoring or time-to-event outcomes in the table of contents of the 2nd edition | M | smlbook.org, read 18 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Flags (§20) | survival analysis recorded as a flag | [I] | not applied, not tested |
| §23 | survival analysis is not listed | `UNLISTED [I]`: "survival analysis: not covered in the book" | the flag names it as outside the book |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** Survival analysis is flagged as a method that might handle outcomes whose follow-up ends early. It is not covered in the book and is not used.

**Flag**

| Method | Chapter | Evidence it might help | Status |
| --- | --- | --- | --- |
| Survival (time-to-event) analysis, which handles outcomes whose follow-up ends early (censoring) | Not in the book (none of chapters 1–14) | 84 % of the cohort is not observed for the full 48 hours and is treated as negative | Not applied and not tested. Nothing here says it would have done better. |

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/sepsis/05_horizon_counts.json`

### DR-08 · SPLIT · step 2

- **Sub-task:** 1
- **Date:** 2026-10-18
- **Question:** How are the patients split into training and test data, and how are the cross-validation folds made?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| User's instruction | "Make the split (20% test, by patient, stratified by outcome and hospital, seed 2026), lock the test set" | M | user, 18 October 2026 |
| Folds | "stratify the cross-validation folds by outcome and hospital, the same as the test split. Record it now." | M | user, 18 October 2026 |
| Unit | one row per patient (39,088 patients), so splitting by row is splitting by patient (DR-02) | M | `Code/outputs/sepsis/06_split.json` |
| Training data | 31,270 patients, 984 positive (3.15 %); A 15,578 (624, 4.01 %), B 15,692 (360, 2.29 %) | M | `Code/outputs/sepsis/06_split.json` |
| Test data | 7,818 patients, 246 positive (3.15 %); A 3,895 (156, 4.01 %), B 3,923 (90, 2.29 %) | M | `Code/outputs/sepsis/06_split.json` |
| Split file | `Code/outputs/sepsis/private/cohort.csv.gz` (patient, set, y, split; not in git), SHA-256 `55dce9ca19702d3829c8ba36a164d2df126e709e3e5f5bd7b3dbffebfc889b4c`; a re-run gives the same checksum | M | `Code/outputs/sepsis/06_split.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| ADM-3, group | split by patient | [B p.329] | no patient in both training and test data, or in more than one fold |
| ADM-4 | validation and test data from both hospitals, like the intended use | [B pp.328–329] | hospitals mixed, not one held out (DR-03, Problem Definition) |
| Shuffle before splitting | shuffled | [B pp.71, 73] | — |
| Test set used once | locked | [B pp.74, 328] | nothing in steps 3 and 4 reads the test patients until step 4g |
| Stratified folds (§16) | stratified by outcome and hospital | `[I]`, extended by the user from outcome to outcome × hospital: `UNLISTED [I]` "stratify the cross-validation folds by outcome and hospital, the same as the test split" | applies to the outer and inner folds in step 4 |
| Test split stratified by outcome and hospital | four strata (A/B × 0/1) | `UNLISTED [I]` | the same positive share in each hospital in training and test |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Test fraction | 20 % (the user's choice) | 7,818 of 39,088 |

- **Options considered:** test fraction 10 % or 20 %; stratified by outcome only, or by outcome and hospital; one hospital held out (not taken, DR-03)
- **Expectation:** n/a
- **Decision:** 20 % of patients, shuffled with seed 2026 and stratified by outcome and hospital, form the test set, which is locked. Cross-validation folds are stratified the same way.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — quoted above
- **Supersedes / superseded by:** n/a
- **Links:** `Code/sepsis_06_split.py`, `Code/outputs/sepsis/06_split.json`, `06_split.md`

### DR-09 · FORM · step 3

- **Sub-task:** 1
- **Date:** 2026-10-18
- **Question:** How do each patient's first 6 ICU hours become one row of inputs (input design, §9)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| User's decision and reason | Option A + D: "Last value, because it is the simplest summary and what a clinician sees at hour 6 (start simple, p. 331); indicators, because the missingness is systematic (p. 345)." | M | user, 18 October 2026 |
| Filling | "(i), the training-fold median, fitted inside each fold, the same for every model family." | M | user, 18 October 2026 |
| Logarithms | "on the ten labs you listed, tagged [I] as domain judgement, not chosen from the outcome": `AST`, `Alkalinephos`, `Bilirubin_total`, `Creatinine`, `BUN`, `Lactate`, `WBC`, `Glucose`, `Platelets`, `PTT` | M | user, 18 October 2026 |
| Unit | "Unit as one categorical input: MICU, SICU or unknown." | M | user, 18 October 2026 |
| Hospital | "Hospital is not an input, as decided in step 1." | M | user, 18 October 2026 |
| Systematic missingness | labs recorded in under 10 % of hours (Data Summary); recording differs between hospitals | M | Data Summary; DR-03 |
| Options put to the user | A last value · B mean · C min and max · D measured indicators; filling (i) median + indicators, (ii) median only, (iii) drop rarely measured columns | M | conversation, 18 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design (§9) | decided with the user, not a configuration axis, not chosen by CV | [B p.18] | one design for every family |
| Summary features and transforms are a design choice | last value per column; natural log of ten labs | [B p.18] | — |
| Start simple | the simplest summary first | [B p.331] | richer summaries only if the errors call for them, as a recorded change |
| Systematic missingness | measured indicators kept beside filled values | [B→I p.345] | the book warns that dropping or imputing systematically missing values creates a mismatch; adding indicators is ours |
| Imputation builds in assumptions | training-fold median, same for every family | [B p.345] | — |
| Missingness handled directly by a method | not used (no native NaN handling in trees) | [B→I p.346] | the families are compared on the same filled inputs |
| REQ-1 | median and encoding fitted inside each fold | [B p.27] + [I] | `preprocessor()` in `Code/sepsis/core.py` |
| REQ-6 | `Unit` one-hot encoded (3 levels) | [B p.49] | — |
| Which inputs get a log | the ten labs | `UNLISTED [I]`: "domain judgement, not chosen from the outcome" | applies to Logistic and k-NN; trees are unaffected |
| Which summary (last value) | A + D | `UNLISTED [I]` | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** A last value · B mean · C min and max (or worst value) · D measured indicators; filling (i) · (ii) · (iii); hospital as an input or not
- **Expectation:** n/a
- **Decision:** Each patient's row holds the last value of each of the 27 clinical columns in hours 1–6 (ten of them on a log scale, empty values filled with the training-fold median), a 0/1 indicator per clinical column for whether it was measured in hours 1–6, `Age`, `Gender`, `HospAdmTime`, and `Unit` (MICU, SICU or unknown); hospital is not an input.
- **Limitation (user's instruction):** the indicators partly capture clinical ordering habits (a lab is drawn when a clinician is concerned) and hospital practice (recording differs between A and B), not only the patient's physiology.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — quoted above
- **Supersedes / superseded by:** superseded by DR-19 (the median rule extended to `Age`, `Gender`, `HospAdmTime`, 27 October 2026)
- **Links:** `Code/sepsis_07_train_table.py`, `Code/outputs/sepsis/07_train_table.json`, `Code/sepsis/core.py` (`preprocessor()`)

### DR-10 · PROP · step 3

- **Sub-task:** 1
- **Date:** 2026-10-18
- **Question:** What are the property values P1–P10 once the input design is fixed and P9–P10 are computed from the training patients?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 output type | binary (unchanged) | M | DR-05 |
| P2 data-to-parameter ratio | 31,270 training patients ÷ (60 input columns after encoding + 1) = 512.6 | M | `Code/outputs/sepsis/07_train_table.json`; `core_p9_p10.json` (`input_columns_after_encoding`: 60) |
| P3 number of inputs | 60 columns after encoding (27 last values, 27 indicators, `Age`, `Gender`, `HospAdmTime`, `Unit` as 3) | M | `Code/outputs/sepsis/core_p9_p10.json` |
| P4 share of categorical inputs | 29 of 58 original input columns = 50.0 %: the 27 indicators, `Gender` and `Unit`. User: "count the 27 indicators as categorical, following the book (pp. 16-17) and consistent with Gender in step 1." | M | `Code/outputs/sepsis/07_train_table.json` (`categorical_input_columns`); user, 18 October 2026 |
| P5, P6, P7, P8 | unchanged from DR-06: P5 inspectable (not a must-have), P6 yes (not a must-have), P7 no, P8 unknown | M | DR-06 |
| P9 classes perfectly separable | no: training accuracy 0.9685 (`0.9685001598976655`) with negligible regularisation (C = 1e8, converged in 30 iterations) | T | `Code/outputs/sepsis/core_p9_p10.json` |
| P10 class imbalance | imbalanced: smallest class 984 of 31,270 = 3.15 % (`0.03146786056923569`) | T | `Code/outputs/sepsis/core_p9_p10.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P1 = binary | task gate | [B p.17] | Logistic, k-NN, Tree admissible (§12) |
| P2 = ample | no entry | [I] threshold | — |
| P3 = many | holds | [I] threshold | k-NN −1 `[I]`; + poly −1 `[B→I p.59]` |
| P4 = high | holds, exactly at the threshold | [I] threshold | k-NN −1 `[I]` |
| Categorical = finite set of values without natural order; yes/no is a modelling choice | the 27 0/1 indicators counted as categorical | [B pp.16–17] | P4 = high |
| P5 = inspectable (not a must-have) | holds | [B→I p.347] | +1 Logistic, Tree; + poly −1 `[I]` |
| P6 = yes (not a must-have) | holds | [B→I pp.50, 53–54] | +1 Logistic; threshold tuned (§16) |
| P7 = no, P8 = unknown | no entry | — | — |
| P9 = no | MOD-1 does not apply | [I] procedure | `Logistic` and `Logistic + poly` stay admissible |
| P10 = imbalanced | holds | [I] threshold | no matrix row (§13); metric and threshold already set for it (DR-05); diagnosis errors are 1 − PR-AUC (`ML Guide.md` §16, `ddda293`) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited if ratio < 10 | 10 | 512.6 |
| P3 many if > 20 inputs | 20 | 60 |
| P4 high if ≥ 50 % categorical | 50 % | 50.0 % (29 of 58) |
| P9 separable if training accuracy = 100 % with negligible regularisation | 100 %, C = 1e8 | 96.85 % |
| P10 imbalanced if smallest class < 20 % | 20 % | 3.15 % |

- **Options considered:** P4 counting the indicators as categorical (high) or not (low, 2 of 31)
- **Expectation:** n/a
- **Decision:** P1 binary, P2 ample, P3 many, P4 high, P5 inspectable and P6 yes (both preferences, not must-haves), P7 no, P8 unknown, P9 no, P10 imbalanced.
- **Note on P4 (user's instruction):** P4 sits exactly on its `[I]` threshold (29 of 58 = 50.0 %), so a one-column change to the inputs would flip it: one categorical column fewer, or one numerical column more, gives low. P4 = high adds −1 to k-NN in the prior (§13), on top of the −1 from P3 = many.
- **Note on P9:** the fit establishes a property only. It is not a candidate model, and its accuracy is not a result.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

**Reference code**

- Function: `p9_p10` (`cd Code && uv run python sepsis/core.py p9p10`) · version: interim core, not reviewed, SHA-256 `43af578e16c91ab05f0f1ce439acf92aa6a21811669d7d2e92368eb0963b30b7` · inputs: the training table, DR-09 design · output: `Code/outputs/sepsis/core_p9_p10.json`, copied above unchanged.

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — the core, interpretations (a)–(c), and P4: "count the 27 indicators as categorical"
- **Supersedes / superseded by:** supersedes DR-06; superseded by DR-11 (27 October 2026, after the `Calcium` cleaning rule)
- **Links:** `Code/sepsis/core.py`, `Code/outputs/sepsis/core_p9_p10.json`, `Code/outputs/sepsis/07_train_table.json`

### DR-11 · PROP · step 3

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** What are the property values P1–P10 after the `Calcium` cleaning rule (values below 2.0 mg/dL set to missing, Data Summary) changed the training table and the core was re-run?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| P1 output type | binary (unchanged) | M | DR-05 |
| P2 data-to-parameter ratio | 31,270 training patients ÷ (60 input columns after encoding + 1) = 512.6 (unchanged) | M | `Code/outputs/sepsis/07_train_table.json`; `core_p9_p10.json` (`input_columns_after_encoding`: 60) |
| P3 number of inputs | 60 columns after encoding (unchanged) | M | `Code/outputs/sepsis/core_p9_p10.json` |
| P4 share of categorical inputs | 29 of 58 original input columns = 50.0 % (unchanged; counting as in DR-10) | M | `Code/outputs/sepsis/07_train_table.json` (`categorical_input_columns`) |
| P5, P6, P7, P8 | unchanged from DR-06: P5 inspectable (not a must-have), P6 yes (not a must-have), P7 no, P8 unknown | M | DR-06 |
| P9 classes perfectly separable | no: training accuracy 0.9684 (`0.9684362008314679`) with negligible regularisation (C = 1e8, converged in 28 iterations) | T | `Code/outputs/sepsis/core_p9_p10.json` |
| P10 class imbalance | imbalanced: smallest class 984 of 31,270 = 3.15 % (`0.03146786056923569`) | T | `Code/outputs/sepsis/core_p9_p10.json` |

**Rules applied**

As DR-10, with the same results: no property value changed.

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| P1 = binary | task gate | [B p.17] | Logistic, k-NN, Tree admissible (§12) |
| P2 = ample | no entry | [I] threshold | — |
| P3 = many | holds | [I] threshold | k-NN −1 `[I]`; + poly −1 `[B→I p.59]` |
| P4 = high | holds, exactly at the threshold | [I] threshold | k-NN −1 `[I]` |
| Categorical = finite set of values without natural order; yes/no is a modelling choice | the 27 0/1 indicators counted as categorical | [B pp.16–17] | P4 = high |
| P5 = inspectable (not a must-have) | holds | [B→I p.347] | +1 Logistic, Tree; + poly −1 `[I]` |
| P6 = yes (not a must-have) | holds | [B→I pp.50, 53–54] | +1 Logistic; threshold tuned (§16) |
| P7 = no, P8 = unknown | no entry | — | — |
| P9 = no | MOD-1 does not apply | [I] procedure | `Logistic` and `Logistic + poly` stay admissible |
| P10 = imbalanced | holds | [I] threshold | no matrix row (§13); metric and threshold already set for it (DR-05); diagnosis errors are 1 − PR-AUC (`ML Guide.md` §16, `ddda293`) |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| P2 limited if ratio < 10 | 10 | 512.6 |
| P3 many if > 20 inputs | 20 | 60 |
| P4 high if ≥ 50 % categorical | 50 % | 50.0 % (29 of 58) |
| P9 separable if training accuracy = 100 % with negligible regularisation | 100 %, C = 1e8 | 96.84 % |
| P10 imbalanced if smallest class < 20 % | 20 % | 3.15 % |

- **Options considered:** whether to write this record at all, since no property changed: a new record superseding DR-10, or only a log row. The user chose the new record, because DR-10's P9 evidence no longer matches the output it says it copies.
- **Expectation:** n/a
- **Decision:** unchanged from DR-10: P1 binary, P2 ample, P3 many, P4 high, P5 inspectable and P6 yes (both preferences, not must-haves), P7 no, P8 unknown, P9 no, P10 imbalanced.
- **What moved:** P9's training accuracy, 0.9685 → 0.9684 (`0.9685001598976655` → `0.9684362008314679`), and its iterations, 30 → 28. The split is unchanged (`cohort.csv.gz` SHA-256 `55dce9ca…`, as recorded by `sepsis_06`), and so are the training patients, positives and input columns.
- **Note on P4:** as in DR-10, P4 sits exactly on its `[I]` threshold; the `Calcium` rule changes values, not columns, so it does not move.
- **Note on P9:** the fit establishes a property only. It is not a candidate model, and its accuracy is not a result.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

**Reference code**

- Function: `p9_p10` (`cd Code && uv run python sepsis/core.py p9p10`) · version: interim core, not reviewed, SHA-256 `43af578e16c91ab05f0f1ce439acf92aa6a21811669d7d2e92368eb0963b30b7` (unchanged) · inputs: the training table after the `Calcium` rule (`train_table.csv.gz` SHA-256 `44d64dd48dc0742c13a666cdd093ab07a12f38180c3ed438fc05193111254ef2`), DR-09 design · output: `Code/outputs/sepsis/core_p9_p10.json`, copied above unchanged.

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** the `Calcium` rule's scope (Analysis Log row 21); writing this record rather than only a log row
- **Supersedes / superseded by:** supersedes DR-10
- **Links:** `Code/sepsis/core.py`, `Code/outputs/sepsis/core_p9_p10.json`, `Code/outputs/sepsis/07_train_table.json`, `Code/outputs/sepsis/03_build_table.json`

### DR-12 · ADMSET · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** Which of the 14 structural configurations (§9) are admissible for sub-task 1, given the property values in DR-11?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Property values passed to the core | P1 binary, P2 ample, P3 many, P4 high, P5 inspectable (not a must-have), P6 yes (not a must-have), P7 no, P8 unknown, P9 no, P10 imbalanced | M / T | DR-11; `Code/sepsis/props_dr11.json` |
| Labels checked before 4a | `SepsisLabel` is built by rule (Sepsis-3), partly from the kinds of measurement that are inputs, and shifted 6 h earlier; inputs come from ICU hours 1–6 and the outcome is the label switching on at hour 7–54. Recorded as a limitation and accepted by the user in step 1; nothing new found | M | DR-01; Data Summary, `Target and leakage` |
| MOD-2, without powers | design matrix with intercept: 61 columns, rank 60, n_train 31,270. One null direction (singular value 1.93e-12): `Unit_unknown` 0.599, `Unit_MICU` 0.567, `Unit_SICU` 0.566 | T | `Code/outputs/sepsis/core_admset.json` |
| MOD-2, with powers 2–3 of the 29 numerical inputs | 119 columns, rank 118, n_train 31,270. The same single null direction (singular value 2.05e-12), the three `Unit` columns | T | `Code/outputs/sepsis/core_admset.json` |
| `Unit` encoding | "Keep 3 columns (DR-09 as is)", chosen from three options without a recommendation: keep 3 columns; 2 columns with one level as reference; reference coding for `Logistic` only | M | user, 27 October 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, P1 = binary | Logistic, k-NN, Tree admissible | [B pp.17, 49–57] | 8 configurations removed: the four `Linear`, both `Poisson`, both `Exponential` |
| Must-have gates (P5, P6) | not applied: neither is a must-have | [B→I p.347]; [B→I pp.50, 53–54] | none removed |
| MOD-1 | P9 = no: does not apply | [B p.61] | none removed |
| MOD-2 | applies: the three one-hot `Unit` columns sum to the intercept (exact collinearity), with and without powers | [B→I pp.46–47, 65] | `Logistic` and `Logistic + poly` removed; their `+ L2` versions remain |
| REQ-6 | `Unit` one-hot encoded with all three levels, as in DR-09 | [B p.49] | the source of the collinearity; kept by the user's choice |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| MOD-2 exact collinearity (interpretation e) | rank < columns at numpy `matrix_rank` default tolerance | rank 60 of 61; 118 of 119 |
| MOD-2 parameters ≥ n_train | 31,270 | 61; 119 |
| Largest polynomial degree checked (§16 grid) | 3 | — |

- **Options considered:** for `Unit`: 3 one-hot columns (DR-09); 2 columns with a reference level, which would remove the collinearity and admit all six binary-task configurations; reference coding for `Logistic` without L2 only, which would give the families different designs
- **Expectation:** stated before the run: MOD-2 would very likely apply because of `Unit`, removing `Logistic` and `Logistic + poly`; the run would show any other collinearity. Outcome: as expected, and `Unit` is the only collinearity.
- **Decision:** admissible: `Logistic + L2`, `Logistic + poly + L2`, `kNN`, `Tree`. DR-09 stands; `Unit` keeps three one-hot columns. Under §14 SEQ-2 the simple-first configuration will be `Logistic + L2`, because MOD-2 removed `Logistic` (applied in 4b).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] |
| `Poisson`, `Poisson + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] |
| `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] |
| `Logistic` | EXCL | MOD-2: 61 parameters, rank 60, n_train 31,270 (the three `Unit` columns and the intercept) [B→I pp.46–47, 65] |
| `Logistic + poly` | EXCL | MOD-2: 119 parameters, rank 118, n_train 31,270 (the same) [B→I pp.46–47, 65] |

**Reference code**

- Function: `admissible_set` (`cd Code && uv run python sepsis/core.py admset sepsis/props_dr11.json`) · version: interim core, not reviewed, SHA-256 `f505ef87a99b9e40fa65ded60c62c9f9432dfb2c0d28c640a35a9644d24636fd` (extended for 4a from `43af578e…`; `p9_p10` unchanged, so DR-11 stays valid) · inputs: DR-11 property values in `Code/sepsis/props_dr11.json`; the training table; interpretations d–f in the core's docstring · output: `Code/outputs/sepsis/core_admset.json`, copied above unchanged.

- **Confidence:** n/a
- **Outcome vs expectation:** agree (see Expectation)
- **User involvement:** approved the 4a extension of the core before it was run; asked — `Unit` encoding: "Keep 3 columns (DR-09 as is)"; asked again at the end of 4a whether P5 should become a must-have (three options: keep as a preference; must-have with similar cases acceptable for k-NN; must-have without), and chose "Keep as a preference", so DR-11 stands
- **Supersedes / superseded by:** n/a
- **Links:** `Code/sepsis/core.py`, `Code/sepsis/props_dr11.json`, `Code/outputs/sepsis/core_admset.json`, DR-09, DR-11

### DR-13 · PRIOR · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** In what order does the advisor expect the admissible configurations to do, which are kept for cross-validation, and what does the advisor expect cross-validation to show?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Admissible set | `Logistic + L2`, `Logistic + poly + L2`, `kNN`, `Tree` | T | DR-12 |
| Property values scored | P3 many, P4 high, P5 inspectable (not a must-have), P6 yes (not a must-have); P1 binary has no matrix entry for these families; P2 ample, P7 no and P8 unknown have no entries; P10 has no row (§13) | M / T | DR-11; `Code/sepsis/props_dr11.json` |
| Prior order | 1 `Logistic + L2` score +2 (P5→Logistic +1 `[B→I p.347]`, P6→Logistic +1 `[B→I pp.50, 53–54]`), 0 add-ons; 2 `Tree` +1 (P5→Tree +1 `[B→I p.347]`), 0 add-ons; 3 `Logistic + poly + L2` 0 (P5→Logistic +1, P6→Logistic +1, P3→poly −1 `[B→I p.59]`, P5→poly −1 `[I]`), 2 add-ons; 4 `kNN` −2 (P3→kNN −1 `[I]`, P4→kNN −1 `[I]`), 0 add-ons | — | `Code/outputs/sepsis/core_prior.json` |
| Simple-first (SEQ-2) | `Logistic + L2`, because MOD-2 removed `Logistic` (DR-12) | — | `Code/outputs/sepsis/core_prior.json` |
| Kept | all four: the simple-first configuration and the three others; no tie at the cut | — | `Code/outputs/sepsis/core_prior.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §13 matrix, P3 = many | k-NN −1; + poly −1 | [I]; [B→I p.59] | `kNN`, `Logistic + poly + L2` marked down |
| §13 matrix, P4 = high | k-NN −1 | [I] | `kNN` marked down |
| §13 matrix, P5 = inspectable (not a must-have) | Logistic +1, Tree +1, + poly −1 | [B→I p.347]; [I] for + poly | — |
| §13 matrix, P6 = yes (not a must-have) | Logistic +1 | [B→I pp.50, 53–54] | — |
| §15.3 order | score, then fewer add-ons; no ties | [I] | order as above |
| §14 SEQ-1 | baseline: most common training class, flag nobody | [B pp.330–331] | cross-validated in round 1 |
| §14 SEQ-2 | simple-first `Logistic + L2` (MOD-2 applies) | [B p.331] | — |
| §14 SEQ-3 | baseline and `Logistic + L2` first; the others only once `Logistic + L2` clearly beats the baseline | [B pp.331–332] | rounds 1 and 2 (4c, 4d) |
| §15.4 keep | simple-first + top 3 others (+ ties) | [I] threshold | all four kept, so no `DISF` |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| §15 number kept besides baseline and simple-first | 3 (plus ties) | 3 others admissible |

- **Options considered:** none: the ranking is mechanical (§15)
- **Expectation:** CV order (PR-AUC): `Logistic + L2` and `Logistic + poly + L2` close to each other, quite possibly within noise, at the top; `Tree` below them; `kNN` last; all four above the baseline. Why (the advisor's reasoning, `[I]`, not a finding): P8 is unknown, so nothing says the relationship needs curves; with 31,270 patients and 60 columns the L2-tuned logistic model has enough data for its 61 parameters, and powers may add a little; a single tree gives a few distinct probabilities (one per leaf), which ranks patients coarsely and tends to cost PR-AUC; k-NN measures distance over 60 standardised columns, half of them 0/1 indicators, and its probabilities are multiples of 1/k, which the matrix already marks down through P3 and P4.
- **Decision:** cross-validate the baseline (flag nobody) and `Logistic + L2` first (round 1); then `Tree`, `Logistic + poly + L2` and `kNN` (round 2), on the same folds.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| none admissible and not kept | — | all four admissible configurations are kept; the other ten are `EXCL` (DR-12) |

**Reference code**

- Function: `prior_ranking` (`cd Code && uv run python sepsis/core.py prior sepsis/props_dr11.json`) · version: interim core, not reviewed, SHA-256 `dbae21d4e80f8a31b7b75addd2c359bab47a82c12ffb969ea67c2c3b7cc9b5bc` (extended for 4b–4g from `f505ef87…`; `admissible_set` and `p9_p10` unchanged; approved by the user before this run) · inputs: DR-11 property values in `Code/sepsis/props_dr11.json` · output: `Code/outputs/sepsis/core_prior.json`, copied above unchanged.

- **Confidence:** n/a
- **Outcome vs expectation:** partial (filled in at 4d, from DR-14 and DR-15). As expected: the two logistic configurations lead and are within noise of each other (`Logistic + L2` 0.0930, `Logistic + poly + L2` 0.0907; margin 0.0023, spread 0.0077), and all four clearly beat the baseline. Not as expected: `kNN` (0.0706) ranks above `Tree` (0.0678), the reverse of the expected order; the margin between them is 0.0028 with spread 0.0088 (computed by the agent from the stored fold values, not a core output).
- **User involvement:** approved the extended core (§13–§19, interpretations g–s) before it was run; approved the method — the admissible set (DR-12), this ranking and the kept configurations, the §16 protocol and the survival-analysis flag (DR-07) — chosen as "Agree; close 4b" from three options without a recommendation, 27 October 2026
- **Supersedes / superseded by:** n/a
- **Links:** `Code/sepsis/core.py`, `Code/outputs/sepsis/core_prior.json`, DR-11, DR-12

### DR-14 · CV · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** Round 1 (SEQ-3): does the simple-first configuration, `Logistic + L2`, clearly beat the baseline under the agreed nested cross-validation?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Baseline (flag nobody), per outer fold | PR-AUC val 0.0313 (folds 0–3, 8, 9) and 0.0317 (folds 4–7): each fold's positive rate | CV | `Code/outputs/sepsis/core_cv_store.json` |
| `Logistic + L2`, per outer fold: tuned λ · PR-AUC train · PR-AUC val · converged | 0: 10⁻² · 0.0943 · 0.0841 · yes; 1: 10⁻³ · 0.0949 · 0.1017 · yes; 2: 10⁻² · 0.0940 · 0.0913 · yes; 3: 10⁻³ · 0.0981 · 0.0774 · yes; 4: 10⁻³ · 0.0987 · 0.0778 · yes; 5: 10⁻³ · 0.0989 · 0.0782 · yes; 6: 10⁻² · 0.0902 · 0.1230 · yes; 7: 10⁻³ · 0.0966 · 0.0969 · yes; 8: 10⁻³ · 0.0959 · 0.1126 · yes; 9: 10⁻³ · 0.0980 · 0.0870 · yes | CV | `Code/outputs/sepsis/core_cv_store.json` |
| Tuned λ | 10⁻³ in 7 of 10 outer folds, 10⁻² in 3; never at an edge of the grid (10⁻⁴ or 10⁴) | CV | `Code/outputs/sepsis/core_cv_store.json` |
| Convergence | all 10 outer refits converged (0 folds not converged) | CV | `Code/outputs/sepsis/core_cv_round1.json` |
| Mean PR-AUC recomputed from the ten fold values | 0.0930, the same as the core's table | CV | the per-fold values above |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §14 SEQ-3 | baseline and simple-first first | [B pp.331–332] | round 2 only once `Logistic + L2` clearly beats the baseline |
| §16 protocol | outer 10 / inner 5 folds, stratified by outcome × hospital, `CV_SEED` 2026; inner grid search on PR-AUC | [B pp.72–73]; [I]; [I] (further-variable rule) | as agreed in DR-13 |
| §17 C2 | margin 0.0615 ≥ 1 × spread 0.0156: clear | [I] threshold | `Logistic + L2` clearly beats the baseline; DX-1 not triggered |
| §16 diagnosis errors, P10 = imbalanced | E = 1 − PR-AUC | [B→I p.91] + [I] | E_train, E_val below |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear if margin ≥ 1 × spread | 1 × 0.0156 = 0.0156 | 0.0615 |
| §16 outer / inner folds | 10 / 5 | — |

**CV table** (outer 10, inner 5, stratified by outcome × hospital, seed 2026; metric PR-AUC as average precision)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean PR-AUC | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (flag nobody) | no | — | 0.0315 | 0.0002 | −0.0615 (0.0156) | — | 0.9685 | 0.9685 |
| `Logistic + L2` | no | λ = 10⁻³ (7 of 10 folds) | 0.0930 | 0.0156 | leader | +0.0615 (0.0156), C2 clear | 0.9040 | 0.9070 |

- **Options considered:** none: SEQ-3 fixes what round 1 runs
- **Expectation:** that `Logistic + L2` would be above the baseline (DR-13). Outcome: it is, by 0.0615 PR-AUC, about 3.9 times the spread.
- **Decision:** `Logistic + L2` clearly beats the baseline (C2 = clear), so DX-1 is not triggered and round 2 may go ahead when the user asks.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `run_cv` via `cd Code && uv run python sepsis/core.py cv round1 sepsis/props_dr11.json` · version: interim core, not reviewed, SHA-256 `dbae21d4e80f8a31b7b75addd2c359bab47a82c12ffb969ea67c2c3b7cc9b5bc` (approved at 4b) · inputs: DR-11 property values; the training table (`train_table.csv.gz` SHA-256 `44d64dd4…`, recorded in the store); `CV_SEED` 2026 · output: `Code/outputs/sepsis/core_cv_round1.json` and `core_cv_store.json` (per-fold values and each patient's outer fold), copied above unchanged, rounded to 4 decimals. Run time about 2 minutes.

- **Confidence:** n/a (computed at 4f)
- **Outcome vs expectation:** agree (round 1 only; the order of all four is compared at 4d)
- **User involvement:** asked for round 1 only, with round 2 not started
- **Supersedes / superseded by:** n/a
- **Links:** `Code/sepsis/core.py`, `Code/outputs/sepsis/core_cv_round1.json`, `Code/outputs/sepsis/core_cv_store.json`, DR-13

### DR-15 · CV · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** Round 2 (§15, SEQ-3): how do the remaining kept configurations — `Tree`, `Logistic + poly + L2`, `kNN` — do on the same folds?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `Tree`, per outer fold: tuned depth / min leaf · PR-AUC train · PR-AUC val | 0: 4/20 · 0.0970 · 0.0670; 1: 6/5 · 0.1468 · 0.0572; 2: 6/20 · 0.1242 · 0.0615; 3: 4/20 · 0.0953 · 0.0731; 4: 5/10 · 0.1145 · 0.0530; 5: 6/5 · 0.1604 · 0.0524; 6: 8/20 · 0.1706 · 0.0874; 7: 4/10 · 0.0943 · 0.0977; 8: 5/20 · 0.1136 · 0.0680; 9: 5/5 · 0.1196 · 0.0604 | CV | `Code/outputs/sepsis/core_cv_store.json` |
| `Logistic + poly + L2`, per outer fold: λ / degree · PR-AUC train · PR-AUC val · converged | 0: 10⁻²/2 · 0.0947 · 0.0877 · yes; 1: 10⁻²/2 · 0.0953 · 0.0887 · yes; 2: 10⁻³/3 · 0.1077 · 0.0797 · yes; 3: 10⁻³/3 · 0.1067 · 0.0846 · yes; 4: 10⁻⁴/2 · 0.1030 · 0.0756 · yes; 5: 10⁻³/2 · 0.1030 · 0.0729 · yes; 6: 10⁻³/3 · 0.1008 · 0.1283 · yes; 7: 10⁻³/2 · 0.0993 · 0.1041 · yes; 8: 10⁻⁴/2 · 0.0999 · 0.1071 · yes; 9: 10⁻³/3 · 0.1066 · 0.0785 · yes | CV | `Code/outputs/sepsis/core_cv_store.json` |
| `kNN`, per outer fold: k · PR-AUC train · PR-AUC val | 0: 51 · 0.1216 · 0.0694; 1: 51 · 0.1199 · 0.0747; 2: 51 · 0.1194 · 0.0686; 3: 51 · 0.1200 · 0.0642; 4: 51 · 0.1217 · 0.0621; 5: 51 · 0.1260 · 0.0519; 6: 51 · 0.1158 · 0.1006; 7: 51 · 0.1170 · 0.0909; 8: 51 · 0.1196 · 0.0631; 9: 51 · 0.1230 · 0.0601 | CV | `Code/outputs/sepsis/core_cv_store.json` |
| Hyperparameters at a grid edge | `kNN`: k = 51, the largest in the grid, in 10 of 10 folds. `Logistic + poly + L2`: λ = 10⁻⁴, the smallest, in 2 of 10. `Tree`: depth never at an edge (4–8); minimum leaf 20, the largest, in 5 of 10 | CV | `Code/outputs/sepsis/core_cv_store.json` |
| Convergence | all `Logistic + poly + L2` refits converged; `Tree` and `kNN` have no iterative fit | CV | `Code/outputs/sepsis/core_cv_round2.json` |
| Means recomputed from the ten fold values | `Tree` 0.0678, `Logistic + poly + L2` 0.0907, `kNN` 0.0706, as in the core's table | CV | the per-fold values above |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §14 SEQ-3 | round 2 run because `Logistic + L2` clearly beat the baseline (DR-14) | [B pp.331–332] | — |
| §16 protocol | the same stored outer folds as round 1 (checked against the training table's checksum and each patient's fold) | [B pp.72–73]; [I] | margins are paired by fold |
| §17 C2 | `Tree`, `Logistic + poly + L2`, `kNN` all clear | [I] threshold | all four configurations clearly beat the baseline |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear if margin ≥ 1 × spread | 1 × spread | `Tree` 0.0363 vs 0.0148; `Logistic + poly + L2` 0.0593 vs 0.0174; `kNN` 0.0391 vs 0.0147 |

**CV table** (all configurations; outer 10, inner 5, stratified by outcome × hospital, seed 2026; metric PR-AUC as average precision)

| Configuration | Post-prior | Tuned hyperparameters (most common) | CV mean PR-AUC | Fold SD | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic + L2` | no | λ = 10⁻³ (7 of 10) | 0.0930 | 0.0156 | leader | +0.0615 (0.0156), clear | 0.9040 | 0.9070 |
| `Logistic + poly + L2` | no | λ = 10⁻³, degree 3 (4 of 10) | 0.0907 | 0.0174 | −0.0023 (0.0077) | +0.0593 (0.0174), clear | 0.8983 | 0.9093 |
| `kNN` | no | k = 51 (10 of 10) | 0.0706 | 0.0148 | −0.0225 (0.0118) | +0.0391 (0.0147), clear | 0.8796 | 0.9294 |
| `Tree` | no | depth 4, min leaf 20 (2 of 10) | 0.0678 | 0.0148 | −0.0252 (0.0151) | +0.0363 (0.0148), clear | 0.8764 | 0.9322 |
| Baseline (flag nobody) | no | — | 0.0315 | 0.0002 | −0.0615 (0.0156) | — | 0.9685 | 0.9685 |

- **Options considered:** none: §15 fixes what round 2 runs
- **Expectation:** DR-13: the two logistic configurations at the top, close; then `Tree`; `kNN` last; all above the baseline.
- **Outcome vs expectation:** partial — top two and all above the baseline as expected; `kNN` above `Tree`, the reverse of the expected order (DR-13). Recorded as found.
- **Decision:** the leader is `Logistic + L2` (0.0930). Round 2 is complete; the diagnosis loop (4e) starts with the leader when the user asks. The grid edges above are recorded as facts; whether O5 holds is checked by the core in 4e for the leading configuration.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

**Reference code**

- Function: `run_cv` via `cd Code && uv run python sepsis/core.py cv round2 sepsis/props_dr11.json` · version: interim core, not reviewed, SHA-256 `dbae21d4e80f8a31b7b75addd2c359bab47a82c12ffb969ea67c2c3b7cc9b5bc` (approved at 4b) · inputs: DR-11 property values; the training table (`44d64dd4…`); the stored folds from round 1; `CV_SEED` 2026 · output: `Code/outputs/sepsis/core_cv_round2.json` and `core_cv_store.json`, copied above unchanged, rounded to 4 decimals. Run time about 35 minutes.

- **Confidence:** n/a (computed at 4f)
- **Outcome vs expectation:** partial (see above; DR-13 updated)
- **User involvement:** asked to continue to round 2
- **Supersedes / superseded by:** n/a
- **Links:** `Code/sepsis/core.py`, `Code/outputs/sepsis/core_cv_round2.json`, `Code/outputs/sepsis/core_cv_store.json`, DR-13, DR-14

### DR-16 · DX · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** Diagnosis pass 1 (§18) on the leading configuration, `Logistic + L2`: which observation holds first, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Errors (1 − PR-AUC, §16, P10 = imbalanced) | E_train 0.9040, E_val 0.9070, gap 0.0029 | CV | `Code/outputs/sepsis/core_diagnose_Logistic___L2.json` |
| Learning curve, E_val mean (fold SD) at 10 %, 20 % … 100 % | 0.9250 (0.0130), 0.9165 (0.0122), 0.9126 (0.0123), 0.9139 (0.0117), 0.9119 (0.0105), 0.9104 (0.0144), 0.9093 (0.0152), 0.9084 (0.0161), 0.9072 (0.0153), 0.9070 (0.0156) | CV | same |
| Learning curve, E_train mean at 10 % … 100 % | 0.8366, 0.8684, 0.8864, 0.8957, 0.8979, 0.8989, 0.9013, 0.9028, 0.9040, 0.9040 | CV | same |
| E_train ÷ gap for every configuration (from the CV table; computed by the agent, not a core output) | `Logistic + L2` 306.9; `Logistic + poly + L2` 81.8; `kNN` 17.6; `Tree` 15.7. O4's test (E_train ≥ 2 × gap) holds for all four; O3's (gap ≥ 2 × E_train) for none | CV | `Code/outputs/sepsis/core_cv_round2.json` |
| First run | stopped at the 70 % learning-curve point: a joblib worker process died (`OSError: [WinError 6] The handle is invalid`, `BrokenProcessPool`); no output was written. Re-run unchanged with the same core; the 10 %–60 % points of the first run equal those of the re-run | — | Analysis Log row 27 |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 = clear (DR-14) |
| O2 training error above what the application needs | no | E_train 0.9040 < 1 − (training positive rate 0.0315 + fold SD 0.0156) = 0.9529 (interpretation o) |
| O5 tuned hyperparameter at a grid edge | no | λ at an edge in 0 of 10 folds |
| O3 overfitting | no | gap 0.0029 < 2 × E_train |
| **O4 underfitting** | **yes** — first that holds | E_train 0.9040 ≥ 2 × gap 0.0059 |
| O6 more data likely to help | no | C3 adequate: E_val(80 %) − E_val(100 %) = 0.0015 < 0.5 × 0.0156 |

- **Action:** DX-5 (O4), more flexibility `[B pp.333–334]`. Its three parts: (i) add polynomial terms only if P3 = few — P3 = many, so not taken; `Logistic + poly + L2` has in any case been compared (DR-15, within noise of the leader); (ii) add k-NN or Tree if not already compared — both were compared in round 2, so nothing to add; (iii) ask whether more input variables exist — this needs the user, so the loop stops here. DX-9 `[B p.334]`: E_train ≫ gap, so more data is not suggested, consistent with O6 not holding.
- **The open point from Analysis Log row 11 applies:** on the 1 − PR-AUC scale E_train is large for any model that is not near perfect, and O4 holds for every configuration compared, including the most flexible (`Tree`, `kNN` with gaps of 0.056 and 0.050). Row 11 asked for this to be raised as a `FRAMEWORK` question with the evidence if it happened; it is raised with the user now. The agent does not change the rule or skip the observation (§7).

**Stopping check**

- S1 (criterion met): not assessed until 4g, as in the Heart Failure analysis. S2 (achievable level): unknown (DR-05). S3 (two passes without gain): first pass. S4 (out of scope): not yet. S5 (user stops it): applies — asked whether more input variables exist, the user chose "No new inputs; stop the loop". S6 (five passes): no. The loop stops under S5 after one pass.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 overfitting: gap ≥ 2 × E_train | 2 × 0.9040 = 1.8081 | 0.0029 |
| O4 underfitting: E_train ≥ 2 × gap | 2 × 0.0029 = 0.0059 | 0.9040 |
| O5 edge in most folds | > 5 of 10 | 0 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0078 | 0.0015 |

- **Options considered:** the three parts of DX-5, above. Put to the user for part (iii), without a recommendation: no new inputs, stop the loop; richer summaries of hours 1–6 (DR-09 option C); restore columns dropped in step 1. For the O4 rule, without a recommendation: keep §18 as written; change it under `FRAMEWORK`; defer to after Sepsis.
- **Expectation:** none was stated to the user before this pass. Analysis Log row 11 (18 October) had anticipated that O4 might hold on the 1 − PR-AUC scale whatever the model; it did.
- **Decision:** O4 → DX-5. Parts (i) and (ii) do not apply; for part (iii) the user chose "No new inputs; stop the loop", so the loop ends under S5 with the four configurations as compared. On the O4 rule the user chose "Keep §18 as written": O4 stands as computed, and this record notes that on the 1 − PR-AUC scale it holds for all four configurations. The open point in Analysis Log row 11 is closed for this analysis.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a (no expectation stated; see above)
- **User involvement:** asked to start 4e; asked — DX-5 part (iii): "No new inputs; stop the loop"; the O4 rule: "Keep §18 as written" (later superseded: the user changed O4 under `FRAMEWORK` the same day)
- **Supersedes / superseded by:** superseded by DR-17 (pass 1 re-run under the `FRAMEWORK` change to §18 O4, 27 October 2026)
- **Links:** `Code/sepsis/core.py` (`observations`, `learning_curve`), `Code/outputs/sepsis/core_diagnose_Logistic___L2.json`, DR-15, Analysis Log row 11

### DR-17 · DX · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** Diagnosis pass 1 on `Logistic + L2`, re-run under the `FRAMEWORK` change to §18 O4 (`ML Guide.md` commit `0d68044`): which observation holds first, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Rule change | §18 O4, when P10 = imbalanced and errors are 1 − the deciding metric: the ratio test **and** E_train worse than what the application needs (the O2 comparison) | M | user, 27 October 2026; `ML Guide.md` §18, version note |
| Core change | `observations()` only: O4 = ratio test and O2 comparison; both parts reported. SHA-256 `dbae21d4…` → `10a7e36c…`. The CV results (DR-14, DR-15) do not use `observations()` and stand | — | `Code/sepsis/core.py` |
| Errors (1 − PR-AUC) | E_train 0.9040, E_val 0.9070, gap 0.0029 — identical to DR-16 | CV | `Code/outputs/sepsis/core_diagnose_Logistic___L2.json` |
| Learning curve | E_val at 10 % … 100 % identical to DR-16 (0.9250 … 0.9070); C3 adequate | CV | same |
| Difference from DR-16 | only O4: `holds` true → false (ratio test true, O2 comparison false); `first_that_holds` O4 → none | CV | `git diff` of the output file against commit `5e0915e` |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 = clear (DR-14) |
| O2 training error above what the application needs | no | E_train 0.9040 < 1 − (0.0315 + 0.0156) = 0.9529 |
| O5 grid edge | no | λ at an edge in 0 of 10 folds |
| O3 overfitting | no | gap 0.0029 < 2 × E_train |
| O4 underfitting | no | ratio test holds (E_train 0.9040 ≥ 2 × gap 0.0059) but the O2 comparison does not (0.9040 < 0.9529) |
| O6 more data likely to help | no | C3 adequate (0.0015 < 0.5 × 0.0156) |

- **Action:** none of O1–O6 holds. §18 sends the loop to DX-7 (error analysis with the user) only if the success criterion is not met; that criterion is stated on the test set and is not assessed until 4g (as in DR-16 and the Heart Failure analysis), so whether DX-7 applies is put to the user. DX-9: no action is suggested that it rules out.

**Stopping check**

- S1 (criterion met): not assessed until 4g. S2 (achievable level): unknown (DR-05). S3 (two passes without gain): first pass. S4 (out of scope): no. S5 (user stops it): applies — the user chose "Stop the loop (S5), go to 4f". S6 (five passes): no. The loop stops under S5 after one pass.

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3: gap ≥ 2 × E_train | 1.8081 | 0.0029 |
| O4 ratio: E_train ≥ 2 × gap | 0.0059 | 0.9040 |
| O4 / O2 comparison: E_train ≥ 1 − (training positive rate + fold SD) | 0.9529 | 0.9040 |
| O5 edge in most folds | > 5 of 10 | 0 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0078 | 0.0015 |

- **Options considered:** put to the user without a recommendation (whether DX-7's trigger, "criterion not met", applies before the test is a reading only the user can make): stop the loop (S5) and go to 4f; error analysis (DX-7) on up to 100 validation errors `[B pp.336–337]`; review DR-17 first.
- **Expectation:** stated in conversation before the re-run: O4 would no longer hold (E_train 0.9040 < 0.9529), and none of O1–O6 would; the errors and learning curve would be unchanged. Outcome: as expected.
- **Decision:** no observation holds. The user chose "Stop the loop (S5), go to 4f": the loop ends after one pass, with the four configurations as compared in DR-14 and DR-15. No error analysis was done.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | codes are assigned at 4f |

- **Confidence:** n/a
- **Outcome vs expectation:** agree
- **User involvement:** asked for the `FRAMEWORK` change and this re-run; asked — next step: "Stop the loop (S5), go to 4f"
- **Supersedes / superseded by:** supersedes DR-16
- **Links:** `Code/sepsis/core.py` (`observations`), `Code/outputs/sepsis/core_diagnose_Logistic___L2.json`, `ML Guide.md` §18, DR-16, Analysis Log row 11

### DR-18 · FINAL · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** Which configuration does the recommendation rule (§19) choose, how confident is the selection (§17), at which decision threshold, and — once the user approves — how does it do on the test set?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV results | the CV table of DR-15 (round 1 and 2, same folds) | CV | `Code/outputs/sepsis/core_cv_store.json` |
| Diagnosis | no observation holds; loop stopped (S5) | CV | DR-17 |
| Threshold trade-off | "F2, as in DR-05", chosen from three options without a recommendation (F2; F1; a fixed minimum recall) | M | user, 27 October 2026 |
| Recommendation | `Logistic + L2`, λ = 10⁻³ (the most common setting, 7 of 10 outer folds; interpretation r), decision threshold r = 0.040 | CV | `Code/outputs/sepsis/core_recommend.json` |
| Selection confidence | Low — C1 none (runner-up `Logistic + poly + L2`, margin 0.0023, spread 0.0077); C2 clear (margin over the baseline 0.0615, spread 0.0156); C3 adequate (E_val 80 % − 100 % = 0.0015 < 0.5 × 0.0156) | CV | same |
| Prior agreement | agree: the CV winner among the prior-kept configurations is `Logistic + L2`, the prior's first | CV | same |
| Grounding | 2 matrix entries, both `[B→I]`: P5 = inspectable → Logistic `[B→I p.347]`; P6 = yes → Logistic `[B→I pp.50, 53–54]` | — | same |
| Selection breadth | 4 configurations compared; the note (> 10) does not apply | — | same |
| Decision threshold, nested CV at r chosen inside each outer fold | r per outer fold 0.040, 0.045, 0.035, 0.040, 0.045, 0.035, 0.035, 0.040, 0.045, 0.040; F2 0.2204 (SD 0.0182), precision 0.0723 (SD 0.0050), recall 0.4582 (SD 0.0737) | CV | same |
| Final threshold, on all training patients' inner out-of-fold probabilities | 0.040 | CV | same |
| Uncertainty for 4g | SD of PR-AUC across the outer folds for `Logistic + L2`: 0.0156 `[B→I pp.71–73]` | CV | same |
| Training positive rate | 0.0315 (984 of 31,270) | T | same |

**§19 trace**

1. **Eligible** (C2 = clear; no must-haves in DR-11): `Logistic + L2` (+0.0615, spread 0.0156), `Logistic + poly + L2` (+0.0593, 0.0174), `kNN` (+0.0391, 0.0147), `Tree` (+0.0363, 0.0148) — all four.
2. **Candidates** (best CV mean, plus any within 0.5 × spread of it): `Logistic + L2` (0.0930, best); `Logistic + poly + L2` (0.0907; margin 0.0023 < 0.5 × 0.0077 = 0.0039).
3. **Choice** (fewest add-ons, then prior score, then CV mean): `Logistic + L2` (1 add-on, prior score +2) over `Logistic + poly + L2` (2 add-ons, prior score 0); decided at the first step, add-ons.
4. **Test once:** pending the user's approval (step 4g).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.1 eligible = C2 clear and every must-have met | all four eligible | [I] (C2 threshold) | — |
| §19.2 candidates within the noise margin | `Logistic + L2`, `Logistic + poly + L2` | [I] threshold 0.5 × spread | — |
| §19.3 fewest add-ons | `Logistic + L2` | [B p.332] | recommended |
| §17 C1, C2, C3 and the level rule | C1 none, C2 clear, C3 adequate → Low | [I]; C3 [B→I pp.334–336] + [I] | reported with its factors |
| §16 decision threshold (P6 = yes) | tuned after selection, maximising F2, nested | [B→I pp.53–54, 92–93] | r = 0.040 |
| Final hyperparameters (interpretation r) | the most common setting across the outer folds | [I] | λ = 10⁻³ |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C1 clear ≥ 1 × spread, moderate ≥ 0.5 × spread | 0.0077 / 0.0039 | 0.0023 → none |
| C2 clear ≥ 1 × spread | 0.0156 | 0.0615 |
| C3 limited if E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0078 | 0.0015 |
| §19 within noise < 0.5 × spread | 0.0039 | 0.0023 |
| Breadth note > 10 configurations | 10 | 4 |
| Threshold grid | 0.005 to 0.500, step 0.005 | chosen 0.040 |

- **Options considered:** the four eligible configurations; the threshold trade-off (F2, F1, a fixed minimum recall)
- **Expectation:** DR-13: the two logistic configurations close at the top, "quite possibly within noise"; no expectation about the choice or the confidence level was stated.
- **Decision:** recommend `Logistic + L2` with λ = 10⁻³ and decision threshold 0.040, selection confidence Low (C1 none). The test set is used only after the user approves.

**Why not** (all 14 structural configurations except the recommendation)

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] (DR-12) |
| `Logistic` | EXCL | MOD-2: 61 parameters, rank 60 (the three `Unit` columns and the intercept) [B→I pp.46–47, 65] (DR-12) |
| `Logistic + poly` | EXCL | MOD-2: 119 parameters, rank 118 [B→I pp.46–47, 65] (DR-12) |
| `Logistic + poly + L2` | SIMP | margin 0.0023 < 0.5 × spread 0.0077; 2 add-ons against the recommendation's 1 |
| `kNN` | OUTP | margin 0.0225, spread 0.0118 (≥ 1 × spread) |
| `Tree` | OUTP | margin 0.0252, spread 0.0151 (≥ 1 × spread) |

**Flags**

| Method | Chapter | Evidence | Status |
| --- | --- | --- | --- |
| Survival analysis | not covered in the book | patients who leave the ICU before hour 54 are counted as negatives (DR-07) | not applied, not tested |

**Reference code**

- Function: `recommend` (`cd Code && uv run python sepsis/core.py recommend sepsis/props_dr11.json`) · version: interim core, not reviewed, SHA-256 `10a7e36c200cdf52823fa78f5ea9f3e7c57d9c3580bdc7e24ecefdcfc19fd1b6` · inputs: DR-11 property values; the CV store (DR-14, DR-15); F2 as the threshold trade-off · output: `Code/outputs/sepsis/core_recommend.json`, copied above unchanged, rounded to 4 decimals. Run time about 20 minutes (learning curve and threshold tuning).

**Test-set result** — pending (step 4g, after the user's approval).

- **Confidence:** Low — C1 none · C2 clear · C3 adequate — rule: Low if C1 = none or C2 = not clear · prior agreement agree · grounding [B] 0 / [B→I] 2 / [I] 0 · breadth note n/a (4 compared)
- **Outcome vs expectation:** agree (choice as expected; the test result is pending)
- **User involvement:** asked — threshold trade-off: "F2, as in DR-05"; approved using the test set: "Approve: commit 4f, then test"
- **Supersedes / superseded by:** superseded by DR-20 (the same recommendation re-run under the core changed for DR-19, before the test set was evaluated)
- **Links:** `Code/sepsis/core.py` (`recommend`, `tune_threshold`), `Code/outputs/sepsis/core_recommend.json`, DR-12 to DR-17

### DR-19 · FORM · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** How are empty values of `Age`, `Gender` and `HospAdmTime` filled, now that a test patient has one?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| What was found | building the test table (`sepsis_12`, after the user's approval at 4f) stopped on its own check: one test patient has `HospAdmTime` empty in every hour of the stay. No training patient has `Age`, `Gender` or `HospAdmTime` empty. The script stopped before writing anything; no outcome was read | M | Analysis Log row 30 |
| DR-09 | fills empty last values of the 27 clinical columns with the training-fold median; it says nothing about the three constant inputs, which were never empty in training | M | DR-09 |
| Options put to the user, without a recommendation | training median inside the core (a core change: new SHA-256, superseding record, re-run `recommend`); training median written into the test table by `sepsis_12`; drop the patient from the test set (7,817) | M | conversation, 27 October 2026 |
| User's choice | "Training median, in the core" | M | user, 27 October 2026 |
| Core change | `preprocessor()`: `Age`, `Gender`, `HospAdmTime` now go through `SimpleImputer(strategy="median")` instead of passing through. SHA-256 `10a7e36c…` → `22353007…` | — | `Code/sepsis/core.py` |
| Check that training results cannot change | on the training patients, the new preprocessing equals the old exactly: over all 31,270 patients, and in each of the 10 outer folds (fitted on the training part, applied to the validation part); the design keeps its 60 columns in the same order | T | check run 27 October 2026 (Analysis Log row 30) |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Imputation builds in assumptions | training-fold median, now for the constant inputs too | [B p.345] | the one empty `HospAdmTime` gets the training median at test time |
| REQ-1 | the median is fitted inside the pipeline, on training data only | [B p.27] + [I] | — |
| Input design (§9) | decided with the user | [B p.18] | DR-09 extended |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** as above
- **Expectation:** no change to any training-data result; `recommend` re-run to match the new core version
- **Decision:** DR-09 stands, extended: empty `Age`, `Gender` and `HospAdmTime` are filled with the training(-fold) median, inside the pipeline.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** agree: the re-run of `recommend` under the new core differs from DR-18's output only in the version line (DR-20)
- **User involvement:** asked — "Training median, in the core"; approved the core change and the plan: "Approve and proceed"
- **Supersedes / superseded by:** supersedes DR-09
- **Links:** `Code/sepsis/core.py` (`preprocessor()`), `Code/sepsis_12_test_table.py`, DR-09

### DR-20 · FINAL · step 4

- **Sub-task:** 1
- **Date:** 2026-10-27
- **Question:** The recommendation of DR-18 under the core changed for DR-19, and its single evaluation on the test set: how does `Logistic + L2` do on new patients, and is the success criterion met?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Recommendation re-run | `recommend` with core `22353007…`: output identical to DR-18's in every value; only `core_version_sha256` differs | CV | `git diff` of `Code/outputs/sepsis/core_recommend.json` against `c13b934` |
| Recommendation, threshold, confidence | as DR-18: `Logistic + L2`, λ = 10⁻³, threshold 0.040; selection confidence Low (C1 none, C2 clear, C3 adequate); prior agreement agree; grounding 2 `[B→I]` | CV | `Code/outputs/sepsis/core_recommend.json`; DR-18 |
| User's approval to use the test set | "Approve: commit 4f, then test"; after the DR-19 change: "Approve and proceed" | M | user, 27 October 2026; quoted in `core_final.json` |
| Test table | 7,818 test patients (A 3,895, B 3,923), 246 positive; built with the training table's construction, which was first shown to rebuild the stored training table exactly; one empty `HospAdmTime`, filled by the core with the training median (DR-19); log inputs all > 0, `Unit` levels all known | M | `Code/outputs/sepsis/12_test_table.json`; test table SHA-256 `4f1dd8d3…` |
| Final fit | `Logistic + L2`, λ = 10⁻³, refitted on all 31,270 training patients | — | `Code/outputs/sepsis/core_final.json` |
| **Test PR-AUC** (average precision) | **0.0847** (`0.08468650120390753`) | TEST | same |
| Uncertainty | SD of PR-AUC across the outer folds, 0.0156 `[B→I pp.71–73]`; n_test 7,818, 246 positives. Each outer fold holds about 3,127 patients, while the test set holds 7,818, so this spread approximates the test result's uncertainty rather than measuring it (step 4g) | CV / TEST | same; DR-14 |
| Baseline (flag nobody) on the test set | PR-AUC 0.0315 (the test positive rate, `0.031465848042977744`); F2 0, recall 0, precision undefined | TEST | same |
| At the decision threshold 0.040 | F2 0.2326, precision 0.0764, recall 0.4756; confusion matrix TP 117, FP 1,414, FN 129, TN 6,158 | TEST | same |
| Success criterion (DR-05) | test PR-AUC > test positive rate + fold SD: 0.0847 > 0.0315 + 0.0156 = 0.0471 → met | TEST | same |
| Independent recomputation | from the saved test predictions, with separate scikit-learn calls: PR-AUC 0.084687, F2 0.232604, precision 0.076421, recall 0.475610, the same confusion matrix; the recomputed predicted classes equal the saved ones | TEST | `Code/outputs/sepsis/private/core_test_predictions.csv.gz` (not in git) |
| CV estimate for comparison | `Logistic + L2` mean PR-AUC 0.0930, fold SD 0.0156 (DR-14); at the threshold, F2 0.2204, precision 0.0723, recall 0.4582 (DR-18) | CV | DR-14, DR-18 |
| Precision–recall curve | computed on the test set (§5.5 calls for it when classes are imbalanced, p. 92) | TEST | `Code/outputs/sepsis/core_final.json` (`pr_curve`) |

**§19 trace**

1. **Eligible:** all four configurations (C2 clear).
2. **Candidates:** `Logistic + L2` (0.0930), `Logistic + poly + L2` (0.0907; margin 0.0023 < 0.5 × 0.0077).
3. **Choice:** `Logistic + L2`, fewer add-ons (1 against 2).
4. **Test once:** test PR-AUC 0.0847 against the baseline's 0.0315 on the same 7,818 patients; success criterion met (required > 0.0471).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.4 test once | evaluated once, refitted on all training patients | [B pp.74, 328] | the test set is not used again for this sub-task |
| SEQ-1 baseline reported beside the result | flag nobody, PR-AUC 0.0315 | [B pp.330–331] | — |
| Uncertainty of the test result (step 4g) | fold SD 0.0156, with n_test and positives | [B→I pp.71–73] | — |
| §5.5 precision–recall curve for imbalanced classes | computed | [B→I p.92] | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Success: test PR-AUC > positive rate + fold SD | 0.0471 | 0.0847 |
| Decision threshold | 0.040 | — |

- **Options considered:** as DR-18
- **Expectation:** DR-13 expected `Logistic + L2` above the baseline; no test-set expectation was stated.
- **Decision:** sub-task 1 is answered by `Logistic + L2` (λ = 10⁻³, threshold 0.040): test PR-AUC 0.0847 (fold SD 0.0156; 7,818 test patients, 246 positive) against 0.0315 for flagging nobody; the success criterion is met. The test set is not used again for this sub-task.

**Why not** (all 14 structural configurations except the recommendation; as DR-18)

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` | EXCL | task gate, P1 = binary [B pp.17, 49–57] (DR-12) |
| `Logistic` | EXCL | MOD-2: 61 parameters, rank 60 [B→I pp.46–47, 65] (DR-12) |
| `Logistic + poly` | EXCL | MOD-2: 119 parameters, rank 118 [B→I pp.46–47, 65] (DR-12) |
| `Logistic + poly + L2` | SIMP | margin 0.0023 < 0.5 × spread 0.0077; 2 add-ons against 1 |
| `kNN` | OUTP | margin 0.0225, spread 0.0118 |
| `Tree` | OUTP | margin 0.0252, spread 0.0151 |

**Flags**

| Method | Chapter | Evidence | Status |
| --- | --- | --- | --- |
| Survival analysis | not covered in the book | patients who leave the ICU before hour 54 are counted as negatives (DR-07) | not applied, not tested |

**Reference code**

- Functions: `recommend` and `final` (`cd Code && uv run python sepsis/core.py recommend sepsis/props_dr11.json`; `… final --approved "…"`) · version: interim core, not reviewed, SHA-256 `223530074b4c9687c199965bfb79a980caa26ef3bbb07a50c96cb556bf693158` · inputs: DR-11 property values; the CV store; the test table (`4f1dd8d3…`) · outputs: `Code/outputs/sepsis/core_recommend.json`, `core_final.json`, `private/core_test_predictions.csv.gz`, copied above unchanged, rounded to 4 decimals.

- **Confidence:** Low — C1 none · C2 clear · C3 adequate — rule: Low if C1 = none or C2 = not clear · prior agreement agree · grounding [B] 0 / [B→I] 2 / [I] 0 · breadth note n/a (4 compared)
- **Outcome vs expectation:** agree (above the baseline, as DR-13 expected)
- **User involvement:** approved using the test set ("Approve: commit 4f, then test"; "Approve and proceed")
- **Supersedes / superseded by:** supersedes DR-18
- **Links:** `Code/sepsis/core.py` (`recommend`, `final`), `Code/sepsis_12_test_table.py`, `Code/outputs/sepsis/core_final.json`, `12_test_table.json`, DR-14 to DR-19

## Recommendation

### Sub-task 1 — Sepsis within 48 hours from the first 6 ICU hours

Assembled on 27 October 2026 from DR-01 to DR-20, at the user's recorded experience level (intermediate: terms used without definition, reasoning in full). Nothing in it is new; every number is from the core's outputs (`Code/outputs/sepsis/core_*.json`).

**1. Problem.** For each patient, predict from ICU hours 1–6 whether `SepsisLabel` switches on at hour 7–54, while the patient is still in the ICU (DR-05). Output binary (P1). Inputs: the DR-09 design — the last value in hours 1–6 of 27 vital signs and laboratory values (ten on a log scale, empty values filled with the training-fold median), a 0/1 "measured" indicator for each, `Age`, `Gender`, `HospAdmTime` (filled with the training median when empty, DR-19) and `Unit` (three levels); hospital is not an input. Deciding metric: PR-AUC, computed as average precision `[I]`; monitored: F2, precision and recall at a threshold tuned on training data (DR-05). Baseline: flag nobody, whose PR-AUC is the positive rate. Success criterion: test PR-AUC above the test positive rate by more than the fold SD of PR-AUC. Achievable level: unknown. Must-haves: none; P5 inspectable and P6 yes are preferences. P7 "no"; P8 "unknown" (DR-05, DR-11). ADM-1 yes (DR-01); ADM-2 predict (DR-04); ADM-3: one row per patient, patient is the group unit, hospital a second grouping (DR-02); ADM-4: yes for adult ICU patients at these two hospitals, unsure beyond (DR-03). Split: 20 % of patients held out, stratified by outcome × hospital, seed 2026: 31,270 training patients (984 positive) and 7,818 test patients (246 positive) (DR-08). Properties: P1 binary, P2 ample, P3 many, P4 high, P9 no, P10 imbalanced (DR-11).

**2. Recommendation.** `Logistic + L2` with λ = 10⁻³ (the most common tuned value, 7 of 10 outer folds) and decision threshold 0.040. Selection confidence: Low (DR-20).

**3. Test-set result.** PR-AUC = 0.0847 (fold SD 0.0156), n_test = 7,818 with 246 positive; baseline (flag nobody) 0.0315 on the same patients. Success criterion (test PR-AUC > 0.0315 + 0.0156 = 0.0471): met. Threshold 0.040, chosen after selection by nested cross-validation on the training patients to maximise F2, the user's trade-off (§16, DR-18). At that threshold: F2 0.2326, precision 0.0764, recall 0.4756; confusion matrix TP 117, FP 1,414, FN 129, TN 6,158. The test precision–recall curve is in `core_final.json` (§5.5). The test numbers were recomputed from the saved predictions by separate calls and agree. The fold SD comes from outer folds of about 3,127 patients against 7,818 in the test set, so it approximates the uncertainty of the test result rather than measuring it (DR-20).

**4. Why this configuration.**
- Constraints: the task gate (P1 = binary) left `Logistic`, `kNN` and `Tree` `[B pp.17, 49–57]`; no must-haves; MOD-1 did not apply (P9 = no); MOD-2 removed `Logistic` and `Logistic + poly`, because the three one-hot `Unit` columns sum to the intercept (rank 60 of 61), an encoding the user kept `[B→I pp.46–47, 65]` (DR-12). So `Logistic + L2` is the simple-first configuration (SEQ-2).
- CV evidence: margin over the runner-up, `Logistic + poly + L2`, 0.0023 (spread 0.0077); over the baseline 0.0615 (spread 0.0156) (DR-15, DR-18).
- Simplicity: decided by the §19 within-noise step. `Logistic + L2` and `Logistic + poly + L2` were both candidates (0.0023 < 0.5 × 0.0077); `Logistic + L2` has 1 add-on against 2 `[B p.332]`.
- Prior support: score +2 from P5 = inspectable → Logistic +1 `[B→I p.347]` and P6 = yes → Logistic +1 `[B→I pp.50, 53–54]` (DR-13).

**5. Ranking.** Outer 10 / inner 5 folds, stratified by outcome × hospital, seed 2026; PR-AUC (DR-14, DR-15).

| Configuration | Prior rank | Prior score | Post-prior | CV mean PR-AUC | Margin vs recommended (± spread) | Margin vs baseline (± spread) | Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic + L2` | 1 | +2 | no | 0.0930 | — | +0.0615 (0.0156) | recommended |
| `Logistic + poly + L2` | 3 | 0 | no | 0.0907 | −0.0023 (0.0077) | +0.0593 (0.0174) | SIMP |
| `kNN` | 4 | −2 | no | 0.0706 | −0.0225 (0.0118) | +0.0391 (0.0147) | OUTP |
| `Tree` | 2 | +1 | no | 0.0678 | −0.0252 (0.0151) | +0.0363 (0.0148) | OUTP |
| Baseline (flag nobody) | — | — | — | 0.0315 | −0.0615 (0.0156) | — | — |

**6. Prior versus evidence.** Prior agreement: agree — the cross-validation winner, `Logistic + L2`, is the prior's first (DR-18). Against the advisor's expectation of the order (DR-13), the outcome is partial: the two logistic configurations led, within noise of each other, as expected; `kNN` (0.0706) ranked above `Tree` (0.0678), the reverse of the expectation. The departure goes against the matrix entries that put `Tree` at +1 (P5 = inspectable → Tree `[B→I p.347]`) and `kNN` at −2 (P3 = many → k-NN `[I]`, P4 = high → k-NN `[I]`). The P5 entry concerns inspectability rather than accuracy, and the margin between the two is 0.0028 with spread 0.0088 (computed by the agent from the stored fold values, DR-13), so cross-validation does not tell the two apart.

**7. Why not the others.**
- EXCL: `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` — task gate, P1 = binary `[B pp.17, 49–57]`. `Logistic` — MOD-2, 61 parameters, rank 60. `Logistic + poly` — MOD-2, 119 parameters, rank 118 `[B→I pp.46–47, 65]` (DR-12).
- USER: none (no must-haves).
- DISF: none (all four admissible configurations kept, DR-13).
- BASE: none (all four clearly beat the baseline).
- OUTP: `kNN` — margin 0.0225, spread 0.0118; `Tree` — margin 0.0252, spread 0.0151.
- SIMP: `Logistic + poly + L2` — margin 0.0023 < 0.5 × spread 0.0077; 2 add-ons against 1.

Flags: survival analysis (not covered in the book) — patients who leave the ICU before hour 54 are counted as negatives, so their outcome after leaving is unknown (DR-07); not applied or tested.

**8. Confidence.** Selection confidence Low: C1 none (runner-up `Logistic + poly + L2`, margin 0.0023, spread 0.0077), C2 clear (margin over the baseline 0.0615, spread 0.0156), C3 adequate (E_val at 80 % minus at 100 % of the training data 0.0015, below 0.5 × 0.0156); rule: Low if C1 = none or C2 = not clear `[I]`. Prior agreement: agree. Grounding: [B] 0 · [B→I] 2 · [I] 0. Breadth note: does not apply (4 configurations compared) (DR-18, DR-20).

**9. How the model predicts** (draft; turned into prose in step 5). Logistic regression with L2: each patient's 60 design columns (DR-09, DR-19) are standardised, combined in a weighted sum with an intercept, and passed through the logistic function to give a probability that the label switches on within the period; the patient is flagged if that probability is above 0.040, the threshold that maximised F2 in cross-validation (§16). The L2 penalty, λ = 10⁻³, shrinks the weights towards zero `[B pp.60–61]`. The weights, on the log-odds scale, show the direction and relative size of each input's effect on the predicted probability, with the others fixed; they are not causal effects (§21). The fitted weights, from a verified rebuild of the final model (Analysis, sub-task 1; `core_weights.json`): intercept −3.6691; per 1 SD of each standardised column, the ten largest by size are `measured_FiO2` +0.2926, `measured_SBP` −0.2294, `measured_Calcium` +0.1940, `MAP` −0.1846, `HR` +0.1769, `Resp` +0.1682, `measured_WBC` +0.1649, `measured_MAP` +0.1443, `Unit_SICU` −0.1343 and `measured_Lactate` +0.1196. The three `Unit` weights are determined only relative to each other, because the columns sum to the intercept. Trust limits: the test PR-AUC is an average over patients like the test patients; it says nothing about the worst individual prediction, and it holds only while new patients resemble these `[B pp.329, 347]`.

**10. Use and limits** (draft; turned into prose in step 5). The model ranks adult ICU patients at the two hospitals by their predicted probability from the first six hours, for flagging for closer monitoring (DR-05). At the threshold, 7.6 % of flagged test patients had the label switch on (precision 0.0764) and 47.6 % of those whose label switched on were flagged (recall 0.4756). Limits, each beside what it qualifies: the outcome is a label constructed by rule (Sepsis-3), partly from the kinds of measurement that are inputs, and shifted 6 hours before onset (DR-01); patients who leave the ICU before hour 54 count as negatives (DR-07); whether it applies beyond these two hospitals is unknown (DR-03); the "measured" indicators partly reflect ordering habits and hospital practice, not only physiology (DR-09); `Magnesium`, `Lactate` and hospital B's `Calcium` peak may mix scales, and vitals are clipped (Data Summary, accepted as-is). The result is an average-case estimate with no worst-case bound.

**11. Improvement history.** Pass 1 on `Logistic + L2` (E as 1 − PR-AUC): E_train 0.9040, E_val 0.9070, gap 0.0029; C3 adequate. Under the first O4 rule, O4 held (ratio test) → DX-5, whose automatic parts did not apply (P3 = many; k-NN and Tree already compared) and whose remaining part, more input variables, the user declined (DR-16, superseded). After the `FRAMEWORK` change to O4 (`ML Guide.md`, `0d68044`), the same pass gave no observation holding: O4's ratio test held but its comparison with what the application needs did not (0.9040 < 0.9529) (DR-17). Stopped by S5: the user stopped the loop after one pass. No configuration was added after the prior.

**12. Thresholds applied.**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| MOD-2 exact collinearity (rank < columns) | numpy default tolerance | rank 60 of 61; 118 of 119 |
| §15 kept besides baseline and simple-first | 3 (+ ties) | 3 others admissible |
| §16 outer / inner folds | 10 / 5 | — |
| C2 clear: margin ≥ 1 × spread | 0.0156 | 0.0615 |
| C1: clear ≥ 1 ×, moderate ≥ 0.5 × spread | 0.0077 / 0.0039 | 0.0023 → none |
| §19 within noise: < 0.5 × spread | 0.0039 | 0.0023 |
| C3 limited: E_val(80 %) − E_val(100 %) ≥ 0.5 × fold SD | 0.0078 | 0.0015 |
| O3 / O4 ratio | 2 × E_train / 2 × gap | gap 0.0029; E_train 0.9040 |
| O4 / O2 comparison | E_train ≥ 0.9529 | 0.9040 |
| O5 grid edge in most folds | > 5 of 10 | 0 |
| Breadth note | > 10 configurations | 4 |
| Decision threshold grid | 0.005 to 0.500, step 0.005 | 0.040 |
| Success: test PR-AUC > positive rate + fold SD | 0.0471 | 0.0847 |
| P10 imbalanced: smallest class < 20 % | 20 % | 3.15 % |

**13. Trace and provenance.** DRs: DR-01 to DR-05 (admissibility, formulation), DR-07 (flag), DR-08 (split), DR-09 and DR-19 (input design), DR-11 (properties), DR-12 (admissible set), DR-13 (prior), DR-14 and DR-15 (CV), DR-16 and DR-17 (diagnosis), DR-18 and DR-20 (recommendation and test). Tags in the *Rules applied* tables of DR-12 to DR-20, counted each time a rule is applied: [B] 16 · [B→I] 11 · [I] 17 · UNLISTED 0. Earlier records carry `UNLISTED [I]` choices: PR-AUC as average precision (DR-05), outcome × hospital stratification (DR-08, since covered by §16), the logged labs and the last-value summary (DR-09).

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1. Created the analysis folder `Demonstration/Sepsis/` from the templates. The user chose the PhysioNet 2019 sepsis training data and stated intermediate ML experience. | `Demonstration/Sepsis/Report.md`, `Appendix.md` |
| 2 | Step 1, describing pass. Re-checked all 40,336 files against the SHA-256 lists (0 mismatches). Described shape, stays, label structure, every column's completeness and range, and the differences between sets A and B. Units and the label definition come from the PhysioNet page; hospitals, inclusion rules and binning from Reyna et al. (2020). No decisions taken. | `Code/outputs/sepsis/01_describe.json`, `01_describe.md` |
| 3 | Step 1, decisions. The user answered ADM-1, ADM-3 and ADM-4 (DR-01, DR-02, DR-03) and decided scope, missing data, cleaning and leakage. Counted, without applying anything: the rows and patients left after setting aside rows from label onset (426 septic patients lose every row), the `FiO2` unit check (fraction scale), and the values each candidate cleaning rule would change. Proposed a variable drop list (7 columns) and cleaning thresholds for the user's approval. | `Code/outputs/sepsis/02_scope_counts.json`, `02_scope_counts.md` |
| 4 | Step 1, decisions applied. The user approved dropping all seven columns under one rule (fewer than 10 % of patients in either hospital), and cleaning only clearly impossible values (`FiO2` outside [0.21, 1.0], `Temp` outside 25–45 °C, `Potassium` > 15, `Hgb` > 25). Not chosen: `Temp` 30–43 and `Potassium` > 10, which would also remove possible values. Calcium's low cluster, positive `HospAdmTime`, patients under 18 and `Age` = 100 are kept as-is and recorded. `ICULOS` is used only for ordering and time windows. Built the derived tables: 1,524,294 hours × 32 inputs; 39,910 patients with hours, 2,506 of whom later become septic. Cleaning changed 385 + 6 + 2 + 3 values, the same as row 3's counts. The positive-`HospAdmTime` count given to the user in conversation (64 rows) had not been computed and was wrong; the computed figure is 8,483 kept hours in 255 patients. Data Summary updated, and the dropped columns' descriptions removed. | `Code/outputs/sepsis/03_build_table.json`, `03_build_table.md`; `Code/outputs/sepsis/private/` (not in git) |
| 5 | Step 1 closed (16 October 2026). | — |
| 6 | Step 2. Counted, for a patient-level target from the first N ICU hours, the usable patients and positives for N = 6 and N = 12, by hospital (counts only, no model). The script was written in an earlier session before the framing was agreed; it is kept because the framing is used. The user answered ADM-2 (predict, DR-04), chose one prediction per patient from the first 6 hours with the outcome "label switches on within 48 hours after the window", and chose to mix both hospitals and split by patient. Hourly prediction (framing (b)) and training on one hospital and testing on the other were not taken; the latter may become a separate sub-task later. | `Code/outputs/sepsis/04_target_counts.json`, `04_target_counts.md` |
| 7 | Step 2. Counted, for N = 6 and H = 48, the patients whose outcome is not observed for the full 48 hours (counts only, no model). Of the 39,088 patients in the cohort: 1,230 positive (label switches on at hour 7–54); 4,842 negatives observed to hour 54 (3,892 never septic with a record reaching hour 54, 950 whose label switches on after hour 54); 33,016 never-septic patients whose record ends before hour 54 (median last hour 37, quartiles 24 and 44; 12,554 end by hour 30). Kept as negatives: 39,088 rows, 3.15 % positive (A 4.01 %, B 2.29 %). Excluded: 6,072 rows, 20.26 % positive (A 23.37 %, B 16.46 %). The 46 positives whose kept record ends at hour 6 are counted as positives. Proposal put to the user; decision pending. | `Code/outputs/sepsis/05_horizon_counts.json`, `05_horizon_counts.md` |
| 8 | Step 2. The user decided: patients who leave before hour 54 are kept as negatives (limitation; FLAG for survival analysis, DR-07); PR-AUC decides, with F2, precision and recall at a threshold tuned on training data monitored; baseline flag nobody, with the positive rate as the no-skill reference; success = test PR-AUC above the no-skill level by more than the outer-fold spread; achievable level unknown; P5 inspectable and P6 yes as preferences, P7 no, P8 unknown; test 20 %, by patient, stratified by outcome and hospital, seed 2026. An earlier set of answers (90 / 10, seed 42, ROC-AUC monitored, calibrated probabilities) was replaced by the user before anything was recorded. The choices were checked against the book and the guide. No conflict was found. Points raised with the user: how PR-AUC is computed (average precision proposed, `[I]`, open); the baseline's PR-AUC equals the no-skill reference; "strong" preference has no separate effect in the guide; §16 stratifies folds by outcome only; and §16 computes the diagnosis-loop errors E_train and E_val as the misclassification rate, which the book says misleads for imbalanced classes (p. 91) — a possible FRAMEWORK question before step 4e. Problem Definition written; DR-05 FORM, DR-06 PROP, DR-07 FLAG. Test set not yet split or locked. | `Demonstration/Sepsis/Appendix.md` |
| 9 | Step 2. The user confirmed: PR-AUC computed as average precision `[I]`; baseline and no-skill reference kept as recorded; P5 a preference; cross-validation folds stratified by outcome and hospital, like the test split; the diagnosis-loop error measure to be raised as a FRAMEWORK change after step 2 closes. `sepsis_05_horizon_counts.py` refactored so its cohort is a function (`build_cohort`) the split also uses; re-run, output byte-identical. Made the split with `sepsis_06_split.py`: 31,270 training patients (984 positive, 3.15 %) and 7,818 test patients (246 positive, 3.15 %), the same positive share in each hospital in both parts (A 4.01 %, B 2.29 %). Re-run gives the same checksum. Test set locked (DR-08). | `Code/outputs/sepsis/06_split.json`, `06_split.md`; `Code/outputs/sepsis/private/cohort.csv.gz` (not in git) |
| 10 | Step 2. Wrote the problem and its sub-task into the `Introduction` of `Report.md`. Step 2 closed (18 October 2026). | `Demonstration/Sepsis/Report.md` |
| 11 | After step 2, `FRAMEWORK` change to `ML Guide.md` §16 and §18 (commit `ddda293`). What prompted it: with 3.15 % positives, flagging nobody already has a misclassification rate of about 3 %, so diagnosis-loop errors measured that way would say almost nothing about over- or underfitting, and the book warns that the misclassification rate misleads for imbalanced classes (p. 91). Now, when P10 = imbalanced, E_train, E_val and the learning curve (and so C3) are measured as 1 − the deciding metric, here 1 − PR-AUC. The user kept the `[I]` ratios for O3 and O4 unchanged. Open point: on the 1 − PR-AUC scale E_train is large for any model that is not near perfect, so O4 (underfitting, E_train ≥ 2 × gap) may fire too often; if it does in step 4e, raise it as a `FRAMEWORK` question with the evidence. No Sepsis record is affected: no interim core or cross-validation exists yet. | `ML Guide.md` |
| 12 | Step 3 started (18 October 2026). Proposed four input designs (last value, mean, min/max, measured indicators), three ways of filling empty values, logarithms on ten labs, `Unit` as one category and hospital as a possible input, with their trade-offs and the book's pp. 18, 331, 345–346; and four figures. The user chose last value + indicators, training-fold median, the ten logs, `Unit` in three levels, hospital not an input, and figures 1–3 (not figure 4, inputs by outcome) (DR-09). Built the training table from the training patients only: 31,270 patients, 984 positive, 58 input columns (60 after encoding); 38 patients have no clinical value in hours 1–6. Wrote the interim core `Code/sepsis/core.py` (input design and P9–P10 only), SHA-256 `43af578e16c91ab05f0f1ce439acf92aa6a21811669d7d2e92368eb0963b30b7`; shown to the user before it is run. | `Code/outputs/sepsis/07_train_table.json`, `07_train_table.md`; `Code/outputs/sepsis/private/train_table.csv.gz` (not in git); `Code/sepsis/core.py` |
| 13 | Step 3. The user approved the core, its interpretations (a)–(c), and counting the 27 indicators as categorical (pp. 16–17). Ran `sepsis/core.py p9p10` on the training patients: P9 = no (training accuracy 0.9685 with negligible regularisation), P10 = imbalanced (3.15 %). With the input design fixed: P2 ample (512.6), P3 many (60), P4 high (29 of 58 = 50.0 %, exactly at the threshold). DR-10 PROP supersedes DR-06. | `Code/outputs/sepsis/core_p9_p10.json` |
| 14 | Step 3. Made the agreed figures from the training patients only, light and dark: coverage by hospital (Figure 1), last-value distributions split into vitals (Figure 2) and labs (Figure 3) so the type stays readable, and label-onset hour by hospital (Figure 4). Colours fixed per variable: hospital A blue, B orange, all training patients green; validated with the palette checker (light: green below 3:1 contrast, used only for filled bars with labelled axes). Fixed overlapping tick labels on the log axes before showing them. Shown to the user before adding to `Results`. | `Code/outputs/sepsis/figures/` |
| 15 | Step 3. The user approved all four figures and captions; added to `Results` in `Report.md` with a line saying they describe the training patients only. Captions checked against `fig1_coverage.json`, `fig2_3_distributions.json` and `fig4_onset.json`. No figure prompted a change to P8, which stays `unknown` (DR-10). Step 3 closed (18 October 2026). | `Demonstration/Sepsis/Report.md` |
| 16 | After step 3. Added `Code/*/core.py -text` to `.gitattributes` (commit `499525a`), so the Sepsis core is checked out byte for byte; a fresh checkout gives the recorded SHA-256 `43af578e…`. Gave the user, in conversation only, a recommendation on Figures 2 and 3; the figures were kept unchanged. At the user's request, counted in the training table two points it raised: (a) last `Calcium` values below 2.0 mg/dL (the gap in the data): 1,763 of 12,386 training patients with a value (14.23 %), all in hospital B (23.60 % of B's 7,469; A 0 of 4,917); between 1.75 and 3.5 the count changes by at most 10. Options put to the user; decision pending. (b) `PTT` stops at exactly 150 s in A (78 patients) and 250 s in B (4 patients): recorded as accepted as-is, with the clipped vitals (Data Summary). | `Code/outputs/sepsis/11_calcium_ptt_counts.json`, `11_calcium_ptt_counts.md` |
| 17 | After step 3. The user chose to set `Calcium` below 2.0 mg/dL to missing as a step 1 cleaning rule (not yet applied), and asked first for the bump around 4–5 mg/dL to be counted by hospital, so the rule's scope is fixed before the re-runs. Added 0.25 mg/dL bins from 2 to 8 by hospital to `sepsis_11_calcium_ptt_counts.py` (earlier numbers unchanged). Training patients' last `Calcium` in (2.0, 5.5]: A 12 of 4,917, B 317 of 7,469; B has a separate peak in (4.0, 5.25] (271 patients) and a trough in (5.5, 6.25] (36) before its main distribution; A has no such peak. Scope decision pending. | `Code/outputs/sepsis/11_calcium_ptt_counts.json` (`calcium_bins_2_to_8_by_set`) |
| 18 | `FRAMEWORK` change to `ML Guide.md` §16 (commit `531ec49`), 27 October 2026. What prompted it: in step 2 the user chose to stratify the cross-validation folds by outcome and hospital, like the test split (row 9, DR-08), but §16 allowed only stratification by outcome, so DR-08 recorded the choice as `UNLISTED [I]`. §16 now has a rule: when the test split was stratified by a further variable as well as the outcome, the outer and inner folds are stratified by the same combination; group folds (ADM-3) take precedence when rows share a unit `[I]`. No threshold added. Nothing to re-run: no cross-validation has been run for this analysis, and the interim core `Code/sepsis/core.py` (SHA-256 `43af578e…`) has no fold code yet; DR-08 stays valid for what it records, and step 4 records will cite the §16 rule. | `ML Guide.md` §16 and version note |
| 19 | `FRAMEWORK` change to `instructions.md` step 4g (commit `0c2aac4`) and `ML Guide.md` §5.2 (commit `ba78a84`), 27 October 2026. What prompted it: the open item in `Note for Florentine.md`; §5.2 called the uncertainty of the test result an open decision, while step 4g already fixed it as the standard deviation of the agreed metric across the outer folds `[B→I pp.71–73]`. §5.2 now states that method, says the bootstrap (Chapter 8) and binomial intervals are not used, and both documents add a limitation: the outer folds and the test set differ in size, so the fold spread approximates the uncertainty of the test result rather than measuring it. The method is unchanged, so no Decision Record is affected: DR-05's success criterion and its uncertainty row already use the SD of PR-AUC across the outer folds, as defined in step 4g. Here each outer fold holds about 3,127 of the 31,270 training patients and the test set 7,818 (DR-08); the limitation will be stated with the result in step 4g. Nothing to re-run: no cross-validation has been run. | `instructions.md` step 4g; `ML Guide.md` §5.2, §25.2 and version note |
| 20 | `FRAMEWORK` change to `instructions.md`, `Step-by-Step Working` (commit `492bfea`), 27 October 2026, at the user's request. The agent does all the coding and the user decides, approves and directs (installing the workspace per `Setup.md` excepted); every decision that is the user's to make is put as 2 to 4 numbered options with one-line trade-offs and book pages, plus "Something else", recommending only where the contract allows; one decision per question; at the end of a step the written completeness check comes first and the options carry no recommendation; the problem, the experience level and any P8 expectation stay open questions, in the user's words. Checked against the contract: four clashes found (step closure, P8 named in two bullets, "every decision" against the agent's own writing and the diagnosis loop, `Setup.md`); the user chose a resolution for each, written into the rule. Effect on this analysis: none on the records. The user has not been asked to write or run code, and the answers already recorded keep their wording. From now on, decisions are put as options, starting with the pending scope of the `Calcium` rule (rows 16–17). | `instructions.md`, `Step-by-Step Working` |
| 21 | After step 3, 27 October 2026. Scope of the `Calcium` rule decided, put as four options without a recommendation (the evidence did not settle whether B's values are wrong): below 2.0 mg/dL only; below 2.0 and B's (4.0, 5.25] peak; check the documentation first; leave as is. The user chose "below 2.0 mg/dL only": `Calcium` values below 2.0 mg/dL are set to missing as a step 1 cleaning rule, in every hour, for all patients; B's (4.0, 5.25] peak (271 training patients by last value) is kept. The agent's suggestion that some of B's values may be ionised rather than total calcium was given as context only; it is unverified and not a finding. Asked again later the same day with the same options, the user kept "below 2.0 mg/dL only". Applying it means re-running the pipeline from the table build. | — |
| 22 | After step 3, 27 October 2026. Applied the `Calcium` rule: added `"Calcium": (2.0, None)` to `CLEAN_RULES` in `sepsis_03_build_table.py` and re-ran `sepsis_03` to `sepsis_07`, the core (`p9p10`) and `sepsis_08` to `sepsis_10`; `sepsis_11` not re-run (user's choice: its outputs stay as the pre-rule record behind rows 16–17). Before → after: `Calcium` values set to missing 0 → 9,464 (A 1, B 9,463; 3,835 patients; all cleaning 396 → 9,860); training patients with a last `Calcium` value 12,386 → 10,967; `Calcium` coverage all 39.61 → 35.07 %, B 47.60 → 38.55 %, A 31.56 % unchanged; smallest last `Calcium` 1.0 → 2.05 mg/dL; P9 training accuracy 0.9685 → 0.9684 (iterations 30 → 28), still no; `hours.csv.gz` SHA-256 `f86128f3…` → `b0459127…`; `train_table.csv.gz` `fbc5c540…` → `44d64dd4…`. Unchanged, checked: the split (`cohort.csv.gz` `55dce9ca…`, as in `06_split.json`), `patients.csv.gz`, the outputs of `sepsis_04` to `sepsis_06`; training patients 31,270, positives 984, 58 input columns, 60 after encoding; P2–P4 and P10; the core (`43af578e…`); Figures 2 and 4 (byte-identical). Figures 1 and 3 regenerated (Calcium bar and panel); both captions checked against `fig1_coverage.json` and `fig2_3_distributions.json` and still correct. No property changed; the user chose a new record, DR-11, superseding DR-10, because DR-10's P9 evidence no longer matched its output. Data Summary: `Calcium` added under `Cleaning`, its `Accepted as-is` entry marked superseded, B's 4.0–5.25 peak added as accepted as-is, new `hours.csv.gz` checksum. | `Code/outputs/sepsis/03_build_table.json`, `07_train_table.json`, `core_p9_p10.json`, `figures/`; DR-11 |
| 23 | Step 4 started, sub-task 1 (27 October 2026); 4a, the admissible set. Checked the labels before 4a: nothing beyond the limitation already recorded in DR-01. Extended the interim core with §9 and §12 (`admissible_set`, `mod2_check`, interpretations d–f), SHA-256 `43af578e…` → `f505ef87…`, `p9_p10` unchanged; wrote the DR-11 values to `Code/sepsis/props_dr11.json`. Showed the extension to the user, who approved it before it was run. Result: task gate leaves `Logistic`, `kNN`, `Tree`; no must-haves; MOD-1 does not apply; MOD-2 applies because the three one-hot `Unit` columns sum to the intercept (rank 60 of 61, 118 of 119 with powers), the only collinearity. Put the `Unit` encoding to the user as three options without a recommendation; the user chose "Keep 3 columns (DR-09 as is)". Admissible: `Logistic + L2`, `Logistic + poly + L2`, `kNN`, `Tree` (DR-12). At the end of 4a the user asked to revisit whether P5 is a must-have; put as three options without a recommendation, the user kept "inspectable" as a preference, so DR-11 and DR-12 stand. | `Code/outputs/sepsis/core_admset.json`; DR-12 |
| 24 | Step 4b, sub-task 1 (27 October 2026). Extended the interim core with §13–§19 so the user's approval at 4b covers the whole core: prior ranking, nested CV with a stored fold assignment, diagnosis observations and learning curve, decision threshold, confidence, recommendation, why-not codes, and the single test-set evaluation (`final`, which needs the user's quoted approval and refuses a second run). Interpretations g–s added to the docstring; `preprocessor()` gained an optional `drop` argument (no change by default). Checked before showing it: it compiles, and each admissible configuration's pipeline runs on synthetic data; nothing was fitted on patients. SHA-256 `f505ef87…` → `dbae21d4…`; the user approved it, then `prior` was run: `Logistic + L2` +2 (simple-first), `Tree` +1, `Logistic + poly + L2` 0, `kNN` −2; all four kept, no `DISF` (DR-13, with the advisor's expectation of the CV order). Presented the property values, kept configurations, §16 protocol and the survival-analysis flag; the user agreed the method ("Agree; close 4b"). Step 4b closed. | `Code/outputs/sepsis/core_prior.json`; DR-13 |
| 25 | Step 4c, sub-task 1 (27 October 2026): cross-validation round 1 with the approved core (`dbae21d4…`), about 2 minutes. Baseline (flag nobody) mean PR-AUC 0.0315 (fold SD 0.0002); `Logistic + L2` 0.0930 (fold SD 0.0156), E_train 0.9040, E_val 0.9070; margin over the baseline +0.0615 with spread 0.0156, so C2 = clear and DX-1 is not triggered. Tuned λ 10⁻³ in 7 folds and 10⁻² in 3, never at a grid edge; all folds converged. Mean recomputed from the ten fold values: 0.0930, as in the core's table. Round 2 not started. | `Code/outputs/sepsis/core_cv_round1.json`, `core_cv_store.json`; DR-14 |
| 26 | Step 4d, sub-task 1 (27 October 2026): cross-validation round 2 with the approved core (`dbae21d4…`) on the stored folds, about 35 minutes. Mean PR-AUC (fold SD): `Logistic + poly + L2` 0.0907 (0.0174), `kNN` 0.0706 (0.0148), `Tree` 0.0678 (0.0148); all clearly beat the baseline (C2). Leader still `Logistic + L2` (0.0930); `Logistic + poly + L2` is 0.0023 behind with spread 0.0077. Grid edges: `kNN` k = 51 in 10 of 10 folds; `Logistic + poly + L2` λ = 10⁻⁴ in 2 of 10; `Tree` minimum leaf 20 in 5 of 10. All logistic refits converged. Means recomputed from the fold values: as in the core's table. DR-13 outcome vs expectation filled in: partial (`kNN` above `Tree`, the reverse of the expectation). | `Code/outputs/sepsis/core_cv_round2.json`, `core_cv_store.json`; DR-15 |
| 27 | Step 4e started, sub-task 1 (27 October 2026): diagnosis pass 1 on `Logistic + L2` with the approved core (`dbae21d4…`). First run stopped at the 70 % learning-curve point when a joblib worker process died (`WinError 6`, `BrokenProcessPool`); nothing was written; re-run unchanged (about 21 minutes), and its 10 %–60 % points equal the first run's. Result: E_train 0.9040, E_val 0.9070, gap 0.0029; O1, O2, O3, O5, O6 do not hold (C3 adequate); O4 (underfitting) holds, so DX-5. DX-5's polynomial part does not apply (P3 = many) and k-NN and Tree were already compared, so its remaining part — whether more input variables exist — needs the user; the loop stops. O4 holds for all four configurations (E_train ÷ gap 15.7 to 306.9), the case Analysis Log row 11 said to raise as a `FRAMEWORK` question; raised with the user. Both put as options without a recommendation: the user chose "No new inputs; stop the loop" (S5, the loop ends after one pass) and "Keep §18 as written" (no `FRAMEWORK` change; row 11's open point closed for this analysis). | `Code/outputs/sepsis/core_diagnose_Logistic___L2.json`; DR-16 |
| 28 | Step 4e, sub-task 1 (27 October 2026). The user then changed §18 O4 under `FRAMEWORK` (superseding the "Keep §18 as written" choice in row 27): when P10 = imbalanced and errors are 1 − the deciding metric, O4 needs the ratio test and the O2 comparison. The agent checked the cited pages against the book (2nd edition draft of 1 September 2026, printed pp. 331–337, read from smlbook.org and not kept): the user's reason cited pp. 334–335 for judging underfitting against the desired performance, which those pages do not state (p. 333: big training error with small gap; p. 335: Fig. 13.2 "High training error?"; p. 331: performance against a reference level); the user chose the tag `[B→I pp.331, 333, 335]`. The agent also pointed out that O4 then never drives an action ahead of O2; the user kept the rule as written. Commits: DR-16 and its output (`5e0915e`), `ML Guide.md` alone (`0d68044`). Core updated (`observations()` only), SHA-256 `dbae21d4…` → `10a7e36c…`; diagnosis re-run (about 19 minutes): errors and learning curve unchanged (E_train 0.9040, E_val 0.9070, gap 0.0029); O4 true → false (ratio test true, O2 comparison false); no observation holds. Put to the user without a recommendation (DX-7 needs the criterion not met, and the criterion is assessed at 4g): the user chose "Stop the loop (S5), go to 4f". DR-17 supersedes DR-16. Resolves the open point in row 11. | `Code/outputs/sepsis/core_diagnose_Logistic___L2.json`; DR-17; `ML Guide.md` §18 |
| 29 | Step 4f, sub-task 1 (27 October 2026). Put the threshold trade-off to the user as three options without a recommendation; the user chose "F2, as in DR-05". Ran `recommend` with the core `10a7e36c…` (about 20 minutes). Recommended `Logistic + L2`, λ = 10⁻³ (7 of 10 folds), decision threshold 0.040; candidates `Logistic + L2` and `Logistic + poly + L2` (margin 0.0023, spread 0.0077), chosen by fewer add-ons. Selection confidence Low: C1 none, C2 clear, C3 adequate. Prior agreement agree; grounding 2 `[B→I]`; breadth note does not apply (4 compared). Nested CV at the tuned threshold: F2 0.2204 (SD 0.0182), precision 0.0723 (0.0050), recall 0.4582 (0.0737). Why-not: 10 `EXCL`, `Logistic + poly + L2` `SIMP`, `kNN` and `Tree` `OUTP`. Uncertainty for 4g: SD of PR-AUC 0.0156. Wrote `Code/sepsis_12_test_table.py` for 4g (not run): it builds the test rows with the training table's construction and first checks that this construction reproduces the stored training table exactly. | `Code/outputs/sepsis/core_recommend.json`; DR-18 |
| 30 | Step 4g, sub-task 1 (27 October 2026). Committed the 4f records (`c13b934`) before the test set was touched, as the user approved. `sepsis_12` rebuilt the training table identically, then stopped on its own check: one test patient has `HospAdmTime` empty in every hour (no training patient has an empty `Age`, `Gender` or `HospAdmTime`); nothing was written and no outcome was read. Put to the user as three options without a recommendation; the user chose "Training median, in the core" (DR-19, superseding DR-09). Core `preprocessor()` now median-fills the three constant inputs; checked on the training patients that the new preprocessing equals the old exactly (all patients, and each outer fold fitted on its training part); SHA-256 `10a7e36c…` → `22353007…`; the user approved the change and the plan ("Approve and proceed"). `recommend` re-run (about 20 minutes): identical to DR-18 except the version line. `sepsis_12` then stopped again on the same check, copied from `sepsis_07`; changed it to keep the check for the training rebuild only and to count the test gaps instead (1 `HospAdmTime`). Test table built: 7,818 patients (A 3,895, B 3,923), 246 positive, as in DR-08. Checked the test inputs only (no outcomes): no log input ≤ 0, all `Unit` levels known. | `Code/outputs/sepsis/12_test_table.json`, `core_recommend.json`; DR-19 |
| 31 | Step 4g, sub-task 1 (27 October 2026): the single test-set evaluation (`final`, core `22353007…`, the user's approval quoted). `Logistic + L2`, λ = 10⁻³, refitted on all 31,270 training patients: test PR-AUC 0.0847 (fold SD 0.0156; 7,818 test patients, 246 positive) against 0.0315 for flagging nobody; success criterion met (> 0.0471). At threshold 0.040: F2 0.2326, precision 0.0764, recall 0.4756; TP 117, FP 1,414, FN 129, TN 6,158. Recomputed from the saved predictions with separate calls: the same values. The test set is not used again for this sub-task. | `Code/outputs/sepsis/core_final.json`; `private/core_test_predictions.csv.gz` (not in git); DR-20 |
| 32 | Step 4h, sub-task 1 (27 October 2026): write-up. Assembled the Recommendation Report (13 parts, §25, at the user's intermediate level) from DR-01 to DR-20; parts 9 and 10 are drafts for step 5, and part 9 notes that the fitted weights were not extracted (the core keeps the final model in memory only). Provenance tags counted in the *Rules applied* tables of DR-12 to DR-20: [B] 16, [B→I] 11, [I] 17. Proposed two evaluation figures; the user chose the precision–recall curve on linear axes and the confusion matrix as an unshaded figure of counts. Made Figure 5 (`sepsis_13_fig5_pr_curve.py`) and Figure 6 (`sepsis_14_fig6_confusion.py`), light and dark, from `core_final.json` only; the model has its own colour (purple), the no-skill line the neutral grey (changed from the baseline grey, which was too faint in the dark version). Added the `Methods` and `Results` paragraphs for sub-task 1 under the same sub-heading, and Figures 5 and 6 with captions, to `Report.md`; the `Results` opening sentence now says the held-out patients appear only in Figures 5 and 6. Checked every number in the new text against `core_final.json`, `core_recommend.json` and the CV store, including the rounded values: all agree. | `Demonstration/Sepsis/Report.md`; `Code/outputs/sepsis/figures/fig5_pr_curve.*`, `fig6_confusion.*` |
| 33 | Step 4h, sub-task 1 (27 October 2026). At the end-of-step check the user chose to extract the fitted weights. Added `explain` to the core (version `22353007…` → `7a848f3e…`, additions only; the user approved it before it ran, and chose to record it as the Heart Failure analysis did, in `Analysis` and here, not as a new Decision Record). Verified rebuild of the final model: probabilities for all 7,818 test patients identical to the saved ones (inputs and saved probabilities only; no outcome read, no metric). Wrote the intercept and the 60 weights; part 9 of the Recommendation Report updated with the ten largest. | `Code/outputs/sepsis/core_weights.json`; Analysis, sub-task 1 |
| 34 | Step 4 closed for sub-task 1 when the user asked for step 5 (27 October 2026); left undone: a breakdown of the test result by hospital (step 5 allows no new analysis) and any look at k-NN beyond its grid (k = 51 at the edge in every fold, recorded as a limitation). Step 5: proposed four themes (why this model; how it predicts; the success criterion and use; the limits of the evaluation) with each limitation placed beside the conclusion it qualifies; the user chose the order A → B → C → D from three options. Wrote the `Discussion` of `Report.md` in four paragraphs, by theme, from `Results`, the Recommendation Report, DR-01, DR-03, DR-07, DR-09, DR-13, DR-20, the weights (Analysis) and log rows 21–22. Checked: every number in it appears in `Results` or this Appendix; no grading words; survival analysis named only as a method not covered in the book and not tried. Suggested three titles; the user chose "Predicting sepsis from the first six hours in intensive care". | `Demonstration/Sepsis/Report.md` |

## Code Summary

Scripts for this analysis are prefixed `sepsis_` and write to `Code/outputs/sepsis/`, so they do not collide with the Heart Failure analysis's files. Outputs hold aggregates only; no patient-level rows are written, because the data is under ODbL and kept out of git.

| File | What it does | Reads | Writes | Run |
| --- | --- | --- | --- | --- |
| `Code/sepsis_01_describe_data.py` | Step 1 describing pass. Verifies every patient file against the SHA-256 lists, then describes rows, patients, stays, `ICULOS` continuity, label structure, per-column completeness (per row and per patient, overall and by set) and ranges, demographics, and the input count. No random steps, no seed. Takes about 45 minutes, mostly in per-patient `groupby().apply`. | `Attachments/sepsis-physionet-2019/training_setA/`, `training_setB/`, `SHA256SUMS_training_setA.txt`, `SHA256SUMS_training_setB.txt` | `Code/outputs/sepsis/01_describe.json`, `01_describe.md` | `cd Code && uv run python sepsis_01_describe_data.py` |
| `Code/sepsis_02_scope_counts.py` | Step 1 decisions, counts only; changes nothing and writes no derived table. Counts the rows and patients left once every row from `SepsisLabel` onset is set aside, `FiO2` values by band (unit check), and the values each candidate cleaning rule (`CANDIDATES`, `[I]` thresholds) would set to missing in the kept rows. No random steps, no seed. A few minutes when the machine stays awake. | same patient files | `Code/outputs/sepsis/02_scope_counts.json`, `02_scope_counts.md` | `cd Code && uv run python sepsis_02_scope_counts.py` |
| `Code/sepsis_03_build_table.py` | Applies the step 1 decisions to derived tables. Drops columns that fewer than `DROP_THRESHOLD_PCT` = 10 % `[I]` of patients in either hospital ever have, sets aside every row from `SepsisLabel` onset, and sets the `CLEAN_RULES` values `[I]` to missing: `FiO2`, `Temp`, `Potassium`, `Hgb`, and since 27 October 2026 `Calcium` below 2.0 mg/dL (user's decision, Analysis Log row 21). Fills nothing in. Writes gzip files with `mtime=0`, so checksums are reproducible. `NOT_INPUTS` = `ICULOS`. No random steps, no seed. About 20 minutes. | same patient files | `Code/outputs/sepsis/private/hours.csv.gz`, `patients.csv.gz` (not in git); `Code/outputs/sepsis/03_build_table.json`, `03_build_table.md` | `cd Code && uv run python sepsis_03_build_table.py` |
| `Code/sepsis_04_target_counts.py` | Step 2, counts only. For candidate windows `WINDOWS` = 6 and 12 hours, counts by hospital the patients with a kept hour in the window, those whose label switches on within it (excluded), the remaining cohort and its positives (label switches on later, at any time), records ending by hour N, patients with no measurement in the window, the label-onset quartiles of the positives, and how many switch on within 24 h and 48 h after the window. No random steps, no seed. A minute or two. | `Code/outputs/sepsis/private/hours.csv.gz`, `patients.csv.gz` | `Code/outputs/sepsis/04_target_counts.json`, `04_target_counts.md` | `cd Code && uv run python sepsis_04_target_counts.py` |
| `Code/sepsis_05_horizon_counts.py` | Step 2, counts only, for the agreed window `N` = 6 and horizon `H` = 48 hours. Same cohort as `sepsis_04` for N = 6. Classes each patient by `label_onset_iculos`, never by kept record length: positive (onset in hours 7–54), negative observed to hour 54, or never-septic with a record ending before hour 54. Gives the cohort size and positive share if those patients are kept as negatives or excluded, by hospital. Asserts that every patient falls in exactly one class. The cohort is built by `build_cohort()`, which `sepsis_06_split.py` imports. No random steps, no seed. About a minute. | same derived tables | `Code/outputs/sepsis/05_horizon_counts.json`, `05_horizon_counts.md` | `cd Code && uv run python sepsis_05_horizon_counts.py` |
| `Code/sepsis_06_split.py` | Step 2, the train/test split. Takes the cohort from `build_cohort()` (one row per patient), sorts it by patient, and splits it with `train_test_split`: `TEST_FRACTION` = 0.2, shuffled, stratified by hospital × outcome, `SEED` = 2026. Writes each patient's `set`, `y` and `split`; later steps read only `split == "train"` until step 4g. Gzip with `mtime=0`, so the checksum is reproducible. About a minute. | same derived tables | `Code/outputs/sepsis/private/cohort.csv.gz` (not in git); `Code/outputs/sepsis/06_split.json`, `06_split.md` | `cd Code && uv run python sepsis_06_split.py` |
| `Code/sepsis_07_train_table.py` | Step 3. Builds one row per training patient with the DR-09 input design: last value of each of the 27 clinical columns in ICU hours 1–6, a 0/1 "measured" indicator per clinical column, `Age`, `Gender`, `HospAdmTime`, and `Unit` (MICU, SICU, unknown) from the last non-empty `Unit1`/`Unit2` in hours 1–6. Leaves empty values empty (filling is in the core's pipeline). Keeps only `split == "train"` patients, filtering the hourly file as soon as it is read. Also counts coverage by hospital and the label-onset hours of the training positives, for the figures. No random steps, no seed. A minute or two. | `Code/outputs/sepsis/private/hours.csv.gz`, `patients.csv.gz`, `cohort.csv.gz` | `Code/outputs/sepsis/private/train_table.csv.gz` (not in git); `Code/outputs/sepsis/07_train_table.json`, `07_train_table.md` | `cd Code && uv run python sepsis_07_train_table.py` |
| `Code/sepsis/core.py` | Interim core, not reviewed. So far: `preprocessor()`, the DR-09 pipeline shared by every model family (log of ten labs, then training-fold median; median for the other clinical columns; indicators as they are; `Age`, `Gender`, `HospAdmTime` training-fold median since 27 October 2026 (DR-19, SHA-256 `22353007…`; before, passed through as they were); `Unit` one-hot), and §11 P9 and P10 on the training patients; since step 4a, the 14 configurations (§9) and `admissible_set` (§12: task gate, must-have gates, MOD-1, and MOD-2 via `mod2_check`, which reports the rank of the design matrix and the columns behind any collinearity). since step 4b, §13–§15 prior ranking (`prior`), §16 nested CV (`cv round1`, `cv round2`, `cv add` for post-prior configurations; outer 10 / inner 5 folds stratified by outcome × hospital, `CV_SEED` = 2026, tuned on PR-AUC; results accumulate in `core_cv_store.json` with each patient's outer fold and the training table's checksum), §18 observations and learning curve (`diagnose`; since 27 October 2026 O4 needs the ratio test and the O2 comparison, following the `FRAMEWORK` change to §18, SHA-256 `10a7e36c…`), §16/§17/§19/§20 threshold, confidence, recommendation and why-not codes (`recommend`), and the single test-set evaluation (`final --approved "…"`, which reads `private/test_table.csv.gz`, built only at 4g); since step 4h, `explain` (SHA-256 `7a848f3e…`), a verified rebuild of the final logistic model that writes its weights only if its test probabilities equal the saved ones exactly (reads test inputs and saved probabilities, no outcomes). `[I]` thresholds and grids are named constants; interpretations a–s are in the docstring. Writes its SHA-256 into every output. Seeds: `CV_SEED` = 2026 for folds, learning-curve subsets and tree tie-breaks. Seconds for `prior`; minutes to tens of minutes per configuration for CV. | `Code/outputs/sepsis/private/train_table.csv.gz`; a properties file such as `Code/sepsis/props_dr11.json` (the DR-11 values); `final` also `private/test_table.csv.gz` | `Code/outputs/sepsis/core_p9_p10.json`, `core_admset.json`, `core_prior.json`, `core_cv_store.json`, `core_cv_round1.json`, `core_cv_round2.json`, `core_diagnose_*.json`, `core_recommend.json`, `core_final.json`, `core_weights.json`; `private/core_test_predictions.csv.gz` (not in git) | `cd Code && uv run python sepsis/core.py <command> …` (commands in the docstring) |
| `Code/sepsis_08_fig1_coverage.py` | Figure 1: share of training patients with at least one value of each clinical column in hours 1–6, by hospital (horizontal bars, A blue, B orange). Reads the counts; computes nothing new. Light and dark versions. | `Code/outputs/sepsis/07_train_table.json` | `Code/outputs/sepsis/figures/fig1_coverage.png`, `dark/fig1_coverage.png`, `fig1_coverage.json` | `cd Code && uv run python sepsis_08_fig1_coverage.py` |
| `Code/sepsis_09_fig2_3_distributions.py` | Figures 2 (seven vitals) and 3 (twenty labs): histograms of the last value in hours 1–6 over the training patients who have one, 40 bins over each panel's full range, the ten DR-09 log inputs on a log axis. Not split by outcome. Writes each panel's count, minimum and maximum for the captions. | `Code/outputs/sepsis/private/train_table.csv.gz` | `Code/outputs/sepsis/figures/fig2_vitals.png`, `fig3_labs.png` (+ `dark/`), `fig2_3_distributions.json` | `cd Code && uv run python sepsis_09_fig2_3_distributions.py` |
| `Code/sepsis_10_fig4_onset.py` | Figure 4: number of training positives whose label switches on in each ICU hour 7–54, by hospital (lines, A blue, B orange). Writes the medians and quartiles for the caption. | `Code/outputs/sepsis/07_train_table.json` | `Code/outputs/sepsis/figures/fig4_onset.png` (+ `dark/`), `fig4_onset.json` | `cd Code && uv run python sepsis_10_fig4_onset.py` |
| `Code/sepsis_11_calcium_ptt_counts.py` | After step 3, counts only. (a) Training patients whose last `Calcium` is below `CALCIUM_LOW` = 2.0 mg/dL `[I]`, by hospital, with the counts at 1.75, 2.5, 3.0 and 3.5 and a binned distribution. (b) Last `PTT` values of exactly 150 and 250 s, and above 150, by hospital. Changes nothing. No random steps, no seed. Its committed outputs describe the training table before the `Calcium` rule (Analysis Log rows 16–17) and were deliberately not regenerated (user's decision, 27 October 2026); run now, it reads the cleaned table and gives different `Calcium` counts. | `Code/outputs/sepsis/private/train_table.csv.gz` | `Code/outputs/sepsis/11_calcium_ptt_counts.json`, `11_calcium_ptt_counts.md` | `cd Code && uv run python sepsis_11_calcium_ptt_counts.py` |
| `Code/sepsis_12_test_table.py` | Step 4g, run only after the user approves using the test set. Builds one row per test patient with `build(split)`, the construction of `sepsis_07` (DR-09 design); before writing, rebuilds the training table with the same function and checks it equals the stored one exactly. Checks no patient is in both tables. Requires `Age`, `Gender`, `HospAdmTime` to be non-empty for the training rebuild only; for the test rows it counts the gaps (the core fills them with the training median, DR-19). Computes no metric. No random steps, no seed. About half a minute. | `Code/outputs/sepsis/private/hours.csv.gz`, `cohort.csv.gz`, `train_table.csv.gz` | `Code/outputs/sepsis/private/test_table.csv.gz` (not in git); `Code/outputs/sepsis/12_test_table.json` | `cd Code && uv run python sepsis_12_test_table.py` |
| `Code/sepsis_13_fig5_pr_curve.py` | Step 4h, Figure 5: precision against recall of the recommended model on the test patients, as a step curve, with the no-skill line (test positive rate, neutral grey) and the point at the decision threshold. Reads the core's single evaluation only; refits and recomputes nothing. Model colour purple. Light and dark versions. | `Code/outputs/sepsis/core_final.json` | `Code/outputs/sepsis/figures/fig5_pr_curve.png` (+ `dark/`), `fig5_pr_curve.json` | `cd Code && uv run python sepsis_13_fig5_pr_curve.py` |
| `Code/sepsis_14_fig6_confusion.py` | Step 4h, Figure 6: the test patients by prediction at the threshold and outcome, a 2 × 2 grid of counts without shading. Reads the core's single evaluation only; checks the counts add up to the test patients and positives. Light and dark versions. | `Code/outputs/sepsis/core_final.json` | `Code/outputs/sepsis/figures/fig6_confusion.png` (+ `dark/`), `fig6_confusion.json` | `cd Code && uv run python sepsis_14_fig6_confusion.py` |

Uses pandas, numpy and scikit-learn (`sepsis_06`) from the existing environment; no new dependency.

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published). Read at smlbook.org; the table of contents was checked on 18 October 2026 for survival analysis (DR-07). Page references in the Decision Records come from `ML Guide.md`.
- Reyna, M., Josef, C., Jeter, R., Shashikumar, S., Moody, B., Westover, M. B., Sharma, A., Nemati, S. and Clifford, G. D. (2019). *Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019* (version 1.0.0) [Dataset]. PhysioNet. [https://doi.org/10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857). Units and the `SepsisLabel` definition are taken from this page (read 15 October 2026).
- Reyna, M. A., Josef, C. S., Jeter, R., Shashikumar, S. P., Westover, M. B., Nemati, S., Clifford, G. D. and Sharma, A. (2020). Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019. *Critical Care Medicine*, 48(2), 210–217. [https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/). Hospitals, inclusion rules, hourly binning and the hidden test sets are taken from its Methods (read 15 October 2026).
