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

## `Mobile Price/` (`train.csv`, `test.csv`)

| Item | Value |
| --- | --- |
| Source | Kaggle, [Mobile Price Classification](https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification), by Abhishek Sharma (`iabhishekofficial`), version 1 |
| Downloaded | 15 October 2026, by the user |
| Licence | **Unknown**, as given in Kaggle's dataset metadata (`licenseNameNullable: "Unknown"`, checked 15 October 2026; the page itself shows no licence to a plain fetch). Because redistribution is not established, the folder is listed in `.gitignore` and is not committed. |
| Format | CSV, comma-separated, ASCII text, header row |
| Number of files | 2. Kaggle lists a total of 186,253 bytes, which equals the two files' combined size. |
| `train.csv` | 122,403 bytes · 2,000 data rows (plus the header) × 21 columns: 20 inputs and `price_range` · SHA-256 `f9e8cd3154b8684a1be0ff401b1fba7750710af6bd076a399c6ce7ceb979c624` |
| `test.csv` | 63,850 bytes · 1,000 data rows (plus the header) × 21 columns: `id` and the same 20 inputs, **with no `price_range`** · SHA-256 `e929f5999ffeedec84abf53cc8d35faa1bbd7e8ebd61826881aa62562d37adce` |
| Columns (`train.csv`) | `battery_power`, `blue`, `clock_speed`, `dual_sim`, `fc`, `four_g`, `int_memory`, `m_dep`, `mobile_wt`, `n_cores`, `pc`, `px_height`, `px_width`, `ram`, `sc_h`, `sc_w`, `talk_time`, `three_g`, `touch_screen`, `wifi`, `price_range` |

The files are the original download and are never modified.

## `Sepsis dataset.csv`

| Item | Value |
| --- | --- |
| Source named by the user | PhysioNet, [Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019](https://physionet.org/content/challenge-2019/), version 1.0.0 (5 August 2019) |
| Downloaded | 15 October 2026, by the user |
| Licence | The PhysioNet page gives the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/) (checked 15 October 2026). This file is not in PhysioNet's own format (see below), so the licence of this particular copy is **to be confirmed** once its source is known. The file is listed in `.gitignore` and is never committed, because it holds patient-level records. |
| Format | One CSV file, comma-separated, ASCII text, header row. PhysioNet distributes the training data as one pipe-separated `.psv` file per patient (training set A, 20,336 patients; training set B, 20,000). This file instead combines patients in one table, with an unnamed row-index first column and an added `Patient_ID` column, so it is a derived copy, and its origin is to be confirmed. |
| Number of files | 1 |
| Size | 54,525,952 bytes (exactly 52 MiB) |
| Rows and columns | 546,123 lines after the header × 44 columns. **The file looks truncated:** its last line ends partway through a row (22 of 44 fields), and its size is an exact multiple of 1 MiB. The 546,122 complete rows cover 14,057 distinct `Patient_ID` values, against 40,336 patients in the PhysioNet training data. |
| Columns | (unnamed index), `Hour`, `HR`, `O2Sat`, `Temp`, `SBP`, `MAP`, `DBP`, `Resp`, `EtCO2`, `BaseExcess`, `HCO3`, `FiO2`, `pH`, `PaCO2`, `SaO2`, `AST`, `BUN`, `Alkalinephos`, `Calcium`, `Chloride`, `Creatinine`, `Bilirubin_direct`, `Glucose`, `Lactate`, `Magnesium`, `Phosphate`, `Potassium`, `Bilirubin_total`, `TroponinI`, `Hct`, `Hgb`, `PTT`, `WBC`, `Fibrinogen`, `Platelets`, `Age`, `Gender`, `Unit1`, `Unit2`, `HospAdmTime`, `ICULOS`, `SepsisLabel`, `Patient_ID` |
| SHA-256 | `af7f8236de8ebb21fdd75c579863c0ba6bffbaac202028955d43a0e370e37e3e` (one file, so one checksum; there are no separate training-set files to checksum) |

Citation required by the PhysioNet page when the resource is used: Reyna et al. (2019), the dataset, version 1.0.0, [https://doi.org/10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857); the original Challenge paper in *Critical Care Medicine* (2019); and the standard PhysioNet citation. Full entries to be copied from the page and checked before any report cites them.
