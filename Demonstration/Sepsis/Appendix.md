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
- **Supersedes / superseded by:** n/a
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
| `Code/sepsis/core.py` | Interim core, not reviewed. So far: `preprocessor()`, the DR-09 pipeline shared by every model family (log of ten labs, then training-fold median; median for the other clinical columns; indicators and `Age`, `Gender`, `HospAdmTime` as they are; `Unit` one-hot), and §11 P9 and P10 on the training patients; since step 4a, the 14 configurations (§9) and `admissible_set` (§12: task gate, must-have gates, MOD-1, and MOD-2 via `mod2_check`, which reports the rank of the design matrix and the columns behind any collinearity). `[I]` thresholds are named constants; interpretations a–f are in the docstring. Writes its SHA-256 into every output. No random steps. Seconds. | `Code/outputs/sepsis/private/train_table.csv.gz`; for `admset`, a properties file such as `Code/sepsis/props_dr11.json` (the DR-11 values) | `Code/outputs/sepsis/core_p9_p10.json`; `core_admset.json` | `cd Code && uv run python sepsis/core.py p9p10`; `cd Code && uv run python sepsis/core.py admset sepsis/props_dr11.json` |
| `Code/sepsis_08_fig1_coverage.py` | Figure 1: share of training patients with at least one value of each clinical column in hours 1–6, by hospital (horizontal bars, A blue, B orange). Reads the counts; computes nothing new. Light and dark versions. | `Code/outputs/sepsis/07_train_table.json` | `Code/outputs/sepsis/figures/fig1_coverage.png`, `dark/fig1_coverage.png`, `fig1_coverage.json` | `cd Code && uv run python sepsis_08_fig1_coverage.py` |
| `Code/sepsis_09_fig2_3_distributions.py` | Figures 2 (seven vitals) and 3 (twenty labs): histograms of the last value in hours 1–6 over the training patients who have one, 40 bins over each panel's full range, the ten DR-09 log inputs on a log axis. Not split by outcome. Writes each panel's count, minimum and maximum for the captions. | `Code/outputs/sepsis/private/train_table.csv.gz` | `Code/outputs/sepsis/figures/fig2_vitals.png`, `fig3_labs.png` (+ `dark/`), `fig2_3_distributions.json` | `cd Code && uv run python sepsis_09_fig2_3_distributions.py` |
| `Code/sepsis_10_fig4_onset.py` | Figure 4: number of training positives whose label switches on in each ICU hour 7–54, by hospital (lines, A blue, B orange). Writes the medians and quartiles for the caption. | `Code/outputs/sepsis/07_train_table.json` | `Code/outputs/sepsis/figures/fig4_onset.png` (+ `dark/`), `fig4_onset.json` | `cd Code && uv run python sepsis_10_fig4_onset.py` |
| `Code/sepsis_11_calcium_ptt_counts.py` | After step 3, counts only. (a) Training patients whose last `Calcium` is below `CALCIUM_LOW` = 2.0 mg/dL `[I]`, by hospital, with the counts at 1.75, 2.5, 3.0 and 3.5 and a binned distribution. (b) Last `PTT` values of exactly 150 and 250 s, and above 150, by hospital. Changes nothing. No random steps, no seed. Its committed outputs describe the training table before the `Calcium` rule (Analysis Log rows 16–17) and were deliberately not regenerated (user's decision, 27 October 2026); run now, it reads the cleaned table and gives different `Calcium` counts. | `Code/outputs/sepsis/private/train_table.csv.gz` | `Code/outputs/sepsis/11_calcium_ptt_counts.json`, `11_calcium_ptt_counts.md` | `cd Code && uv run python sepsis_11_calcium_ptt_counts.py` |

Uses pandas, numpy and scikit-learn (`sepsis_06`) from the existing environment; no new dependency.

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published). Read at smlbook.org; the table of contents was checked on 18 October 2026 for survival analysis (DR-07). Page references in the Decision Records come from `ML Guide.md`.
- Reyna, M., Josef, C., Jeter, R., Shashikumar, S., Moody, B., Westover, M. B., Sharma, A., Nemati, S. and Clifford, G. D. (2019). *Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019* (version 1.0.0) [Dataset]. PhysioNet. [https://doi.org/10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857). Units and the `SepsisLabel` definition are taken from this page (read 15 October 2026).
- Reyna, M. A., Josef, C. S., Jeter, R., Shashikumar, S. P., Westover, M. B., Nemati, S., Clifford, G. D. and Sharma, A. (2020). Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019. *Critical Care Medicine*, 48(2), 210–217. [https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/). Hospitals, inclusion rules, hourly binning and the hidden test sets are taken from its Methods (read 15 October 2026).
