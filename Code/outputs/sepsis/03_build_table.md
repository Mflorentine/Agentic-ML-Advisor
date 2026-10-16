# Sepsis: derived tables (step 1)

```
{
  "drop_threshold_pct": 10,
  "dropped": {
    "EtCO2": {
      "A": 0.0,
      "B": 16.08
    },
    "BaseExcess": {
      "A": 62.21,
      "B": 2.79
    },
    "HCO3": {
      "A": 97.37,
      "B": 2.08
    },
    "Chloride": {
      "A": 97.33,
      "B": 8.09
    },
    "Bilirubin_direct": {
      "A": 2.88,
      "B": 7.36
    },
    "TroponinI": {
      "A": 2.4,
      "B": 32.82
    },
    "Fibrinogen": {
      "A": 12.62,
      "B": 9.74
    }
  },
  "cleaning": {
    "FiO2": {
      "low": 0.21,
      "high": 1.0,
      "set_to_missing": 385,
      "by_set": {
        "A": 318,
        "B": 67
      },
      "patients": 299
    },
    "Temp": {
      "low": 25,
      "high": 45,
      "set_to_missing": 6,
      "by_set": {
        "A": 4,
        "B": 2
      },
      "patients": 6
    },
    "Potassium": {
      "low": null,
      "high": 15,
      "set_to_missing": 2,
      "by_set": {
        "A": 1,
        "B": 1
      },
      "patients": 2
    },
    "Hgb": {
      "low": null,
      "high": 25,
      "set_to_missing": 3,
      "by_set": {
        "A": 1,
        "B": 2
      },
      "patients": 3
    }
  },
  "kept_as_is": {
    "hospadmtime_positive_rows": 8483,
    "hospadmtime_positive_patients": 255,
    "age_under_18_patients": 21,
    "age_min": 14.0,
    "age_min_patients": 2,
    "age_100_patients": {
      "A": 0,
      "B": 389
    }
  },
  "table": {
    "hours_rows": 1524294,
    "hours_columns": [
      "patient",
      "set",
      "HR",
      "O2Sat",
      "Temp",
      "SBP",
      "MAP",
      "DBP",
      "Resp",
      "FiO2",
      "pH",
      "PaCO2",
      "SaO2",
      "AST",
      "BUN",
      "Alkalinephos",
      "Calcium",
      "Creatinine",
      "Glucose",
      "Lactate",
      "Magnesium",
      "Phosphate",
      "Potassium",
      "Bilirubin_total",
      "Hct",
      "Hgb",
      "PTT",
      "WBC",
      "Platelets",
      "Age",
      "Gender",
      "Unit1",
      "Unit2",
      "HospAdmTime",
      "ICULOS"
    ],
    "inputs": [
      "HR",
      "O2Sat",
      "Temp",
      "SBP",
      "MAP",
      "DBP",
      "Resp",
      "FiO2",
      "pH",
      "PaCO2",
      "SaO2",
      "AST",
      "BUN",
      "Alkalinephos",
      "Calcium",
      "Creatinine",
      "Glucose",
      "Lactate",
      "Magnesium",
      "Phosphate",
      "Potassium",
      "Bilirubin_total",
      "Hct",
      "Hgb",
      "PTT",
      "WBC",
      "Platelets",
      "Age",
      "Gender",
      "Unit1",
      "Unit2",
      "HospAdmTime"
    ],
    "n_inputs": 32,
    "categorical_inputs": [
      "Gender",
      "Unit1",
      "Unit2"
    ],
    "patients_total": 40336,
    "patients_with_hours": 39910,
    "septic_total": 2932,
    "septic_with_hours": 2506,
    "by_set": {
      "A": {
        "rows": 773079,
        "patients_with_hours": 20133,
        "septic_with_hours": 1587
      },
      "B": {
        "rows": 751215,
        "patients_with_hours": 19777,
        "septic_with_hours": 919
      }
    }
  },
  "sha256": {
    "private/hours.csv.gz": "f86128f3be3c87bf84aee2abf5f7c8852af7f5227c495133ea4b7dba8dd2b86e",
    "private/patients.csv.gz": "0d8ab8d4a46df453298d725f3a6b61855dd355cc9b10c4685715cffd144d1535"
  }
}
```
