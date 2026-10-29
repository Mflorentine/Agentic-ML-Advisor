# A step-by-step workflow for supervised machine learning with an AI agent, with every choice traced to a textbook

## Abstract

Supervised machine learning involves many choices besides fitting a model, and a reader can check them only if they are recorded as they are made. This project builds a step-by-step workflow, following the working practice of Lindholm et al. (2026), in which an AI agent proposes each step and writes all the code while the user takes every decision, and carries it through four classification analyses of three public datasets: death in heart failure, twice, the second time with the workflow as revised during the project; sepsis in intensive care; and the price band of mobile phones. The workflow chooses among the book's k-nearest neighbours, decision trees, and linear, logistic and generalised linear models, with polynomial terms and L2 regularisation, by removing configurations that cannot serve the problem, ranking the rest before any model is fitted, comparing them by nested cross-validation on the training data, and recommending the simplest whose score cannot be told apart from the best. The recommended model is evaluated once on held-out test data, with the spread of the metric across the outer cross-validation folds as its uncertainty. Every rule applied is tagged with its source: of the 199 rules applied, 97 were the book's advice, 36 were facts from the book turned into advice and 55 were our own. Logistic regression was recommended in three analyses and a decision tree in one. The selection confidence was Low in three, because the recommended model could not be told apart from the runner-up, and the ranking made before fitting placed the cross-validation winner first in one. Three analyses met their own success criteria, among them Sepsis (test PR-AUC 0.0847 against 0.0315 for flagging nobody) and Mobile Price (test accuracy 0.9600 against 0.2500); the original Heart Failure analysis did not (test F2 0.6780, where more than 0.7903 was required). On the same 60 Heart Failure test patients, the rerun met its criterion on PR-AUC (0.6983 against 0.3167), but at their tuned thresholds both models' F2 (0.6780 and 0.6400) was below that of flagging every patient (0.6985). The workflow was revised on the same analyses that test it, and only on categorical outputs, so how it performs on a new kind of problem has not been tested.

## Introduction

Fitting a model is the smaller part of supervised machine learning. The larger part is the set of choices around it: what exactly is predicted and from what, which metric decides between models, which baseline a model must beat, which data are held back for the final test, which model types are compared, and when to stop. Made after the results are seen, these choices can turn an evaluation into a description of whatever happened to work, and unless they are written down as they are made, a reader cannot check them. The question becomes sharper when an AI agent does much of the work: a reader then needs to see not only what was chosen, but who chose it and on what grounds.

Lindholm et al. (2026) set out a working practice for these choices: fix the problem, the metric, a baseline and the test data before any model is fitted; compare models by cross-validation on the training data; start simple and add complexity only when the errors call for it; and use the test data once, at the end. The book is openly available at smlbook.org, and its chapters 2, 3, 4 and 13 cover both the model types and this practice, so it gives a fixed reference against which each choice can be checked. Where the book gives advice, a choice can cite it; where it does not, the choice has to be marked as ours.

This project builds a step-by-step workflow for carrying a supervised learning problem from the data to a model evaluated once on held-out test data, following that practice. An AI agent proposes each step and writes and runs all the code; the user takes every decision that is theirs. The book's advice is distilled into a guide in which every rule is tagged as the book's advice, a fact from the book turned into advice, or our own, and the mechanical parts of the model choice are computed by code rather than judged by the agent. Every choice is written down as it is made, with the tags of the rules it applies, so that each can be traced to its source. The aim is not the best possible model for any one problem, but a record of how each model was chosen that a reader can check against the book.

The workflow was carried through four analyses of three public datasets:
1. Heart Failure: predicting death during follow-up for 299 heart failure patients from eleven routine clinical measurements (Chicco and Jurman, 2020; Heart Failure Clinical Records, 2020).
2. Sepsis: predicting, from a patient's first six hours in intensive care, whether the sepsis label switches on during hours 7 to 54, from a dataset of 40,336 intensive-care patients at two US hospitals, of whom the analysis used 39,088 (Reyna et al., 2019, 2020).
3. Mobile Price: predicting which of four price bands a mobile phone falls in from 20 of its specifications, for 2,000 phones (Sharma, 2018).
4. Heart Failure rerun: the first problem again, on the same data and the same test patients, with the workflow as it stood after the changes made while the other analyses were worked through.

## Methods

The method is described under three headings, which Results follows in the same order.

### The machine learning methods used

The workflow chooses among a fixed set of model types from chapters 2 and 3 of Lindholm et al. (2026): linear regression, logistic regression, Poisson and exponential generalised linear models, k-nearest neighbours and decision trees. Polynomial terms (squares and cubes of the numerical inputs) and L2 regularisation can be added to the regression models where the book allows them, which gives fourteen configurations in all. Methods from other chapters, such as ensembles or neural networks, are not used. Which inputs a model receives, and whether any is transformed, is agreed with the user beforehand and is not part of the comparison. The choice among the fourteen is then made in four steps, illustrated here by the four analyses: the original Heart Failure analysis, on the heart failure clinical records (Chicco and Jurman, 2020; Heart Failure Clinical Records, 2020); Sepsis, on the PhysioNet/Computing in Cardiology Challenge 2019 data (Reyna et al., 2019, 2020); Mobile Price, on the Mobile Price Classification data (Sharma, 2018); and the Heart Failure rerun, on the same heart failure data.

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

The chosen model was then refitted on all the training data and evaluated once on the test data, only after the user had approved it. The uncertainty reported with that result is the variation of the deciding metric across the ten outer folds. Each fold is smaller than the test set, so this approximates the uncertainty of the test result rather than measuring it; using it in this way is ours. Each analysis fixed its success criterion before any model was fitted: the test result had to exceed the baseline by more than this uncertainty, the baseline being flagging nobody in Sepsis and the rerun, the most common price band in Mobile Price, and, in the original Heart Failure analysis, the F2 of flagging every patient on the training rows. Table 1 sets out these choices for each analysis.

<small><b>Table 1.</b> Split, cross-validation folds, metric, decision threshold and uncertainty for each analysis.</small>

| Analysis | Split | Training / test rows (positives) | Folds stratified by | Metric for comparing and tuning | Decision threshold | Uncertainty of the test result |
| --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | new | 239 / 60 (77 / 19 deaths) | outcome | F2 | chosen to maximise F2 | fold variation of F2 at the tuned threshold |
| Sepsis | new, by patient | 31,270 / 7,818 (984 / 246 with sepsis) | outcome and hospital | PR-AUC | chosen to maximise F2 | fold variation of PR-AUC |
| Mobile Price | new | 1,600 / 400 (400 / 100 per price band) | price band | accuracy | none (not needed) | fold variation of accuracy |
| Heart Failure rerun | reused from the original | 239 / 60 (77 / 19 deaths) | outcome | PR-AUC | chosen to maximise F2 | fold variation of PR-AUC |

All four analyses used seed 2026 for the split and the folds. PR-AUC is the area under the precision–recall curve, computed as average precision.


## Results

Each sub-section reports what came out of the method described under the same heading in Methods.

### The machine learning methods used

Table 2 gives, for each analysis, the recommended configuration and its single evaluation on the test data, on the metric agreed for that problem, and whether that analysis's own success criterion was met. The uncertainty is the standard deviation of that metric across the ten outer cross-validation folds. The selection confidence is followed by its three factors: the margin over the runner-up (C1), the margin over the baseline (C2), and whether more training data was still lowering the validation error (C3).

<small><b>Table 2.</b> Recommended configuration and test result for each analysis.</small>

| Analysis | Recommended configuration | Deciding metric | Test result (fold SD) | Baseline | Test rows (positives) | Success criterion | Selection confidence (C1, C2, C3) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | decision tree, depth 3, minimum leaf size 20; threshold 0.2 | F2 | 0.6780 (0.0865) | 0.7038 (flag everyone, on the training rows; the agreed reference); the most common class scores 0 | 60 (19 deaths) | not met (required above 0.7038 + 0.0865 = 0.7903) | Low (none, clear, adequate) |
| Sepsis | logistic regression with L2, λ = 10⁻³; threshold 0.040 | PR-AUC | 0.0847 (0.0156) | 0.0315 (flag nobody, on the test data) | 7,818 (246 with sepsis) | met (required above 0.0315 + 0.0156 = 0.0471) | Low (none, clear, adequate) |
| Mobile Price | logistic regression with L2, λ = 10⁻⁵ | accuracy | 0.9600 (0.0141) | 0.2500 (most common band, on the test data) | 400 (100 per band) | met (0.9600 − 0.0141 = 0.9459, required above 0.2500) | High (clear, clear, adequate) |
| Heart Failure rerun | logistic regression; threshold 0.10 | PR-AUC | 0.6983 (0.0938) | 0.3167 (flag nobody, on the test data) | 60 (19 deaths) | met (0.6983 − 0.0938 = 0.6045, required above 0.3167) | Low (none, clear, adequate) |

#### Heart Failure (original): cross-validation

The mean F2 at threshold 0.5 was:
- flagging every patient 0.7032;
- decision tree 0.5567;
- logistic regression with squares and cubes 0.5286;
- logistic regression, with and without L2, 0.4798 each;
- the most common class 0.

A variant of the tree with a wider range of leaf sizes, added by the diagnosis, scored 0.5207. The tree's margin over the runner-up was 0.0281 (spread 0.1422), and its margin over the most common class 0.5567 (spread 0.1124).

#### Sepsis: cross-validation

The mean PR-AUC was:
- logistic regression with L2 0.0930;
- the same with squares and cubes 0.0907;
- k-nearest neighbours 0.0706;
- decision tree 0.0678;
- flagging nobody 0.0315.

The margin over the runner-up was 0.0023 (spread 0.0077), and over the baseline 0.0615 (spread 0.0156).

#### Mobile Price: cross-validation

The mean accuracy was:
- logistic regression with L2, with λ searched down to 10⁻⁸, 0.9706;
- the same with λ searched down to 10⁻⁴, 0.9637;
- with squares and cubes added, 0.9431;
- decision tree 0.8281;
- k-nearest neighbours 0.6250;
- the most common band 0.2500.

The margin over the runner-up was 0.0069 (spread 0.0055), and over the baseline 0.7206 (spread 0.0141).

#### Heart Failure rerun: cross-validation

The mean PR-AUC was:
- logistic regression with squares and cubes 0.7064;
- the same with L2 0.6882;
- logistic regression with L2 0.6703;
- logistic regression 0.6627;
- k-nearest neighbours 0.5633;
- decision tree 0.5546;
- flagging nobody 0.3221.

The recommended model's margin over the runner-up was −0.0437 (spread 0.1171), and over the baseline 0.3406 (spread 0.0892).

#### The two Heart Failure analyses on the same 60 test patients (19 deaths)

- The rerun used a different deciding metric and success criterion from the original: PR-AUC, with success meaning test PR-AUC minus its fold SD above the test share of deaths, where the original used F2, with success meaning test F2 above the flag-everyone F2 on the training rows by more than its fold SD.
- The original analysis's decision tree, at threshold 0.2, had a test F2 of 0.6780.
- The rerun's logistic regression had a test PR-AUC of 0.6983, and a test F2 of 0.6400 at threshold 0.10.
- In nested cross-validation at their tuned thresholds, the mean F2 was 0.6943 for the tree and 0.7127 for the logistic regression.

Flagging every patient gives an F2 of 0.6985 on these test patients and 0.7038 on the 239 training patients.

### How it relates to smlbook.org

Table 3 counts the rules applied in each analysis's Decision Records by the tag each carries: the book's advice ([B]), a fact from the book turned into advice ([B→I]), or ours ([I]). Each row of a record's table of rules applied is counted once, under one tag, taking a rule not in the guide (UNLISTED) first, then [B→I], then [B], then [I]; records later superseded in full, and the diagnosis records, which have no such table, are not counted.

<small><b>Table 3.</b> Rules applied in the Decision Records in force, by provenance tag.</small>

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

The training and test rows of each analysis, with the positives or the rows per class, are in Table 1. The spread of the deciding metric across the outer folds for each recommended configuration, and whether each analysis's own success criterion was met, are in Table 2. Mobile Price needed no decision threshold. For the other three analyses, Table 4 gives the threshold chosen on the training data, the nested cross-validation result at that threshold, and the test F2; for the two Heart Failure analyses it also gives the F2 of flagging every patient.

<small><b>Table 4.</b> Decision threshold, nested cross-validation at the tuned threshold, and F2 on the test data, with the F2 of flagging every patient.</small>

| Analysis | Threshold | Nested CV F2 (fold SD) | Nested CV precision (fold SD) | Nested CV recall (fold SD) | Test F2 | Flag everyone: F2 on the training rows | Flag everyone: F2 on the test rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | 0.2 | 0.6943 (0.0865) | not recorded | not recorded | 0.6780 | 0.7038 | 0.6985 |
| Sepsis | 0.040 | 0.2204 (0.0182) | 0.0723 (0.0050) | 0.4582 (0.0737) | 0.2326 | not reported | not reported |
| Heart Failure rerun | 0.10 | 0.7127 (0.0614) | 0.4012 (0.0553) | 0.8946 (0.1056) | 0.6400 | 0.7038 | 0.6985 |

## Discussion

The project carried one workflow through four analyses of three datasets: heart failure, twice, sepsis and mobile phone prices. Each analysis fixed its problem, metric, baseline and test data before any model was fitted, chose among the book's configurations by nested cross-validation, and evaluated the chosen model once on its test data. Every choice was written down as a Decision Record; the 63 records still in force hold 199 rules applied, each tagged with its source (Table 3). This shows that the procedure can be followed from the data to a recommendation and leaves a record a reader can check rule by rule. It does not show that the procedure works for every kind of problem. All four outputs were categories, so linear regression and the Poisson and exponential models were excluded every time, and the parts of the method for numerical outputs have not been exercised. The code that computed each analysis's mechanical steps was also written for that analysis alone, and its records label it as not reviewed.

Three of the four recommendations were logistic regression: plain in the Heart Failure rerun, and with L2 regularisation in Sepsis and Mobile Price. The fourth, in the original Heart Failure analysis, was a decision tree of depth 3. The selection confidence was High only in Mobile Price, where logistic regression with L2 led every other configuration by more than the variation of the difference across the folds. In the other three it was Low, each time for the same reason: the recommended model could not be told apart from the runner-up (C1 none), while it was clearly ahead of its baseline (C2 clear). In those three the data did not single out one configuration, and the choice among the leaders was made by the rule that prefers the simpler model; in the rerun that rule recommended plain logistic regression although logistic regression with squares and cubes had the higher cross-validated mean (0.7064 against 0.6627). A Low confidence therefore says that another configuration near the top would have served about as well, not that the recommended model fails to beat its baseline. That reading needs one qualification in the original Heart Failure analysis, where C2 was measured against the most common class, which scores an F2 of 0. Against flagging every patient, its agreed baseline, the tree's cross-validated F2 at threshold 0.5 (0.5567) was below (0.7032). Four analyses, all with categorical outputs, also do not show that logistic regression is generally the better choice.

The ranking made before any model was fitted placed the cross-validation winner first once in four analyses: prior agreement was agree in Sepsis, partial in the rerun, where the winner was second, and disagree in the original Heart Failure analysis and in Mobile Price. The entries behind the recommended configurations' prior scores were few (two in Sepsis, one in each Heart Failure analysis, none in Mobile Price), and all were facts from the book turned into advice ([B→I]) about wanting an inspectable model or needing class probabilities or a tuned threshold, not about predictive fit. In Mobile Price no entry applied at all, so the order came from the number of add-ons alone. The ranking therefore did what the method asks of it, deciding what was compared first while cross-validation decided what was chosen; predicting the cross-validation order is not what its entries were built to do, and in these analyses it mostly did not. The advisor's written expectation of the order behaved differently from the ranking: it agreed with cross-validation in Mobile Price, where the ranking disagreed, and disagreed in the rerun, where the ranking partly agreed. Four analyses are too few to say how often either would be right on another problem.

The two Heart Failure analyses were evaluated on the same 60 patients, 19 of whom died. The original analysis decided on F2 and did not meet its success criterion: its tree reached a test F2 of 0.6780, where the criterion required more than 0.7903. The rerun decided on PR-AUC and met its criterion: 0.6983 against 0.3167 for flagging nobody, and still above it after subtracting the fold spread. The two outcomes answer different questions. PR-AUC summarises how well a model ranks patients by risk across all thresholds (Lindholm et al., 2026), so the rerun's result shows that its logistic model orders these patients by risk better than chance. F2 at a threshold scores one rule for whom to flag. On that measure, at their tuned thresholds, both models were below flagging every patient on the test data: 0.6780 for the tree and 0.6400 for the logistic model, against 0.6985. In nested cross-validation the logistic model's F2 (0.7127) was above flagging every patient on the training rows (0.7038), and the tree's (0.6943) below it. The change of metric and criterion therefore explains why one analysis met its criterion and the other did not; it does not show that the rerun's model is a better rule for whom to flag, nor that the changes to the method improved the prediction. The figures come from 60 patients, and the fold spreads of F2 at the tuned threshold (0.0865 for the tree, 0.0614 for the logistic model) are larger than the differences between the two models' test F2 and between either and flagging every patient. The rerun also reused a test set whose result was already known, so its test result is a like-for-like comparison with the original rather than a fresh estimate of performance on new patients.

Of the 199 rules applied, 97 were the book's advice, 36 were facts from the book turned into advice and 55 were ours; six were rules not in the guide, and five carried no tag because they recorded that a rule had nothing to act on or cited the working contract (Table 3). The mix varied with the problem: Sepsis applied the most of the book's advice (31 of 52 rules), Mobile Price the most of ours (18 of 50). The method follows the book where a result is decided, in the held-out test data, the comparison by cross-validation and the start from simple models, and is ours mainly in how that practice is turned into rules and thresholds. The five changes made during the work kept that balance: two brought the diagnosis closer to the book, in how error is measured when one outcome is rare and in judging underfitting against what the application needs, and three filled gaps the four chapters leave. Some gaps showed up first as rules not in the guide: Sepsis stratified its folds by hospital before the guide allowed it, and a change on 27 October made that a rule. A further change on the same day altered how the work is done rather than what the method computes: the agent writes and runs all the code, and every decision that is the user's is put as two to four numbered options, each with its trade-off and book page. Mobile Price and the rerun were worked through under it from the start. Table 3 does not show it, since it counts the rules applied, not how decisions were put to the user. The tally also counts each rule once whatever its effect on the result, so it shows how the rules applied are sourced, not how much each source weighed in a recommendation.

The work points to three next steps. Each analysis wrote its own interim core, labelled in its records as not reviewed; the workflow foresees a single core in `Code/advisor/`, built once and reviewed, and running the four analyses through it and comparing with their recorded outputs would show whether it reproduces them. In both Heart Failure analyses the model's F2 at its threshold was compared with flagging every patient, which reaches a high F2 when about a third of patients die; only the original made it the baseline, and Sepsis, which also tuned a threshold, did not report it. Reporting the F2 of flagging every patient wherever a threshold is tuned for F2 would put that comparison in every such analysis; it would be a change to the method, made as the five above were. Finally, a problem with a numerical or count output would exercise the parts of the method these four analyses never reached.

## Limitations

Problems met:
- **The method changed while it was being applied.** Four of the five changes were made while Sepsis was in progress, three of them prompted by its data, and Sepsis re-ran a diagnosis pass under one of them; the fifth was made at the end of Mobile Price, prompted by its data. The first four were then used on Mobile Price, which had not prompted them, and all five on the Heart Failure rerun, whose data and earlier results the user and the advisor had already seen and whose test result was already known.
- **The data carry their own limits.** In Mobile Price, the origin of the rows and the rule that set the price bands are undocumented, so no claim about real phones or a real market rests on it. In Sepsis, the label is constructed by the data's publisher from the Sepsis-3 criteria and starts six hours before onset, and patients who left intensive care before the outcome could be observed count as negatives. In Heart Failure, a patient recorded as not having died was not observed to die during a follow-up of varying length, which is not the same as surviving.
- **The Heart Failure test set is small, and every uncertainty is approximate.** Heart Failure was tested on 60 patients, 19 of whom died. Every reported uncertainty is the spread across the outer cross-validation folds, which are smaller than the test sets, so it approximates the uncertainty of the test result rather than measuring it.

Not built or not tested:
- **The interim cores are not reviewed.** Each analysis wrote its own, and some of the readings of the guide built into them were not checked, such as how the L2 strength converts for four classes in Mobile Price.
- **Only categorical outputs were tested.** The configurations for numerical and count outputs were never fitted, so the rules that choose among them have not been tried on data.
- **Only four chapters of the book are used.** Methods from other chapters, such as ensembles and neural networks, and survival analysis, which the book does not cover, were left out or flagged and never fitted, so the project says nothing about how they would compare.
- **One person directed and reviewed the work.** The agent did the work and the author directed and reviewed each part; no independent review of the method, its changes or the code is recorded. The supervisor has not yet reviewed the method changes or the open questions.

## Disclaimer

This report was written with the help of agentic AI: designing the workflow, writing the code, running the four analyses and drafting the text. Each part was directed and reviewed by the author.

## Appendix

The material behind this report:
- The four analyses, each with a report and an appendix holding its data summary, problem definition, Decision Records, Recommendation Report, analysis log and code summary:
  - Heart Failure (original): [Demonstration/Heart Failure/](Demonstration/Heart%20Failure/Demonstration%20Report.md), as `Demonstration Report.md` and `Demonstration Appendix.md`;
  - Sepsis: [Demonstration/Sepsis/](Demonstration/Sepsis/Report.md);
  - Mobile Price: [Demonstration/Mobile Price/](Demonstration/Mobile%20Price/Report.md);
  - Heart Failure rerun: [Demonstration/Heart Failure rerun/](Demonstration/Heart%20Failure%20rerun/Report.md).
- [ML Guide.md](ML%20Guide.md): the guide the advisor follows. Part I summarises the four chapters with page references, Part II is the selection procedure with a provenance tag on every rule, and its version note records the five changes to the method.
- [instructions.md](instructions.md): the working contract for the step-by-step workflow.
- [Code/outputs/project/provenance_tally.md](Code/outputs/project/provenance_tally.md): the tally behind Table 3, produced by `Code/project_01_provenance_tally.py`.

## References

- Chicco, D. and Jurman, G. (2020). Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone. *BMC Medical Informatics and Decision Making*, 20, 16. [https://doi.org/10.1186/s12911-020-1023-5](https://doi.org/10.1186/s12911-020-1023-5).
- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R).
- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published).
- Reyna, M., Josef, C., Jeter, R., Shashikumar, S., Moody, B., Westover, M. B., Sharma, A., Nemati, S. and Clifford, G. D. (2019). *Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019* (version 1.0.0) [Dataset]. PhysioNet. [https://doi.org/10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857).
- Reyna, M. A., Josef, C. S., Jeter, R., Shashikumar, S. P., Westover, M. B., Nemati, S., Clifford, G. D. and Sharma, A. (2020). Early prediction of sepsis from clinical data: the PhysioNet/Computing in Cardiology Challenge 2019. *Critical Care Medicine*, 48(2), 210–217. [https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6964870/).
- Sharma, A. (2018). *Mobile Price Classification* [Dataset], version 1. Kaggle. [https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification).
