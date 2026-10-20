"""Renders screenshot-style images of real excerpts from the Sepsis analysis, for the presentation.

Each image is a verbatim excerpt (shortened only where marked "…") of a file or of the agent conversation, drawn in
an editor- or terminal-like frame whose title bar names the source. They are renders of the files, not captures of
the screen. Rendered with headless Chrome.

Run:    python Presentation/build/make_screenshots.py
Writes  Presentation/build/screens/*.png
"""
import html
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "screens"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #ffffff; font-family: 'Segoe UI', Calibri, Arial, sans-serif; padding: 18px; }
.win { border-radius: 10px; overflow: hidden; box-shadow: 0 6px 24px rgba(0,0,0,.25); }
.bar { height: 38px; display: flex; align-items: center; padding: 0 14px; gap: 8px; font-size: 15px; }
.dot { width: 12px; height: 12px; border-radius: 6px; display: inline-block; }
.dark .bar { background: #2d2d30; color: #cccccc; } .dark .pane { background: #1e1e1e; color: #d4d4d4; }
.light .bar { background: #e9e9ec; color: #333; } .light .pane { background: #ffffff; color: #1f1f1f; }
.pane { padding: 22px 28px; font-size: 19px; line-height: 1.5; }
.mono { font-family: Consolas, 'Courier New', monospace; font-size: 18px; line-height: 1.45; white-space: pre; }
h3 { font-size: 23px; margin: 4px 0 10px; } h4 { font-size: 19px; margin: 14px 0 6px; }
table { border-collapse: collapse; margin: 6px 0 10px; font-size: 16.5px; }
td, th { border: 1px solid #cfcfd4; padding: 5px 9px; text-align: left; vertical-align: top; }
th { background: #f1f1f4; }
code { font-family: Consolas, monospace; font-size: .92em; background: rgba(127,127,127,.15); padding: 0 4px; border-radius: 3px; }
.user { background: #2b3a44; color: #fff; border-radius: 10px; padding: 12px 16px; margin-bottom: 16px; font-size: 18px; }
.who { font-size: 13px; text-transform: uppercase; letter-spacing: .08em; color: #8aa; margin-bottom: 4px; }
.agent li { margin: 4px 0 4px 22px; } .agent ol > li { margin-top: 10px; }
.del { background: #5a1d1d; color: #ffb3b3; } .add { background: #1d4a2a; color: #b8f5c8; }
.k { color: #9cdcfe; } .s { color: #ce9178; } .n { color: #b5cea8; } .p { color: #6a9955; }
.more { color: #888; font-style: italic; }
"""


def frame(title: str, body: str, theme: str = "dark") -> str:
    dots = "".join(f'<span class="dot" style="background:{c}"></span>' for c in ("#ff5f56", "#ffbd2e", "#27c93f"))
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"<div class='win {theme}'><div class='bar'>{dots}<span style='margin-left:10px'>{html.escape(title)}</span>"
            f"</div><div class='pane'>{body}</div></div></body></html>")


def shoot(name: str, page: str, w: int, h: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / f"{name}.html"
    src.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    "--force-device-scale-factor=2", f"--screenshot={OUT / (name + '.png')}", src.as_uri()],
                   check=True, capture_output=True)
    src.unlink()
    from PIL import Image, ImageChops
    png = OUT / f"{name}.png"
    im = Image.open(png).convert("RGB")
    box = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
    pad = 24
    im.crop((max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, im.width), min(box[3] + pad, im.height))).save(png)
    print("wrote", OUT / f"{name}.png")


def chat() -> str:
    user = ("Check each choice against the book and ML Guide.md, and tell me if any conflicts with them or with the "
            "guide's procedure (for example §16). Then write the records and the Problem Definition, show me a "
            "summary, and wait before locking the test set.")
    agent = """<h3>Points raised by the check</h3><ol>
<li><b>How PR-AUC is computed.</b> The book draws the precision–recall curve and its area (p. 92) but doesn't say how to compute the area.
<ul><li>I propose average precision (scikit-learn's <code>average_precision_score</code>), which adds up precision at each step in recall.</li>
<li>This choice is ours (<code>[I]</code>). Please confirm it or choose the other.</li></ul></li>
<li><b>The baseline and the no-skill reference are the same number.</b> "Flag nobody" gives every patient the same score, so its PR-AUC equals the positive rate. <span class="more">…</span></li>
<li value="5"><b>A problem in the guide (a possible FRAMEWORK question, not about your choices).</b> The diagnosis loop (§16, §18) measures training and validation error as the misclassification rate.
<ul><li>With 3 % positives, flagging nobody already gives an error of about 3 %, so the checks for overfitting and underfitting would say almost nothing.</li>
<li>The book itself warns that the misclassification rate misleads when classes are imbalanced (p. 91).</li></ul></li></ol>
<p class="more">… excerpt; points 3–4 and the rest of the reply omitted</p>"""
    body = f"<div class='who'>User (step 2)</div><div class='user'>{html.escape(user)}</div><div class='who'>Agent</div><div class='agent'>{agent}</div>"
    return frame("Claude Code — Sepsis analysis, step 2 (conversation, 17–18 October 2026)", body)


def decision_record() -> str:
    body = """<h3>DR-10 · PROP · step 3</h3>
<p><b>Question:</b> What are the property values P1–P10 once the input design is fixed and P9–P10 are computed from the training patients?</p>
<h4>Evidence</h4><table><tr><th>Item</th><th>Value</th><th>Tag</th></tr>
<tr><td>P4 share of categorical inputs</td><td>29 of 58 original input columns = 50.0 %: the 27 indicators, <code>Gender</code> and <code>Unit</code></td><td>M</td></tr>
<tr><td>P9 classes perfectly separable</td><td>no: training accuracy 0.9685 with negligible regularisation (C = 1e8, converged in 30 iterations)</td><td>T</td></tr>
<tr><td>P10 class imbalance</td><td>imbalanced: smallest class 984 of 31,270 = 3.15 %</td><td>T</td></tr></table>
<h4>Rules applied</h4><table><tr><th>Rule</th><th>Result</th><th>Provenance</th><th>Effect</th></tr>
<tr><td>P4 = high</td><td>holds, exactly at the threshold</td><td>[I] threshold</td><td>k-NN −1 <code>[I]</code></td></tr>
<tr><td>Categorical = finite set of values without natural order</td><td>the 27 0/1 indicators counted as categorical</td><td>[B pp.16–17]</td><td>P4 = high</td></tr>
<tr><td>P9 = no</td><td>MOD-1 does not apply</td><td>[I] procedure</td><td><code>Logistic</code> and <code>Logistic + poly</code> stay admissible</td></tr></table>
<p><b>Reference code:</b> <code>p9_p10</code> · interim core, not reviewed, SHA-256 <code>43af578e…b30b7</code> · output copied unchanged.</p>
<p><b>Supersedes:</b> DR-06 &nbsp;<span class="more">… excerpt</span></p>"""
    return frame("Demonstration/Sepsis/Appendix.md — Decision Records", body, "light")


def core_terminal() -> str:
    j = json.loads((ROOT / "Code/outputs/sepsis/core_p9_p10.json").read_text(encoding="utf-8"))
    p9, p10 = j["P9"], j["P10"]
    lines = [
        '<span class="p">PS Code&gt;</span> uv run python sepsis/core.py p9p10',
        "{",
        f'  <span class="k">"core_version_sha256"</span>: <span class="s">"{j["core_version_sha256"][:16]}…"</span>,',
        f'  <span class="k">"rows_used"</span>: <span class="s">"{j["rows_used"]}"</span>,',
        f'  <span class="k">"n_train"</span>: <span class="n">{j["n_train"]}</span>,',
        '  <span class="more">…  "inputs": [58 names] omitted</span>',
        '  <span class="k">"P9"</span>: {',
        f'    <span class="k">"value"</span>: <span class="s">"{p9["value"]}"</span>,',
        f'    <span class="k">"training_accuracy_negligible_regularisation"</span>: <span class="n">{p9["training_accuracy_negligible_regularisation"]}</span>,',
        '    <span class="more">…  C_used, converged_iterations, max_iter omitted</span>',
        f'    <span class="k">"threshold"</span>: <span class="s">"{p9["threshold"]}"</span>, <span class="k">"provenance"</span>: <span class="s">"{p9["provenance"]}"</span>',
        "  },",
        '  <span class="k">"P10"</span>: {',
        f'    <span class="k">"value"</span>: <span class="s">"{p10["value"]}"</span>,',
        f'    <span class="k">"smallest_class_share"</span>: <span class="n">{p10["smallest_class_share"]}</span>,',
        f'    <span class="k">"class_counts"</span>: {{ <span class="k">"0"</span>: <span class="n">{p10["class_counts"]["0"]}</span>, <span class="k">"1"</span>: <span class="n">{p10["class_counts"]["1"]}</span> }},',
        f'    <span class="k">"threshold"</span>: <span class="s">"{p10["threshold"]}"</span>, <span class="k">"provenance"</span>: <span class="s">"{p10["provenance"]}"</span>',
        "  },",
        f'  <span class="k">"input_columns_after_encoding"</span>: <span class="n">{j["input_columns_after_encoding"]}</span>',
        "}",
    ]
    return frame("Terminal — the deterministic core computes P9 and P10 (Code/outputs/sepsis/core_p9_p10.json)",
                 f"<div class='mono'>{chr(10).join(lines)}</div>")


def framework_diff() -> str:
    body = """<p style="margin-bottom:10px">§16 Cross-validation protocol, row <b>Diagnosis errors</b> (commit <code>ddda293</code>)</p>
<p class="del" style="padding:8px 12px;border-radius:6px">− E_train and E_val computed with the book's default error function (misclassification rate or squared error, p. 67), whatever the selection metric &nbsp;|&nbsp; [I]</p>
<p class="add" style="padding:8px 12px;border-radius:6px;margin-top:10px">+ … whatever the selection metric, except when P10 = imbalanced. Then they are computed with the deciding metric agreed in step 2, written as an error so that lower is better: 1 − metric (e.g. 1 − PR-AUC, 1 − F2). The learning curve, and so C3, uses the same error. &nbsp;|&nbsp; [I]; the imbalanced case [B→I p.91]</p>
<p style="margin-top:14px"><b>Version note:</b> 18 October 2026 (FRAMEWORK): … Prompted by the Sepsis analysis, where 3 % of patients are positive.</p>"""
    return frame("ML Guide.md — FRAMEWORK change, shown to the user before it was committed", body)


def calcium_terminal() -> str:
    j = json.loads((ROOT / "Code/outputs/sepsis/11_calcium_ptt_counts.json").read_text(encoding="utf-8"))
    c = j["calcium"]
    rows = ['<span class="p"># formatted from 11_calcium_ptt_counts.json</span>', "",
            "Last Calcium below 2.0 mg/dL, training patients",
            f"  hospital   with value   below 2.0   share",
            f"  A          {c['A']['with_calcium']:>10,}   {c['A']['low']:>9,}   {c['A']['low_pct']:>5.2f} %",
            f"  B          {c['B']['with_calcium']:>10,}   {c['B']['low']:>9,}   {c['B']['low_pct']:>5.2f} %",
            f"  cut at 1.75 / 2.5 / 3.0 / 3.5 →  " + " / ".join(f"{v:,}" for v in c['all']['at_other_cutoffs'].values()),
            "", "Calcium 0.25 mg/dL bins, 4.0–5.5", "  bin            A      B"]
    fine = j["calcium_bins_2_to_8_by_set"]
    for k in ["(4.0, 4.25]", "(4.25, 4.5]", "(4.5, 4.75]", "(4.75, 5.0]", "(5.0, 5.25]", "(5.25, 5.5]"]:
        rows.append(f"  {k:<13}{fine['A'][k]:>3}  {fine['B'][k]:>5}")
    return frame("Counting a data problem seen in Figure 3 — training patients only",
                 f"<div class='mono'>{chr(10).join(rows)}</div>")


# ---- Heart Failure (Demonstration/Heart Failure/Demonstration Appendix.md), verbatim excerpts ----
HF = "Demonstration/Heart Failure/Demonstration Appendix.md"


def hf_problem() -> str:
    body = """<h3>Problem Definition — Discussion</h3>
<ul class="agent">
<li><b>The F2 target of 0.6 is met by a trivial classifier.</b> Flagging every patient gives recall 1 and precision equal to the share of deaths. On the training rows, that is F2 = 5 × 0.3222 / (4 × 0.3222 + 1) = <b>0.7038</b>; on the full file it is 0.7028. That is above the target of 0.6, without any model. The "never flag" baseline (the most common class) scores F2 = 0.</li></ul>
<h3 style="margin-top:16px">Problem</h3>
<ul class="agent">
<li><b>Success criterion</b> (DR-08): <b>test F2 above the flag-everyone reference (F2 = 0.7038 on the training rows) by more than the spread of F2 across the 10 outer cross-validation folds</b>.
<ul><li><i>Superseded (DR-05):</i> "F2 clearly above the baseline's 0, with a target of F2 ≥ 0.6. The 0.6 is my own choice, not from the book." Replaced because flagging every patient already reaches F2 = 0.7038.</li></ul></li></ul>
<p class="more">… excerpt</p>"""
    return frame(f"{HF} — step 2", body, "light")


def hf_prior() -> str:
    body = """<h3>DR-13 · PRIOR · step 4</h3>
<p><b>Expectation:</b> <code>Logistic</code> ≈ <code>Logistic + L2</code> &gt; <code>Logistic + poly</code> &gt; <code>Tree</code>, with all four clearly above the most-common-class baseline. <span class="more">…</span></p>
<p style="margin-top:8px"><b>Decision:</b> … The prior order is <code>Logistic</code>, <code>Logistic + L2</code>, <code>Tree</code>, <code>Logistic + poly</code>.</p>
<p style="margin-top:14px"><b>Outcome vs expectation: disagree</b> (DR-15). The expected order was <code>Logistic</code> ≈ <code>Logistic + L2</code> &gt; <code>Logistic + poly</code> &gt; <code>Tree</code>. The CV order is <code>Tree</code> (0.5567) &gt; <code>Logistic + poly</code> (0.5286) &gt; <code>Logistic</code> = <code>Logistic + L2</code> (0.4798).</p>
<ul class="agent"><li>Two parts of the expectation held: <code>Logistic + L2</code> added nothing over <code>Logistic</code> …, and all four configurations clearly beat the most-common-class baseline.</li>
<li>Two parts did not: <code>Tree</code>, expected last, leads; and <code>Logistic + poly</code> is above <code>Logistic</code>.</li>
<li>… My reasoning about tree variance was not a matrix entry, and it was wrong here.</li></ul>"""
    return frame(f"{HF} — the prior ranking, and how it turned out", body, "light")


def hf_cv() -> str:
    rows = [("<code>Tree</code>", "depth 3, min leaf 20 (4/10 folds)", "0.5567", "leader", "+0.5567 ± 0.1124 (C2 clear)"),
            ("<code>Logistic + poly</code>", "degree 2 (8/10)", "0.5286", "−0.0281 ± 0.1422", "+0.5286 ± 0.1315 (C2 clear)"),
            ("<code>Logistic</code>", "none to tune", "0.4798", "−0.0769 ± 0.1357", "+0.4798 ± 0.1777 (C2 clear)"),
            ("<code>Logistic + L2</code>", "λ = 10⁻⁴ (8/10)", "0.4798", "−0.0769 ± 0.1357", "+0.4798 ± 0.1777 (C2 clear)"),
            ("Baseline (most common class)", "n/a", "0.0000", "−0.5567 ± 0.1124", "—"),
            ("Flag everyone", "n/a", "0.7032", "+0.1466 ± 0.1056", "+0.7032 ± 0.0181")]
    tr = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in rows)
    body = f"""<h3>DR-15 · CV · step 4</h3>
<p><b>CV table</b> (outer 10, inner 5, stratified, seed 2026; F2 at r = 0.5; margins as mean ± spread of the 10 fold differences)</p>
<table><tr><th>Configuration</th><th>Tuned hyperparameters (most common)</th><th>CV mean F2</th><th>Margin vs leader</th><th>Margin vs baseline (most common class)</th></tr>{tr}</table>
<p class="more">… columns Post-prior, E_train and E_val omitted</p>"""
    return frame(f"{HF} — cross-validation, round 2 (239 training patients)", body, "light")


def hf_final() -> str:
    rows = [("Test F2 (r = 0.2)", "0.6780"), ("Uncertainty (DR-08)", "fold SD of F2 across the 10 outer folds: 0.0865; n_test = 60, 19 positives"),
            ("Recall", "0.8421 (16 of 19 deaths flagged)"), ("Precision", "0.3810 (16 of 42 flagged patients died)"),
            ("Baseline (most common class), test", "F2 0"), ("Flag everyone, test (for context only)", "F2 0.6985"),
            ("Success criterion", "required: test F2 &gt; 0.7038 + 0.0865 = 0.7903; observed 0.6780: <b>not met</b>")]
    tr = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    body = f"""<h3>DR-19 · FINAL · step 4 — Test result</h3>
<p>(step 4g, run once on 14 October 2026; 60 test rows, 19 deaths)</p>
<table><tr><th>Item</th><th>Value</th></tr>{tr}</table>
<p><b>Confidence:</b> Low — C1 none (+0.0281 ± 0.1422 over <code>Logistic + poly</code>) · C2 clear (+0.5567 ± 0.1124) · C3 adequate … Prior agreement: disagree.</p>
<p style="margin-top:6px"><b>User involvement:</b> approved — "I approve a single evaluation of the recommended Tree on the test set." The user also said: "Do not change the model, threshold or criterion after seeing the result."</p>"""
    return frame(f"{HF} — the single test evaluation", body, "light")


if __name__ == "__main__":
    shoot("h1_problem", hf_problem(), 1300, 700)
    shoot("h2_prior", hf_prior(), 1300, 700)
    shoot("h3_cv", hf_cv(), 1300, 700)
    shoot("h4_final", hf_final(), 1300, 900)
    shoot("s1_chat", chat(), 1300, 830)
    shoot("s2_decision_record", decision_record(), 1300, 820)
    shoot("s3_core_terminal", core_terminal(), 1300, 640)
    shoot("s4_framework_diff", framework_diff(), 1300, 470)
    shoot("s5_calcium_terminal", calcium_terminal(), 1100, 600)
