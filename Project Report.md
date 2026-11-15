# [Title]

*Chosen by the user at the end of step 5, from the titles suggested once the `Discussion` is written.*

## Abstract

*Draft*

This analysis asks whether the fuel use of a new car, in litres per 100 km, can be predicted from its design, model year and country of origin. The data are 392 cars from model years 1970 to 1982 in the Auto MPG dataset of the UCI Machine Learning Repository, after six cars with no horsepower value were dropped. Cars with the same name are kept together when the data is split, and one in five cars is held back as a test set, used once at the end. The model learns from seven measurements of the car, used as recorded, with model year and number of cylinders as numbers and origin as a category. Three charts of the training cars show how the fuel figure is spread and how it is distributed against weight and origin code. A small set of methods from the book will be compared by cross-validation, and the chosen one judged against one error measure and against a baseline that predicts the average fuel use for every car.

## Introduction

A buyer or a car designer would like to know how much fuel a car will use before it is tested on the road. This analysis asks whether that can be predicted from the car's design, using the engine size, horsepower, weight, acceleration, number of cylinders, model year and country of origin recorded for cars from 1970 to 1982.

The figure predicted is the fuel used per 100 km, in litres, computed from the recorded miles per gallon on the assumption of US gallons. A prediction is judged by one error measure, the root mean squared error, which must be at most 1 litre per 100 km on held-out cars, and by whether it does clearly better than predicting the average fuel use of the training cars for every car.

The approach is to compare a small set of model types from the book, each judged by cross-validation on the training cars, in which the training cars are split into parts and each part is held back in turn to test a model fitted to the rest (Lindholm et al., 2026). The chosen model is then evaluated once on the held-out test cars.

The sub-tasks are:

1. Predict the fuel use, in litres per 100 km, of a new car from its design, model year and country of origin, against the success criterion above.


## Methods

### Data and evaluation

The data are the Auto MPG file of the UCI Machine Learning Repository (Quinlan, 1993), licensed under CC BY 4.0 and downloaded on 11 November 2026. The file holds 398 cars from model years 1970 to 1982. Six cars with no horsepower value were dropped, leaving 392 cars.

The predicted quantity is the fuel used per 100 km, in litres, computed as 235.2 divided by the recorded miles per gallon, on the assumption of US gallons. The seven inputs are engine displacement, horsepower, weight, acceleration, number of cylinders, model year and country of origin, in the units recorded in the file. Those units are not verified.

Cars with the same name are kept together, so that every row with one name lies on the same side of any split. One in five cars is held back as the test set: 78 cars, with 314 cars for training, split at random with seed 2026. The test set is not used until the final evaluation.

The single number that decides between models is the root mean squared error, in litres per 100 km. The mean absolute error, in the same units, is reported beside it but does not decide. The baseline is the average fuel use of the training cars, predicted for every car.

The success criterion has two parts, both checked on the test set. First, the root mean squared error is at most 1 litre per 100 km. Second, the method beats the baseline by a clear margin: the margin over the baseline is at least as large as one times its variation across the cross-validation folds of the training cars.

The charts of the training data use the 314 training cars only. The test cars are not read until the final evaluation. The chart of the fuel figure to be predicted is a histogram with bars one litre per 100 km wide, which shows how the figure is spread across the cars and does not relate it to the inputs.

## Results

### The training data

![[Code/outputs/Auto_MPG/fig1_fuel_histogram.png]]

<small><b>Figure 1.</b> Number of training cars in each band of fuel use, in litres per 100 km. Training cars only, 314 cars; the test cars are not shown.</small>

Each bar covers a band of one litre per 100 km. Its height is the number of training cars whose fuel use falls in that band. The chart shows how the figure to be predicted is spread across the cars, and nothing about its relation to the inputs.

![[Code/outputs/Auto_MPG/fig2_fuel_vs_weight.png]]

<small><b>Figure 2.</b> Fuel use against weight for the training cars, one dot per car. Training cars only, 314 cars; the test cars are not shown. Weight is in the units recorded in the file, which are not verified.</small>

Each dot is one training car: its weight across the bottom and its fuel use up the side. No line is drawn; the dots are shown as they are.

![[Code/outputs/Auto_MPG/fig3_fuel_by_origin.png]]

<small><b>Figure 3.</b> Fuel use by origin code, one dot per training car. Each column is one origin code, labelled with its number of training cars; the line marks the median of the column. The sideways spread of the dots within a column has no meaning. Training cars only; the test cars are not shown. The file does not name the countries behind the codes.</small>

Each dot is one training car, placed at its fuel use. The line in each column is the middle value of that column. The columns are of different sizes, as the labels show.

## Discussion

*Written in step 5, organised by theme: why the recommended configuration and not the others, how it makes predictions, what it can and cannot be used for, and the limits of the evaluation.*

## Disclaimer

This report was written with the help of agentic AI at every stage: importing and describing the data, cleaning it, framing the questions, choosing and fitting the models, producing the figures, and drafting the text. Each step was directed and reviewed by the author, who agreed every method before it was applied, and each number reported here comes from code that can be re-run. The record of what was done, including what was tried and abandoned, is in the appendix.

## Appendix

*A pointer to [Appendix.md](Appendix.md), where the data, the decisions and the full workings are recorded.*

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). *Machine Learning – A First Course for Engineers and Scientists*. 2nd edition, online draft version of 1 September 2026. [smlbook.org](https://smlbook.org/).
- Quinlan, R. (1993). Auto MPG [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5859H](https://doi.org/10.24432/C5859H).

