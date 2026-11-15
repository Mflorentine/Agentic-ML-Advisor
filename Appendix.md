# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

### Provenance

- Source: supplied by the user in the folder `Attachments/Auto MPG/`, which holds `auto-mpg.data`, `auto-mpg.data-original`, `auto-mpg.names` and `Index`. The user states the copy came from the UCI Machine Learning Repository, https://archive.ics.uci.edu/dataset/9/auto+mpg (asked on 2026-11-14). The user downloaded the data on 11 November 2026 (stated by the user, recorded 2026-11-14).
- `auto-mpg.names` says the data was taken from the StatLib library at Carnegie Mellon University, used in the 1983 American Statistical Association Exposition, and dated 7 July 1993. It cites Quinlan (1993) for predicting mpg. `Index` is dated 2 December 1996 and lists the four files.
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0), https://creativecommons.org/licenses/by/4.0/legalcode. The UCI dataset page states it under "License": sharing and adaptation for any purpose, provided credit is given. Checked on 2026-11-14. The repository home page gives no other dataset licence or terms; its only related text is a cookie and privacy notice.
- Credit to give (the page's citation): Quinlan, R. (1993). Auto MPG [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5859H.
- Checksums (SHA-256): `auto-mpg.data` 48b830e11feee5572525f8f1691ddb9d38d3d7b7063edcd8fca672c2a5e17d8d; `auto-mpg.data-original` 57c15897a86fe1bdddb96416698f3dbb064164eb80c0a1eea011eb7674bc0094; `auto-mpg.names` f6ac336f3b11955d71adee2100faf30f8c1be20e6727476836d437d35804599c; `Index` 841000f240b9562fc3985ef5eeba74db747b07cee8c10633608f6e6e5f7bde22.
- Best available form: asked on 2026-11-14. The user answered yes, use the modified file `auto-mpg.data`. No search for an earlier or archived copy was made at the user's choice.

### Files

- Used: `auto-mpg.data`, 398 rows. The user chose it over the original file.
- Not used: `auto-mpg.data-original`. Its only extra rows are 8 cars with no mpg value, which cannot be learned from. This was the user's choice, made in step 1; the reason given is that the modified file is the one the names file describes as used in the published studies.

### Units

- The names file gives mpg as "city-cycle fuel consumption in miles per gallon". It gives no units for displacement, horsepower, weight or acceleration, and does not say whether any column is a measurement or a model output. Checked on 2026-11-14 against the UCI dataset page (https://archive.ics.uci.edu/dataset/9/auto+mpg) and the R package documentation for the same data (https://search.r-project.org/CRAN/refmans/s2net/html/data_auto_mpg.html). Neither states units for any column except mpg, which both quote from Quinlan (1993) as miles per gallon. The UCI variable table has empty Units and Description cells. Secondary search results describe displacement as cubic inches and weight as pounds, but no fetched source confirms this, and no source found states units for acceleration or horsepower. Whether any column is a measurement or a model output is not stated anywhere checked. Status: units for the four columns are unverified. Decision (user, step 1): the four columns are recorded without units. Any unit quoted in the report must be marked unverified.

### Shape and columns (`auto-mpg.data`)

398 rows, 9 columns. Numbers are separated by spaces; the car name follows a tab.

| Column | Type as the names file gives it | Observed values | Missing |
| --- | --- | --- | --- |
| mpg | continuous | 9.0 to 46.6 | 0 |
| cylinders | multi-valued discrete | 3, 4, 5, 6, 8 | 0 |
| displacement | continuous | 68 to 455 | 0 |
| horsepower | continuous | 46 to 230 | 6, written `?` |
| weight | continuous | 1613 to 5140 | 0 |
| acceleration | continuous | 8.0 to 24.8 | 0 |
| model year | multi-valued discrete | 70 to 82 (1970 to 1982, two-digit) | 0 |
| origin | multi-valued discrete | 1, 2, 3 (the file does not say what the codes mean) | 0 |
| car name | string | text | 0 |

### Coverage

- Model years 1970 to 1982, with 27 to 40 rows in each year.
- Origin code 1: 249 rows; code 2: 70; code 3: 79.
- Cylinders 3: 4 rows; 4: 204; 5: 3; 6: 84; 8: 103. The levels 3 and 5 are rare.
- 149 rows share a car name with at least one other row, so the names file's statement that the name is unique for each instance does not hold for this file. Names repeat across years (for example "ford pinto"), so the name is not a unique identifier.

### Completeness

- No mpg values are missing.
- Horsepower is missing for 6 rows, written `?`. These rows are dropped (see Cleaning).
- Systematic check, requested by the user before step 1 closes and run after the drop was chosen (`Code/Auto_MPG/02_compare_dropped_cars.py`, descriptive only). The 6 cars differ from the other 392. All six have 4 or 6 cylinders and none has 8 (103 of the 398 cars have 8). Their mean displacement is 129 against 194 for the rest, their mean weight is 2503 against 2978, and their mean mpg is 28.0 against 23.5. Four are origin 1, two origin 2 and none origin 3 (79 of the 398 cars are origin 3). The gaps are therefore not spread evenly across the file: the 392-car set has fewer small-engine cars than the file does. After the check, the user chose to keep the drop. The report will say that small-engine cars are fewer in the 392-car set than in the file.

### Scope

- Scope: 392 rows, chosen by the user. These are the 398 rows of `auto-mpg.data` less the 6 rows with no horsepower value (see Cleaning).
- Excluded from the original file: nothing further. Its 8 extra rows have no mpg value and are not in the modified file, so the analysis loses nothing it could learn from.

### Cleaning

- Dropped 6 rows whose horsepower is written `?`, leaving 392 rows. The user chose this over keeping them with estimated values, so no value has been estimated or changed. The user confirmed the drop after the systematic check under Completeness. The attachment files have not been altered.

### Accepted as-is

- Units of displacement, horsepower, weight and acceleration are not stated in any source checked. The user chose to record them as unverified, with no unit given (step 1). Any unit quoted in the report must be marked unverified.
- The names file says each car name is unique for each instance. In this file 149 rows share a name with another row. The user chose to group rows by car name anyway (DR-02). A name is a proxy for a car model, not a physical car, and this is not corrected.
- The 8 original rows with no mpg value are not in the modified file. Removed by the source, accepted as the user's choice of file.
- The file's car-name grouping and the 6 cars dropped for missing horsepower are both recorded above under Cleaning and Scope.

### Admissibility

- Admissibility 1: outcome recorded. Answered yes by the user; mpg is present for all 398 rows. Decision Record DR-01.
- Admissibility 3: grouped or time-ordered rows. Answered yes by the user: rows with the same car name belong together. Decision Record DR-02. Group column: `car_name`.
- Grouping: the group column is `car_name`, as the user chose. The 392 used rows fall into 301 names. 147 rows sit in 56 names with two or more rows (34 names with 2 rows, 12 with 3, 7 with 4, 3 with 5). 245 names occur once. 55 names span two or more model years. The file does not identify a physical car, so a name is a proxy for a car model and may group different cars that share a name. Whether that proxy is good enough is noted here; it is not tested.
- Time order: the model year is recorded. Asked on 2026-11-14 whether the split must follow model year. The user first answered yes, then chose to split by car name only, with model year kept as an input. Decision Record DR-04. The guide's time-series method is flagged out of scope; no time-series model is used.
- Admissibility 4: new cases like these. Answered yes by the user: the cases the predictions are used on will look like these (1970 to 1982 cars, with engine sizes and weights in the same range). Decision Record DR-03.

### Target and leakage

- Candidate target: mpg, continuous, described as city-cycle fuel consumption in miles per gallon. How the values were measured is not stated in the files. Open.
- Output type suggested by the data: numeric. Property 1 is to be confirmed in step 2.
- Class counts: not applicable, because the target is not categorical.
- Candidate inputs (7): cylinders, displacement, horsepower, weight, acceleration, model year, origin.
- Set aside: car name, the text naming each car model. It is not proposed as an input.
- Leakage: confirmed by the user on 2026-11-14: no candidate input is built from the fuel figure.
- Input columns: 7. If the three multi-valued discrete columns are treated as categories and one-hot encoded, the count is 4 continuous, 5 cylinder, 13 model year and 3 origin columns, 25 in all, before one level per variable is dropped.
- Categorical share: 3 of the 7 inputs are multi-valued discrete (43%). Whether they are treated as categories is for step 2.

### Experience level

- Stated by the user in step 1, in their own words: "I am a beginner in Machine Learning." Explanations are pitched at a beginner's level; the level changes how much is explained, not what is reported.

## Problem Definition

### Discussion

The user's own words, given on 2026-11-14 when asked what problem they want to solve: "I want to predict the fuel use of a new car from its design based on its engine, weight and size. This could help a buyer or a car designer know how much fuel a car will use before it is tested on the road."

Admissibility 2: prediction or understanding: answered on 2026-11-14 as prediction. Decision Record DR-05.

Open for the formulation: the data records miles per gallon, which goes up as fuel use goes down. The user's phrase is fuel use. Whether the predicted quantity is miles per gallon or fuel used per distance is to be agreed.

### Problem

- What is predicted (y): litres per 100 km, computed as 235.2 divided by the recorded miles per gallon (`235.2 / mpg`), assuming US gallons. Chosen by the user on 2026-11-14 and replaces the gallons per 100 miles target (DR-08). Each recorded figure is between 9.0 and 46.6 miles per gallon, so y would lie between about 5.0 and 26.1 litres per 100 km. The inputs stay in their recorded units, which are unverified.
- Output type (Property 1: output type): non-negative real. Confirmed by the user on 2026-11-14: gallons used per 100 miles can never be below zero (see DR-06).
- From what (x): the candidate inputs in the `Data Summary` (engine, weight and size). Not yet agreed.
- Metric (the single number that decides between models): root mean squared error (RMSE), in litres per 100 km. The choice was made on 2026-11-14 (DR-07); its units changed to litres per 100 km under DR-08.
- Success criterion, in the user's words (2026-11-15): "a good model is usually wrong by at most 1 litre per 100 km, and it does clearly better than guessing the average for every car." Clarified by the user on 2026-11-15: "usually" means the single agreed number (the metric in DR-07, root mean squared error) is at most 1 litre per 100 km. "Clearly better" is set by the user on 2026-11-15 as: the model beats the average guess (the baseline, SML p. 330) by more than the normal variation between the cross-validation folds. The workflow's rule for a clear margin over the baseline is C2: the margin must be at least 1 times the spread (`ML Guide.md` section 17, a threshold of ours `[I]`). The user chose on 2026-11-15 the first of the two measures: how much the margin itself changes from one check to the next, that is the spread of the margin across the cross-validation folds, as in C2. Chosen by the user on 2026-11-15: the margin is checked once on the test data, against its variation across the training folds.
- Success criterion, as the user has set it (2026-11-15): (1) the agreed single number (root mean squared error, DR-07) is at most 1 litre per 100 km on the test data; and (2) the model beats the average guess (the baseline, SML p. 330) by a clear margin, meaning the margin is at least 1 times its variation across the training checks (`ML Guide.md` section 17, C2, a threshold of ours `[I]`), checked once on the test data. Both must hold. Not yet written as a formal test in the record of DR-07; the formal record follows when the rest of step 2 is agreed.
- Measures monitored alongside the metric (reported, not used to decide): mean absolute error (MAE), in litres per 100 km, the average size of the miss counting over- and under-estimates alike. Chosen by the user on 2026-11-15 (SML p. 330). Recorded in DR-09.
- Property 5: interpretability: no requirement. The user answered on 2026-11-15: "No requirement" (DR-11). The earlier answer "Explainable" (DR-10) was a mistake and is superseded.
- Property 6: probabilities: no requirement. The user answered on 2026-11-15: "No, a single figure is enough" (DR-12). The output is one fuel figure per car, so the question of chances does not apply.
- Property 7: extrapolation: no. The user answered on 2026-11-15: "No, only cars like those in the data" (DR-13). Predictions are needed only within the range of the data.
- Property 8: expected shape: unknown. The user's words on 2026-11-15: "I expect heavier cars and bigger engines to use more fuel, but I do not know whether the relationship is a straight line or a curve." The expected direction is recorded in these words; the shape is not known, so the value is unknown (DR-14).
- Sub-tasks (the separately answered parts): one sub-task. The user chose one question on 2026-11-15: predict the fuel use of a new car from its design, model year and country of origin, measured by the success criterion above (DR-15; wording changed by DR-18).
- Division of the data (`SPLIT`, DR-16): one in five cars held back as the test part, split by car name, with seed 2026: 314 training cars and 78 test cars (61 car names). The test cars are locked and are not read before the final evaluation. Written to `Code/outputs/Auto_MPG/split_seed2026.csv`.

### Sub-tasks

- To be agreed in step 2.

## Analysis

### The training data (step 3, Figure 1)

- Figure 1: histogram of fuel use, litres per 100 km, for the 314 training cars. Script: `Code/Auto_MPG/05_fig1_fuel_histogram.py`. Output: `Code/outputs/Auto_MPG/fig1_fuel_histogram.png` (light) and `Code/outputs/Auto_MPG/dark/fig1_fuel_histogram.png` (dark).
- Summary numbers (from `Code/outputs/Auto_MPG/fig1_fuel_histogram_summary.txt`): minimum 5.05, maximum 26.13, mean 11.35, median 10.23 litres per 100 km; bars one litre per 100 km wide.
- The chart was proposed to the user, who asked for it to be drawn, on 2026-11-15. The test cars are not read by the script.
- Figure 2: fuel use against weight, one dot per training car. Script: `Code/Auto_MPG/06_fig2_fuel_vs_weight.py`. Output: `Code/outputs/Auto_MPG/fig2_fuel_vs_weight.png` (light) and `Code/outputs/Auto_MPG/dark/fig2_fuel_vs_weight.png` (dark). Proposed to the user and drawn on 2026-11-15. Plots the observations only; no line is fitted. Weight is in the recorded units, not verified.
- Figure 3: fuel use by origin code, one dot per training car, with the median of each column. Script: `Code/Auto_MPG/07_fig3_fuel_by_origin.py`. Output: `Code/outputs/Auto_MPG/fig3_fuel_by_origin.png` (light) and `Code/outputs/Auto_MPG/dark/fig3_fuel_by_origin.png` (dark). Training cars per code: 201, 54 and 59. Proposed and drawn on 2026-11-15. The horizontal jitter of the dots is seeded (2026) and has no meaning.
- Observed in the chart, not interpreted: the fuel use is spread over the range; most training cars fall between 6 and 14 litres per 100 km; a few cars are above 20; there is a gap between about 17 and 18.


## Decision Records

### DR-01 · Admissibility · step 1

- **Type:** Admissibility (Admissibility 1: outcome recorded)
- **Step:** 1
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** Is there a recorded output y for the rows the model learns from?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| mpg present | all 398 rows of `auto-mpg.data`; 0 missing; all 392 used rows included | M | `Code/Auto_MPG/01_describe_data.py` output; `Attachments/Auto MPG/auto-mpg.data` |
| User's answer | "Yes, every car has one" | M | Question put to the user in step 1 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 1: outcome recorded | Yes: a recorded output exists for the rows used | [B SML p. 15] | Gate passed; the analysis continues as a supervised problem |

**Thresholds applied:** n/a

**Options considered:** n/a (closed yes/no check)

**Expectation:** n/a

**Decision:** Admissibility 1 is met: mpg is recorded for every car used in the analysis.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Yes, every car has one".

**Supersedes / superseded by:** n/a

**Links:** `Attachments/Auto MPG/auto-mpg.data`; `Code/Auto_MPG/01_describe_data.py`

### DR-02 · Admissibility · step 1

- **Type:** Admissibility (Admissibility 3: grouped or time-ordered rows)
- **Step:** 1
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** Do several rows belong to the same unit, or are the rows ordered in time, so that the split and the cross-validation must keep them together?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Rows sharing a car name | 392 used rows; 301 names; 147 rows in 56 names of two or more rows; 55 names span two or more model years | M (user's answer); the counts are from the file, output of `Code/Auto_MPG/03_group_sizes.py` | `Attachments/Auto MPG/auto-mpg.data` |
| User's answer | "Yes, rows with the same name belong together" | M | Question put to the user in step 1 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 3: grouped or time-ordered rows | Grouped, by car name | [B SML pp. 16, 38–39, 329] | Splits and cross-validation folds will keep each car name together (step 2 `SPLIT` record) |

**Thresholds applied:** n/a

**Options considered:** (a) rows split one by one; (b) rows split by car name. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** Rows with the same car name are treated as one group, and are kept together in every split and fold. The group column is `car_name`.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Yes, rows with the same name belong together".

**Supersedes / superseded by:** n/a

**Links:** `Attachments/Auto MPG/auto-mpg.data`; `Code/Auto_MPG/03_group_sizes.py`

### DR-03 · Admissibility · step 1

- **Type:** Admissibility (Admissibility 4: new cases like these)
- **Step:** 1
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** Will the cases the model is used on look like the data it learns from?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Years and ranges of the data used | model years 1970 to 1982; displacement 68 to 455; weight 1613 to 5140 (392 used rows) | M (from the file, output of `Code/Auto_MPG/01_describe_data.py`) | `Attachments/Auto MPG/auto-mpg.data` |
| User's answer | "Yes, cars like these" | M | Question put to the user in step 1 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 4: new cases like these | Yes: future cases are expected to look like the data | [B SML pp. 328–329] | The analysis continues with the validation and test data drawn from this file, with no separate source to agree |

**Thresholds applied:** n/a

**Options considered:** n/a (closed yes/no check)

**Expectation:** n/a

**Decision:** Future cases are expected to resemble these cars, so the validation and test data are drawn from this file.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Yes, cars like these".

**Supersedes / superseded by:** n/a

**Links:** `Attachments/Auto MPG/auto-mpg.data`

### DR-04 · Admissibility · step 1

- **Type:** Admissibility (Admissibility 3: grouped or time-ordered rows, time part)
- **Step:** 1
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** Are the rows ordered in time, so that the split must respect that order?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Time column | model year, 1970 to 1982, recorded for every row | M | `Attachments/Auto MPG/auto-mpg.data` |
| First answer | "Yes, the split must follow model year" | M | Question put to the user in step 1 |
| Second answer | "Split by car name only" | M | Question put to the user in step 1, after the guide's rules were explained |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 3: grouped or time-ordered rows, time column | Time column present; the user did not want an autoregressive reformulation, so time-series modelling is flagged as out of scope | [B SML pp. 16, 38–39] | No time-series model is used. Model year stays an input. The split is by car name (DR-02). |

**Thresholds applied:** n/a

**Options considered:** (a) split by year, newer cars for testing; (b) split by car name only, model year as an input. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** The split is by car name only. Model year is an input, not a timeline. Time-series modelling is flagged as out of scope.

**Why not:** Option (a) is not described in the four chapters in scope and the workflow's rules do not yet allow it; it would first need a change to those rules (`FRAMEWORK`).

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, first answered "Yes, the split must follow model year", then, after the rules were explained, "Split by car name only".

**Supersedes / superseded by:** n/a (DR-02 covers the grouping; this record covers the time part only)

**Links:** `Attachments/Auto MPG/auto-mpg.data`

### DR-05 · Admissibility · step 2

- **Type:** Admissibility (Admissibility 2: prediction or understanding)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** Is the main aim to predict the outcome for new cases, or to understand how the variables are connected?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's aim | "I want to predict the fuel use of a new car from its design based on its engine, weight and size." | M | User's statement, step 2, recorded in `Appendix.md` Problem Definition, Discussion |
| User's answer | "Predict new cars' fuel figures" | M | Question put to the user in step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 2: prediction or understanding | Predict: the workflow continues | [B SML p. 20] | The analysis optimises prediction for new cases. It does not claim to show how the variables are connected. |

**Thresholds applied:** n/a

**Options considered:** (a) predict new cases' fuel figures; (b) understand how the variables are connected. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** The aim is to predict the fuel figure of new cars from their engine, weight and size. The analysis does not claim to explain how these variables cause fuel use.

**Why not:** Option (b) was not chosen; it would need the user to confirm continuing under this workflow.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Predict new cars' fuel figures".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Problem Definition, Discussion

### DR-06 · FORM · step 2

- **Type:** FORM (partial: the target only; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** What quantity is predicted (y)?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's aim | predict the fuel use of a new car from its design | M | DR-05; `Appendix.md` Problem Definition, Discussion |
| Recorded measure | miles per gallon, 9.0 to 46.6; higher means further per gallon | M (metadata: the names file describes mpg as miles per gallon) | `Attachments/Auto MPG/auto-mpg.names` |
| User's choice | "Gallons used per 100 miles" | M | Question put to the user in step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 1: output type | Proposed: non-negative real, since y is never below 0 (the guide's category for continuous values never below 0). To be confirmed with the user. | [B SML pp. 61–62] | y = 100 / mpg, computed in the analysis code. The value chosen decides the task gate (§12) and the prior. |

**Thresholds applied:** n/a

**Options considered:** (a) miles per gallon, as recorded; (b) gallons used per 100 miles. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** The predicted quantity is gallons used per 100 miles, computed from the recorded miles per gallon. A higher figure means more fuel used.

**Why not:** Option (a) was not chosen; the user's aim is fuel use.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, chose: "Gallons used per 100 miles".

**Supersedes / superseded by:** superseded by DR-08 (the target changed from gallons used per 100 miles to litres per 100 km).

**Links:** `Attachments/Auto MPG/auto-mpg.names`; `Appendix.md` Problem Definition

### DR-07 · FORM · step 2

- **Type:** FORM (partial: the metric only; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** Which single number decides between models?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Output | gallons used per 100 miles (DR-06), positive and never below zero (Property 1: output type, non-negative real, confirmed by the user) | M | DR-06; `Appendix.md` Problem Definition |
| Default error for regression | squared error | [B SML p. 67] | `ML Guide.md` §2 and §16 |
| User's choice | "Root mean squared error (RMSE)" | M | Question put to the user in step 2, options named and explained in plain words |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Diagnosis errors use the agreed selection metric when it is an error function in its own right | RMSE is an error function, so it is used as it is | [I] | The selection metric is RMSE in gallons per 100 miles |

**Thresholds applied:** n/a

**Options considered:** (a) mean absolute error (MAE), the average size of the miss, counting over- and under-estimates alike; (b) root mean squared error (RMSE), where big misses count for much more. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** The single number that decides between models is root mean squared error, in gallons used per 100 miles.

**Why not:** Option (a) was not chosen by the user; it counts all misses in proportion and does not weight large misses more heavily.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, chose: "Root mean squared error (RMSE)".

**Supersedes / superseded by:** the choice of RMSE stands; its units are superseded by DR-08 (litres per 100 km instead of gallons per 100 miles).

**Links:** `Appendix.md` Problem Definition, Problem

### DR-08 · FORM · step 2

- **Type:** FORM (partial: the target, replacing DR-06; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-14
- **Question:** What quantity is predicted (y), in which units?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Recorded measure | miles per gallon, 9.0 to 46.6 | M (the names file describes mpg as miles per gallon) | `Attachments/Auto MPG/auto-mpg.names` |
| Conversion | litres per 100 km = 235.2 ÷ miles per gallon, assuming US gallons | M (user's statement) | User's message, step 2 |
| Units of the inputs | recorded units, not verified | M (DR-07 and Data Summary, Units) | `Appendix.md` Data Summary, Units |
| User's choice | "litres per 100 km instead of gallons per 100 miles", because these are the units used in Rwanda and Europe | M | User's message, step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 1: output type | non-negative real (unchanged from DR-06): y is never below zero | [B SML pp. 61–62] | The output type is unchanged by the change of units |

**Thresholds applied:** n/a

**Options considered:** (a) gallons used per 100 miles (DR-06); (b) litres per 100 km. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** The predicted quantity is litres per 100 km, computed as 235.2 divided by the recorded miles per gallon. This replaces DR-06. The inputs stay in their recorded units.

**Why not:** Option (a) is replaced because the user's audience uses litres per 100 km. The conversion assumes the miles per gallon figures are US gallons; this is the user's assumption and is not verified against the source.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, chose: litres per 100 km, with the conversion and the unverified inputs noted as above.

**Supersedes / superseded by:** supersedes DR-06. DR-07 (RMSE) stands with its units changed.

**Links:** `Attachments/Auto MPG/auto-mpg.names`; `Appendix.md` Problem Definition, Problem

### DR-09 · FORM · step 2

- **Type:** FORM (partial: monitored measures; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** Which measures are reported alongside the single number that decides between models?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Book guidance | Beside the single number, it is useful to monitor other metrics to reveal the trade-offs | [B SML p. 330] | SML p. 330 |
| User's choice | "Mean absolute error (MAE)" | M | Question put to the user in step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Metrics to monitor alongside the single number (`ML Guide.md` section 2) | Mean absolute error reported beside the root mean squared error | [B SML p. 330] | Reported in the results; does not decide between models |

**Thresholds applied:** n/a

**Options considered:** (a) mean absolute error (MAE); (b) largest miss; (c) none, only the one number. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** Mean absolute error, in litres per 100 km, is reported alongside the root mean squared error. It does not decide between models.

**Why not:** (b) and (c) were not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, chose: "Mean absolute error (MAE)".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Problem Definition, Problem

### DR-10 · FORM · step 2 · SUPERSEDED by DR-11

- **Type:** FORM (partial: Property 5 must-have; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** Must a person be able to follow how each prediction is made, or must there be a guaranteed limit on how wrong any single prediction can be?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "Explainable": a person must be able to follow how each prediction is made | M | Question put to the user in step 2 |
| Book basis | Models from chapters 2 and 3 can, to some degree, be inspected | [B→I SML p. 347] | SML p. 347 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 5: interpretability = inspectable (must-have) | Must-have: the linear, logistic, Poisson, exponential and tree models stay admissible; k-NN only if showing the most similar past cases is acceptable to the user | [B→I SML p. 347] | To be applied at step 4a, when the admissible set is built |

**Thresholds applied:** n/a

**Options considered:** (a) none; (b) inspectable (must-have); (c) worst-case bound. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** Predictions must be inspectable: a person must be able to follow how each one is made. This is a must-have.

**Why not:** (a) and (c) were not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Explainable".

**Supersedes / superseded by:** superseded by DR-11. The user's answer "Explainable" was given in error; the user meant "No requirement".

**Links:** `Appendix.md` Problem Definition, Problem

### DR-11 · FORM · step 2

- **Type:** FORM (partial: Property 5 must-have; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** Must a person be able to follow how each prediction is made, or must there be a guaranteed limit on how wrong any single prediction can be?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "No requirement" (the user states this replaces the earlier answer "Explainable", which was given in error) | M | Question put to the user in step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 5: interpretability = none | No must-have; interpretability does not remove any model | [B→I SML p. 347] | None at step 4a for this property |

**Thresholds applied:** n/a

**Options considered:** (a) no requirement; (b) explainable (must-have, given in error and superseded); (c) guaranteed limit on any single miss. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** No requirement on explaining predictions or on a limit for any single prediction. DR-10 is superseded.

**Why not:** (b) was given in error; (c) was not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked; answered "No requirement" (correction of an earlier answer of "Explainable").

**Supersedes / superseded by:** supersedes DR-10.

**Links:** `Appendix.md` Problem Definition, Problem

### DR-12 · FORM · step 2

- **Type:** FORM (partial: Property 6 must-have; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** Do you need class probabilities, or a decision threshold tuned to the costs of each error, or is a single figure enough?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "No, a single figure is enough" | M | Question put to the user in step 2 |
| Output | one numeric figure per car (DR-08); not a choice between classes | M | `Appendix.md` Problem Definition, Problem |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 6: probabilities | No requirement; the question does not apply to a numeric output | [B SML pp. 50, 53–54, 92–93] | None at step 4a for this property |

**Thresholds applied:** n/a

**Options considered:** (a) no requirement, a single figure is enough; (b) chances or a chosen cut-off needed. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** No requirement for class probabilities or a tuned decision threshold. A single figure per car is the output.

**Why not:** (b) was not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "No, a single figure is enough".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Problem Definition, Problem

### DR-13 · FORM · step 2

- **Type:** FORM (partial: Property 7 requirement; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** Will predictions be needed for inputs beyond the range seen in the data?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "No, only cars like those in the data" | M | Question put to the user in step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 7: extrapolation = no | Predictions are needed only within the range of the data | Not applicable: the guide's effect (`[B→I SML p. 26]`, `[I]`) applies only when the answer is yes | No effect; the choice of method stays open |

**Thresholds applied:** n/a

**Options considered:** (a) only cars like those in the data; (b) cars beyond the range of the data. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** Predictions are needed only for cars like those in the data, not beyond its range.

**Why not:** (b) was not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "No, only cars like those in the data".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Problem Definition, Problem

### DR-14 · FORM · step 2

- **Type:** FORM (partial: Property 8 expectation; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** Does the user, or the subject's known science, expect a particular shape of relationship between the inputs and the fuel figure?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's words | "I expect heavier cars and bigger engines to use more fuel, but I do not know whether the relationship is a straight line or a curve." | M (user's statement) | Question put to the user in step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 8: expected shape = unknown | Shape not known to the user. The expected direction (more fuel for heavier cars and bigger engines) is recorded in the user's words and does not select a shape. | No rule row: the guide's shape rules apply only to linear, curved or interactions/irregular (`ML Guide.md` section 11) | Unknown changes nothing in the ranking (the default) |

**Thresholds applied:** n/a

**Options considered:** (a) straight line; (b) curve; (c) interactions or irregular; (d) unknown. Chosen: (d), as the user does not know the shape.

**Expectation:** The user expects fuel use to rise with weight and engine size; the shape is not expected.

**Decision:** Property 8: expected shape is unknown. The user's words are recorded above.

**Why not:** (a), (b) and (c): the user does not know the shape.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: the words quoted in the evidence.

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Problem Definition, Problem

### DR-15 · FORM · step 2

- **Type:** FORM (sub-tasks; the rest of the formulation is to be agreed)
- **Step:** 2
- **Sub-task:** n/a (this record defines the sub-tasks)
- **Date:** 2026-11-15
- **Question:** Should the problem be answered as one question, or as separate questions, each with its own result?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's choice | "One question" | M | Question put to the user in step 2 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Sub-tasks (`ML Guide.md` section 2; `instructions.md`, step 2) | One sub-task | [I] | One sub-task: the whole problem. Each sub-task is taken through step 4 in turn. |

**Thresholds applied:** n/a

**Options considered:** (a) one question; (b) separate questions. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** One sub-task: predict the fuel use of a new car from its engine, weight and size, against the success criterion.

**Why not:** (b) was not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, chose: "One question".

**Supersedes / superseded by:** the number of sub-tasks stands; the wording of the sub-task (engine, weight and size) is superseded by DR-18 (design, model year and country of origin).

**Links:** `Appendix.md` Problem Definition, Sub-tasks

### DR-16 · SPLIT · step 2

- **Type:** SPLIT
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** What share of the cars is held back as the test part, and how is the split made?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Used rows | 392 cars with a horsepower value | M (Data Summary) | `Appendix.md` Data Summary |
| Group column | car name (DR-02) | M | DR-02 |
| User's choice | one in five cars held back | M | Question put to the user in step 2 |
| Result | 314 training cars, 78 test cars, 61 test car names; 0 names on both sides | Counts from the file; no model fitted | `Code/outputs/Auto_MPG/split_seed2026.csv`; `Code/Auto_MPG/04_split.py` |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Split by group where rows share a unit (`ML Guide.md` section 3) | Group split by car name | [B SML p. 329] | All rows with one name go to the same side |
| Split randomly (`ML Guide.md` section 3) | Random, with seed 2026 | [B SML pp. 71, 73] | Reproducible split |
| Test data used once (`ML Guide.md` section 3) | Test rows locked until the final evaluation | [B SML pp. 74, 328] | No step before the final evaluation reads the test rows |

**Thresholds applied:** test share one in five cars (user's choice). Test share of rows: 0.199.

**Options considered:** (a) one in five cars held back; (b) one in ten cars held back. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** Split by car name, one in five cars held back as the test part, seed 2026. The test part is locked until the single final evaluation.

**Why not:** (b) was not chosen by the user; it would leave fewer cars for the final check.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, chose: "One in five cars".

**Supersedes / superseded by:** n/a

**Links:** `Code/Auto_MPG/04_split.py`; `Code/outputs/Auto_MPG/split_seed2026.csv`

### DR-17 · PROP · step 2

- **Type:** PROP (step 2 values; Properties 9 and 10 come in step 3)
- **Step:** 2
- **Sub-task:** n/a (applies to the analysis as a whole)
- **Date:** 2026-11-15
- **Question:** What are the property values known at the close of step 2?

**Evidence**

| Property | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | non-negative real | M (user confirmed, DR-06 and DR-08) | `Appendix.md` Problem Definition |
| Property 2: data-to-parameter ratio | ample under both readings of the category question: 314 training cars against 25 or 22 input columns gives 12.1 or 13.7 cars per parameter (threshold 10, ours) | M (computed from the file: training count and input count) | `Code/outputs/Auto_MPG/split_seed2026.csv` |
| Property 3: number of inputs | open: 25 input columns if every category keeps one yes-or-no column per value, or 22 if one column per category is dropped (threshold 20, ours) | M (computed from the file, pending the user's choice) | `Appendix.md` Data Summary |
| Property 4: categorical share | low under any reading: 3 of 7 inputs (43%) if model year, number of cylinders and origin are categories, or 2 of 7 (29%) without model year (threshold 50%, ours) | M (computed from the file) | `Appendix.md` Data Summary |
| Property 5: interpretability | none | M (user, DR-11) | DR-11 |
| Property 6: probabilities | none | M (user, DR-12) | DR-12 |
| Property 7: extrapolation | no | M (user, DR-13) | DR-13 |
| Property 8: expected shape | unknown; the user expects more fuel for heavier cars and bigger engines (user's words, DR-14) | M (user) | DR-14 |
| Properties 9 and 10 | not yet computed; step 3 | not applicable yet | n/a |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 2, Property 3, Property 4 (`ML Guide.md` section 11) | Property 2 ample; Property 4 low; Property 3 open (few or many) | Thresholds marked ours | Property 3 decides whether the nearest-cases and polynomial methods are disfavoured; it must be settled before step 4a |

**Thresholds applied:** Property 2 limited below 10 rows per parameter (ours); Property 3 many above 20 inputs (ours); Property 4 high at 50% or more (ours). The values used are those shown above.

**Options considered:** n/a (a record of the values known at this step)

**Expectation:** n/a

**Decision:** Properties 1, 2, 4, 5, 6, 7 and 8 are recorded as above. Property 3 is open, pending the user's choice of how categories become yes-or-no columns and whether model year, cylinders and origin count as categories. Properties 9 and 10 are recorded in step 3.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** informed: the category question was not decided; the user chose to close step 2 with it recorded as open.

**Supersedes / superseded by:** Property 3 (open) superseded by DR-19; the other values stand.

**Links:** `Appendix.md` Data Summary; `Code/outputs/Auto_MPG/split_seed2026.csv`

### DR-18 · FORM · step 2

- **Type:** FORM (sub-task wording; supersedes the wording in DR-15)
- **Step:** 2 (recorded when step 3 began)
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** How is the sub-task worded?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's wording | "from its design, model year and country of origin" | M | User's instruction in step 3 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Sub-tasks (`ML Guide.md` section 2; `instructions.md`, step 2) | One sub-task, worded by the user | [I] | The Introduction and the Problem Definition use the new wording |

**Thresholds applied:** n/a

**Options considered:** (a) engine, weight and size (DR-15); (b) design, model year and country of origin. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** The sub-task is to predict the fuel use of a new car from its design, model year and country of origin.

**Why not:** (a) is superseded by the user's own wording.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked; the user instructed the wording.

**Supersedes / superseded by:** supersedes the wording in DR-15.

**Links:** `Appendix.md` Problem Definition, Sub-tasks; `Project Report.md` Introduction

### DR-19 · PROP · step 3 (input design)

- **Type:** PROP (supersedes the open Property 3 in DR-17) and input design (`ML Guide.md` section 9, decided with the user)
- **Step:** 3 (input design, decided at the start of step 3)
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** Are model year, number of cylinders and country of origin categories, and is one yes-or-no column per category dropped?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Model year | a number, not a category (user) | M | User's answer, step 3 |
| Number of cylinders | a number, not a category (user) | M | User's answer, step 3 |
| Country of origin | a category (user); the file codes it 1, 2 or 3 without naming the countries | M | User's answer, step 3; `Attachments/Auto MPG/auto-mpg.names` |
| Yes-or-no columns | one column per category is dropped (user) | M | User's answer, step 3 |
| Input columns after encoding | displacement, horsepower, weight, acceleration, model year, cylinders: 6 numbers; origin: 2 yes-or-no columns (3 values, one dropped); total 8 | T (counted from the training data layout) | `Code/Auto_MPG/04_split.py` (the split) |
| Training cars | 314 | T | `Code/outputs/Auto_MPG/split_seed2026.csv` |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 3: number of inputs | 8 input columns after encoding: few (threshold 20, ours) | [I] (threshold) | Does not disfavour k-NN or polynomial terms on this count |
| Property 2: data-to-parameter ratio | 314 training cars against 8 input columns gives 34.9 cars per parameter: ample (threshold 10, ours) | [I] (threshold) | No change |
| Property 4: categorical share | 1 of 7 original inputs is a category (origin): 14%, low (threshold 50%, ours) | [I] (threshold) | Does not disfavour k-NN |
| Input design | Domain transformations and the choice of inputs are decided with the user; allowed for every family | [B SML p. 18] | Model year and cylinders enter as numbers; origin as a category |

**Thresholds applied:** Property 2 limited below 10 rows per parameter (ours); Property 3 many above 20 input columns (ours); Property 4 high at 50% or more (ours). The values used are those shown above.

**Options considered:** (a) model year, cylinders and origin all categories; (b) model year and cylinders numbers, origin a category, one column per category dropped (chosen); other combinations not chosen by the user.

**Expectation:** n/a

**Decision:** Model year and number of cylinders are numbers. Country of origin is a category. One yes-or-no column per category is dropped. Input columns after encoding: 8. Property 3 is few; Property 2 is ample; Property 4 is low.

**Why not:** Other combinations were not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: model year "No, a number"; cylinders "No, a number"; origin "Yes, a category"; columns "Drop one column per category".

**Supersedes / superseded by:** supersedes the open Property 3 in DR-17.

**Links:** `Appendix.md` Data Summary; `Code/outputs/Auto_MPG/split_seed2026.csv`

### DR-20 · PROP · step 3 (input design: choice of inputs)

- **Type:** PROP (input design, `ML Guide.md` section 9, decided with the user)
- **Step:** 3
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** Which measurements of the car are inputs?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Candidate inputs | engine size (displacement), horsepower, weight, acceleration, number of cylinders, model year, origin | M (Data Summary) | `Appendix.md` Data Summary |
| User's answer | "All seven, as now" | M | Question put to the user in step 3 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design: choice of inputs (`ML Guide.md` section 9) | All seven candidate inputs are used | [B SML p. 18] | The input set is the seven listed; no measurement is left out |

**Thresholds applied:** n/a

**Options considered:** (a) all seven; (b) leave out acceleration; (c) leave out horsepower. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** All seven candidate inputs are used. The user reads "design" in the sub-task to include these measurements.

**Why not:** (b) and (c) were not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "All seven, as now".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Data Summary; `Appendix.md` Decision Records, DR-19

### DR-21 · PROP · step 3 (input design: transformations)

- **Type:** PROP (input design, `ML Guide.md` section 9, decided with the user)
- **Step:** 3
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** Should any measurement be transformed (for example, by its logarithm) before the model uses it?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer | "No, use them as recorded" | M | Question put to the user in step 3 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design: domain transformations (`ML Guide.md` section 9) | None applied; every measurement is used as recorded | [B SML p. 18] | The inputs enter in the units recorded in the file; no logarithm is taken |

**Thresholds applied:** n/a

**Options considered:** (a) use the measurements as recorded; (b) take the logarithm of weight and engine size. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** No transformation of any input. The inputs are used as recorded.

**Why not:** (b) was not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "No, use them as recorded".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Decision Records, DR-19 and DR-20

### DR-22 · PROP · step 3 (input design: car name)

- **Type:** PROP (input design, `ML Guide.md` section 9, decided with the user)
- **Step:** 3
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** Should the car name be an input?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Distinct car names among the training cars | most names appear once; 149 rows share a name with another row in the used data (DR-02) | T (counted from the training data) | `Code/Auto_MPG/03_group_sizes.py`; DR-02 |
| User's answer | "Leave it out, as now" | M | Question put to the user in step 3 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design: choice of inputs (`ML Guide.md` section 9) | Car name not an input | [B SML p. 18] | The car name is used only as the group column for the split (DR-02), never as an input |

**Thresholds applied:** n/a

**Options considered:** (a) leave the car name out; (b) use it as an input, one category per name. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** The car name is not an input. It is used only to keep rows of one name together in the split.

**Why not:** (b) was not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Leave it out, as now".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Decision Records, DR-02 and DR-20

### DR-23 · PROP · step 3 (Properties 9 and 10)

- **Type:** PROP (Properties 9 and 10, step 3)
- **Step:** 3
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** What are Property 9 (separability) and Property 10 (class imbalance) for this analysis?

**Evidence**

| Property | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Output type | non-negative real (a number, not classes) | M (user, DR-06 and DR-08) | DR-08 |
| Property 9: separability | not applicable: the guide defines it for classification only | [I] (the guide's definition, classification only) | `ML Guide.md` section 11 |
| Property 10: class imbalance | not applicable: the guide defines it for classification only | [I] (threshold, ours); the book's point about imbalance is at SML p. 91 | `ML Guide.md` section 11 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 9: separability (classification only) | Not computed: the output is not classes | `ML Guide.md` section 11 | None |
| Property 10: class imbalance (classification only) | Not computed: the output is not classes | `ML Guide.md` section 11 | None |

**Thresholds applied:** n/a

**Options considered:** n/a (the two properties do not apply to a numeric output)

**Expectation:** n/a

**Decision:** Properties 9 and 10 are recorded as not applicable, because the output is a number.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** informed: the user closed step 3 on 2026-11-15 after this was set out in the written check.

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Decision Records, DR-17 (Properties 9 and 10 to be recorded in step 3)

## Recommendation

*Written at the end of step 4, one sub-heading per sub-task, after its single test-set evaluation: the thirteen-part Recommendation Report of `ML Guide.md` §25, assembled from the Decision Records. Nothing in it is new.*

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1 started. Analysis named Auto_MPG. Root `Project Report.md` and `Appendix.md` set up from the templates (the root files held no earlier analysis). Describing pass on the Auto MPG attachment: shape, columns, missing values, ranges and category counts, and comparison with the original file. The user chose `auto-mpg.data` (398 rows) over the original file. Data Summary and Code Summary written. The 6 cars with no horsepower value are dropped, leaving 392 rows (the user's choice). Still open in step 1: units, the admissibility answers, the ML experience level, whether this is the best available form, and the publisher's address. | `Code/Auto_MPG/01_describe_data.py`; `Appendix.md` Data Summary |
| 2 | Descriptive check of the 6 cars with no horsepower value against the other 392, at the user's request before step 1 closes. Found the six differ systematically (see Completeness). The user then confirmed the drop. | `Code/Auto_MPG/02_compare_dropped_cars.py`; `Appendix.md` Data Summary |
| 3 | Admissibility 1 (outcome recorded) asked and answered yes by the user. | `Appendix.md` Decision Records, DR-01 |
| 4 | Units of displacement, horsepower, weight and acceleration checked at the user's request. No source found states them; the UCI dataset page, the R package page and the names file are silent. Status: unverified. | `Appendix.md` Data Summary, Units |
| 5 | User chose to record the units of displacement, horsepower, weight and acceleration as unverified, with no unit given. | `Appendix.md` Data Summary, Units |
| 6 | User confirmed that `auto-mpg.data` is the best available form of the data for this analysis. | `Appendix.md` Data Summary, Provenance |
| 7 | Admissibility 3 (grouped or time-ordered rows) asked and answered: rows with the same car name are kept together. Grouping computed for the record. | `Appendix.md` Decision Records, DR-02; `Code/Auto_MPG/03_group_sizes.py` |
| 8 | Admissibility 4 (new cases like these) asked and answered yes by the user. | `Appendix.md` Decision Records, DR-03 |
| 9 | User described their machine learning experience as beginner, in their own words. | `Appendix.md` Data Summary, Experience level |
| 10 | Admissibility 3, time part, asked. The user first chose a split that follows model year, then, after the workflow's rules were explained, chose a split by car name only. Model year stays an input; time-series modelling flagged out of scope. | `Appendix.md` Decision Records, DR-04 |
| 11 | Source of the copy asked: the user states it came from the UCI Machine Learning Repository. Download date not known. | `Appendix.md` Data Summary, Provenance |
| 12 | Licence checked on the UCI dataset page: CC BY 4.0, attribution required. The licence had not been checked before this request. | `Appendix.md` Data Summary, Provenance |
| 13 | Step 1 closed by the user. Still unconfirmed and carried into step 2: whether any input is built from the fuel figure (no such input found in the names file; not confirmed by the user). Draft Abstract written in `Project Report.md`. | `Project Report.md` Abstract; `Appendix.md` Data Summary |
| 14 | Two facts from step 1 confirmed by the user: no candidate input is built from the fuel figure (leakage check); the data was downloaded on 11 November 2026. Row 13 is corrected accordingly. | `Appendix.md` Data Summary, Provenance and Target and leakage |
| 15 | Step 2 started. User's problem recorded in its own words. Admissibility 2 (prediction or understanding) answered: predict. | `Appendix.md` Problem Definition, Discussion; Decision Records, DR-05 |
| 16 | Target chosen by the user: gallons used per 100 miles, computed from the recorded miles per gallon. | `Appendix.md` Problem Definition, Problem; Decision Records, DR-06 |
| 17 | Output type confirmed by the user: non-negative real (never below zero). | `Appendix.md` Problem Definition, Problem; Decision Records, DR-06 |
| 18 | Metric chosen by the user: root mean squared error (RMSE), in gallons used per 100 miles. | `Appendix.md` Problem Definition, Problem; Decision Records, DR-07 |
| 19 | Target changed by the user: litres per 100 km (235.2 ÷ miles per gallon, assuming US gallons) instead of gallons used per 100 miles. Inputs kept in recorded units. DR-06 superseded by DR-08; DR-07 units superseded. Range of y: about 5.0 to 26.1 litres per 100 km. | `Appendix.md` Problem Definition; Decision Records, DR-06 (superseded), DR-07 (units superseded), DR-08 |
| 20 | The user's success criterion recorded in their own words. Not yet turned into a testable rule; two points to clarify. | `Appendix.md` Problem Definition, Problem |
| 21 | Success criterion, first part clarified by the user: the agreed single number must be at most 1 litre per 100 km. The comparison with the average guess is still open. | `Appendix.md` Problem Definition, Problem |
| 22 | "Clearly better" set by the user as beating the average guess by more than the normal variation between the cross-validation folds. Which spread is meant is still open. | `Appendix.md` Problem Definition, Problem |
| 23 | The user chose the margin's own variation across the folds as the measure of normal variation for "clearly better". Whether the margin is checked on the test data is still open. | `Appendix.md` Problem Definition, Problem |
| 24 | The success criterion is complete as the user set it: the single number must be at most 1 litre per 100 km, and the margin over the average guess must be at least 1 times its variation across the training checks, checked once on the test data. | `Appendix.md` Problem Definition, Problem |
| 25 | Other measure to report alongside the main number, not used to decide: mean absolute error (MAE), in litres per 100 km. | `Appendix.md` Problem Definition, Problem; Decision Records, DR-09 |
| 26 | Must-have set by the user as explainable (DR-10), in error: the user meant no requirement. DR-10 superseded. | `Appendix.md` Decision Records, DR-10 (superseded) |
| 27 | Property 5 (interpretability) set by the user as no requirement, correcting the earlier answer. | `Appendix.md` Problem Definition, Problem; Decision Records, DR-11 |
| 28 | Property 6 (probabilities) set by the user as no requirement: a single figure is enough. | `Appendix.md` Problem Definition, Problem; Decision Records, DR-12 |
| 29 | Property 7 (extrapolation) set by the user as no: predictions only for cars like those in the data. | `Appendix.md` Problem Definition, Problem; Decision Records, DR-13 |
| 30 | Property 8 (expected shape) recorded in the user's words; shape unknown. | `Appendix.md` Problem Definition, Problem; Decision Records, DR-14 |
| 31 | Sub-tasks set by the user: one question, the fuel use of a new car from its engine, weight and size. | `Appendix.md` Problem Definition, Sub-tasks; Decision Records, DR-15 |
| 32 | Split made and locked: one in five cars held back as the test part, grouped by car name, seed 2026: 314 training and 78 test cars. | `Appendix.md` Decision Records, DR-16; `Code/Auto_MPG/04_split.py`; `Code/outputs/Auto_MPG/split_seed2026.csv` |
| 33 | Step 2 closed by the user. Property values recorded (DR-17). Property 3 (number of inputs) left open: whether model year, cylinders and origin count as categories, and whether one yes-or-no column per category is dropped. | `Appendix.md` Decision Records, DR-17 |
| 34 | Written at the close of step 2: Introduction, Methods (Data and evaluation), draft Abstract and References in `Project Report.md`. | `Project Report.md` |
| 35 | Sub-task wording changed by the user to: from its design, model year and country of origin. DR-15 wording superseded by DR-18. | `Appendix.md` Decision Records, DR-18; `Project Report.md` Introduction |
| 36 | Step 3 started with the open category questions. The user decided: model year and cylinders are numbers; country of origin is a category; one yes-or-no column per category is dropped. Input columns after encoding: 8. Property 3 closed. | `Appendix.md` Decision Records, DR-19 |
| 37 | Property 2 (ample), Property 3 (few) and Property 4 (low) recorded for the input design. Property 3 superseded in DR-17. | `Appendix.md` Decision Records, DR-17 (part superseded), DR-19 |
| 38 | Step 3: Figure 1 (histogram of fuel use, training cars only) drawn after the user agreed the chart. Added to Results under The training data. | `Code/Auto_MPG/05_fig1_fuel_histogram.py`; `Project Report.md` Results |
| 39 | Step 3: Figure 2 (fuel use against weight, one dot per training car) drawn after the user agreed the chart. Added to Results under The training data. | `Code/Auto_MPG/06_fig2_fuel_vs_weight.py`; `Project Report.md` Results |
| 40 | The Methods sub-heading The training data was merged into Data and evaluation at the user's instruction. This is consistent with `instructions.md`: the first pair of sub-headings is Data and evaluation in Methods and The training data in Results, and Results says The training data matches Data and evaluation in Methods. No rule change is needed. | `Project Report.md` Methods; `instructions.md`, Methods and Results |
| 41 | Step 3: Figure 3 (fuel use by origin code, training cars only) drawn after the user agreed the chart. Added to Results under The training data. | `Code/Auto_MPG/07_fig3_fuel_by_origin.py`; `Project Report.md` Results |
| 42 | Input design, choice of inputs, decided by the user: all seven candidate inputs are used. | `Appendix.md` Decision Records, DR-20 |
| 43 | Input design, transformations, decided by the user: none. Every input is used as recorded. | `Appendix.md` Decision Records, DR-21 |
| 44 | Input design, car name, decided by the user: left out as an input; used only as the group column for the split. | `Appendix.md` Decision Records, DR-22 |
| 45 | Step 3 closed by the user. Properties 9 and 10 recorded as not applicable (numeric output, DR-23). Draft Abstract updated in Project Report.md. | `Appendix.md` Decision Records, DR-23; `Project Report.md` Abstract |

## Code Summary

- `Code/Auto_MPG/02_compare_dropped_cars.py`: descriptive comparison of the 6 cars with no horsepower value against the other 392, for step 1. Reads `Attachments/Auto MPG/auto-mpg.data` and writes nothing. Run from `Code/` with `uv run python Auto_MPG/02_compare_dropped_cars.py`. No random numbers.
- `Code/Auto_MPG/03_group_sizes.py`: counts of rows that share a car name, for the grouping decision. Reads the raw file and writes nothing. Run from `Code/` with `uv run python Auto_MPG/03_group_sizes.py`. No random numbers.
- `Code/Auto_MPG/04_split.py`: the locked train/test split, one in five cars held back, grouped by car name, seed 2026. Writes `Code/outputs/Auto_MPG/split_seed2026.csv` (one row per used car, with its set). Run from `Code/` with `uv run python Auto_MPG/04_split.py`. Seed 2026; the file is not to be read for the test rows before the final evaluation.
- `Code/Auto_MPG/05_fig1_fuel_histogram.py`: Figure 1, a histogram of fuel use for the 314 training cars. Reads the raw file and `Code/outputs/Auto_MPG/split_seed2026.csv`; writes the light and dark PNG files and the summary text. Run from `Code/` with `uv run python Auto_MPG/05_fig1_fuel_histogram.py`. No random numbers; uses the locked split (seed 2026), training cars only.
- `Code/Auto_MPG/06_fig2_fuel_vs_weight.py`: Figure 2, fuel use against weight, one dot per training car. Reads the raw file and the split file; writes the light and dark PNG files. Run from `Code/` with `uv run python Auto_MPG/06_fig2_fuel_vs_weight.py`. No random numbers; training cars only.
- `Code/Auto_MPG/07_fig3_fuel_by_origin.py`: Figure 3, fuel use by origin code, one dot per training car, with each column's median. Reads the raw file and the split file; writes the light and dark PNG files. Run from `Code/` with `uv run python Auto_MPG/07_fig3_fuel_by_origin.py`. Jitter seed 2026; training cars only.
- `Code/Auto_MPG/01_describe_data.py`: describing pass on the raw Auto MPG files for step 1. It reads `Attachments/Auto MPG/auto-mpg.data` and `auto-mpg.data-original`, prints counts, missing values, ranges and category counts, and writes nothing. Run from `Code/` with `uv run python Auto_MPG/01_describe_data.py`. It uses no random numbers, so no seed applies. It needs pandas, which is in `Code/pyproject.toml`.

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). *Machine Learning – A First Course for Engineers and Scientists*. 2nd edition, online draft version of 1 September 2026. [smlbook.org](https://smlbook.org/). Checked 2026-11-15 against the local copy in `Attachments/smlbook/`.
- Quinlan, R. (1993). Auto MPG [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5859H](https://doi.org/10.24432/C5859H). Licence CC BY 4.0 (stated on the dataset page, checked 2026-11-14). Downloaded 11 November 2026 (stated by the user).

