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

*Which chapters of the book you drew on and how it followed the book's advice. What else is added*

### Training and validation methods 

*How the data is split, how candidate configurations are compared by cross-validation, and how the chosen one is evaluated once on held-out test data.*


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
