# Agentic ML Advisor: step-by-step guidance through the ML workflow

A folder for working through a machine learning problem with an agent, one step at a time, and coming out with a recommended model and a report you can defend.

It is an Obsidian vault with [Claudian](https://github.com/YishenTu/claudian) installed, so the conversation happens beside the documents it is writing. The agent's working contract is [instructions.md](instructions.md), which it reads automatically. The agent's knowledge of machine learning comes from chapters 2, 3, 4 and 13 of Lindholm et al., [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), distilled into [ML Guide.md](ML%20Guide.md) with page references.

## What makes this different from just asking

Ask an agent to solve a prediction problem and it will hand you a finished model in one pass: a model picked, trained, charts drawn, conclusions written. It will look right. You will have no idea which choices were made on your behalf.

This folder is built to stop that. The agent does one step per request and then stops. It does not add analysis, findings or prose you did not ask for. It agrees the method with you before applying it, works through one sub-task at a time, and asks before it touches the held-out test data, which it uses once. The parts that require judgement stay with you, which is the whole point.

Every model choice is recorded as it is made. Each decision gets a Decision Record that names the evidence and the rule it rests on, with the book page — or says plainly that the rule is our own inference. The mechanical parts — which models are admissible, how they rank, how confident the choice is, which one is recommended — are computed by code, not argued by the agent.

## Start here

1. **Install** the environment: [Setup.md](Setup.md) covers Obsidian, `uv` and Python.
2. **Put your data** in `Attachments/`.
3. **Ask for step 1** in a Claudian conversation: import and describe the data. The agent asks for a name for the analysis and sets up two files at the top of the workspace, [Project Report.md](Project%20Report.md) and [Appendix.md](Appendix.md). **You work in those two files throughout.**
4. **Work through the five steps**, one request at a time (below). To see the criteria the agent works through, open [Glossary.md](Glossary.md).
5. **When the analysis is finished**, say so: the agent submits it to `Demonstration/<Name>/` and resets the two files for the next one.

To see what a finished analysis looks like, open one in [Demonstration/](Demonstration/):

- [xG/](Demonstration/xG/): an expected-goals model for football shots from StatsBomb open data, and whether knowing the team improves it. [Report](Demonstration/xG/Report.md), [Appendix](Demonstration/xG/Appendix.md).
- [Heart Failure/](Demonstration/Heart%20Failure/): predicting death during follow-up from the Heart Failure Clinical Records data. [Report](Demonstration/Heart%20Failure/Demonstration%20Report.md), [Appendix](Demonstration/Heart%20Failure/Demonstration%20Appendix.md).
- [Sepsis/](Demonstration/Sepsis/): stopped after step 1.

Each finished analysis's code, outputs and data stay in `Code/` and `Attachments/`, so the file paths and checksums recorded in it stay valid; [Code/README.md](Code/README.md) says which files belong to which analysis.

## Progress

| Part of the brief | Status |
| --- | --- |
| Agentic system that guides users through ML problem-solving | Done: the five-step workflow in [instructions.md](instructions.md). |
| Uses smlbook.org chapters 2, 3, 4 and 13 | Done: [ML Guide.md](ML%20Guide.md), with page references. |
| Helps users choose ML techniques | Done for classification, using an interim core (`Code/core.py`); the reusable `Code/advisor/` is next. |
| Step-by-step guidance from formulation to evaluation | Demonstrated end to end on the heart failure data ([Demonstration/Heart Failure/](Demonstration/Heart%20Failure/)) and the xG data ([Demonstration/xG/](Demonstration/xG/)). The sepsis demonstration stopped after step 1 ([Demonstration/Sepsis/](Demonstration/Sepsis/)). |
| Available online through GitHub | Done. |

### Next steps

See [Notes/Note for Florentine.md](Notes/Note%20for%20Florentine.md) for how the method is to be improved by working through the datasets, and [Notes/Davids Changes.md](Notes/Davids%20Changes.md) for the framework changes made since.

- Build `Code/advisor/`.
- Finish the sepsis and Mobile Price demonstrations. All are classification problems, making three datasets in total with heart failure.
- Write the report on the project as a whole, from [Templates/Whole-Project Report.md](Templates/Whole-Project%20Report.md).

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
| [Glossary.md](Glossary.md) | The checks and properties the advisor works through (Admissibility 1–4, Property 1–10), in plain words, with what each one changes, plus the other labels you will see in the decision records. Start here to see what criteria an analysis follows. Changed only with `FRAMEWORK`, together with the guide. |
| [Templates/](Templates/) | The empty [Report.md](Templates/Report.md) and [Appendix.md](Templates/Appendix.md), copied to the top of the workspace when an analysis starts; and [Whole-Project Report.md](Templates/Whole-Project%20Report.md), the template for a report on the project as a whole. Not edited by an analysis. |
| [Project Report.md](Project%20Report.md) and [Appendix.md](Appendix.md) | The analysis in progress: the report, built up through the five steps, and the running record (data, problem, workings, decision records, recommendation, log, code guide), filled from step 1. This is where you work. |
| [Demonstration/](Demonstration/) | Finished analyses, one folder each, submitted from the top of the workspace when an analysis is finished: [xG/](Demonstration/xG/), [Heart Failure/](Demonstration/Heart%20Failure/), and [Sepsis/](Demonstration/Sepsis/) (stopped after step 1). A finished analysis is not edited by a new one. |
| `Attachments/` | Your data. Never modified. Holds the data of the example analyses, and a local copy of the book in `smlbook/` (not committed); see [Attachments/SOURCE.md](Attachments/SOURCE.md). |
| [Notes/](Notes/) | Notes for collaborators: [Davids Changes.md](Notes/Davids%20Changes.md), a running summary of every framework change, and [Note for Florentine.md](Notes/Note%20for%20Florentine.md), the handover note. |
| [Code/](Code/) | The Python environment, the figure style (`sml_style.py`), and each analysis's scripts, interim core and outputs. [Code/README.md](Code/README.md) says which files belong to which analysis. |
| [Setup.md](Setup.md) | Installation and the everyday commands. |

## Report and appendix

Two documents, two readers.

`Project Report.md` is the argument: what was asked, what was done, what was found, and what it does not support. It stays short, carries no diagnostic detail, and every number in it comes from generated output rather than from anyone's memory.

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
