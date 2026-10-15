# [Title]

*A plain, literal title naming what the project built and what it is for.*

## Abstract

*The whole project in one paragraph: the problem it addresses, what was built in parts A, B and C, what the heart failure example showed, and the main limitation.*

## Introduction

*The area the project belongs to and why it matters; the background to each of the three parts — guiding a user through an analysis step by step, advising on model choice from a textbook, and keeping the work traceable and reproducible — and the gap each addresses; and what this project does.*

## Methods

### A. The step-by-step agentic workflow

*How the workflow in [instructions.md](instructions.md) is designed: the five steps, the rule of one step per request, how the user directs and closes each step, and how the report and appendix are built up as the work proceeds.*

### B. The ML advisor grounded in smlbook.org

*How chapters 2, 3, 4 and 13 of the book were distilled into [ML Guide.md](ML%20Guide.md), how the reasoning procedure turns them into a recommendation, and how the deterministic parts are computed by code (the interim core, `Code/core.py`) rather than by the agent.*

### C. Traceability and reproducibility

*How each decision is recorded and can be checked: Decision Records, provenance tags on every rule, checksums of the source data, recorded seeds, and one commit per step.*

## Results

### A. The step-by-step agentic workflow

*What the workflow produced when used end to end on the heart failure example, with evidence from [Examples/heart-failure/](Examples/heart-failure/).*

### B. The ML advisor grounded in smlbook.org

*What the advisor recommended for the heart failure example and how its prior ranking compared with cross-validation, with evidence from [Examples/heart-failure/](Examples/heart-failure/).*

### C. Traceability and reproducibility

*What a reader can trace and reproduce in the heart failure example — from a reported number back to its decision record, rule, code and data — with evidence from [Examples/heart-failure/](Examples/heart-failure/).*

## Discussion

*What the project achieved, what the findings on A, B and C mean when taken together, and what the work makes possible next.*

## Limitations

*What qualifies the findings: problems met, what was not built or not tested, and what a single worked example cannot show.*

## Disclaimer

This report was written with the help of agentic AI: designing the workflow, writing the code, running the example analysis and drafting the text. Each part was directed and reviewed by the author.

## Appendix

*Pointers to the material behind this report: [ML Guide.md](ML%20Guide.md), the advisor's knowledge and reasoning procedure; [instructions.md](instructions.md), the working contract; and [Examples/heart-failure/](Examples/heart-failure/), the worked example with its full record.*

## References

*Works cited in this report, each cited in the text in author–date style. Always the last section.*
