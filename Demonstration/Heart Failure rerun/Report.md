# [Title]

*Chosen by the user at the end of step 5, from the titles suggested once the `Discussion` is written.*

## Introduction

Patients with advanced heart failure who are likely to die in the coming months could be followed more closely if they could be recognised when follow-up starts. We want to flag such patients from routine clinical measurements. The data are the Heart Failure Clinical Records dataset (Heart Failure Clinical Records, 2020): 299 patients with left ventricular systolic dysfunction in NYHA class III or IV, treated at two hospitals in Faisalabad, Pakistan, between April and December 2015 (Chicco and Jurman, 2020). For each patient the data record age and sex; whether they had anaemia, diabetes or high blood pressure, and whether they smoked; their ejection fraction; and blood levels of creatinine phosphokinase, platelets, serum creatinine and serum sodium. They also record whether the patient died during a follow-up period whose length varies from patient to patient. 96 of the 299 died. A patient recorded as not having died was not observed to die during their follow-up; the source does not say how follow-up ended for them. The length of follow-up is not used as an input, because it is known only once follow-up ends.

Missing a patient who dies is worse than a false alarm. Models are compared by the area under the precision–recall curve, which summarises how well a model ranks patients over all decision thresholds; a model with no skill scores the share of patients who die. Alongside it we report F2, which counts recall twice as heavily as precision, and precision and recall themselves, at a decision threshold chosen on the training patients. We count the model as successful if its area under the precision–recall curve on the held-out patients exceeds their share of deaths by more than the area varies across the cross-validation folds. We compare a small set of model types from Lindholm et al. (2026) by cross-validation on 239 of the patients, and then evaluate the chosen one once on the remaining 60. These are the same held-out patients as in an earlier analysis of these data, so that the two methods can be compared on equal terms. The question is one of prediction for new patients, not of how the measurements are connected to death.

1. Predict, from the 11 clinical measurements, whether a patient dies during the follow-up period.

## Methods

*Written in step 4, one sub-heading per sub-task, in step with `Results`: how candidate configurations were chosen, how they were compared (nested cross-validation), how the recommendation was decided, and how the final model was evaluated.*

## Results

*Figures of the training data go in during step 3. In step 4: the recommended configuration, its test-set result against the baseline, a summary of the ranking, the selection confidence, and evaluation figures such as learning curves or precision–recall curves.*

## Discussion

*Written in step 5, organised by theme: why the recommended configuration and not the others, how it makes predictions, what it can and cannot be used for, and the limits of the evaluation.*

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to [Appendix.md](Appendix.md), where the data, the decisions and the full workings are recorded.*

## References

- Chicco, D. and Jurman, G. (2020). Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone. *BMC Medical Informatics and Decision Making*, 20, 16. [https://doi.org/10.1186/s12911-020-1023-5](https://doi.org/10.1186/s12911-020-1023-5).
- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R).
- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published).
