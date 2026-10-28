# Describing pass: `heart_failure_clinical_records_dataset.csv` (Heart Failure rerun)

299 rows × 13 columns; 12,239 bytes; SHA-256 `9c73cea7468ff5d517801ec050fe9993da5912fce4b56f296f8df3b38dd75912` (matches SOURCE.md: True); CRLF: False; ASCII only: True. Missing cells: 0. Duplicate rows: 0; rows with identical inputs: 0. Rows sorted by `time`: True.

`DEATH_EVENT` counts: 0: 203, 1: 96 (share of 1: 0.3211).

`time` by `DEATH_EVENT`: 0: min 12, median 172, max 285; 1: min 4, median 44.5, max 241.

| Column | Meaning (UCI) | Unit (UCI) | UCI type | Range (paper) | dtype | Missing | Distinct | Min | 1st pct | Median | 99th pct | Max | Zeros | Non-integer | 0 / 1 counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `age` | age of the patient | years | Integer | [40, ..., 95] | float64 | 0 | 47 | 40 | 40 | 60 | 90.08 | 95 | 0 | 2 | — |
| `anaemia` | decrease of red blood cells or hemoglobin | none (boolean) | Binary | 0, 1 | int64 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | 170 | 0 | 170 / 129 |
| `creatinine_phosphokinase` | level of the CPK enzyme in the blood | mcg/L | Integer | [23, ..., 7861] | int64 | 0 | 208 | 23 | 47 | 250 | 5222.46 | 7861 | 0 | 0 | — |
| `diabetes` | if the patient has diabetes | none (boolean) | Binary | 0, 1 | int64 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | 174 | 0 | 174 / 125 |
| `ejection_fraction` | percentage of blood leaving the heart at each contraction | % | Integer | [14, ..., 80] | int64 | 0 | 17 | 14 | 16.96 | 38 | 62.06 | 80 | 0 | 0 | — |
| `high_blood_pressure` | if the patient has hypertension | none (boolean) | Binary | 0, 1 | int64 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | 194 | 0 | 194 / 105 |
| `platelets` | platelets in the blood | kiloplatelets/mL | Continuous | [25.01, ..., 850.00] | float64 | 0 | 176 | 25100 | 61780 | 262000 | 544560 | 850000 | 0 | 25 | — |
| `serum_creatinine` | level of serum creatinine in the blood | mg/dL | Continuous | [0.50, ..., 9.40] | float64 | 0 | 40 | 0.5 | 0.6 | 1.1 | 6.114 | 9.4 | 0 | 243 | — |
| `serum_sodium` | level of serum sodium in the blood | mEq/L | Integer | [114, ..., 148] | int64 | 0 | 27 | 113 | 123.94 | 137 | 145 | 148 | 0 | 0 | — |
| `sex` | woman or man | none (binary) | Binary | 0, 1 | int64 | 0 | 2 | 0 | 0 | 1 | 1 | 1 | 105 | 0 | 105 / 194 |
| `smoking` | if the patient smokes or not | none (boolean) | Binary | 0, 1 | int64 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | 203 | 0 | 203 / 96 |
| `time` | follow-up period | days | Integer | [4, ..., 285] | int64 | 0 | 148 | 4 | 7 | 115 | 271.14 | 285 | 0 | 0 | — |
| `DEATH_EVENT` | if the patient died during the follow-up period (UCI role: Target) | none (boolean) | Binary | 0, 1 | int64 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | 203 | 0 | 203 / 96 |

Non-integer values of `age`: [60.667, 60.667].
