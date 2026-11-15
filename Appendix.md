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
- To be agreed: the metrics to monitor alongside, the success criterion, the baseline, the requirements, and any expectation about the shape of the relationship.

### Sub-tasks

- To be agreed in step 2.

## Analysis

*The workings, one sub-heading per sub-task, added as steps 3 and 4 proceed: exploration of the training data, cross-validation tables, learning curves, diagnostics, error analysis, checks that changed nothing, and anything computed but not reported.*

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

## Code Summary

- `Code/Auto_MPG/02_compare_dropped_cars.py`: descriptive comparison of the 6 cars with no horsepower value against the other 392, for step 1. Reads `Attachments/Auto MPG/auto-mpg.data` and writes nothing. Run from `Code/` with `uv run python Auto_MPG/02_compare_dropped_cars.py`. No random numbers.
- `Code/Auto_MPG/01_describe_data.py`: describing pass on the raw Auto MPG files for step 1. It reads `Attachments/Auto MPG/auto-mpg.data` and `auto-mpg.data-original`, prints counts, missing values, ranges and category counts, and writes nothing. Run from `Code/` with `uv run python Auto_MPG/01_describe_data.py`. It uses no random numbers, so no seed applies. It needs pandas, which is in `Code/pyproject.toml`.

## References

*Added as sources are cited. Always the last section.*
