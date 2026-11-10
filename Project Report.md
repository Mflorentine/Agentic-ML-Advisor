# [Title]

*Chosen by the user at the end of step 5, from the titles suggested once the `Discussion` is written.*

## Abstract

*Draft*

The analysis asks whether students who will drop out of a higher-education course can be identified after their first year. The data are 4,424 students with 36 inputs: enrolment information and results in the first and second semesters. The outcome is Dropout yes or no, with students still enrolled counted as not dropped out. The approach compares a small set of model types from the book by cross-validation, chooses one, and evaluates it once on a held-out test set of 885 students. Success is judged by F2, which weights catching dropouts more heavily than unneeded flags, and the chosen model must beat flagging every student. The problem, the metric and the split were fixed before any model was compared. So far the training data have been checked for class balance and separability, and the year-one results and tuition status have been plotted. A single logistic regression was fitted only to check separability; no models have been compared.

## Introduction

Students who leave higher education before finishing their course leave without a degree, and support can reach them only if they are identified in time. This analysis asks whether students who end their course as dropouts can be recognised from what is recorded by the end of their first year: their enrolment information and their results in the first and second semesters.

The data describe 4,424 students of a higher-education institution in Portugal. Each student is labelled Dropout or not; students who graduated and students still enrolled at the end of the normal course duration are both labelled not dropout. The aim is to predict this label for students who are not yet in the data, so that support can be offered to those flagged. Success is judged by F2, a score that weights catching dropouts more heavily than unneeded flags, because a missed dropout is the costlier error. A prediction is measured against two references: a baseline that never flags a student, and flagging every student.

The approach compares a small set of model types from the book by cross-validation on the training data, chooses one, and then evaluates the chosen model once on a held-out test set that has informed no choice.

1. Predict Dropout yes/no after the first year, for students not yet in the data, from enrolment information and the first and second semester results, with success measured by F2 on the test set against the two references.

## Methods

### Data and evaluation

The data come from one file of 4,424 students, one row per student: the Student Dropout dataset published by the UCI Machine Learning Repository (Realinho et al., 2021). The repository documents the inputs as the information known at enrolment and the students' results at the end of the first and second semesters, and the outcome as the student's status at the end of the normal course duration. The repository page does not name the institution or the enrolment years. No value is missing, and no row was removed or changed. Nine integer columns that are codes rather than amounts are treated as categories, and the yes/no flags and counts as numbers.

The outcome is binary: Dropout is 1, and Graduate or still Enrolled is 0. Dropout is 32.1% of students. The data are split at random into 3,539 students for training and 885 for testing (20%). The split is stratified so that both sets keep the same share of dropouts, and the seed is 2026. Each student is one row, so no group is kept together. The test set is held out and used once, in the final evaluation; no choice is made with it.

The metric that decides between models is F2, the F-beta score with β = 2, which weights recall (the share of dropouts flagged) twice as heavily as precision (the share of flags that were right) (Lindholm et al., 2026). Recall, precision and the confusion matrix are reported alongside it. The baseline is the most common training class, which here means "not dropout" for every student. That baseline has F2 = 0. Flagging every student is reported beside each model as a reference. The success criterion is that the chosen model's F2 on the test set is above the F2 of flagging every student on the same test rows.

### Dropout after year one

The admissible configurations were set before any model was compared. Class probabilities are required, so only logistic regression is admissible. Two configurations remain: logistic regression with an L2 penalty, and the same with polynomial terms in the non-binary numeric inputs. The baseline, which always predicts "not dropout", is included in every comparison. Logistic regression with the L2 penalty is the simple-first model. It is compared with the baseline first, and the polynomial version is added afterwards.

Each configuration is compared by nested cross-validation on the training data. The outer loop uses 10 stratified, shuffled folds with seed 2026, the same for every configuration. Within each outer training set, an inner 5-fold grid search chooses the L2 strength, over values from 10⁻⁴ to 10⁴, and, for the polynomial version, the degree (2 or 3). The decision threshold is also chosen in the inner loop, by F2 over a grid from 0.05 to 0.95, so that each configuration is compared at its own best threshold.

The comparison between two configurations is the mean of the ten outer-fold differences in F2, and its uncertainty is the standard deviation of those differences. A configuration is eligible for recommendation if it beats the baseline by a clear margin, which is at least one standard deviation, and meets every requirement. The recommended configuration is the eligible one with the best mean F2. A tie is broken by the fewer add-ons, then by the prior ranking, then by the mean. The chosen configuration is refitted on all training data, and the locked test set is evaluated once, with the baseline evaluated on the same rows.

## Results

### The training data

Each panel is one outcome, and each bar counts the students with a given total of approved units, as a share of their own panel. The two panels can be compared although the groups differ in size.

![[Code/outputs/dropout/figures/fig1_approved_units.png|640]]

<small><b>Figure 1.</b> Total curricular units approved over the first and second semesters, for the training students: 1,137 who dropped out (left panel) and 2,402 who did not (right panel). Each bar is the share of its panel's students with the total shown on the horizontal axis; the bars in each panel sum to 100%.</small>

Each bar is one group of training students, split by whether their tuition fees are up to date. The height of a bar is the share of that group who dropped out; the number under the bar is the number of students in the group.

![[Code/outputs/dropout/figures/fig2_tuition_share.png|460]]

<small><b>Figure 2.</b> Share of the training students who dropped out, for those whose tuition fees are up to date (left bar) and those whose fees are not (right bar). The number under each bar is the number of students in that group.</small>

## Discussion

*Written in step 5, organised by theme: why the recommended configuration and not the others, how it makes predictions, what it can and cannot be used for, and the limits of the evaluation.*

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to [Appendix.md](Appendix.md), where the data, the decisions and the full workings are recorded.*

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). *Machine Learning – A First Course for Engineers and Scientists*, 2nd edition, online draft of 1 September 2026. [https://smlbook.org/](https://smlbook.org/). Details taken from `ML Guide.md`. Not yet checked against the title page on smlbook.org; the local copy in `Attachments/smlbook/` is not in the workspace.
- Realinho, V., Vieira Martins, M., Machado, J. and Baptista, L. (2021). Predict Students' Dropout and Academic Success [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5MC89](https://doi.org/10.24432/C5MC89). Checked on the UCI dataset page and its metadata on 10 November 2026.
