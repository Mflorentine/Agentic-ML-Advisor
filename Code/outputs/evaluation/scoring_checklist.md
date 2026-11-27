# Scoring checklist: one-go AI reports against the workspace report

Written on 25 November 2026, before any of the one-go reports was read. The checklist is not changed after reading them; if a criterion turns out to be unclear, the problem is noted under each score rather than the criterion being rewritten.

## What is compared

All four reports answer the same question on the same data: predict a car's fuel use in litres per 100 km from the Auto MPG data (398 cars).

| Report | Made by | Input | How |
| --- | --- | --- | --- |
| Workspace | Claude Code in the workspace, with the user, 12–17 November 2026 | `Attachments/Auto MPG/auto-mpg.data` and `.names` | Five steps, the user deciding at each step |
| Claude | claude.ai, new chat | `Attachments/Evaluation/auto-mpg.csv` | One message, first answer only |
| Copilot | Microsoft Copilot, new chat | the same CSV | One message, first answer only |
| DeepSeek | DeepSeek, new chat | the same CSV | One message, first answer only |

The message: *"I have attached a dataset about cars (auto-mpg.csv). Build a machine learning model that predicts a car's fuel use in litres per 100 km, and write a report of the analysis."*

## Scores

Each criterion is scored **Yes** (fully met, with the evidence quoted), **Partly** (some of it, or stated without evidence), or **No** (absent). A score is given only from what the report itself says; nothing is assumed from what the AI might have done.

## Criteria

| # | Criterion | Yes means | Source |
| --- | --- | --- | --- |
| 1 | Problem defined before modelling | The target, the measure of error that decides between models, and a success criterion are stated, and not chosen after seeing the results | Book: the problem is defined by the validation data, the test data and a single-number metric agreed before any model is fitted (SML pp. 327, 330) |
| 2 | Baseline | A simple reference, such as predicting the average, is evaluated on the same test data and reported beside the model | Book: a baseline the model must beat (SML pp. 330–331) |
| 3 | Test data used once | A test set is held out, the model is chosen without it (validation data or cross-validation), and the test set is used once, at the end | Book (SML pp. 72–74, 328) |
| 4 | Models compared fairly, starting simple | Several models are compared on the same validation data or folds, starting from a simple model | Book (SML pp. 331–337) |
| 5 | Uncertainty of the result | The test result comes with a measure of its uncertainty and the number of test rows | Book fact turned into our rule: a hold-out estimate varies, less the larger the hold-out set (SML pp. 71–73) |
| 6 | Data decisions stated | Each change to the data (the 6 missing horsepower values, the unit conversion, removed or transformed columns) is stated with its reason | Ours (workspace contract, step 1) |
| 7 | Leakage prevented | Steps that learn from the data (scaling, filling missing values) are fitted on the training data only; rows of the same car model are not split across training and test, or the risk is discussed | Book: preprocessing on the training data only; grouping is ours |
| 8 | Choices attributed | The report says which choices were made and by whom (the AI or the user) | Ours. This criterion favours the workspace by design: a one-go answer has no user to ask |
| 9 | Sources given | The methods are linked to a source, such as a textbook with pages | Ours |
| 10 | Honest conclusion | The report says whether the success criterion was met, and states the limits: the error is an average over cases like these data and holds only for new cases that resemble them | Book (SML pp. 68–69, 347) |
| 11 | Reproducible | Code, random seed and data version are given, so the result can be repeated | Ours (workspace contract, Analysis Standards) |

## Recorded but not scored

The recommended model, the test error in litres per 100 km and the baseline error, if reported. They are not scored, because the reports may use different test sets and are not comparable on accuracy.

## Known biases of this comparison

- The criteria come from the book and from the workspace's own rules, so they reward what the workspace was built to do.
- The scorer is the AI agent that helped build the workspace. A second scorer who does not know which report is which (for example David, given copies with the AI names removed) would make the scores more trustworthy.
- One dataset and one message. The prompt did not ask for any of these criteria; a user who knew what to ask for could get more from a one-go AI.
- The workspace report came from several days of work with the user; the one-go reports from one message.
