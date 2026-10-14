# Source of the data

## `heart_failure_clinical_records_dataset.csv`

| Item | Value |
| --- | --- |
| Source | UCI Machine Learning Repository, [Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records) (dataset 519; donated 4 February 2020) |
| Downloaded | 14 October 2026, by the user |
| Licence | [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/), as stated on the UCI page (checked 14 October 2026). Sharing and adaptation are allowed with appropriate credit. |
| Format | CSV, comma-separated, ASCII text, LF line endings, header row |
| Size | 12,239 bytes |
| Rows and columns | 299 data rows (plus the header) × 13 columns. The UCI page lists 299 instances and 12 features; the 13th column is `DEATH_EVENT`. |
| Columns | `age`, `anaemia`, `creatinine_phosphokinase`, `diabetes`, `ejection_fraction`, `high_blood_pressure`, `platelets`, `serum_creatinine`, `serum_sodium`, `sex`, `smoking`, `time`, `DEATH_EVENT` |
| SHA-256 | `9c73cea7468ff5d517801ec050fe9993da5912fce4b56f296f8df3b38dd75912` |

The file is the original download and is never modified. The checksum is of the file as downloaded, with LF line endings. `.gitattributes` marks `Attachments/*.csv` as `-text`, so git never converts its line endings and the checksum holds on every platform.

## Citation

The UCI page's "Cite" section gives the dataset citation:

- Heart Failure Clinical Records [Dataset]. (2020). UCI Machine Learning Repository. [https://doi.org/10.24432/C5Z89R](https://doi.org/10.24432/C5Z89R).

The same page names the original authors' paper as the introductory paper for the dataset, describing the data in its Dataset section:

- Chicco, D. and Jurman, G. (2020). Machine learning can predict survival of patients with heart failure from serum creatinine and ejection fraction alone. *BMC Medical Informatics and Decision Making*, 20, 16. [https://doi.org/10.1186/s12911-020-1023-5](https://doi.org/10.1186/s12911-020-1023-5).

These details are taken from the UCI page; the paper itself has not been opened.
