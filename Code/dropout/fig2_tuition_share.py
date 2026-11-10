"""Step 3, Figure 2: share of students who dropped out, by whether tuition fees are up to date. Training rows only.

Each bar is one group (fees up to date: yes, or no). Its height is the share of that group's students
whose Target is Dropout. The number of students in each group is printed under its bar.

Reads   Attachments/Student Dropout/data.csv (never modified)
        Code/outputs/dropout/02_split.csv (training rows only are plotted)
Writes  Code/outputs/dropout/figures/fig2_tuition_share.png        (light)
        Code/outputs/dropout/figures/dark/fig2_tuition_share.png   (dark)
        Code/outputs/dropout/fig2_tuition_share.csv                 (the plotted numbers)

Run     cd Code && uv run python dropout/fig2_tuition_share.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "Code"))
import sml_style  # noqa: E402

SRC = ROOT / "Attachments" / "Student Dropout" / "data.csv"
SPLIT = ROOT / "Code" / "outputs" / "dropout" / "02_split.csv"
OUT = ROOT / "Code" / "outputs" / "dropout"
FIG_DIR = OUT / "figures"

df = pd.read_csv(SRC, sep=";", encoding="utf-8-sig")
df.columns = [c.strip() for c in df.columns]
split = pd.read_csv(SPLIT)
assert len(split) == len(df)

train = (split["split"] == "train").values
d = df.loc[train].copy()
assert len(d) == 3539, len(d)

d["dropout"] = (d["Target"] == "Dropout")
groups = [("Yes", 1), ("No", 0)]  # tuition fees up to date

rows = []
shares = []
ns = []
for label, code in groups:
    g = d[d["Tuition fees up to date"] == code]
    n = len(g)
    k = int(g["dropout"].sum())
    share = k / n
    shares.append(share)
    ns.append(n)
    rows.append({"tuition_fees_up_to_date": label, "students": n, "dropout": k, "share_dropout": share})
pd.DataFrame(rows).to_csv(OUT / "fig2_tuition_share.csv", index=False, lineterminator="\n")

for theme_name in ["light", "dark"]:
    theme = sml_style.use(theme_name)
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    xs = range(len(groups))
    bars = ax.bar(xs, shares, width=0.55, color=sml_style.BLUE, edgecolor=theme.ink, linewidth=0.4)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"{label}\n(n = {n:,})" for (label, _), n in zip(groups, ns)])
    ax.set_xlabel("Tuition fees up to date")
    ax.set_ylabel("Share of students who dropped out")
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=6))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    sml_style.save(fig, FIG_DIR, "fig2_tuition_share", theme)

print("wrote", FIG_DIR / "fig2_tuition_share.png", "and dark variant")
print(pd.DataFrame(rows).to_string(index=False))
