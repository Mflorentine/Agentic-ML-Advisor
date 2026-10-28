# Describing pass: Mobile Price `train.csv` and `test.csv`

## Files

| File | Rows | Columns | Bytes | SHA-256 | Matches SOURCE.md | CRLF | ASCII only | Missing cells |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `train.csv` | 2000 | 21 | 122,403 | `f9e8cd3154b8684a1be0ff401b1fba7750710af6bd076a399c6ce7ceb979c624` | True | False | True | 0 |
| `test.csv` | 1000 | 21 | 63,850 | `e929f5999ffeedec84abf53cc8d35faa1bbd7e8ebd61826881aa62562d37adce` | True | True | True | 0 |

## `train.csv`

Duplicate rows: 0. Rows with identical inputs: 0. Input patterns with conflicting targets: 0. Rows sorted by `price_range`: False; longest run of one class: 6.

Class counts of `price_range`: 0: 500 (25.0%), 1: 500 (25.0%), 2: 500 (25.0%), 3: 500 (25.0%).

Inputs: 20, of which 6 are 0/1 (`blue`, `dual_sim`, `four_g`, `three_g`, `touch_screen`, `wifi`).

| Column | Meaning (Kaggle) | Unit (Kaggle) | Type | Missing | Distinct | Min | 1st pct | Median | 99th pct | Max | Zeros | Non-integer | 0 / 1 counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `battery_power` | Total energy a battery can store in one time measured in mAh | mAh | int64 | 0 | 1094 | 501 | 510 | 1226 | 1987 | 1998 | 0 | 0 | — |
| `blue` | Has bluetooth or not | 0/1 | int64 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | 1010 | 0 | 1010 / 990 |
| `clock_speed` | speed at which microprocessor executes instructions | not stated | float64 | 0 | 26 | 0.5 | 0.5 | 1.5 | 3 | 3 | 0 | 1844 | — |
| `dual_sim` | Has dual sim support or not | 0/1 | int64 | 0 | 2 | 0 | 0 | 1 | 1 | 1 | 981 | 0 | 981 / 1019 |
| `fc` | Front Camera mega pixels | megapixels | int64 | 0 | 20 | 0 | 0 | 3 | 16 | 19 | 474 | 0 | — |
| `four_g` | Has 4G or not | 0/1 | int64 | 0 | 2 | 0 | 0 | 1 | 1 | 1 | 957 | 0 | 957 / 1043 |
| `int_memory` | Internal Memory in Gigabytes | GB | int64 | 0 | 63 | 2 | 2 | 32 | 64 | 64 | 0 | 0 | — |
| `m_dep` | Mobile Depth in cm | cm | float64 | 0 | 10 | 0.1 | 0.1 | 0.5 | 1 | 1 | 0 | 1894 | — |
| `mobile_wt` | Weight of mobile phone | not stated | int64 | 0 | 121 | 80 | 80 | 141 | 199 | 200 | 0 | 0 | — |
| `n_cores` | Number of cores of processor | count | int64 | 0 | 8 | 1 | 1 | 4 | 8 | 8 | 0 | 0 | — |
| `pc` | Primary Camera mega pixels | megapixels | int64 | 0 | 21 | 0 | 0 | 10 | 20 | 20 | 101 | 0 | — |
| `px_height` | Pixel Resolution Height | pixels (not stated; implied by 'Pixel Resolution') | int64 | 0 | 1137 | 0 | 15 | 564 | 1791.01 | 1960 | 2 | 0 | — |
| `px_width` | Pixel Resolution Width | pixels (not stated; implied by 'Pixel Resolution') | int64 | 0 | 1109 | 500 | 512.99 | 1247 | 1987 | 1998 | 0 | 0 | — |
| `ram` | Random Access Memory in Mega Bytes | MB | int64 | 0 | 1562 | 256 | 296.99 | 2146.5 | 3958.01 | 3998 | 0 | 0 | — |
| `sc_h` | Screen Height of mobile in cm | cm | int64 | 0 | 15 | 5 | 5 | 12 | 19 | 19 | 0 | 0 | — |
| `sc_w` | Screen Width of mobile in cm | cm | int64 | 0 | 19 | 0 | 0 | 5 | 17 | 18 | 180 | 0 | — |
| `talk_time` | longest time that a single battery charge will last when you are | not stated | int64 | 0 | 19 | 2 | 2 | 11 | 20 | 20 | 0 | 0 | — |
| `three_g` | Has 3G or not | 0/1 | int64 | 0 | 2 | 0 | 0 | 1 | 1 | 1 | 477 | 0 | 477 / 1523 |
| `touch_screen` | Has touch screen or not | 0/1 | int64 | 0 | 2 | 0 | 0 | 1 | 1 | 1 | 994 | 0 | 994 / 1006 |
| `wifi` | Has wifi or not | 0/1 | int64 | 0 | 2 | 0 | 0 | 1 | 1 | 1 | 986 | 0 | 986 / 1014 |
| `price_range` | This is the target variable with value of 0(low cost), 1(medium cost), 2(high cost) and 3(very high cost). | class 0-3 | int64 | 0 | 4 | 0 | 0 | 1.5 | 3 | 3 | 500 | 0 | — |

Value combinations counted (not judged): `px_height_lt_100` = 150; `px_height_eq_0` = 2; `sc_w_eq_0` = 180; `sc_w_gt_sc_h` = 0; `px_height_gt_px_width` = 0; `fc_gt_pc` = 0; `four_g_1_and_three_g_0` = 0; `m_dep_values` = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]; `n_cores_values` = [1, 2, 3, 4, 5, 6, 7, 8]; `clock_speed_values_count` = 26.

## `test.csv`

Has `price_range`: False. `id` runs 1 to 1000: True. Rows with identical inputs: 0. Rows whose 20 inputs also appear in `train.csv`: 0.

Rows with an input outside the `train.csv` range: `battery_power` 3, `blue` 0, `clock_speed` 0, `dual_sim` 0, `fc` 0, `four_g` 0, `int_memory` 0, `m_dep` 0, `mobile_wt` 0, `n_cores` 0, `pc` 0, `px_height` 0, `px_width` 0, `ram` 0, `sc_h` 0, `sc_w` 0, `talk_time` 0, `three_g` 0, `touch_screen` 0, `wifi` 0.

| Column | Type | Missing | Distinct | Min | Median | Max | Zeros | 0 / 1 counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | int64 | 0 | 1000 | 1 | 500.5 | 1000 | 0 | — |
| `battery_power` | int64 | 0 | 721 | 500 | 1246.5 | 1999 | 0 | — |
| `blue` | int64 | 0 | 2 | 0 | 1 | 1 | 484 | 484 / 516 |
| `clock_speed` | float64 | 0 | 26 | 0.5 | 1.5 | 3 | 0 | — |
| `dual_sim` | int64 | 0 | 2 | 0 | 1 | 1 | 483 | 483 / 517 |
| `fc` | int64 | 0 | 20 | 0 | 3 | 19 | 210 | — |
| `four_g` | int64 | 0 | 2 | 0 | 0 | 1 | 513 | 513 / 487 |
| `int_memory` | int64 | 0 | 63 | 2 | 34.5 | 64 | 0 | — |
| `m_dep` | float64 | 0 | 10 | 0.1 | 0.5 | 1 | 0 | — |
| `mobile_wt` | int64 | 0 | 121 | 80 | 139 | 200 | 0 | — |
| `n_cores` | int64 | 0 | 8 | 1 | 4 | 8 | 0 | — |
| `pc` | int64 | 0 | 21 | 0 | 10 | 20 | 40 | — |
| `px_height` | int64 | 0 | 694 | 0 | 564.5 | 1907 | 2 | — |
| `px_width` | int64 | 0 | 743 | 501 | 1250 | 1998 | 0 | — |
| `ram` | int64 | 0 | 872 | 263 | 2153.5 | 3989 | 0 | — |
| `sc_h` | int64 | 0 | 15 | 5 | 12 | 19 | 0 | — |
| `sc_w` | int64 | 0 | 19 | 0 | 5 | 18 | 112 | — |
| `talk_time` | int64 | 0 | 19 | 2 | 11 | 20 | 0 | — |
| `three_g` | int64 | 0 | 2 | 0 | 1 | 1 | 244 | 244 / 756 |
| `touch_screen` | int64 | 0 | 2 | 0 | 0.5 | 1 | 500 | 500 / 500 |
| `wifi` | int64 | 0 | 2 | 0 | 1 | 1 | 493 | 493 / 507 |
