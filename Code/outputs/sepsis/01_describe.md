# Sepsis: describing pass (step 1)

Rows: {'all': 1552210, 'A': 790215, 'B': 761995}  
Patients: {'all': 40336, 'A': 20336, 'B': 20000}  
Duplicate rows within a patient: 0  
Rows with no vital or lab value: 128039

## Checksums

```
{
  "A": {
    "listed": 20336,
    "on_disk": 20336,
    "mismatched": 0,
    "missing_from_list": 0,
    "missing_from_disk": 0,
    "list_sha256": "ef8e0184be4b5bd28b7e0a1642fdcd9c8b04cf10b5dd4bd666156a71ab05697d"
  },
  "B": {
    "listed": 20000,
    "on_disk": 20000,
    "mismatched": 0,
    "missing_from_list": 0,
    "missing_from_disk": 0,
    "list_sha256": "ca9da41aa7154b5b02f4818de98fc157c03599a475abca5f63bffddacff96ca4"
  }
}
```

## Stays

```
{
  "all": {
    "patients": 40336,
    "hours_min": 8,
    "hours_median": 38.0,
    "hours_max": 336,
    "iculos_first_not_1": 8793,
    "iculos_first_max": 304,
    "iculos_last_max": 336,
    "iculos_with_gaps": 0
  },
  "A": {
    "patients": 20336,
    "hours_min": 8,
    "hours_median": 39.0,
    "hours_max": 336,
    "iculos_first_not_1": 7497,
    "iculos_first_max": 304,
    "iculos_last_max": 336,
    "iculos_with_gaps": 0
  },
  "B": {
    "patients": 20000,
    "hours_min": 8,
    "hours_median": 38.0,
    "hours_max": 336,
    "iculos_first_not_1": 1296,
    "iculos_first_max": 26,
    "iculos_last_max": 336,
    "iculos_with_gaps": 0
  }
}
```

## Label

```
{
  "all": {
    "patients_septic": 2932,
    "patients_septic_pct": 7.27,
    "rows_label1": 27916,
    "rows_label1_pct": 1.8,
    "septic_label_not_monotone": 0,
    "septic_label1_from_first_row": 426,
    "septic_first_label1_iculos_median": 29.0,
    "septic_first_label1_iculos_max": 331.0,
    "septic_rows_label1_median": 10.0,
    "septic_rows_label1_max": 10
  },
  "A": {
    "patients_septic": 1790,
    "patients_septic_pct": 8.8,
    "rows_label1": 17136,
    "rows_label1_pct": 2.17,
    "septic_label_not_monotone": 0,
    "septic_label1_from_first_row": 203,
    "septic_first_label1_iculos_median": 29.5,
    "septic_first_label1_iculos_max": 331.0,
    "septic_rows_label1_median": 10.0,
    "septic_rows_label1_max": 10
  },
  "B": {
    "patients_septic": 1142,
    "patients_septic_pct": 5.71,
    "rows_label1": 10780,
    "rows_label1_pct": 1.41,
    "septic_label_not_monotone": 0,
    "septic_label1_from_first_row": 223,
    "septic_first_label1_iculos_median": 28.5,
    "septic_first_label1_iculos_max": 331.0,
    "septic_rows_label1_median": 10.0,
    "septic_rows_label1_max": 10
  }
}
```

## Per-patient constancy and demographics

```
{
  "constancy": {
    "age_varies": 0,
    "gender_varies": 0,
    "hospadmtime_varies": 0
  },
  "demographics": {
    "all": {
      "gender_0": 17770,
      "gender_1": 22566,
      "gender_missing": 0,
      "age_100": 392,
      "age_median": 63.11,
      "unit1_ever": 12267,
      "unit2_ever": 12452,
      "unit_all_missing": 15617,
      "both_units": 0
    },
    "A": {
      "gender_0": 8502,
      "gender_1": 11834,
      "gender_missing": 0,
      "age_100": 0,
      "age_median": 64.67,
      "unit1_ever": 5344,
      "unit2_ever": 5470,
      "unit_all_missing": 9522,
      "both_units": 0
    },
    "B": {
      "gender_0": 9268,
      "gender_1": 10732,
      "gender_missing": 0,
      "age_100": 392,
      "age_median": 62.0,
      "unit1_ever": 6923,
      "unit2_ever": 6982,
      "unit_all_missing": 6095,
      "both_units": 0
    }
  },
  "unit1_plus_unit2": {
    "1.0": 940250
  }
}
```

## Columns (both sets)

| Column | Group | Unit | Rows present % | Patients ever % (A / B) | Min | P1 | Median | P99 | Max |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HR` | vital | beats per minute | 90.12 | 99.99 (100.0 / 99.98) | 20 | 50 | 83.5 | 130 | 280 |
| `O2Sat` | vital | % | 86.94 | 99.96 (99.94 / 99.97) | 20 | 89 | 98 | 100 | 100 |
| `Temp` | vital | deg C | 33.84 | 99.3 (98.84 / 99.76) | 20.9 | 35.1 | 37 | 38.8 | 50 |
| `SBP` | vital | mm Hg | 85.42 | 99.3 (98.73 / 99.88) | 20 | 80 | 121 | 186 | 300 |
| `MAP` | vital | mm Hg | 87.55 | 99.74 (99.99 / 99.49) | 20 | 52 | 80 | 128 | 300 |
| `DBP` | vital | mm Hg | 68.65 | 81.63 (63.69 / 99.86) | 20 | 38 | 62 | 103 | 300 |
| `Resp` | vital | breaths per minute | 84.65 | 99.82 (99.86 / 99.78) | 1 | 9 | 18 | 34 | 100 |
| `EtCO2` | vital | mm Hg | 3.71 | 7.97 (0.0 / 16.08) | 10 | 13 | 33 | 52 | 100 |
| `BaseExcess` | lab | mmol/L | 5.42 | 32.75 (62.21 / 2.79) | -32 | -13 | 0 | 11 | 100 |
| `HCO3` | lab | mmol/L | 4.19 | 50.12 (97.37 / 2.08) | 0 | 13 | 24 | 36 | 55 |
| `FiO2` | lab | % | 8.33 | 44.15 (58.94 / 29.11) | -50 | 0.21 | 0.5 | 1 | 4000 |
| `pH` | lab | none | 6.93 | 46.94 (64.82 / 28.77) | 6.62 | 7.15 | 7.38 | 7.53 | 7.93 |
| `PaCO2` | lab | mm Hg | 5.56 | 45.51 (61.85 / 28.9) | 10 | 24 | 40 | 76 | 100 |
| `SaO2` | lab | % | 3.45 | 32.45 (39.16 / 25.62) | 23 | 53 | 97 | 99.8 | 100 |
| `AST` | lab | IU/L | 1.62 | 35.59 (28.98 / 42.32) | 3 | 10 | 41 | 5003 | 9961 |
| `BUN` | lab | mg/dL | 6.87 | 95.0 (97.9 / 92.04) | 1 | 4 | 17 | 103 | 268 |
| `Alkalinephos` | lab | IU/L | 1.61 | 35.14 (28.04 / 42.35) | 7 | 25 | 74 | 555 | 3833 |
| `Calcium` | lab | mg/dL | 5.88 | 86.76 (81.37 / 92.25) | 1 | 1.07 | 8.3 | 10.5 | 27.9 |
| `Chloride` | lab | mmol/L | 4.54 | 53.08 (97.33 / 8.09) | 26 | 90 | 106 | 120 | 145 |
| `Creatinine` | lab | mg/dL | 6.1 | 94.92 (97.73 / 92.06) | 0.1 | 0.37 | 0.94 | 9.7 | 46.6 |
| `Bilirubin_direct` | lab | mg/dL | 0.19 | 5.1 (2.88 / 7.36) | 0.01 | 0.06 | 0.445 | 19.82 | 37.5 |
| `Glucose` | lab | mg/dL | 17.11 | 96.08 (98.0 / 94.14) | 10 | 65 | 127 | 326 | 988 |
| `Lactate` | lab | mg/dL | 2.67 | 30.97 (38.03 / 23.8) | 0.2 | 0.6 | 1.8 | 14.22 | 31 |
| `Magnesium` | lab | mmol/dL | 6.31 | 87.78 (93.17 / 82.28) | 0.2 | 1.3 | 2 | 3.3 | 9.8 |
| `Phosphate` | lab | mg/dL | 4.01 | 70.21 (82.05 / 58.18) | 0.2 | 1.1 | 3.3 | 8.5 | 18.8 |
| `Potassium` | lab | mmol/L | 9.31 | 95.37 (97.87 / 92.83) | 1 | 2.9 | 4.1 | 6.1 | 27.5 |
| `Bilirubin_total` | lab | mg/dL | 1.49 | 35.32 (28.37 / 42.39) | 0.1 | 0.2 | 0.9 | 25.1 | 49.6 |
| `TroponinI` | lab | ng/mL | 0.95 | 17.49 (2.4 / 32.82) | 0.01 | 0.01 | 0.3 | 135.5 | 440 |
| `Hct` | lab | % | 8.85 | 94.26 (98.21 / 90.24) | 5.5 | 19.5 | 30.3 | 45.1 | 71.7 |
| `Hgb` | lab | g/dL | 7.38 | 93.93 (97.51 / 90.3) | 2.2 | 6.5 | 10.3 | 15.5 | 32 |
| `PTT` | lab | seconds | 2.94 | 50.17 (77.89 / 21.99) | 12.5 | 21 | 32.4 | 150 | 250 |
| `WBC` | lab | count*10^3/uL | 6.41 | 93.49 (96.93 / 90.0) | 0.1 | 2.5 | 10.3 | 31.2 | 440 |
| `Fibrinogen` | lab | mg/dL | 0.66 | 11.19 (12.62 / 9.74) | 34 | 71 | 250 | 817.6 | 1760 |
| `Platelets` | lab | count*10^3/uL | 5.94 | 93.61 (97.12 / 90.04) | 1 | 34 | 181 | 542 | 2322 |
| `Age` | demographic | years (100 for 90 or above) | 100.0 | 100.0 (100.0 / 100.0) | 14 | 21 | 64 | 89 | 100 |
| `Gender` | demographic | 0 female, 1 male | 100.0 | 100.0 (100.0 / 100.0) | 0 | 0 | 1 | 1 | 1 |
| `Unit1` | demographic | MICU (identifier) | 60.57 | 61.28 (53.18 / 69.53) | 0 | 0 | 0 | 1 | 1 |
| `Unit2` | demographic | SICU (identifier) | 60.57 | 61.28 (53.18 / 69.53) | 0 | 0 | 1 | 1 | 1 |
| `HospAdmTime` | demographic | hours, hospital admit to ICU admit | 100.0 | 100.0 (100.0 / 100.0) | -5367 | -630.1 | -6.03 | 0 | 23.99 |
| `ICULOS` | demographic | hours since ICU admit | 100.0 | 100.0 (100.0 / 100.0) | 1 | 1 | 21 | 166 | 336 |
| `SepsisLabel` | outcome | 0 or 1 | 100.0 | 100.0 (100.0 / 100.0) | 0 | 0 | 0 | 1 | 1 |
