# Appendix

*The running record. Filled from the first step, not at the end. Everything that does not belong in the report belongs here: the workings, the diagnostics, the decisions and what each one cost.*

## Data Summary

*Step 1 complete; revised in step 2 (10 November 2026) when the Bundesliga was dropped. Provenance, the scope of shots, the description of the data used and the step 1 decisions are recorded below.*

**Provenance.** StatsBomb Open Data, season 2015/16, for the Premier League (ENG, 380 matches), La Liga (ESP, 380), Serie A (ITA, 380), Ligue 1 (FRA, 377) and 1. Bundesliga (GER, 34). Downloaded on 9 November 2026 from [github.com/statsbomb/open-data](https://github.com/statsbomb/open-data), pinned to commit `4b73468fc5b0f1950f9f66fada70ad3a4f9327cb`. Stored in `Attachments/statsbomb-open-data-2015-16/`, with full details in `Attachments/SOURCE.md`; `SHA256SUMS_raw.txt` (SHA-256 `17c312fb…4312e`) lists a checksum for each of the 1,556 raw files. This source was chosen because the user's `xT_Model_comparison` project used the same leagues and season. That project's converted tables (`../data`) were not on disk, so the data was downloaded again. As a cross-check, the 38,728 shots in the download match that project's README exactly. **Best available form.** Whether a fuller form exists was raised: StatsBomb 360 frames for these matches, or later seasons of these leagues that could act as a future test set. The user decided that this download is the data the analysis uses: "We don't have any more data. So this is what we have." (9 November 2026). Neither possibility was checked.

**Scope of shots, first version (9 November 2026), superseded by the version below.** Only open-play shots are kept: those whose StatsBomb `shot.type` is `Open Play`. Excluded: 410 penalties, 1,801 direct free kicks and 9 direct corners. No kick-off shots occur. This leaves 36,508 shots, 3,533 of which are goals. The filter is on the shot's own type. A shot later in a move that began at a set piece (`play_pattern` = "From Corner", "From Free Kick", …) still counts as open play and is kept.

**Scope of shots, second version (9 November 2026), superseded by the version below.** Open-play shots are kept, except those whose key pass is a corner. The key pass is the pass StatsBomb links to the shot through `shot.key_pass_id`: the pass that set it up. This removes a further 2,606 open-play shots (ENG 694, ESP 607, ITA 601, FRA 643, GER 61) and leaves 33,902 shots, 3,340 of which are goals. Not excluded, and recorded so the choice can be revisited:

- 3,584 kept shots come later in a possession that included a corner, with at least one other pass or touch in between.
- 1,387 kept shots have a free kick as their key pass (an indirect free kick played in).

**Scope of shots, third version (9 November 2026), superseded by the version below.** Open-play shots are kept, except those whose key pass (`shot.key_pass_id`) is a corner or a free kick. A ball delivered from a dead-ball situation and shot directly is treated as a set piece, not open play. This removes 2,606 corner-assisted shots (ENG 694, ESP 607, ITA 601, FRA 643, GER 61) and 1,387 free-kick-assisted shots (ENG 323, ESP 336, ITA 324, FRA 369, GER 35). It leaves 32,515 shots, 3,217 of which are goals. Not excluded: 3,584 kept shots come later in a possession that included a corner, with at least one other pass or touch in between. Shots assisted by a throw-in (240) or a goal kick (15) are also kept.

**Scope of shots, fourth version (9 November 2026), superseded by the version below.** Open-play shots are kept, except those whose key pass (`shot.key_pass_id`) is a corner, a free kick or a throw-in. A ball delivered from a restart and shot directly is treated as a set piece, not open play. This removes 2,606 corner-assisted shots (ENG 694, ESP 607, ITA 601, FRA 643, GER 61), 1,387 free-kick-assisted shots (ENG 323, ESP 336, ITA 324, FRA 369, GER 35) and 240 throw-in-assisted shots (ENG 65, ESP 56, ITA 57, FRA 56, GER 6). It leaves 32,275 shots, 3,204 of which are goals. Not excluded: 3,584 kept shots come later in a possession that included a corner, with at least one other pass or touch in between. Shots assisted by a goal kick (15) or a kick-off (4) are also kept.

**Scope of shots, by shot and key pass (decided by the user, 9 November 2026).** Open-play shots are kept, except those whose key pass (`shot.key_pass_id`) comes from a restart. Excluded: 2,606 shots after a corner (ENG 694, ESP 607, ITA 601, FRA 643, GER 61), 1,387 after a free kick (ENG 323, ESP 336, ITA 324, FRA 369, GER 35), 240 after a throw-in (ENG 65, ESP 56, ITA 57, FRA 56, GER 6), 15 after a goal kick (ENG 4, ESP 2, ITA 6, FRA 3) and 4 after a kick-off (ENG 2, ITA 1, FRA 1). It leaves 32,256 shots, 3,203 of which are goals. Every kept shot either has no key pass (8,903) or has one from open play: a regular pass (21,937), a recovery (1,365) or an interception (51). Not excluded: 3,584 kept shots come later in a possession that included a corner, with at least one other pass or touch in between.

**Scope of leagues (decided by the user, 10 November 2026).** The Bundesliga (GER) is dropped completely: 34 matches, 674 shots and 72 goals before cleaning. The open data holds only Bayer Leverkusen's matches for that season, so each of the other 17 teams appears twice. That made it impossible to give every team the same number of test matches, which the user wanted (DR-09). The analysis uses the four complete leagues: ENG, ESP, ITA and FRA.

The excluded shots can't be described by any model fitted here.

Key-pass type of the 36,508 open-play shots, before the corner exclusion: regular pass 21,937; no key pass 8,903; corner 2,606; free kick 1,387; recovery 1,365; throw-in 240; interception 51; goal kick 15; kick-off 4.

| League | Open play (kept) | Free kick | Penalty | Corner |
| --- | --- | --- | --- | --- |
| ENG | 9,415 | 401 | 91 | 1 |
| ESP | 8,661 | 409 | 97 | 1 |
| ITA | 9,396 | 479 | 121 | 2 |
| FRA | 8,260 | 460 | 91 | 3 |
| GER | 776 | 52 | 10 | 2 |

**Derived tables** (`Code/outputs/xg/`, written by `Code/xg/01_download_shots.py`): `shots_open_play.csv`, one row per kept shot, 32,256 rows, SHA-256 `00bdc7fe…3b725657`; `freeze_frames_open_play.csv`, one row per player visible in each kept shot's freeze frame, 394,917 rows, SHA-256 `13abf160…a0649d`. (Earlier versions had 36,508 / 461,989, 33,902 / 420,340, 32,515 / 398,485 and 32,275 / 395,129 rows and have been overwritten.) The full checksums are in `download_log.txt`. **The analysis uses the cleaned tables** written by `Code/xg/03_clean_shots.py`: `shots_clean.csv`, 31,509 rows, SHA-256 `5d46319e…7d39efd85`, and `freeze_frames_clean.csv`, 385,457 rows, SHA-256 `6a6c2b4a…e710387`. Full checksums are in `clean_log.txt`. (The version before GER was dropped had 32,182 and 393,923 rows.)

### Description of the data used: `shots_clean.csv`

This is a describing pass: it says what is in the file and judges nothing. It covers the cleaned table that the analysis uses: `shots_open_play.csv` without the Bundesliga and without the oddities listed under *Cleaning* below. The full outputs are `Code/outputs/xg/describe_shots_clean.md` (cleaned table) and `describe_shots.md` (the table before cleaning, which is where the oddities were found). Both are written by `Code/xg/02_describe_shots.py`.

**Shape.** 31,509 rows and 38 columns, one row per shot. No `shot_id` is duplicated and no row is duplicated. No value is missing except where noted below.

**Coverage.** 1,517 matches in four leagues, played between 7 August 2015 and 17 May 2016. Every match has at least one shot (minimum 4, median 20, maximum 40). There are 80 teams and 1,746 player IDs. Six of the IDs appear under two spellings of a name; player names are not used. Shots per player: median 10, maximum 175, and 154 players have a single shot.

| League | Matches | Shots | Goals | Goal share | Teams | Players |
| --- | --- | --- | --- | --- | --- | --- |
| ENG | 380 | 8,305 | 790 | 0.095 | 20 | 441 |
| ESP | 380 | 7,638 | 831 | 0.109 | 20 | 435 |
| FRA | 377 | 7,173 | 749 | 0.104 | 20 | 454 |
| ITA | 380 | 8,393 | 751 | 0.089 | 20 | 443 |

**Units and coordinates.** Locations are in StatsBomb's pitch coordinates (documentation, Appendix 2). The pitch is 120 long by 80 wide whatever the real size of the ground, and every shot is oriented so the attacking team plays towards x = 120. The goal is at x = 120, between y = 36 and y = 44. The documentation gives pass lengths in yards, but the coordinate frame is fixed rather than measured, so a coordinate unit is a yard only on a pitch of 120 × 80 yards. Appendix 2 is a diagram, and its numbers could not be read as text; the goal-mouth values above are the usual StatsBomb convention and have not been checked against the diagram. All `x` lie in [60.2, 120] and all `y` in [1.5, 78.8].

**Measurement or model output.** Every column is coded by StatsBomb analysts from match video. That makes each one a recorded judgement rather than an instrument reading, except `statsbomb_xg`, which is a model output.

| Column | Meaning | Type, unit | Values |
| --- | --- | --- | --- |
| `shot_id`, `match_id`, `possession`, `key_pass_id` | Identifiers: the shot, the match, the possession sequence within the match, and the pass that set up the shot | ID | `key_pass_id` missing for 8,664 shots with no assisting pass |
| `league`, `match_date`, `home_team`, `away_team`, `team`, `player_id`, `player`, `position` | Context: who shot, for whom, when, and from which tactical position | categorical / date | 4 leagues, 80 teams, 1,746 players, 22 positions (centre forward 5,063 … centre back 56) |
| `period`, `minute`, `second` | Time of the shot | integer; minutes | Period 1: 14,288 shots, period 2: 17,221. Minute 0–98, including stoppage time |
| `play_pattern` | How the possession began | categorical, 9 levels | Regular play 12,585; from throw-in 6,467; from free kick 4,732; from corner 3,493; from counter 1,696; from goal kick 1,442; from keeper 628; from kick-off 418; other 48 |
| `x`, `y` | Where the shot was taken | pitch units | See above |
| `under_pressure` | An opponent pressured the shooter at the moment of the shot | boolean | True 7,668 (24.3 %) |
| `body_part` | Body part used | categorical, 4 | Right foot 17,489; left foot 10,761; head 3,194; other 65 |
| `technique` | Striking technique | categorical, 7 | Normal 23,205; half volley 5,259; volley 2,289; lob 309; overhead kick 212; backheel 120; diving header 115 |
| `first_time`, `follows_dribble`, `open_goal`, `one_on_one`, `aerial_won`, `redirect` | Analyst flags describing the situation | boolean | True: 11,169; 15; 360; 1,674; 1,517; 79 |
| `key_pass_type` | Type of the assisting pass | categorical, 3 + none | Regular 21,476; recovery 1,320; interception 49; none 8,664 |
| `freeze_frame_players` | Number of other players shown in the freeze frame | count | 2–20, median 12 |
| `end_x`, `end_y`, `end_z` | Where the ball ended up (`end_z` is height) | pitch units | `end_z` missing for 9,792 shots: every `Blocked` (8,148) and every `Wayward` (1,644) shot, and no others |
| `duration` | Time the shot event lasted | seconds | Median 0.66, 99.9th percentile 4.1, maximum 7.1 |
| `deflected` | The shot was deflected by another player's touch | boolean | True 460 |
| `outcome` | What happened to the shot | categorical, 8 | Off target 10,341; blocked 8,148; saved 7,494; goal 3,121; wayward 1,644; post 553; saved off target 113; saved to post 95 |
| `goal` | 1 if `outcome` is `Goal`, else 0 (derived in the extraction script) | binary | 0: 28,388; 1: 3,121 (9.91 %) |
| `statsbomb_xg` | StatsBomb's own expected-goals value for the shot | probability; model output | 0.0027–0.995, median 0.049. Sums to 3,033.1 against 3,121 goals |
| `shot_type` | Shot type | constant | `Open Play` for every row, by construction |

**Freeze frames** (`freeze_frames_clean.csv`). Every shot has one, with 385,457 player rows in total: 257,286 opponents (one goalkeeper per shot, 31,509) and 128,171 teammates of the shooter (17 of them goalkeepers). 22 frames show two or fewer players. A frame shows the players the analyst recorded, not all 21 others on the pitch.

**Machine learning checks.**

- *Target:* `goal`, derived from `outcome`. The label is the analyst's record of whether the shot scored. Own goals are separate events in StatsBomb data and are not shots, so they are not in the file. Class counts: 3,121 goals and 28,388 non-goals.
- *Output type it suggests (Property 1: output type, to be confirmed in step 2):* binary.
- *Columns recorded after the shot, or derived from the outcome:* `outcome` and `goal` (the target itself); `end_x`, `end_y` and `end_z` (where the ball went, with `end_z` missing exactly for blocked and wayward shots); `duration` (the ball's flight time); `deflected` (a touch after the shot is struck). `statsbomb_xg` is another model's prediction of the same target. All are kept out as inputs (see *Target and leakage* below). `freeze_frame_players` is a feature of how the frame was recorded, and the description does not show whether it is related to the outcome.
- *Number of inputs (Property 3: number of inputs, Property 4: categorical share).* Not yet fixed, because which columns enter is a decision for steps 2 and 3. For orientation only, take the shot's own attributes recorded at the moment of the shot: `x`, `y`, `body_part`, `technique`, `play_pattern`, `key_pass_type`, `under_pressure`, `first_time`, `follows_dribble`, `open_goal`, `one_on_one`, `aerial_won` and `redirect`. That is 13 columns: 2 numeric, 4 categorical with several levels, and 7 boolean. After one-hot encoding with one indicator per level, they make 2 + (4 + 7 + 9 + 4) + 7 = 33 inputs. The share of categorical columns is 4 of 13 if booleans count as numeric, or 11 of 13 if they count as categorical. A team factor would add 80 indicators, and inputs built from the freeze frames (for example distance, angle, or defenders between the ball and the goal) would also change these counts.

**Step 1 decisions** (9 November 2026, by the user).

| Decision | What was decided, and why | What it costs |
| --- | --- | --- |
| **Provenance** | StatsBomb open data, 2015/16, five leagues downloaded, pinned to commit `4b73468` (see *Provenance* above); four used. | Only one season is available. |
| **Units** | StatsBomb pitch coordinates (120 × 80, attacking towards x = 120) and seconds, from the *Open Data Events v4.0.0* documentation. Every column except `statsbomb_xg` is an analyst's coding from video; `statsbomb_xg` is a model output. | The goal-mouth coordinates are the usual convention and were not read from the documentation's diagram. |
| **Scope** | Open-play shots only. Removed: shots of type penalty, free kick or corner (2,220), and open-play shots whose key pass came from a restart: corner, free kick, throw-in, goal kick or kick-off (4,252). Then the Bundesliga (674 shots, 10 November 2026) and the 73 oddities under *Cleaning*. 31,509 shots remain, from ENG, ESP, ITA and FRA. | The model cannot be used for set pieces or for shots assisted directly from a restart, and it is not tested on the Bundesliga. |
| **Target and leakage** | The target is `goal`, which is 1 when StatsBomb records the shot's outcome as `Goal`. Kept out of every model as inputs: `outcome` (the target itself); `end_x`, `end_y` and `end_z` (where the ball went, known only after the shot; `end_z` is missing exactly for blocked and wayward shots); `duration` (the ball's flight time); `deflected` (a touch after the shot); and `statsbomb_xg` (another model's prediction of the same target). `statsbomb_xg` stays in the file and may be used later as a point of comparison, never as an input. | Nothing the model can know at the moment of the shot is lost. |
| **Admissibility** | Admissibility 1: outcome recorded — yes (DR-01). Admissibility 3: grouped or time-ordered rows — grouped by match, so the split and every cross-validation fold keep a match's shots together. The data is not treated as a time series (DR-03). Admissibility 4: new cases like these — the model is for future seasons (DR-02). The test data are whole matchweeks drawn at random within each league, so every team has the same number of test matches (DR-09, superseding DR-04's random draw by match). Admissibility 2: prediction or understanding is asked in step 2. | The test estimates the error on new 2015/16-like matches. How much shots change between seasons can't be measured with one season, so the estimate holds for future seasons only as far as they resemble 2015/16. |
| **Grouping and time order** | Group column `match_id` (1,517 matches, 4–40 shots each). Teams and players also recur across matches but are not used as groups. | A team or player can appear in both training and test data. |
| **Missing data** | Nothing is imputed. `key_pass_id` and `key_pass_type` are missing for 8,664 shots with no assisting pass; this is a real category ("none"), not a gap. `end_z` is missing for blocked and wayward shots, but it is never an input. | None. |
| **Cleaning** | At the user's request, the oddities from the describing pass were removed (`Code/xg/03_clean_shots.py`): 1 shot whose event lasted 1,746.6 s (more than `MAX_DURATION_S` = 60 s), 41 shots from the shooter's own half (x < 60), and 31 shots whose freeze frame shows no opposing goalkeeper. The groups don't overlap: 73 shots removed, 10 of them goals, all 10 among the no-goalkeeper shots. (Counted after the Bundesliga was dropped; before, there were 32 no-goalkeeper shots and 74 removed.) Two event-file team names were harmonised with the match files: `Caen` became `Stade Malherbe Caen` and `Marseille` became `Olympique de Marseille` (189 shots). No value was altered. | The model is not fitted to shots from a player's own half. The 31 no-goalkeeper shots scored at a much higher rate (10 of 31) than the rest. None of them is flagged `open_goal`, so they look like frames where the goalkeeper was not recorded rather than empty-net chances. |
| **Accepted as-is** | Six player IDs with two spellings of a name: names are not used, and the IDs are consistent. 22 freeze frames with two or fewer players: kept, because a frame shows only the players the analyst recorded. | Inputs built from the freeze frames will be computed from incomplete frames for some shots. |
| **Experience level** | The user describes their experience with machine learning as "reasonable". | — |


## Problem Definition

*Written in step 2 (9–10 November 2026), before anything was fitted.*

### Discussion

- **The problem, in the user's words:** "I want measure how good a chance is, but also see if some teams are better than others given the same chance (hence teams)."
- **Admissibility 2: prediction or understanding** (DR-05). The user's stated aim was understanding. They were told that the workflow optimises prediction and does not establish how variables are connected, and they confirmed that the work should continue on the prediction basis. Chance quality is the predicted probability that a shot scores. The team question is answered in its prediction form: whether knowing the team improves predictions for new shots beyond the chance itself. A better prediction with team would not show that a team *causes* more goals. It could equally reflect differences in chance quality that the inputs do not capture.
- **Considered and ruled out.**
  - *A significance test of the team coefficients* was the user's first criterion for sub-task 2. It is classical statistics, which the book sets aside (SML p. 20); chapters 2, 3, 4 and 13 give no method for it. With about 80 team coefficients, shots correlated within matches and L2 shrinkage, a valid test would need methods from outside the book. The user chose the prediction criterion instead.
  - *XGBoost* (gradient boosting) was asked about. It is in chapter 8, outside the solution space (`ML Guide.md` §23). If the diagnosis loop finds evidence that more flexibility would help, it can be recorded as a flag, never used.
  - *Accuracy as the metric.* Predicting "no goal" for every shot is right about 90 % of the time, so accuracy cannot tell models apart on this problem.
- **Feasibility.**
  - *Output:* `goal` is recorded for every shot (DR-01).
  - *Rows per input:* there are 24,816 training shots, about 730 per parameter without team and about 218 with it, so data is ample on either count. (The figure of 222 written first counted 78 teams instead of 80; corrected in step 3, Analysis Log row 29.)
  - *Grouping:* shots are grouped by match, so the split and every fold keep whole matches together (DR-03).
  - *Scope:* under the must-have on probabilities, only logistic regression remains in scope. Its four configurations (plain, with polynomial terms, with L2, with both) are all within the four chapters.

### Problem

- **Predicted:** y = `goal` (1 if the shot scored), for open-play shots not assisted directly from a restart, in the Premier League, La Liga, Serie A and Ligue 1. **Property 1: output type** = binary.
- **From:** attributes of the chance known at the moment of the shot. The candidate columns, before step 3's input design, are `x`, `y`, `body_part`, `technique`, `play_pattern`, `key_pass_type`, `under_pressure`, `first_time`, `follows_dribble`, `open_goal`, `one_on_one`, `aerial_won` and `redirect`. Sub-task 2 adds `team`. Inputs built from these columns or from the freeze frames, such as distance and angle to goal or defenders in the way, are decided in step 3; the input design is in DR-13. The columns set aside as leakage in step 1 are never inputs.
- **What a prediction is for:** to measure how good a chance was, as a probability of scoring (an xG value), and to compare teams on finishing given the same chances. No decision threshold is applied; the probability is the product. An error is a probability that is too high or too low for shots like this one.
- **Deciding metric:** log-loss (cross-entropy) on held-out shots, lower is better. It is the loss logistic regression is trained on (SML pp. 52–53), and the book allows many error functions besides its defaults, keeping the error function used to evaluate a model separate from the loss used to train it (SML p. 67); the metric is chosen as part of defining the problem (SML p. 330). Using log-loss as the evaluation metric is our interpretation of those facts `[B→I SML pp. 52–53, 67, 330]`: the classification metrics in SML pp. 89–93 judge classes rather than probabilities. (First written `[I]`; corrected after the book was checked, Analysis Log row 32.)
- **Monitored alongside:** the Brier score (mean squared difference between probability and outcome); ROC-AUC (SML p. 90), which checks that better chances are ranked higher; and the total of predicted probabilities against the number of goals, as a check on calibration.
- **Baseline:** the training goal rate, 2,479 / 24,816 = 0.0999, predicted for every shot. This is the probability version of the book's most-common-class baseline (SML pp. 330–331).
- **Achievable level:** StatsBomb's own xG (`statsbomb_xg`), scored on the same test shots. It is a comparable model, not an input (SML p. 331).
- **Success criteria:**
  - *Sub-task 1:* on the test shots, the model's improvement in log-loss over the baseline is at least 90 % of StatsBomb xG's improvement. In symbols, (LL_baseline − LL_model) ≥ 0.9 × (LL_baseline − LL_StatsBomb). The user's words: "Should be similar to statsbomb xG"; they chose this form ("(b) is good").
  - *Sub-task 2:* the model with team beats the recommended model of sub-task 1 on cross-validated log-loss, on the same outer folds, by a margin of at least one fold spread (the standard deviation of the fold differences). The test set must agree: on the same test shots, the model with team has the lower log-loss. The user chose this over a significance test ("Do 1. a)").
- **Requirements and expectations** (user, 10 November 2026):
  - *Property 5: interpretability* — none for sub-task 1; inspectable for sub-task 2, so that the team effects can be read ("No. Just for teams.").
  - *Property 6: probabilities* — yes, a must-have ("Property 6 must have."). This leaves only logistic regression in scope (`ML Guide.md` §12).
  - *Property 7: extrapolation* — no ("No.").
  - *Property 8: expected shape* — unknown. The user's expectation is a direction, not a shape: "Longer distance, lower chance." / "direction only".

### Sub-tasks

1. **Chance quality.** Predict `goal` from attributes of the chance only. Success: at least 90 % of StatsBomb xG's test-set improvement in log-loss over the baseline.
2. **Team.** Predict `goal` from the same attributes plus the shooting team. Success: beats the sub-task 1 model on cross-validated log-loss by at least one fold spread, and has the lower test-set log-loss.

### Split

Whole matchweeks are drawn at random: 8 of the 38 matchweeks in each league go to the test set (DR-10). Every team plays exactly once per matchweek, so every team has the same number of test matches: 8, except Bastia and Gazélec Ajaccio with 7, because Ligue 1's matchweek 14 has only 9 matches. Agreed with the user as "20 % of matches"; whole weeks give about 21 %. Seed 20261111. The weeks drawn are ENG 3, 8, 16, 27, 31, 34, 35, 36; ESP 2, 5, 7, 9, 10, 12, 17, 35; ITA 2, 7, 11, 12, 17, 26, 28, 35; FRA 1, 4, 7, 11, 14, 16, 17, 22.

| | Matches | Shots | Goals | Goal share |
| --- | --- | --- | --- | --- |
| Training | 1,198 | 24,816 | 2,479 | 0.0999 |
| Test | 319 | 6,693 | 642 | 0.0959 |

**The test set is locked.** It is in `Code/outputs/xg/split/test_locked/`. Nothing in steps 3 and 4 reads it until the single final evaluation of each sub-task.

**First split, superseded (DR-08).** The first split drew 20 % of matches at random with `GroupShuffleSplit` (seed 20261110): 1,240 training and 311 test matches. It gave teams between 2 and 16 test matches each, and put both of Ingolstadt's matches in the test set. It was replaced, before anything was fitted, by the matchweek split above, with the Bundesliga dropped (DR-09, DR-10).

## Analysis

### The training data (step 3)

Figures 1–3 were drawn from the 24,816 training shots; Figures 1 and 2 are in `Project Report.md`. They were first drawn in David's figure style and redrawn on 10 November 2026 in the style of the book's figures (`Code/sml_style.py`, via `Code/xg/xg_style.py`: serif type, full box, inward ticks, framed legend, the book's palette; 300 dpi), in a light and a dark variant; the report embeds the light one. Red is goals and the share scored, grey is all shots, in every figure. Figure 3 is 16 × 14 cm instead of 10 × 8 cm so that its 24 labelled bars stay readable. Every number quoted with the figures comes from the files written by the figure scripts, not from the images.

- **Figure 1** (`06_fig1_shot_map.py`): 24,816 shots, 2,479 goals; 14,181 shots and 2,154 goals inside the penalty area (`figures/fig1_numbers.txt`).
- **Figure 2** (`07_fig2_goal_share_distance.py`): shots, goals and share per 2-unit band, bands from 40 units pooled (`figures/fig2_numbers.csv`). The 0–2 band holds 8 shots, all goals; the pooled band holds 217 shots and 2 goals.
- **Figure 3, dropped from the report by the user** (`08_fig3_goal_share_types.py`; the script and image are kept): shots, goals and share per level of body part, technique, play pattern and key-pass type (`figures/fig3_numbers.csv`). The smallest levels hold 31 (play pattern "Other"), 38 (interception) and 56 (body part "Other") shots.

The figures describe the training data. They do not set Property 8: expected shape, which stays as the user stated it (DR-14).

## Decision Records

*The advisor's reasoning trace, one record per decision, written when the decision is made, in the format of `ML Guide.md` §24. Records are never renumbered; a reversed decision stays, marked superseded.*

### DR-01 · Admissibility · step 1

- **Sub-task:** all
- **Date:** 2026-11-09
- **Question:** Is there a recorded output y for the rows to be learned from (Admissibility 1: outcome recorded)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| `goal` | recorded for all 32,256 shots: 29,053 × 0, 3,203 × 1; derived from the StatsBomb shot outcome (`Goal`) | M | `Code/outputs/xg/describe_shots.md`; StatsBomb *Open Data Events v4.0.0* |
| User's answer | "yes" | M | user, 9 November 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 1: outcome recorded | yes | [B SML p. 15] | supervised problem; continue |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** continue with `goal` · stop
- **Expectation:** n/a
- **Decision:** `goal` is the recorded output. The problem is supervised, so the work continues.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "yes"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/xg/02_describe_shots.py`, `Code/outputs/xg/describe_shots.md`

### DR-02 · Admissibility · step 1

- **Sub-task:** all
- **Date:** 2026-11-09
- **Question:** Will the cases the model is used on look like the data we have (Admissibility 4: new cases like these)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Data | open-play shots from one season, 2015/16, in five men's top-flight leagues (four complete, plus 34 Bundesliga matches) | M | `Data Summary` |
| Intended use | "New cases will be future seasons" | M | user, 9 November 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 4: new cases like these | unsure: the shots are of the same kind, but they come from seasons the data doesn't contain | [B SML pp. 328–329] | agree with the user where the validation and test data should come from, before splitting |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** yes (split as if future seasons were like 2015/16) · unsure (agree the source of the validation and test data first)
- **Expectation:** n/a
- **Decision:** The model is for shots in future seasons, which no data here comes from. Before the split, the user and the advisor agree how the validation and test data should stand in for future seasons. That agreement is recorded in DR-04.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "New cases will be future seasons"
- **Supersedes / superseded by:** n/a
- **Links:** n/a

### DR-03 · Admissibility · step 1

- **Sub-task:** all
- **Date:** 2026-11-09
- **Question:** Do several rows belong to the same unit, or are rows ordered in time (Admissibility 3: grouped or time-ordered rows)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Matches | 1,551 matches, 4–40 shots each (median 20); shots in a match share the conditions, the score and the goalkeepers | M | `Code/outputs/xg/describe_shots_clean.md` |
| Teams, players | 98 teams and 1,912 players recur across matches | M | `Code/outputs/xg/describe_shots_clean.md` |
| Time | shots are dated (`match_date`, `minute`), but a shot's outcome is not modelled as depending on earlier outcomes | M | `Data Summary` |
| User's answer | to the proposal to keep each match together and not treat the data as a time series: "I agree. Do that." | M | user, 9 November 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 3: grouped or time-ordered rows | group column `match_id`; no time column used | [B SML pp. 16, 38–39, 329] | split and cross-validate by match: all of a match's shots go to the same side |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** no grouping (random split by shot) · group by match · group by team · group by player · time column (autoregressive reformulation or flag)
- **Expectation:** n/a
- **Decision:** Rows are grouped by `match_id`. The train/test split and every cross-validation fold keep a match's shots together. The data is not treated as a time series.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "I agree. Do that."
- **Supersedes / superseded by:** n/a
- **Links:** `Code/xg/02_describe_shots.py`, `Code/outputs/xg/describe_shots_clean.md`

### DR-04 · Admissibility · step 1 · **superseded**

- **Sub-task:** all
- **Date:** 2026-11-09
- **Question:** Where should the validation and test data come from, so that they stand in for the future seasons the model is for (the action required by DR-02)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Intended use | "New cases will be future seasons" | M | user, DR-02 |
| Data | a single season, 2015/16 | M | `Data Summary` |
| Options set out | (a) random by match, which assumes future seasons look like 2015/16; (b) chronological, testing on the last matchdays of the season | M | conversation, 9 November 2026 |
| User's answer | "Do (a) random by match." | M | user, 9 November 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 4: new cases like these | validation and test data drawn at random by match from 2015/16 | [B SML pp. 328–329] | the test estimates the error on new matches like 2015/16; a shift between seasons is not measured |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** (a) random by match · (b) chronological split within the season
- **Expectation:** n/a
- **Decision:** The validation and test data are drawn at random by match from 2015/16. The test result is read as an estimate for future seasons only as far as they resemble 2015/16.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Do (a) random by match."
- **Supersedes / superseded by:** superseded by DR-09
- **Links:** n/a

### DR-05 · Admissibility · step 2

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** Is the main aim to predict y for new cases, or to understand how the variables are connected (Admissibility 2: prediction or understanding)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| User's aim | "I want understanding. I want measure how good a chance is, but also see if some teams are better than others given the same chance (hence teams)." | M | user, 9 November 2026 |
| Explanation given | The workflow optimises prediction and does not establish how variables are connected. The team question can be answered in its prediction form: whether knowing the team improves predictions for new shots beyond the chance itself. A team coefficient shows direction and size, not cause (`ML Guide.md` §21). | M | conversation, 9 November 2026 |
| User's answer | asked whether to continue on that prediction basis: "Yes" | M | user, 10 November 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 2: prediction or understanding | understand, then confirmed after the explanation | [B SML p. 20] | continue on the prediction basis |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** continue on the prediction basis · stop and recommend a statistical analysis instead
- **Expectation:** n/a
- **Decision:** The work continues as a prediction problem. Chance quality is the predicted probability of a goal. The team question is answered by whether the team improves prediction, not by whether a team causes more goals.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Yes"
- **Supersedes / superseded by:** n/a
- **Links:** n/a

### DR-06 · FORM · step 2 · **superseded**

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** What is predicted, from what, how is success judged, and what must the model provide?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| y | `goal`, binary | M | `Data Summary`; DR-01 |
| x | attributes of the chance at the moment of the shot (13 candidate columns); sub-task 2 adds `team` | M | `Problem Definition` |
| Property 1: output type | binary | M | user agreed the formulation, 9 November 2026 |
| Metric | log-loss; monitored: Brier, ROC-AUC, predicted vs actual goal totals | M | user: "7. Yes." (9 November 2026) |
| Baseline | training goal rate 0.0979 for every shot | M | `Code/outputs/xg/split/split.json` |
| Achievable level | `statsbomb_xg` on the same test shots | M | `Data Summary` |
| Success, sub-task 1 | (LL_baseline − LL_model) ≥ 0.9 × (LL_baseline − LL_StatsBomb) on the test set | M | user: "(b) is good" |
| Success, sub-task 2 | CV margin over the sub-task 1 model ≥ 1 fold spread, and lower test log-loss | M | user: "Do 1. a) Prediction criterion" |
| Property 5: interpretability | sub-task 1 none; sub-task 2 inspectable | M | user: "No. Just for teams." |
| Property 6: probabilities | yes, must-have | M | user: "Property 6 must have." |
| Property 7: extrapolation | no | M | user: "No." |
| Property 8: expected shape | unknown; direction stated | M | user: "Longer distance, lower chance." and "direction only" |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, Property 1: output type = binary | Logistic, k-NN, Tree admissible | [B SML pp. 17, 49–57] | applied in step 4a |
| Must-have Property 6: probabilities = yes | Logistic only | [B→I SML pp. 50, 53–54] | k-NN and Tree will be removed with code `USER` in step 4a |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** metric: log-loss · Brier · misclassification rate · ROC-AUC; sub-task 2 criterion: prediction margin · significance test (outside the four chapters); Property 6: probabilities as must-have · as preference
- **Expectation:** n/a
- **Decision:** y = `goal` (binary) from the attributes of the chance, plus `team` in sub-task 2. Log-loss decides, with the baseline and success criteria above. Probabilities are a must-have, so only logistic regression is compared.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — answers quoted under *Evidence*
- **Supersedes / superseded by:** superseded by DR-11
- **Links:** `Appendix.md` § Problem Definition

### DR-07 · PROP · step 2 · **superseded**

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** What are the property values known before any model is fitted?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | binary | M | DR-06 |
| Property 2: data-to-parameter ratio | sub-task 1: 25,865 / (33 + 1) = 760.7 → ample; sub-task 2: 25,865 / (33 + 97 + 1) = 197.4 → ample | M | counts from `shots_train.csv`: one indicator per level (body part 4, technique 7, play pattern 9, key-pass type 4 including none, team 97 in training) |
| Property 3: number of inputs | sub-task 1: 33 → many; sub-task 2: 130 → many | M | as above |
| Property 4: categorical share | sub-task 1: 11 of 13 columns (85 %) → high; sub-task 2: 12 of 14 (86 %) → high. The 7 true/false flags count as categorical. | M | as above |
| Property 5: interpretability | sub-task 1 none; sub-task 2 inspectable | M | DR-06 |
| Property 6: probabilities | yes, must-have | M | DR-06 |
| Property 7: extrapolation | no | M | DR-06 |
| Property 8: expected shape | unknown | M | DR-06; user: "Longer distance, lower chance." / "direction only" |
| Property 9: separability, Property 10: class imbalance | not yet computed (step 3, training data) | — | — |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property dictionary (§11) | values recorded | [I] | input to the admissible set and prior ranking in step 4 |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Property 2: data-to-parameter ratio, limited | < 10 | 760.7; 197.4 |
| Property 3: number of inputs, many | > 20 | 33; 130 |
| Property 4: categorical share, high | ≥ 50 % | 85 %; 86 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** Properties 1–8 as listed. Properties 2–4 rest on the 13 candidate columns and are provisional: step 3's input design may change them, and the step 3 `PROP` record supersedes this one.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed
- **Supersedes / superseded by:** superseded by DR-12
- **Links:** `Code/outputs/xg/split/shots_train.csv`

### DR-08 · SPLIT · step 2 · **superseded**

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** How are the training and test sets drawn, and is the test set locked?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Grouping | `match_id` | M | DR-03 |
| Source of test data | random by match from 2015/16 | M | DR-04 |
| Test fraction | 20 % of matches | M | user: "3. Sounds good" (10 November 2026) |
| Result | training 1,240 matches, 25,865 shots, 2,533 goals (0.0979); test 311 matches, 6,317 shots, 660 goals (0.1045); no match on both sides (checked by assertion) | M | `Code/outputs/xg/split/split.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 3: grouped or time-ordered rows | group split | [B SML p. 329] | whole matches on one side |
| Test set used once | locked | [B SML pp. 74, 328] | test files kept in `test_locked/`, read only in step 4g |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** random by shot · random by match (chosen) · chronological
- **Expectation:** n/a
- **Decision:** A 20 % test set of whole matches, drawn by `GroupShuffleSplit` with seed 20261110, is set aside and locked.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "3. Sounds good"
- **Supersedes / superseded by:** superseded by DR-10
- **Links:** `Code/xg/04_split.py`, `Code/outputs/xg/split/split.json`

### DR-09 · Admissibility · step 2

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** Where should the test data come from, so that it stands in for future seasons and treats every team alike (Admissibility 4: new cases like these)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Intended use | "New cases will be future seasons" | M | user, DR-02 |
| First split (DR-08) | teams had between 2 and 16 test matches out of 38; Ingolstadt (GER) had both its matches in the test set | M | `split.json` of DR-08; match counts from `shots_clean.csv` |
| User's question | "Could we sample the same number matches for every team?" | M | user, 10 November 2026 |
| Matchweeks | in ENG, ESP and ITA every matchweek has 10 matches and every team plays once per week; in FRA, weeks 14, 23 and 36 have 9 | M | StatsBomb match files, `match_week` |
| GER | open data holds Bayer Leverkusen's 34 matches only; the other 17 teams appear twice each | M | match counts from `shots_clean.csv` |
| User's answer | "Drop GER completely. I accept matchweek idea" | M | user, 10 November 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 4: new cases like these | test data drawn at random by matchweek within each league | [B SML pp. 328–329] | every team has the same number of test matches; future seasons are represented only as far as they resemble 2015/16 |
| Split by group | whole matches stay on one side | [B SML p. 329] | unchanged |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** random by match (DR-04) · random by matchweek, GER in training only · random by matchweek, GER half in test · random by matchweek, GER dropped (chosen)
- **Expectation:** n/a
- **Decision:** The test data are whole matchweeks drawn at random within each league, and the Bundesliga is dropped from the analysis. Balancing the test matches across teams is our choice `[I]`; the book asks only that the split be random and keep groups together.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "Drop GER completely. I accept matchweek idea"
- **Supersedes / superseded by:** supersedes DR-04
- **Links:** `Code/xg/04_split.py`

### DR-10 · SPLIT · step 2

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** How are the training and test sets drawn, and is the test set locked?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Grouping | `match_id`, kept whole by sampling whole matchweeks | M | DR-03, DR-09 |
| Test size | 8 of 38 matchweeks per league (about 21 % of matches; 20 % was agreed, rounded to whole weeks) | M | user: "3. Sounds good" (20 %); DR-09 |
| Weeks drawn | ENG 3, 8, 16, 27, 31, 34, 35, 36; ESP 2, 5, 7, 9, 10, 12, 17, 35; ITA 2, 7, 11, 12, 17, 26, 28, 35; FRA 1, 4, 7, 11, 14, 16, 17, 22 | M | `Code/outputs/xg/split/split.json` |
| Result | training 1,198 matches, 24,816 shots, 2,479 goals (0.0999); test 319 matches, 6,693 shots, 642 goals (0.0959); no match on both sides (checked by assertion) | M | `split.json` |
| Test matches per team | 8 for 78 teams; 7 for Bastia and Gazélec Ajaccio (FRA week 14 has 9 matches) | M | `split.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Admissibility 3: grouped or time-ordered rows | group split | [B SML p. 329] | whole matches on one side |
| Test set used once | locked | [B SML pp. 74, 328] | test files kept in `test_locked/`, read only in step 4g |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** random 20 % of matches (DR-08) · 8 random matchweeks per league (chosen)
- **Expectation:** n/a
- **Decision:** 8 matchweeks per league, drawn with `numpy.random.default_rng(20261111)` in the order ENG, ESP, ITA, FRA, form the test set. It is set aside and locked.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — the matchweek design was accepted (DR-09)
- **Supersedes / superseded by:** supersedes DR-08
- **Links:** `Code/xg/04_split.py`, `Code/outputs/xg/split/split.json`

### DR-11 · FORM · step 2

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** What is predicted, from what, how is success judged, and what must the model provide?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| y | `goal`, binary; Premier League, La Liga, Serie A and Ligue 1 (Bundesliga dropped, DR-09) | M | `Data Summary`; DR-01 |
| x | attributes of the chance at the moment of the shot (13 candidate columns); sub-task 2 adds `team` | M | `Problem Definition` |
| Property 1: output type | binary | M | user agreed the formulation, 9 November 2026 |
| Metric | log-loss; monitored: Brier, ROC-AUC, predicted vs actual goal totals | M | user: "7. Yes." (9 November 2026) |
| Baseline | training goal rate 0.0999 for every shot (2,479 / 24,816, split of DR-10) | M | `Code/outputs/xg/split/split.json` |
| Achievable level | `statsbomb_xg` on the same test shots | M | `Data Summary` |
| Success, sub-task 1 | (LL_baseline − LL_model) ≥ 0.9 × (LL_baseline − LL_StatsBomb) on the test set | M | user: "(b) is good" |
| Success, sub-task 2 | CV margin over the sub-task 1 model ≥ 1 fold spread, and lower test log-loss | M | user: "Do 1. a) Prediction criterion" |
| Property 5: interpretability | sub-task 1 none; sub-task 2 inspectable | M | user: "No. Just for teams." |
| Property 6: probabilities | yes, must-have | M | user: "Property 6 must have." |
| Property 7: extrapolation | no | M | user: "No." |
| Property 8: expected shape | unknown; direction stated | M | user: "Longer distance, lower chance." and "direction only" |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, Property 1: output type = binary | Logistic, k-NN, Tree admissible | [B SML pp. 17, 49–57] | applied in step 4a |
| Must-have Property 6: probabilities = yes | Logistic only | [B→I SML pp. 50, 53–54] | k-NN and Tree will be removed with code `USER` in step 4a |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** metric: log-loss · Brier · misclassification rate · ROC-AUC; sub-task 2 criterion: prediction margin · significance test (outside the four chapters); Property 6: probabilities as must-have · as preference
- **Expectation:** n/a
- **Decision:** y = `goal` (binary) from the attributes of the chance, plus `team` in sub-task 2. Log-loss decides, with the baseline and success criteria above. Probabilities are a must-have, so only logistic regression is compared.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — answers quoted under *Evidence*
- **Supersedes / superseded by:** supersedes DR-06 (same formulation; the baseline value and the leagues changed with the new split)
- **Links:** `Appendix.md` § Problem Definition


### DR-12 · PROP · step 2 · **superseded**

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** What are the property values known before any model is fitted, on the split of DR-10?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | binary | M | DR-11 |
| Property 2: data-to-parameter ratio | sub-task 1: 24,816 / (33 + 1) = 729.9 → ample; sub-task 2: 24,816 / (33 + 78 + 1) = 221.6 → ample | M | counts from `shots_train.csv`: one indicator per level (body part 4, technique 7, play pattern 9, key-pass type 4 including none, team 78 in training) |
| Property 3: number of inputs | sub-task 1: 33 → many; sub-task 2: 111 → many | M | as above |
| Property 4: categorical share | sub-task 1: 11 of 13 columns (85 %) → high; sub-task 2: 12 of 14 (86 %) → high. The 7 true/false flags count as categorical. | M | as above |
| Property 5: interpretability | sub-task 1 none; sub-task 2 inspectable | M | DR-11 |
| Property 6: probabilities | yes, must-have | M | DR-11 |
| Property 7: extrapolation | no | M | DR-11 |
| Property 8: expected shape | unknown | M | DR-11; user: "Longer distance, lower chance." / "direction only" |
| Property 9: separability, Property 10: class imbalance | not yet computed (step 3, training data) | — | — |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property dictionary (§11) | values recorded | [I] | input to the admissible set and prior ranking in step 4 |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Property 2: data-to-parameter ratio, limited | < 10 | 729.9; 221.6 |
| Property 3: number of inputs, many | > 20 | 33; 111 |
| Property 4: categorical share, high | ≥ 50 % | 85 %; 86 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** Properties 1–8 as listed; the values are the same as in DR-07, with the counts recomputed on the new training set. Properties 2–4 rest on the 13 candidate columns and are provisional: step 3's input design may change them, and the step 3 `PROP` record supersedes this one.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed
- **Supersedes / superseded by:** supersedes DR-07; superseded by DR-14
- **Links:** `Code/outputs/xg/split/shots_train.csv`

### DR-13 · FORM · step 3

- **Sub-task:** all
- **Date:** 2026-11-10
- **Question:** Which inputs does the model see (input design, `ML Guide.md` §9)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Candidate columns | 13 attributes of the chance (DR-11) plus the freeze frames | M | `Data Summary` |
| Location | logistic regression adds a contribution per input, so raw `y` can favour one touchline but not the centre over both wings; distance and angle to goal describe the geometry directly | M | geometry of the pitch, not the data |
| User's expectation | "Longer distance, lower chance." (Property 8: expected shape = unknown, direction only) | M | DR-11 |
| Freeze frames | every training shot has exactly one opposing goalkeeper in its frame; frames show a median of 12 players | M | `Data Summary`; assertion in `xg/features.py` |
| Rare flags | `follows_dribble` true for 15 shots, `redirect` for 79 (all shots) | M | `Data Summary` |
| User's answer | to the proposal (distance and angle in place of x and y; opponents in the triangle and goalkeeper distance from the freeze frame; the coded attributes): "drop the rare ones. Otherwise follow your recommendations." | M | user, 10 November 2026 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Input design (§9) | decided with the user, not by cross-validation | [B SML p. 18] | the inputs below enter every configuration |
| REQ-1 | the new inputs are fixed formulas, nothing is fitted | [B SML p. 27] | the same functions apply to the test shots at the final evaluation without leakage |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** x and y · distance and angle (chosen) · both; freeze-frame features: none · opponents in the triangle and goalkeeper distance (chosen) · others (goalkeeper distance from the goal line); rare flags: keep · drop (chosen)
- **Expectation:** n/a
- **Decision:** Sub-task 1 uses 13 inputs: `distance` (to the centre of the goal, pitch units), `angle` (between the lines to the two posts, degrees), `opp_in_triangle` (opponents other than the goalkeeper inside the triangle of shot and posts), `gk_distance` (shot to opposing goalkeeper, pitch units), `body_part`, `technique`, `play_pattern`, `key_pass_type` (with "none" for no assisting pass), `under_pressure`, `first_time`, `one_on_one`, `open_goal` and `aerial_won`. Sub-task 2 adds `team`. Dropped: `x`, `y`, `follows_dribble`, `redirect`.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "drop the rare ones. Otherwise follow your recommendations."
- **Supersedes / superseded by:** supersedes DR-11 for the inputs (x) only; the rest of DR-11 stands
- **Links:** `Code/xg/features.py`, `Code/xg/05_build_inputs.py`, `Code/outputs/xg/inputs_train_summary.md`

### DR-14 · PROP · step 3

- **Sub-task:** 1 and 2
- **Date:** 2026-11-10
- **Question:** What are the property values, with the input design of DR-13 and Properties 9 and 10 computed on the training shots?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | binary | M | DR-11 |
| Property 2: data-to-parameter ratio | sub-task 1: 24,816 / (33 + 1) = 729.9 → ample; sub-task 2: 24,816 / (113 + 1) = 217.7 → ample | M | `Code/outputs/xg/inputs_train_summary.md` |
| Property 3: number of inputs | sub-task 1: 33 encoded → many; sub-task 2: 113 → many | M | as above: 4 numeric, categorical levels 4 + 7 + 9 + 4, 5 boolean; team 80 levels |
| Property 4: categorical share | sub-task 1: 9 of 13 columns (69 %) → high; sub-task 2: 10 of 14 (71 %) → high; booleans counted as categorical | M | as above |
| Property 5: interpretability | sub-task 1 none; sub-task 2 inspectable | M | DR-11 |
| Property 6: probabilities | yes, must-have | M | DR-11 |
| Property 7: extrapolation | no | M | DR-11 |
| Property 8: expected shape | unknown | M | DR-11; user: "Longer distance, lower chance." / "direction only" |
| Property 9: separability | no for both sub-tasks: training accuracy with negligible regularisation (C = 10⁸) 0.9047 (sub-task 1), 0.9057 (sub-task 2) | T | `Code/outputs/xg/core_p9_p10.json` |
| Property 10: class imbalance | imbalanced: goals are 2,479 of 24,816 training shots (9.99 %) | T | `Code/outputs/xg/core_p9_p10.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property dictionary (§11) | values recorded | [I] | inputs to the admissible set and prior ranking in step 4 |
| MOD-1 | does not apply (Property 9: separability = no) | [B SML p. 61] | plain logistic regression stays admissible |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Property 2: data-to-parameter ratio, limited | < 10 | 729.9; 217.7 |
| Property 3: number of inputs, many | > 20 | 33; 113 |
| Property 4: categorical share, high | ≥ 50 % | 69 %; 71 % |
| Property 9: separability | 100 % training accuracy | 90.47 %; 90.57 % |
| Property 10: class imbalance | smallest class < 20 % | 9.99 % |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** Properties 1–10 as listed. The values of Properties 2–4 are unchanged from DR-12; the counts now follow the input design of DR-13 and the correct number of teams (80).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Reference code:** `Code/xg/core.py p9p10`, interim core, not reviewed, SHA-256 `bf1528b047dc192354d9888693993b46c576be7b2556a29d04ffa9a8e9cab4f3`; inputs: `Code/outputs/xg/split/inputs_train.csv` (training shots only); output: `Code/outputs/xg/core_p9_p10.json`, copied above unchanged. The fit for Property 9 establishes a property only; it is not a candidate model.
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "yes" (to computing Properties 9 and 10)
- **Supersedes / superseded by:** supersedes DR-12
- **Links:** `Code/xg/core.py`, `Code/outputs/xg/core_p9_p10.json`, `Code/outputs/xg/inputs_train_summary.md`

### DR-15 · ADMSET · step 4a

- **Sub-task:** 1
- **Date:** 2026-11-10
- **Question:** Which of the 14 configurations are admissible for sub-task 1?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Property 1: output type | binary | M | DR-14 |
| Property 6: probabilities | yes, must-have | M | DR-11, DR-14 |
| Property 5: interpretability | none (sub-task 1) | M | DR-11 |
| Property 9: separability | no | T | DR-14 |
| MOD-2 check | design matrix with intercept: 30 parameters, rank 30 (plain); 38, rank 38 (polynomial terms at degree 3); 24,816 training shots | T | `Code/outputs/xg/core_admset_subtask1.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, Property 1: output type = binary | Logistic, k-NN, Tree admissible | [B SML pp. 17, 49–57] | Linear, Poisson and Exponential configurations removed |
| Must-have Property 6: probabilities = yes | Logistic only | [B→I SML pp. 50, 53–54] | k-NN and Tree removed |
| MOD-1 | does not apply (Property 9: separability = no) | [B SML p. 61] | none |
| MOD-2 | does not apply (parameters < n_train; full rank) | [B→I SML pp. 46–47, 65] | none |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** the 14 structural configurations of §9
- **Expectation:** n/a
- **Decision:** Four configurations are admissible: `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `kNN` | USER | must-have Property 6: probabilities = yes [B→I SML pp. 50, 53–54] |
| `Tree` | USER | must-have Property 6: probabilities = yes [B→I SML pp. 50, 53–54] |

- **Reference code:** `Code/xg/core.py admset --subtask 1`, interim core, not reviewed, SHA-256 `26da0c6637b9a433d2c58f174f06c1bb9f06be7e63730809d3f4b62e4a372f86`; inputs: `Code/xg/inputs/subtask1_props.json` (DR-14 values), training inputs; output: `Code/outputs/xg/core_admset_subtask1.json`, copied above unchanged.
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed
- **Supersedes / superseded by:** n/a
- **Links:** `Code/xg/core.py`, `Code/outputs/xg/core_admset_subtask1.json`

### DR-16 · PRIOR · step 4b

- **Sub-task:** 1
- **Date:** 2026-11-10
- **Question:** How are the admissible configurations ranked before any training, and which are kept for cross-validation?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Properties | as DR-14; Property 8: expected shape = unknown, so no shape entry applies | M, T | DR-14 |
| Admissible set | `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2` | — | DR-15 |
| Ranking | 1 `Logistic` (score 0, 0 add-ons); 2 `Logistic + L2` (0, 1); 3 `Logistic + poly` (−1, 1); 4 `Logistic + poly + L2` (−1, 2) | — | `Code/outputs/xg/core_prior_subtask1.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 3: number of inputs=many→poly | holds | [B→I SML p. 59] | −1 on `Logistic + poly` and `Logistic + poly + L2` |
| §15.3 order | score, then fewer add-ons | [I] | ranking above |
| SEQ-1 | baseline included: the training share of goals for every shot (core interpretation g) | [B SML pp. 330–331] | compared in round 1 |
| SEQ-2 | simple-first = `Logistic` | [B SML p. 331] | compared in round 1 |
| §15.4 keep | simple-first plus the three highest-ranked others | [I] | all four kept |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| §15 number kept besides baseline and simple-first | 3 (plus ties) | 3 others admissible |

- **Options considered:** `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`
- **Expectation:** The cross-validated order follows the prior: `Logistic` and `Logistic + L2` first and indistinguishable, because with about 830 training shots per parameter (24,816 / 30) the tuned penalty should be small and change little; both clearly ahead of the baseline. The two polynomial configurations are marked down by the prior for the number of inputs, but their extra terms apply only to the four numeric inputs (8 more parameters at degree 3), so they are expected to be close to the plain ones rather than clearly worse.
- **Decision:** All four admissible configurations are kept: the baseline and `Logistic` are cross-validated in round 1; `Logistic + L2`, `Logistic + poly` and `Logistic + poly + L2` in round 2.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a (nothing admissible left out) | | |

- **Reference code:** `Code/xg/core.py prior --subtask 1`, interim core, not reviewed, SHA-256 `26da0c6637b9a433d2c58f174f06c1bb9f06be7e63730809d3f4b62e4a372f86`; output: `Code/outputs/xg/core_prior_subtask1.json`, copied above unchanged.
- **Confidence:** n/a
- **Outcome vs expectation:** **partial** (filled in from DR-18). As expected, `Logistic` and `Logistic + L2` are indistinguishable (margin 0.00003) and the tuned penalty is small. Not as expected: the two polynomial configurations are not merely close to the plain ones but ahead of them by about 3.5 times the spread (0.00300, spread 0.00086), so the configurations the prior ranked last lead. The prior marked polynomial terms down for the number of inputs; with the terms applied to only four numeric inputs and ample data, that mark did not anticipate the result.
- **User involvement:** approved — "FRAMEWORK yes to all three" (the method, the core, and the change to the diagnosis errors)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/xg/core.py`, `Code/outputs/xg/core_prior_subtask1.json`

### DR-17 · CV · step 4c

- **Sub-task:** 1
- **Date:** 2026-11-10
- **Question:** Does the simple-first configuration, `Logistic`, clearly beat the baseline (round 1, SEQ-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV round 1 | table below | CV | `Code/outputs/xg/core_cv_round1_subtask1.json` |

**CV table** (log-loss, lower is better; margins in negative log-loss, positive = better; outer 10 / inner 5 folds, StratifiedGroupKFold by match, seed 2026; E_train and E_val in log-loss, the §16 diagnosis error)

| Configuration | Post-prior | Tuned hyperparameters | CV mean log-loss (fold SD) | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic` | no | none (unregularised, no grid) | 0.25896 (0.00600) | leader | +0.06589 (0.00570), C2 clear | 0.25769 | 0.25896 |
| Baseline (training goal share) | no | n/a | 0.32485 (0.00130) | −0.06589 (0.00570) | — | 0.32485 | 0.32485 |

Misclassification at r = 0.5, alongside: `Logistic` E_train 0.0951, E_val 0.0954; baseline 0.0999 and 0.0999. No convergence warnings.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 | `Logistic` clearly beats the baseline | [B SML pp. 331–332] | round 2 may proceed; DX-1 not needed |
| C2 | clear: margin 0.06589 ≥ 1 × spread 0.00570 | [I] | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear over baseline | ≥ 1 × spread | margin / spread = 11.6 |
| §16 outer / inner folds | 10 / 5 | — |

- **Options considered:** n/a
- **Expectation:** n/a (the `PRIOR` expectation is tested in round 2)
- **Decision:** `Logistic` clearly beats the baseline; the remaining kept configurations are cross-validated in round 2 on the same folds.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Reference code:** `Code/xg/core.py cv round1 --subtask 1`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; inputs: DR-14 property values, `inputs_train.csv`; outputs: `Code/outputs/xg/core_cv_round1_subtask1.json` and `core_cv_store_subtask1.json`, copied above unchanged (rounded to 5 decimals).
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed
- **Supersedes / superseded by:** n/a
- **Links:** `Code/xg/core.py`, `Code/outputs/xg/core_cv_round1_subtask1.json`

### DR-18 · CV · step 4d

- **Sub-task:** 1
- **Date:** 2026-11-10
- **Question:** How do the remaining kept configurations compare on the same folds (round 2), and does the result agree with the prior expectation?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV round 2 | table below | CV | `Code/outputs/xg/core_cv_round2_subtask1.json` |

**CV table** (log-loss, lower is better; margins in negative log-loss, positive = better; outer 10 / inner 5 folds, StratifiedGroupKFold by match, seed 2026; E_train and E_val in log-loss)

| Configuration | Post-prior | Tuned hyperparameters (folds) | CV mean log-loss (fold SD) | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic + poly + L2` | no | degree 3, λ = 10⁻⁴ (10/10) | 0.25596 (0.00550) | leader | +0.06889 (0.00524), C2 clear | 0.25443 | 0.25596 |
| `Logistic + poly` | no | degree 3 (10/10) | 0.25597 (0.00531) | −0.00001 (0.00035) | +0.06888 (0.00502), C2 clear | 0.25429 | 0.25597 |
| `Logistic + L2` | no | λ = 10⁻⁴ (10/10) | 0.25893 (0.00597) | −0.00297 (0.00081) | +0.06592 (0.00570), C2 clear | 0.25770 | 0.25893 |
| `Logistic` | no | none | 0.25896 (0.00600) | −0.00300 (0.00086) | +0.06589 (0.00570), C2 clear | 0.25769 | 0.25896 |
| Baseline (training goal share) | no | n/a | 0.32485 (0.00130) | −0.06889 (0.00524) | — | 0.32485 | 0.32485 |

The tuned λ is the smallest value in the grid (10⁻⁴) in every outer fold, for both L2 configurations. No convergence warnings.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Same outer folds as round 1 | checked by the core (stored fold indices) | [I] | margins are fold by fold |
| §15.5 expectation | tested (see `PRIOR` DR-16) | [I] | outcome vs expectation: partial |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear over baseline | ≥ 1 × spread | 13.1, 13.7, 11.6, 11.6 × spread |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** The leading configuration is `Logistic + poly + L2`, indistinguishable from `Logistic + poly`; both are ahead of the configurations without polynomial terms by about 3.5 times the spread. The diagnosis loop (step 4e) starts from the leader.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a (assigned at 4f) | | |

- **Reference code:** `Code/xg/core.py cv round2 --subtask 1`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; outputs: `Code/outputs/xg/core_cv_round2_subtask1.json`, `core_cv_store_subtask1.json`, copied above unchanged (rounded to 5 decimals).
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "yes" (to running round 2)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/xg/core.py`, `Code/outputs/xg/core_cv_round2_subtask1.json`

### DR-19 · DX · step 4e

- **Sub-task:** 1
- **Date:** 2026-11-10
- **Question:** Pass 1: what does the leading configuration, `Logistic + poly + L2`, show, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Leader | `Logistic + poly + L2`: E_train 0.25443, E_val 0.25596, gap 0.00153 (log-loss) | CV | `core_diagnose_Logistic_+_poly_+_L2_subtask1.json` |
| Learning curve | validation log-loss 0.26419 at 10 % of the training matches, 0.25627 at 80 %, 0.25596 at 100 % (fold SD 0.00550) | CV | same file |
| O2 reference | the success criterion on the training shots: baseline 0.32485, StatsBomb xG 0.24973, required log-loss ≤ 0.25724 | T | same file (core interpretation j) |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 clear |
| O2 training error above what is needed | no | training log-loss 0.25443 ≤ 0.25724 |
| O5 hyperparameter at a grid edge | **yes** | λ = 10⁻⁴, the smallest grid value, in 10/10 folds |
| O3 overfitting | no | gap 0.00153 < 2 × 0.25443 |
| O4 underfitting | yes | 0.25443 ≥ 2 × 0.00153 |
| O6 more data likely to help | no | C3 adequate: 80 %→100 % change 0.00031 < 0.5 × 0.00550 |

First that holds: O5 → DX-3, extend the λ grid downwards. The new grid is λ ∈ {10⁻⁸, 10⁻⁷, 10⁻⁶, 10⁻⁵, 10⁻⁴}, degree ∈ {2, 3}; entry `Logistic + poly + L2, λ 1e-8 to 1e-4` (post-prior). Misclassification alongside: O3 no, O4 yes, C3 adequate, the same verdicts.

**Stopping check**

S1 not known before the test set. S2: no. S3: one pass so far. S4: no. S5: no. S6: 1 of 5 passes. None applies; the loop continues.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §18 priority O1 > O2 > O5 > O3 > O4 > O6 | first that holds taken | [I] | one action per pass |
| DX-3 | extend the λ grid in the direction of the edge | [I] | new post-prior CV entry on the same folds |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 / O4 ratios | gap ≥ 2 × E_train / E_train ≥ 2 × gap | see observations |
| O5 grid edge | more than half the outer folds | see observations |
| S3 no-gain passes | 2 passes without a gain of 0.5 × spread | see stopping check |
| C3 learning curve | 80 % − 100 % difference ≥ 0.5 × fold SD | see observations |

- **Options considered:** the actions of §18 for the first observation that holds
- **Expectation:** Smaller λ will be chosen, and the log-loss will not change by as much as 0.5 × spread, because λ = 10⁻⁴ is already a negligible penalty with 24,816 shots.
- **Decision:** Cross-validate `Logistic + poly + L2` with the extended grid on the same folds.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Reference code:** `Code/xg/core.py diagnose` and `cv add`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; outputs copied above unchanged (rounded).
- **Confidence:** n/a
- **Outcome vs expectation:** **partial**. The log-loss did not change: 0.25600 against 0.25596 (difference −0.00004, spread 0.00012). But a smaller λ was not chosen: λ = 10⁻⁴, now the top of the new grid, was chosen in 9 of 10 folds (10⁻⁵ in one), so O5 held again at the opposite edge (DR-20).
- **User involvement:** approved — "yes" (to starting the diagnosis; actions on configurations run without stopping)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_diagnose_Logistic_+_poly_+_L2_subtask1.json`, `core_cv_add_Logistic_+_poly_+_L2,_λ_1e-8_to_1e-4_subtask1.json`

### DR-20 · DX · step 4e

- **Sub-task:** 1
- **Date:** 2026-11-10
- **Question:** Pass 2: λ is now at the upper edge of the extended grid; which action follows, and does a stopping rule apply?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Pass 1 result | `Logistic + poly + L2, λ 1e-8 to 1e-4`: log-loss 0.25600; λ = 10⁻⁴ (the grid's largest value) in 9/10 folds | CV | `core_cv_store_subtask1.json` |
| Pass 2 entry | `Logistic + poly + L2, λ 1e-6 to 1e-2`: λ ∈ {10⁻⁶, 10⁻⁵, 10⁻⁴, 10⁻³, 10⁻²}, degree ∈ {2, 3}; λ = 10⁻⁴ in 9/10 folds, 10⁻⁵ in 1; log-loss 0.25600 (fold SD 0.00552) | CV | same file |
| Pass 2 observations | E_train 0.25441, E_val 0.25600, gap 0.00159; λ at an edge in 0/10 folds; C3 adequate | CV | `core_diagnose_Logistic_+_poly_+_L2,_λ_1e-6_to_1e-2_subtask1.json` |

**Observation → action**

Pass 1 left O5 holding at the upper edge (λ = 10⁻⁴ in 9/10 folds, the largest value of the extended grid). DX-3 again: extend upwards, keeping the previous optimum inside the grid: λ ∈ {10⁻⁶, …, 10⁻²}. On the result:

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 | no | C2 clear |
| O2 | no | training log-loss 0.25441 ≤ 0.25724 |
| O5 | no | λ at an edge in 0/10 folds |
| O3 | no | gap 0.00159 < 2 × 0.25441 |
| O4 | **yes** | 0.25441 ≥ 2 × 0.00159 |
| O6 | no | C3 adequate: 0.00031 < 0.5 × 0.00552 |

The next action would be DX-5 for O4 (more flexibility), but the loop stops first (S3).

**Stopping check**

**S3 applies:** two consecutive passes without a gain of at least 0.5 × spread. Pass 1: −0.00004 against the leader (spread 0.00012). Pass 2: 0.00000 against pass 1 (identical fold scores; the same λ was chosen). The loop stops. For the record, the action S3 pre-empts: DX-5 for O4 offers polynomial terms only if Property 3: number of inputs = few (it is many, and the leader already has them), k-NN or a tree (both removed by the must-have on probabilities), or asking the user for more input variables.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §18 priority O1 > O2 > O5 > O3 > O4 > O6 | first that holds taken | [I] | one action per pass |
| DX-3 | extend the λ grid in the direction of the edge | [I] | new post-prior CV entry on the same folds |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 / O4 ratios | gap ≥ 2 × E_train / E_train ≥ 2 × gap | see observations |
| O5 grid edge | more than half the outer folds | see observations |
| S3 no-gain passes | 2 passes without a gain of 0.5 × spread | see stopping check |
| C3 learning curve | 80 % − 100 % difference ≥ 0.5 × fold SD | see observations |

- **Options considered:** the actions of §18 for the first observation that holds
- **Expectation:** λ = 10⁻⁴ will now be inside the grid and chosen in most folds; no gain.
- **Decision:** Stop the diagnosis loop (S3). The leading configurations go to the recommendation (step 4f).

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Reference code:** `Code/xg/core.py diagnose` and `cv add`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; outputs copied above unchanged (rounded).
- **Confidence:** n/a
- **Outcome vs expectation:** **agree**: λ = 10⁻⁴ chosen in 9/10 folds, now inside the grid; log-loss identical to pass 1.
- **User involvement:** approved — "yes" (to starting the diagnosis; actions on configurations run without stopping)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_diagnose_Logistic_+_poly_+_L2,_λ_1e-6_to_1e-2_subtask1.json`, `core_cv_add_Logistic_+_poly_+_L2,_λ_1e-6_to_1e-2_subtask1.json`

### DR-21 · FINAL · steps 4f–4g

- **Sub-task:** 1
- **Date:** 2026-11-10
- **Question:** Which configuration is recommended for sub-task 1, how confident is the choice, and how does it do on the test set?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV table | six entries: DR-17, DR-18, DR-19, DR-20 | CV | `Code/outputs/xg/core_cv_store_subtask1.json` |
| Recommendation | `Logistic + poly`, degree 3 (chosen in 10/10 outer folds), unregularised | CV | `Code/outputs/xg/core_recommend_subtask1.json` |
| Test result | log-loss 0.24573 on 6,693 test shots (642 goals, 319 matches); baseline 0.31612; StatsBomb xG 0.24010; 92.6 % of StatsBomb's improvement over the baseline | TEST | `Code/outputs/xg/core_final_subtask1.json`; recomputed independently from `core_test_predictions_subtask1.csv` |

**§19 trace**

1. *Eligible* (C2 clear over the baseline): all six entries.
2. *Candidates* (best CV mean, plus margin to it < 0.5 × spread): `Logistic + poly + L2` 0.25596 (best); `Logistic + poly` 0.25597 (margin 0.00001, spread 0.00035); `Logistic + poly + L2, λ 1e-8 to 1e-4` and `…, λ 1e-6 to 1e-2`, both 0.25600 (margin 0.00004, spread 0.00012). Not candidates: `Logistic` and `Logistic + L2` (margins about 0.0030, spread about 0.0008–0.0009).
3. *Choice:* fewest add-ons among the candidates: `Logistic + poly` (1 add-on; the others have 2).
4. *Test once:* refitted on all 24,816 training shots with degree 3; evaluated once on the 6,693 test shots (319 matches, 642 goals), with the user's approval ("Yes.").

**Test-set result**

| | Log-loss | Brier score | ROC-AUC | Predicted goals (actual 642) |
| --- | --- | --- | --- | --- |
| `Logistic + poly` (recommended) | 0.24573 | 0.07044 | 0.8309 | 664.5 |
| Baseline (0.0999 for every shot) | 0.31612 | 0.08674 | 0.5000 | 668.6 |
| StatsBomb xG (reference, not an input) | 0.24010 | 0.06834 | 0.8385 | 642.5 |

- **E_new estimate:** log-loss 0.2457, uncertainty ± 0.0053 (the standard deviation of log-loss across the ten outer folds for this configuration, instructions.md step 4g, [B→I SML pp. 71–73]); n_test = 6,693 shots, 642 goals.
- **Success criterion** (DR-11): (LL_baseline − LL_model) ≥ 0.9 × (LL_baseline − LL_StatsBomb). Improvement of the model 0.07039; of StatsBomb xG 0.07602; ratio 0.926. **Met.**
- **Decision threshold:** none; the probabilities are the product (core interpretation n).
- **Check:** log-loss, the ratio, the Brier score and the predicted-goal total were recomputed from the saved predictions with a separate script, giving the same values.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.1 eligible | all six clear over the baseline | [I] | — |
| §19.2 candidates | four within noise of the best | [I] | — |
| §19.3 fewest add-ons | `Logistic + poly` | [B SML p. 332] + [I] | recommended |
| §17 confidence | Low (C1 none) | [I] | reported with its factors |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| §19 within-noise margin | < 0.5 × spread | 0.00001 / 0.00035; 0.00004 / 0.00012 |
| C1 clear / moderate / none | ≥ 1 / 0.5–1 / < 0.5 × spread | margin −0.00001 vs runner-up `Logistic + poly + L2`, spread 0.00035 → none |
| C2 clear over baseline | ≥ 1 × spread | 0.06888 / 0.00502 = 13.7 |
| C3 learning curve | 80 %→100 % change ≥ 0.5 × fold SD | 0.00040 < 0.5 × 0.00531 → adequate |
| Breadth note | > 10 configurations compared | 6 → does not apply |

- **Options considered:** the six cross-validated entries; all 14 structural configurations (why-not below)
- **Expectation:** n/a
- **Decision:** Recommend `Logistic + poly` (logistic regression with squared and cubed terms of distance, angle, opponents in the triangle and goalkeeper distance; no penalty), to be refitted on all training shots and evaluated once on the test set, with the user's approval.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `kNN` | USER | must-have Property 6: probabilities = yes [B→I SML pp. 50, 53–54] |
| `Tree` | USER | must-have Property 6: probabilities = yes [B→I SML pp. 50, 53–54] |
| `Logistic` | OUTP | margin of the recommendation 0.00298, spread 0.00105 |
| `Logistic + L2` | OUTP | margin 0.00296, spread 0.00102 |
| `Logistic + poly + L2` | SIMP | margin −0.00001, spread 0.00035; 2 add-ons against 1 |

- **Reference code:** `Code/xg/core.py recommend --subtask 1` and `final --subtask 1 --approved "Yes."`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; output `Code/outputs/xg/core_recommend_subtask1.json`, copied above unchanged (rounded).
- **Confidence:** Selection confidence **Low**: C1 = none (the runner-up, `Logistic + poly + L2`, cannot be told apart: margin −0.00001, spread 0.00035), C2 = clear (13.7 × spread over the baseline), C3 = adequate. Rule: Low if C1 is none. Alongside: prior agreement **disagree** (the cross-validation winner among the kept configurations, `Logistic + poly + L2`, was ranked 4th by the prior); grounding of the recommendation's prior score: one entry, `[B→I]` (Property 3: number of inputs=many→poly, −1); breadth note: does not apply (6 configurations compared, 2 of them post-prior).
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "yes" (to running the recommendation); "Yes." (to using the test set)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/xg/core.py`, `Code/outputs/xg/core_recommend_subtask1.json`, `core_final_subtask1.json`, `core_test_predictions_subtask1.csv`, `core_final_model_subtask1.joblib`

### DR-22 · PROP · step 4a

- **Sub-task:** 2
- **Date:** 2026-11-10
- **Question:** What are the property values for sub-task 2, now that the user has said whether inspectability is a must-have?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Properties 1–4, 6–10 | as DR-14, sub-task 2 column: binary; ample (217.7); many (113); high (71 %); probabilities must-have; extrapolation no; shape unknown; not separable (0.9057); imbalanced (9.99 %) | M, T | DR-14 |
| Property 5: interpretability | inspectable, **must-have** | M | user: "must have" (10 November 2026), answering whether reading the team effects is a must-have or a preference |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property dictionary (§11) | values recorded | [I] | inputs to the admissible set and prior ranking for sub-task 2 |
| Must-have Property 5: interpretability = inspectable | gate, not a matrix entry | [B→I SML p. 347] | removes configurations that cannot be inspected; adds no prior score |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** must-have · preference
- **Expectation:** n/a
- **Decision:** Sub-task 2 uses the DR-14 values with Property 5: interpretability = inspectable as a must-have.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Reference code:** n/a (values recorded by the agent from DR-14 and the user's answer; written to `Code/xg/inputs/subtask2_props.json`)
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** asked — "must have"
- **Supersedes / superseded by:** supersedes DR-14 for sub-task 2 only
- **Links:** `Code/xg/inputs/subtask2_props.json`

### DR-23 · ADMSET · step 4a

- **Sub-task:** 2
- **Date:** 2026-11-10
- **Question:** Which of the 14 configurations are admissible for sub-task 2?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Properties | DR-22 | M, T | DR-22 |
| MOD-2 check | design matrix with intercept: 109 parameters, rank 109 (plain); 117, rank 117 (polynomial terms at degree 3); 24,816 training shots | T | `Code/outputs/xg/core_admset_subtask2.json` |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Task gate, Property 1: output type = binary | Logistic, k-NN, Tree admissible | [B SML pp. 17, 49–57] | Linear, Poisson and Exponential configurations removed |
| Must-have Property 5: interpretability = inspectable | Linear, Logistic, GLMs, Tree; k-NN only if "the most similar past cases" is acceptable (not asked: k-NN is removed by Property 6 in any case) | [B→I SML p. 347] | k-NN removed |
| Must-have Property 6: probabilities = yes | Logistic only | [B→I SML pp. 50, 53–54] | k-NN and Tree removed |
| MOD-1 | does not apply | [B SML p. 61] | none |
| MOD-2 | does not apply (parameters < n_train; full rank) | [B→I SML pp. 46–47, 65] | none |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| n/a | | |

- **Options considered:** the 14 structural configurations of §9
- **Expectation:** n/a
- **Decision:** Four configurations are admissible, as in sub-task 1: `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `kNN` | USER | must-have Property 5: interpretability = inspectable [B→I SML p. 347]; must-have Property 6: probabilities = yes [B→I SML pp. 50, 53–54] |
| `Tree` | USER | must-have Property 6: probabilities = yes [B→I SML pp. 50, 53–54] |

- **Reference code:** `Code/xg/core.py admset --subtask 2`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; inputs: `Code/xg/inputs/subtask2_props.json`, training inputs with `team`; output: `Code/outputs/xg/core_admset_subtask2.json`, copied above unchanged.
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_admset_subtask2.json`

### DR-24 · PRIOR · step 4b

- **Sub-task:** 2
- **Date:** 2026-11-10
- **Question:** How are the admissible configurations for sub-task 2 ranked before any training, and which are kept?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Properties | DR-22; Property 5 is a must-have, so its matrix entries do not apply | M, T | DR-22 |
| Ranking | 1 `Logistic` (score 0, 0 add-ons); 2 `Logistic + L2` (0, 1); 3 `Logistic + poly` (−1, 1); 4 `Logistic + poly + L2` (−1, 2) | — | `Code/outputs/xg/core_prior_subtask2.json` |
| Sub-task 1 cross-validation | polynomial terms ahead by 0.0030 (spread about 0.001); the L2 penalty changed nothing | CV | DR-18, DR-21 |

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Property 3: number of inputs=many→poly | holds | [B→I SML p. 59] | −1 on the two polynomial configurations |
| §15.3 order | score, then fewer add-ons | [I] | ranking above |
| SEQ-1, SEQ-2 | baseline and `Logistic` first | [B SML pp. 330–331] | round 1 |
| §15.4 keep | simple-first plus three | [I] | all four kept |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| §15 number kept besides baseline and simple-first | 3 (plus ties) | 3 others admissible |

- **Options considered:** `Logistic`, `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2`
- **Expectation:** The order differs from the prior, as in sub-task 1: the two polynomial configurations ahead of the plain ones by about the same margin (0.003). Unlike sub-task 1, the L2 penalty may help a little: 80 team indicators, many estimated from a few hundred shots each, are where shrinkage can reduce variance (SML p. 60); a tuned λ above the bottom of the grid is expected.
- **Decision:** All four kept: the baseline and `Logistic` in round 1; `Logistic + L2`, `Logistic + poly`, `Logistic + poly + L2` in round 2, on the same outer folds as sub-task 1.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a (nothing admissible left out) | | |

- **Reference code:** `Code/xg/core.py prior --subtask 2`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; output `Code/outputs/xg/core_prior_subtask2.json`, copied above unchanged.
- **Confidence:** n/a
- **Outcome vs expectation:** **partial** (filled in from DR-26). As expected, the polynomial configurations lead the plain ones by about 0.003 (0.00294, spread 0.00105). Not as expected: the L2 penalty did not help. With polynomial terms, λ = 10⁻⁴, the bottom of the grid, was chosen in all ten folds and changed log-loss by less than 0.000001; without them, λ = 10⁻³ was chosen in eight folds, inside the grid, and log-loss was 0.00002 worse than without the penalty.
- **User involvement:** approved — "yes" (method for sub-task 2)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_prior_subtask2.json`

### DR-25 · CV · step 4c

- **Sub-task:** 2
- **Date:** 2026-11-10
- **Question:** Does the simple-first configuration with team, `Logistic`, clearly beat the baseline (round 1, SEQ-3)?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV round 1, sub-task 2 | table below; same outer folds as sub-task 1 (checked: identical fold indices) | CV | `Code/outputs/xg/core_cv_round1_subtask2.json` |

**CV table** (log-loss, lower is better; margins in negative log-loss, positive = better; outer 10 / inner 5 folds, StratifiedGroupKFold by match, seed 2026; E_train and E_val in log-loss)

| Configuration | Post-prior | Tuned hyperparameters | CV mean log-loss (fold SD) | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic` (with team) | no | none | 0.26059 (0.00651) | leader | +0.06426 (0.00615), C2 clear | 0.25529 | 0.26059 |
| Baseline (training goal share) | no | n/a | 0.32485 (0.00130) | −0.06426 (0.00615) | — | 0.32485 | 0.32485 |

For reference, not a rule input: the sub-task 1 `Logistic` (without team) had 0.25896 on the same folds, with E_train 0.25769 (DR-17).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| SEQ-3 | `Logistic` clearly beats the baseline | [B SML pp. 331–332] | round 2 may proceed |
| C2 | clear: 0.06426 ≥ 1 × 0.00615 | [I] | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear over baseline | ≥ 1 × spread | 10.5 |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** `Logistic` with team clearly beats the baseline; round 2 may proceed on the same folds.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Reference code:** `Code/xg/core.py cv round1 --subtask 2`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; outputs `core_cv_round1_subtask2.json`, `core_cv_store_subtask2.json`, copied above unchanged (rounded).
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** informed
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_cv_round1_subtask2.json`

### DR-26 · CV · step 4d

- **Sub-task:** 2
- **Date:** 2026-11-10
- **Question:** How do the remaining kept configurations with team compare on the same folds (round 2), and does the result agree with the prior expectation?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| CV round 2, sub-task 2 | table below | CV | `Code/outputs/xg/core_cv_round2_subtask2.json` |

**CV table** (log-loss, lower is better; margins in negative log-loss, positive = better; outer 10 / inner 5 folds, StratifiedGroupKFold by match, seed 2026; E_train and E_val in log-loss)

| Configuration | Post-prior | Tuned hyperparameters (folds) | CV mean log-loss (fold SD) | Margin vs leader (spread) | Margin vs baseline (spread) | E_train | E_val |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic + poly` | no | degree 3 (10/10) | 0.25765 (0.00582) | leader | +0.06720 (0.00547), C2 clear | 0.25198 | 0.25765 |
| `Logistic + poly + L2` | no | degree 3, λ = 10⁻⁴ (10/10) | 0.25765 (0.00604) | −0.0000005 (0.00039) | +0.06720 (0.00570), C2 clear | 0.25212 | 0.25765 |
| `Logistic` | no | none | 0.26059 (0.00651) | −0.00294 (0.00105) | +0.06426 (0.00615), C2 clear | 0.25529 | 0.26059 |
| `Logistic + L2` | no | λ = 10⁻³ (8/10; 10⁻⁴ in 2) | 0.26061 (0.00628) | −0.00296 (0.00101) | +0.06424 (0.00598), C2 clear | 0.25552 | 0.26061 |
| Baseline (training goal share) | no | n/a | 0.32485 (0.00130) | −0.06720 (0.00547) | — | 0.32485 | 0.32485 |

For reference, not a rule input: the sub-task 1 recommended model, `Logistic + poly` without team, had 0.25597 on the same folds (DR-18). The formal comparison is made by the core at the recommendation (step 4f).

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| Same outer folds as round 1 and as sub-task 1 | checked by the core | [I] | margins are fold by fold |
| §15.5 expectation | tested (see DR-24) | [I] | outcome vs expectation: partial |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| C2 clear over baseline | ≥ 1 × spread | 12.3, 11.8, 10.5, 10.7 × spread |

- **Options considered:** n/a
- **Expectation:** n/a
- **Decision:** The leading configuration is `Logistic + poly`, indistinguishable from `Logistic + poly + L2`; both are ahead of the configurations without polynomial terms by about 2.8 times the spread. The diagnosis loop (step 4e) starts from the leader.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a (assigned at 4f) | | |

- **Reference code:** `Code/xg/core.py cv round2 --subtask 2`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; outputs `core_cv_round2_subtask2.json`, `core_cv_store_subtask2.json`, copied above unchanged (rounded).
- **Confidence:** n/a
- **Outcome vs expectation:** n/a
- **User involvement:** approved — "Go for it!"
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_cv_round2_subtask2.json`

### DR-27 · DX · step 4e

- **Sub-task:** 2
- **Date:** 2026-11-10
- **Question:** Pass 1: what does the leading configuration with team, `Logistic + poly`, show, and which action follows?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Leader | `Logistic + poly` with team: E_train 0.25198, E_val 0.25765, gap 0.00567 (log-loss) | CV | `Code/outputs/xg/core_diagnose_Logistic_+_poly_subtask2.json` |
| Learning curve | held-out log-loss 0.38883 at 10 % of the training matches (fold SD 0.03546), 0.29422 at 20 %, 0.26094 at 50 %, 0.25832 at 80 %, 0.25765 at 100 % (fold SD 0.00582); training log-loss 0.22221 at 10 %, 0.25198 at 100 % | CV | same file |
| O2 reference | required log-loss on the training shots ≤ 0.25724 (baseline 0.32485, StatsBomb xG 0.24973) | T | same file |

**Observation → action**

| Observation | Holds | Test values |
| --- | --- | --- |
| O1 doesn't beat the baseline | no | C2 clear |
| O2 training error above what is needed | no | 0.25198 ≤ 0.25724 |
| O5 hyperparameter at a grid edge | no | no tuned λ; degree exempt (core interpretation k) |
| O3 overfitting | no | gap 0.00567 < 2 × 0.25198 |
| O4 underfitting | **yes** | 0.25198 ≥ 2 × 0.00567 |
| O6 more data likely to help | no | C3 adequate: 80 %→100 % change 0.00067 < 0.5 × 0.00582 |

First that holds: O4 → DX-5, more flexibility. Of its actions: polynomial terms only if Property 3: number of inputs = few (it is many, and the leader already has them); k-NN or a tree (both removed by the must-haves, DR-23); **ask the user whether more input variables exist**, an action that needs the user. DX-9 does not forbid adding flexibility (the gap is not much larger than E_train). Misclassification alongside: O3 no, O4 yes, C3 adequate.

**Stopping check**

S1 not known before the test. S2: no. S3: one pass. S4: no. S5: no. S6: 1 of 5. None applies. The loop pauses for the user's answer on more input variables.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §18 priority | O4 is the first that holds | [I] | DX-5 |
| DX-5 | the only applicable action needs the user | [B SML pp. 333–334] | the loop stops until the user answers |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| O3 / O4 ratios | 2 | gap 0.00567; E_train 0.25198 |
| C3 | 80 %→100 % change ≥ 0.5 × fold SD | 0.00067 against 0.00291 |

- **Options considered:** the DX-5 actions listed above
- **Expectation:** O4 is the first observation, as in sub-task 1; only the user can supply new inputs.
- **Decision:** Ask the user whether more input variables exist.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| n/a | | |

- **Reference code:** `Code/xg/core.py diagnose "Logistic + poly" --subtask 2`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; output copied above unchanged (rounded).
- **Confidence:** n/a
- **Outcome vs expectation:** **agree**: O4 first; its only applicable action needs the user.
- **User involvement:** approved — "yes" (to starting the diagnosis); the question on more input variables is put to the user
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_diagnose_Logistic_+_poly_subtask2.json`

### DR-28 · FINAL · steps 4f–4g

- **Sub-task:** 2
- **Date:** 2026-11-10
- **Question:** Which configuration with team is recommended, how confident is the choice, does it beat the sub-task 1 model in cross-validation, and how does it do on the test set?

**Evidence**

| Item | Value | Tag | Where |
| --- | --- | --- | --- |
| Diagnosis loop | ended by the user after pass 1 ("no. end loop", in answer to whether more input variables exist): S5 | M | DR-27 |
| CV table | four entries: DR-25, DR-26 | CV | `Code/outputs/xg/core_cv_store_subtask2.json` |
| Recommendation | `Logistic + poly` with team, degree 3 (10/10 folds), unregularised | CV | `Code/outputs/xg/core_recommend_subtask2.json` |
| Comparison with sub-task 1 | team model minus sub-task 1 model (`Logistic + poly` without team), fold by fold on the same matches, in negative log-loss: margin −0.00168, spread 0.00117 | CV | same file (core interpretation o) |
| Test result | log-loss 0.24638 on 6,693 test shots (642 goals, 319 matches); sub-task 1 model 0.24573 on the same shots; baseline 0.31612; StatsBomb xG 0.24010 | TEST | `Code/outputs/xg/core_final_subtask2.json`; recomputed independently from the saved predictions |

**§19 trace**

1. *Eligible:* all four entries (C2 clear).
2. *Candidates:* `Logistic + poly` 0.25765 (best); `Logistic + poly + L2` 0.25765 (margin 0.0000005, spread 0.00039). Not candidates: `Logistic`, `Logistic + L2` (margins about 0.0029, spread about 0.001).
3. *Choice:* fewest add-ons: `Logistic + poly`.
4. *Test once:* refitted on all 24,816 training shots; evaluated once on the 6,693 test shots, with the user's approval ("yes.").

**Test-set result**

| | Log-loss | Brier score | ROC-AUC | Predicted goals (actual 642) |
| --- | --- | --- | --- | --- |
| `Logistic + poly` with team (recommended) | 0.24638 | 0.07057 | 0.8290 | 667.0 |
| Sub-task 1 model (`Logistic + poly`, no team) | 0.24573 | 0.07044 | 0.8309 | 664.5 |
| Baseline | 0.31612 | 0.08674 | 0.5000 | 668.6 |
| StatsBomb xG (reference) | 0.24010 | 0.06834 | 0.8385 | 642.5 |

- **E_new estimate:** log-loss 0.2464, uncertainty ± 0.0058 (fold SD of log-loss for this configuration); n_test = 6,693 shots, 642 goals.
- **Success criterion, test part:** the team model must have the lower test log-loss than the sub-task 1 model: 0.24638 against 0.24573, so **not met**. With the cross-validation part also not met, the criterion is **not met**.
- **Check:** the log-loss of both models, the baseline and StatsBomb xG on the test shots were recomputed from the saved predictions with a separate script, giving the same values.

**Success criterion, cross-validation part** (DR-11): the team model must beat the sub-task 1 model by at least 1 × spread. Margin −0.00168 (the team model is worse), spread 0.00117: **not met**. The criterion needs both parts, so it cannot be met whatever the test shows.

**Rules applied**

| Rule | Result | Provenance | Effect |
| --- | --- | --- | --- |
| §19.1–§19.3 | `Logistic + poly` | [B SML p. 332] + [I] | recommended |
| §17 confidence | Low (C1 none) | [I] | reported with its factors |
| Sub-task 2 criterion, CV part | not met | [I] (user's criterion, DR-11) | reported |
| S5 | the user stopped the loop | [I] | — |

**Thresholds applied**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| §19 within noise | < 0.5 × spread | 0.0000005 / 0.00039 |
| C1 | ≥ 1 / 0.5–1 / < 0.5 × spread | 0.0000005 / 0.00039 → none |
| C2 | ≥ 1 × spread | 0.06720 / 0.00547 = 12.3 |
| C3 | 80 %→100 % change ≥ 0.5 × fold SD | 0.00067 < 0.00291 |
| Sub-task 2 criterion, CV part | margin ≥ 1 × spread | −0.00168 against 0.00117 |
| Breadth note | > 10 | 4 |

- **Options considered:** the four cross-validated configurations; all 14 structural configurations (why-not below)
- **Expectation:** n/a
- **Decision:** Recommend `Logistic + poly` with team for sub-task 2. In cross-validation it does not beat the sub-task 1 model without team: it is worse by 0.00168, against a fold-by-fold spread of 0.00117.

**Why not**

| Configuration | Code | Evidence |
| --- | --- | --- |
| `Linear` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Linear + poly + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Poisson + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `Exponential + L2` | EXCL | task gate, Property 1: output type = binary [B SML pp. 17, 49–57] |
| `kNN` | USER | must-haves Property 5: interpretability = inspectable and Property 6: probabilities = yes |
| `Tree` | USER | must-have Property 6: probabilities = yes |
| `Logistic` | OUTP | margin of the recommendation 0.00294, spread 0.00105 |
| `Logistic + L2` | OUTP | 0.00296, spread 0.00101 |
| `Logistic + poly + L2` | SIMP | 0.0000005, spread 0.00039; 2 add-ons against 1 |

- **Reference code:** `Code/xg/core.py recommend --subtask 2` and `final --subtask 2 --approved "yes."`, interim core, not reviewed, SHA-256 `a45bd1384791408b4ab2af6941fb04a4be1356c7c6c67fe48d44ac61416b2806`; output `core_recommend_subtask2.json`, copied above unchanged (rounded).
- **Confidence:** Selection confidence **Low**: C1 none (runner-up `Logistic + poly + L2`, margin 0.0000005, spread 0.00039), C2 clear (12.3 × spread), C3 adequate. Prior agreement: disagree (the prior ranked `Logistic + poly` 3rd). Grounding: [B→I] 1 (Property 3: number of inputs=many→poly, −1). Breadth note: does not apply (4 compared).
- **Outcome vs expectation:** n/a
- **User involvement:** "no. end loop" (loop ended); "yes." (to the figures and to using the test set)
- **Supersedes / superseded by:** n/a
- **Links:** `Code/outputs/xg/core_recommend_subtask2.json`, `core_final_subtask2.json`, `core_test_predictions_subtask2.csv`, `core_final_model_subtask2.joblib`

## Recommendation

### Sub-task 1 — chance quality

**1. Problem.** Predict whether an open-play shot scores (`goal`, Property 1: output type = binary) from 13 attributes of the chance at the moment of the shot: distance and angle to goal, opponents in the triangle and goalkeeper distance from the freeze frame, body part, technique, how the attack started, assisting pass, and five analyst flags (DR-13). Metric: log-loss; monitored: Brier score, ROC-AUC, predicted against actual goals. Baseline: the training share of goals, 0.0999, for every shot. Achievable level: StatsBomb xG on the same test shots. Success: at least 90 % of StatsBomb xG's test improvement in log-loss over the baseline. Must-have: Property 6: probabilities = yes; Property 5: interpretability = none for this sub-task; Property 7: extrapolation = no; Property 8: expected shape = unknown ("Longer distance, lower chance." — direction only). Admissibility: outcome recorded (yes); prediction or understanding (understanding stated, prediction basis confirmed); grouped by match; new cases are future seasons, test data drawn by random matchweek from 2015/16. Split: 8 of 38 matchweeks per league in the test set, seed 20261111; 24,816 training and 6,693 test shots. (DR-01, DR-03, DR-05, DR-09–DR-14)

**2. Recommendation.** `Logistic + poly` with polynomial degree 3 (squared and cubed terms of the four numeric inputs), no penalty. Selection confidence: Low.

**3. Test-set result.** Log-loss = 0.2457 (± 0.0053, fold SD), n_test = 6,693 shots (642 goals, 319 matches); baseline 0.3161; StatsBomb xG 0.2401. Success criterion (≥ 90 % of StatsBomb's improvement): met, 92.6 %. Brier 0.0704 (baseline 0.0867, StatsBomb 0.0683); ROC-AUC 0.831 (StatsBomb 0.838); predicted goals 664.5 against 642. No threshold. (DR-21) Calibration on the test shots, ten equal-size groups (our addition, at the user's request; SML p. 113 places calibration outside the book): highest group predicted 0.423, observed 0.410 (StatsBomb 0.430, 0.430); largest gap in the eighth group, predicted 0.123, observed 0.093 (`figures/fig_calibration_subtask1.csv`).

**4. Why this configuration.**
- Constraints: the task gate for a binary output and the must-have on probabilities leave only logistic regression (SML pp. 17, 49–57; [B→I SML pp. 50, 53–54]); MOD-1 and MOD-2 do not apply (DR-15).
- CV evidence: over `Logistic` 0.00298 (spread 0.00105); over the runner-up `Logistic + poly + L2` −0.00001 (spread 0.00035); over the baseline 0.06888 (spread 0.00502).
- Simplicity: decided by the §19 within-noise step: four candidates within noise of the best; `Logistic + poly` has 1 add-on, the others 2.
- Prior support: one entry, Property 3: number of inputs=many→poly, −1 `[B→I SML p. 59]`: the prior marked this configuration down.

**5. Ranking.**

| Configuration | Prior rank | Prior score | Post-prior | CV mean log-loss | Margin vs recommended (± spread) | Margin vs baseline (± spread) | Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic + poly + L2` | 4 | −1 | no | 0.25596 | +0.00001 (0.00035) | +0.06889 (0.00524) | SIMP |
| `Logistic + poly` | 3 | −1 | no | 0.25597 | — | +0.06888 (0.00502) | recommended |
| `Logistic + poly + L2, λ 1e-8 to 1e-4` | — | −1 | yes | 0.25600 | −0.00003 | clear | (variant) |
| `Logistic + poly + L2, λ 1e-6 to 1e-2` | — | −1 | yes | 0.25600 | −0.00003 | clear | (variant) |
| `Logistic + L2` | 2 | 0 | no | 0.25893 | −0.00296 (0.00102) | +0.06592 (0.00570) | OUTP |
| `Logistic` | 1 | 0 | no | 0.25896 | −0.00298 (0.00105) | +0.06589 (0.00570) | OUTP |
| Baseline | — | — | no | 0.32485 | −0.06888 (0.00502) | — | — |

Margins in negative log-loss, positive = better than the reference. The two post-prior variants are the λ-grid extensions of the diagnosis loop.

**6. Prior versus evidence.** Disagree (post-prior entries excluded): the cross-validation winner among the kept configurations, `Logistic + poly + L2`, was ranked 4th. The departure contradicts the entry Property 3: number of inputs=many→poly (−1, `[B→I SML p. 59]`). It suggests that, with ample data and polynomial terms applied to only four numeric inputs, the number of inputs did not make polynomial terms overfit; the curvature they add in distance, angle and the freeze-frame inputs improved the fit.

**7. Why not the others.**
- EXCL: `Linear`, `Linear + L2`, `Linear + poly`, `Linear + poly + L2`, `Poisson`, `Poisson + L2`, `Exponential`, `Exponential + L2` — task gate, Property 1: output type = binary [B SML pp. 17, 49–57].
- USER: `kNN`, `Tree` — must-have Property 6: probabilities = yes [B→I SML pp. 50, 53–54].
- DISF: none.
- BASE: none.
- OUTP: `Logistic` (margin 0.00298, spread 0.00105); `Logistic + L2` (0.00296, spread 0.00102).
- SIMP: `Logistic + poly + L2` (margin −0.00001, spread 0.00035; 2 add-ons against 1).

Flags: none.

**8. Confidence.** Selection confidence Low: C1 none (runner-up `Logistic + poly + L2`, margin −0.00001, spread 0.00035), C2 clear (13.7 × spread), C3 adequate (80 %→100 % change 0.00040 < 0.5 × 0.00531); rule: Low if C1 is none. Prior agreement: disagree. Grounding: [B] 0 · [B→I] 1 · [I] 0. Breadth note: does not apply (6 configurations compared).

**9. How the model predicts.** The model adds up a contribution from each input on the log-odds scale and turns the sum into a probability with the logistic function (SML pp. 49–55). Each numeric input contributes through itself, its square and its cube, so its effect is a curve rather than a straight line; per §21, individual polynomial coefficients are hard to read on their own, and the effect of each numeric input is best shown as a prediction curve over its range. The categorical inputs and flags each shift the log-odds by a fixed amount. The coefficients describe associations in this data, not causes.

**10. Use and limits.** The estimate (log-loss 0.2457 ± 0.0053) is an average over shots like the test shots: open play, not assisted directly from a restart, in four men's leagues in 2015/16. It says nothing about the worst individual prediction (SML p. 347), and it holds for future seasons only as far as they resemble 2015/16 (DR-09). The model is not fitted to shots from the shooter's own half or to set pieces. The freeze frames show only the players the analyst recorded.

**11. Improvement history.** Pass 1: O5 (λ = 10⁻⁴, the bottom of the grid, in 10/10 folds) → DX-3, grid extended to 10⁻⁸ → no gain (−0.00004, spread 0.00012); λ = 10⁻⁴ at the new top in 9/10 folds. Pass 2: O5 at the upper edge → DX-3, grid 10⁻⁶ to 10⁻² → no gain; λ inside the grid. O4 (E_train ≥ 2 × gap in log-loss) held in both passes; its action was not reached. Stopped by S3. (DR-19, DR-20)

**12. Thresholds applied.**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Property 2: data-to-parameter ratio, limited | < 10 | 729.9 |
| Property 3: number of inputs, many | > 20 | 33 |
| Property 4: categorical share, high | ≥ 50 % | 69 % |
| Property 9: separability | 100 % training accuracy | 90.47 % |
| Property 10: class imbalance | smallest class < 20 % | 9.99 % |
| §15 kept besides baseline and simple-first | 3 | 3 |
| §16 outer / inner folds | 10 / 5 | — |
| C1 | ≥ 1 / 0.5–1 / < 0.5 × spread | −0.00001 / 0.00035 |
| C2 | ≥ 1 × spread | 13.7 |
| C3 | ≥ 0.5 × fold SD | 0.00040 against 0.00266 |
| §19 within noise | < 0.5 × spread | 0.00001 / 0.00035; 0.00004 / 0.00012 |
| O3 / O4 | ratio 2 | gap 0.00153–0.00159; E_train 0.2544 |
| O5 | more than half the folds | 10/10, 9/10, 0/10 |
| S3 | 2 passes without a gain of 0.5 × spread | 2 |
| Success | 90 % of StatsBomb's improvement | 92.6 % |

**13. Trace and provenance.** DRs: DR-01–DR-05 (Admissibility, DR-04 superseded), DR-06 and DR-11 (FORM, DR-06 superseded), DR-13 (FORM, input design), DR-07, DR-12, DR-14 (PROP, the first two superseded), DR-08, DR-10 (SPLIT, DR-08 superseded), DR-15 (ADMSET), DR-16 (PRIOR), DR-17, DR-18 (CV), DR-19, DR-20 (DX), DR-21 (FINAL). Rules and entries used, counted by script from the *Rules applied* tables of DR-01 to DR-21, superseded records included (42 rows): [B] 22 · [B→I] 5 · [I] 16 · UNLISTED 0.


### Sub-task 2 — team

**1. Problem.** As sub-task 1, with the shooting `team` (80 teams) added as an input; Property 5: interpretability = inspectable as a must-have, so that each team's effect can be read (DR-22). Success: the team model beats the sub-task 1 model on cross-validated log-loss by at least one fold-by-fold spread, and has the lower test log-loss (DR-11). Same split and folds as sub-task 1. (DR-11, DR-13, DR-22)

**2. Recommendation.** `Logistic + poly` with team, polynomial degree 3, no penalty. Selection confidence: Low.

**3. Test-set result.** Log-loss = 0.2464 (± 0.0058, fold SD), n_test = 6,693 shots (642 goals); sub-task 1 model 0.2457, baseline 0.3161, StatsBomb xG 0.2401. Success criterion: not met. Cross-validation part: the team model is worse than the sub-task 1 model by 0.00168 (spread 0.00117); test part: 0.24638 against 0.24573. No threshold. (DR-28)

**4. Why this configuration.**
- Constraints: binary output and the must-haves on probabilities and inspectability leave logistic regression only (DR-23).
- CV evidence: over `Logistic` 0.00294 (spread 0.00105); over the runner-up `Logistic + poly + L2` 0.0000005 (spread 0.00039); over the baseline 0.06720 (spread 0.00547).
- Simplicity: decided by the §19 within-noise step (1 add-on against 2).
- Prior support: Property 3: number of inputs=many→poly, −1 `[B→I SML p. 59]`.

**5. Ranking.**

| Configuration | Prior rank | Prior score | Post-prior | CV mean log-loss | Margin vs recommended (± spread) | Margin vs baseline (± spread) | Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Logistic + poly` | 3 | −1 | no | 0.25765 | — | +0.06720 (0.00547) | recommended |
| `Logistic + poly + L2` | 4 | −1 | no | 0.25765 | −0.0000005 (0.00039) | +0.06720 (0.00570) | SIMP |
| `Logistic` | 1 | 0 | no | 0.26059 | −0.00294 (0.00105) | +0.06426 (0.00615) | OUTP |
| `Logistic + L2` | 2 | 0 | no | 0.26061 | −0.00296 (0.00101) | +0.06424 (0.00598) | OUTP |
| Baseline | — | — | no | 0.32485 | −0.06720 (0.00547) | — | — |

**6. Prior versus evidence.** Disagree: the winner, `Logistic + poly`, was ranked 3rd. As in sub-task 1, the departure contradicts Property 3: number of inputs=many→poly (−1, `[B→I SML p. 59]`). The expectation that the L2 penalty would help the team coefficients was not borne out (DR-24).

**7. Why not the others.**
- EXCL: the eight Linear, Poisson and Exponential configurations — task gate, Property 1: output type = binary [B SML pp. 17, 49–57].
- USER: `kNN` (must-haves on inspectability and probabilities), `Tree` (must-have on probabilities).
- DISF, BASE: none.
- OUTP: `Logistic` (0.00294, spread 0.00105); `Logistic + L2` (0.00296, spread 0.00101).
- SIMP: `Logistic + poly + L2` (0.0000005, spread 0.00039; 2 add-ons against 1).

Flags: none.

**8. Confidence.** Selection confidence Low: C1 none, C2 clear (12.3 × spread), C3 adequate (0.00067 < 0.5 × 0.00582); rule: Low if C1 is none. Prior agreement: disagree. Grounding: [B] 0 · [B→I] 1 · [I] 0. Breadth note: does not apply (4 compared).

**9. How the model predicts.** As sub-task 1, plus one coefficient per team on the log-odds scale, relative to a reference team (the first in alphabetical order), which shifts the predicted probability of all that team's shots by the same amount on that scale. The coefficients describe associations in this data, not causes; with the team model not predicting better than the model without it, the individual team coefficients are not reported as findings.

**10. Use and limits.** The cross-validation and test results say that, with these inputs and one season of data, knowing the team did not improve predictions for new shots. They do not show that teams do not differ in finishing: the learning curve with the team was still falling (more steeply at small sizes than without it), and a classical test of team differences is outside the four chapters (DR-11).

**11. Improvement history.** Pass 1: O4 (E_train 0.25198 ≥ 2 × gap 0.00567) → DX-5; its only applicable action, asking for more input variables, needed the user, who answered that there are none and ended the loop (S5). (DR-27)

**12. Thresholds applied.**

| Threshold | Value used | Value compared |
| --- | --- | --- |
| Property 2: data-to-parameter ratio, limited | < 10 | 217.7 |
| Property 3: number of inputs, many | > 20 | 113 |
| Property 4: categorical share, high | ≥ 50 % | 71 % |
| Property 9: separability | 100 % | 90.57 % |
| Property 10: class imbalance | < 20 % | 9.99 % |
| C1 | ≥ 1 / 0.5–1 / < 0.5 × spread | 0.0000005 / 0.00039 |
| C2 | ≥ 1 × spread | 12.3 |
| C3 | ≥ 0.5 × fold SD | 0.00067 against 0.00291 |
| §19 within noise | < 0.5 × spread | 0.0000005 / 0.00039 |
| O3 / O4 | ratio 2 | gap 0.00567; E_train 0.25198 |
| Sub-task 2 criterion, CV part | margin ≥ 1 × spread | −0.00168 against 0.00117 |

**13. Trace and provenance.** DRs: DR-01–DR-05 (Admissibility), DR-11 (FORM), DR-13 (FORM, inputs), DR-14 and DR-22 (PROP), DR-10 (SPLIT), DR-23 (ADMSET), DR-24 (PRIOR), DR-25, DR-26 (CV), DR-27 (DX), DR-28 (FINAL); superseded records DR-04, DR-06–DR-08, DR-12 included in the count. Rules and entries used, counted by script from the *Rules applied* tables of DR-01–DR-14 and DR-22–DR-28 (42 rows): [B] 22 · [B→I] 7 · [I] 14 · UNLISTED 0.

## Analysis Log

*A numbered row per step taken, added as the work happens. What was done, what it changed, and where the output is. Superseded decisions stay, marked as such — a reader cannot judge a choice without seeing the alternatives. A row that involved a decision names its Decision Record IDs.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Step 1. Looked for shot data in `xT_Model_comparison`. That folder holds code and results only; its shot tables (`../data`) are not on disk. | — |
| 2 | Step 1. Analysis folder `Demonstration/xG/` created from the templates. Downloaded StatsBomb open data for 2015/16 (5 leagues, 1,551 matches, commit `4b73468`) and extracted the open-play shots, as the user asked: no penalties, no direct free kicks, no direct corners: 36,508 shots. Superseded by row 3. | `Attachments/statsbomb-open-data-2015-16/`, `Code/outputs/xg/` |
| 3 | Step 1. At the user's request, also excluded open-play shots whose key pass is a corner (2,606 shots). Kept: 33,902 shots, 3,340 goals (before: 36,508 and 3,533). Added a `key_pass_type` column. Superseded by row 4. | `Code/outputs/xg/` |
| 4 | Step 1. At the user's request, also excluded open-play shots whose key pass is a free kick (1,387 shots). Kept: 32,515 shots, 3,217 goals (before: 33,902 and 3,340). Superseded by row 5. | `Code/outputs/xg/` |
| 5 | Step 1. At the user's request, also excluded open-play shots whose key pass is a throw-in (240 shots). Kept: 32,275 shots, 3,204 goals (before: 32,515 and 3,217). Superseded by row 6. | `Code/outputs/xg/` |
| 6 | Step 1. At the user's request, also excluded open-play shots whose key pass is a goal kick (15) or a kick-off (4). Kept: 32,256 shots, 3,203 goals (before: 32,275 and 3,204). Shot scope settled. | `Code/outputs/xg/` |
| 7 | Step 1. Describing pass on the shot table: columns, units, coverage, missing values, oddities and the machine learning checks. Nothing changed in the data. Units were checked in StatsBomb's *Open Data Events v4.0.0* documentation, read as extracted text, so the coordinate diagram in its Appendix 2 was not read. | `Code/outputs/xg/describe_shots.md` |
| 8 | Step 1. The user set the target and the columns kept out as leakage: `goal` is the target; `outcome`, `end_x/y/z`, `duration`, `deflected` and `statsbomb_xg` are never inputs. | `Data Summary`, Step 1 decisions |
| 9 | Step 1. Concept explained in conversation: the admissibility questions (`ML Guide.md` §10), then called ADM-1 to ADM-4. | — |
| 10 | `FRAMEWORK` change (commit `f117f48`): the admissibility checks were renamed *Admissibility 1–4*, each with a short name, and the record type `ADM` became `Admissibility`. No admissibility answer had been recorded yet, so nothing in this analysis is superseded. | `instructions.md`, `ML Guide.md` |
| 11 | Step 1. Admissibility 1: outcome recorded answered yes (DR-01). Admissibility 4: new cases like these answered "New cases will be future seasons" (DR-02); where the validation and test data should come from is still to be agreed. The user asked whether a team factor could be used; that is a choice of inputs, discussed in conversation and not yet decided. | DR-01, DR-02 |
| 12 | Step 1. Admissibility 3: grouped by `match_id`, not a time series (DR-03). Validation and test data drawn at random by match (DR-04). User's experience with machine learning recorded as "reasonable". | DR-03, DR-04 |
| 13 | Step 1. At the user's request, the oddities were removed: 74 shots (10 goals), namely 1 with a 1,746.6 s duration, 41 from the shooter's own half and 32 with no opposing goalkeeper in the frame. Two team names were harmonised (189 shots). Before: 32,256 shots, 3,203 goals. After: 32,182 shots, 3,193 goals. The Data Summary description was redone for the cleaned table, and every count in it was updated. | `Code/outputs/xg/shots_clean.csv`, `clean_log.txt`, `describe_shots_clean.md` |
| 14 | Step 1. Asked whether a fuller form of the data exists (StatsBomb 360, later seasons). The user decided this download is the data used; neither was checked. Step 1 closed. | `Data Summary`, Provenance |
| 15 | Step 2 started. The user stated the problem: chance quality, and whether teams differ given the same chance. Admissibility 2: prediction or understanding — understanding was stated, then the prediction basis was confirmed after the explanation (DR-05). Agreed so far: two sub-tasks (1: chance attributes only; 2: plus team), the deciding metric (log-loss), Property 5: interpretability (inspectable for the team question only), Property 7: extrapolation = no, and Property 8: expected shape in the user's words: "Longer distance, lower chance." Still open: the success criteria, which are raised with the user. | DR-05 |
| 16 | `FRAMEWORK` change (commit `879affb`): book pages are written `SML p. x` / `SML pp. x–y` everywhere. Applied to this Appendix: 4 provenance tags rewritten, no page numbers changed. | `instructions.md`, `ML Guide.md` |
| 17 | Step 2. Success criteria chosen by the user. Sub-task 1: the model's improvement in test log-loss over the baseline is at least 90 % of StatsBomb xG's improvement on the same test shots ("(b) is good"). Sub-task 2: the prediction criterion, not a significance test ("Do 1. a)"): the model with team beats the model without team on cross-validated log-loss by more than the fold spread, and the test set agrees. A significance test of team coefficients was considered and not used: it is outside the four chapters. The user asked about XGBoost; it is boosting, from chapter 8, and outside the solution space (`ML Guide.md` §23). | — |
| 18 | `FRAMEWORK` change (commit `c100768`): properties are written *Property n: short name* (previously P1–P10), checks always carry their short name, and `Criteria.md` lists both for the user. Applied to this Appendix; no decision changed. | `instructions.md`, `ML Guide.md`, `Criteria.md` |
| 19 | `FRAMEWORK` change: `Criteria.md` renamed `Glossary.md`. | `Glossary.md` |
| 20 | Step 2. The user set Property 6: probabilities as a must-have, Property 8: expected shape as a direction only (shape unknown), and the test fraction at 20 %. Formulation recorded (DR-06); Properties 1–8 recorded (DR-07; Properties 2–4 provisional until the step 3 input design); split by match with seed 20261110 and the test set locked (DR-08). | DR-06, DR-07, DR-08; `Code/outputs/xg/split/` |
| 21 | Step 2. Problem and sub-tasks written into the `Introduction` of `Report.md`. | `Report.md` |
| 22 | Step 2. The first split (DR-08) gave teams between 2 and 16 test matches each, and put both of Ingolstadt's matches in the test set. At the user's request, the Bundesliga was dropped completely (674 shots, 72 goals, 34 matches) and the test set was redrawn as 8 random matchweeks per league (DR-09, DR-10). Nothing had been fitted and no test result had been seen. Before: 32,182 shots; training 25,865 shots (2,533 goals, 0.0979), test 6,317 (660, 0.1045). After: 31,509 shots; training 24,816 (2,479, 0.0999), test 6,693 (642, 0.0959). Cleaning now removes 73 shots (31 without a goalkeeper in the frame, previously 32). The Data Summary description, the Problem Definition and the Introduction were updated; DR-06 and DR-07 were superseded by DR-11 and DR-12 with the new counts. | DR-09–DR-12; `Code/outputs/xg/split/split.json`, `clean_log.txt` |
| 23 | `FRAMEWORK` change (commit `a6226c3`): a draft `Abstract` goes into `Report.md` from the end of step 1 and is rewritten at the end of every step; the `Methods` paragraph is drafted at step 4b and made final at 4h, with anything not used removed. Applied here: an `Abstract` section was added to `Report.md`, with a draft covering steps 1 and 2. | `Report.md` |
| 24 | `FRAMEWORK` change (commit `aa07116`): the analysis in progress is written at the root. This analysis's report and appendix moved from `Demonstration/xG/` to the root `Project Report.md` and `Appendix.md`; `Demonstration/xG/` was removed and is recreated when the analysis is submitted. Links were updated; no content changed. | `Project Report.md`, `Appendix.md` |
| 25 | Step 2 closed by the user (10 November 2026). Left open, to be settled where they belong: the choice of inputs (step 3), and whether Property 5: interpretability for sub-task 2 is a must-have or a preference (no practical effect, because Property 6: probabilities as a must-have already limits the comparison to logistic regression). The draft `Abstract` already covers step 2. | — |
| 26 | `FRAMEWORK` change (commit `0e78355`): `Methods` opens with `Data and evaluation`, written at the end of step 2. Applied here: `Data and evaluation` written in `Project Report.md` from the Data Summary and DR-09–DR-12. The `Introduction` was trimmed to the question and the approach; the details it held (31,509 shots, log-loss, the matchweek split) moved to `Data and evaluation`. | `Project Report.md` |
| 27 | Step 3 started. | — |
| 28 | Step 3. Input design agreed with the user (DR-13): distance and angle replace x and y; opponents in the triangle and goalkeeper distance from the freeze frames; the coded attributes, without the rare `follows_dribble` and `redirect`. Inputs built for the training shots only. Encoded inputs: 33 for sub-task 1, 113 for sub-task 2. | DR-13; `Code/outputs/xg/split/inputs_train.csv`, `inputs_train_summary.md` |
| 29 | Step 3. Correction: DR-12 counted 78 teams in training; there are 80 (four leagues of 20). Sub-task 2 then has 33 + 80 = 113 encoded inputs and a ratio of 24,816 / 114 = 217.7, not 111 and 221.6. Property 2 (ample) and Property 3 (many) are unchanged. DR-12 stays as written and is superseded by the step 3 `PROP` record. | DR-12 |
| 30 | Step 3. Interim core started (`Code/xg/core.py`), with only §11 (Property 9: separability, Property 10: class imbalance). Shown to the user before it is run. The rest of the core is added before step 4b, where the user approves the whole script. | `Code/xg/core.py` |
| 31 | Step 3. Concept explained in conversation: what the book says about class imbalance (SML pp. 53–54, 91–93), and how it applies when the deciding metric is log-loss. | — |
| 32 | Step 3. Under the new `FRAMEWORK` rule (commit `7374d79`), the book was opened (2nd edition draft of 1 September 2026, smlbook.org) to check the answers given about imbalance and log-loss. *Imbalance:* the book defines imbalanced and asymmetric problems (SML pp. 54, 91), warns that the misclassification rate and the ROC curve can mislead, and recommends F1, F_β and the precision–recall curve (SML pp. 91–92); it gives no numeric threshold, so the 20 % in Property 10 is ours, as the guide says. *Log-loss:* the book trains logistic regression by minimising the cross-entropy (SML pp. 52–53) and separates the error function used for evaluation from the training loss, with misclassification and squared error as defaults among "many possible error functions" (SML p. 67); chapter 4 does not propose cross-entropy as an error function. Chapter 5, outside the four chapters, shows the cross-entropy is minimised by the true class probability (SML p. 112) and calls evaluating calibration beyond the book's scope (SML p. 113). The guide agrees with the book. The tag on the metric in the Problem Definition was corrected from `[I]` to `[B→I SML pp. 52–53, 67, 330]`; no decision changed. | `Problem Definition` |
| 33 | `FRAMEWORK` change (commit `8061a8f`): the book is kept locally in `Attachments/smlbook/`, git-ignored. The copy downloaded for row 32 was moved there: `sml-book-2nd-edition-draft-latest.pdf`, draft of 1 September 2026 (the version named in `ML Guide.md`), SHA-256 `4afca16e…1fe51`, with its extracted text for searching. | `Attachments/smlbook/` |
| 34 | `FRAMEWORK` change (commit `cae72bf`): requests and reports say in plain words what an action does, what it uses, what comes out and why, not workspace shorthand such as "run the core". `Glossary.md` gains entries for the core and Decision Records. | — |
| 35 | Step 3. Properties 9 and 10 computed by the interim core on the training shots, with the user's approval: not separable (training accuracy 90.47 % and 90.57 % with negligible regularisation), imbalanced (goals 9.99 %). New properties record DR-14 supersedes DR-12. | DR-14; `Code/outputs/xg/core_p9_p10.json` |
| 36 | `FRAMEWORK` change (commit `9b864b3`): every framework change is summarised in `Davids Changes.md`, for Florentine; the file was written for all changes made so far. | `Davids Changes.md` |
| 37 | Step 3. Figures 1–3 proposed and agreed ("All of them."), drawn from the training shots in light and dark variants, and added to `Results` under *The training data* with captions. Figure 1's legend reads "All shots", because goals are shots too; Figure 2's tick at 40 was dropped where it collided with "40+"; Figure 3's axis was narrowed to 0–0.5 and its labels put in sentence case. | `Code/outputs/xg/figures/`; `Project Report.md` |
| 38 | `FRAMEWORK` change (commit `bced066`): files are changed with scripts, not with the editor tools that show a diff box in the conversation; answers say which files changed. | — |
| 39 | Step 3. The user dropped Figure 3 (goal share by type of shot) from the report; its script and image stay in `Code/`. No figure is made for sub-task 2 ("No figure required for task 2."). The `Results` text now refers to Figures 1 and 2. | `Project Report.md` |
| 40 | Step 3 closed by the user (10 November 2026). Draft `Abstract` updated with the inputs chosen in step 3. | `Project Report.md` |
| 41 | `FRAMEWORK` change (commit `e8a0cc8`): plans and methods are presented with the book pages behind each part, checked in the local copy, and with our own parts marked. The step 4 overview was given again in that form. | — |
| 42 | Step 4 started, sub-task 1. The interim core was completed (`Code/xg/core.py`, SHA-256 `26da0c66…`): admissible set, prior ranking, nested cross-validation by match, diagnosis, recommendation and the single test evaluation, with its interpretations listed at the top of the file. Properties 9 and 10 were recomputed with the completed core: identical values (training accuracy 0.9047 and 0.9057; goals 9.99 %), so DR-14 stands. | `Code/xg/core.py` |
| 43 | Step 4a, sub-task 1: four logistic configurations admissible (DR-15). Step 4b: prior ranking; all four kept (DR-16). Presented to the user for agreement with the cross-validation protocol and the core; nothing cross-validated yet. | DR-15, DR-16 |
| 44 | Step 4b, sub-task 1. The user agreed the method and approved the core ("FRAMEWORK yes to all three"), including a `FRAMEWORK` change raised by the agent: §16 diagnosis errors use log-loss, the agreed metric, instead of the misclassification rate, which is near-constant when goals are 10 % of shots (guide commit `670f1f1`, `Davids Changes.md` entry 13). The core was updated accordingly (interpretations i and l) and is now SHA-256 `a45bd138…`; the admissible set and prior ranking were re-run with it and are identical, so DR-15 and DR-16 stand. The user-involvement field of DR-16 was filled in. | `Code/xg/core.py`; DR-15, DR-16 |
| 45 | Step 4b, sub-task 1. `Methods` paragraph drafted in `Project Report.md`, before any cross-validation. | `Project Report.md` |
| 46 | Step 4c, sub-task 1, round 1: `Logistic` cross-validated log-loss 0.25896 (fold SD 0.00600) against the baseline's 0.32485; margin 0.06589, spread 0.00570, clearly better (DR-17). | DR-17 |
| 47 | Step 4d, sub-task 1, round 2 (DR-18): `Logistic + poly + L2` 0.25596 and `Logistic + poly` 0.25597 lead, indistinguishable from each other; `Logistic + L2` 0.25893 and `Logistic` 0.25896 trail by 0.0030 (spread 0.0008–0.0009). Tuned λ at the bottom of its grid in all folds. The prior's expectation is met in part (DR-16). | DR-18, DR-16 |
| 48 | Step 4e, sub-task 1, diagnosis loop. Pass 1 (DR-19): λ at the bottom of its grid in all folds (O5), so the grid was extended down to 10⁻⁸; λ = 10⁻⁴ was still chosen, now at the top, with no change in log-loss. Pass 2 (DR-20): grid centred on 10⁻⁴ (10⁻⁶ to 10⁻²); λ = 10⁻⁴ inside the grid, no gain. Stopped by S3 (two passes without gain). O4 (underfitting by the §18 ratio) holds throughout; its action was not reached. Two post-prior entries added to the CV store. | DR-19, DR-20 |
| 49 | Step 4f, sub-task 1: recommendation rule applied (DR-21). `Logistic + poly`, degree 3, unregularised; selection confidence Low (C1 none against `Logistic + poly + L2`; C2 clear; C3 adequate); prior agreement disagree. Test-set use put to the user. | DR-21 |
| 50 | `FRAMEWORK` change (commit `242070d`, `Davids Changes.md` entry 14): the model selection is written up (new step 4f′) before the user is asked about the test set. | `instructions.md` |
| 51 | Step 4f′, sub-task 1. `Methods` checked against what was done before the test: unchanged, because the diagnosis passes (DR-19, DR-20) changed nothing reported and stay in this Appendix. First `Results` paragraph written, with Figure 3 (comparison of the models in cross-validation: log-loss ± fold SD, and fold-by-fold differences from the recommended model) and Figure 4 (learning curve of the recommended model). Figure 3 gained a right-hand panel beyond the proposal: with fold SDs of about 0.006, plain error bars would hide the 0.003 difference that the fold-by-fold comparison shows (spread 0.001). Figure 4 omits the baseline line proposed, because at 0.325 it would compress the two curves into a fifth of the height; the baseline's value is in the text of Figure 3. Every number comes from `core_cv_round2_subtask1.json` and `core_recommend_subtask1.json`. | `Project Report.md`; `Code/outputs/xg/figures/` |
| 52 | Step 4g, sub-task 1: the single test evaluation, approved by the user ("Yes."). `Logistic + poly` test log-loss 0.24573 (± 0.00531), baseline 0.31612, StatsBomb xG 0.24010; 92.6 % of StatsBomb's improvement, so the success criterion is met. Recomputed from the saved predictions with a separate script: identical. DR-21 completed. The test set is not used again for sub-task 1. | DR-21; `core_final_subtask1.json` |
| 53 | Step 4h, sub-task 1: Recommendation Report assembled in `Recommendation`; test-result paragraph added to `Results` after the 4f′ paragraph, which was not changed; `Methods` checked, unchanged; draft `Abstract` updated. | `Appendix.md`, `Project Report.md` |
| 54 | Step 4h, sub-task 1, at the user's request ("Lets add a callibration curve anyway"): Figure 5, a calibration curve on the test shots (ten equal-size groups by predicted probability; the model and StatsBomb xG), drawn from the saved test predictions without refitting or re-evaluating. Marked in `Methods` as our addition, since the book places the evaluation of calibration outside its scope (SML p. 113). `Methods` gained one sentence after the test for it. Sub-task 1 closed by the user ("Otherwise complete."). | `Project Report.md`; `figures/fig_calibration_subtask1.csv` |
| 55 | Sub-task 2 started. The user made Property 5: interpretability a must-have ("must have"; DR-22). Step 4a: four logistic configurations admissible, as in sub-task 1 (DR-23). Step 4b: prior ranking identical to sub-task 1, all four kept (DR-24). Presented for agreement; nothing cross-validated. | DR-22–DR-24 |
| 56 | Step 4b, sub-task 2: method agreed ("yes"); `Methods` paragraph for sub-task 2 drafted before any cross-validation. | `Project Report.md` |
| 57 | Step 4c, sub-task 2, round 1 (DR-25): `Logistic` with team 0.26059 (fold SD 0.00651) against the baseline's 0.32485, clearly better. For reference, sub-task 1's `Logistic` had 0.25896 on the same folds; the training log-loss with team is 0.25529 against 0.25769, so the gap between training and held-out log-loss grew from 0.0013 to 0.0053. | DR-25 |
| 58 | Step 4d, sub-task 2, round 2 (DR-26): `Logistic + poly` 0.25765 and `Logistic + poly + L2` 0.25765 lead, indistinguishable; `Logistic` 0.26059 and `Logistic + L2` 0.26061 trail by about 0.0029. The penalty helped in neither case. For reference, the sub-task 1 model without team had 0.25597 on the same folds. Expectation met in part (DR-24). | DR-26, DR-24 |
| 59 | Step 4e, sub-task 2, diagnosis pass 1 (DR-27): O4 (underfitting by the §18 ratio) holds first; DX-5's only applicable action is to ask the user whether more input variables exist. Loop paused. The learning curve with team falls steeply at small sizes (held-out log-loss 0.389 at 10 % of the training matches) and levels off (0.2583 at 80 %, 0.2577 at 100 %; C3 adequate). | DR-27 |
| 60 | Step 4e, sub-task 2: the user answered that there are no more input variables and ended the loop ("no. end loop"; S5). Step 4f: recommendation `Logistic + poly` with team, selection confidence Low (DR-28). The cross-validation part of the sub-task 2 criterion is not met: the team model is worse than the sub-task 1 model by 0.00168 in log-loss, fold-by-fold spread 0.00117. | DR-27, DR-28 |
| 61 | `FRAMEWORK` change (commit `6cdfa32`, `Davids Changes.md` entry 15): figures in the style of the book's (`Code/sml_style.py`). Figures 1–5 were redrawn from the same data with no number changed; the captions that name colours were updated (goals red instead of coral; Figure 4 coral dashed and lavender; Figure 5 blue and orange dashed). | `Code/outputs/xg/figures/`; `Project Report.md` |
| 62 | Step 4f′, sub-task 2. `Methods` checked against what was done: unchanged (the diagnosis pass changed nothing reported). First `Results` paragraph written, with Figure 6 (the ten fold-by-fold differences between the team model and the sub-task 1 model, and their mean ± spread, which the figure script checks against the core's reported comparison) and Figure 7 (held-out learning curves with and without team). Both proposed and agreed ("yes"). | `Project Report.md`; `figures/fig_team_vs_noteam.csv` |
| 63 | Step 4g, sub-task 2: the single test evaluation ("yes."). Team model test log-loss 0.24638 (± 0.00582) against the sub-task 1 model's 0.24573 on the same shots; baseline 0.31612; StatsBomb xG 0.24010. Test part not met; with the cross-validation part also not met, the sub-task 2 criterion is not met. Recomputed from the saved predictions: identical. DR-28 completed. | DR-28; `core_final_subtask2.json` |
| 64 | Step 4h, sub-task 2: Recommendation Report assembled; test-result paragraph added to `Results` after the 4f′ paragraph, unchanged; `Methods` checked, unchanged; draft `Abstract` updated. | `Appendix.md`, `Project Report.md` |
| 65 | Step 4 closed by the user ("All good. Move on"). Team coefficients are not shown in the report; how the model predicts is left to step 5. Step 5 started. | — |
| 66 | Step 5: the user agreed the five themes of the `Discussion` ("Agree."). The `Discussion` was written; theme 2 (how the model predicts) in words only, without prediction curves, since those would need new computation. The final `Abstract` replaced the draft. Parts 9 and 10 of both Recommendation Reports lost their *Draft* marks. | `Project Report.md`, `Appendix.md` |
| 67 | Step 5: the user chose the title, "Using expected goals to test whether some football teams convert their chances better than others?", in place of the three suggested. Entered in `Project Report.md` as written. Raised with the user: the word "test" may suggest a statistical test of team differences, which the analysis did not make (DR-05, DR-11). | `Project Report.md` |
| 68 | Step 5: at the user's request the question mark was removed from the title ("no question mark"). The point about the word "test" (row 67) was raised; the user kept the wording. | `Project Report.md` |
| 69 | `FRAMEWORK` change (commit `149c2f5`, `Davids Changes.md` entry 16): the content is checked against the title and the user consulted. Check made for the chosen title; findings put to the user, decision pending. | — |
| 70 | Step 5, title check resolved: the user kept the title and asked for the content to emphasise it ("change content to emphasise title"). The `Abstract` and `Introduction` now open on the team question, present the xG model as the instrument, and say that the test is one of prediction, not a statistical test of team differences; the sub-task headings became *Sub-task 1: the measure of chance quality* and *Sub-task 2: testing the teams* in `Methods` and `Results`; the `Discussion` now opens with the team answer, followed by the xG model. No number, result or claim was added or changed. Rechecked against the title: the word "test" is defined where it is first used, and the report now leads with the title's question. | `Project Report.md` |
| 71 | Step 5 closed by the user ("It is complete."). The report's `Appendix` section, still a template note, was filled with a pointer to this Appendix and the code. The analysis was submitted to `Demonstration/xG/` as `Report.md` and `Appendix.md`, with the report's links rewritten relative to that folder (`../../Code/…`) and checked; the root `Project Report.md` and `Appendix.md` were reset from the templates. | `Demonstration/xG/` |

## Code Summary

`Code/xg/01_download_shots.py` downloads the five 2015/16 match lists and 1,551 event files from StatsBomb open data, pinned to commit `4b73468`. It caches each file's original bytes, gzip-compressed, in `Attachments/statsbomb-open-data-2015-16/raw/`, so later runs read the cache and don't download again. It writes `SHA256SUMS_raw.txt`, and in `Code/outputs/xg/` it writes `shots_open_play.csv`, `freeze_frames_open_play.csv` and `download_log.txt` (shot counts by type and league, and checksums). Two settings affect the result: `KEEP_SHOT_TYPE = "Open Play"` and `EXCLUDE_KEY_PASS_TYPES = {"Corner", "Free Kick", "Throw-in", "Goal Kick", "Kick Off"}`. The latter drops shots whose key pass (`shot.key_pass_id`) comes from a restart. The log also gives the key-pass types and the number of kept shots that come later in a possession containing a corner. The script uses no randomness and only the standard library. Run it with `cd Code && uv run python xg/01_download_shots.py`.

`Code/xg/02_describe_shots.py` takes a table name, `open_play` (the default) or `clean`, and reads the matching shot and freeze-frame tables. It writes `describe_shots.md` (for `open_play`) or `describe_shots_clean.md` (for `clean`) in `Code/outputs/xg/`. Each gives a per-column summary, value counts, coverage by league, location ranges, the pattern of missing values and a freeze-frame summary. It uses no randomness. Run it with `cd Code && uv run python xg/02_describe_shots.py [open_play|clean]`.

`Code/xg/03_clean_shots.py` applies the user's scope and cleaning decisions to `shots_open_play.csv` and `freeze_frames_open_play.csv`. It drops the leagues in `EXCLUDE_LEAGUES` = {GER}, then removes shots whose event lasted longer than `MAX_DURATION_S` = 60 s, shots with `x` < `HALFWAY` = 60, and shots whose freeze frame shows no opposing goalkeeper. It also maps two event-file team names (`TEAM_NAMES`) to the match files' names. It writes `shots_clean.csv`, `freeze_frames_clean.csv` and `clean_log.txt`, which gives the counts per rule and the checksums. It uses no randomness. Run it after `01` with `cd Code && uv run python xg/03_clean_shots.py`, then run `02` with `clean`.

`Code/xg/04_split.py` splits `shots_clean.csv` into training and test sets by matchweek. It reads each match's `match_week` from the StatsBomb match files, draws `TEST_WEEKS` = 8 of the 38 weeks per league with `numpy.random.default_rng(SEED)` (`SEED` = 20261111, leagues in the order ENG, ESP, ITA, FRA), and puts those weeks' matches in the test set. It writes `Code/outputs/xg/split/shots_train.csv` and `freeze_frames_train.csv`, the locked test files in `split/test_locked/`, and `split.json`, which gives the seed, the weeks drawn, the test matches per team, the match IDs on each side, the counts and the checksums. Only the final evaluation of each sub-task may read `test_locked/`. Run it with `cd Code && uv run python xg/04_split.py`. (Its first version drew 20 % of matches with `GroupShuffleSplit`, seed 20261110; DR-08, superseded.)

`Code/xg/features.py` holds the input design (DR-13) as fixed formulas: distance and angle to goal from `x` and `y`; the number of opponents other than the goalkeeper inside the triangle of shot and posts; and the distance from the shot to the opposing goalkeeper, from the freeze frame. It lists the inputs of each sub-task (`INPUTS_SUBTASK1`, `INPUTS_SUBTASK2`). Nothing in it is fitted, so it is applied unchanged to the test shots at the final evaluation.

`Code/xg/05_build_inputs.py` applies `features.py` to the training shots only. It writes `Code/outputs/xg/split/inputs_train.csv` and `Code/outputs/xg/inputs_train_summary.md`, which gives the ranges and counts of every input and the encoded input counts behind Properties 2–4. It uses no randomness. Run it with `cd Code && uv run python xg/05_build_inputs.py`.

`Code/xg/core.py` is the interim core for this analysis (interim core, not reviewed); Decision Records quote its SHA-256 as the code version. Its docstring lists what it implements (§11–§19) and every interpretation it makes (a–o). Commands, run from `Code/` with `--subtask 1` or `2`: `p9p10`, `admset`, `prior`, `cv round1`, `cv round2`, `cv add`, `diagnose`, `recommend`, `final --approved "<the user's words>"`. Each writes a JSON file to `Code/outputs/xg/` (`core_*.json`); cross-validation results accumulate in `core_cv_store_subtask<n>.json`. Seeds: `CV_SEED` = 2026 for the outer and inner folds and the learning-curve subsets. Property values are read from `Code/xg/inputs/subtask<n>_props.json`, copied from the latest `PROP` record. Only `final` reads the locked test set, once per sub-task.

`Code/xg/xg_style.py` applies the workspace figure style (`Code/sml_style.py`, in the style of the book's figures) and fixes one colour per variable for this analysis: red for goals, blue for the sub-task 1 model, rose for the team model, orange for StatsBomb xG, coral for training error, lavender for held-out error, grey for all shots and the baseline. Each figure is drawn twice, on a light and on a dark background, into `Code/outputs/xg/figures/` and `figures/dark/`.

`Code/xg/06_fig1_shot_map.py`, `07_fig2_goal_share_distance.py` and `08_fig3_goal_share_types.py` draw Figures 1–3 from the training shots only (`split/shots_train.csv`, `split/inputs_train.csv`), and write the numbers quoted in the text beside the images (`fig1_numbers.txt`, `fig2_numbers.csv`, `fig3_numbers.csv`). No randomness. Run each with `cd Code && uv run python xg/<script>`.

`Code/xg/09_fig_cv_comparison.py` and `10_fig_learning_curve.py` draw report Figures 3 and 4 for sub-task 1 from the core's outputs only (`core_cv_round2_subtask1.json`, `core_recommend_subtask1.json`); they refit nothing and recompute no reported number. Run each with `cd Code && uv run python xg/<script>`.

`Code/xg/11_fig_calibration_subtask1.py` draws report Figure 5 from the saved test predictions (`core_test_predictions_subtask1.csv`): ten equal-size groups by predicted probability, for the model and StatsBomb xG. It refits nothing and does not evaluate the test set again; the plotted values are in `figures/fig_calibration_subtask1.csv`.

`Code/xg/12_fig_team_vs_noteam.py` and `13_fig_learning_curves_team.py` draw report Figures 6 and 7 for sub-task 2 from the core's outputs only (the two CV stores and the two `core_recommend_subtask<n>.json` files). Figure 6's script asserts that its mean and spread equal the comparison the core reports, and writes the ten fold differences to `figures/fig_team_vs_noteam.csv`.

## References

- Lindholm, A., Wahlström, N., Lindsten, F. and Schön, T. B. (2026). [*Machine Learning – A First Course for Engineers and Scientists*](https://smlbook.org/), 2nd edition, online draft version of 1 September 2026. Cambridge University Press (to be published). Read at smlbook.org. Page references in the Decision Records come from `ML Guide.md`.
- StatsBomb Open Data [Dataset]. StatsBomb. [https://github.com/statsbomb/open-data](https://github.com/statsbomb/open-data), commit `4b73468fc5b0f1950f9f66fada70ad3a4f9327cb`, downloaded 9 November 2026. The repository's terms ask that published work based on the data names StatsBomb as the source and uses its logo (`Attachments/SOURCE.md`).
