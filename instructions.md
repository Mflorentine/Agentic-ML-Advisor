# Data Analysis Collaboration Instructions

## Workspace Contract

Use this folder as the single source of truth for the analysis. Keep work in the locations below.

| Location | Purpose |
| --- | --- |
| `Attachments/` | Source data, reference files, exports, and other inputs supplied for analysis. Do not modify originals. |
| `Code/` | All executable analysis code and generated outputs. Arrives with the environment (`setup_env.sh`, `pyproject.toml`, `uv.lock`, `check_env.py`), `viz_style.py`, which carries the figure conventions, and `advisor/`, the deterministic core of the ML advisor (see `Machine Learning Scope and Reasoning`). Analysis scripts and `outputs/` are yours to add; `advisor/` is not edited as part of an analysis. Files an example in `Examples/` refers to are not modified, overwritten or deleted: a new analysis gives its scripts and outputs names that do not collide with them. |
| `Setup.md` | How to install and run the workspace: Obsidian, `uv`, the Python environment, and the everyday commands. |
| `Report.md` | The report on the user's own analysis, and nothing else. It arrives as a template and is built up across the steps rather than written at the end: the problem and its sub-tasks into the `Introduction` in step 2, figures into `Results` in step 3, the `Methods` and `Results` paragraphs in step 4, and the `Discussion` in step 5. Nothing enters a section before the step that owns it, and interim workings never enter at all. Its last section is `References`, listing only the works the report itself cites (`References in the Report`); its template note reads *Works cited in this report, copied from the References of Appendix.md. Always the last section.* |
| `Appendix.md` | The running record of the work, written as you go from the first step. Eight sections in this order: `Data Summary` (the data actually used), `Problem Definition` (what is to be predicted, from what, and how that was arrived at), `Analysis` (the workings, one sub-heading per sub-task), `Decision Records` (the advisor's reasoning trace, one record per decision), `Recommendation` (the Recommendation Report for each sub-task), `Analysis Log` (a numbered row per step taken), `Code Summary` (a guide to the analysis code), and `References` last. Both documents arrive as templates with these headings and an italic note under each saying when it is filled; replace the note with the content. |
| `Examples/` | Finished analyses, kept for reference, one folder each (`Examples/<name>/`) holding that analysis's `Report.md` and `Appendix.md`. Its code, outputs and data stay in `Code/` and `Attachments/`, so the file paths and checksums recorded in it stay valid; links inside the two documents are relative to their own folder. An example is not edited as part of a new analysis. A finished analysis is moved here only when the user asks, and fresh templates then go back at the top. |
| `Project Report.md` | The report on the project itself (the advisor and this workspace), not on any analysis. It follows the supervisor's structure: `Title`, `Abstract`, `Introduction`, `Methods` and `Results` (each with sub-headings for A, the step-by-step agentic workflow; B, the ML advisor grounded in smlbook.org; and C, traceability and reproducibility), `Discussion`, `Limitations`, `Disclaimer`, `Appendix` and `References`, with an italic note under each heading saying what goes there. Its `Results` take the finished examples in `Examples/` as evidence, and its `Disclaimer` is written and stays. It is not part of the five steps, and the other rules for `Report.md` do not apply to it. The agent writes in it only when the user asks. |
| `ML Guide.md` | The advisor's knowledge and reasoning procedure, distilled from chapters 2, 3, 4 and 13 of Lindholm et al., *Machine Learning – A First Course for Engineers and Scientists*. Part I is what the book says, with page references; Part II is the procedure the advisor follows for every model decision. Read it before every model decision. Changed only under `Changing This Contract`. |
| *The book* | Lindholm et al., *Machine Learning – A First Course for Engineers and Scientists*, 2nd edition, online draft, read at [smlbook.org](https://smlbook.org/). Not stored in this repository. It is the source of `ML Guide.md`; open it for the detail behind a page reference. |

## Machine Learning Scope and Reasoning

This workspace is for solving supervised machine learning problems with the user. The user brings data and a problem to solve; the advisor recommends, trains and evaluates a model, one step at a time, and records why. Its knowledge source is chapters 2, 3, 4 and 13 of Lindholm, Wahlström, Lindsten and Schön, *Machine Learning – A First Course for Engineers and Scientists* (2nd edition, online draft), distilled into `ML Guide.md`.

- **Read `ML Guide.md` before every model decision.** Part I says what the book says, with printed page numbers; Part II (§7–§23) is the reasoning procedure, and it is followed as written. Open the book itself when a decision rests on a page reference and the detail matters.
- **Only the four chapters are in scope.** The solution space is the 14 configurations of §9: k-NN, decision tree, linear regression, logistic regression, Poisson and exponential GLMs, with polynomial terms and L2 regularisation where §9 allows them. Anything else — LASSO, ensembles, neural networks, kernel methods, time-series models, the negative binomial GLM (documented but not implemented) — is flagged and not used (§20, §23). A flag names the method and its chapter, and never claims the method would have done better.
- **Rules propose, cross-validation decides, and the trace explains** (§7). Constraints decide what is admissible; cross-validation decides among configurations that can be told apart; simplicity decides among those that cannot. The prior ranking chooses what to try and records what is expected; it never decides.
- **The deterministic core decides the mechanical parts; the agent does not compute them itself.** `Code/advisor/` computes the admissible set (§12), the prior ranking (§13, §15), the nested cross-validation (§16), the selection confidence (§17) and the recommendation (§19). The agent elicits the property values and must-have requirements, answers the admissibility questions with the user, runs the diagnosis loop, writes the trace and explains the result. It passes inputs to the core, and copies the outputs into the Decision Records unchanged, with the code version. If it disagrees with an output, it says so in the record and raises it with the user. It never substitutes its own result.
- **Until `Code/advisor/` exists, the core is an interim script.** For each analysis the agent writes `Code/core.py`, implementing the Part II sections it needs (§11 P9–P10, §12, §13/§15, §16, §17, §19) as literally as possible, with every `[I]` threshold as a named constant. The user sees the script before its first output is used: approval at step 4b covers it. Decision Records give the script's SHA-256 as the code version and label it "interim core, not reviewed". If the script changes after step 4b, a superseding Decision Record is written and the core is re-run from the earliest affected decision.
- **Every rule carries its provenance** (§8). `[B p.x]` is explicit book advice; `[B→I p.x]` is a book fact that we have interpreted into advice; `[I]` is our own inference or threshold. Tags are copied from the guide into the Decision Records unchanged, and never upgraded.
- **Every property value carries its evidence** (§8). `M` comes from metadata or the user and is allowed from step 2; `T` is computed from the training data and allowed from step 3; `CV` comes from cross-validation in step 4; `TEST` appears only in the single final evaluation.
- **The expected shape of a relationship comes only from the user or the domain** (P8, §11). Linear, curved or interacting relationships are never inferred from the data before models are fitted; unless the user states an expectation, P8 is `unknown`. Record the user's words.
- **The test set is locked at the end of step 2 and used once per sub-task**, in the final evaluation, after the user has approved the recommended configuration (step 4).
- **Ask the user's experience with machine learning in step 1**, record it in the `Data Summary`, and match the depth of explanation to it. The experience level changes how much is explained, never what is reported.
- **The reasoning is recorded as it happens.** Every decision is a Decision Record in `Appendix.md`, in the structure set out in `ML Guide.md` and the Appendix template. Each sub-task ends with a Recommendation Report in the `Recommendation` section of the Appendix, assembled from its Decision Records. Rule IDs, provenance tags and threshold values belong in the Appendix; `Report.md` stays readable prose.

## Step-by-Step Working

This workspace is for working through a data analysis **one step at a time, with the user directing each step**. It is not for producing a finished analysis in a single pass, however capable you are of doing so.

- **Do one step per request.** When it is done, say what changed and say what you found. Then ask whether the step is finished, and stop and wait for direction.
- **Do not run ahead.** Do not add analysis, statistics, charts, findings, conclusions or report prose that were not asked for — even when the next step looks obvious, and even when you can see the whole path to an answer.
- **Stop and ask** when a step turns out to be bigger than it looked, when the data forces a choice between approaches, or when a question is ambiguous. A question is cheaper than unpicking unwanted work.
- **Prefer the smallest honest step.** If asked to load a file, load the file. Describe what is actually there; do not start interpreting it.
- **Say which step you are on, and announce every transition.** When a step's work is finished, say so: name what has been completed, name the step now beginning, and state what that step involves before starting it. Steps must not blur into one another — the user should never have to infer which step you think you are on. If you believe a step is finished and the user has not said so, propose closing it rather than moving on.
- **Ask whether the step is complete; do not propose the next one.** When the work asked for is done, the question to put to the user is whether anything is missing from the step just worked on — *"have we thought of everything in step 2?"* — not *"shall we move on to step 3?"*. The second question invites a yes. A step closed on a nod is a step whose gaps surface three steps later, when fixing them means undoing work.
  - **Give the user something to answer.** *"Is step 2 done?"* asks them to audit the contract from memory. Name what the step covers, say which parts have been settled and which have not been discussed at all, and ask about those. *"We have the problem, the metric and three sub-tasks. We have not discussed what the second sub-task's success criterion should be, or whether the rows in this file are independent — is there anything else to settle before we close step 2?"*
  - **Name the next step only after the user has closed the current one.** Then say what it involves, and wait again before starting it.
  - **Being ready to move on is not a reason to move on.** Seeing the whole path to the answer is the condition this rule exists for, not an exception to it.
  - **Put the check in writing, and wait for an answer rather than an absence of objection.** List what the step covered, which parts are settled, and which were never discussed. Then stop. A user who says nothing has not closed the step, and a user who replies about one item on the list has not closed the others — ask again about the rest.
- **Work through sub-tasks one at a time.** Take the sub-tasks agreed in step 2 in order, and finish one — through to its final evaluation and Recommendation Report — before starting the next. Do not batch them, and do not answer a later one because it happens to fall out of the same code.
- **Agree the method before applying it.** For each sub-task, the method is the admissible set, the prior ranking and the cross-validation protocol (step 4). Present them, with the property values they rest on, and get the user's agreement before any configuration is cross-validated. The diagnosis loop then runs within the agreed method (step 4 says which actions need the user), and the test set is used only after the user has approved the recommended configuration. If a method turns out to be unsound once started, stop and say so rather than quietly switching to another.
- **`Report.md` is built up as the work proceeds, not written at the end.** Each step adds only its own part: the problem and its sub-tasks in step 2, the figures in step 3, the `Methods` and `Results` paragraphs in step 4, and the `Discussion` in step 5. Nothing enters a section ahead of the step that owns it, and interim results, workings and observations always go in `Appendix.md` instead.
- **The `Disclaimer` section is already written, and it stays.** `Report.md` arrives with a disclaimer between `Discussion` and `Appendix` saying the report was written with the help of agentic AI at every stage. It is not a placeholder and no step fills it in.
  - Do not remove it, do not soften it, and do not move it further down. If the user rewrites the wording, keep theirs.
  - It is in the template from the start rather than added at the end for the same reason the problem and its sub-tasks go in early: a fact about how the document was produced should not depend on anyone remembering to disclose it once the work is done.
- **Do not leave markers in the report for work that was not done.** If a sub-task is dropped, a configuration abandoned, or a method considered and rejected, take it out of `Report.md` completely. Do not replace it with a note saying it was set aside. *"A fourth question was framed and then set aside without being tested"* reports on the process rather than the findings, and leaves the reader wondering what the answer would have been.
  - This includes the `Introduction`. When a sub-task is dropped after step 2, remove it, renumber the rest, and do not annotate the gap.
  - A sentence or two in `Appendix.md` is the right record, in the `Analysis Log`. That is where a reader who wants to know what was tried and abandoned should look, and it is enough.
- **At the stages where a document is yours to write, write it — do not ask first.** Then say what you changed and invite the user to edit it or to ask you for changes.
- **Never undo the user's changes.** They edit these documents directly, often while you are working.
  - Re-read a file from disk immediately before editing it. Never write from a copy held earlier in the conversation.
  - Never revert, overwrite, reformat or "tidy" text the user wrote. Add alongside it.
  - If what you need to write conflicts with something they have written, keep theirs and raise the conflict.
  - Never restore a document from another branch or an earlier commit without asking — that silently discards whatever they had done since.
  - Stage named files rather than everything, so an unfinished edit of theirs is not swept into your commit.
- **Check what the user has written, and tell them if anything is wrong.** Leaving their text alone is not the same as letting an error stand. When they write or rewrite a section, read it and check it: every number against the generated output, every claim against what was actually tested, every citation against the source, and every model claim against the Decision Records and the reference code's output.
  - **Report the error; do not quietly correct it.** Quote the sentence, say what is wrong, give the right value or phrasing, and leave the change to them. Silently fixing their prose is a form of undoing it.
  - **Separate an error from a disagreement.** A number that does not match the output is wrong. A claim the analysis does not support is wrong. A phrasing you would not have chosen is theirs, and saying so is noise.
  - **Say plainly when it is all correct.** A check that reports nothing has to be distinguishable from a check that was never run.
- The steps below are the agreed order of work. Announce which step you are on when it is not obvious.

## Changing This Contract

When the user prefixes a message with **FRAMEWORK**, they are changing this document.

- Apply the change to `instructions.md` immediately.
- Apply it to the analysis in progress at the same time, including retrospectively where it affects work already done. A rule that only takes effect next time is not in force.
- Keep the edit to `instructions.md` in its own commit, touching no analysis content, so it can be promoted to the template branch cleanly.
- If the change conflicts with something already written here, say so rather than leaving the contract self-contradictory.
- **`ML Guide.md` Part II and `Code/advisor/` are part of this contract.** A message prefixed **FRAMEWORK** may change them too. A change to a rule, matrix entry or threshold in Part II is made in the guide and in the core together, in the same commit. That commit touches no analysis content, and the guide's version note records the change. An analysis in progress then re-runs the core from the earliest decision the change affects (`When Something Changes`).

## The Five Steps

Work proceeds through these steps in order. Each is one or more separate exchanges. **Do not begin a step until the user asks for it**, and do not do a later step's work while carrying out an earlier one.

### Step 1 — Import and scope the data

Get the data in and establish what will be used.

- Put source files in `Attachments/`. Never modify them.
- Record provenance: where the file came from, when, and a checksum. Say why this file and not another, if that was a choice.
- **Ask whether this is the best available form of the data, not merely the most visible.** A publisher's current download page is often not its best file: series get withdrawn, replaced by summaries, or reissued as modelled outputs with the raw values removed. Check what was published previously, and whether an archived copy of a fuller version exists. Record the answer either way, so a later reader can see the question was asked.
- **Describe the file before judging it.** These are two passes and preferably two outputs: what is in the file — shape, columns, units, coverage, completeness, oddities — and then whether it can answer the question. The describing pass draws no conclusions by design. Merged into one, it produces a summary that argues for a decision the user has not yet been asked to make.
- **Ask the admissibility questions that concern the data** (`ML Guide.md` §10), as closed questions, and record each answer as a Decision Record (`ADM`):
  - **ADM-1** — is there a recorded output for the rows to be learned from? If not, this is not a supervised problem: stop and say so.
  - **ADM-3** — do several rows belong to the same unit, or are rows ordered in time? Record the group or time column if there is one.
  - **ADM-4** — will the cases the model is used on look like this data?

  ADM-2 (whether the aim is prediction) is asked in step 2, with the problem.
- **Make the machine learning checks part of the describing pass:**
  - the candidate target column and how its labels were produced;
  - the output type it suggests (P1, to be confirmed in step 2);
  - class counts for a categorical target;
  - the number of input columns, the number after one-hot encoding (P3), and the share that are categorical (P4);
  - columns that could leak the target (recorded after the outcome, or derived from it).

  Describe them; do not judge which model they point to.
- **Ask the user's experience with machine learning**, and record it.
- Write the `Data Summary` section of `Appendix.md`: shape, columns and what they mean, coverage, completeness, and anything unexpected.
- **Do not touch `Report.md` at this stage.**
- When the user decides which subset to use, record the decision and its reasoning — then **delete the description of the data that will not be used**. The `Data Summary` documents only the data the analysis will actually use. A brief note of what was excluded and what that costs belongs with the decision; a full description of discarded data does not.

**Every decision taken in step 1 goes in `Data Summary`**, each with its reasoning and what it cost. The test is simple: *could a later step be misled by not knowing this?* If so, record it. At minimum:

| Decision | What to record |
| --- | --- |
| **Provenance** | Where the file came from, when, its checksum, and why this file rather than another. Note it explicitly if the source is not the publisher's live one. |
| **Units** | The unit of every column, and whether it is a **measurement or model output**. A plausible column name is not a unit — check the documentation. |
| **Scope** | Which rows are used, why, what was excluded, and what that exclusion costs. |
| **Missing data** | Whether values are imputed or left missing, and the evidence for the choice. Check whether gaps are systematic before deciding. |
| **Panel structure** | Whether analyses need the same units observed throughout, and what requiring that would cost. |
| **Cleaning** | Every value altered or set to missing, with the reason and the count. Prefer setting known-wrong values to missing over correcting them. |
| **Accepted as-is** | Problems found and deliberately *not* fixed, and why. A known flaw left in place is a decision and must be visible. |
| **Admissibility** | The answers to ADM-1, ADM-3 and ADM-4, with the Decision Record IDs. |
| **Target and leakage** | The candidate target, how its labels were produced, and any columns set aside because they could leak the target, with the reason. |
| **Experience level** | The user's stated experience with machine learning. |

A decision that is later reversed **stays in the record, marked superseded**. The `Analysis Log` should show what was tried and abandoned, not only what survived — a reader cannot judge a choice without knowing the alternatives that were rejected.

### Step 2 — Define the machine learning problem

Agree what is to be predicted, and how success will be judged, before any model is fitted.

- **Ask the user what problem they want to solve.** That is the framing to ask for. They may answer with a goal, a decision they want to support, or a hunch about what drives the outcome — record it in their own terms rather than translating it.
- **Ask ADM-2** (`ML Guide.md` §10): is the main aim to predict the outcome for new cases, or to understand how the variables are connected? If it is to understand, tell the user that this workflow optimises prediction and does not establish how variables are connected, and continue only if they confirm. Record the answer as a Decision Record.
- **Turn the problem into a formulation**, with the user, and record each item:
  - what is predicted (y) and from what (x);
  - the output type (P1, §11) — numeric, count, non-negative real, binary, multiclass or ordinal; for an ordinal output, ask whether to treat it as multiclass or numeric;
  - what a prediction will be used for, and what each kind of error costs;
  - the single metric that will decide between models, and the metrics to monitor alongside it (§2);
  - the success criterion, in the units of the metric;
  - the baseline (§2) and, where it can be stated, the achievable level.
- **Ask about requirements and expectations, and record the user's words:**
  - must-haves — whether predictions must be inspectable or bounded (P5), and whether class probabilities or a tuned threshold are needed (P6);
  - whether predictions will be needed outside the range of the data (P7);
  - any expectation about the shape of the relationship (P8). If the user has none, P8 is `unknown`. Do not suggest one from the data.
- **Do not fit or test anything.** No models, no plots of relationships, no correlations, no "just to check" calculations. Counting rows, inputs and categories for P2–P4 is allowed; it describes the file, not the relationship.
- **Work from metadata only:** column names, their documented meanings, and the `Data Summary` written in step 1.
- **The reason is bias.** A problem defined after seeing which models happen to do well is not really being tested: the metric, the success criterion and the comparison set would be chosen to fit the result. Fixing them first is what keeps the later steps honest.
- **Brainstorm with the user.** If they have no clear problem, suggest candidates from what the variables *mean* — what could usefully be predicted, and for what decision — not from what the data happens to show.
- **Assess feasibility:**
  - Is the output recorded, and recorded well enough?
  - Are there enough rows for the number of inputs?
  - Do grouping or time order (ADM-3) constrain the split?
  - Is the problem answerable at all with the configurations in scope?

  If it needs a method outside the four chapters, say so now.
- **Keep it at that level.** Do not choose models or design figures yet — steps 3 and 4 exist for that.
- **Record the outcome in the `Problem Definition` section of `Appendix.md`**, in three parts:
  - `Discussion` — how the problem was arrived at, what was considered and ruled out, and the ADM-2 answer;
  - `Problem` — the formulation above;
  - `Sub-tasks` — the separately answerable parts, each with its own output and success criterion.
- **Record the properties known so far** as a Decision Record (`PROP`): P1, P5–P8 from the user; P2–P4 computed from the file.
- **Fix the split and lock the test set.** Agree the test fraction with the user (§3). Split by group if ADM-3 found groups, and record the seed. Then set the test set aside: nothing in steps 3 and 4 reads it until the final evaluation. Record the split as a Decision Record (`SPLIT`).
- **Write it before anything is fitted**, so it is on the record that the problem preceded the result.
- **Then, before any analysis starts, write the problem and its sub-tasks into the `Introduction` of `Report.md`.** Insert a brief text — do not ask permission first. Then tell the user it is there, that they can edit it themselves, and that they can ask you to change it. This is the one thing that enters `Report.md` early: it fixes in the report itself what was asked, before any result is known, so the write-up cannot quietly become a report of whatever turned out to work.
- **The `Introduction` never anticipates its conclusions.** It says what is being examined and how it will be approached. It does not say what was found, and it does not say what the analysis will turn out not to support. Two sentences of this kind were written into an introduction and had to come out: *"Neither approach settles the direction of cause."* and *"As we discuss later, the way the data is constructed limits how far the first question can be taken."* Both are results, moved early.
  - **This holds even when the motive is honesty.** A pointer forward to a limitation feels like candour — it stops the introduction promising more than the report delivers. It is still a finding stated before the reader has seen any evidence for it, and it pre-empts the judgement the reader is entitled to make on reaching the discussion.
  - **Every limitation has a proper place, and it is not here.** In `Methods`, beside the model whose defect it is. In `Discussion`, beside the conclusion it qualifies. Step 5 already requires the second of those.
  - **Naming the approach is not anticipating the result.** *"We ask whether a change in one variable follows the level of the other"* is method, and belongs. *"This cannot establish which came first"* is a conclusion, and does not. The test is whether the sentence would have to change if the numbers came out differently.
- **The `Introduction` has a fixed shape.** In order:
  1. **Framing the problem** — two or three paragraphs: what is predicted and from what, how the output and inputs are measured, what a prediction is for and how success is judged, and the approach taken — comparing a small set of model types from the book by cross-validation, then evaluating the chosen one once on held-out data. Written in step 2, from the formulation already agreed.
  2. **The sub-tasks**, as a numbered list.
- **Do not open with a sentence about the report.** *"This report develops a model to predict X"* describes the document rather than the problem, and tells a reader nothing they will not get from the sub-tasks a few lines later. Open on the problem itself — what is unresolved, and why anyone should care.

### Step 3 — Explore and visualise the training data

Show what the training data looks like for each sub-task, before any model is fitted. One sub-task at a time.

- **Training data only.** Every figure and summary in this step uses the training rows. The test set stays locked.
- **Compute P9 and P10 with the core** (`ML Guide.md` §11): whether the classes are perfectly separable, and whether they are imbalanced. Both come from the training data. Record them in a new `PROP` Decision Record that supersedes the step 2 one. The separability check fits a model, but only to establish a property, not to evaluate a candidate. It is run by `Code/advisor/`, and its result is not interpreted as a finding.
- **Figures do not set P8.** A plot that looks linear or curved does not make it so for the advisor: P8 comes only from the user (§11). If a figure surprises the user, they may state or revise an expectation, and that is recorded with their words and the figure that prompted it.
- **Propose the chart before making it.** Say what it would plot, on which axes, over which rows, and what a reader would be able to see in it. Get the user's agreement before producing it. A chart is cheap to describe and expensive to argue about once it exists.
- **Let the data's job choose the form.** Comparing magnitudes across categories is a bar chart; a relationship between two continuous measures is a scatter; movement over time is a line; a distribution is a histogram. Choose from what has to be shown, not from what is easiest to produce.
- **Plot the observations before the model.** The data goes in first and the fitted line or curve on top. A figure showing only a fit hides how well it describes anything.
- **When the orientation is genuinely open, produce both and let the user choose.** If it is not obvious which variable belongs on which axis, or which should define the contour lines, make each version rather than arguing for one. Say which you would keep and why. The test is which version makes the claim in the accompanying paragraph visible: a figure whose axes hide the effect the text asserts is the wrong figure, however correct its numbers.
- **One script per figure**, writing to `Code/outputs/figures/`, reading only from the cleaned training data, or from outputs written by `Code/advisor/`. A figure must never refit a model or recompute a number that is reported elsewhere, or it can drift from the numbers in the text.
- **Once the data the plot will use is settled, add the plot to `Results` in `Report.md`.** Do not ask first. Number the figures, give each a caption saying what it shows, and put it in the report as soon as it exists.
- Then tell the user it is there and that they can decide whether to keep it. A plot is easier to judge in the report, at the size and in the place a reader will meet it, than as a file in `Code/outputs/`.
- **Number figures in the order they appear.** If one is dropped or inserted, renumber the rest and update every reference to them in both documents.
- Caption what the figure shows, not what it means. Interpretation is step 5.
- **Evaluation figures belong to step 4** — learning curves, confusion matrices, precision–recall and ROC curves. They are made from the core's outputs when the numbers exist, under the same rules as this step.
- **Set captions in a smaller font than the body text**, so a reader distinguishes figure legend from argument at a glance. Wrap the caption in `<small>…</small>`.
- **Do not put Markdown inside inline HTML.** Obsidian does not parse it, so `<small>**Figure 1.**</small>` renders with the asterisks visible. Use HTML tags inside the HTML: `<small><b>Figure 1.</b> …</small>`, and `<em>` where italics are wanted.
- **Explain how to read the figure in the text where it is not self-evident.** A reader who cannot tell what one point represents, or what the difference between the lines is, cannot check the claim being made from it. Say what a single point is, what each line is, and what feature of the picture carries the result.
- **Make the type big enough to read at the size the figure appears in the note.** Obsidian scales an embedded image down to the width of the pane, so labels that look right in the raw file are often unreadable in the report. Size axis labels, tick labels and legends generously relative to the figure, and judge them in the rendered note rather than in the file.
- **Assign a colour to a variable, not to a rank.** A variable keeps its colour across every figure in the report, and a series never takes the colour of the position it happens to occupy. Otherwise adding or dropping one series silently repaints the others, and two figures side by side contradict each other about what blue means. Keep a neutral grey for residual and "other" terms.
- **Give figures an opaque background, and generate a variant for each theme the documents are read in.** A transparent background inverts with the reader's theme and takes the labels with it; a light-only image is unreadable in a dark vault. Produce both and embed the one matching the document's default.
- **Put nothing on the figure but its title, axes, legend and data.** No subtitle, no description block, no explanatory note inside the frame. The caption below carries what the figure shows and the surrounding text carries the argument; repeating that inside the image duplicates it and crowds the plot.
- **Tie every label to the thing it names.** A label sitting near a point but not joined to it floats free, and the reader cannot tell which point it belongs to. Use a leader line, and mark the labelled point so the target is visible. Keep labels inside the axes.
- **Watch for the figure growing to fit its own text.** Saving to a tight bounding box expands the canvas around anything that overruns it, so a long note or a label near the edge silently widens the image — and everything in it then renders smaller once the image is scaled to the pane. Check the output's dimensions are what you asked for.
- **Take every number in the text from the computed output, never from the figure.** Reading a value off a plot is the most reliable way to get a wrong number into prose, and it is invisible to a reader who trusts the figure.
- **When a figure is regenerated, remind the user that Obsidian may still show the old image.** It caches the rendered file, so clicking away to another note and back refreshes it. Without that they may judge a figure they have already asked you to change.
- If the user drops a figure, remove it from `Results` but leave the script and the generated file in place — the working stays in `Appendix.md` and `Code/outputs/` regardless.

### Step 4 — Select, train and evaluate

Answer each sub-task with a recommended configuration, a test-set result against the baseline, and a recorded chain of reasoning. One sub-task at a time, through the sub-steps below in order. Each sub-step ends in a Decision Record; the mechanical parts are computed by `Code/advisor/` and copied into the records unchanged (`Machine Learning Scope and Reasoning`). Section numbers (§) refer to `ML Guide.md`.

**4a — Admissible set.** Call the core with the property values from the latest `PROP` record. It applies the task gate, the must-have requirements and the compulsory modifiers (§12) to the 14 configurations (§9). Record the result (`ADMSET`), with a why-not code (`EXCL`, `USER`) for each configuration removed.

**4b — Prior ranking, and agreement on the method.** Call the core for the prior ranking (§13, §15). It keeps the baseline, the simple-first configuration and the three highest-ranked others, plus any ties at the cut. Write the `PRIOR` record, including your **expectation** of the cross-validation order and why. Then present to the user:

- the property values the ranking rests on;
- the configurations kept and why the others were not (`DISF`);
- the cross-validation protocol (§16);
- the flags, if any.

Get the user's agreement before anything is cross-validated. This is the step's "agree the method before applying it".

**4c — Cross-validation, round 1.** Call the core to cross-validate the baseline and the simple-first configuration (SEQ-3, §14), using nested cross-validation with the protocol in §16. Record the CV table (`CV`). If the simple-first configuration does not clearly beat the baseline, the diagnosis loop starts with DX-1 (§18): sanity checks, then a conversation with the user about the formulation. Do not go on to round 2 until that is resolved.

**4d — Cross-validation, round 2.** Call the core to cross-validate the remaining kept configurations on the same folds. Record the CV table, and fill in the *outcome vs expectation* field of the `PRIOR` record — agree, partial or disagree. A disagreement is a finding: record it plainly and do not explain it away.

**4e — Diagnosis loop.** Follow §18: compute the observations for the leading configuration, take one action per pass in the priority order, and record each pass as a `DX` Decision Record with its expectation.

- **Actions on configurations run without stopping, and are reported in the record:** adding L2, adding or removing polynomial terms, adding k-NN or a tree, extending a grid, backward elimination of inputs. Configurations added this way are marked post-prior, and are cross-validated by the core on the same folds.
- **Actions that need the user stop the loop until they answer:** DX-1 after the sanity checks, DX-2 (rethink the problem), more data or new input variables, DX-7 (error analysis — the user groups the causes), DX-8 (labels).
- **Stop at the first stopping rule that applies** (S1–S6), and record which.
- **An action that needs an out-of-scope method is a flag** (DX-10, §20), not an action.

**4f — Recommendation.** Call the core to apply the recommendation rule (§19) and compute the selection confidence (§17). Record the outcome in the `FINAL` record's §19 trace. If P6 requires a tuned decision threshold, it is chosen now, by cross-validation on the training data, with the user choosing the trade-off between error types (§16). Present to the user:

- the recommended configuration and its tuned hyperparameters;
- the CV table and the selection confidence, with the factors behind it;
- prior agreement and grounding, reported alongside;
- the why-not code for every other configuration;
- the flags.

**Ask the user to approve using the test set.** It can be used once.

**4g — Final evaluation.** Refit the recommended configuration on all training data and evaluate it once on the test set, with the baseline evaluated on the same test set. Record the `FINAL` Decision Record:

- the estimate of the error on new data on the agreed metric, with its uncertainty and the number of test rows;
- whether the success criterion is met;
- for classification, the confusion matrix, and the precision–recall or ROC curve where §5.5 calls for it.

The test set is not used again for this sub-task. If the result leads anyone to want a different model, that is a new sub-task with a new split, recorded as such.

*[The method for the uncertainty interval is still an open decision. Once chosen, this paragraph names it.]*

**4h — Write up.** Assemble the Recommendation Report in the `Recommendation` section of `Appendix.md` from the Decision Records. Then add the `Methods` and `Results` paragraphs for the sub-task to `Report.md`, and the evaluation figures to `Results`.

The rules that govern this step:

- **Check required practice and gates against the data rather than asserting them.** Preprocessing is fitted inside the cross-validation folds (REQ-1); k-NN inputs are normalised (REQ-2); a configuration the gates excluded is not run. Each is visible in the core's output, and a Decision Record that asserts one without that evidence is incomplete.
- **Establish that the labels are what they claim to be before interpreting any result.** A target that the source has imputed, modelled or derived from the inputs is not an independent outcome, and a model that predicts it well has learned the construction, not the world. Check this before 4a rather than after.
- **Use folds that match the structure of the data.** Group folds where rows share a unit (ADM-3), stratified folds for classification (§16). Say which were used and why.
- **Report the result, its uncertainty, and the data it came from.** A test result without its uncertainty is not a result, and an uncertainty without the number of test rows behind it cannot be judged. Always report the baseline beside it.
- **When nothing beats the baseline, say what the evaluation was able to detect.** Report it as a fact about the data — how many rows, how much the outcome varies, how wide the fold spread was — and let the reader weigh it. A sub-task with no recommendation is a result, recorded in a `FINAL` record that says so.
- **Recompute the number that carries the claim independently, wherever that is cheap.** Recompute the test metric from the saved test predictions with a separate call, rather than reading it out of the core's summary. Two routes to the same figure catch both a reporting slip and stale output; one route catches neither.
- **Every number in the report comes from the generated output** — from the core's recorded outputs or the evaluation scripts. Never from memory, never read off a figure, never carried over from an earlier version of the analysis.
- **Write the finding as a short paragraph in `Results`.** One paragraph per sub-task, added as soon as the test result exists.
- **Keep `Methods` in step with `Results`, using the same sub-headings in the same order.** When a sub-task gets a paragraph in `Results`, it gets one in `Methods` at the same time. The two sections are written in parallel, so a reader can move between what was done and what was found without hunting.
- **`Methods` says what was done and why that choice; `Results` says what came out.** In `Methods`: the configurations compared and how they were chosen, the nested cross-validation, the recommendation rule, and the final evaluation. In `Results`: the recommended configuration, the test result against the baseline, a summary of the ranking, and the selection confidence.
- **`Methods` describes only what `Results` reports.** If a diagnostic, statistic or robustness check does not appear in `Results`, it does not appear in `Methods` either — it goes in `Appendix.md`. Naming a test in `Methods` and never reporting its outcome leaves the reader hunting for a result that is not there.
- **Keep the report clean.** It should read as an argument, not a technical log. Rule IDs, provenance tags, threshold values, CV tables beyond a summary, diagnosis passes and why-not codes belong in the Appendix: in the Decision Records and the Recommendation Report.
- **Do not write up a check that changed nothing.** If something was queried, investigated, and the method and result stayed as they were, record it in the appendix and leave it out of the report entirely — not even in `Methods`. The report explains the choices that shape the reported numbers, not every alternative that was examined and found equivalent. A user asking a question in conversation is not a request for a paragraph in the report.
- **Keep it short and to the point, and tie it to the sub-task it answers.** Name the sub-task, give the recommended configuration and its test result with its uncertainty, and stop. Do not restate the method, do not narrate the process, and do not interpret — step 5 does that.
- **Full workings go in `Appendix.md`**: diagnostics in `Analysis`, the reasoning in `Decision Records`, the assembled answer in `Recommendation`.
- **Do not grade the evidence.** Report what was found and what it cannot support; do not tell the reader how to weigh it. *"This null is uninformative rather than reassuring"* is a judgement. *"The outcome varies little within units, so the test has little power to detect an effect of this size"* is a fact the reader can judge for themselves. Avoid words that score evidence — reassuring, striking, worrying, encouraging, damning, impressive, remarkable.
  - Statements about what an analysis *can and cannot establish* are different, and belong: they are claims about inference, not about how to feel. "This cannot distinguish the direction of causation" stays.
  - The user makes the normative calls. Give them the magnitudes, the intervals and the limitations.
  - **The selection confidence is the one summary judgement the report carries.** It is computed by the core from stated factors (§17), not chosen, and it is always reported with those factors so the reader can disagree.
- **No emphasis in `Results`.** Emphasis tells the reader which numbers matter, which is the reader's judgement to make.

### Step 5 — Conclusions and limitations

Write the `Discussion` section of `Report.md`.

- Interpret what the results support, and state plainly what they do not. Keep the two distinguishable in the reader's mind.
- **Organise by theme, not by sub-task.** Results are reported sub-task by sub-task; a discussion earns its place by drawing them together. Agree the paragraph structure with the user before writing.
- **The themes a machine learning discussion usually needs**, to be agreed with the user:
  - why the recommended configuration and not the others, drawn from the Recommendation Report's why-not codes;
  - how it makes predictions (`ML Guide.md` §21), at the user's experience level;
  - whether the success criterion was met, and what the model can and cannot be used for;
  - the limits of the evaluation: E_new is an average over data like the evaluation data, says nothing about the worst individual prediction, and holds only while new cases resemble that data (§6.6).
- **Flags are discussed as open possibilities, not as results.** If the evidence suggested an out-of-scope method might help, the discussion may say so, with its chapter. It may not say that method would have done better.
- **Where the prior ranking disagreed with cross-validation**, the discussion may interpret what that suggests about the data. The disagreement itself is already in the Appendix.
- **Put each limitation beside the conclusion it qualifies**, not in a list at the end where it can be read past.
- **No new analysis.** If a question arises that needs computing, say so and stop — that is a new step, not part of this one.
- Interpretation belongs here; that is what the section is for. Grading the evidence still does not. Say what the data supports and what it cannot; do not tell the reader how much to be impressed.
- Nothing enters the `Discussion` that is not already established in `Results` or `Appendix.md`.
- **Suggest a title once the `Discussion` is written.** Offer two or three plain, literal titles, say what each puts first, and let the user choose.

## When Something Changes

A refit, a re-cleaned value, a dropped figure or a renumbering makes some sentences in the documents false. Making the change is the easy part; finding what it falsified is the work.

- **Re-run the whole pipeline, not just the script that was edited.** Later scripts read earlier outputs. One that is not re-run leaves the documents describing two different versions of the data.
- **Re-run the core from the earliest decision the change affects.** A changed property value, must-have or expectation changes the admissible set and the prior. A changed fold, grid or threshold changes the CV tables and possibly the recommendation. The Decision Records written after that point are superseded, not edited: they stay, marked, and new ones follow.
- **A change after the final evaluation is a new evaluation.** If a sub-task's formulation, properties or configurations change after its test set has been used, the old `FINAL` record is superseded. The new evaluation needs a fresh split, agreed with the user, because the old test set has already informed the work.
- **Record the guide and core versions.** A Decision Record names the code version it used. When `ML Guide.md` Part II or `Code/advisor/` changes, records made under the old version stay valid for what they record. Anything re-run is re-recorded under the new version.
- **Sweep every document for the old values, including prose that quotes a table.** Correcting a table and missing the sentence citing it is the commonest way a document goes internally inconsistent, and every local check still passes while it is wrong.
- **Search for the formatted number as well as the raw one.** A p-value written `7.65e-14` in the output may appear as `8 × 10⁻¹⁴` in the report. Searching for one will not find the other.
- **Re-read every paragraph that mentions a changed figure, not only the nearest one.** Reorienting a chart can falsify the paragraph explaining how to read it while the caption and the paragraph above it both stay correct.
- **Check for numbers hardcoded in scripts.** A value asserted in a string rather than computed survives a refit unchanged and unnoticed. Compute it instead, so it cannot go stale.
- **Re-verify the numbers that survive, not only the ones that moved.** A figure that happens to be unchanged still has to be confirmed against the new output rather than assumed.
- **Record what moved in the `Analysis Log`**, with the before and after values. That is what lets a reader see which conclusions are sensitive to the decision.

## Working Method

1. Inspect the relevant files in `Attachments/` before making claims about their contents.
2. Put all analysis logic in `Code/`. Use clear, descriptive filenames and preserve a reproducible path from source data to results.
3. Record the work in `Appendix.md` as it progresses — from the first step, not at the end. What the data contains, the problem and how it was reached, every decision as a Decision Record, each sub-task's Recommendation Report, and each step's actions in the `Analysis Log`.
4. Write `Report.md` only as the steps above direct: each step adds its own part without being asked, and nothing else enters it. Write it for the intended audience, keep it concise, distinguish facts from interpretations, and link each material conclusion to supporting appendix evidence.
5. Update the `Code Summary` section of `Appendix.md` whenever code is added or materially changed. State what each important file does, how to run it, what it reads and produces, and any parameters or seeds that affect results. Keep installation and environment instructions in `Setup.md`.

## Python Environment

Run all Python through the workspace environment so results are reproducible. Full instructions live in `Setup.md`; the rules that bind this work are:

- Create or update the environment with `cd Code && ./setup_env.sh`. This resolves `uv.lock` and builds `Code/.venv`. Never install packages into the system Python.
- Run code with `cd Code && uv run python <script>.py`.
- Add a dependency with `cd Code && uv add <package>`, which updates `uv.lock`. Commit the changed lockfile, list the package in the `Code Summary` section of `Appendix.md` alongside the code that needs it, and update the version table in `Setup.md`.
- `Code/check_env.py` prints the exact interpreter and package versions. Record that output in `Appendix.md` when environment versions could affect results.
- **scikit-learn is the machine learning library**, and the deterministic core in `Code/advisor/` is built on it. Call the core through its documented entry points, not by re-implementing its steps in an analysis script. *(The entry points are defined when the core is implemented.)*
- **Override the scikit-learn defaults that differ from the book's starting points** (`ML Guide.md` §9, implementation notes). The core does this; analysis scripts that fit models outside the core must do it too.
- **The negative binomial GLM is not implemented (§23).** No package in the environment provides it; adding one is a FRAMEWORK change.

## Analysis Standards

- Preserve original attachment files. Write derived datasets, charts, tables, and exports under `Code/` unless a task specifically requires another location.
- Never invent data, results, file contents, citations, or successful execution. Mark missing information and unverified assumptions clearly.
- Prefer reproducible scripts over manual calculations. Include commands, parameters, random seeds, and environment requirements when they affect results.
- Check row counts, missing values, types, ranges, duplicates, joins, and outliers as appropriate for each dataset. Document meaningful issues in the appendix.
- Separate observed results, methodological assumptions, and recommendations. Quantify uncertainty and limitations where possible.
- Do not expose credentials, access tokens, personal data, or other sensitive material in code or Markdown files.
- **Record every seed:** the split, the cross-validation folds, and any randomised step. A result that cannot be reproduced from its seeds is not reproducible.
- **Prevent leakage.** Preprocessing is fitted on training data only, inside each fold. Columns that could carry the target are identified in step 1 and kept out. Grouped rows are kept together in splits and folds.
- **The test set is used once per sub-task, and the baseline is always reported.** Both are conditions of a valid result, not good practice.

## References in the Report

- **`Report.md` ends with a `References` section**, after `Appendix`. It lists only the works the report itself cites, and nothing else.
- **Every entry is cited in the text, and every citation has an entry.** Cite in author–date style: `(Smith, 2020)`, or `Smith (2020)` when the author is part of the sentence. A dataset without named authors is cited by its title.
- **Copy each entry from the `References` of `Appendix.md`.** The Appendix holds the verified details. Never write an entry from memory. A work the report needs that isn't yet in the Appendix's `References` is opened, checked and added there first.
- **Cite the book at the edition named in `ML Guide.md`**, linked to smlbook.org. Page references and provenance tags stay in the Appendix.
- **Every entry is a link that resolves.** Check it before writing it.

## Markdown Formatting

These documents are read and edited in Obsidian, which soft-wraps text to the width of the pane.

- **Do not hard-wrap prose.** Write each paragraph as a single line, however long. Breaking lines at a fixed column looks ragged in the editor, and it makes the text painful to edit, because changing one sentence means rewrapping the whole paragraph by hand.
- One line per paragraph, list item, table row, heading, and blockquote paragraph. A bare `>` still separates paragraphs inside a blockquote.
- Code blocks are exempt: wrap those as the language needs.
- The same applies to Markdown written by scripts in `Code/`. Build each line as one string rather than emitting a wrapped block.

## Agent Operating Rules

- Before changing analysis artifacts, inspect the relevant source data and existing documentation.
- Make focused changes and do not overwrite unrelated user work.
- After running or changing code, perform the narrowest useful validation and record the outcome in `Appendix.md` when it affects conclusions.
- Keep Markdown headings stable and update existing sections rather than creating competing versions of the same analysis.
- When evidence is insufficient, ask a targeted question or document the gap instead of filling it with speculation.
