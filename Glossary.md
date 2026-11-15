# Glossary

Words and checks this workspace uses, explained in plain words. Book pages are to Lindholm et al., *Machine Learning – A First Course for Engineers and Scientists*, written SML p. x. Where a limit or rule is the workspace's own choice rather than the book's, the Book column says *Ours*. Older analyses use earlier labels: ADM-1 to ADM-4 for the admissibility checks, and P1 to P10 for the properties.

## Words you will meet

| Word | What it means | Example | Book | More detail |
| --- | --- | --- | --- | --- |
| **Success criterion** | The result a model must reach to be useful. It is agreed before any model is made, and checked once on the test data. | A school's marking tool must reach a set error before teachers rely on it. | Ours; the related idea is at SML p. 330 | `instructions.md`, step 2 |
| **Metric** | The single number that decides which model is best. It is agreed before any models are compared. | The average size of the error in predicted exam scores. | SML p. 330 | `ML Guide.md`, section 2 |
| **Baseline** | The simplest guess, which a model must beat to be worth using. | Predicting the average exam score of past students for every new student. | SML pp. 330–331 | `ML Guide.md`, section 2 |

## Admissibility checks

These are asked before any model is chosen, in steps 1 and 2.

| Check | What it means | Example | Book | More detail |
| --- | --- | --- | --- | --- |
| **Admissibility 1: outcome recorded** | Every row must have a known answer to learn from. Without one, this is not a prediction problem with this data. | Each patient in the records has a recorded diagnosis. | SML p. 15 | `ML Guide.md`, section 10 |
| **Admissibility 2: prediction or understanding** | Is the aim to predict for new cases, or to explain how things are connected? This workflow is built for prediction. | Predicting the price of a house not yet for sale, rather than explaining why extra rooms add value. | SML p. 20 | `ML Guide.md`, section 10 |
| **Admissibility 3: grouped or time-ordered rows** | Several rows may describe the same unit, or the rows may follow one another in time. The split must then keep them together or in order. | Several visits by the same patient all go on the same side of the split. | SML pp. 16, 38–39, 329 | `ML Guide.md`, section 10 |
| **Admissibility 4: new cases like these** | Will future cases look like the data we have? If not, the test data must be chosen with care. | Predicting for houses in a town the data never covered. | SML pp. 328–329 | `ML Guide.md`, section 10 |
## Properties

Facts about the problem that decide which kinds of model are suitable, and the order they are tried in.

| Property | What it means | Example | Book | More detail |
| --- | --- | --- | --- | --- |
| **Property 1: output type** | What kind of value is predicted: a number, a count, a positive amount, a yes or no, one of several classes, or ordered classes. | The number of students who drop out is a count; a house's price is a positive amount. | SML pp. 61–62 | `ML Guide.md`, section 11 |
| **Property 2: data-to-parameter ratio** | Whether there are enough rows for the number of inputs. | 20 patients with 15 measurements each is too few; 400 patients with 7 measurements is ample. | Ours | `ML Guide.md`, section 11 |
| **Property 3: number of inputs** | How many input columns the model receives, after categories are turned into separate yes-or-no columns. | A category with 10 values, such as 10 postcodes, adds up to 10 columns. | Ours | `ML Guide.md`, section 11 |
| **Property 4: categorical share** | The share of the inputs that are categories rather than numbers. | If 4 of 6 measurements are categories, such as blood group, the share is two thirds. | Ours | `ML Guide.md`, section 11 |
| **Property 5: interpretability** | Must a person be able to follow how a prediction is made, or must there be a limit on how wrong any one prediction can be? | A school that must explain why a student was flagged for extra help. | SML p. 347 | `ML Guide.md`, section 11 |
| **Property 6: probabilities** | Do you need the chance of each outcome, or a cut-off chosen to balance the two kinds of mistake? | A doctor who wants a chance of illness, not only yes or no. | SML pp. 50, 53–54, 92–93 | `ML Guide.md`, section 11 |
| **Property 7: extrapolation** | Will predictions be needed for inputs beyond the range seen in the data? | Predicting the price of a house larger than any in the data. | Ours | `ML Guide.md`, section 11 |
| **Property 8: expected shape** | Does the user, or the subject's known science, expect a particular shape of relationship? It is never worked out from the data itself. | "House prices should rise as floor area rises", if the user says so. | Ours | `ML Guide.md`, section 11 |
| **Property 9: separability** | Can the classes be told apart perfectly using the training data? | Students who pass and students who fail, if every pass has a higher mark than every fail. | SML p. 61 | `ML Guide.md`, section 11 |
| **Property 10: class imbalance** | Is one class much rarer than the others? | Two patients with the illness in a hundred. | SML p. 91 | `ML Guide.md`, section 11 |
## Other labels you will meet

| Label | What it means | Example | More detail |
| --- | --- | --- | --- |
| `[B SML p. x]`, `[B→I SML p. x]`, `[I]` | Where a rule comes from: the book's own advice; a book fact turned into advice; or the workflow's own inference or threshold. | `[B SML p. 15]` marks a rule taken straight from the book. | `ML Guide.md`, section 8 |
| `EXCL`, `USER`, `DISF`, `BASE`, `OUTP`, `SIMP` | Short reasons why a model was not recommended. `EXCL`: the problem rules it out. `USER`: it fails a requirement you set. `DISF`: it was not kept after the first ranking. `BASE`: it did not beat the baseline. `OUTP`: another model was clearly better. `SIMP`: no real difference, so the simpler one was kept. | `OUTP`: another model was clearly better. | `ML Guide.md`, section 20 |
| Task gate, `MOD-n`, `REQ-n` | Rules that decide which kinds of model are allowed at all, when a rule that keeps the model's settings from becoming extreme is compulsory, and practice that must always be followed (for example, scaling the inputs inside each fold). | A kind of model the output type rules out is never tried. | `ML Guide.md`, section 12 |
| `SEQ-n` | The order in which models are tried: the baseline first, then the simplest model, then more complex ones. | The baseline is tried before any model. | `ML Guide.md`, section 14 |
| `DX-n`, `O1`–`O6`, `S1`–`S6` | The diagnosis loop. `O1`–`O6` are what is observed after the models are compared, `DX-n` is the action that follows, and `S1`–`S6` are the rules for when to stop. | `O2`: the training error is already above what the application needs. | `ML Guide.md`, section 18 |
| `C1`–`C3` | The three factors behind how confident the choice of model is: the margin over the next-best model, the margin over the baseline, and whether more data would still help. | `C1`: a clear margin over the next-best model. | `ML Guide.md`, section 17 |
| Decision Record (DR) | One numbered entry in `Appendix.md` for each decision, with the question, the evidence, the options and what was decided. | `DR-01`, the record of whether every row has a recorded outcome. | `ML Guide.md`, section 24 |
| Core (interim core) | The program that does the calculations the workflow must do the same way every time, so the agent does not judge them. Until the advisor's own core exists, each analysis has its own, which the user approves before its results are used. | The script that ranks the candidate models before any is tested. | `instructions.md`, *Machine Learning Scope and Reasoning* |
| Flag | A method outside the book's chapters 2, 3, 4 and 13 that might help. It is named and never used, and never claimed to be better. | Noting that a neural network might help, without using one. | `ML Guide.md`, sections 20 and 23 |
