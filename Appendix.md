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

### DR-24 · ADMSET · step 4a

- **Type:** ADMSET
- **Step:** 4a
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** Which of the 14 structural configurations are admissible, given the property values?
- **Reference code:** `Code/Auto_MPG/core.py`, function `main`; code version sha256:4aa2a3fc8c590cf0afe956fe97f4c17158cddb8c5d147d6c2d9e0db55df7ebb9 (interim core, not reviewed); inputs passed: `Code/Auto_MPG/props.json`, the training rows from `Code/outputs/Auto_MPG/split_seed2026.csv`; output `Code/outputs/Auto_MPG/core_admset.json`.

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | non-negative real | M (user) | DR-06, DR-08 |
| Must-haves | none | M (user) | DR-11, DR-12, DR-13 |
| Property 9 and 10 | not applicable (numeric output) | n/a | DR-23 |
| Training rows | 314 | T | DR-16 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, non-negative real (`ML Guide.md` section 12) | Exponential, Linear, k-NN and Tree admissible; Logistic and Poisson not | [B SML pp. 17, 63] | Logistic (4 configurations) and Poisson (2) removed, code EXCL |
| Must-have requirements (section 12) | None set | n/a | No configuration removed with code USER |
| MOD-1, separability (section 12) | Not applicable: numeric output | n/a | None |
| MOD-2, collinearity or parameters at least the training rows (section 12) | Checked for Linear, Linear + poly and Exponential, without L2: 9, 21 and 9 parameters against 314 rows; each design has full rank once columns are standardised | [B→I SML pp. 46–47, 61, 63, 65] | No configuration removed by MOD-2 |

**Thresholds applied:** none (MOD-2 uses the exact-rank test, not a threshold)

**Options considered:** the 14 structural configurations of section 9

**Expectation:** n/a

**Decision:** Eight configurations are admissible: Linear, Linear + L2, Linear + poly, Linear + poly + L2, Exponential, Exponential + L2, kNN and Tree. Six are removed by the task gate (EXCL): Logistic, Logistic + L2, Logistic + poly, Logistic + poly + L2, Poisson and Poisson + L2.

**Why not:**

| Configuration | Code | Evidence |
| --- | --- | --- |
| Logistic | EXCL | Task gate: not admissible for a non-negative real output |
| Logistic + L2 | EXCL | Task gate, as above |
| Logistic + poly | EXCL | Task gate, as above |
| Logistic + poly + L2 | EXCL | Task gate, as above |
| Poisson | EXCL | Task gate: Poisson is for counts |
| Poisson + L2 | EXCL | Task gate, as above |

**Correction recorded:** the first run of the interim core flagged Linear + poly under MOD-2, because the unstandardised polynomial columns gave a false rank deficiency (rank 20 of 21). The core was corrected before its output was used: exact collinearity is tested on standardised columns (rank 21 of 21). The corrected run is the one recorded here.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** informed: the admissible set follows from the properties the user has given; no user choice is needed at this stage.

**Supersedes / superseded by:** n/a

**Links:** `Code/Auto_MPG/core.py`; `Code/Auto_MPG/props.json`; `Code/outputs/Auto_MPG/core_admset.json`

### DR-25 · PRIOR · step 4b

- **Type:** PRIOR
- **Step:** 4b
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** Which admissible configurations are tried first, and which are kept for cross-validation, given the property values, before any model is trained?
- **Reference code:** `Code/Auto_MPG/core_prior.py`, code version sha256:062a113552100c3a9eebdb49df958d69e310b4ff8bc745e5fd944fcda091c5ee (interim core, not reviewed); admissible set from `Code/Auto_MPG/core.py`, code version sha256:4aa2a3fc8c590cf0afe956fe97f4c17158cddb8c5d147d6c2d9e0db55df7ebb9 (DR-24); inputs passed: `Code/Auto_MPG/props.json`; output `Code/outputs/Auto_MPG/core_prior.json`.

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | non-negative real | M | DR-06, DR-08 |
| Property 2: data-to-parameter ratio | ample | M (computed) | DR-19 |
| Property 3: number of inputs | few (8 columns) | M (computed) | DR-19 |
| Property 4: categorical share | low | M (computed) | DR-19 |
| Properties 5, 6, 7 | none, no, no | M (user) | DR-11, DR-12, DR-13 |
| Property 8: expected shape | unknown | M (user) | DR-14 |
| Properties 9 and 10 | not applicable | n/a | DR-23 |

Only the Property 1 row of the suitability matrix is known to apply, so only it is scored: Linear −1, Exponential +1. Property 2 and Property 3 have entries only for the "limited" and "many" values, which do not hold. Unknown and not-applicable properties contribute nothing.

**Ranking (admissible set, highest score first; ties broken by fewer add-ons):**

| Rank | Configuration | Score | Add-ons | Kept or not |
| --- | --- | --- | --- | --- |
| 1 | Exponential | +1 | 0 | kept |
| 2 | Exponential + L2 | +1 | 1 | kept |
| 3 | kNN | +0 | 0 | kept |
| 3 | Tree | +0 | 0 | kept |
| 4 | Linear | -1 | 0 | DISF |
| 5 | Linear + L2 | -1 | 1 | DISF |
| 5 | Linear + poly | -1 | 1 | DISF |
| 6 | Linear + poly + L2 | -1 | 2 | DISF |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 1: output type = non-negative real, suitability row (section 13) | Linear −1; Poisson·exponential +1 | [B SML p. 62]; [B SML pp. 61–62] | Exponential +1; Linear −1; k-NN and Tree 0 |
| SEQ-1 (section 14) | The baseline is always included | [B SML pp. 330–331] | Kept |
| SEQ-2 (section 14) | Simple-first: the plain parametric model for a non-negative real output, taken as Exponential | [I] (the guide's own reading for exponential as simple-first) | Kept; see the open point below |
| Keep rule (section 15, step 4) | The baseline, the simple-first, the three highest-ranked others, and any tie at the third place | [I] | Exponential + L2, k-NN and Tree kept; no tie at the cut |

**Thresholds applied:** none (the prior uses no numeric threshold)

**Options considered:** the eight admissible configurations (DR-24)

**Expectation:** The prior ranks the exponential family first for a non-negative real output, so the expected cross-validation order is: Exponential and Exponential + L2 close together, ahead of k-NN and Tree; all of them ahead of the baseline. The L2 version carries one add-on that the prior does not expect to help. This is what the advisor can know before fitting; the prior does not decide.

**Decision:** Keep the baseline, Exponential (simple-first), Exponential + L2, k-NN and Tree for cross-validation. Linear, Linear + L2, Linear + poly and Linear + poly + L2 are not kept.

**Why not:**

| Configuration | Code | Evidence |
| --- | --- | --- |
| Linear | DISF | Ranked 4th of 6 with score −1; not one of the three highest-ranked others |
| Linear + L2 | DISF | Score −1, one add-on; not kept after the ranking |
| Linear + poly | DISF | Score −1, one add-on; not kept after the ranking |
| Linear + poly + L2 | DISF | Score −1, two add-ons; not kept after the ranking |

**Open point for the user:** the simple-first rule (SEQ-2) names the plain parametric model for the task. For a non-negative real output, Linear is also admissible. Taking Exponential as the simple-first is our reading. If Linear is to be the simple-first, it is kept as well and cross-validated in round 1.

**Confidence:** n/a

**Outcome vs expectation (filled at 4d, DR-29): partial.** Agreed: the two exponential models are close to each other, both beat the baseline, and the decision tree is behind them. Disagreed: the nearest-cases method is not behind the exponential models; on this measure it has the lowest cross-validation error of the five kept configurations, and the straight-line model (not in the prior's kept set, added by the user) is also ahead of the exponential model in round 1. The penalty version was not ahead of the plain exponential model, as expected. Recorded as a finding; not explained away.

**User involvement:** informed: the ranking and the kept set are presented for agreement at 4b; no cross-validation has been run.

**Supersedes / superseded by:** n/a

**Links:** `Code/Auto_MPG/core_prior.py`; `Code/outputs/Auto_MPG/core_prior.json`; `Appendix.md` Decision Records, DR-24

### DR-26 · PRIOR · step 4b (user amendment and approval of the interim core)

- **Type:** PRIOR (amendment: the simple-first set and approval of the interim core)
- **Step:** 4b
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** Which configurations are cross-validated in round 1, and is the interim core approved for use?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Prior kept set (core) | baseline, Exponential, Exponential + L2, kNN, Tree | M (computed) | DR-25; `Code/outputs/Auto_MPG/core_prior.json` |
| User's choice on the simple start | "Also the straight-line model": Linear is kept and cross-validated in round 1, alongside Exponential | M (user) | Question put to the user at 4b |
| Approval of the script | "Approve the script" (`Code/Auto_MPG/core.py`, `Code/Auto_MPG/core_prior.py`, not reviewed by anyone else) | M (user) | Question put to the user at 4b |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-2 (section 14), simple-first | The simple start is the plain parametric model for the task; the user adds the straight-line model to the simple starts | [B SML p. 331]; the user's choice | Linear is kept; it was DISF in DR-25 and is no longer DISF |
| Interim core (`Machine Learning Scope and Reasoning`) | Approved by the user before its outputs are used | n/a | Results of `core.py` (DR-24) and `core_prior.py` (DR-25) may be used |

**Thresholds applied:** none

**Options considered:** (a) Exponential only as the simple start; (b) Exponential and Linear as simple starts. Chosen: (b), by the user.

**Expectation:** n/a

**Decision:** Round 1 cross-validates the baseline, Exponential and Linear. Round 2 cross-validates Exponential + L2, kNN and Tree. The interim core is approved for use.

**Why not:** (a) was not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Approve the script"; "Also the straight-line model".

**Supersedes / superseded by:** amends the kept set of DR-25: Linear is kept (DISF removed for it).

**Links:** `Appendix.md` Decision Records, DR-25; `Code/Auto_MPG/core_prior.py`

### DR-27 · PRIOR · step 4b (cross-validation protocol)

- **Type:** PRIOR (cross-validation protocol, agreed at 4b)
- **Step:** 4b
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** How are the configurations compared, and how are their settings chosen?

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Grouping | rows with one car name are kept in the same part | M (DR-02) | DR-02 |
| Outer checking | ten parts of the training cars, shuffled with seed 2026; the same parts for every configuration | M (user agreed the protocol at 4b) | `ML Guide.md` section 16 |
| Settings | chosen inside each outer training part by five further parts (grouped) | M (user agreed) | `ML Guide.md` section 16 |
| Selection measure | root mean squared error, in litres per 100 km | M (DR-07) | DR-07 |
| Test set | 78 cars, locked until the single final evaluation | M (DR-16) | DR-16 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Outer checking, ten parts (section 16) | ten shuffled parts, same for every configuration | [B SML pp. 72–73] | The comparison uses the same parts |
| Group folds (section 16) | parts kept together by car name | [B SML p. 329] | No car name is on both sides of a check |
| Hyperparameter tuning (section 16) | five further parts inside each outer training part | [I]; tuning on the checking parts would make them optimistic [B SML p. 74] | Settings are chosen without touching the held-back part |
| Scaling for k-NN and penalised fits (REQ-2, REQ-3, REQ-1) | scaling fitted inside each training part only | [B SML pp. 26–27]; [I] | No information leaks from the held-back part |
| Exponential model (section 9, implementation notes) | fitted as a gamma regression with a logarithmic link | [I] | The exponential model of the workflow |
| Grids (section 16) | k in {1, 3, 5, 7, 9, 15, 21, 31, 51}; tree depth and leaf size; penalty strength over a grid of powers of ten | [I] | Settings searched over these grids |

**Thresholds applied:** none beyond the grids above

**Options considered:** the protocol of section 16 of the guide, as set out in 4b

**Expectation:** n/a

**Decision:** Ten outer parts, grouped by car name, shuffled with seed 2026; five inner parts for settings; the same outer parts for every configuration; the root mean squared error as the measure; the test cars locked.

**Why not:** n/a (no alternative was put forward by the user)

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Agree the methods and the checking".

**Supersedes / superseded by:** n/a

**Links:** `ML Guide.md` section 16; `Code/outputs/Auto_MPG/split_seed2026.csv`

### DR-28 · CV · step 4c (round 1)

- **Type:** CV
- **Step:** 4c
- **Sub-task:** the one sub-task
- **Date:** 2026-11-15
- **Question:** How do the simple-first configurations compare with the baseline in cross-validation, and does the simple-first beat the baseline clearly (SEQ-3)?
- **Reference code:** `Code/Auto_MPG/core_cv.py`, code version sha256:8f4859c2c13bb6e26e38f4f02e010c6e9aaca860091b7d8cda462a0ff4f9cde7 (interim core, not reviewed); inputs: training rows (314), outer parts from seed 2026, `Code/Auto_MPG/props.json`; output `Code/outputs/Auto_MPG/core_cv_round1.json`.

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Outer parts | ten, grouped by car name, seed 2026; sizes [31, 31, 31, 31, 32, 31, 31, 31, 31, 34] | CV | DR-27 |
| Measure | root mean squared error, litres per 100 km | CV | DR-07 |
| Training rows used | 314 (the test cars are not read) | T | DR-16 |

**CV table (round 1)**

| Configuration | Post-prior | Tuned hyperparameters | CV mean (RMSE) | Margin vs baseline (mean) | Spread of margin (SD) | Margin / spread | E_train (mean) | E_val (mean) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (mean of training outputs) | no | n/a | 3.950 | n/a | n/a | n/a | 3.968 | 3.950 |
| Exponential (simple-first, SEQ-2) | no | none (no penalty) | 1.418 | 2.532 | 0.672 | 3.768 | 1.391 | 1.418 |
| Linear (simple start, added by the user) | no | none (no penalty) | 1.381 | 2.569 | 0.585 | 4.391 | 1.354 | 1.381 |

Margins are the baseline's fold error minus the model's fold error, so positive means better than the baseline. The spread is the standard deviation of the ten fold margins (section 16, not the standard error).

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 (section 14): continue once the simple-first beats the baseline | Exponential margin / spread = 3.768, at least 1 (C2 threshold, ours) | [B SML pp. 331–332]; threshold [I] | Round 2 may proceed; no DX-1 |
| C2, margin over the baseline (section 17) | Linear and Exponential both clear, at margin / spread 4.391 and 3.768 | [I] | Recorded for 4d and 4f |

**Thresholds applied:** margin at least 1 times the spread (C2, ours). Value used: Exponential 3.768; Linear 4.391.

**Options considered:** the baseline, Exponential and Linear (round 1, DR-26)

**Expectation:** n/a (round 1 has no expectation of its own; the expectation for the order is in DR-25)

**Decision:** The simple-first configurations beat the baseline clearly; round 2 is run. No diagnosis pass is needed at this point.

**Why not:** n/a

**Confidence:** n/a (selection confidence is computed at 4f)

**Outcome vs expectation:** n/a for round 1 (the prior's expectation in DR-25 is filled in at 4d, after round 2)

**User involvement:** informed: round 1 ran as agreed at 4b (DR-26, DR-27). **Approved:** the script `Code/Auto_MPG/core_cv.py` was written in step 4c, after the scripts were approved at 4b, and its output was recorded before the user had seen it. The user approved the script on 2026-11-17 after it was described in plain words, and the round 1 results stand.

**Supersedes / superseded by:** n/a

**Links:** `Code/Auto_MPG/core_cv.py`; `Code/outputs/Auto_MPG/core_cv_round1.json`

### DR-29 · CV · step 4d (round 2)

- **Type:** CV
- **Step:** 4d
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** How do the remaining kept configurations compare with the baseline and round 1 on the same ten outer parts, with their settings chosen inside each part?
- **Reference code:** `Code/Auto_MPG/core_cv_round2.py`, code version sha256:631bea526162473fe9860ea626f29bac94e02a3ed0fad02057ae862ccffff5e3 (interim core, approved by the user on 2026-11-17); it imports the approved round 1 functions from `Code/Auto_MPG/core_cv.py` (approved 2026-11-17); inputs: 314 training rows, outer parts from seed 2026; output `Code/outputs/Auto_MPG/core_cv_round2.json`.

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Outer parts | ten, grouped by car name, seed 2026; sizes [31, 31, 31, 31, 32, 31, 31, 31, 31, 34] (the same as round 1) | CV | DR-27 |
| Inner parts | five, grouped by car name, inside each outer training part, seed 2026 | CV | DR-27 |
| Grids | penalty strength 1e-4 to 1e4 in powers of ten; k in {1, 3, 5, 7, 9, 15, 21, 31, 51}; tree depth {1, 2, 3, 4, 5, 6, 8, 10, 15, 20} with leaf size {1, 5, 10, 20} | CV | DR-27 |
| Measure | root mean squared error, litres per 100 km | CV | DR-07 |

**CV table (round 2, with round 1 for reference)**

| Configuration | Post-prior | Tuned hyperparameters (most common across outer parts) | CV mean (RMSE) | Margin vs baseline (mean) | Spread of margin (SD) | Margin / spread | E_train (mean) | E_val (mean) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline (mean of training outputs) | no | n/a | 3.950 | n/a | n/a | n/a | n/a | 3.950 |
| Exponential + L2 (round 2) | no | penalty strength 0.0001 (by part: 0.01, 0.1, 0.0001, 0.0001, 0.0001, 0.1, 0.0001, 0.0001, 0.0001, 0.0001) | 1.445 | 2.504 | 0.682 | 3.675 | 1.400 | 1.445 |
| kNN (round 2) | no | k = 3 (by part: 5, 3, 5, 3, 5, 5, 3, 3, 3, 3) | 1.315 | 2.635 | 0.561 | 4.696 | 1.009 | 1.315 |
| Tree (round 2) | no | depth 6, leaf 5 (by part: (6, 5), (6, 1), (6, 10), (6, 5), (6, 1), (5, 1), (4, 1), (5, 1), (8, 10), (6, 5)) | 1.629 | 2.321 | 0.553 | 4.199 | 1.007 | 1.629 |

For reference, from round 1 (DR-28): Exponential 1.418; Linear 1.381; baseline 3.950.

Margins are the baseline's fold error minus the model's fold error, so positive means better than the baseline. The spread is the standard deviation of the ten fold margins.

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Settings tuned inside each outer part (section 16) | five inner parts, lowest mean inner error chosen | [I] | The outer parts were not used to choose settings |
| REQ-2, REQ-3, REQ-1 | scaling fitted inside each training part | [B SML pp. 26–27]; [I] | No leak from the held-back part |
| C2, margin over the baseline (section 17) | Exponential + L2 3.675; kNN 4.696; Tree 4.199 (each at least 1) | [I] | Recorded for 4f |

**Observations recorded, not interpreted here:** the gap between training and held-back error is small for the exponential models (about 0.026 for Exponential in round 1), and large for kNN (0.306) and Tree (0.622). These gaps are an input to the diagnosis at 4e.

**Thresholds applied:** margin at least 1 times the spread (C2, ours); each of the three margins is above 1.

**Options considered:** the three remaining kept configurations (DR-25, with the user's choice in DR-26)

**Expectation:** n/a (the expectation is in DR-25)

**Decision:** Round 2 is recorded as run on the same outer parts. The outcome against the prior's expectation is recorded in DR-25 (partial).

**Why not:** n/a

**Confidence:** n/a (computed at 4f)

**Outcome vs expectation:** n/a (see DR-25)

**User involvement:** asked, approved the script on 2026-11-17 before the run.

**Supersedes / superseded by:** n/a

**Links:** `Code/Auto_MPG/core_cv_round2.py`; `Code/outputs/Auto_MPG/core_cv_round2.json`; `Code/outputs/Auto_MPG/core_cv_round1.json`

### DR-30 · DX · step 4e (diagnosis pass 1)

- **Type:** DX
- **Step:** 4e
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** For the leading configuration, which observation holds first, and what action follows (section 18)?
- **Reference code:** observations computed from `Code/outputs/Auto_MPG/core_cv_round1.json` and `Code/outputs/Auto_MPG/core_cv_round2.json` (approved scripts, DR-28 and DR-29). No new program was run for this pass.

**Leading configuration:** kNN (lowest cross-validation error of the kept set, 1.315 litres per 100 km; DR-29).

**Observation → action**

| ID | Observation | Test | Result | Values |
| --- | --- | --- | --- | --- |
| O1 | Does not beat the baseline | C2 = not clear | does not hold | margin / spread 4.696 (C2 clear, at least 1) |
| O2 | Training error already above what the application needs | error on training parts worse than the success criterion (1 litre per 100 km) | **holds** | mean 1.009 against 1.0; 4 of 10 parts above 1.0 |
| O5 | Tuned setting at the edge of its grid | selected value at the smallest or largest grid value in most outer parts | does not hold | k = 3 in 6 parts, k = 5 in 4; not at the edge of {1 … 51} |
| O3 | Overfitting | gap ≥ 2 × training error | does not hold | gap 0.306 against 2 × 1.009 = 2.018 |
| O4 | Underfitting | training error ≥ 2 × gap | would hold (1.009 ≥ 0.612), but O2 comes first | not used |
| O6 | More data likely to help | C3 = limited | not evaluated | C3 is computed at 4f; not needed for this pass |

**Action taken:** DX-2: stop and rethink the problem and the method with the user (`[B SML p. 78]`). The loop pauses here until the user answers.

**Stopping check (S1–S6):** none of S1 to S6 applies yet. The pause is for the user, not a stopping rule.

**Thresholds applied:** O2 uses the success criterion of 1 litre per 100 km (agreed in step 2); O3 and O4 use the ratio of 2 in the guide (ours, `[I]`); O5 uses the grid edge.

**Expectation:** n/a (DX-2 does not change the configurations, so there is no CV result to expect)

**Decision:** Pause the loop and ask the user about the 1-litre limit: the error on the training cars is at or just above it for the leading method, so the limit may not be reachable with these methods on this data.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: keep the 1-litre limit and carry on with the checks (2026-11-17). See DR-31.

**Supersedes / superseded by:** n/a

**Links:** `Code/outputs/Auto_MPG/core_cv_round2.json`; `Appendix.md` Decision Records, DR-27 and DR-29

### DR-31 · DX · step 4e (user's answer to DX-2)

- **Type:** DX
- **Step:** 4e
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** After DX-2 (rethink the problem with the user), should the 1-litre limit change, and how should the loop continue?
- **Reference code:** none (a decision by the user; no calculation)

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| Observation O2 (training error at or above the limit) | holds for the leading method (1.009 against 1.0) | M (from DR-30) | DR-30 |
| User's answer | "Keep the 1-litre limit and carry on with the checks" | M | Question put to the user at 4e |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| DX-2 (section 18) | The user keeps the limit; the problem is not changed | `[B SML p. 78]` | Formulation unchanged; the success criterion stays as agreed in step 2 |
| Order of observations (section 18) | O2 still holds after DX-2, because the limit is unchanged; the rules give no action that moves past it without changing the problem or the data | n/a | Open point: see the decision below |

**Thresholds applied:** the success criterion of 1 litre per 100 km (agreed in step 2)

**Options considered:** (a) keep the limit; (b) change the limit to a level the user chooses; (c) stop. Chosen: (a), by the user.

**Expectation:** n/a

**Decision:** The limit stays at 1 litre per 100 km. The guide does not say what the loop does next when O2 still holds after DX-2 with the limit kept. The next action is therefore put to the user, rather than chosen by the agent.

**Why not:** (b) and (c) were not chosen by the user.

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "Keep the 1-litre limit and carry on with the checks".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Decision Records, DR-30

### DR-32 · DX · step 4e (diagnosis pass 2, pending approval)

- **Type:** DX
- **Step:** 4e
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** After the user chose to try more flexible models (DR-31), which observation holds next, and what action follows?
- **Reference code:** `Code/Auto_MPG/core_cv_round3.py`, code version sha256:cdea08943a39ab2b3faa71ebf04361ec5fa23d96c58aeefd3fe1f0e0256aa63a (interim program, approved by the user on 2026-11-17 after a plain-words description).

**Observations (from the approved round 1 and round 2 outputs, DR-28 and DR-29)**

| ID | Observation | Result | Values |
| --- | --- | --- | --- |
| O1 | does not beat the baseline | does not hold | margin / spread 4.696 for the leading method |
| O2 | training error above the limit | holds, but already answered by the user (DR-31) | 1.009 against 1.0 |
| O5 | tuned setting at the grid edge | does not hold for the leading method | k = 3 or 5 |
| O3 | overfitting | does not hold | gap 0.306 against 2 × 1.009 |
| O4 | underfitting | **holds**: training error ≥ 2 × gap (1.009 ≥ 0.612) | first observation left to act on |
| O6 | more data likely to help | not evaluated | C3 is computed at 4f |

**Action (DX-5, section 18):** add polynomial terms, since the number of inputs is few (Property 3, DR-19). The leading method is the nearest-cases method, which does not take polynomial terms, so the action applies to the straight-line model: **Linear + poly**, a post-prior configuration (admissible, DR-24; it was not kept at 4b, DR-25). It is checked on the same ten groups, with the degree (2 or 3) chosen inside each training part (DR-27 protocol).

**Also required by DX-5:** asking the user whether more input measurements exist. Not yet asked.

**Stopping check (S1–S6):** none applies.

**Thresholds applied:** margin at least 1 times the spread (C2, ours); O3 and O4 ratio of 2 (ours).

**Expectation:** Linear + poly should lower the error on the training cars, since the observation says the model is too simple for them. Whether it also lowers the error on held-back groups is the question; the advisor does not expect a large gain, since the straight-line model's gap is already small (about 0.03 in round 1). This is a prediction to be checked, not a finding.

**Decision:** Propose the check of Linear + poly on the same ten groups, once the user has approved the program that runs it.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** pending

**User involvement:** asked, answered (DR-31): try more flexible models. Program approved on 2026-11-17.

**Supersedes / superseded by:** n/a

**Links:** `Code/Auto_MPG/core_cv_round3.py`; `Appendix.md` Decision Records, DR-30, DR-31

### DR-33 · CV · step 4e (diagnosis pass 2, result)

- **Type:** CV (post-prior configuration, added by the diagnosis loop)
- **Step:** 4e
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** Does Linear + poly, checked on the same ten groups, beat the leading method (nearest cases) or the simple starts?
- **Reference code:** `Code/Auto_MPG/core_cv_round3.py`, code version sha256:cdea08943a39ab2b3faa71ebf04361ec5fa23d96c58aeefd3fe1f0e0256aa63a; output `Code/outputs/Auto_MPG/core_cv_round3.json`.

**CV table (post-prior)**

| Configuration | Post-prior | Tuned hyperparameters | CV mean (RMSE) | Margin vs baseline (mean) | Spread of margin (SD) | Margin / spread | E_train (mean) | E_val (mean) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Linear + poly | yes | degree 3 (degree 2 in 3 parts) | 1.328 | 2.622 | 0.541 | 4.847 | 1.236 | 1.328 |

For comparison (DR-28, DR-29): nearest cases 1.315, exponential with penalty 1.445, tree 1.629.

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Post-prior configuration (section 18) | Linear + poly added and checked on the same parts | [I] | Counts for the breadth note, not for prior agreement |
| Stopping check, S3 (section 18) | Two consecutive passes with no gain of at least 0.5 × spread: only one pass has changed the configurations so far | [I] | S3 not yet met |
| Leading configuration | Unchanged: nearest cases, 1.315, is still lower than Linear + poly, 1.328 | n/a | Observations recomputed at the next pass |

**Observations for the next pass:** O2 (error on training cars above the limit) still holds for the leader. O4 (underfitting) still holds for the leader. No configuration with a lower error than the leader has been found.

**Action taken:** DX-5 applied in full except one part: adding polynomial terms (this pass). The remaining part of DX-5 is to ask whether more input measurements exist; that question is put to the user next.

**Thresholds applied:** margin at least 1 times the spread (C2, ours)

**Options considered:** Linear + poly (post-prior)

**Expectation:** Linear + poly should lower the error on training cars (it does: 1.236, against 1.354 for the straight-line model in round 1) and should not gain much on held-back groups.

**Decision:** Linear + poly does not change the leader. The next step is to ask the user about more input measurements.

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** the lowering of the training error was as expected; the held-back error (1.328) is near the leader's and above it, which is consistent with the expectation of no large gain. Agree.

**User involvement:** informed; program approved on 2026-11-17.

**Supersedes / superseded by:** n/a

**Links:** `Code/Auto_MPG/core_cv_round3.py`; `Code/outputs/Auto_MPG/core_cv_round3.json`; DR-32

### DR-34 · DX · step 4e (answer to DX-5, and the stopping rule)

- **Type:** DX
- **Step:** 4e
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** Are there more input measurements to try (DX-5), and does a stopping rule now apply (S1 to S6)?
- **Reference code:** none new (a decision by the user; the stopping check uses the recorded results in DR-28, DR-29 and DR-33)

**Evidence**

| Item | Value | Evidence tag | Where |
| --- | --- | --- | --- |
| User's answer on more measurements | "No, these seven are all there are" | M | Question put to the user at 4e |
| Pass 1 (DX-2) | no change to any configuration; the user kept the limit | M | DR-30, DR-31 |
| Pass 2 (DX-5, polynomial terms) | the leading method unchanged; Linear + poly did not beat it | CV | DR-33 |
| Leader's spread across parts (SD of its margins over the baseline) | 0.561 (round 2); half of it is 0.280 | CV | DR-29 |
| Gain in the leader's error from pass 2 | none: 1.315 before, 1.315 after | CV | DR-29, DR-33 |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| DX-5 (section 18) | Both parts done: polynomial terms tried (DR-33); more measurements: none (user) | [B SML pp. 333–334] | DX-5 is exhausted |
| S3 (section 18): two consecutive passes give no gain of at least 0.5 × spread | Pass 1 and pass 2 both gave no gain | [I] | **Applies: stop** |
| S1, S2, S4, S5, S6 | S1 not met (the limit is not met on the training cars); S2 not stated; S4 not applicable; S5 not requested; S6 (five passes) not reached | n/a | None applies beyond S3 |
| DX-6 (more data likely to help, O6) | Not evaluated: the loop stops at S3 first | n/a | Not used |

**Thresholds applied:** no gain of at least 0.5 × spread (S3, ours). The spread used is 0.561 (leader, round 2); the gain is zero.

**Options considered:** (a) stop the loop now (S3); (b) try further configurations (none is left by the rules).

**Expectation:** n/a

**Decision:** The diagnosis loop stops under S3. The leading method stays nearest cases, with CV mean error 1.315 litres per 100 km (DR-29). The next step is the recommendation (4f).

**Why not:** n/a

**Confidence:** n/a

**Outcome vs expectation:** n/a

**User involvement:** asked, answered: "No, these seven are all there are".

**Supersedes / superseded by:** n/a

**Links:** `Appendix.md` Decision Records, DR-29, DR-30, DR-31, DR-33

### DR-35 · FINAL · step 4f (recommendation, before the test set)

- **Type:** FINAL (part 1: recommendation and confidence; the test result is added at 4g)
- **Step:** 4f
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** Which configuration is recommended, and how sure is the choice (section 19 and section 17)?
- **Reference code:** `Code/Auto_MPG/core_recommend.py`, code version sha256:63165b95dbe1fe973ab8427a27bbc68437ab47c190e57a21c7c4041700070348 (interim program, approved by the user on 2026-11-17); inputs: the approved checking results (`core_cv_round1.json`, `core_cv_round2.json`, `core_cv_round3.json`); output `Code/outputs/Auto_MPG/core_recommend.json`. The test set has not been read.

**Section 19 trace**

| Step | Result |
| --- | --- |
| 1. Eligible (C2 clear, no must-haves set) | all six configurations checked: Linear, Exponential, Exponential + L2, kNN, Tree, Linear + poly |
| 2. Best CV mean | kNN, 1.315 |
| 2. Candidates (margin to kNN below half a spread) | kNN, Linear (0.066 against half-spread 0.095), Linear + poly (0.013 against 0.109) |
| 3. Choose (fewest add-ons, then prior score, then CV mean) | kNN: no add-ons, prior score 0; Linear: no add-ons, prior score −1; so kNN |
| Chosen | kNN, with k tuned inside each part (most often 3) |

**Selection confidence (section 17)**

| Factor | Value | Rule |
| --- | --- | --- |
| C1 margin over the runner-up (Linear + poly) | none: margin 0.013, spread 0.218, ratio 0.059 | clear if at least 1 × spread; moderate 0.5 to 1; none below 0.5 |
| C2 margin over the baseline | clear: margin 2.635, spread 0.561 | clear if at least 1 × spread |
| C3 data adequacy | adequate: error at 80 % 1.394, at 100 % 1.315; drop 0.079, against half the fold spread 0.152 | limited if still falling by at least half a spread |
| **Selection confidence** | **Low** (C1 = none) | High needs C1 clear; Low if C1 is none or C2 is not clear |

**Reported alongside, not combined into the level**
- Prior agreement: **disagree**. The prior expected the exponential model first; cross-validation ranks the nearest-cases method first (DR-25, DR-29).
- Grounding: the nearest-cases method has prior score 0 with no matrix entries, so no [B], [B→I] or [I] entries stand behind its prior score.
- Breadth note: six configurations were compared, plus the baseline; the note for more than ten does not apply.

**Why not (all 14 structural configurations except the recommendation, each with one code)**

| Configuration | Code | Evidence |
| --- | --- | --- |
| Logistic, Logistic + L2, Logistic + poly, Logistic + poly + L2 (4) | EXCL | Not admissible for a non-negative real output (DR-24) |
| Poisson, Poisson + L2 (2) | EXCL | Not admissible for a non-negative real output (DR-24) |
| Linear + L2, Linear + poly + L2 (2) | DISF | Admissible but not kept after the prior ranking (DR-25) |
| Linear (margin 0.066, below half a spread) | SIMP | Could not be told apart from the recommendation; no add-ons in either; the prior score chose kNN (DR-25) |
| Linear + poly (margin 0.013, below half a spread) | SIMP | Could not be told apart; the recommendation has fewer add-ons (DR-33) |
| Exponential (margin 0.103, spread 0.201) | OUTP | Recommendation ahead, but the margin is moderate (about half a spread), not clear. The guide's codes name no moderate case; OUTP is the closest (ours, flagged for the user) |
| Exponential + L2 (margin 0.130, spread 0.203) | OUTP | As above (moderate margin) |
| Tree (margin 0.314, spread 0.314) | OUTP | Clearly behind: margin at least one spread |

**Thresholds applied:** candidates below half a spread (section 19, step 2); C1 at 1 and 0.5 spread; C2 at 1 spread; C3 at half the fold spread (ours, `[I]`)

**Options considered:** the six configurations cross-validated (DR-28, DR-29, DR-33); the eight admissible ones (DR-24)

**Expectation:** n/a (the expectation is recorded in DR-25; the outcome is in DR-25)

**Decision:** Recommend kNN (nearest cases), with k tuned inside each part. Selection confidence is Low, because the margin over the next best method is none. The test set is not used yet.

**Why not:** the table above.

**Confidence:** Low (C1 none, C2 clear, C3 adequate). Prior agreement: disagree. Grounding: none. Breadth note: six compared.

**Outcome vs expectation:** n/a

**User involvement:** informed: the recommendation and its confidence are presented for agreement before the test set is used.

**Supersedes / superseded by:** n/a

**Links:** `Code/outputs/Auto_MPG/core_recommend.json`; DR-24, DR-25, DR-28, DR-29, DR-33

### DR-36 · FINAL · step 4g (test result, once)

- **Type:** FINAL (part 2: the single test-set evaluation)
- **Step:** 4g
- **Sub-task:** the one sub-task
- **Date:** 2026-11-17
- **Question:** How does the recommended method perform on the held-back test cars, once, against the average guess?
- **Reference code:** `Code/Auto_MPG/core_final.py`, sha256:fc73659298e0739daaa7dc0eed788781b731d3d5828287985fc32b52c4546fad (interim program, approved by the user on 2026-11-17); outputs `Code/outputs/Auto_MPG/core_final.json` and `core_final_predictions.csv`. The error was recomputed from the saved predictions by a separate calculation: 1.077, which matches 1.077.

**Test result**

| Item | Value |
| --- | --- |
| Method | nearest cases, number of neighbours 3 (lowest average error across the ten training parts) |
| Test cars | 78 (held back; used once) |
| Error on the test cars (root mean squared error) | 1.077 litres per 100 km |
| Average guess on the same test cars | 3.658 litres per 100 km |
| Uncertainty | 0.336 litres per 100 km (spread of the error across the ten training parts, for 3 neighbours) |
| Margin over the average guess on the test cars | 2.581 litres per 100 km |
| Spread of that margin across the training parts | 0.561 litres per 100 km |

**Success criterion (agreed in step 2)**

| Part | Requirement | Result | Met? |
| --- | --- | --- | --- |
| 1 | error at most 1 litre per 100 km on the test cars | 1.077 | no |
| 2 | margin over the average guess at least as large as its spread across the training parts | margin 2.581 against spread 0.561 | yes |
| Overall | both parts | | **not met** |

**Rules applied**

| Rule ID | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Test set used once (`ML Guide.md` section 3) | the 78 test cars read once, in this step | [B SML pp. 74, 328] | No further use of the test cars for this sub-task |
| Recomputed test error (the check required in step 4g) | same value by two routes | [I] | Consistency check passed |

**Thresholds applied:** the success criterion's 1 litre per 100 km (agreed in step 2); the clear-margin rule of at least 1 times the spread (ours, `[I]`)

**Options considered:** n/a (the single evaluation of the recommended method)

**Expectation:** n/a

**Decision:** The success criterion is **not met** on the test cars: the first part is not met, and the second part is met.

**Why not:** n/a

**Confidence:** Low (as in DR-35). The test result does not change the level.

**Outcome vs expectation:** n/a

**User involvement:** asked; approved the final check on 2026-11-17, with the program described in plain words first.

**Supersedes / superseded by:** n/a

**Links:** `Code/outputs/Auto_MPG/core_final.json`; `Code/outputs/Auto_MPG/core_final_predictions.csv`; DR-35

## Recommendation

### Sub-task: fuel use of a new car from its design, model year and country of origin

**1. Problem.** Predict the fuel use of a new car, in litres per 100 km, computed as 235.2 divided by the recorded miles per gallon (assuming US gallons). Output: non-negative real (DR-06, DR-08). Inputs: displacement, horsepower, weight, acceleration, model year and cylinders as numbers, origin as a category, one yes-or-no column dropped per category, no transformation, car name not an input (DR-19 to DR-22). Metric: root mean squared error (DR-07); monitored alongside: mean absolute error (DR-09). Success criterion (DR-18 and the Problem Definition): error at most 1 litre per 100 km on the test cars, and a clear margin over the average guess (at least one spread). Baseline: the mean of the training outputs (SEQ-1). Achievable level: not stated. Must-haves: none (DR-11, DR-12). Extrapolation: no (DR-13). Expected shape: unknown; the user expects more fuel for heavier cars and bigger engines (DR-14).

**2. Recommendation.** Nearest cases (k-nearest neighbours), with the number of neighbours 3 (the value with the lowest average error across the ten training parts). Selection confidence: **Low** (DR-35).

**3. Test-set result.** Error 1.077 litres per 100 km on 78 test cars, against 3.658 for the average guess on the same cars; uncertainty 0.336 (spread across parts). Success criterion: **not met** (DR-36). Mean absolute error on the same cars (reported beside the main number, not deciding; `Code/outputs/Auto_MPG/core_mae.json`): 0.81 for the recommended method, 3.02 for the average guess.

**4. Why this configuration.** Constraints: the output is a positive amount, so the logistic family and the Poisson family are excluded (EXCL, DR-24); no must-have is set; the collinearity check removes no configuration (DR-24). Cross-validation evidence: the margin over the next best method (straight line with curves) is 0.013 against a spread of 0.218, which is none; the margin over the baseline is 2.635 against 0.561, which is clear (DR-29, DR-33, DR-35). Simplicity: no add-ons; the straight line also has none, so the prior score decided the tie (DR-35).

**5. Ranking table** (margins are positive when the recommended method is better; "vs baseline" is the margin over the average guess, with its spread).

| Rank | Configuration | Prior rank | Prior score | Post-prior | CV mean | Margin vs recommended (± spread) | Margin vs baseline (± spread) | Why-not code |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Nearest cases (recommended) | 3 | 0 | no | 1.315 | n/a | 2.635 ± 0.561 | recommended |
| 2 | Straight line with curves | not kept | −1 | yes | 1.328 | 0.013 ± 0.218 | 2.622 ± 0.541 | SIMP |
| 3 | Straight line | 4 | −1 | no | 1.381 | 0.066 ± 0.189 | 2.569 ± 0.585 | SIMP |
| 4 | Exponential (simple start) | 1 | +1 | no | 1.418 | 0.103 ± 0.201 | 2.532 ± 0.672 | OUTP (moderate margin; see part 7) |
| 5 | Exponential with penalty | 2 | +1 | no | 1.445 | 0.130 ± 0.203 | 2.504 ± 0.682 | OUTP (moderate margin; see part 7) |
| 6 | Decision tree | 3 | 0 | no | 1.629 | 0.314 ± 0.314 | 2.321 ± 0.553 | OUTP |
| — | Straight line with penalty; straight line with curves and penalty | not kept | −1 | — | not run | — | — | DISF |
| — | Logistic family (4); Poisson family (2) | — | — | — | — | — | — | EXCL |

**6. Prior versus evidence.** Agreement: **disagree**. The prior expected the exponential model first and the straight line after it (DR-25). The cross-validation put the nearest-cases method first and the straight line ahead of the exponential model (DR-28, DR-29). The prior's positive-output rule did not separate the families on this data. The expectation was recorded before any fitting; the disagreement is reported as found.

**7. Why not the others.** Grouped by code, in priority order: EXCL: the logistic family (four) and the Poisson family (two), as the output is a positive amount (DR-24). DISF: the two straight-line settings with the penalty, not kept after the prior ranking (DR-25). SIMP: the straight line and the straight line with curves, which could not be told apart from the recommendation (margins below half a spread). OUTP: the exponential model, the exponential model with the penalty, and the decision tree, all behind the recommendation. For the exponential models the margin is moderate (about half a spread) rather than clear; the guide's codes name no moderate case, so OUTP is the closest code and is flagged here as our reading.

**8. Confidence.** Level: **Low**. C1 (margin over the next best, the straight line with curves): none, 0.013 against a spread of 0.218. C2 (margin over the baseline): clear, 2.635 against 0.561. C3 (more training cars would still help): adequate; the error fell from 1.394 at 80 % to 1.315 at 100 %, a drop of 0.079 against half a spread of 0.152. Prior agreement: disagree. Grounding: the nearest-cases method has prior score 0 and no matrix entries behind it. Breadth: six configurations compared plus the baseline, so the breadth note does not apply.

**9. How the model predicts.** For a new car, the method finds the 3 training cars most similar to it on the scaled inputs, and reports their average fuel use. It has no formula to inspect; a person can see which cars it used. Trust limits: the error is an average over cars like those in the data; it says nothing about the worst single prediction; it holds only for cars like those in the data.

**10. Use and limits.** The model can be used to estimate typical fuel use for cars like those in the data, as an average. It was not shown to meet the 1-litre part of the criterion on the test cars. Limits from the data: units of the inputs are not verified; the origin codes are not named in the file; six cars with no horsepower value were dropped, and small-engine cars are fewer in the 392-car set than in the file; the test result rests on 78 cars, with an uncertainty of 0.336; car names are a proxy for car models, not for physical cars (DR-02, DR-22).

**11. Improvement history.** Pass 1: observation that the error on training cars is at the limit (O2) → DX-2, the limit kept by the user (DR-30, DR-31). Pass 2: observation that the model is too simple (O4) → DX-5, straight line with curves added; no gain (DR-32, DR-33). DX-5, the question on more measurements: none (DR-34). Stop: rule S3, two passes without a gain of at least half a spread (DR-34).

**12. Thresholds applied.** Clear margin: at least 1 times the spread (C2). Candidates: margin below half a spread (section 19). C1: 1 and 0.5 times the spread. C3: half the fold spread. Settings grids: as in DR-27. Learning check: error at 80 % and 100 % of the training cars. Stop rule S3: half a spread. Observation O2: the 1-litre limit. Observations O3 and O4: a ratio of 2.

**13. Trace index and provenance.** Decision Records: DR-01 to DR-04 (admissibility); DR-05 to DR-15 (formulation); DR-16 (split); DR-17 and DR-19 to DR-23 (properties and input design); DR-24 (admissible set); DR-25 to DR-27 and DR-26 (prior and protocol); DR-28, DR-29 and DR-33 (cross-validation); DR-30 to DR-32 and DR-34 (diagnosis); DR-35 and DR-36 (recommendation and test). Tags in the decision records, counted as occurrences, not rules: book advice [B SML]: 32; book fact turned into advice [B→I SML]: 6; our inference or threshold [I]: 26. The counts are occurrences in the text and are not an independent tally of rules.

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
| 46 | Step 4 started. Step 4a: the interim core (`Code/Auto_MPG/core.py`, not reviewed) gives the admissible set: eight of the fourteen configurations. The first run's MOD-2 flag on Linear + poly was a numerical artifact and was corrected before any output was used. | `Appendix.md` Decision Records, DR-24; `Code/outputs/Auto_MPG/core_admset.json` |
| 47 | Step 4b: the interim prior core (`Code/Auto_MPG/core_prior.py`, not reviewed) gives the prior ranking. Kept: baseline, Exponential, Exponential + L2, k-NN, Tree. Not kept: four Linear configurations (DISF). Recorded as DR-25 before any training. | `Appendix.md` Decision Records, DR-25; `Code/outputs/Auto_MPG/core_prior.json` |
| 48 | User approved the interim core (`core.py`, `core_prior.py`) and chose to add the straight-line model to the simple starts. Round 1: baseline, Exponential, Linear. Round 2: Exponential + L2, kNN, Tree. Recorded as DR-26. | `Appendix.md` Decision Records, DR-26 |
| 49 | Cross-validation protocol agreed at 4b: ten outer parts grouped by car name (seed 2026), five inner parts, the same outer parts for every configuration, root mean squared error, test cars locked. Recorded as DR-27. Draft Methods paragraph written in `Project Report.md`. | `Appendix.md` Decision Records, DR-27; `Project Report.md` Methods |
| 50 | Step 4c: cross-validation round 1 (baseline, Exponential, Linear), with the interim script `Code/Auto_MPG/core_cv.py`. Both simple-first configurations beat the baseline clearly. Recorded as DR-28. | `Appendix.md` Decision Records, DR-28; `Code/outputs/Auto_MPG/core_cv_round1.json` |
| 51 | Approval gap recorded. `Code/Auto_MPG/core_cv.py` was written in step 4c, after the user approved `core.py` and `core_prior.py` at 4b, and its round 1 output was recorded (DR-28) before the user saw the script. Round 1 is provisional until the user approves the script. Round 2 is held until then. | `Appendix.md` Decision Records, DR-28 |
| 52 | User approved `Code/Auto_MPG/core_cv.py` (round 1) on 2026-11-17, after its description in plain words. Round 1 results stand (DR-28). | `Appendix.md` Decision Records, DR-28 |
| 53 | Round 2 script `Code/Auto_MPG/core_cv_round2.py` written for Exponential + L2, kNN and Tree, with inner tuning. Not yet approved and not run; no round 2 output exists. Awaiting the user's approval. | `Code/Auto_MPG/core_cv_round2.py` |
| 54 | Round 2 script approved by the user on 2026-11-17 and run: Exponential + L2, kNN and Tree on the same outer parts. Recorded as DR-29. Outcome against the prior's expectation filled in DR-25 (partial). Step 4d complete. | `Appendix.md` Decision Records, DR-29 and DR-25; `Code/outputs/Auto_MPG/core_cv_round2.json` |
| 55 | Step 4e, diagnosis pass 1, on the leading method (nearest cases). The error on training cars is just above the 1-litre limit (observation O2 holds), so the action is DX-2: pause and ask the user. Recorded as DR-30. | `Appendix.md` Decision Records, DR-30 |
| 56 | User kept the 1-litre limit (answer to DX-2). The rules do not say what follows when the same observation still holds with the limit kept; the next step is put to the user. Recorded as DR-31. | `Appendix.md` Decision Records, DR-31 |
| 57 | Diagnosis pass 2: observation O4 (underfitting) holds; action DX-5 proposes Linear + poly, checked on the same ten groups. The user approved the program on 2026-11-17 after a plain-words description; it was run and the result is recorded as DR-33. | `Appendix.md` Decision Records, DR-32; `Code/Auto_MPG/core_cv_round3.py` |
| 58 | Diagnosis pass 2 result: Linear + poly, CV mean 1.328, does not beat the leader (nearest cases, 1.315). Recorded as DR-33. Next: ask the user whether more input measurements exist (remaining part of DX-5). | `Appendix.md` Decision Records, DR-33; `Code/outputs/Auto_MPG/core_cv_round3.json` |
| 59 | User: no further measurements. Stopping rule S3 applies (two passes, no gain of at least half a spread). Step 4e closed. Next: the recommendation (4f). Recorded as DR-34. | `Appendix.md` Decision Records, DR-34 |
| 60 | Step 4f started. A new program, `Code/Auto_MPG/core_recommend.py`, is written to choose the recommended method by the workflow's rule and to rate confidence (including a learning check for the recommended method). Not yet approved by the user and not run; no result from it is used. | `Code/Auto_MPG/core_recommend.py` |
| 61 | Step 4f: the approved program gives the recommendation: kNN (nearest cases), selection confidence Low (no clear margin over Linear + poly). Prior agreement: disagree. Recorded as DR-35, before the test set is used. | `Appendix.md` Decision Records, DR-35; `Code/outputs/Auto_MPG/core_recommend.json` |
| 62 | Step 4f′ (write-up before the test set): Methods paragraph for the sub-task revised to match what was done, including the straight-line model with curved terms added in the diagnosis; first Results paragraph written with the cross-validation figures and the selection confidence. No test result yet. | `Project Report.md` Methods and Results |
| 63 | Cross-validation figures drawn after the user asked for them (before the test set): Figure 4, comparison of methods (average and spread across parts); Figure 5, learning curve of the nearest-cases method. Read only from the approved result files. Added to Results. Codes removed from the report wording at the user's request; kept here. | `Code/Auto_MPG/08_fig4_cv_comparison.py`; `Code/Auto_MPG/09_fig5_learning_curve.py`; `Project Report.md` Results |
| 64 | User kept Figures 4 and 5 in the report. Plain-words rewrite of the Methods and Results paragraphs for the sub-task (codes removed from the report, kept here). Next: approval of the final check on the test cars (not yet given). | `Project Report.md` Methods and Results |
| 65 | Final check program `Code/Auto_MPG/core_final.py` written (the nearest-cases method, refitted on all training cars, checked once on the test cars, with the average guess on the same cars). Not yet approved and not run; the test cars have not been read. | `Code/Auto_MPG/core_final.py` |
| 66 | Final check run once on the 78 test cars (approved by the user): nearest cases, 3 neighbours, error 1.077; average guess 3.658; success criterion not met. Recorded as DR-36. Test cars not used again. | `Appendix.md` Decision Records, DR-36; `Code/outputs/Auto_MPG/core_final.json` |
| 67 | Step 4f′ and 4g write-up completed: Results paragraph for the test result; Methods sentence on the final fit; draft Abstract updated; Recommendation Report (13 parts) written in the Appendix. | `Project Report.md`; `Appendix.md` Recommendation |
| 68 | Step 4 closed by the user. Step 5 started: the Discussion is to be written after its paragraph structure is agreed with the user. | `Appendix.md` Analysis Log |
| 69 | Step 5: Discussion written in four themes, as agreed with the user (why this method; how it predicts; whether the success criterion was met and what the model can be used for; the limits, including the six dropped small-engine cars, unverified units, the US-gallon assumption, unnamed origin codes, cars from 1970 to 1982, and the learning curve still falling a little). Final Abstract written, with the word Draft removed. Title to be chosen by the user. | `Project Report.md` Discussion and Abstract |
| 70 | Title chosen by the user: "Predicting the fuel use of new cars from their design". Title check run against the report: the word "new" does not match the data, which are cars from model years 1970 to 1982; the Discussion says the results say nothing about newer cars. Two ways to resolve it are offered to the user (see the message to the user). | `Project Report.md` title; `Appendix.md` Analysis Log |
| 71 | Title changed at the user's choice to: "Predicting the fuel use of cars from their design" (the word "new" removed to match the 1970 to 1982 data). | `Project Report.md` title |
| 72 | Mean absolute error on the 78 test cars added to Results, from the saved predictions, after the user approved the calculation: 0.81 for the recommended method; 3.02 for the average guess. Program: `Code/Auto_MPG/core_mae.py` (approved by the user). | `Code/outputs/Auto_MPG/core_mae.json`; `Project Report.md` Results |
| 73 | At the user's request, "a new car" changed to "a car that has not yet been tested on the road" in the Abstract and the Introduction, to match the title. Other uses (Discussion, sub-headings) not yet changed. | `Project Report.md` Abstract and Introduction |

## Code Summary

- `Code/Auto_MPG/02_compare_dropped_cars.py`: descriptive comparison of the 6 cars with no horsepower value against the other 392, for step 1. Reads `Attachments/Auto MPG/auto-mpg.data` and writes nothing. Run from `Code/` with `uv run python Auto_MPG/02_compare_dropped_cars.py`. No random numbers.
- `Code/Auto_MPG/03_group_sizes.py`: counts of rows that share a car name, for the grouping decision. Reads the raw file and writes nothing. Run from `Code/` with `uv run python Auto_MPG/03_group_sizes.py`. No random numbers.
- `Code/Auto_MPG/04_split.py`: the locked train/test split, one in five cars held back, grouped by car name, seed 2026. Writes `Code/outputs/Auto_MPG/split_seed2026.csv` (one row per used car, with its set). Run from `Code/` with `uv run python Auto_MPG/04_split.py`. Seed 2026; the file is not to be read for the test rows before the final evaluation.
- `Code/Auto_MPG/05_fig1_fuel_histogram.py`: Figure 1, a histogram of fuel use for the 314 training cars. Reads the raw file and `Code/outputs/Auto_MPG/split_seed2026.csv`; writes the light and dark PNG files and the summary text. Run from `Code/` with `uv run python Auto_MPG/05_fig1_fuel_histogram.py`. No random numbers; uses the locked split (seed 2026), training cars only.
- `Code/Auto_MPG/06_fig2_fuel_vs_weight.py`: Figure 2, fuel use against weight, one dot per training car. Reads the raw file and the split file; writes the light and dark PNG files. Run from `Code/` with `uv run python Auto_MPG/06_fig2_fuel_vs_weight.py`. No random numbers; training cars only.
- `Code/Auto_MPG/07_fig3_fuel_by_origin.py`: Figure 3, fuel use by origin code, one dot per training car, with each column's median. Reads the raw file and the split file; writes the light and dark PNG files. Run from `Code/` with `uv run python Auto_MPG/07_fig3_fuel_by_origin.py`. Jitter seed 2026; training cars only.
- `Code/Auto_MPG/core.py`: interim core (not reviewed) for step 4a, the admissible set, from `ML Guide.md` sections 9 and 12. Reads `Code/Auto_MPG/props.json` and the training rows; writes `Code/outputs/Auto_MPG/core_admset.json`. Run from `Code/` with `uv run python Auto_MPG/core.py`. Code version: the SHA-256 is in DR-24. No random numbers.
- `Code/Auto_MPG/props.json`: the property values passed to the core, copied from the Decision Records with their sources.
- `Code/Auto_MPG/core_prior.py`: interim core (not reviewed) for step 4b, the prior ranking, from `ML Guide.md` sections 13 to 15. Uses the admissible set from `core.py`. Writes `Code/outputs/Auto_MPG/core_prior.json`. Run from `Code/` with `uv run python Auto_MPG/core_prior.py`. No random numbers.
- `Code/Auto_MPG/core_cv.py`: interim core (not reviewed; approved by the user on 2026-11-17) for cross-validation, round 1: baseline, Exponential and Linear, on ten outer parts grouped by car name (seed 2026). Writes `Code/outputs/Auto_MPG/core_cv_round1.json`. Run from `Code/` with `uv run python Auto_MPG/core_cv.py`. Seed 2026; training cars only.
- `Code/Auto_MPG/core_cv_round2.py`: interim core (not reviewed; approved by the user on 2026-11-17) for cross-validation, round 2: Exponential + L2, kNN and Tree, with settings tuned by five further parts inside each outer part. Run on 2026-11-17. Writes `Code/outputs/Auto_MPG/core_cv_round2.json` when run. Seed 2026; training cars only.
- `Code/Auto_MPG/core_cv_round3.py`: interim program (not reviewed; approved by the user on 2026-11-17) for diagnosis pass 2: Linear + poly, with the degree (2 or 3) chosen inside each training part, on the same ten groups. Run on 2026-11-17. Writes `Code/outputs/Auto_MPG/core_cv_round3.json`. Seed 2026; training cars only.
- `Code/Auto_MPG/core_recommend.py`: interim program (not reviewed; approved by the user on 2026-11-17) for step 4f: picks the recommended method from the approved checking results by the workflow's rule (section 19), rates confidence (section 17), and runs a learning check for the chosen method. Reads the approved result files; writes `Code/outputs/Auto_MPG/core_recommend.json` when run. Seed 2026; training cars only. Run on 2026-11-17.
- `Code/Auto_MPG/08_fig4_cv_comparison.py`: Figure 4, average error of each method across the ten parts, with its spread. Reads `Code/outputs/Auto_MPG/core_recommend.json`; writes light and dark PNG files. Run from `Code/` with `uv run python Auto_MPG/08_fig4_cv_comparison.py`. No random numbers.
- `Code/Auto_MPG/09_fig5_learning_curve.py`: Figure 5, learning curve of the nearest-cases method across the ten parts, with its spread. Reads `Code/outputs/Auto_MPG/core_recommend.json`; writes light and dark PNG files. Run from `Code/` with `uv run python Auto_MPG/09_fig5_learning_curve.py`. No random numbers.
- `Code/Auto_MPG/core_mae.py`: calculation of the mean absolute error on the 78 test cars, from the saved predictions only (approved by the user on this date). Writes `Code/outputs/Auto_MPG/core_mae.json`. Run from `Code/` with `uv run python Auto_MPG/core_mae.py`. No random numbers.
- `Code/Auto_MPG/core_final.py`: interim program (not reviewed; NOT YET APPROVED) for the final check: chooses the number of neighbours across the ten training parts, refits on all 314 training cars, checks once on the 78 test cars, with the average guess on the same cars and a second calculation from saved predictions. Writes `Code/outputs/Auto_MPG/core_final.json` and `core_final_predictions.csv` when run. Seed 2026. Not yet run.
- `Code/Auto_MPG/01_describe_data.py`: describing pass on the raw Auto MPG files for step 1. It reads `Attachments/Auto MPG/auto-mpg.data` and `auto-mpg.data-original`, prints counts, missing values, ranges and category counts, and writes nothing. Run from `Code/` with `uv run python Auto_MPG/01_describe_data.py`. It uses no random numbers, so no seed applies. It needs pandas, which is in `Code/pyproject.toml`.

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). *Machine Learning – A First Course for Engineers and Scientists*. 2nd edition, online draft version of 1 September 2026. [smlbook.org](https://smlbook.org/). Checked 2026-11-15 against the local copy in `Attachments/smlbook/`.
- Quinlan, R. (1993). Auto MPG [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5859H](https://doi.org/10.24432/C5859H). Licence CC BY 4.0 (stated on the dataset page, checked 2026-11-14). Downloaded 11 November 2026 (stated by the user).

