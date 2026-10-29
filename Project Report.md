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

Much of the method is ours, and is marked as ours wherever it is used: the step-by-step workflow in which the user agrees each step before it is applied (`instructions.md`); the interim cores that compute the mechanical parts, so that the agent does not; the prior ranking of candidates before any model is fitted; the selection confidence reported with each recommendation; and the numerical thresholds that turn the book's advice into rules, such as treating two models as indistinguishable when their difference is less than half its variation across the folds. Every rule in Part II of the guide carries a tag saying whether it is the book's advice ([B]), a fact from the book that we turned into advice ([B→I]), or our own ([I]), and the Decision Records copy the tags of the rules they apply, so a reader can see how much of each choice rests on the book.

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

Where the user wanted a flag rather than only a probability, a decision threshold was chosen after the model, on the training data only. It was set to maximise F2, which counts recall twice as heavily as precision, the trade-off the user chose (Lindholm et al., 2026).

The chosen model was then refitted on all the training data and evaluated once on the test data, only after the user had approved it. The uncertainty reported with that result is the variation of the deciding metric across the ten outer folds. Each fold is smaller than the test set, so this approximates the uncertainty of the test result rather than measuring it; using it in this way is ours.

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

*The configuration recommended for each problem, its test result against the baseline with its uncertainty, how the other configurations ranked, and how confident the selection was.*

### How it relates to smlbook.org

*How much of each recommendation rested on the book's advice and how much on what was added, and whether cross-validation agreed with the ranking the book's guidance predicted.*

### Training and validation methods

*How many rows were used for training and testing, how much the results varied across cross-validation folds, and whether the success criterion was met in the single test evaluation.*

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
