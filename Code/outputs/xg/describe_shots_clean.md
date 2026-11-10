# Describing pass: shots_clean.csv

Rows: 31509. Columns: 38. Duplicate `shot_id`: 0. Fully duplicated rows: 0.

## Per column

| column               | dtype   |   missing |   distinct | summary                                                                                                                                                                                                                                          |
|:---------------------|:--------|----------:|-----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| shot_id              | str     |         0 |      31509 | b0f184e6-bf9c-4c5f-8f81-2c197cdf38b4 1; 1aec37a9-5908-4a5a-b6f9-55ffb093fbb3 1; 5485a770-f859-441a-bd51-a10d6bfb55b7 1; fc8e7e77-fdbc-441a-b81a-59681b1fbfcd 1; 9a0921e9-2ef6-42fd-9eed-52bc7ac69a4d 1; 43aa4774-0851-4e64-a1b8-2ed198f8d75f 1 … |
| match_id             | int64   |         0 |       1517 | min 2.658e+05, median 3.826e+06, mean 3.754e+06, max 3.901e+06                                                                                                                                                                                   |
| league               | str     |         0 |          4 | ITA 8393; ENG 8305; ESP 7638; FRA 7173                                                                                                                                                                                                           |
| match_date           | str     |         0 |        171 | 2015-09-26 475; 2016-05-08 470; 2015-09-12 465; 2015-09-20 464; 2015-10-17 464; 2016-05-15 459 …                                                                                                                                                 |
| home_team            | str     |         0 |         80 | Frosinone 506; Real Madrid 496; Liverpool 480; Napoli 472; Chelsea 462; Tottenham Hotspur 459 …                                                                                                                                                  |
| away_team            | str     |         0 |         80 | Frosinone 575; Real Madrid 472; West Ham United 459; Tottenham Hotspur 453; Everton 452; AS Roma 449 …                                                                                                                                           |
| team                 | str     |         0 |         80 | Real Madrid 598; Napoli 595; Liverpool 561; Tottenham Hotspur 554; AS Roma 511; Juventus 508 …                                                                                                                                                   |
| player_id            | int64   |         0 |       1746 | min 2936, median 6680, mean 1.543e+04, max 4.032e+05                                                                                                                                                                                             |
| player               | str     |         0 |       1752 | Gonzalo Gerardo Higuaín 175; Cristiano Ronaldo dos Santos Aveiro 174; Harry Kane 136; Luis Alberto Suárez Díaz 126; Zlatan Ibrahimović 119; Lorenzo Insigne 119 …                                                                                |
| position             | str     |         0 |         22 | Center Forward 5063; Left Wing 3295; Right Wing 2980; Center Attacking Midfield 2525; Left Center Forward 2134; Right Center Forward 1983 …                                                                                                      |
| period               | int64   |         0 |          2 | min 1, median 2, mean 1.547, max 2                                                                                                                                                                                                               |
| minute               | int64   |         0 |         99 | min 0, median 49, mean 48.64, max 98                                                                                                                                                                                                             |
| second               | int64   |         0 |         60 | min 0, median 30, mean 29.61, max 59                                                                                                                                                                                                             |
| possession           | int64   |         0 |        239 | min 2, median 107, mean 105.2, max 249                                                                                                                                                                                                           |
| play_pattern         | str     |         0 |          9 | Regular Play 12585; From Throw In 6467; From Free Kick 4732; From Corner 3493; From Counter 1696; From Goal Kick 1442 …                                                                                                                          |
| x                    | float64 |         0 |        500 | min 60.2, median 103.8, mean 102.9, max 120                                                                                                                                                                                                      |
| y                    | float64 |         0 |        571 | min 1.5, median 39.8, mean 39.81, max 78.8                                                                                                                                                                                                       |
| end_x                | float64 |         0 |        350 | min 70.5, median 118.6, mean 115.1, max 120                                                                                                                                                                                                      |
| end_y                | float64 |         0 |        601 | min 0.1, median 40.1, mean 40.03, max 80                                                                                                                                                                                                         |
| end_z                | float64 |      9792 |         79 | min 0, median 1.1, mean 1.914, max 7.8                                                                                                                                                                                                           |
| duration             | float64 |         0 |      31156 | min 0.000166, median 0.6578, mean 0.716, max 7.124                                                                                                                                                                                               |
| under_pressure       | bool    |         0 |          2 | True 7668 (24.3%)                                                                                                                                                                                                                                |
| shot_type            | str     |         0 |          1 | Open Play 31509                                                                                                                                                                                                                                  |
| body_part            | str     |         0 |          4 | Right Foot 17489; Left Foot 10761; Head 3194; Other 65                                                                                                                                                                                           |
| technique            | str     |         0 |          7 | Normal 23205; Half Volley 5259; Volley 2289; Lob 309; Overhead Kick 212; Backheel 120 …                                                                                                                                                          |
| first_time           | bool    |         0 |          2 | True 11169 (35.4%)                                                                                                                                                                                                                               |
| follows_dribble      | bool    |         0 |          2 | True 15 (0.0%)                                                                                                                                                                                                                                   |
| open_goal            | bool    |         0 |          2 | True 360 (1.1%)                                                                                                                                                                                                                                  |
| one_on_one           | bool    |         0 |          2 | True 1674 (5.3%)                                                                                                                                                                                                                                 |
| aerial_won           | bool    |         0 |          2 | True 1517 (4.8%)                                                                                                                                                                                                                                 |
| deflected            | bool    |         0 |          2 | True 460 (1.5%)                                                                                                                                                                                                                                  |
| redirect             | bool    |         0 |          2 | True 79 (0.3%)                                                                                                                                                                                                                                   |
| key_pass_id          | str     |      8664 |      22845 | 9d8a5de2-8f8d-4587-ba43-25dd3e821df6 1; de992258-6ff2-4da2-9bb2-262d00ad9033 1; 0c0a9f1a-17fe-41d9-8d3f-78c12e648582 1; 6188ccaf-58b2-4cc2-aadf-430b165a501b 1; d1d446ec-f47c-4809-9f73-f2c5b2b4d881 1; 0972c51c-cd73-413f-93f7-c3d3b988ad3d 1 … |
| key_pass_type        | str     |      8664 |          3 | Regular 21476; Recovery 1320; Interception 49                                                                                                                                                                                                    |
| freeze_frame_players | int64   |         0 |         19 | min 2, median 12, mean 12.23, max 20                                                                                                                                                                                                             |
| statsbomb_xg         | float64 |         0 |      31462 | min 0.002722, median 0.04908, mean 0.09626, max 0.9951                                                                                                                                                                                           |
| outcome              | str     |         0 |          8 | Off T 10341; Blocked 8148; Saved 7494; Goal 3121; Wayward 1644; Post 553 …                                                                                                                                                                       |
| goal                 | int64   |         0 |          2 | min 0, median 0, mean 0.09905, max 1                                                                                                                                                                                                             |

## `league`

| league   |   count |
|:---------|--------:|
| ITA      |    8393 |
| ENG      |    8305 |
| ESP      |    7638 |
| FRA      |    7173 |

## `period`

|   period |   count |
|---------:|--------:|
|        2 |   17221 |
|        1 |   14288 |

## `play_pattern`

| play_pattern   |   count |
|:---------------|--------:|
| Regular Play   |   12585 |
| From Throw In  |    6467 |
| From Free Kick |    4732 |
| From Corner    |    3493 |
| From Counter   |    1696 |
| From Goal Kick |    1442 |
| From Keeper    |     628 |
| From Kick Off  |     418 |
| Other          |      48 |

## `position`

| position                  |   count |
|:--------------------------|--------:|
| Center Forward            |    5063 |
| Left Wing                 |    3295 |
| Right Wing                |    2980 |
| Center Attacking Midfield |    2525 |
| Left Center Forward       |    2134 |
| Right Center Forward      |    1983 |
| Left Center Midfield      |    1844 |
| Right Center Midfield     |    1641 |
| Left Midfield             |    1473 |
| Right Midfield            |    1335 |
| Left Defensive Midfield   |    1222 |
| Right Defensive Midfield  |    1184 |
| Left Back                 |    1157 |
| Right Back                |    1081 |
| Center Defensive Midfield |     689 |
| Right Center Back         |     564 |
| Left Center Back          |     534 |
| Right Wing Back           |     279 |
| Left Wing Back            |     250 |
| Right Attacking Midfield  |     121 |
| Left Attacking Midfield   |      99 |
| Center Back               |      56 |

## `body_part`

| body_part   |   count |
|:------------|--------:|
| Right Foot  |   17489 |
| Left Foot   |   10761 |
| Head        |    3194 |
| Other       |      65 |

## `technique`

| technique     |   count |
|:--------------|--------:|
| Normal        |   23205 |
| Half Volley   |    5259 |
| Volley        |    2289 |
| Lob           |     309 |
| Overhead Kick |     212 |
| Backheel      |     120 |
| Diving Header |     115 |

## `key_pass_type`

| key_pass_type   |   count |
|:----------------|--------:|
| Regular         |   21476 |
| nan             |    8664 |
| Recovery        |    1320 |
| Interception    |      49 |

## `outcome`

| outcome          |   count |
|:-----------------|--------:|
| Off T            |   10341 |
| Blocked          |    8148 |
| Saved            |    7494 |
| Goal             |    3121 |
| Wayward          |    1644 |
| Post             |     553 |
| Saved Off Target |     113 |
| Saved to Post    |      95 |

## `goal`

|   goal |   count |
|-------:|--------:|
|      0 |   28388 |
|      1 |    3121 |

## Coverage

| league   |   matches |   shots |   goals |   teams |   players | first      | last       |   goal_share |
|:---------|----------:|--------:|--------:|--------:|----------:|:-----------|:-----------|-------------:|
| ENG      |       380 |    8305 |     790 |      20 |       441 | 2015-08-08 | 2016-05-17 |       0.0951 |
| ESP      |       380 |    7638 |     831 |      20 |       435 | 2015-08-21 | 2016-05-15 |       0.1088 |
| FRA      |       377 |    7173 |     749 |      20 |       454 | 2015-08-07 | 2016-05-14 |       0.1044 |
| ITA      |       380 |    8393 |     751 |      20 |       443 | 2015-08-22 | 2016-05-15 |       0.0895 |

Matches with at least one kept shot: 1517. Teams: 80. Players: 1746.

Shots per player: median 10, max 175; players with 1 shot: 154.

Shots per match: min 4, median 20, max 40.

## Location ranges

`x` outside [0, 120]: 0; `y` outside [0, 80]: 0; shots with `x` < 60 (own half): 0.

`end_z` missing by outcome:

| outcome          |   sum |   size |
|:-----------------|------:|-------:|
| Blocked          |  8148 |   8148 |
| Goal             |     0 |   3121 |
| Off T            |     0 |  10341 |
| Post             |     0 |    553 |
| Saved            |     0 |   7494 |
| Saved Off Target |     0 |    113 |
| Saved to Post    |     0 |     95 |
| Wayward          |  1644 |   1644 |

## `statsbomb_xg`

Missing 0; zero 0; min 0.002722; max 0.9951; sum 3033.1 against 3121 goals.

## Freeze frames

Rows: 385457. Shots with a freeze frame: 31509 of 31509. Players per frame: min 2, median 12, max 20.

| teammate   | gk    |   rows |
|:-----------|:------|-------:|
| False      | False | 225777 |
| False      | True  |  31509 |
| True       | False | 128154 |
| True       | True  |     17 |

Shots with no opposing goalkeeper in the freeze frame: 0.
