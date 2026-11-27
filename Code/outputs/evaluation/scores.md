# Scores: one-go AI reports against the workspace report

Scored on 25 November 2026 against `scoring_checklist.md`, which was written before the one-go reports were read. Scorer: the AI agent (Claude Code) that helped build the workspace; see the biases listed in the checklist. A second, blind scorer has not yet scored the reports. The Gemini report was added and scored on 27 November 2026 against the same checklist, unchanged.

What was read for each report:

- **Claude:** `Attachments/Evaluation/Claude files/Claude report.md` and the code `fuel_model.py`. The saved model `fuel_model.joblib` was not opened.
- **Copilot (excluded):** `Attachments/Evaluation/Excluded/Copilot report.docx` (one page).
- **DeepSeek (excluded):** `Attachments/Evaluation/Excluded/Deepseek report.docx`. Its section 9, *Reproducible Code (core)*, has a heading but no code in the saved file.
- **Gemini:** `Attachments/Evaluation/Gemini Report.pdf` (4 pages). No code or saved model came with it.
- **Workspace:** `Demonstration/Auto MPG/Report.md`, with its `Appendix.md` for the decision records, pages and checksum it points to.

## Summary

| # | Criterion | Workspace | Claude | Gemini |
| --- | --- | --- | --- | --- |
| 1 | Problem defined before modelling | Yes | Partly | Partly |
| 2 | Baseline | Yes | Yes | Partly |
| 3 | Test data used once | Yes | Partly | No |
| 4 | Models compared fairly, starting simple | Yes | Yes | Yes |
| 5 | Uncertainty of the result | Yes | Partly | Partly |
| 6 | Data decisions stated | Yes | Yes | Yes |
| 7 | Leakage prevented | Yes | Partly | Partly |
| 8 | Choices attributed | Yes | Partly | Partly |
| 9 | Sources given | Yes | No | No |
| 10 | Honest conclusion | Yes | Partly | Partly |
| 11 | Reproducible | Yes | Partly | No |
| | **Yes / Partly / No** | **11 / 0 / 0** | **3 / 7 / 1** | **2 / 6 / 3** |

Copilot and DeepSeek were also run, and are excluded from the comparison (27 November 2026, the user's decision). The reason is the record, not the score: the saved files may not be the complete first answers (DeepSeek's code section is empty; Copilot's file is a one-page Word summary), and the original chats could not be opened to check. Their files are kept in `Attachments/Evaluation/Excluded/`, and their scores, made before the exclusion, are kept at the end of this file.

## Evidence

### 1. Problem defined before modelling
- **Workspace, Yes.** "A prediction is judged by one error measure, the root mean squared error, which must be at most 1 litre per 100 km on held-out cars"; the rule for choosing "was fixed before any results were seen".
- **Claude, Partly.** The target and its conversion are stated. Three measures are reported (MAE, RMSE, R²) with none named as deciding, and there is no success criterion.
- **DeepSeek (excluded), Partly.** The target is defined with a reason, and the models are compared on "RMSE in L/100km". There is no success criterion.
- **Copilot (excluded), Partly.** Only the target and its conversion are stated.

### 2. Baseline
- **Workspace, Yes.** On the 78 test cars, 1.08 against "3.66 for the average guess" on the same cars.
- **Claude, Yes.** "Baseline (mean)" on the same held-out test set: MAE 3.15, RMSE 3.74.
- **DeepSeek (excluded), No.** No simple reference is reported.
- **Copilot (excluded), No.**

### 3. Test data used once
- **Workspace, Yes.** "The test set is not used until the final evaluation"; the chosen method is "evaluated once on the 78 test cars".
- **Claude, Partly.** A test set is held out and the model is chosen on cross-validation, but four models are "scored ... once on the held-out test set" and compared there ("random forest slightly ahead on the test set").
- **Claude, further evidence.** In `fuel_model.py`, the summaries and correlations reported under *What drives fuel use* are computed on all 398 cars before the split, so the test cars were looked at before the model was chosen.
- **DeepSeek (excluded), Yes.** The model is selected by 5-fold cross-validation on the training set, and the selected model is reported on the "held-out 20%".
- **Copilot (excluded), No.** It does not say on which data the performance was measured.

### 4. Models compared fairly, starting simple
- **Workspace, Yes.** The baseline and a simple starting model, then the other kept methods, on the same ten parts.
- **Claude, Yes.** "a mean-only baseline, linear regression, ridge regression, random forest and gradient boosting" with the same 5-fold cross-validation.
- **DeepSeek (excluded), Yes.** Ridge regression, random forest, gradient boosting and HistGradientBoosting on 5-fold cross-validation.
- **Copilot (excluded), No.** One model: "A Random Forest Regressor was trained".

### 5. Uncertainty of the result
- **Workspace, Yes.** "The uncertainty of the result is 0.34 litres per 100 km", on 78 test cars.
- **Claude, Partly.** The number of test cars (77) and "the test set is small, so the gap between them is within noise"; no measure of uncertainty for the test result.
- **DeepSeek (excluded), Partly.** A "95% prediction interval ... ≈ ±2.4 L/100km" is the spread of single predictions, not the uncertainty of the test error; the test size is given only as "n≈80".
- **Copilot (excluded), No.**

### 6. Data decisions stated
- **Workspace, Yes.** Six cars with no horsepower value were dropped, with what that cost: "small-engine cars are fewer in the 392 cars used than in the file". The conversion "assumes US gallons; this is an assumption", and the units "are not verified".
- **Claude, Yes.** The conversion and its US-gallon assumption, median filling "inside the modelling pipeline", and car name not used.
- **DeepSeek (excluded), Yes.** A table of each issue and its handling, for example horsepower "Imputed with median within cylinder group".
- **Copilot (excluded), Partly.** The conversion and median filling are named, with no reasons.

### 7. Leakage prevented
- **Workspace, Yes.** "Cars with the same name are kept together, so that every row with one name lies on the same side of any split", and "Any scaling of the inputs is fitted inside each training part only".
- **Claude, Partly.** The test split is grouped by car name and filling happens inside the pipeline, but the cross-validation folds in `fuel_model.py` are plain `KFold`, not grouped, and the report does not mention this.
- **DeepSeek (excluded), Partly.** "median imputation + standard scaling inside a Pipeline, fit on train only", but the split is "stratified by origin" with repeated car models "Kept", and the risk that the same car model appears in both training and test data is not discussed.
- **Copilot (excluded), No.**

### 8. Choices attributed
- **Workspace, Yes.** "At the user's request, the straight-line model was also kept"; each decision is recorded in the Appendix with who made it.
- **Claude, Partly.** The main choices are stated as the AI's own ("I chose tuned gradient boosting"); the user decided nothing, and some choices appear only in the code.
- **DeepSeek (excluded), Partly.** The choices are stated; all are the AI's own.
- **Copilot (excluded), No.**

### 9. Sources given
- **Workspace, Yes.** Lindholm et al. (2026) and the dataset (Quinlan, 1993) are cited, with book pages in the Appendix.
- **Claude, No.** No source is cited.
- **DeepSeek (excluded), No.** No source is cited.
- **Copilot (excluded), No.** No source is cited.

### 10. Honest conclusion
- **Workspace, Yes.** "The success criterion is not met", and the error "is an average over cars like those in the data. It says nothing about the worst single prediction".
- **Claude, Partly.** The limits are stated clearly (old cars, small sample, unit assumption), but there is no success criterion to judge against.
- **DeepSeek (excluded), Partly.** The limits are stated, but the result is called "accurate enough for consumer-facing estimates and fleet screening", a claim no criterion was set to test.
- **Copilot (excluded), No.** "The model achieved strong predictive performance", with no limits.

### 11. Reproducible
- **Workspace, Yes.** The seed (2026) and the download date are given; "each number reported here comes from code that can be re-run"; the checksum is in the Appendix.
- **Claude, Partly.** The code is saved with its random seeds; the data's source and version are not identified.
- **DeepSeek (excluded), No.** `random_state=42` is given, but the code section is empty in the saved file. Whether DeepSeek ran any code cannot be told from the report.
- **Copilot (excluded), No.**

## Gemini (added 27 November 2026)

1. **Problem defined, Partly.** The target and its conversion are stated with exact unit definitions. Four measures are reported (RMSE, MAE, MAPE, R²) with none named as deciding, and there is no success criterion.
2. **Baseline, Partly.** "OLS Linear Regression (Baseline)" is reported on the same test data (test RMSE 1.1815), but it is a full linear model, not a simple reference such as the average guess.
3. **Test data used once, No.** All eight models are scored on the test set, and one is recommended because of it: "Gradient Boosting Regressor (lowest holdout error, Test MAE = 0.75 L/100 km)". This contradicts its own phrase "the untouched 20% test set".
4. **Models compared fairly, Yes.** Eight models on the same 10-fold cross-validation, from ordinary linear regression upwards.
5. **Uncertainty, Partly.** The test size is given (n = 80); there is no measure of the uncertainty of the test result.
6. **Data decisions stated, Yes.** The conversion with exact constants, horsepower filled by 5 nearest neighbours "based on correlated mechanical attributes", car name excluded "to prevent overfitting on individual model trims".
7. **Leakage prevented, Partly.** "All transformations were encapsulated inside a scikit-learn Pipeline fitted strictly on training folds", but the split is "stratified by origin", not grouped by car name, and the summary statistics and correlations use all 398 cars.
8. **Choices attributed, Partly.** The choices are stated, with reasons, in the passive voice; all are the AI's own.
9. **Sources given, No.** The dataset is named (UCI Auto MPG) without a reference; no method source.
10. **Honest conclusion, Partly.** Limits are stated (1970–1982 cars, no fuel-type or transmission data), but there is no criterion, and it gives a "Deployment Recommendation: For production inference".
11. **Reproducible, No.** Tuned settings are given, but no code and no random seed.

## Recorded but not scored

| Report | Recommended model | Test error (RMSE, L/100 km) | Baseline on the same test data | Test cars |
| --- | --- | --- | --- | --- |
| Workspace | k-nearest neighbours, 3 neighbours | 1.08 | 3.66 | 78 (392 cars used) |
| Claude | gradient boosting (tuned) | 1.20 | 3.74 | 77 (398 cars) |
| Gemini | tuned extra trees, or gradient boosting (two recommended) | 1.21 (tuned extra trees); 1.07 (tuned gradient boosting; its summary gives 1.05, which its own table assigns to the default gradient boosting) | 1.18 (linear regression; no average guess) | 80 (398 cars) |
| DeepSeek (excluded) | gradient boosting | 1.24 | not reported | about 80 |
| Copilot (excluded) | random forest | 1.20 (data not stated) | not reported | not stated |

The errors are not comparable: each report used a different split, and the workspace dropped the six cars without horsepower. Gradient boosting, random forest and extra trees are ensemble methods, and Gemini's support vector regressor is a kernel method; both are from chapters of the book the workspace does not use.

## Excluded reports: scores made before the exclusion

Scored on 25 November 2026 and kept for the record. They are not part of the comparison.

| # | Criterion | DeepSeek | Copilot |
| --- | --- | --- | --- |
| 1 | Problem defined before modelling | Partly | Partly |
| 2 | Baseline | No | No |
| 3 | Test data used once | Yes | No |
| 4 | Models compared fairly, starting simple | Yes | No |
| 5 | Uncertainty of the result | Partly | No |
| 6 | Data decisions stated | Yes | Partly |
| 7 | Leakage prevented | Partly | No |
| 8 | Choices attributed | Partly | No |
| 9 | Sources given | No | No |
| 10 | Honest conclusion | Partly | No |
| 11 | Reproducible | No | No |
| | **Yes / Partly / No** | **3 / 5 / 3** | **0 / 2 / 9** |
