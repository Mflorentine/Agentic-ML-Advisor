# [Title]

*Chosen by the user at the end of step 5, from the titles suggested once the `Discussion` is written.*

## Abstract

*Draft*

This analysis asks how well the fuel economy of a car, in miles per gallon, can be predicted from its engine size, horsepower, weight, acceleration, number of cylinders, model year and country of origin. The data are 392 cars from model years 1970 to 1982, from the Auto MPG dataset of the UCI Machine Learning Repository, after six cars with no horsepower value were dropped. Cars with the same name are kept together when the data is split. The problem, the measure of success and the methods to compare are to be agreed before any model is fitted.

## Introduction

*The problem and its sub-tasks go in at the end of step 2, before anything is trained.*

## Methods

*Opens with a sub-section `Data and evaluation`, written at the end of step 2: the data and its scope, the split and the held-out test set, the metric, the baseline and the success criteria. Then one sub-heading per sub-task, drafted in step 4b once the method is agreed and made final in step 4h, in step with `Results`: how candidate configurations were chosen, how they were compared (nested cross-validation), how the recommendation was decided, and how the final model was evaluated.*

## Results

*Opens with a sub-section `The training data`, matching `Data and evaluation` in `Methods`: figures of the training data go in during step 3. In step 4: the recommended configuration, its test-set result against the baseline, whether the agreed success criterion was met, stated plainly as met or not met; where a decision threshold was tuned for F2 or another F-beta, the F-beta of flagging every case beside the model's; a summary of the ranking, the selection confidence, and evaluation figures such as learning curves or precision–recall curves.*

## Discussion

*Written in step 5, organised by theme: why the recommended configuration and not the others, how it makes predictions, what it can and cannot be used for, and the limits of the evaluation.*

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to [Appendix.md](Appendix.md), where the data, the decisions and the full workings are recorded.*

## References

*Works cited in this report, copied from the References of Appendix.md. Always the last section.*
