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

Only `train.csv` has the target, `price_range`. `test.csv` has no labels, so it cannot be used to evaluate a model; any training and test split comes from `train.csv`.

The files are the original download and are never modified.

## `sepsis-physionet-2019/`

| Item | Value |
| --- | --- |
| Source | PhysioNet, [Early Prediction of Sepsis from Clinical Data: the PhysioNet/Computing in Cardiology Challenge 2019](https://physionet.org/content/challenge-2019/), version 1.0.0 (5 August 2019): the training data in [`training/`](https://physionet.org/files/challenge-2019/1.0.0/training/), plus `LICENSE.txt` and `SHA256SUMS.txt` from [the project's files](https://physionet.org/files/challenge-2019/1.0.0/). |
| Downloaded | 15 October 2026, by the agent at the user's request. `LICENSE.txt` and `SHA256SUMS.txt` came from physionet.org. The 40,336 patient files came from PhysioNet's open-data mirror on AWS (`s3://physionet-open/challenge-2019/1.0.0/training/`), because the physionet.org directory listings stop early (at `p017933` in set A and `p116380` in set B) and offer no zip. Each file was checked against the mirror's MD5 on download, and a random sample of 30 files (seed 2026) is byte-identical to the copies on physionet.org. |
| Licence | **ODC Open Database License (ODbL)**, from `LICENSE.txt`. The dataset page gives a different licence, the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/) (checked 15 October 2026). We follow the stricter terms (ODbL): PhysioNet is credited, the raw data is not redistributed, and any derived dataset is kept out of the repository unless shared under ODbL. The folder is listed in `.gitignore`. |
| Format | One pipe-separated `.psv` file per patient, ASCII text, LF line endings, header row; one row per hour in the ICU |
| Files | `training_setA/`: 20,336 files, `p000001.psv` to `p020643.psv` (307 numbers in that range are unused). `training_setB/`: 20,000 files, `p100001.psv` to `p120000.psv`. Plus `LICENSE.txt` (25,815 bytes) and `SHA256SUMS.txt`. |
| Patients | 40,336, one per file, matching the dataset page (set A 20,336; set B 20,000) |
| Size | 255,057,484 bytes for the 40,336 patient files, equal to the total listed on the mirror |
| Rows and columns | 1,552,210 hourly rows (set A 790,215; set B 761,995) × 41 columns. Every file has the same header, every row has 41 fields, and every file ends on a complete line. |
| Columns | `HR`, `O2Sat`, `Temp`, `SBP`, `MAP`, `DBP`, `Resp`, `EtCO2`, `BaseExcess`, `HCO3`, `FiO2`, `pH`, `PaCO2`, `SaO2`, `AST`, `BUN`, `Alkalinephos`, `Calcium`, `Chloride`, `Creatinine`, `Bilirubin_direct`, `Glucose`, `Lactate`, `Magnesium`, `Phosphate`, `Potassium`, `Bilirubin_total`, `TroponinI`, `Hct`, `Hgb`, `PTT`, `WBC`, `Fibrinogen`, `Platelets`, `Age`, `Gender`, `Unit1`, `Unit2`, `HospAdmTime`, `ICULOS`, `SepsisLabel` |
| SHA-256 | PhysioNet's `SHA256SUMS.txt` covers only `LICENSE.txt` and two diagrams, not the training files; `LICENSE.txt` matches it. For the training data, a list of per-file SHA-256 checksums was written for each set, kept with the data in the ignored folder, and each list is fingerprinted here. `SHA256SUMS_training_setA.txt`: `ef8e0184be4b5bd28b7e0a1642fdcd9c8b04cf10b5dd4bd666156a71ab05697d`. `SHA256SUMS_training_setB.txt`: `ca9da41aa7154b5b02f4818de98fc157c03599a475abca5f63bffddacff96ca4`. Each list has one line per file, `<sha256>  training_setX/<file>`, sorted by file name, with LF line endings. |

A copy from Kaggle (`tea340yashjoshi/sepsis-prediction-dataset`, a single combined CSV) was tried first and replaced: it was truncated at exactly 52 MiB, partway through a row, and covered 14,057 patients. It was deleted on 15 October 2026.

Citation required by the PhysioNet page when the resource is used: Reyna et al. (2019), the dataset, version 1.0.0, [https://doi.org/10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857); the original Challenge paper in *Critical Care Medicine* (2019); and the standard PhysioNet citation. Full entries to be copied from the page and checked before any report cites them.
