# [Title]

*Chosen by the user at the end of step 5, from the titles suggested once the `Discussion` is written.*

## Introduction

Patients in intensive care who are about to develop sepsis could be watched more closely if they could be recognised early in their stay. We want to flag such patients using only what is recorded in their first six hours in the intensive care unit (ICU). The data are the training data of the PhysioNet/Computing in Cardiology Challenge 2019 (Reyna et al., 2019): hourly vital signs, laboratory values and patient characteristics for 40,336 ICU patients at two US hospitals, Beth Israel Deaconess Medical Center and Emory University Hospital (Reyna et al., 2020). Whether a patient has sepsis is not recorded at the bedside. It is a label constructed from the Sepsis-3 criteria, which switches on six hours before the estimated onset.

For each patient we predict whether the sepsis label switches on within the 48 hours after the first six ICU hours, while the patient is still in the ICU. A patient who leaves the ICU within that period without it counts as not having developed sepsis. The inputs are the 27 vital signs and laboratory values recorded in the first six hours, together with age, sex, the type of ICU and the time between hospital and ICU admission. The time the patient has spent in the ICU, and the length of the stay, are not used. The analysis covers the 39,088 patients who were in the ICU during the first six hours and whose label had not yet switched on, of whom 3.15 % develop sepsis within the period. The question is one of prediction for new patients, not of which measurements are connected to sepsis.

Missing a patient who develops sepsis is worse than a false alarm. Models are compared by the area under the precision–recall curve, which summarises how well a model ranks patients over all decision thresholds; a model with no skill scores the share of patients who develop sepsis. Alongside it we report F2, which counts recall twice as heavily as precision, and precision and recall themselves, at a decision threshold chosen on the training patients. We count the model as successful if its area under the precision–recall curve on the held-out patients exceeds their share of sepsis cases by more than the area varies across the cross-validation folds. We compare a small set of model types from Lindholm et al. (2026) by cross-validation on 31,270 of the patients, and then evaluate the chosen one once on the remaining 7,818, drawn from both hospitals and held out until that point.

1. Predict, from the first six ICU hours, whether the sepsis label switches on within the following 48 hours while the patient is still in the ICU.

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

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published).
- Reyna, M., Josef, C., Jeter, R., Shashikumar, S., Moody, B., Westover, M. B., Sharma, A., Nemati, S. and Clifford, G. D. (2019). *Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019* (version 1.0.0) [Dataset]. PhysioNet. [https://doi.org/10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857).
- Reyna, M. A., Josef, C. S., Jeter, R., Shashikumar, S. P., Westover, M. B., Nemati, S., Clifford, G. D. and Sharma, A. (2020). Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019. *Critical Care Medicine*, 48(2), 210–217. [https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/).
