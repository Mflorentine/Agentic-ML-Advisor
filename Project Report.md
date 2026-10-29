# [Title]

*A plain, literal title naming what the project built and what it is for.*

## Abstract

*The project in one paragraph: the problems it addresses, the machine learning methods used and how they were chosen, how the work relates to smlbook.org, how the models were trained and validated, what was found, and the main limitation.*

## Introduction

*The area the project belongs to and why it matters; the problems addressed by the analyses in `Demonstration/`; why the methods follow smlbook.org; and what this project does. It does not anticipate the results.*

## Methods

*Three sub-sections: the machine learning methods used and how they were chosen; how the work relates to smlbook.org; and the training and validation methods. Results uses the same sub-headings in the same order.*

### The machine learning methods used

The workflow chooses among a fixed set of model types from chapters 2 and 3 of Lindholm et al. (2026): linear regression, logistic regression, Poisson and exponential generalised linear models, k-nearest neighbours and decision trees. Polynomial terms (squares and cubes of the numerical inputs) and L2 regularisation can be added to the regression models where the book allows them, which gives fourteen configurations in all. Methods from other chapters, such as ensembles or neural networks, are not used. Which inputs a model receives, and whether any is transformed, is agreed with the user beforehand and is not part of the comparison. The choice among the fourteen is then made in four steps, illustrated here by the four analyses: the original Heart Failure analysis, Sepsis, Mobile Price and the Heart Failure rerun.

First, configurations that cannot serve the problem are removed. The output decides the families (Lindholm et al., 2026). In all four analyses it is a category, either a yes/no outcome or one of four price bands, so linear regression and the two generalised linear models, which predict numbers, were excluded every time.

Two further rules remove logistic regression without regularisation when its parameters would not be well defined. When a straight boundary separates the training classes perfectly, the book notes that the parameters grow without limit and that regularisation is the usual remedy (Lindholm et al., 2026); this removed the unregularised logistic models in Mobile Price. When some inputs exactly duplicate others, the parameters are not uniquely determined (Lindholm et al., 2026); that this rules the unregularised models out is our reading. It removed them in Sepsis, where three indicator columns for the type of intensive-care unit always summed to one. Requirements the user marks as essential would remove configurations too, but none was marked in these analyses.

Second, the remaining configurations are ranked before any model is fitted, from properties of the problem and the user's stated preferences. The best-ranked few are kept, together with the simplest model for the task and a baseline. This ranking and its scores are our addition, not the book's. It decides what is compared first, not what is chosen. In the original Heart Failure analysis it left out k-nearest neighbours and logistic regression with both additions. In the rerun it left out k-nearest neighbours and the decision tree, which the diagnosis in the third step later brought back.

Third, the kept configurations are compared by cross-validation on the metric agreed for the problem, as the book recommends for choosing between models (Lindholm et al., 2026). Each model's own settings, such as the regularisation strength or the size of a tree, are tuned inside the training part of each fold. The leading model is then checked for underfitting and overfitting following the book's chapter on working practice (Lindholm et al., 2026), and the comparison is extended where the check points. In Mobile Price this meant a wider range of regularisation strengths; in the rerun it meant adding k-nearest neighbours and a decision tree.

Fourth, the recommendation is the simplest of the models whose cross-validated score cannot be told apart from the best, following the book's advice not to settle on a complicated model where a simpler one would do (Lindholm et al., 2026). "Cannot be told apart" means a difference smaller than half its variation across the folds, a threshold that is ours. This rule decided three of the four analyses:
- in the original Heart Failure analysis, the decision tree over logistic regression with squares and cubes;
- in Sepsis, logistic regression with L2 over the same with squares and cubes added;
- in the rerun, plain logistic regression over three logistic models with additions.

In Mobile Price, logistic regression with L2 was ahead of every other model by more than the variation of the difference, so the rule did not come into play.

Each recommendation is reported with a selection confidence, which is ours, computed from three factors: whether the recommended model is ahead of the runner-up by at least the variation of the difference across the folds (C1 clear), by at least half of it (moderate) or by less (none); whether it is ahead of the baseline by at least that variation (C2 clear or not clear), the baseline being the most common class in the original Heart Failure analysis; and whether its validation error was still falling between 80 % and 100 % of the training data (C3 limited, otherwise adequate); the confidence is High when C1 and C2 are clear and C3 is adequate, Low when C1 is none or C2 is not clear, and Medium otherwise.

### How it relates to smlbook.org

The method rests on four chapters of Lindholm et al. (2026):
- chapter 2, on supervised learning, k-nearest neighbours and decision trees;
- chapter 3, on linear and logistic regression, polynomial terms with L2 regularisation, and generalised linear models;
- chapter 4, on evaluating performance;
- chapter 13, on the practical side of machine learning.

What these chapters say is summarised, with page references, in Part I of the guide the advisor follows (`ML Guide.md`). Methods outside the four chapters are not used. Where the evidence suggests one might help, it is recorded as a flag and never claimed to be better. This happened once: in Sepsis, survival analysis was flagged for patients who left intensive care before the outcome could be observed, a topic the book does not cover.

The method follows the book's practice at the points that decide a result (Lindholm et al., 2026):
- **Before any model is fitted,** the problem is fixed by agreeing the test data, a single metric and a baseline the model must beat.
- **The test data are held out** and used once, after every choice has been made.
- **Models are compared** by k-fold cross-validation on the training data.
- **The work starts simple,** and adds complexity only when diagnosing underfitting or overfitting calls for it.
- **The work avoids ending with a complicated model** where a simpler one would have done.
- **When one outcome is rare, or one kind of error costs more,** precision, recall and the precision–recall curve are used rather than the misclassification rate, and the decision threshold is a trade-off chosen by the user.

Fitting every preprocessing step inside each cross-validation fold extends the book's rule that preprocessing is fitted on the training data only; the extension is ours.

Much of the method is ours, and is marked as ours wherever it is used: the step-by-step workflow in which the user agrees each step before it is applied (`instructions.md`); the interim cores that compute the mechanical parts, so that the agent does not; the prior ranking of candidates before any model is fitted; the selection confidence reported with each recommendation; and the numerical thresholds that turn the book's advice into rules, such as treating two models as indistinguishable when their difference is less than half its variation across the folds. Every rule in Part II of the guide carries a tag saying whether it is the book's advice ([B]), a fact from the book that we turned into advice ([B→I]), or our own ([I]), and the Decision Records copy the tags of the rules they apply, so a reader can see how much of each choice rests on the book. To show how far the ranking predicted the comparison, each analysis also recorded, all in ways that are ours, the order it expected the kept configurations to take, written down before cross-validation and checked against it afterwards; whether the configuration that won cross-validation had been first in the ranking (prior agreement); and how many of the ranking entries behind the recommended configuration's score carry each tag (grounding).

The method changed five times while the analyses were worked through, each change made in the guide and recorded in its version note.
- **Two moved it towards the book.**
  - When one class is rare, the diagnosis now measures error with the agreed metric rather than the misclassification rate, following the book's warning that the misclassification rate misleads for imbalanced classes.
  - Underfitting is judged against what the application needs, as the book judges performance against a reference level.

  Both were prompted by Sepsis, where 3 % of patients developed sepsis.
- **Three fill gaps the book leaves.**
  - The cross-validation folds are stratified in the same way as the test split (prompted by Sepsis).
  - The uncertainty of the test result is the spread of the metric across the outer cross-validation folds. The four chapters give no method for it; this one rests on the book's account of k-fold cross-validation and of how a held-out estimate varies with its size.
  - Model variants with an input removed by backward elimination cannot be recommended unless the removal was kept, so that which inputs a model receives stays a decision taken with the user (prompted by Mobile Price).

The original Heart Failure analysis chose its model and made its test evaluation before any of these changes. Sepsis was worked through while the first four were made. Mobile Price prompted the fifth. The Heart Failure rerun used the method with all five in place.

### Training and validation methods 

Each dataset was divided once into training data and test data, before any model was fitted (Lindholm et al., 2026). A fifth of the rows was set aside as test data. The rows were shuffled first, as the book advises. The split was also stratified, so that both parts keep the same share of each outcome; stratifying the split and the folds is our choice. The test data were then locked: nothing in the exploration or the model choice read them.

The Heart Failure rerun did not make a new split. At the user's choice, it reused the original analysis's test set, so that the two versions of the method are compared on exactly the same 60 patients. Those patients had already produced the original analysis's test result, which was known, so the rerun's test result is a like-for-like comparison rather than a fresh estimate.

Models were compared on the training data alone, by cross-validation (Lindholm et al., 2026). The training data are divided into ten parts, or folds. Each model is fitted ten times, each time on nine folds, and scored on the tenth, which it has not seen; the ten scores are averaged. Every model was scored on the same ten folds, so two models can be compared fold by fold. The variation of the difference across the folds shows whether a gap between them is larger than chance would produce.

Each model also has settings that must be chosen, such as the strength of its regularisation, the number of neighbours or the size of a tree. Choosing them on the same folds that score the model would make the score too favourable (Lindholm et al., 2026). So the settings were chosen inside each of the ten training parts by a second, smaller cross-validation with five folds, and only then was the model scored on the held-out fold. This is called nested cross-validation; the reason for it is the book's, and this design of it is ours. Every step that learns from the data, such as rescaling the inputs, was also fitted inside the training part each time.

Where the user wanted a flag rather than only a probability, a decision threshold was chosen after the model, on the training data only. It was set to maximise F2, which counts recall twice as heavily as precision, the trade-off the user chose (Lindholm et al., 2026). In the two Heart Failure analyses, the model's F2 at its threshold is reported beside the F2 of flagging every patient, which has recall 1 and precision equal to the share of deaths; in the original analysis this was the agreed baseline for F2.

The chosen model was then refitted on all the training data and evaluated once on the test data, only after the user had approved it. The uncertainty reported with that result is the variation of the deciding metric across the ten outer folds. Each fold is smaller than the test set, so this approximates the uncertainty of the test result rather than measuring it; using it in this way is ours. Each analysis fixed its success criterion before any model was fitted: the test result had to exceed the baseline by more than this uncertainty, the baseline being flagging nobody in Sepsis and the rerun, the most common price band in Mobile Price, and, in the original Heart Failure analysis, the F2 of flagging every patient on the training rows.

| Analysis | Split | Training / test rows (positives) | Folds stratified by | Metric for comparing and tuning | Decision threshold | Uncertainty of the test result |
| --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | new | 239 / 60 (77 / 19 deaths) | outcome | F2 | chosen to maximise F2 | fold variation of F2 at the tuned threshold |
| Sepsis | new, by patient | 31,270 / 7,818 (984 / 246 with sepsis) | outcome and hospital | PR-AUC | chosen to maximise F2 | fold variation of PR-AUC |
| Mobile Price | new | 1,600 / 400 (400 / 100 per price band) | price band | accuracy | none (not needed) | fold variation of accuracy |
| Heart Failure rerun | reused from the original | 239 / 60 (77 / 19 deaths) | outcome | PR-AUC | chosen to maximise F2 | fold variation of PR-AUC |

All four analyses used seed 2026 for the split and the folds. PR-AUC is the area under the precision–recall curve, computed as average precision.


## Results

*What came out of each method, under the same sub-headings as Methods.*

### The machine learning methods used

Table 1 gives, for each analysis, the recommended configuration and its single evaluation on the test data, on the metric agreed for that problem, and whether that analysis's own success criterion was met. The uncertainty is the standard deviation of that metric across the ten outer cross-validation folds. The selection confidence is followed by its three factors: the margin over the runner-up (C1), the margin over the baseline (C2), and whether more training data was still lowering the validation error (C3).

<small><b>Table 1.</b> Recommended configuration and test result for each analysis.</small>

| Analysis | Recommended configuration | Deciding metric | Test result (fold SD) | Baseline | Test rows (positives) | Success criterion | Selection confidence (C1, C2, C3) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | decision tree, depth 3, minimum leaf size 20; threshold 0.2 | F2 | 0.6780 (0.0865) | 0.7038 (flag everyone, on the training rows; the agreed reference); the most common class scores 0 | 60 (19 deaths) | not met (required above 0.7038 + 0.0865 = 0.7903) | Low (none, clear, adequate) |
| Sepsis | logistic regression with L2, λ = 10⁻³; threshold 0.040 | PR-AUC | 0.0847 (0.0156) | 0.0315 (flag nobody, on the test data) | 7,818 (246 with sepsis) | met (required above 0.0315 + 0.0156 = 0.0471) | Low (none, clear, adequate) |
| Mobile Price | logistic regression with L2, λ = 10⁻⁵ | accuracy | 0.9600 (0.0141) | 0.2500 (most common band, on the test data) | 400 (100 per band) | met (0.9600 − 0.0141 = 0.9459, required above 0.2500) | High (clear, clear, adequate) |
| Heart Failure rerun | logistic regression; threshold 0.10 | PR-AUC | 0.6983 (0.0938) | 0.3167 (flag nobody, on the test data) | 60 (19 deaths) | met (0.6983 − 0.0938 = 0.6045, required above 0.3167) | Low (none, clear, adequate) |

**Heart Failure (original): cross-validation.** The mean F2 at threshold 0.5 was:
- flagging every patient 0.7032;
- decision tree 0.5567;
- logistic regression with squares and cubes 0.5286;
- logistic regression, with and without L2, 0.4798 each;
- the most common class 0.

A variant of the tree with a wider range of leaf sizes, added by the diagnosis, scored 0.5207. The tree's margin over the runner-up was 0.0281 (spread 0.1422), and its margin over the most common class 0.5567 (spread 0.1124).

**Sepsis: cross-validation.** The mean PR-AUC was:
- logistic regression with L2 0.0930;
- the same with squares and cubes 0.0907;
- k-nearest neighbours 0.0706;
- decision tree 0.0678;
- flagging nobody 0.0315.

The margin over the runner-up was 0.0023 (spread 0.0077), and over the baseline 0.0615 (spread 0.0156).

**Mobile Price: cross-validation.** The mean accuracy was:
- logistic regression with L2, with λ searched down to 10⁻⁸, 0.9706;
- the same with λ searched down to 10⁻⁴, 0.9637;
- with squares and cubes added, 0.9431;
- decision tree 0.8281;
- k-nearest neighbours 0.6250;
- the most common band 0.2500.

The margin over the runner-up was 0.0069 (spread 0.0055), and over the baseline 0.7206 (spread 0.0141).

**Heart Failure rerun: cross-validation.** The mean PR-AUC was:
- logistic regression with squares and cubes 0.7064;
- the same with L2 0.6882;
- logistic regression with L2 0.6703;
- logistic regression 0.6627;
- k-nearest neighbours 0.5633;
- decision tree 0.5546;
- flagging nobody 0.3221.

The recommended model's margin over the runner-up was −0.0437 (spread 0.1171), and over the baseline 0.3406 (spread 0.0892).

**The two Heart Failure analyses on the same 60 test patients (19 deaths).**
- The rerun used a different deciding metric and success criterion from the original: PR-AUC, with success meaning test PR-AUC minus its fold SD above the test share of deaths, where the original used F2, with success meaning test F2 above the flag-everyone F2 on the training rows by more than its fold SD.
- The original analysis's decision tree, at threshold 0.2, had a test F2 of 0.6780.
- The rerun's logistic regression had a test PR-AUC of 0.6983, and a test F2 of 0.6400 at threshold 0.10.
- In nested cross-validation at their tuned thresholds, the mean F2 was 0.6943 for the tree and 0.7127 for the logistic regression.

Flagging every patient gives an F2 of 0.6985 on these test patients and 0.7038 on the 239 training patients.

### How it relates to smlbook.org

Table 2 counts the rules applied in each analysis's Decision Records by the tag each carries: the book's advice ([B]), a fact from the book turned into advice ([B→I]), or ours ([I]). Each row of a record's table of rules applied is counted once, under one tag, taking a rule not in the guide (UNLISTED) first, then [B→I], then [B], then [I]; records later superseded in full, and the diagnosis records, which have no such table, are not counted.

<small><b>Table 2.</b> Rules applied in the Decision Records in force, by provenance tag.</small>

| Analysis | Records in force (of all) | Rules applied | [B] | [B→I] | [I] | UNLISTED | No tag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | 15 (19) | 45 | 17 | 12 | 15 | 1 | 0 |
| Sepsis | 15 (20) | 52 | 31 | 11 | 7 | 3 | 0 |
| Mobile Price | 17 (21) | 50 | 23 | 5 | 18 | 1 | 3 |
| Heart Failure rerun | 16 (17) | 52 | 26 | 8 | 15 | 1 | 2 |
| All four | 63 | 199 | 97 | 36 | 55 | 6 | 5 |

The six UNLISTED rows are rules not in the guide, recorded as ours: in the original Heart Failure analysis, how the diagnosis judged whether the training error was above what the application needs, by comparing the training F2 with the flag-everyone reference; in Sepsis, the flag for survival analysis and the stratification of the test split and of the folds by hospital as well as outcome; in Mobile Price, the misclassification rate as the main metric for four classes, with the full confusion matrix reported; in the rerun, computing PR-AUC as average precision. The five untagged rows record that a rule had nothing to act on, such as no ranking entry applying or no hyperparameter to tune, or cite the working contract (`instructions.md`) rather than the guide.

Before cross-validation, each analysis recorded the order it expected the kept configurations to take; the outcome compares that expectation with the order cross-validation produced. Prior agreement records whether the configuration that won cross-validation, among those ranked before any model was fitted, was first in the ranking (agree), in its top two (partial), or neither (disagree). Grounding counts the ranking entries behind the recommended configuration's prior score, by tag.
- Heart Failure (original): expectation disagree, the decision tree, expected last, coming first; prior agreement disagree, the tree being third in the ranking; grounding one [B→I] entry, that an inspectable model was preferred.
- Sepsis: expectation partial, the two logistic configurations leading as expected but k-nearest neighbours above the decision tree, the reverse of the order expected; prior agreement agree; grounding two [B→I] entries, that an inspectable model was preferred and that class probabilities or a tuned threshold were needed.
- Mobile Price: expectation agree, the two logistic configurations leading; prior agreement disagree, logistic regression with L2 being third in a ranking in which no entry applied, so that every prior score was 0 and the order came from the number of add-ons alone; grounding none.
- Heart Failure rerun: expectation disagree, logistic regression with squares and cubes, expected last of the four logistic configurations, coming first; prior agreement partial, the winner being second in the ranking; grounding one [B→I] entry, that class probabilities or a tuned threshold were needed.

Of the five changes to the method listed under Methods, the original Heart Failure analysis ran under none. Sepsis ran under the first four, made while it was in progress, and its first diagnosis pass was re-run under the change to how underfitting is judged when one class is rare. Mobile Price ran under the first four from the start; the fifth was made after it finished, as a general rule in place of the reading of the guide agreed with the user at its recommendation step, and nothing was re-run. The Heart Failure rerun ran under all five.

### Training and validation methods

The training and test rows of each analysis, with the positives or the rows per class, are in the table under Methods. The spread of the deciding metric across the outer folds for each recommended configuration, and whether each analysis's own success criterion was met, are in Table 1. Mobile Price needed no decision threshold. For the other three analyses, Table 3 gives the threshold chosen on the training data, the nested cross-validation result at that threshold, and the test F2; for the two Heart Failure analyses it also gives the F2 of flagging every patient.

<small><b>Table 3.</b> Decision threshold, nested cross-validation at the tuned threshold, and F2 on the test data, with the F2 of flagging every patient.</small>

| Analysis | Threshold | Nested CV F2 (fold SD) | Nested CV precision (fold SD) | Nested CV recall (fold SD) | Test F2 | Flag everyone: F2 on the training rows | Flag everyone: F2 on the test rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | 0.2 | 0.6943 (0.0865) | not recorded | not recorded | 0.6780 | 0.7038 | 0.6985 |
| Sepsis | 0.040 | 0.2204 (0.0182) | 0.0723 (0.0050) | 0.4582 (0.0737) | 0.2326 | not reported | not reported |
| Heart Failure rerun | 0.10 | 0.7127 (0.0614) | 0.4012 (0.0553) | 0.8946 (0.1056) | 0.6400 | 0.7038 | 0.6985 |

## Discussion

*What the project achieved; what the findings mean taken together — the methods used and how they were chosen, how closely the work followed the book and what was added, and how the models were trained and validated; and what the work makes possible next.*

## Limitations

*What qualifies the findings: problems met, and what was not built or not tested.*

## Disclaimer

This report was written with the help of agentic AI: designing the workflow, writing the code, running the example analysis and drafting the text. Each part was directed and reviewed by the author.

## Appendix

*Pointers to the material behind this report: the working contract, the ML Guide, and the worked analyses.*

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published).
