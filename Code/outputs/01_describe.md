# Describing pass: `heart_failure_clinical_records_dataset.csv`

299 rows × 13 columns; 12,239 bytes; SHA-256 `9c73cea7468ff5d517801ec050fe9993da5912fce4b56f296f8df3b38dd75912`. Missing cells: 0. Duplicate rows: 0. Rows sorted by `time`: True.

| Column | Meaning (UCI) | Unit (UCI) | Type | Missing | Distinct | Min | Median | Max | Zeros | 0 / 1 counts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `age` | age of the patient | years | float64 | 0 | 47 | 40 | 60 | 95 | 0 | — |
| `anaemia` | decrease of red blood cells or hemoglobin | boolean | int64 | 0 | 2 | 0 | 0 | 1 | 170 | 170 / 129 |
| `creatinine_phosphokinase` | level of the CPK enzyme in the blood | mcg/L | int64 | 0 | 208 | 23 | 250 | 7861 | 0 | — |
| `diabetes` | if the patient has diabetes | boolean | int64 | 0 | 2 | 0 | 0 | 1 | 174 | 174 / 125 |
| `ejection_fraction` | percentage of blood leaving the heart at each contraction | % | int64 | 0 | 17 | 14 | 38 | 80 | 0 | — |
| `high_blood_pressure` | if the patient has hypertension | boolean | int64 | 0 | 2 | 0 | 0 | 1 | 194 | 194 / 105 |
| `platelets` | platelets in the blood | kiloplatelets/mL | float64 | 0 | 176 | 25100 | 262000 | 850000 | 0 | — |
| `serum_creatinine` | level of serum creatinine in the blood | mg/dL | float64 | 0 | 40 | 0.5 | 1.1 | 9.4 | 0 | — |
| `serum_sodium` | level of serum sodium in the blood | mEq/L | int64 | 0 | 27 | 113 | 137 | 148 | 0 | — |
| `sex` | woman or man | binary | int64 | 0 | 2 | 0 | 1 | 1 | 105 | 105 / 194 |
| `smoking` | if the patient smokes or not | boolean | int64 | 0 | 2 | 0 | 0 | 1 | 203 | 203 / 96 |
| `time` | follow-up period | days | int64 | 0 | 148 | 4 | 115 | 285 | 0 | — |
| `DEATH_EVENT` | if the patient died during the follow-up period (target on the UCI page) | boolean | int64 | 0 | 2 | 0 | 0 | 1 | 203 | 203 / 96 |

Non-integer values of `age`: [60.667, 60.667].
