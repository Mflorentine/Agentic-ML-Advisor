# Provenance tags in the *Rules applied* tables of the six analyses

Counting method: see the docstring of `Code/project_01_provenance_tally.py`. Records in force exclude fully superseded records; DX records have no *Rules applied* table.

| Analysis | Records in force (of all) | Rule rows | [B] | [B→I] | [I] | UNLISTED | no tag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | 15 (19) | 45 | 17 | 12 | 15 | 1 | 0 |
| Sepsis | 15 (20) | 52 | 31 | 11 | 7 | 3 | 0 |
| Mobile Price | 17 (21) | 50 | 23 | 5 | 18 | 1 | 3 |
| Heart Failure rerun | 16 (17) | 52 | 26 | 8 | 15 | 1 | 2 |
| Student Dropout | 27 (28) | 71 | 28 | 14 | 23 | 0 | 6 |
| Auto MPG | 34 (36) | 59 | 28 | 3 | 17 | 0 | 11 |
| **All six** | 124 | 329 | 153 | 53 | 95 | 6 | 22 |

Rows by strongest tag (one class per row, priority UNLISTED > [B→I] > [B] > [I]). Tag mentions (each distinct tag kind in a row counted once), records in force: [B] 155, [B→I] 53, [I] 123, UNLISTED 6, none 22.

Over all records, including superseded ones, rows by strongest tag: [B] 173, [B→I] 71, [I] 121, UNLISTED 8, none 26 (399 rows).
