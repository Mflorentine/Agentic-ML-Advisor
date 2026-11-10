# Glossary

The questions and properties the advisor uses to decide what can be modelled and which models to try, in plain words. This is a reading list for the user. The rules themselves are in `ML Guide.md` (§10 for the admissibility checks, §11–§13 for the properties), and where the two differ, the guide is authoritative. Book pages are to Lindholm et al., *Machine Learning – A First Course for Engineers and Scientists*, written SML p. x. Thresholds marked *ours* are the framework's own choices, not the book's. The list is the same for every analysis: it describes the procedure, not any particular problem.

Analyses written before November 2026 use older labels: ADM-1 … ADM-4 for *Admissibility 1 … 4*, P1 … P10 for *Property 1 … 10*, and page numbers without `SML`.

## Admissibility checks

Asked before any modelling, in steps 1 and 2. Each answer is recorded as a Decision Record of type `Admissibility`.

| Check | The question | What follows from the answer | Step | Book |
| --- | --- | --- | --- | --- |
| **Admissibility 1: outcome recorded** | Is the outcome recorded for the rows the model learns from? | No → the problem is not supervised learning, and the work stops. This is the only check that can stop it. | 1 | SML p. 15 |
| **Admissibility 2: prediction or understanding** | Is the aim to predict the outcome for new cases, or to understand how the variables are connected? | Understanding → you are told that the workflow optimises prediction and does not show how variables are connected, and the work continues only if you confirm. | 2 | SML p. 20 |
| **Admissibility 3: grouped or time-ordered rows** | Do several rows belong to the same unit (for example, several measurements of one person), or are they ordered in time? | Grouped → the data is split and cross-validated by group, so a unit is never on both sides. Ordered in time → either rebuild the problem from past values, or flag time-series modelling as out of scope. | 1 | SML pp. 16, 38–39, 329 |
| **Admissibility 4: new cases like these** | Will the cases the model is used on look like this data? | No or unsure → agree with you where the validation and test data should come from before the data is split. | 1 | SML pp. 328–329 |

## Properties

Facts about the problem that decide which models are allowed and in what order they are tried. Each value is recorded in a Decision Record of type `PROP`, with where it came from: *M* (metadata or your own statement), *T* (computed from the training data).

| Property | The question | Values | Who decides, and when | What it changes |
| --- | --- | --- | --- | --- |
| **Property 1: output type** | What kind of thing is predicted? | numeric · count · non-negative real · binary · multiclass · ordinal | You, checked against the data; step 2 | Which model families are allowed at all. Binary or multiclass → logistic regression, k-NN, decision tree. Count → Poisson model, linear regression, k-NN, decision tree. |
| **Property 2: data-to-parameter ratio** | Are there enough training rows for the number of inputs? | ample · limited | Computed; step 2 | Limited (fewer than 10 rows per parameter, *ours*) → L2 regularisation favoured, polynomial terms and trees disfavoured. |
| **Property 3: number of inputs** | How many inputs are there after encoding categories? | few · many | Computed; step 2 | Many (more than 20, *ours*) → k-NN and polynomial terms disfavoured. |
| **Property 4: categorical share** | What share of the original inputs are categories rather than numbers? | low · high | Computed; step 2 | High (50 % or more, *ours*) → k-NN disfavoured. |
| **Property 5: interpretability** | Must a person be able to follow how a prediction is made, or must there be a limit on how wrong any prediction can be? | none · inspectable · worst-case bound | You; step 2 | As a must-have, removes the models that cannot meet it. As a preference, favours them in the ranking. |
| **Property 6: probabilities** | Do you need probabilities for each class, or a decision threshold tuned to the costs of each error? | yes · no | You; step 2 | As a must-have, only logistic regression remains. As a preference, logistic regression is favoured. |
| **Property 7: extrapolation** | Will the model be used on input values outside the range seen in the data? | yes · no | You; step 2 | Yes → k-NN and trees disfavoured, because they cannot predict beyond what they have seen. |
| **Property 8: expected shape** | Do you or the subject-matter literature expect a particular shape for the relationship? | linear · curved · interactions/irregular · unknown | You or the domain only, never the data; step 2 | Favours the models that can represent the expected shape. Unknown (the default) changes nothing. Your words are quoted in the record. |
| **Property 9: separability** | Can the training classes be separated perfectly? | yes · no | Computed from the training data; step 3 | Yes → logistic regression is only allowed with L2 regularisation. |
| **Property 10: class imbalance** | Is one class rare? | balanced · imbalanced | Computed from the training data; step 3 | Imbalanced (smallest class under 20 % of rows, *ours*) → changes how results are measured, not which models are tried. |

## Other labels you will meet

| Label | What it is | In the guide |
| --- | --- | --- |
| `[B SML p. x]` · `[B→I SML p. x]` · `[I]` | Where a rule comes from: the book's own advice; a book fact we have turned into advice; our own inference or threshold | §8 |
| Task gate · `MOD-n` · `REQ-n` | Which model families the output type allows; when L2 regularisation is forced; practice required whenever a model is used (for example, scaling fitted inside each fold) | §12 |
| `SEQ-n` | The order in which models are tried: the baseline and the simplest model first | §14 |
| `DX-n` · `O1`–`O6` · `S1`–`S6` | The diagnosis loop: what is observed after cross-validation, which action follows, and when to stop | §18 |
| `C1`–`C3` | The factors behind the selection confidence: margin over the runner-up, margin over the baseline, and whether more data would still help | §17 |
| `EXCL` · `USER` · `DISF` · `BASE` · `OUTP` · `SIMP` | Why a model was not recommended: excluded by the task; fails a must-have; not kept after the ranking; did not beat the baseline; clearly beaten; could not be told apart, so the simpler one was chosen | §20 |
| Flag | A method outside the book's chapters 2, 3, 4 and 13 that the evidence suggests might help. It is named, never used, and never claimed to be better | §20, §23 |
