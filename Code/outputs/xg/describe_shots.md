# Describing pass: shots_open_play.csv

Rows: 32256. Columns: 38. Duplicate `shot_id`: 0. Fully duplicated rows: 0.

## Per column

| column               | dtype   |   missing |   distinct | summary                                                                                                                                                                                                                                          |
|:---------------------|:--------|----------:|-----------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| shot_id              | str     |         0 |      32256 | b0f184e6-bf9c-4c5f-8f81-2c197cdf38b4 1; 1aec37a9-5908-4a5a-b6f9-55ffb093fbb3 1; 5485a770-f859-441a-bd51-a10d6bfb55b7 1; fc8e7e77-fdbc-441a-b81a-59681b1fbfcd 1; 9a0921e9-2ef6-42fd-9eed-52bc7ac69a4d 1; 43aa4774-0851-4e64-a1b8-2ed198f8d75f 1 … |
| match_id             | int64   |         0 |       1551 | min 2.658e+05, median 3.829e+06, mean 3.757e+06, max 3.901e+06                                                                                                                                                                                   |
| league               | str     |         0 |          5 | ITA 8407; ENG 8327; ESP 7660; FRA 7188; GER 674                                                                                                                                                                                                  |
| match_date           | str     |         0 |        171 | 2015-09-26 495; 2015-09-20 490; 2015-09-12 482; 2015-10-17 479; 2016-02-13 473; 2016-03-20 472 …                                                                                                                                                 |
| home_team            | str     |         0 |         98 | Frosinone 507; Real Madrid 497; Liverpool 480; Napoli 472; Chelsea 463; Tottenham Hotspur 460 …                                                                                                                                                  |
| away_team            | str     |         0 |         98 | Frosinone 576; Real Madrid 473; West Ham United 460; Tottenham Hotspur 454; Everton 454; AS Roma 451 …                                                                                                                                           |
| team                 | str     |         0 |        100 | Real Madrid 600; Napoli 597; Liverpool 562; Tottenham Hotspur 554; AS Roma 511; Juventus 509 …                                                                                                                                                   |
| player_id            | int64   |         0 |       1912 | min 2936, median 6699, mean 1.535e+04, max 4.032e+05                                                                                                                                                                                             |
| player               | str     |         0 |       1918 | Cristiano Ronaldo dos Santos Aveiro 175; Gonzalo Gerardo Higuaín 175; Harry Kane 136; Luis Alberto Suárez Díaz 126; Lorenzo Insigne 121; Zlatan Ibrahimović 120 …                                                                                |
| position             | str     |         0 |         22 | Center Forward 5150; Left Wing 3346; Right Wing 3028; Center Attacking Midfield 2608; Left Center Forward 2195; Right Center Forward 2040 …                                                                                                      |
| period               | int64   |         0 |          2 | min 1, median 2, mean 1.547, max 2                                                                                                                                                                                                               |
| minute               | int64   |         0 |        101 | min 0, median 49, mean 48.66, max 102                                                                                                                                                                                                            |
| second               | int64   |         0 |         60 | min 0, median 30, mean 29.61, max 59                                                                                                                                                                                                             |
| possession           | int64   |         0 |        239 | min 2, median 107, mean 105.3, max 249                                                                                                                                                                                                           |
| play_pattern         | str     |         0 |          9 | Regular Play 12850; From Throw In 6616; From Free Kick 4867; From Corner 3585; From Counter 1750; From Goal Kick 1468 …                                                                                                                          |
| x                    | float64 |         0 |        539 | min 35.4, median 103.8, mean 102.9, max 120                                                                                                                                                                                                      |
| y                    | float64 |         0 |        583 | min 1.5, median 39.8, mean 39.8, max 78.8                                                                                                                                                                                                        |
| end_x                | float64 |         0 |        353 | min 70.5, median 118.6, mean 115.1, max 120                                                                                                                                                                                                      |
| end_y                | float64 |         0 |        603 | min 0.1, median 40.1, mean 40.03, max 80                                                                                                                                                                                                         |
| end_z                | float64 |     10028 |         79 | min 0, median 1.1, mean 1.904, max 7.8                                                                                                                                                                                                           |
| duration             | float64 |         0 |      31889 | min 0.000166, median 0.6573, mean 0.7724, max 1747                                                                                                                                                                                               |
| under_pressure       | bool    |         0 |          2 | True 7866 (24.4%)                                                                                                                                                                                                                                |
| shot_type            | str     |         0 |          1 | Open Play 32256                                                                                                                                                                                                                                  |
| body_part            | str     |         0 |          4 | Right Foot 17949; Left Foot 10977; Head 3263; Other 67                                                                                                                                                                                           |
| technique            | str     |         0 |          7 | Normal 23713; Half Volley 5407; Volley 2346; Lob 335; Overhead Kick 217; Backheel 122 …                                                                                                                                                          |
| first_time           | bool    |         0 |          2 | True 11452 (35.5%)                                                                                                                                                                                                                               |
| follows_dribble      | bool    |         0 |          2 | True 15 (0.0%)                                                                                                                                                                                                                                   |
| open_goal            | bool    |         0 |          2 | True 372 (1.2%)                                                                                                                                                                                                                                  |
| one_on_one           | bool    |         0 |          2 | True 1715 (5.3%)                                                                                                                                                                                                                                 |
| aerial_won           | bool    |         0 |          2 | True 1548 (4.8%)                                                                                                                                                                                                                                 |
| deflected            | bool    |         0 |          2 | True 475 (1.5%)                                                                                                                                                                                                                                  |
| redirect             | bool    |         0 |          2 | True 80 (0.2%)                                                                                                                                                                                                                                   |
| key_pass_id          | str     |      8903 |      23353 | 9d8a5de2-8f8d-4587-ba43-25dd3e821df6 1; de992258-6ff2-4da2-9bb2-262d00ad9033 1; 0c0a9f1a-17fe-41d9-8d3f-78c12e648582 1; 6188ccaf-58b2-4cc2-aadf-430b165a501b 1; d1d446ec-f47c-4809-9f73-f2c5b2b4d881 1; 0972c51c-cd73-413f-93f7-c3d3b988ad3d 1 … |
| key_pass_type        | str     |      8903 |          3 | Regular 21937; Recovery 1365; Interception 51                                                                                                                                                                                                    |
| freeze_frame_players | int64   |         0 |         21 | min 1, median 12, mean 12.24, max 21                                                                                                                                                                                                             |
| statsbomb_xg         | float64 |         0 |      32209 | min 0.002585, median 0.04917, mean 0.09651, max 0.9951                                                                                                                                                                                           |
| outcome              | str     |         0 |          8 | Off T 10536; Blocked 8310; Saved 7699; Goal 3203; Wayward 1718; Post 571 …                                                                                                                                                                       |
| goal                 | int64   |         0 |          2 | min 0, median 0, mean 0.0993, max 1                                                                                                                                                                                                              |

## `league`

| league   |   count |
|:---------|--------:|
| ITA      |    8407 |
| ENG      |    8327 |
| ESP      |    7660 |
| FRA      |    7188 |
| GER      |     674 |

## `period`

|   period |   count |
|---------:|--------:|
|        2 |   17644 |
|        1 |   14612 |

## `play_pattern`

| play_pattern   |   count |
|:---------------|--------:|
| Regular Play   |   12850 |
| From Throw In  |    6616 |
| From Free Kick |    4867 |
| From Corner    |    3585 |
| From Counter   |    1750 |
| From Goal Kick |    1468 |
| From Keeper    |     645 |
| From Kick Off  |     427 |
| Other          |      48 |

## `position`

| position                  |   count |
|:--------------------------|--------:|
| Center Forward            |    5150 |
| Left Wing                 |    3346 |
| Right Wing                |    3028 |
| Center Attacking Midfield |    2608 |
| Left Center Forward       |    2195 |
| Right Center Forward      |    2040 |
| Left Center Midfield      |    1863 |
| Right Center Midfield     |    1659 |
| Left Midfield             |    1537 |
| Right Midfield            |    1394 |
| Left Defensive Midfield   |    1277 |
| Right Defensive Midfield  |    1228 |
| Left Back                 |    1185 |
| Right Back                |    1102 |
| Center Defensive Midfield |     693 |
| Right Center Back         |     577 |
| Left Center Back          |     556 |
| Right Wing Back           |     286 |
| Left Wing Back            |     256 |
| Right Attacking Midfield  |     121 |
| Left Attacking Midfield   |      99 |
| Center Back               |      56 |

## `body_part`

| body_part   |   count |
|:------------|--------:|
| Right Foot  |   17949 |
| Left Foot   |   10977 |
| Head        |    3263 |
| Other       |      67 |

## `technique`

| technique     |   count |
|:--------------|--------:|
| Normal        |   23713 |
| Half Volley   |    5407 |
| Volley        |    2346 |
| Lob           |     335 |
| Overhead Kick |     217 |
| Backheel      |     122 |
| Diving Header |     116 |

## `key_pass_type`

| key_pass_type   |   count |
|:----------------|--------:|
| Regular         |   21937 |
| nan             |    8903 |
| Recovery        |    1365 |
| Interception    |      51 |

## `outcome`

| outcome          |   count |
|:-----------------|--------:|
| Off T            |   10536 |
| Blocked          |    8310 |
| Saved            |    7699 |
| Goal             |    3203 |
| Wayward          |    1718 |
| Post             |     571 |
| Saved Off Target |     116 |
| Saved to Post    |     103 |

## `goal`

|   goal |   count |
|-------:|--------:|
|      0 |   29053 |
|      1 |    3203 |

## Coverage

| league   |   matches |   shots |   goals |   teams |   players | first      | last       |   goal_share |
|:---------|----------:|--------:|--------:|--------:|----------:|:-----------|:-----------|-------------:|
| ENG      |       380 |    8327 |     794 |      20 |       441 | 2015-08-08 | 2016-05-17 |       0.0954 |
| ESP      |       380 |    7660 |     834 |      20 |       435 | 2015-08-21 | 2016-05-15 |       0.1089 |
| FRA      |       377 |    7188 |     751 |      22 |       454 | 2015-08-07 | 2016-05-14 |       0.1045 |
| GER      |        34 |     674 |      72 |      18 |       169 | 2015-08-15 | 2016-05-14 |       0.1068 |
| ITA      |       380 |    8407 |     752 |      20 |       443 | 2015-08-22 | 2016-05-15 |       0.0894 |

Matches with at least one kept shot: 1551. Teams: 100. Players: 1912.

Shots per player: median 9, max 175; players with 1 shot: 227.

Shots per match: min 4, median 21, max 40.

## Location ranges

`x` outside [0, 120]: 0; `y` outside [0, 80]: 0; shots with `x` < 60 (own half): 41.

`end_z` missing by outcome:

| outcome          |   sum |   size |
|:-----------------|------:|-------:|
| Blocked          |  8310 |   8310 |
| Goal             |     0 |   3203 |
| Off T            |     0 |  10536 |
| Post             |     0 |    571 |
| Saved            |     0 |   7699 |
| Saved Off Target |     0 |    116 |
| Saved to Post    |     0 |    103 |
| Wayward          |  1718 |   1718 |

## `statsbomb_xg`

Missing 0; zero 0; min 0.002585; max 0.9951; sum 3113.0 against 3203 goals.

## Freeze frames

Rows: 394917. Shots with a freeze frame: 32256 of 32256. Players per frame: min 1, median 12, max 21.

| teammate   | gk    |   rows |
|:-----------|:------|-------:|
| False      | False | 231168 |
| False      | True  |  32224 |
| True       | False | 131480 |
| True       | True  |     45 |

Shots with no opposing goalkeeper in the freeze frame: 32.
