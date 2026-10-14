# Agentic ML Advisor: step-by-step guidance through the ML workflow

A folder for working through a machine learning problem with an agent, one step at a time, and coming out with a recommended model and a report you can defend.

It is an Obsidian vault with [Claudian](https://github.com/YishenTu/claudian) installed, so the conversation happens beside the documents it is writing. The agent's working contract is [instructions.md](instructions.md), which it reads automatically. The agent's knowledge of machine learning comes from chapters 2, 3, 4 and 13 of Lindholm et al., [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), distilled into [ML Guide.md](ML%20Guide.md) with page references.

## What makes this different from just asking

Ask an agent to solve a prediction problem and it will hand you a finished model in one pass: a model picked, trained, charts drawn, conclusions written. It will look right. You will have no idea which choices were made on your behalf.

This folder is built to stop that. The agent does one step per request and then stops. It does not add analysis, findings or prose you did not ask for. It agrees the method with you before applying it, works through one sub-task at a time, and asks before it touches the held-out test data, which it uses once. The parts that require judgement stay with you, which is the whole point.

Every model choice is recorded as it is made. Each decision gets a Decision Record that names the evidence and the rule it rests on, with the book page — or says plainly that the rule is our own inference. The mechanical parts — which models are admissible, how they rank, how confident the choice is, which one is recommended — are computed by code, not argued by the agent.

## Getting started

1. Install the environment — [Setup.md](Setup.md) covers Obsidian, `uv` and Python.
2. Put your data in `Attachments/`.
3. Open a Claudian conversation and ask for step 1: import and describe the data.
4. Work through the five steps, one request at a time.

## Example analysis

[Report.md](Report.md) and [Appendix.md](Appendix.md) hold a completed example: predicting death during follow-up from the Heart Failure Clinical Records data (sub-task 1), worked through steps 1–5 in this folder. The report is the argument; the appendix is the full record behind it, including every decision record.

## Progress

| Part of the brief | Status |
| --- | --- |
| Agentic system that guides users through ML problem-solving | Done: the five-step workflow in [instructions.md](instructions.md). |
| Uses smlbook.org chapters 2, 4 and 13 (plus chapter 3, agreed with my supervisor) | Done: [ML Guide.md](ML%20Guide.md), with page references. |
| Helps users choose ML techniques | Done for classification, using an interim core (`Code/core.py`); the reusable `Code/advisor/` is next. |
| Step-by-step guidance from formulation to evaluation | Demonstrated end to end on the heart failure data ([Report.md](Report.md), [Appendix.md](Appendix.md)). |
| Available online through GitHub | Done. |

### Next steps

- Build `Code/advisor/`.
- Demonstrate on more datasets: a regression and a multiclass example.
- Write the project report.

## The five steps

| Step | What happens | What it fills in |
| --- | --- | --- |
| 1 | Import and scope the data | `Data Summary` in the appendix |
| 2 | Define the machine learning problem | `Problem Definition` in the appendix; the problem and sub-tasks go into the report |
| 3 | Explore and visualise the training data | Figures into the report's `Results` |
| 4 | Select, train and evaluate | `Decision Records` and `Recommendation` in the appendix; `Methods` and `Results` in the report |
| 5 | Conclusions and limitations | `Discussion` in the report |

Nothing enters a section before the step that owns it. The report is built up as the work proceeds rather than written at the end, and the workflow ends with model selection and evaluation: the `Discussion` in step 5 is its last part.

The report also carries a standing disclaimer, between `Discussion` and `Appendix`, saying it was written with the help of agentic AI at every stage. It is in the template from the outset rather than added at the end, and the agent will not remove it.

## What is in the folder

| Location | What it is |
| --- | --- |
| [CLAUDE.md](CLAUDE.md) | Imports the contract so the agent picks it up automatically. Nothing to edit here. |
| [instructions.md](instructions.md) | The working contract. The agent reads this; you change it by prefixing a message with `FRAMEWORK`. |
| [ML Guide.md](ML%20Guide.md) | What the book says (Part I), the procedure the agent follows for every model decision (Part II), and the formats of its decision records and recommendation reports (Part III). Changed only with `FRAMEWORK`. |
| [Report.md](Report.md) | The completed example analysis: the report on the heart failure data, sub-task 1. |
| [Appendix.md](Appendix.md) | The completed example analysis: the running record for the same work — data, problem, workings, decision records, recommendation, log, code guide. |
| `Attachments/` | Your data. Never modified. Holds the heart failure data used by the example analysis; see [Attachments/SOURCE.md](Attachments/SOURCE.md). |
| `Code/` | The environment and `viz_style.py`, which carries the figure conventions. Your scripts and outputs go here. `advisor/` will hold the deterministic core the agent calls for ranking, cross-validation, confidence and the recommendation (not yet implemented). Until then, each analysis writes an interim core: the example analysis used `Code/core.py` (not reviewed), which `Code/advisor/` will replace. |
| [Setup.md](Setup.md) | Installation and the everyday commands. |

## Report and appendix

Two documents, two readers.

`Report.md` is the argument: what was asked, what was done, what was found, and what it does not support. It stays short, carries no diagnostic detail, and every number in it comes from generated output rather than from anyone's memory.

`Appendix.md` is the record, and it fills up from the first step. Every decision with its reasoning and what it cost, every workings, every check that changed nothing, and every decision that was later reversed — marked superseded rather than deleted, because a reader cannot judge a choice without seeing the alternatives.

## Changing the contract

Prefix a message with `FRAMEWORK` and the agent treats it as a change to `instructions.md` rather than a request about the analysis. It applies the rule, applies it retrospectively to work already done, and commits it on its own so the rule can travel to another project without the analysis coming with it. The same applies to Parts II and III of `ML Guide.md` and to the code that implements them, which change together.

That is how the current contract was built: each rule was written the moment the agent did something that was not wanted.

## Version control

Commit as you go. The agent stages named files rather than everything, so an unfinished edit of yours is never swept into its commit, and it will not commit or push unless you ask.

## Licence

This workspace is based on the [human-agentic-data-analysis](https://github.com/Vivid-Insights/human-agentic-data-analysis) template by Vivid-Insights, licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Changes in this repository are shared under the same licence; see [LICENSE](LICENSE).

The included dataset is the UCI Heart Failure Clinical Records dataset (CC BY 4.0), credited in [Attachments/SOURCE.md](Attachments/SOURCE.md). Any other data you analyse remains under its owners' terms.

The book the guide is based on is read at [smlbook.org](https://smlbook.org/) and remains under its owners' terms.
