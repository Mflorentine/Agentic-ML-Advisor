# Predicting Car Fuel Use (L/100 km): Analysis Report

Dataset: auto-mpg.csv (398 cars, model years 1970–1982)

## Summary

I built a model that predicts a car's fuel consumption in litres per 100 km from its weight, engine size, power, age and origin. The best-performing models (gradient boosting and random forest) predict to within roughly 0.8–0.9 L/100 km on average on cars they had never seen, and explain about 90% of the variation in fuel use. A model that always guessed the average would be off by about 3.1 L/100 km. Weight and model year are the strongest drivers of fuel use.

## Data and preparation

The file has 398 rows and 9 columns: mpg, cylinders, displacement, horsepower, weight, acceleration, model year, origin (1 = USA, 2 = Europe, 3 = Japan) and car name.

- **Target.** The dataset records fuel economy in miles per US gallon. I converted it to the requested unit with L/100 km = 235.215 / mpg. This assumes US gallons, which is the convention for this well-known dataset. The converted target ranges from 5.1 to 26.1 L/100 km, with a mean of 11.2.
- **Missing values.** Six cars had a "?" for horsepower. I treated these as missing and filled them with the median inside the modelling pipeline, so no information leaks from the test data.
- **Features.** Cylinders, displacement, horsepower, weight, acceleration, model year (as a number) and origin (one-hot encoded). Car name was not used as a predictor.
- **Units.** Weight is in pounds and displacement in cubic inches, as in the source data. The model uses them as given, so new predictions must use the same units.

## What drives fuel use

Rank correlations (Spearman) with L/100 km:

| Feature | Correlation |
| --- | --- |
| Weight | +0.88 |
| Displacement | +0.86 |
| Horsepower | +0.85 |
| Cylinders | +0.82 |
| Acceleration time | −0.44 |
| Model year | −0.57 |
| Origin (higher code) | −0.58 |

Heavier, bigger-engined cars burn more fuel. Four-cylinder cars average 8.3 L/100 km, six-cylinder cars 12.1 and eight-cylinder cars 16.2. By origin, American cars average 12.9 L/100 km, European cars 8.9 and Japanese cars 8.1. Average consumption also fell over time, from about 14.6 L/100 km in 1970 to about 7.6 in 1982.

These features are strongly correlated with each other (heavy cars tend to have large engines and many cylinders), so individual effects are hard to separate and some of the origin effect simply reflects that American cars were bigger.

Working in L/100 km rather than mpg also helps the modelling: fuel use per distance is much closer to a straight-line function of weight than mpg is, which is why even simple linear models do well here.

## Modelling approach

I held out 20% of the data (77 cars) as a test set, splitting by car name so that the same model name never appears in both training and test data. This gives a more honest estimate than a purely random split, because many cars appear several times under the same name.

On the remaining 321 cars I compared five models with 5-fold cross-validation: a mean-only baseline, linear regression, ridge regression, random forest and gradient boosting. I then tuned gradient boosting with a small grid search (learning rate, tree depth, number of trees) and scored the finalists once on the held-out test set.

## Results

Cross-validation on the training data:

| Model | MAE (L/100 km) | RMSE (L/100 km) | R² |
| --- | --- | --- | --- |
| Baseline (mean) | 3.25 | 3.92 | −0.03 |
| Linear regression | 1.02 | 1.34 | 0.879 |
| Ridge | 1.01 | 1.34 | 0.879 |
| Random forest | 0.95 | 1.32 | 0.880 |
| Gradient boosting | 0.94 | 1.30 | 0.885 |

Held-out test set (77 cars):

| Model | MAE (L/100 km) | RMSE (L/100 km) | R² |
| --- | --- | --- | --- |
| Baseline (mean) | 3.15 | 3.74 | −0.01 |
| Ridge | 0.96 | 1.35 | 0.870 |
| Gradient boosting (tuned) | 0.86 | 1.20 | 0.897 |
| Random forest | 0.82 | 1.15 | 0.905 |

Gradient boosting and random forest are effectively tied. The test set is small, so the gap between them is within noise; gradient boosting was slightly ahead in cross-validation and random forest slightly ahead on the test set. I chose tuned gradient boosting as the final model. Its average error of 0.86 L/100 km is about 8% of the average fuel use, and 90% of its test predictions were within 1.6 L/100 km of the true value.

A useful reference point: a straight-line model using weight alone reaches R² of 0.76 and an average error of 1.5 L/100 km. The other features and non-linear modelling bring the error down by roughly 40%.

## Which features matter most

I measured permutation importance on the test set, meaning how much the error grows when one feature's values are shuffled:

1. Weight (largest effect by a wide margin)
2. Model year
3. Horsepower
4. Displacement
5. Acceleration
6. Origin and cylinders (almost no additional effect once the others are known)

Cylinders and origin rank low because their information is largely captured by weight, displacement and horsepower. That does not mean origin has no relationship with fuel use, only that it adds little once the other variables are known.

## Error analysis

- Errors are smaller for Japanese cars (average 0.45 L/100 km) than for European (0.78) or American cars (1.02). American cars span the widest range of sizes and engines, which makes them harder to predict.
- The model slightly under-predicts on the test set on average (bias of about +0.15 L/100 km, meaning actual consumption was a little higher than predicted), which is small relative to the typical error.

## Limitations

- **Age of the data.** These are cars from 1970–1982. Predictions for modern vehicles, including hybrids, turbochargers, direct injection and electric cars, would be unreliable. The model should not be used outside the range of weights, engine sizes and years it was trained on.
- **Small sample.** With 398 rows and a 77-car test set, performance estimates carry real uncertainty, and the ranking of the top two models is not conclusive.
- **Measurement basis.** The mpg values come from an older test procedure and may not match real-world consumption.
- **Unit assumption.** The conversion assumes US gallons.
- **Final model.** The saved model was refitted on all 398 cars after evaluation, so the figures above describe the training procedure, not an additional held-out check of the saved model.

## Possible next steps

- Add features such as fuel-injection type, transmission or body style if more data is available.
- Collect or merge more recent data if predictions for modern cars are needed.
- Report prediction intervals (for example with quantile regression) so users see the uncertainty alongside each estimate.

## Files

The code (fuel\_model.py) and the trained model (fuel\_model.joblib) were saved alongside this report. Inputs for a prediction are cylinders, displacement (cu in), horsepower, weight (lb), acceleration, model year (e.g. 1976) and origin (1, 2 or 3); the output is predicted L/100 km.
