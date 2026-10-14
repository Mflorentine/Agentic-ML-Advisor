# [Title]

*Chosen by the user at the end of step 5, from the titles suggested once the `Discussion` is written.*

## Introduction

Heart failure patients at high risk of dying could be monitored more closely if that risk could be recognised in advance. We want to flag such patients from the clinical measurements recorded in their medical records. The data cover 299 patients with severe heart failure, NYHA class III or IV, treated at two hospitals in Faisalabad, Pakistan, in 2015. For each patient we predict whether they died during their follow-up period. Follow-up lasted between 4 and 285 days, so the outcome records death within each patient's own follow-up, not survival over a fixed period.

We predict from eleven inputs: age, sex, smoking, anaemia, diabetes, high blood pressure, ejection fraction, and the blood levels of creatinine phosphokinase, platelets, serum creatinine and serum sodium. The length of follow-up is in the data but isn't used, because it ends when the outcome happens. The question is one of prediction for new patients, not of which factors cause death. Missing a patient who dies is worse than a false alarm. So we judge models by the F2 score, which counts recall twice as heavily as precision. The same score is used to choose the model, to set the decision threshold on its predicted probabilities, and to judge whether it succeeded. We count the model as successful if its F2 on the held-out patients is above that of flagging every patient, 0.70 on the training patients, by more than F2 varies across the cross-validation folds.

We compare a small set of model types from Lindholm et al.'s *Machine Learning – A First Course for Engineers and Scientists* by cross-validation on 239 of the patients, and then evaluate the chosen one once on the remaining 60, which are held out until that point.

1. Predict whether a patient dies during their follow-up period from the eleven inputs.

## Methods

*Written in step 4, one sub-heading per sub-task, in step with `Results`: how candidate configurations were chosen, how they were compared (nested cross-validation), how the recommendation was decided, and how the final model was evaluated.*

## Results

Figures 1 to 3 describe the 239 training patients; the 60 held-out patients are not shown. In all three, blue marks patients who did not die during follow-up and orange those who died.

![Figure 1](Code/outputs/figures/fig1_numeric_by_outcome.png)

<small><b>Figure 1.</b> Distribution of the six numeric inputs among training patients who did not die (blue, n = 162) and who died (orange, n = 77). Each outline is a histogram whose bar heights are the share of that group, so the two outlines can be compared despite the different group sizes. Serum creatinine and creatinine phosphokinase are drawn on a logarithmic axis.</small>

Each panel compares the shapes of two distributions, not their counts. Where the orange outline lies to one side of the blue one, patients who died tended to have values on that side.

![Figure 2](Code/outputs/figures/fig2_death_share_binary.png)

<small><b>Figure 2.</b> Share of training patients who died, within each level of the five yes/no inputs. The number inside each bar is the number of patients at that level. The dashed line is the share who died among all 239 training patients, 32.2 %.</small>

![Figure 3](Code/outputs/figures/fig3_creatinine_ejection.png)

<small><b>Figure 3.</b> Serum creatinine (logarithmic axis) against ejection fraction for each training patient, coloured by outcome. Ejection fraction takes only 16 distinct values among the training patients, so many points lie on the same horizontal lines and some overlap.</small>

*In step 4: the recommended configuration, its test-set result against the baseline, a summary of the ranking, the selection confidence, and evaluation figures such as learning curves or precision–recall curves.*

## Discussion

*Written in step 5, organised by theme: why the recommended configuration and not the others, how it makes predictions, what it can and cannot be used for, and the limits of the evaluation.*

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to [Appendix.md](Appendix.md), where the data, the decisions and the full workings are recorded.*
