# Provenance tags in the *Rules applied* tables of the four analyses

Counting method: see the docstring of `Code/project_01_provenance_tally.py`. Records in force exclude fully superseded records; DX records have no *Rules applied* table.

| Analysis | Records in force (of all) | Rule rows | [B] | [B→I] | [I] | UNLISTED | no tag |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Heart Failure (original) | 15 (19) | 45 | 17 | 12 | 15 | 1 | 0 |
| Sepsis | 15 (20) | 52 | 31 | 11 | 7 | 3 | 0 |
| Mobile Price | 17 (21) | 50 | 23 | 5 | 18 | 1 | 3 |
| Heart Failure rerun | 16 (17) | 52 | 26 | 8 | 15 | 1 | 2 |
| **All four** | 63 | 199 | 97 | 36 | 55 | 6 | 5 |

Rows by strongest tag (one class per row, priority UNLISTED > [B→I] > [B] > [I]). Tag mentions (each distinct tag kind in a row counted once), records in force: [B] 98, [B→I] 36, [I] 69, UNLISTED 6, none 5.

Over all records, including superseded ones, rows by strongest tag: [B] 114, [B→I] 51, [I] 81, UNLISTED 8, none 9 (263 rows).
