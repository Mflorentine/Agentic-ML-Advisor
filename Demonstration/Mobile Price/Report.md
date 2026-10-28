# [Title]

*Chosen by the user at the end of step 5, from the titles suggested once the `Discussion` is written.*

## Introduction

A maker designing a new mobile phone has to decide which price band it belongs in. We want to place a phone in one of four price bands, from low to very high cost, using only its specifications. The data are the Mobile Price Classification dataset (Sharma, 2018): 2,000 phones, each described by 20 specifications and labelled with its price band, with 500 phones in each band. Fourteen specifications are numbers, such as battery capacity, memory, screen size, pixel resolution, camera megapixels and the number of processor cores. Six record whether the phone has Bluetooth, dual SIM, 3G, 4G, a touch screen or wifi. The source does not say where the phones come from, what their prices were, or where the boundaries between the bands lie.

Each band is treated as a separate category, so the order of the bands is not used, and every wrong band counts as one error. Models are compared by accuracy, the share of phones placed in the right band. Alongside it we report which bands are mistaken for which. The reference is a rule that always predicts the same band. Because the four bands are equally common, it places 25 % of phones correctly. We count a model as successful if its accuracy on the held-out phones, less the amount its accuracy varies across the cross-validation folds, is above 25 %. We compare a small set of model types from Lindholm et al. (2026) by cross-validation on 1,600 of the phones, and then evaluate the chosen one once on the remaining 400, held out until that point. The question is one of prediction for new phones, not of how the specifications are connected to price.

1. Predict a phone's price band (low, medium, high or very high cost) from its 20 specifications.

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
- Sharma, A. (2018). *Mobile Price Classification* [Dataset], version 1. Kaggle. [https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification).
