# Florentine's Changes

Changes before 16 October are already in David's version of the workspace, so they are not listed here.

A running summary of the changes Florentine made to the framework (`instructions.md`, `ML Guide.md`, `Glossary.md`) with messages beginning **FRAMEWORK**, written for David. Newest last. Each entry gives the date, the commit, what changed, why, and what it means in practice. Where the commit message does not give a reason, the entry says "Reason to confirm with Florentine" rather than guessing.

## October 2026

### 1. Diagnosis errors on imbalanced classes (18 October, `ddda293`)

- **What changed.** In `ML Guide.md` §16 and §18, when the classes are imbalanced, the errors used to judge over- and underfitting are 1 minus the deciding metric, not the misclassification rate. The check against the required error compares with 1 minus the criterion's value.
- **Why.** "Following the book's warning" (SML p. 91), as the commit message gives it.
- **In practice.** Only classification with imbalanced classes. Regression analyses such as Auto MPG are not affected.

### 2. Stratifying the folds by a further variable (27 October, `531ec49`)

- **What changed.** `ML Guide.md` §16: when the test split is stratified by a further variable as well as the outcome (for example hospital), the outer and inner folds are stratified by the same combination. Group folds still take precedence.
- **Why.** "Prompted by Sepsis."
- **In practice.** Only analyses whose split is stratified by more than the outcome.

### 3. Test-set uncertainty as the spread across folds (27 October, `0c2aac4`, `ba78a84`)

- **What changed.** `instructions.md` step 4g and `ML Guide.md` §5.2 state the method: the uncertainty of the test result is the standard deviation of the agreed metric across the outer folds. The limit is stated: the folds and the test set differ in size, so the spread approximates the uncertainty rather than measuring it. §5.2 no longer calls this an open decision; §25.2 part 3 points to it.
- **Why.** "Prompted by the open item in Note for Florentine.md."
- **In practice.** Every analysis reports the test uncertainty this way, with the number of test rows and the limit stated.

### 4. The agent codes; the user decides through numbered options (27 October, `492bfea`)

- **What changed.** `instructions.md`: the agent writes, runs and checks all code. Decisions for the user are given as two to four numbered options with trade-offs and book pages, plus "Something else", through the question tool where available. Recommendations only where the contract allows them. One decision per question. At the end of a step the written check comes first, and no option is recommended. The problem, the experience level and any expectation about the shape stay open, in the user's words.
- **Why.** Reason to confirm with Florentine.
- **In practice.** The user is never asked to write or run code, and each decision is put as a clear choice.

### 5. Underfitting and the O2 comparison on imbalanced classes (27 October, `0d68044`)

- **What changed.** `ML Guide.md` §18: when classes are imbalanced and the errors are 1 minus the deciding metric, underfitting (O4) holds only if the ratio test holds and the training error is worse than the application needs, the same comparison as O2. O4 never drives an action ahead of O2.
- **Why.** "Prompted by Sepsis."
- **In practice.** As entry 1: only imbalanced classification.

### 6. Backward elimination and the runner-up (28 October, `e1a2ed3`)

- **What changed.** `ML Guide.md` §19 and §17 C1: configurations made by backward elimination whose input drop was not kept count in the breadth note, but cannot be the candidate, the runner-up or the recommendation. The input design is decided with the user, not treated as a configuration.
- **Why.** "Generalises interpretation z of the Mobile Price interim core."
- **In practice.** Such configurations are reported, but cannot be recommended.

### 7. Abstract, data-and-split Methods, success criterion and F-beta reference (30 October, `2ebdf24`, `34bf9d9`, `2a821ed`)

- **What changed.** Step 5 writes an Abstract after the Discussion. Methods opens with the data and the split. Results states, for each sub-task, whether the success criterion was met. Where a threshold is tuned for an F-beta measure, the F-beta of flagging every case is reported beside the model's, as a reference only (`ML Guide.md` §16). `instructions.md`, `Templates/Report.md` and `ML Guide.md` Part III (the FINAL record and the Recommendation Report) match these parts.
- **Why.** Reason to confirm with Florentine.
- **In practice.** The analysis report has these parts. In an analysis with a tuned F-beta threshold, the flag-everyone reference is shown beside the model.

## November 2026

### 8. Keep every message short (3 November, `f725bf9`)

- **What changed.** `instructions.md`: a message to the user is at most about five lines, then the decision as numbered options of one line each. Details go in `Appendix.md`.
- **Why.** Reason to confirm with Florentine.
- **In practice.** Applies to future analyses; finished analyses are not affected.

### 9. Merge of David's branch into Florentine's (10 November, `bb79a8c`)

- **What changed.** The merge joined David's branch (`david/florentine-demo`) with Florentine's. From David's branch, the merge kept: the workspace rules in `instructions.md` (the Workspace Contract table, submitting a finished analysis, the root-file rules, the plain-words rules on actions, the draft Abstract, the disclaimer, and the notes on the book and the Glossary); the write-up of the model selection before the test, step 4f′ (entry 14 of `Davids Changes.md`); `Templates/Whole-Project Report.md`; and the `Notes/` folder. From Florentine's branch, the merge kept: the rules on putting decisions to the user as numbered options, the question-tool rule, the rule to keep every message short, the rule that the agent does all the coding, the F-beta reference in `ML Guide.md` §16 and Part III, and the test uncertainty as the spread across the outer folds (entry 3). The two diagnosis rules were combined in `ML Guide.md` §16: an error function in its own right (for example log-loss) is used as it is; when the classes are imbalanced and the metric is higher-is-better and at most 1, the error is 1 minus the metric; otherwise the book's default error is used. This combines entry 1 (Florentine) with entry 13 of `Davids Changes.md` (David).
- **Why.** David asked me to merge his branch with mine, taking the best from both.
- **In practice.** The two branches' rules now sit in one version of `instructions.md` and `ML Guide.md`. The combined diagnosis rule is the one applied from this point.

### 10. The whole-project report at the root (10 November, `329e555`)

- **What changed.** The whole-project report is `Whole-Project Report.md` at the top of the workspace. `Project Report.md` is reset from the template for the next analysis, and the Demonstration row of `instructions.md` names the root file.
- **Why.** "Rename my finished whole-project report so the root Project Report.md is free for the next analysis, as instructions.md now says."
- **In practice.** The whole-project report stays at the top, outside `Demonstration/`.

### 11. Logistic regression as a generalised linear model (10 November, `8f6b1df`)

- **What changed.** `ML Guide.md`: MOD-2 (collinearity or too many parameters) now also covers unregularised logistic regression. The column "GLM" in §13 becomes "Poisson · exponential". The Student Dropout interim core (`Code/dropout/admissible.py`) changed to match. The guide's version note says records made under the earlier rule stay valid for what they record.
- **Why.** Reason to confirm with Florentine. The commit message says only "FRAMEWORK change"; the guide's version note gives the book's reading (SML p. 63).
- **In practice.** The Student Dropout analysis is finished, and its records are unchanged.

### 12. The decision threshold for F-beta (10 November, `ded1bdf`)

- **What changed.** `ML Guide.md` §16: when the selection metric is F2 or another F-beta, the threshold is tuned inside each configuration's inner cross-validation, so each configuration is compared at its own best threshold. Otherwise the threshold is tuned after model selection, as before.
- **Why.** Reason to confirm with Florentine.
- **In practice.** Only analyses with an F-beta selection metric and a tuned threshold. This change is inside a commit titled "students dropout step 4b", which also contains the Student Dropout analysis's own work; only the guide change is a framework change.

### 13. Plain words in messages (11 November, `cce610c`, `58f3c88`)

- **What changed.** `instructions.md`: a list of technical words that must be explained on the same line when used in a message (metric, model, fitted, threshold, recall, precision, cross-validation, fold, baseline, test set, configuration, prior, ranking, spread, logistic, squared terms, penalty). At most two numbers in a message. The plain-words rule applies to every message.
- **Why.** David's feedback at our meeting on 11 November: the options and messages were too technical for a beginner.
- **In practice.** Messages to the user keep to plain words, and technical terms come with an explanation.

### 14. Choices explained to the user (11 November, `2a00272`)

- **What changed.** `instructions.md`: each decision for the user opens with one plain sentence on what it is about and why it matters, with the book page cited once. Checks and properties are named by their short names. Options carry no codes or page lists.
- **Why.** David's feedback at our meeting on 11 November: the options and messages were too technical for a beginner.
- **In practice.** Each decision is put in plain words, with the reason first.

### 15. Explaining the user's own analysis (11 November, `07f2203`)

- **What changed.** `instructions.md`: when the workflow explains the user's own analysis, it says what happened in their data and why, in at most five lines. The general procedure stays in `ML Guide.md`.
- **Why.** David's feedback at our meeting on 11 November: the options and messages were too technical for a beginner.
- **In practice.** Explanations are about the user's data, not the general method.

### 16. The welcome message (12 November, `46520d0`)

- **What changed.** `instructions.md`: a greeting or an opening with no task gets a short welcome (at most about five lines) and four numbered options: start a new analysis; continue the analysis in progress, only if one is in progress; learn how the workflow works; something else. A note the user has open or linked is context, not a request.
- **Why.** Reason to confirm with Florentine.
- **In practice.** The first message from the agent follows this form.

### 17. Options with a name, meaning and reason; a plainer Glossary (15 November, `6f1ca1c`)

- **What changed.** `instructions.md`: a named method or measure in an option takes at most two short lines: its name with its short name in brackets, what it is in plain words, and why to choose it. No links to `Glossary.md` in messages or question boxes; the pointer is written in plain words. `Glossary.md` is rewritten in plain words for a beginner, with examples from everyday topics, a book page and a "More detail" pointer, and the words success criterion, metric and baseline are added.
- **Why.** David's feedback at our meeting on 11 November: the options and messages were too technical for a beginner.
- **In practice.** Options and the Glossary are easier to read for someone new to machine learning.

### 18. A typical-error entry in the Glossary (15 November, `460a6e9`)

- **What changed.** `Glossary.md`: one entry added, "Typical error": how far wrong a prediction usually is, looking at many cases. The same commit records the user's success criterion in `Appendix.md`; that is analysis content, not a framework change.
- **Why.** Reason to confirm with Florentine.
- **In practice.** The Glossary has the term; an analysis can refer to it.

### 19. Short messages, no technical words, and approval of every calculation program (17 November, `cdd7fa0`)

- **What changed.** `instructions.md`: (a) when asking the user to approve a program that does calculations, say in one or two plain sentences what it does, that the user does not need to read the code, and that it has not yet been checked by an expert; this applies to every new program after step 4b, and its results are not used before approval. (b) No working notes while work is in progress: one message when the work is done, at most five short lines. (c) No code file names, and no words such as script, core, interim, prior, family, nested, penalty or exponential, unless explained on the same line.
- **Why.** David's feedback at our meeting on 11 November: the options and messages were too technical for a beginner.
- **In practice.** The user sees one short message per piece of work, and approves each calculation program before its results are used.
