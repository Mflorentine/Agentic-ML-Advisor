# Davids Changes

A running summary of the changes David has made to the framework (`instructions.md`, `ML Guide.md` Part II and III, the templates and the workspace layout) with messages beginning **FRAMEWORK**, written for Florentine. Newest last. Each entry gives the date, the commit, what changed, why, and what it means in practice. The full wording is in the files themselves; the reasoning that led to each change is in the `Analysis Log` of the analysis in progress at the time (the xG analysis, `Appendix.md` at the root).

Most of these changes came out of working through a new analysis: an expected-goals (xG) model built from StatsBomb open data for four European leagues in 2015/16. They share two aims: keep the method close to the book, and make the workflow easier for a user to follow.

## Before November 2026

On 16 October 2026 David added the `Purpose` section at the top of `instructions.md` (the report should be consistent with how the book's authors would work), reduced `Project Report.md` to a template whose Methods and Results share three sub-headings, and wrote [Note for Florentine.md](Note%20for%20Florentine.md). Those changes are described in that note.

## November 2026

### 1. Admissibility checks get names (9 November, `f117f48`)

- **What changed.** ADM-1 … ADM-4 became *Admissibility 1: outcome recorded*, *Admissibility 2: prediction or understanding*, *Admissibility 3: grouped or time-ordered rows* and *Admissibility 4: new cases like these*. The Decision Record type `ADM` became `Admissibility`. Each check is put to the user by number and name, in plain words, with one sentence on why it matters for their data.
- **Why.** "ADM" meant nothing to the user, who had to ask what it was.
- **Unchanged.** The questions, answers and actions.

### 2. Book pages written as SML p. x (10 November, `879affb`)

- **What changed.** Every book page reference, in conversation and in every document, is written *SML p. 20* or *SML pp. 52–53*, including inside provenance tags (`[B SML p. 15]`). About 270 references in `ML Guide.md` were rewritten.
- **Why.** A bare "p. 5" reads like the property P5.

### 3. Properties written with their names; a user-facing list (10 November, `c100768`, `2b71d3f`, `81bc900`, `cea92c3`)

- **What changed.** P1 … P10 became *Property 1: output type*, *Property 2: data-to-parameter ratio*, and so on; checks and properties are never written as a bare number or code. A new file, [Glossary.md](Glossary.md), lists the four admissibility checks and ten properties in plain words: the question each asks, its values, who decides it and when, what it changes, and the book page. It also explains the other labels in the Decision Records (provenance tags, why-not codes, confidence factors, the core). First named `Criteria.md`, then renamed. It is the same for every analysis and maps the older labels (ADM-n, Pn) used by Heart Failure and Sepsis. Listed in the README.
- **Why.** "We should have a clean list the user can look at to see what criteria they are following."
- **Unchanged.** No rule, value or threshold. Heart Failure and Sepsis keep their old labels, because their records copy outputs of `Code/core.py`, which uses them and is never changed.

### 4. Draft Abstract from step 1; Methods drafted before cross-validation (10 November, `a6226c3`)

- **What changed.** The analysis report has an `Abstract` section. A first draft, headed *Draft*, goes in at the end of step 1 and is rewritten at the end of every step; the final version replaces it in step 5. The `Methods` paragraph for each sub-task is drafted at step 4b, once the user has agreed the method and before anything is cross-validated, and made final at 4h with `Results`. Anything not used in the end (a dropped configuration, a method set aside, a check that changed nothing) is removed from the report completely, unless the user asks for it; the record stays in the Appendix.
- **Why.** "The report should show what we are doing." Writing the method before the results fixes it in the report, as the Introduction fixes the question.

### 5. Work at the root; submit to Demonstration when finished (10 November, `aa07116`)

- **What changed.** The analysis in progress is written in two files at the top of the workspace: `Project Report.md` (the report) and `Appendix.md` (the record), copied from `Templates/Report.md` and `Templates/Appendix.md`. When the user says the analysis is finished, it is copied into `Demonstration/<Name>/` as `Report.md` and `Appendix.md`, with links adjusted, and the root files are reset. The root report uses the same structure as the Heart Failure example (Abstract, Introduction, Methods and Results by sub-task, Discussion). The previous project-level template, with the three sub-headings, moved to `Templates/Whole-Project Report.md`, used when the user asks for a report on the project as a whole. README and `ML Guide.md` §24.1 and §25.1 follow.
- **Why.** "The user should always work in the project report and Appendix in root. Once they are done we can submit to Demonstration." The user should see their work where they open the vault.
- **Note for Florentine.** The *Open items* in [Note for Florentine.md](Note%20for%20Florentine.md) about `Project Report.md` now refer to `Templates/Whole-Project Report.md`.

### 6. Methods opens with Data and evaluation, written in step 2 (10 November, `0e78355`)

- **What changed.** `Methods` opens with a sub-section *Data and evaluation*, written at the end of step 2: the data and its scope, the cleaning, the split and the held-out test set, the metric, the baseline and each sub-task's success criterion. `Results` opens with a matching sub-section, *The training data*, for the step 3 figures. The `Introduction` keeps to the question and the approach.
- **Why.** By the end of step 2 these are fixed, and the book treats the validation data, the test data and the metric as what defines the problem (SML pp. 327, 330).

### 7. Always check the book when asked about it (10 November, `7374d79`)

- **What changed.** When the user asks what the book says, or whether something is in it, the agent opens the book and checks before answering: the pages the guide cites, and a search of the four chapters. It says what the book says, with pages, and whether the guide agrees, and corrects the guide or a record if the check shows it is wrong.
- **Why.** Answers had been given from `ML Guide.md` alone. The first check corrected one tag: using log-loss as the evaluation metric rests on book facts (SML pp. 52–53, 67, 330), so it is `[B→I]`, not `[I]`.

### 8. A local copy of the book (10 November, `8061a8f`)

- **What changed.** The book (2nd edition draft of 1 September 2026, the version `ML Guide.md` is written from) is kept in `Attachments/smlbook/`, with its extracted text for searching. The folder is in `.gitignore` and never committed, because the book is for personal use only. If the copy is missing when the book is first needed, the agent suggests downloading it from smlbook.org and does so only with the user's agreement.
- **Why.** So that checking the book (change 7) is quick and always uses the right version.

### 9. Say in plain words what an action will do (10 November, `cae72bf`)

- **What changed.** Before asking to do something, or when reporting it, the agent says in ordinary words what will be done, what it uses and leaves alone, what comes out and what that changes, and why it is needed now. Script names, sub-step numbers, record types and rule IDs are given as well, never instead. `Glossary.md` gained entries for the core and for Decision Records.
- **Why.** "'Run the core' is not clear what it means."

### 10. This file (10 November, the commit that added it)

- **What changed.** Every FRAMEWORK change is summarised here as it is made, in the form above (`instructions.md`, *Changing This Contract*).
- **Why.** David will send the summary to Florentine.

### 11. No file-change boxes in answers (10 November, `bced066`)

- **What changed.** The agent no longer edits files with the tools that show a diff box in the conversation; it makes changes with scripts and says in the answer which files changed and how (`instructions.md`, *Agent Operating Rules*).
- **Why.** "Remove these file changes boxes that sometime come up in answers."
- **In practice.** The exact changes are no longer previewed in the chat; they can be read in the files or with `git diff`.

### 12. Book pages when presenting a plan (10 November, `e8a0cc8`)

- **What changed.** When the agent presents a plan, a step or a method, it gives the book pages behind each part and says which parts are ours, checking the pages in the local copy of the book first (`instructions.md`, *Say in plain words what an action will do*).
- **Why.** "When presenting something like this you should add book pages", said of the overview of step 4.

### 13. Diagnosis uses the agreed metric (10 November, `670f1f1`)

- **What changed.** In `ML Guide.md` §16, overfitting and underfitting are judged with the metric agreed in step 2 when it is an error function in its own right (log-loss in the xG analysis), instead of always with the misclassification rate. The learning-curve check (C3, §17) follows.
- **Why.** In the xG data goals are 10 % of shots, so almost every model predicts "no goal" and the misclassification rate stays near 0.10 whatever the model does: the diagnosis would be blind. The book calls the misclassification rate "problematic for imbalanced problems" (SML p. 91) and leaves the error function to the problem (SML p. 67). Raised by the agent at step 4b; David: "yes".
- **In practice.** Analyses whose metric is the misclassification rate or squared error are unchanged.

### 14. Write up the model selection before the test (10 November, `242070d`)

- **What changed.** A new sub-step, 4f′, between the recommendation and the test: `Methods` is made to match what was done, a first `Results` paragraph reports the cross-validation comparison, the recommended configuration and its selection confidence, and figures from cross-validation (such as the comparison of configurations and the learning curve) are added. Only then is the user asked about the test set. At 4h the test result is added after it; nothing written at 4f′ is reworded because of the test result, and any change is logged.
- **Why.** "Shouldn't we write up training and maybe add some figures before moving on to test?" Writing the selection down first fixes it in the report before the test result is known, following the book's order: choose on validation data, then test once (SML pp. 74, 328).

### 15. Figures in the style of the book (10 November, `6cdfa32`)

- **What changed.** A new style module, `Code/sml_style.py`, draws every figure the way the book draws its data figures: serif type, a full box with small inward ticks, no grid, a legend with a thin black frame, series told apart by line style as well as colour, and the book's own colours (sampled from rendered pages of the local copy: training error coral, held-out error lavender, classes red and blue). The light and dark variants, one colour per variable and readable type stay as workspace rules. `Code/viz_style.py` is kept for the Heart Failure analysis, whose figures are not redrawn.
- **Why.** "Could you standardise the figures format to keep in line with those in the SML book."
- **In practice.** The xG analysis's figures were redrawn in the new style.

### 16. Check the title against the content (10 November, @@HASH@@)

- **What changed.** Whenever a title is chosen or changed, the agent reads the report against it: whether each word describes what was done and found, whether the report spends its space on what the title puts first, and whether the title could lead a reader to expect a claim the report does not make. It reports where they match and where they do not, and offers both remedies, a title that fits or a change to the content that fits the title without overclaiming; the user decides (`instructions.md`, step 5).
- **Why.** "Does the content reflect the title? You should check this and consult with user on it."

