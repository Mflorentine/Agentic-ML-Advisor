# ML Guide

A working guide to choosing, training and evaluating a supervised machine learning model, distilled from four chapters of Lindholm, Wahlström, Lindsten and Schön, *Machine Learning – A First Course for Engineers and Scientists*, 2nd edition, online draft of 1 September 2026 (`sml-book-2nd-edition-draft-latest.pdf`, [smlbook.org](http://smlbook.org)). The chapters are 2 (supervised learning, k-NN, decision trees), 3 (linear and logistic regression, polynomial regression with L2 regularisation, generalised linear models), 4 (evaluating performance) and 13 (user aspects of machine learning).

This is a set of notes written in our own words, not a substitute for the book. Every entry gives the printed page number it rests on, so the claim can be checked. **Printed page = PDF page − 10** (chapter 2 starts on printed p. 15, PDF p. 25). Where a line is our own inference or practice rather than something the book says, it is marked *(not from the book)*.

The guide has two parts. **Part I (sections 1–6) is knowledge**: what the book says, with pages. **Part II (sections 7–23) is the advisor's reasoning procedure**: how that knowledge is turned into a recommendation, a ranking, a confidence level and a reasoning trace. Part II is our construction. Every rule in it carries a provenance tag (section 8), so a reader can see how much of any recommendation is the book's and how much is ours.

**Scope.** Only chapters 2, 3, 4 and 13. Every other method — L1/LASSO included — is flagged and not used (section 23).

# Part I — What the book says

## 1. Is this a supervised learning problem at all?

- **Supervised learning** means learning the relationship between inputs x and an output y from examples of both, so as to predict y for new inputs where only x is known (p. 15). Without a recorded or labelled output there is no supervised problem; a row with a missing output is of no use for supervised learning and is dropped (p. 345).
- **The book has two possible aims, and covers one.** A model can be built (i) to reason about how variables are connected — whether a relationship exists, as in medicine or sociology — or (ii) to predict y for new x. The first is the traditional focus of classical statistics; the book is about the second (p. 20). If the user's question is really of type (i), say so: it may be better served by a statistical analysis than by the workflow in this guide.
- **The data points are assumed independent.** The book considers only problems where the individual data points are (probabilistically) independent, which excludes time series analysis where consecutive observations are correlated (p. 16). Check for this before anything else. Two common breaches:
  - *Sequences.* A single series can be turned into a supervised problem by using a window of past values as the input and the next value as the output — "self-supervised" learning, giving e.g. an autoregressive tree (pp. 38–39). This is the only sequence handling in the chapters in scope.
  - *Groups.* Several rows may belong to the same unit (several X-ray images from one patient). A random split then puts the same unit in both training and validation data, and the measured performance is better than production will see — *group leakage*. The fix is to split by group, not by row (p. 329).

## 2. Defining the problem

The book's position is that the machine learning problem is defined by three things together: the validation data, the test data, and a single-number evaluation metric (pp. 327, 330).

- **Regression or classification** is decided by the output alone: numerical output → regression, categorical output → classification. The inputs can be of either type, and mixed, in both cases (p. 17). Classification with two classes is *binary*; more is *multiclass* (pp. 17–18).
- **Numerical or categorical** is partly a modelling decision. A numerical variable has a natural order; a categorical one does not and takes a finite set of values. Codes like 1 = Sweden, 2 = Denmark are categorical despite being numbers. Whether e.g. "number of children" is treated as numerical or as yes/no is the analyst's decision (pp. 16–17, Table 2.1).
- **Output types beyond these two.** If y is a count (0, 1, 2, … with no upper limit) or a non-negative real value, neither plain linear regression nor classification fits it well, and a generalised linear model is the in-scope choice (pp. 61–63; see 4.7).
- **Inputs are a design choice.** Summary features can work better than raw high-dimensional data; transforming an input (e.g. taking the logarithm of a length) can make values more homogeneous (p. 18).
- **One metric, agreed up front.** There is no single correct metric; choosing it is part of defining the problem. Agree one number to decide between models, and monitor others alongside it to see the trade-offs being made (p. 330).
- **The default error functions** are the misclassification rate for classification (accuracy = 1 − misclassification) and squared error for regression (p. 67). For imbalanced or asymmetric classification, see section 5.5.
- **Baseline.** Before modelling, fix a deliberately simple reference that the model must beat: the training-data mean for regression, the most common training class for classification, or a randomly drawn training output (pp. 330–331).
- **Achievable performance.** Where possible, also state the best level that can realistically be expected: the irreducible error (regression) or Bayes error rate (classification) in theory; in practice human-level performance or what comparable models achieve (p. 331). If the model is already close to it, further improvement may not be possible.

## 3. Splitting the data

- **Training, validation, test.** Training data fits the model; validation data (or k-fold cross-validation) compares models, chooses hyperparameters and selects features; test data evaluates the final model (p. 328).
- **The test data is used once**, after every model and hyperparameter choice has been made. Tuning against cross-validation makes the cross-validation error optimistic, which is why a separate test set is needed (p. 74). If decisions start being made on the test data, its result stops being an honest measure (p. 328). If validation performance is much better than test performance, the model has been overfitted to the validation data (p. 328).
- **Split randomly.** Shuffle before splitting; a dataset may arrive sorted, and an unshuffled split can put one class entirely in training and the other in validation (pp. 71, 73).
- **Split by group where rows share a unit** (p. 329), see section 1.
- **Validation and test data must look like production.** Both should come from the distribution the model will meet when used; otherwise the work optimises toward the wrong target (pp. 328–329). Training data can, with good reason, come from a slightly different distribution (pp. 329, 338).
- **Sizes depend on how much data there is.** With about 500 points, a 60/20/20 split leaves too little validation data to compare many models, and k-fold cross-validation on the non-test data is the better choice; a test set is still needed for a final estimate. With about a million points, 98/1/1 is reasonable and k-fold adds little (pp. 329–330).
- **Set the test set aside before any artificial enlargement** of the training data (duplication with noise, simulation, related datasets) (p. 74).
- **Fit preprocessing on training data only.** Scaling factors for normalisation are computed from training data and then applied to new data; normalising before setting test data aside gives a misleading estimate of future performance (p. 27). *(Not from the book: the same reasoning applies to any preprocessing that learns from the data, such as imputation values or category lists, and inside cross-validation it means refitting preprocessing within each fold.)*

## 4. The models in scope

All seven are from chapters 2 and 3. Each card says what the book says the model does, when it suits, what must be chosen, and what to watch for.

### 4.1 k-nearest neighbours (k-NN) — pp. 21–27

- **What it does.** Predicts from the k training points closest to the new input (Euclidean distance): their average for regression, a majority vote for classification (pp. 21–22). It is *nonparametric*: it keeps and uses the training data when predicting (p. 22).
- **Shape of the fit.** Predictions are piecewise constant, also for regression (p. 26). Decision boundaries are non-linear, so k-NN is a non-linear classifier (p. 24).
- **Hyperparameter: k.** k = 1 reproduces every training point and overfits to noise; very large k averages everything away and in the limit predicts the overall mean. There is no general best k; choose it by cross-validation (pp. 24–26).
- **Preprocessing: normalise the inputs — this is crucial.** Distances are otherwise dominated by whichever input has the largest range. Use min–max scaling (eq. 2.1) or standardisation (eq. 2.2), with the factors computed on training data only (pp. 26–27). Categorical inputs need encoding (p. 49).
- **Watch for.** Poor behaviour at the edge of the data: near the largest input values the k nearest neighbours stop changing and the prediction cannot follow a trend (p. 26, the stopping-distance example).
- **Suits** problems where nearby inputs should give similar outputs and the relationship is not expected to be linear. It is one of the book's suggested "simple first" models (p. 331).

### 4.2 Decision trees (classification and regression trees) — pp. 27–38

- **What it does.** Splits the input space into axis-aligned boxes by a sequence of yes/no rules on one input at a time, and predicts a constant in each box: the average output for regression, the majority class for classification (pp. 27–29, 31).
- **How it is learned.** By recursive binary splitting: greedy, one split at a time, each split chosen to minimise squared error (regression) or a class-impurity criterion (classification) (pp. 30–33). Finding the optimal tree is computationally infeasible, which is why the greedy method is used (p. 30).
- **Classification splitting criterion.** Misclassification rate, Gini index or entropy (eq. 2.7). Gini and entropy favour pure nodes, which suits the greedy procedure and can mean fewer splits in total (pp. 33, 35–36).
- **Hyperparameters: tree size.** A fully grown tree fits the training data exactly and overfits, like 1-NN (pp. 31, 38). Control size with a maximum depth, a minimum number of training points per leaf, or a number of regions (p. 31); choose by cross-validation (Ch. 4). Pruning exists but is not covered (p. 38).
- **Preprocessing.** Not stated as required by the book. *(Not from the book: because each split compares one input with a threshold, trees are unaffected by rescaling of the inputs.)*
- **Trust.** Trees can be inspected by a person, and the leaves of a regression tree give the range within which every prediction will lie — a form of worst-case statement more complex models cannot offer (p. 347).
- **Suits** non-linear relationships, interactions between inputs, and cases where an explainable set of rules is valued.

### 4.3 Linear regression — pp. 41–49

- **What it does.** Models the output as an intercept plus a weighted sum of the inputs plus noise (eq. 3.2). The noise is assumed to have mean zero and to be independent of x (pp. 41–42). It is *parametric*: once learned, only the parameters are needed (p. 41).
- **How it is learned.** By least squares, which has a closed-form solution (the normal equations, eq. 3.13–3.14) (pp. 45–46). Least squares is the same as maximum likelihood under an assumption of independent Gaussian noise (pp. 47–48).
- **Not local.** Unlike k-NN and trees, every training point influences every prediction (p. 47).
- **When least squares has no unique solution.** The normal equations give a unique solution only if XᵀX is invertible; otherwise there are no or infinitely many equally good solutions (pp. 46–47, Time to reflect 3.1; p. 65). *(Not from the book: this happens when there are at least as many parameters as data points, or when inputs are exact linear combinations of each other — e.g. a full set of one-hot columns plus an intercept. L2 regularisation (4.6) removes the problem, since its closed form always has a unique solution for λ > 0.)*
- **Categorical inputs.** Use a 0/1 dummy for two categories, one-hot encoding for more (pp. 49). This applies to any method, not only linear regression (p. 49).
- **Suits** regression where the relationship is roughly linear in the inputs (or can be made so with transformed inputs, 4.5), and a simple model is wanted first (p. 331). The fitted coefficients can be inspected (p. 347).

### 4.4 Logistic regression (binary and multiclass) — pp. 49–58

- **What it does.** Despite the name, a classifier. Passes a linear combination of the inputs through the logistic function to give a probability of the positive class (eq. 3.29) (pp. 51–52); for more than two classes uses the softmax function to give a probability for each class (eq. 3.41–3.43) (pp. 56–57).
- **How it is learned.** By maximum likelihood (minimising the cross-entropy / logistic loss); there is no closed form, so it is solved numerically (pp. 52–53).
- **Decision threshold.** Turning a probability into a class needs a threshold r. r = 0.5 minimises the misclassification rate if the model's probabilities are correct, but for asymmetric or imbalanced problems another threshold may be better, and the choice is the user's (pp. 53–54; example on pp. 92–93).
- **Decision boundary is linear** (a hyperplane), so logistic regression is a *linear classifier*; k-NN and trees are non-linear (p. 55).
- **It returns probabilities,** not only classes, which is useful when the strength of the prediction matters (p. 50).
- **Use with L2 regularisation in practice** — see 4.6: it is common practice, and without it training diverges when the classes can be separated perfectly by a straight boundary (p. 61).
- **Suits** classification where a linear boundary is plausible, class probabilities are wanted, and interpretability matters (pp. 50, 347).

### 4.5 Polynomial regression — pp. 58–60

- **What it does.** Adds powers of an input (x², x³, …) as extra inputs to linear regression; the same can be done inside logistic regression (p. 59). It is still a linear model in its parameters, with a "lifted" input (p. 59). The book describes this for a one-dimensional input raised to different powers (p. 59). *(Not from the book: with several inputs, Part II uses powers of each input separately and no product terms such as x₁x₂, unless the user asks for them — see section 9.)*
- **Risk.** Each power adds a parameter, so a high degree overfits easily: a 10th-order polynomial on the stopping-distance data does worse than a straight line (pp. 59–60).
- **Controls.** Choose which transformed inputs to include (forward selection, backward elimination) and compare by cross-validation, or use regularisation (p. 60).
- **Suits** a curved relationship in a few inputs where a plain line underfits.

### 4.6 L2 regularisation: ridge regression and regularised logistic regression — pp. 60–61

- **What it does.** Adds a penalty λ‖θ‖² to the cost so the parameters stay small unless the data clearly calls for large ones (p. 60). For linear regression this is *ridge regression*, which still has a closed form (eq. 3.49) (p. 61); for logistic regression see eq. 3.50 (p. 61).
- **Hyperparameter: λ.** λ = 0 is no regularisation; very large λ forces all parameters to zero. Choose λ by cross-validation (p. 60). More regularisation means more bias and less variance (pp. 85–86).
- **Practical notes.** It can be wise to leave the intercept out of the penalty (p. 60, footnote). *(Not from the book: because the penalty acts on parameter sizes, inputs on very different scales are penalised unevenly, so standardise the inputs before using it.)*
- **In-scope regularisation is L2 only.** L1 (LASSO), which drives some parameters exactly to zero and so selects features, is described in section 5.3 and mentioned on p. 346, which are outside the chapters in scope. **LASSO is out of scope (decided 10 October 2026)**: if feature selection is needed, use the in-scope routes — forward selection or backward elimination compared by cross-validation (p. 60), or dropping features (p. 346) — and flag LASSO as the out-of-scope alternative.

### 4.7 Generalised linear models (GLMs) — pp. 61–64

- **What it does.** Generalises linear regression to outputs with other properties by choosing (i) a distribution for the output from the exponential family, (ii) a linear term θᵀx, and (iii) a link function connecting the linear term to the mean of the output (p. 63). Logistic regression is one example (p. 63).
- **Poisson regression** is the worked example: for count outputs, the mean count is exp(θᵀx), which keeps it positive (Example 3.6, pp. 62–63).
- **Other members named:** negative binomial regression (a more flexible model for counts) and exponential regression (for non-negative real outputs) (p. 63). *Negative binomial is documented but not implemented in this workspace (decided 10 October 2026): scikit-learn has no implementation and statsmodels has not been added. If counts look more variable than a Poisson model allows, flag it (section 23).*
- **How it is learned.** By maximum likelihood, numerically; regularisation can be added (pp. 63–64).
- **Suits** counts (number of events in an interval) and other outputs that are restricted in ways a normal linear model ignores, e.g. non-negative values (pp. 61–62).

## 5. Evaluating a model (chapter 4)

### 5.1 What we are trying to estimate

- **E_new**, the expected error on new data from the same distribution, is the quantity that matters: how the model will perform in production (pp. 68–69). It cannot be computed, only estimated (p. 69).
- **E_new belongs to one trained model on one problem.** There is no "E_new of logistic regression" in general (p. 69).
- **The training error E_train is not an estimate of E_new.** The same data was used to fit the model, and typically E_train < E_new (p. 70).

### 5.2 How to estimate it

- **Hold-out validation.** Train on part of the data, compute the error on the rest. Unbiased; less variable the larger the hold-out set, but the larger it is the less is left for training (pp. 70–71). Enough when data is plentiful (p. 71).
- **k-fold cross-validation.** Split into k batches, train k times each time holding one batch out, and average the k errors; then retrain on all the data. Not exactly unbiased, but usually good enough for large enough k (pp. 72–73). k = n is leave-one-out; k = 10 is a realistic choice when training is expensive (p. 73).
- **Uses.** Judging whether performance is good enough, choosing between methods, choosing hyperparameters, and reporting expected performance (p. 69).
- **Then a test set, once** (p. 74; section 3 above).
- **Selecting on validation is optimistic.** After many models have been compared on the same validation data, the winner may simply have done well on that data by chance; the test set exists to detect this (p. 328). The more candidates and hyperparameter values compared, the larger the risk.
- *(Not from the book: the chapters in scope give no method for an interval around a test-set error. **Open decision — method not yet chosen.** The variability of a hold-out estimate shrinks with its size (p. 71), but turning that into an interval needs a method the book introduces only later — the bootstrap, Chapter 8 — or a standard binomial interval for an error rate.)*

### 5.3 Underfitting, overfitting and the generalisation gap

- **Decomposition.** E_new = E_train + generalisation gap (p. 75). The more a model adapts to the training data, the larger the gap (p. 75).
- **The U-shape.** As model complexity grows, E_train falls while E_new first falls then rises. Too little complexity underfits, too much overfits; the minimum is a balanced fit, which is what tuning hyperparameters by cross-validation searches for (pp. 76–77, Fig. 4.3).
- **More data** usually shrinks the gap (p. 78).
- **Two rules of thumb** (p. 79):
  - validation error ≈ training error (small gap, possibly underfitting) → increase flexibility: less regularisation, more parameters;
  - training error near zero but validation error not → probably overfitting: more regularisation, lower polynomial order, etc.
- **If E_train is already far above the required error**, cross-validation will not rescue the model; rethink the problem and method (p. 78).
- **Complexity is not one dial.** When comparing different methods, one can have a smaller gap at the same training error; some methods simply suit some data better (*inductive bias*). Good practice is to choose models known to suit the type of data, draw on experience with similar problems, and compare by cross-validation (p. 79).

### 5.4 Bias and variance

- **Decomposition.** For regression with squared error, E_new = bias² + variance + irreducible error (eq. 4.19, p. 84). Bias: how far the average learned model is from the truth; variance: how much the learned model changes between training sets; irreducible error: noise no model can predict (p. 84).
- **High complexity → low bias, high variance; low complexity → high bias, low variance** (p. 84). Variance shrinks as the training set grows; bias roughly does not (p. 85).
- **Practical link** (rough): generalisation gap ≈ variance, and training error ≈ bias² + noise (eq. 4.23, p. 87).
- Regularisation trades variance for bias (Example 4.3, pp. 85–86).

### 5.5 Classification metrics beyond accuracy (binary) — pp. 89–93

*The book presents these for binary problems. (Not from the book: for multiclass problems, use the misclassification rate as the primary metric unless the user's error costs say otherwise, report the full confusion matrix, and if precision/recall are needed compute them one class against the rest and average, stating which averaging was used.)*

- **Confusion matrix:** true/false positives and negatives; by convention the positive class (y = 1) means presence of the thing detected (p. 89).
- **Recall** (sensitivity, true positive rate) = TP / all actual positives; low recall means false negatives. **Precision** (positive predictive value) = TP / all predicted positives; low precision means false positives (p. 90, Table 4.1).
- **ROC curve and ROC-AUC:** recall against false-positive rate over all thresholds; AUC 1 is perfect, 0.5 is random guessing (p. 90).
- **Imbalanced** (one class dominates) and **asymmetric** (one error type costs more) problems need more than the misclassification rate: a classifier that always predicts the majority class can score well on it (p. 91).
  - **F1** (harmonic mean of precision and recall) is often preferred as the single summary for imbalanced problems; it is only high if both are (pp. 91–92).
  - **F_β** weights recall β times as heavily as precision, for asymmetric problems (p. 92).
  - **Precision–recall curve and PR-AUC** are more informative than ROC for imbalanced problems; a random classifier gives a horizontal line at the positive proportion P/n (p. 92).
  - **The threshold** can be moved to trade false negatives against false positives; which trade-off is right depends on the consequences of each error, which is a judgement for the user (pp. 92–93).

## 6. Working practice (chapter 13)

### 6.1 Start simple

- Begin with a basic model such as k-NN or linear/logistic regression; do not add regularisation to the very first model; keep preprocessing to the minimum; optionally start on a subset of the data. Build the evaluation code at the same time (pp. 331–332).
- Starting simple reveals problem-formulation issues early and reduces the risk of ending with a complicated model where a simple one would have done (p. 332).

### 6.2 Check the code is doing what it should

- **Compare with the baseline.** Failing to beat it suggests a bug in training or evaluation (p. 332).
- **Overfit a tiny subset.** On a very small subset (even two points) the model should reach the best possible training performance (p. 332).

### 6.3 Decide the next improvement from the errors

- **Training error vs generalisation gap** (pp. 332–335, Fig. 13.2):
  - high training error (underfitting) → a more flexible model, more input variables, less regularisation (pp. 333–334);
  - high gap (overfitting) → a less flexible model, more regularisation, more training data (p. 333);
  - if the training error is much larger than the gap, more data will most likely not help; if the gap is much larger than the training error, a more flexible model will most likely not help (p. 334).
- **Learning curves.** Train on increasing fractions of the training data (10 %, 20 %, …) and plot training and validation error; extrapolating shows whether collecting more data is likely to pay off (pp. 334–336, Fig. 13.3).
- **Error analysis.** Look by hand at a sample (say 100) of validation points the model gets wrong and group the causes; each group's share is an upper bound on the improvement from fixing it (pp. 336–337). The same works for regression (p. 336).
- **Mislabelled data.** Correct labels in validation and test data first — it gives a fairer estimate — and in training data only if it is worth the effort (p. 337). If labellers disagree, check inter-rater reliability (p. 338).
- **Training data from a slightly different distribution.** Carve a "training-validation" set out of the training data to measure how much of the validation error comes from the mismatch (pp. 338–339).

### 6.4 When more data cannot be collected — pp. 339–343

- **Extra data from a slightly different source.** Keep validation and test data from the data the model must work on; put the other source only into training (Option 3), or do not use it (Option 1). Shuffling both together into all three sets (Option 2) is not recommended (pp. 340–341).
- **Data augmentation** (creating new points by transformations that do not change the label) is mainly an image technique and requires understanding which transformations are valid (p. 341).
- Transfer learning, semi-supervised and proxy-task learning (pp. 341–343) rely on neural networks or generative models outside the chapters in scope.

### 6.5 Practical data issues — pp. 343–346

- **Outliers.** First ask whether they are something the model should predict or noise. If noise, go back to the data provider; then remove them or use a learning method robust to them (the robust losses are in Chapter 5, out of scope). If they are of interest, a more flexible model is needed, with care not to overfit; if they turn out to be a rare class, the problem is an imbalanced one (pp. 343–344).
- **Missing data** (pp. 345–346):
  - First find out why values are missing, and whether they can be recovered from the source (p. 345).
  - Rows with a missing output are dropped (p. 345).
  - Dropping rows with missing inputs is simplest and works if enough data remains — but if values are missing systematically (e.g. more often for one class), dropping them creates a mismatch with reality (p. 345).
  - Dropping a column that is often missing is another option (p. 345).
  - Imputing (e.g. the mean or median of the column, or within the class) builds in assumptions that may not hold; poor imputation can perform worse than dropping (p. 345).
  - Methods that handle missingness directly rely on strong assumptions such as "missing completely at random", rarely met in practice (p. 346).
  - Note that missing values are sometimes coded as 0 rather than as empty (p. 345).
- **Feature selection** (p. 346): removing a feature is a form of regularisation. Cross-validation can tell whether including a feature helps. Low correlation with the output hints a feature may be useless, but looking at one feature at a time can mislead; highly correlated pairs of features may be redundant and add variance.

### 6.6 Can the model be trusted? — p. 347

- Machine learning is designed to predict, not to explain. The simpler models of chapters 2–3 can, to a degree, be inspected and their reasoning explained to a non-expert; complex models are much harder (p. 347).
- E_new is a statistical, average-case claim that holds only if the evaluation data resembles what the model will meet. It says nothing about how wrong the worst individual predictions can be (p. 347).
- Logistic regression and trees can be inspected to reason about the worst case — e.g. a regression tree's leaves bound every possible prediction (p. 347).
- The model should eventually be evaluated in production too; if it does systematically worse there than on the test data, find out why (p. 329).



# Part II — How the advisor reasons

The architecture is fixed: **admissibility → prior ranking → cross-validation → diagnosis loop → recommendation**. Sections 7–9 set the principle, the tags and the solution space. Sections 10–15 produce the prior ranking. Sections 16–19 decide. Sections 20–23 explain and bound the result.

## 7. The governing principle

**Rules propose, cross-validation decides, and the trace explains.** The book says that when choosing between methods, one method can simply suit a problem better than another, and that in a real problem — unlike a simulation — this cannot be seen directly. Good practice is to pick models known to work for the type of data, draw on experience with similar problems, and compare by cross-validation `[B p.79]`. In three tiers:

1. **Constraints decide what is admissible.** The admissibility checks (section 10), the task gates (section 12) and requirements the user states as must-haves.
2. **Cross-validation decides among admissible configurations that can be told apart** (sections 16–17).
3. **Simplicity decides among configurations that cannot be told apart.** The book favours not ending with a complicated model where a simple one would have done `[B p.332]` (section 19).

The prior ranking (section 15) does not decide anything. It chooses what is worth trying, records what the advisor expects, and makes that expectation checkable against the cross-validation result.

**The recommendation is computed, not argued.** It follows mechanically from the CV table and the rule in section 19. The agent writes the reasoning afterwards. It never explains away a CV result that contradicts its prior: a contradiction is recorded as a finding.

**Who does what (decided 10 October 2026).** The mechanical parts are computed by reference code that the agent calls — the deterministic core, in `Code/advisor/` (not yet implemented) — and the agent does not compute them itself.

| Reference code (the deterministic core) | The agent |
| --- | --- |
| Admissible set from the gates and modifiers (§12), given the property values | Eliciting the property values and must-haves from the user and the data (§11), with the evidence for each |
| Matrix score and prior ranking (§13, §15) | Answering the admissibility questions with the user (§10) |
| Nested cross-validation and the CV table (§16) | Writing the expectation before CV, and comparing it with the result |
| Selection confidence C1–C3 (§17) | Reading the diagnosis observations and choosing the action (§18), including the steps that need the user (DX-7, DX-8) |
| The recommendation rule (§19) | Recording flags (§20); writing every Decision Record and the Recommendation Report; explaining the model (§21) |

The agent passes inputs to the reference code and copies its outputs into the Decision Records unchanged, together with the code version. If the agent disagrees with an output, it says so in the record and raises it with the user. It never substitutes its own result.

## 8. Provenance tags and rule kinds

**Provenance tags.** Every rule, matrix entry and threshold carries one:

| Tag | Meaning | Example |
| --- | --- | --- |
| `[B p.x]` | **Explicit book advice**: the book tells the reader what to do | "Do not add add-ons like regularisation for the first model" (p. 331) |
| `[B→I p.x]` | **Book fact, our interpretation into advice**: the book states a property of a method; turning it into "prefer it when…" is ours | The book says logistic regression has a linear decision boundary (p. 55); "disfavour it when the user expects an irregular boundary" is ours |
| `[I]` | **Our inference**, practice or threshold, not in the four chapters | "k-NN is disfavoured with more than 20 inputs" |

Tags are shown wherever a rule is used, including in every Decision Record. They do not change a rule's weight (section 15); they are reported so that the share of a recommendation resting on each kind can be seen (section 17).

**Evidence tags.** Every property value carries one:
- `M` — from metadata or the user's statement; allowed from step 2.
- `T` — computed from the training data; allowed from step 3.
- `CV` — from cross-validation; step 4.
- `TEST` — only in the single final evaluation.

**Rule kinds.** Only suitability is scored.

| Kind | What it does | Where |
| --- | --- | --- |
| **Admissibility** | Stops, redirects or asks before modelling | Section 10 |
| **Gate** | Decides which families are admissible for the task, and applies must-have user requirements | Section 12 |
| **Compulsory modifier** | Forces an add-on (L2) when a model would otherwise be ill-posed | Section 12 |
| **Required practice** | Must be done whenever a configuration is used | Section 12 |
| **Suitability** | +1 / 0 / −1 entries in the family × property matrix; summed into the prior score | Section 13 |
| **Sequencing** | Says in what order things are tried; never a score | Section 14 |

## 9. The solution space

A **configuration** is a model family × an input-transformation type × a regularisation type. Hyperparameters (k, tree size, degree, λ, decision threshold) are not part of a configuration's identity. They are tuned inside it by cross-validation (section 16).

| Axis | Options | Notes |
| --- | --- | --- |
| **Family** | Linear regression · Logistic regression · Poisson GLM · Exponential GLM · k-NN · Decision tree | Linear and logistic regression are themselves GLMs (p. 63); "GLM" here means Poisson and exponential. Negative binomial: documented, not implemented (section 23). |
| **Polynomial terms** | none · `poly` | Powers of each numerical input separately, degree 2 or 3, no product terms `[I]`; the book describes powers of a single input (p. 59). Parametric families only. |
| **Regularisation** | none · `L2` | Parametric families only (pp. 60–61, 63–64). For k-NN and trees, flexibility is set by k and tree size, tuned by CV (pp. 24–26, 31). |
| **Input design** | Domain transformations (e.g. a logarithm of an input) and the choice of inputs | Allowed for every family (p. 18). Not a configuration axis: decided with the user in steps 2–3 and recorded in a Decision Record. |

**Valid configurations** (14 structural configurations, plus the baseline):

| Family | Valid configurations |
| --- | --- |
| Linear | `Linear` · `Linear + L2` · `Linear + poly` · `Linear + poly + L2` |
| Logistic | `Logistic` · `Logistic + L2` · `Logistic + poly` · `Logistic + poly + L2` |
| Poisson GLM | `Poisson` · `Poisson + L2` |
| Exponential GLM | `Exponential` · `Exponential + L2` |
| k-NN | `kNN` |
| Decision tree | `Tree` |

*(GLMs without polynomial terms `[I]`: excluded to keep the solution space manageable (decided 10 October 2026); to be revisited only if the evaluation shows a need.)*

**Implementation notes for scikit-learn `[I]`.** Several defaults differ from the book's starting points and must be set explicitly:

| Concern | scikit-learn default | Required setting |
| --- | --- | --- |
| Unregularised logistic regression | `LogisticRegression` is L2-regularised (C = 1.0) | Regularisation switched off explicitly for `Logistic` and `Logistic + poly` |
| Tree size | `DecisionTree*` grows fully | Size always tuned (section 16); a fully grown tree is never reported |
| k | `KNeighbors*` uses k = 5 | k always tuned |
| Polynomial terms | `PolynomialFeatures` adds all products of inputs | Powers of each input separately (custom transformer) |
| Exponential GLM | no estimator by that name | `GammaRegressor` (log link) estimates the same mean model `[I]` |
| λ scaling | `Ridge` minimises ‖y − Xθ‖² + α‖θ‖² | Report both α and the book's λ. **Open implementation note:** verify the exact conversion against eq. 3.48–3.49 in the PDF when implementing Ridge (decided 10 October 2026). |
| Preprocessing | — | Inside a `Pipeline`, so scaling and encoding are refitted in every fold (p. 27) |

## 10. Admissibility

Each check is a fixed question with closed answers. It is asked in step 1 or 2 and recorded in a Decision Record. Only ADM-1 is a gate.

| ID | Question | Answers → action | Basis |
| --- | --- | --- | --- |
| ADM-1 | Is there a recorded output y for the rows to be learned from? | no → stop: not a supervised problem | `[B p.15]` |
| ADM-2 | Is the main aim to predict y for new cases, or to understand how the variables are connected? | predict → continue · understand → tell the user that this workflow optimises prediction and does not establish how variables are connected; continue only if they confirm. The book says the distinction "is not a clear-cut" one, so this is a question, not a gate. | `[B p.20]` |
| ADM-3 | Do several rows belong to the same unit, or are rows ordered in time? | none → random split · group column *X* → split and cross-validate by group · time column *Y* → autoregressive reformulation if the user wants it, otherwise flag time-series modelling as out of scope | `[B pp.16, 38–39, 329]` |
| ADM-4 | Will the cases the model is used on look like the data we have? | yes → continue · no or unsure → agree with the user which data validation and test sets should come from before splitting | `[B pp.328–329]` |

Whether an out-of-scope method is needed is not decided here. It is decided from evidence, in the diagnosis loop (DX-10), and recorded as a flag (section 20).

## 11. Property dictionary

The prior ranking uses only these properties. Each has a fixed set of values, a decider, an evidence tag and an operational definition. A property whose value is not known is recorded as `unknown` and contributes nothing.

| ID | Property | Values | Decided by | Evidence | Operational definition |
| --- | --- | --- | --- | --- | --- |
| P1 | Output type | numeric · count · non-negative real · binary · multiclass · ordinal | user, checked against data | M | Count = non-negative integers with no fixed upper limit (pp. 61–62). Non-negative real = continuous, never below 0. Ordinal → see section 12. |
| P2 | Data-to-parameter ratio | ample · limited | computed | M | n_train ÷ (number of input columns after one-hot encoding + 1). Limited if < 10 `[I]`. |
| P3 | Number of inputs | few · many | computed | M | Input columns after encoding. Many if > 20 `[I]`. |
| P4 | Share of categorical inputs | low · high | computed | M | Share of original input columns that are categorical. High if ≥ 50 % `[I]`. |
| P5 | Interpretability needed | none · inspectable · worst-case bound | user | M | Inspectable = a person must be able to follow how predictions are made. Worst-case bound = a limit on how wrong any prediction can be (p. 347). |
| P6 | Probabilities or a tuned threshold needed | yes · no | user | M | The user needs class probabilities, or will choose a trade-off between error types (pp. 50, 53–54, 92–93). |
| P7 | Predictions beyond the training range | yes · no | user | M | The model will be used on input values outside the range seen in training. |
| P8 | Expected shape | linear · curved · interactions/irregular · unknown | **user or domain expectation only** | M | Never inferred from the data before fitting (decided 10 October 2026). Default `unknown`. Recorded with the user's words quoted. |
| P9 | Classes perfectly separable | yes · no | computed | T | Classification only. Yes if logistic regression with negligible regularisation reaches 100 % training accuracy `[I]`. |
| P10 | Class imbalance | balanced · imbalanced | computed | T | Classification only. Imbalanced if the smallest class is < 20 % of training rows `[I]`. Changes the metric and threshold handling (§5.5, p. 91), not the family. |

## 12. Gates, compulsory modifiers and required practice

**Task gate (from P1).**

| P1 | Admissible families | Basis |
| --- | --- | --- |
| numeric | Linear, k-NN, Tree | `[B p.17]` |
| count | Poisson, Linear, k-NN, Tree | `[B pp.17, 61–63]` |
| non-negative real | Exponential, Linear, k-NN, Tree | `[B pp.17, 63]` |
| binary, multiclass | Logistic, k-NN, Tree | `[B pp.17, 49–57]` |
| ordinal | Ask the user whether to treat it as multiclass or as numeric; record the choice `[I]` | Ordinal outputs are not covered in ch. 2–4 |

**Must-have requirements.** If the user says a requirement is a must-have, it becomes a gate. Families that cannot meet it get why-not code `USER`.

| Must-have | Families that meet it | Basis |
| --- | --- | --- |
| P5 = inspectable | Linear, Logistic, Poisson, Exponential, Tree; k-NN only if "showing the most similar past cases" is acceptable to the user | `[B→I p.347]` (the book: models from ch. 2–3 can "to some degree" be inspected) |
| P5 = worst-case bound | Tree (regression: every prediction lies within the leaf range); Logistic | `[B→I p.347]` (the book's examples) |
| P6 = yes | Logistic | `[B→I pp.50, 53–54]` |

**Compulsory modifiers.**

| ID | Condition | Effect | Basis |
| --- | --- | --- | --- |
| MOD-1 | P9 = yes | `Logistic` and `Logistic + poly` are inadmissible; only the `+ L2` versions remain | `[B p.61]` — without regularisation the optimal parameters are not finite for separable data, and it is common practice to train with L2 |
| MOD-2 | Parameters ≥ n_train, or exactly collinear inputs | Linear and GLM configurations without L2 are inadmissible | `[B→I pp.46–47, 65]` — the least-squares solution is not unique when XᵀX is not invertible; that L2 fixes this is our reading of eq. 3.49 |

**Required practice** (whenever the configuration is used):

| ID | Practice | Basis |
| --- | --- | --- |
| REQ-1 | Fit all preprocessing on training data only, refitted inside each CV fold | `[B p.27]` + `[I]` for the CV extension |
| REQ-2 | Normalise inputs for k-NN | `[B pp.26–27]` |
| REQ-3 | Standardise inputs before L2 | `[I]` |
| REQ-4 | Tune k, tree size, degree and λ by CV | `[B pp.24–26, 31, 60]` |
| REQ-5 | Leave the intercept out of the L2 penalty | `[B p.60]` |
| REQ-6 | One-hot encode categorical inputs | `[B p.49]` |

## 13. Suitability matrix (family × property)

The only scored rules. Each cell is +1, −1 or blank (0), with its tag. A property contributes at most one entry to each column, so no family gains points from having more rules written about it.

A configuration's score is the sum of its **family column** plus the **`+ poly` column** if it has polynomial terms, plus the **`+ L2` column** if it has L2, over all properties whose value is known.

| Property value | Linear | Logistic | GLM | k-NN | Tree | + poly | + L2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 = count or non-negative real | −1 `[B p.62]` | | +1 `[B pp.61–62]` | | | | |
| P2 = limited | | | | | −1 `[I]` | −1 `[B→I pp.59–60]` | +1 `[B→I p.60]` |
| P3 = many | | | | −1 `[I]` | | −1 `[B→I p.59]` | |
| P4 = high | | | | −1 `[I]` | | | |
| P5 = inspectable (not a must-have) | +1 `[B→I p.347]` | +1 `[B→I p.347]` | +1 `[B→I p.347]` | | +1 `[B→I p.347]` | −1 `[I]` | |
| P5 = worst-case bound (not a must-have) | | +1 `[B→I p.347]` | | | +1 `[B→I p.347]` | | |
| P6 = yes (not a must-have) | | +1 `[B→I pp.50, 53–54]` | | | | | |
| P7 = yes | | | | −1 `[B→I p.26]` | −1 `[I]` | | |
| P8 = linear | +1 `[B→I p.41]` | +1 `[B→I p.55]` | +1 `[B→I p.63]` | | | | |
| P8 = curved | −1 `[B→I pp.58–59]` | | | +1 `[B→I p.26]` | | +1 `[B→I p.59]` | |
| P8 = interactions/irregular | −1 `[B→I p.41]` | −1 `[B→I p.55]` | −1 `[B→I p.63]` | +1 `[B→I p.24]` | +1 `[B→I pp.27–29]` | | |

**Reading the entries.**
- **P1** is the only row resting on explicit book advice: count data "is not well described by a linear regression model", and a distribution with support matching the data should be chosen (pp. 61–62).
- **P2:** high-degree polynomials overfit easily (pp. 59–60) and regularisation counters overfitting (p. 60). Trees are marked down because a deep tree overfits `[I]`.
- **P8 rows** apply only when the user or domain states the expectation. The family's entry follows from what the book says it can represent: a straight line, a linear boundary, a piecewise-constant fit (pp. 24, 26, 41, 55).
- **P10 has no row.** Imbalance changes the metric and threshold (§5.5), not the family.

## 14. Sequencing rules (never scored)

| ID | Rule | Basis |
| --- | --- | --- |
| SEQ-1 | Always include the baseline: mean of training outputs (regression) or most common training class (classification). | `[B pp.330–331]` |
| SEQ-2 | Always include one simple-first configuration with no add-ons: the plain parametric model for the task (`Linear`, `Logistic`, `Poisson` or `Exponential`), or its `+ L2` version if MOD-1 or MOD-2 applies. | `[B p.331]`; GLMs as simple-first are `[I]` |
| SEQ-3 | Cross-validate the baseline and the simple-first configuration first. Continue to the other configurations only once the simple-first configuration beats the baseline (DX-1 otherwise). | `[B pp.331–332]` |

SEQ-3 is how "add-ons come later" (p. 331) is honoured. The basic pipeline is shown to work before configurations with add-ons are compared.

## 15. Prior ranking

1. **Admissible set:** the valid configurations (section 9) that pass the gates and compulsory modifiers (section 12). Every configuration removed gets a why-not code.
2. **Score:** sum the matrix entries (section 13) for each admissible configuration. Every entry is +1 or −1 whatever its tag. Unknown properties contribute nothing.
3. **Order:** highest score first. Ties are broken by fewer add-ons. Configurations still tied share a rank, and no family is ranked above another by default.
4. **Keep:** the baseline, the simple-first configuration (SEQ-2) and the three highest-ranked others. If there is a tie at third place, keep every tied configuration. Every configuration not kept gets `DISF`.
5. **Record:** the prior is written as a Decision Record before any training, including the advisor's expectation of the CV order.

**Expected behaviour.** When P8 is unknown, which is the default, most configurations within a task score alike, and the prior is driven by P1, P2, P3 and the user's requirements. This is intended. The prior encodes what the advisor can know before fitting, and nothing more.

## 16. Cross-validation protocol (fixed)

| Item | Setting | Basis |
| --- | --- | --- |
| Outer CV (comparison) | 10-fold, shuffled, seed recorded; the same folds for every configuration | `[B pp.72–73]` (k = 10 realistic) |
| Classification | Stratified folds | `[I]` |
| Grouped rows (ADM-3) | Group folds | `[B p.329]` |
| Hyperparameter tuning | Inner 5-fold grid search within each outer training fold | `[I]`; tuning on the comparison folds would make them optimistic (p. 74). Nested CV kept despite its cost (decided 10 October 2026). |
| Grids | k ∈ {1, 3, 5, 7, 9, 15, 21, 31, 51} (below the inner training size); tree max depth ∈ {1, 2, 3, 4, 5, 6, 8, 10, 15, 20} × minimum leaf size ∈ {1, 5, 10, 20}; degree ∈ {2, 3}; λ ∈ {10⁻⁴, 10⁻³, …, 10⁴} | `[I]` |
| Selection metric | The single metric agreed in step 2 | `[B p.330]` |
| Direction | All margins expressed so that positive = better | `[I]` |
| Margin | For configurations A and B: the mean over the 10 outer folds of (A's fold score − B's fold score) | `[I]` |
| Spread | The standard deviation (not the standard error) of those 10 fold differences. The fold estimates are not independent, because the training sets overlap; using the SD rather than the SE is deliberately cautious. | `[I]` |
| Diagnosis errors | E_train and E_val computed with the book's default error function (misclassification rate or squared error, p. 67), whatever the selection metric | `[I]` |
| Learning curve | For the leading configuration only: training fractions 10 %, 20 %, …, 100 % on the outer folds | `[B pp.334–336]` |
| Decision threshold | Default 0.5 (p. 53). Tuned only if P6 = yes, after model selection, by CV on training data, with the trade-off chosen by the user. | `[B→I pp.53–54, 92–93]` |

## 17. Confidence

**Selection confidence** — how sure we are of the choice. It is computed by code from the CV table, never judged by the agent. No probabilities are given.

| Factor | Levels | Definition |
| --- | --- | --- |
| C1 Margin over the runner-up | clear · moderate · none | margin ≥ 1 × spread → clear; 0.5–1 × → moderate; < 0.5 × → none `[I]` |
| C2 Margin over the baseline | clear · not clear | margin ≥ 1 × spread → clear `[I]` |
| C3 Data adequacy | adequate · limited | Limited if the learning-curve validation error at 100 % is lower than at 80 % by at least 0.5 × its fold SD, i.e. still falling `[B→I pp.334–336]` + `[I]` threshold |

| Level | Rule `[I]` |
| --- | --- |
| **High** | C1 = clear, C2 = clear and C3 = adequate |
| **Low** | C1 = none, or C2 = not clear |
| **Medium** | Everything else |

**Reported alongside, not combined into the level:**
- **Prior agreement:** agree (CV winner = prior first), partial (in the prior's top two), disagree. Configurations added in the diagnosis loop are excluded.
- **Grounding:** for the recommended configuration, the number of matrix entries behind its prior score by tag (`[B]`, `[B→I]`, `[I]`).
- **Selection breadth note:** if more than 10 configurations were compared, including those added in the loop, state that the winner's CV score may be optimistic because many were compared on the same data (p. 328) `[I]` threshold.

## 18. Diagnosis and improvement policy (chapter 13)

The loop runs on cross-validation only and ends before the test set is used. Hyperparameters are already tuned inside each configuration, so the loop acts on **configurations, inputs and data**, not on k, λ or depth directly.

**Observations**, computed for the leading configuration using E_train, E_val and gap = E_val − E_train (section 16):

| ID | Observation | Test |
| --- | --- | --- |
| O1 | Doesn't beat the baseline | C2 = not clear |
| O2 | Training error already above what the application needs | E_train worse than the success criterion, when the criterion is in the same units |
| O3 | Overfitting | gap ≥ 2 × E_train `[B→I p.334]` + `[I]` ratio |
| O4 | Underfitting | E_train ≥ 2 × gap `[B→I p.334]` + `[I]` ratio |
| O5 | Tuned hyperparameter at the edge of its grid | the selected value is the smallest or largest in the grid in most outer folds `[I]` |
| O6 | More data likely to help | C3 = limited |

**Actions.** One per pass, taken from the first observation that holds, in the order O1 > O2 > O5 > O3 > O4 > O6:

| ID | Trigger | Action | Basis |
| --- | --- | --- | --- |
| DX-1 | O1 | Sanity checks: overfit a tiny subset; check the evaluation code; then revisit the formulation with the user | `[B p.332]` |
| DX-2 | O2 | Stop and rethink the problem and method with the user | `[B p.78]` |
| DX-3 | O5 | Extend the grid in that direction and rerun | `[I]` |
| DX-4 | O3 | Less flexibility: add L2 to a parametric configuration without it; remove polynomial terms; feature selection by backward elimination compared by CV; ask whether more data is available | `[B pp.60, 333, 346]` |
| DX-5 | O4 | More flexibility: add polynomial terms (if P3 = few); add k-NN or Tree if not already compared; ask whether more input variables exist | `[B pp.333–334]` |
| DX-6 | O6 | Tell the user more data is likely to help | `[B pp.334–336]` |
| DX-7 | Criterion not met and none of O1–O6 holds | Error analysis with the user: show a sample (up to 100) of validation errors; the user groups the causes; the largest group is addressed first | `[B pp.336–337]` |
| DX-8 | The user or the error analysis finds wrong labels | Correct validation and test labels first, training labels if worth it — the user decides | `[B pp.337–338]` |
| DX-9 | — | **Don't** suggest more data when E_train ≫ gap; **don't** add flexibility when gap ≫ E_train | `[B p.334]` |
| DX-10 | The only remaining action is out of scope | Flag it (section 20) | Scope decision |

Configurations added by the loop are marked **post-prior** in the CV table. They count towards the selection breadth note but not towards prior agreement.

**Stopping rules.** Record which one applies:
- S1: the success criterion is met.
- S2: the result is at the achievable level `[B p.331]`.
- S3: two consecutive passes give no gain of at least 0.5 × spread `[I]`.
- S4: the next action is out of scope (DX-10).
- S5: the user stops it.
- S6: five passes reached `[I]`.

## 19. Recommendation rule (mechanical)

1. **Eligible:** configurations with C2 = clear that meet every must-have. If none is eligible, there is no recommendation: report this with DX-1 or DX-2.
2. **Candidates:** the eligible configuration with the best CV mean, plus any eligible configuration whose margin to it is "none" (< 0.5 × spread).
3. **Choose:** among the candidates, the one with the fewest add-ons (p. 332). If still tied, the higher prior score. If still tied, the better CV mean.
4. **Test once:** evaluate the chosen configuration on the test set (pp. 74, 328), refitted on all training data with its tuned hyperparameters.

## 20. Why-not codes and flags

Every structural configuration in section 9 that is not recommended gets exactly one code: the first that applies, in this priority order.

| Priority | Code | Meaning | Evidence required |
| --- | --- | --- | --- |
| 1 | `EXCL` | Fails the task gate or a compulsory modifier | Gate or MOD ID |
| 2 | `USER` | Fails a must-have requirement | The requirement, quoted |
| 3 | `DISF` | Admissible, not kept after the prior ranking | Its score and the matrix entries behind it |
| 4 | `BASE` | Kept, but did not clearly beat the baseline (C2) | Margin and spread vs baseline |
| 5 | `OUTP` | Kept, clearly outperformed by the recommendation | Margin and spread |
| 6 | `SIMP` | Could not be told apart from the recommendation; the simpler one was chosen | Margin (< 0.5 × spread) and add-on counts |

**Flags** are recorded separately, not as codes: methods outside the solution space that the evidence suggests might help, each with the reason and its chapter (section 23). A flag says a method *might* help. It never claims it would have done better, because that was not tested.

## 21. Explanation guidance

The recommendation explains how the chosen configuration makes predictions, at the depth the user's experience calls for. Machine learning is designed to deliver predictions rather than explain them, and only simpler models allow explanation to some degree `[B p.347]`.

| Family | What to show | What it can and cannot say | Basis |
| --- | --- | --- | --- |
| Linear | Coefficients in the units of the inputs, noting which were standardised | The change in prediction per unit change of an input, with the others fixed; not a causal effect; with L2, coefficients are shrunk | `[B→I p.347]` + `[I]` |
| Logistic | Coefficients on the log-odds scale; the threshold and why it was chosen | Direction and relative size of each input's effect on the probability; not causal | `[B→I pp.53–54, 347]` + `[I]` |
| Poisson / Exponential | Coefficients through the log link: multiplicative effects on the mean | As for linear, on the multiplicative scale | `[B→I p.63]` + `[I]` |
| Tree | The tree or its top levels; each leaf's range | The rules followed for any prediction; for regression, an interval containing every prediction | `[B p.347]` |
| k-NN | For a given prediction, the k neighbours used | "These past cases were the most similar"; no global summary | `[I]` |
| `+ poly` | Prediction curves over each input's range | Individual polynomial coefficients are hard to read on their own | `[I]` |

Every explanation states the trust limits: E_new is an average over data like the evaluation data; it says nothing about the worst individual prediction; and it holds only while production data resembles that data `[B pp.329, 347]`.

## 22. Decision tree

```
USER PROBLEM (own words) + ML experience level
│
├─ ADMISSIBILITY (section 10; closed questions, step 1–2)
│   ADM-1 output y recorded? ──────── no → STOP: not supervised (p.15)
│   ADM-2 aim: predict or understand? ─ understand → explain limits; continue only if user confirms (p.20)
│   ADM-3 groups / time order? ─────── group col → group split + group CV (p.329)
│                                      time col → autoregressive reformulation or FLAG (pp.16, 38–39)
│   ADM-4 future cases like our data? ─ no/unsure → agree val/test source with user (pp.328–329)
│
├─ FORMULATION (step 2, metadata only)
│   P1 output type → task gate (section 12) · metric · success criterion · baseline · achievable level
│   must-haves (P5, P6) · expectations (P7, P8 — user/domain only)
│   split fixed, seed recorded → TEST SET LOCKED
│
├─ PROPERTIES (section 11)   P2–P4 computed (M) · P9–P10 computed on training data (T)
│
├─ ADMISSIBLE SET   14 configurations → task gate → must-haves (USER) → MOD-1/MOD-2 (EXCL)
│
├─ PRIOR RANKING (sections 13, 15)   matrix score → tie-break by add-ons
│   keep: baseline + simple-first + top 3 (+ ties) · DISF for the rest · expectation recorded
│
├─ CROSS-VALIDATION (section 16; nested, same outer folds)
│   SEQ-3: baseline + simple-first first ── simple-first not beating baseline → DX-1
│   then remaining kept configurations
│
├─ DIAGNOSIS LOOP (section 18)   O1 > O2 > O5 > O3 > O4 > O6 → one action per pass
│   new configurations marked post-prior → back to CROSS-VALIDATION
│   stop at S1–S6
│
└─ RECOMMENDATION (sections 17, 19)
    eligible (beats baseline, meets must-haves) → best CV → within-noise → fewest add-ons
    single test-set evaluation · selection confidence (C1–C3) · prior agreement · grounding
    why-not per configuration (section 20) · flags · explanation + trust limits (section 21)
```

## 23. Outside the solution space — flag, do not use

If the evidence suggests one of these might help, record a flag (section 20) naming the method and the chapter, and don't apply it.

| Method | Status |
| --- | --- |
| Negative binomial GLM | In ch. 3 (p. 63), **documented but not implemented** (no scikit-learn implementation; statsmodels not added) |
| L1 regularisation (LASSO), robust loss functions, hyperparameter optimisation beyond grid search | Chapter 5 |
| Neural networks, deep learning | Chapters 6–7 |
| Bagging, random forests, boosting; the bootstrap | Chapter 8 |
| Kernel methods, support vector machines | Chapter 9 |
| Bayesian methods, Gaussian processes | Chapter 10 |
| Generative models, semi-supervised learning, clustering | Chapter 11 |
| Representation learning, PCA | Chapter 12 |
| Transfer learning, foundation models | Sections 13.3, 13.6 |
| Time-series models | Not covered; the book assumes independent data points (p. 16) |
| Ordinal regression | Not covered in ch. 2–4 |

## Appendix to Part II — thresholds to validate

Every number below is ours (`[I]`). Each is reported in the Decision Record wherever it is applied (under *Thresholds applied*). Each is validated in the evaluation phase against two alternative values, listed in the advisor evaluation framework (planned as `Evaluation/README.md`, section 7; not yet in the workspace) (decided 10 October 2026).

| Where | Threshold | Value |
| --- | --- | --- |
| P2 | Limited data-to-parameter ratio | < 10 |
| P3 | Many inputs | > 20 |
| P4 | High categorical share | ≥ 50 % |
| P9 | Separability test | 100 % training accuracy with negligible regularisation |
| P10 | Imbalance | smallest class < 20 % |
| §15 | Number kept besides baseline and simple-first | 3 (plus ties) |
| §16 | Outer / inner folds; grids | 10 / 5; as listed |
| C1 | Clear / moderate / none | ≥ 1 / 0.5–1 / < 0.5 × spread |
| C2 | Clear over baseline | ≥ 1 × spread |
| C3 | Learning curve still falling | 100 % vs 80 % difference ≥ 0.5 × fold SD |
| Breadth note | Many configurations compared | > 10 |
| §19 | Within-noise margin (same cut-off as C1 = none) | < 0.5 × spread |
| O3 / O4 | Overfitting / underfitting ratios | gap ≥ 2 × E_train / E_train ≥ 2 × gap |
| O5 | Grid edge | most outer folds |
| S3 / S6 | No-gain passes / maximum passes | 2 / 5 |
