# Training inputs (input design DR-13)

Rows: 24816. Goals: 2479. SHA-256 of inputs_train.csv: 0171d54ec6aa8330baca21f9a2edcb98dab403f82d71912e37dd5fe993f3708a

## Numeric inputs

|                 |   count |   mean |    std |   min |    25% |    50% |    75% |     max |
|:----------------|--------:|-------:|-------:|------:|-------:|-------:|-------:|--------:|
| distance        |   24816 | 19.904 |  8.247 | 1.14  | 13.515 | 19.582 | 25.826 |  66.218 |
| angle           |   24816 | 23.83  | 14.638 | 0     | 14.877 | 18.816 | 27.57  | 180     |
| opp_in_triangle |   24816 |  0.644 |  0.822 | 0     |  0     |  0     |  1     |   8     |
| gk_distance     |   24816 | 16.438 |  8.436 | 0.361 |  9.617 | 15.873 | 22.719 |  60.486 |

## Categorical inputs (levels)

- `body_part` (4): Right Foot 13787; Left Foot 8470; Head 2503; Other 56
- `technique` (7): Normal 18299; Half Volley 4115; Volley 1813; Lob 244; Overhead Kick 160; Backheel 95; Diving Header 90
- `play_pattern` (9): Regular Play 9920; From Throw In 5065; From Free Kick 3754; From Corner 2759; From Counter 1345; From Goal Kick 1120; From Keeper 493; From Kick Off 329; Other 31
- `key_pass_type` (4): Regular 16964; none 6765; Recovery 1049; Interception 38

## Boolean inputs (count of 1)

- `under_pressure`: 5981
- `first_time`: 8799
- `one_on_one`: 1320
- `open_goal`: 273
- `aerial_won`: 1178

Teams in training: 80

## Encoded inputs (one indicator per level) for Properties 2-4

- Sub-task 1: 13 columns (4 numeric, 4 categorical, 5 boolean) -> 33 encoded; ratio 24816 / (33 + 1) = 729.9; categorical share 9/13 = 69% (booleans counted as categorical)
- Sub-task 2: 14 columns (+ team) -> 113 encoded; ratio 24816 / (113 + 1) = 217.7; categorical share 10/14 = 71%
