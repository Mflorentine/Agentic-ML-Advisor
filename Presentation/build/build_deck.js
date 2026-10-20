// Builds Presentation/Agentic ML Advisor.pptx: the advisor explained, with the Heart Failure analysis as the worked example.
// Every number on the slides is copied from Demonstration/Heart Failure/ (report and appendix) or its outputs.
// Screens come from make_screenshots.py; figures from Code/outputs/figures/ (Heart Failure).
//
// Run:  NODE_PATH=<folder with pptxgenjs> node Presentation/build/build_deck.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL + "/scripts/apply_theme.js");

const ROOT = path.resolve(__dirname, "..", "..");
const SCR = (f) => path.join(__dirname, "screens", f);
const FIG = (f) => path.join(ROOT, "Code", "outputs", "figures", f);
const OUTFILE = path.join(ROOT, "Presentation", "Agentic ML Advisor.pptx");

const THEME = {
  name: "Agentic ML Advisor",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2631", lt1: "FFFFFF", dk2: "0E4D57", lt2: "EEF3F4",
    accent1: "0E7C86", accent2: "E0703A", accent3: "6C8A93", accent4: "2A78D6",
    accent5: "1BAF7A", accent6: "8E5BA8", hlink: "0E7C86", folHlink: "6C8A93",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.title = "An agentic ML advisor that works the way the book does";
pres.author = "Florentine Mukamana";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---- Layouts ----
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: HEX.dk2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.7, h: 1.9, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.1, w: 11.7, h: 1.6, fontSize: 18, color: C.background2, valign: "top" }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: HEX.lt1 },
  margin: [0.5, 0.6, 0.5, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 30, bold: true, color: C.text2, valign: "middle", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.4, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: HEX.accent3 },
});
pres.defineSlideMaster({
  title: "SECTION",
  background: { color: HEX.lt2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.6, w: 11.7, h: 1.2, fontSize: 36, bold: true, color: C.text2, valign: "bottom", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 3.9, w: 11.7, h: 1.0, fontSize: 18, color: C.text1, valign: "top" }, text: "" } },
  ],
  slideNumber: { x: 12.4, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: HEX.accent3 },
});

// ---- Helpers ----
function circleNum(slide, n, x, y, d, fill) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill || C.accent1 }, line: { color: fill || C.accent1 }, objectName: `circle ${n}` });
  slide.addText(String(n), { x, y, w: d, h: d, align: "center", valign: "middle", fontSize: d > 0.6 ? 20 : 14, bold: true, color: C.background1, margin: 0, isTextBox: true });
}
function fitImage(slide, file, pxW, pxH, x, y, maxW, maxH, name) {
  const r = pxW / pxH;
  let w = maxW, h = maxW / r;
  if (h > maxH) { h = maxH; w = maxH * r; }
  slide.addImage({ path: file, x: x + (maxW - w) / 2, y, w, h, objectName: name });
  return { w, h, x: x + (maxW - w) / 2 };
}
function source(slide, text, y) {
  slide.addText(text, { x: 0.6, y: y || 6.95, w: 11.5, h: 0.35, fontSize: 10, italic: true, color: C.accent3, margin: 0, isTextBox: true });
}
function sideCard(slide, x, y, w, h, title, body) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: `card ${title}` });
  slide.addText([
    { text: title, options: { bold: true, fontSize: 16, color: C.text2, breakLine: true } },
    { text: body, options: { fontSize: 14, color: C.text1 } },
  ], { x: x + 0.2, y: y + 0.12, w: w - 0.4, h: h - 0.24, valign: "top", margin: 0, paraSpaceAfter: 4, isTextBox: true });
}

// ---- 1. Title ----
pres.addSection({ title: "The idea" });
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "The idea" });
s.addText("An agentic ML advisor that works the way the book does", { placeholder: "title" });
s.addText([
  { text: "Machine learning guidance from Lindholm et al., chapters 2, 3, 4 and 13 — with the Heart Failure analysis as a worked example", options: { breakLine: true } },
  { text: "Florentine Mukamana · CoRE AI research visit · October 2026", options: { fontSize: 15 } },
], { placeholder: "body" });
s.addNotes("This talk explains the agentic ML advisor: what it is for, how it works, and what it did on a real analysis. Everything shown comes from the files in the workspace; the 'screenshots' are renders of real excerpts, each labelled with its source.");

// ---- 2. The aim ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The idea" });
s.addText("The aim: a report the book's authors would recognise", { placeholder: "title" });
s.addText([
  { text: "An AI agent works through a supervised ML problem with the user, one step at a time.", options: { breakLine: true } },
  { text: "Every rule it follows is judged by one test: is this how Lindholm, Wahlström, Lindsten and Schön would work?", options: {} },
], { x: 0.6, y: 1.45, w: 4.6, h: 3.0, fontSize: 18, color: C.text1, valign: "top", paraSpaceAfter: 12, margin: 0, isTextBox: true });
s.addText("Machine Learning – A First Course for Engineers and Scientists, 2nd ed. (smlbook.org)", { x: 0.6, y: 4.7, w: 4.6, h: 0.8, fontSize: 13, italic: true, color: C.accent3, margin: 0, isTextBox: true });
const aims = [
  ["Predict, don't explain", "The aim is the output for new cases, not how variables are connected (p. 20)"],
  ["Define the problem first", "Validation and test data, one metric and a baseline, agreed before any model (pp. 327–331)"],
  ["Start simple", "Add complexity only when the errors call for it (pp. 331–337)"],
  ["Compare by cross-validation, test once", "The chosen model meets the test set a single time (pp. 72–74, 328)"],
  ["Report E_new", "An average-case estimate on data like the evaluation data (pp. 68–69, 347)"],
];
aims.forEach(([h, b], i) => {
  const y = 1.45 + i * 1.02;
  circleNum(s, i + 1, 5.8, y + 0.08, 0.55);
  s.addText([
    { text: h, options: { bold: true, fontSize: 17, color: C.text2, breakLine: true } },
    { text: b, options: { fontSize: 14, color: C.text1 } },
  ], { x: 6.55, y, w: 6.2, h: 0.9, valign: "top", margin: 0, isTextBox: true });
});
s.addNotes("The Purpose section of instructions.md: the work should end in a report consistent with how the book's authors would work. These five principles come from ML Guide.md Part I, with the book's page numbers.");

// ---- 3. How it works ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The idea" });
s.addText("Four parts, each with one job", { placeholder: "title" });
const boxes = [
  ["The user", "Directs every step, answers the questions only they can answer, makes every call", C.accent2],
  ["The agent", "Claude Code, bound by instructions.md and ML Guide.md: asks, explains, checks, writes the records", C.accent1],
  ["The deterministic core", "Python / scikit-learn: properties, admissible set, prior ranking, nested CV, recommendation", C.text2],
  ["The records", "Appendix.md: Decision Records and log. Report.md: built up step by step", C.accent3],
];
boxes.forEach(([h, b, col], i) => {
  const x = 0.6 + i * 3.15;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.75, w: 2.8, h: 3.1, rectRadius: 0.15, fill: { color: col }, line: { color: col }, objectName: `box ${h}` });
  s.addText([
    { text: h, options: { bold: true, fontSize: 20, color: C.background1, breakLine: true } },
    { text: b, options: { fontSize: 14, color: C.background1 } },
  ], { x: x + 0.2, y: 1.9, w: 2.4, h: 2.8, valign: "top", paraSpaceAfter: 10, margin: 0, isTextBox: true });
  if (i < 3) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + 2.83, y: 3.12, w: 0.29, h: 0.36, fill: { color: C.accent3 }, line: { color: C.accent3 }, objectName: `arrow ${i}` });
});
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 5.3, w: 12.1, h: 1.2, rectRadius: 0.12, fill: { color: C.background2 }, line: { color: C.background2 }, objectName: "principle" });
s.addText([
  { text: "Rules propose, cross-validation decides, the trace explains. ", options: { bold: true, color: C.text2 } },
  { text: "The agent never computes the mechanical parts itself: it passes inputs to the core and copies the outputs into the records unchanged, with the code's SHA-256.", options: { color: C.text1 } },
], { x: 0.85, y: 5.4, w: 11.6, h: 1.0, fontSize: 16, valign: "middle", margin: 0, isTextBox: true });
s.addNotes("ML Guide.md §7. Until Code/advisor/ is built, each analysis has an interim core (Code/sepsis/core.py), shown to the user before its first output is used and labelled 'interim core, not reviewed'.");

// ---- 4. Five steps ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The idea" });
s.addText("Five steps, one at a time, closed by the user", { placeholder: "title" });
const steps = [
  ["Import and scope", "Provenance, units, missing data, leakage; admissibility questions"],
  ["Define the problem", "Target, metric, baseline, success criterion; test set locked"],
  ["Explore training data", "Input design, P9–P10 from the core, figures"],
  ["Select, train, evaluate", "Admissible set, prior, nested CV, diagnosis, one test"],
  ["Conclusions", "What the results support, and what they do not"],
];
s.addShape(pres.shapes.LINE, { x: 1.0, y: 2.25, w: 10.9, h: 0, line: { color: HEX.accent3, width: 2 }, objectName: "timeline" });
steps.forEach(([h, b], i) => {
  const x = 0.6 + i * 2.45;
  const done = true;
  circleNum(s, i + 1, x + 0.6, 1.9, 0.7, done ? C.accent1 : C.accent3);
  s.addText([
    { text: h, options: { bold: true, fontSize: 17, color: C.text2, breakLine: true } },
    { text: b, options: { fontSize: 14, color: C.text1 } },
  ], { x, y: 2.85, w: 2.2, h: 2.0, valign: "top", align: "left", paraSpaceAfter: 6, margin: 0, isTextBox: true });
});
s.addText([
  { text: "Each step ends with a written check: ", options: { bold: true, color: C.text2 } },
  { text: "what is settled, what was never discussed — then the agent waits. All five were completed on Heart Failure.", options: { color: C.text1 } },
], { x: 0.6, y: 4.75, w: 12.1, h: 0.8, fontSize: 16, margin: 0, isTextBox: true });
s.addNotes("From instructions.md, The Five Steps. The agent asks 'have we thought of everything in step 2?' rather than 'shall we move on?'. The Heart Failure analysis went through all five; the Sepsis analysis has closed steps 1 to 3.");

// ---- 5. Provenance ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "The idea" });
s.addText("Every rule says how much of it is the book's", { placeholder: "title" });
const tags = [
  ["[B]", "Explicit book advice", "e.g. split by group where rows share a unit (p. 329)"],
  ["[B→I]", "A book fact we turned into advice", "e.g. the imbalanced diagnosis error (p. 91)"],
  ["[I]", "Our own inference or threshold", "e.g. P10 imbalanced if smallest class < 20 %"],
];
tags.forEach(([t, h, e], i) => {
  const y = 1.5 + i * 1.45;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y, w: 1.6, h: 1.15, rectRadius: 0.12, fill: { color: [C.text2, C.accent1, C.accent2][i] }, line: { color: [C.text2, C.accent1, C.accent2][i] }, objectName: `tag ${t}` });
  s.addText(t, { x: 0.6, y, w: 1.6, h: 1.15, align: "center", valign: "middle", fontSize: 24, bold: true, color: C.background1, margin: 0, isTextBox: true });
  s.addText([
    { text: h, options: { bold: true, fontSize: 17, color: C.text2, breakLine: true } },
    { text: e, options: { fontSize: 14, color: C.text1 } },
  ], { x: 2.45, y: y + 0.1, w: 4.0, h: 1.0, valign: "top", margin: 0, isTextBox: true });
});
sideCard(s, 7.0, 1.5, 5.7, 2.05, "Evidence tags on every value", "M metadata or the user (from step 2) · T training data (step 3) · CV cross-validation (step 4) · TEST the single final evaluation");
sideCard(s, 7.0, 3.85, 5.7, 2.05, "A small, fixed solution space", "14 configurations from chapters 2–3: k-NN, decision tree, linear, logistic, Poisson and exponential GLMs, with polynomial terms and L2 where allowed. Anything else is flagged, never used.");
s.addNotes("ML Guide.md §8 and §9. Tags are copied into Decision Records unchanged and never upgraded, so a reader can count how much of a recommendation rests on the book and how much on our own thresholds.");

// ---- 6. Section: Heart Failure ----
pres.addSection({ title: "Worked example" });
s = pres.addSlide({ masterName: "SECTION", sectionTitle: "Worked example" });
s.addText("Worked example: death during heart failure follow-up", { placeholder: "title" });
s.addText("Heart Failure Clinical Records, UCI (2020): NYHA class III–IV patients, two hospitals in Faisalabad, Pakistan, 2015", { placeholder: "body" });
const stats = [["299", "patients in the file"], ["239 / 60", "training / test patients"], ["32.2 %", "of training patients died"], ["F2", "one metric for model, threshold and success"]];
stats.forEach(([n, l], i) => {
  const x = 0.9 + i * 3.0;
  s.addText([
    { text: n, options: { fontSize: 36, bold: true, color: C.accent1, breakLine: true } },
    { text: l, options: { fontSize: 14, color: C.text1 } },
  ], { x, y: 5.1, w: 2.8, h: 1.3, valign: "top", margin: 0, isTextBox: true });
});
s.addNotes("The finished reference analysis, Demonstration/Heart Failure. The user's problem: 'Flag heart failure patients at high risk of dying during follow-up, so they can be monitored more closely.' Eleven inputs; follow-up time is in the file but not used, because it ends when the outcome happens.");

// ---- 7. Step 2: problem fixed first ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Worked example" });
s.addText("Step 2: the problem is fixed before any model", { placeholder: "title" });
fitImage(s, SCR("h1_problem.png"), 2600, 976, 0.6, 1.4, 8.4, 5.3, "screen problem");
sideCard(s, 9.3, 1.4, 3.4, 1.55, "Prediction, not explanation", "\"The aim is prediction for new patients, not explaining causes\" (ADM-2, p. 20).");
sideCard(s, 9.3, 3.15, 3.4, 1.55, "One metric", "F2 counts recall twice as heavily as precision: a missed death costs more than a false alarm (p. 92).");
sideCard(s, 9.3, 4.9, 3.4, 1.65, "A weak target caught", "Flagging everyone already scores 0.7038, so the target of 0.6 was replaced before any model.");
source(s, "Render of Demonstration/Heart Failure/Demonstration Appendix.md, Problem Definition (excerpt).");
s.addNotes("The test set was locked at the end of step 2: 60 patients, stratified by outcome, seed 2026. The success criterion is test F2 above flag-everyone (0.7038 on the training patients) by more than the fold spread of F2.");

// ---- 8. Step 3: figures ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Worked example" });
s.addText("Step 3: the training data, before any model", { placeholder: "title" });
fitImage(s, FIG("fig1_numeric_by_outcome.png"), 2646, 1492, 0.6, 1.4, 6.6, 4.3, "figure 1");
fitImage(s, FIG("fig3_creatinine_ejection.png"), 2231, 1374, 7.45, 1.4, 5.25, 4.3, "figure 3");
s.addText([
  { text: "Blue: no death; orange: died. ", options: { bold: true, color: C.text2 } },
  { text: "239 training patients; the 60 held-out patients are not shown. The user expected higher creatinine and lower ejection fraction to go with risk — a direction, recorded in their words, not a shape, so P8 stays unknown.", options: { color: C.text1 } },
], { x: 0.6, y: 5.75, w: 12.1, h: 0.95, fontSize: 15, valign: "top", margin: 0, isTextBox: true });
source(s, "Figures 1 and 3 of Demonstration/Heart Failure/Demonstration Report.md.");
s.addNotes("Serum creatinine and creatinine phosphokinase enter every model as logarithms (DR-11, the user's decision). Figures never set the expected shape of a relationship.");

// ---- 9. Step 4: prior vs CV ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Worked example" });
s.addText("The prior records an expectation — this one was wrong", { placeholder: "title" });
fitImage(s, SCR("h2_prior.png"), 2600, 930, 0.6, 1.4, 8.4, 5.3, "screen prior");
sideCard(s, 9.3, 1.4, 3.4, 1.55, "Rules propose", "The ranking kept the baseline, plain logistic regression and the three highest-ranked others.");
sideCard(s, 9.3, 3.15, 3.4, 1.55, "Cross-validation decides", "The tree, expected last, came first.");
sideCard(s, 9.3, 4.9, 3.4, 1.65, "Recorded, not explained away", "The disagreement is a finding; the record says which reasoning was wrong.");
source(s, "Render of Demonstration/Heart Failure/Demonstration Appendix.md, DR-13 (excerpt).");
s.addNotes("The prior entries that favoured logistic regression concern inspectability and probabilities, not predictive fit, so the disagreement on F2 does not contradict them.");

// ---- 10. CV table ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Worked example" });
s.addText("Cross-validation decides; simplicity breaks the tie", { placeholder: "title" });
fitImage(s, SCR("h3_cv.png"), 2600, 1040, 0.6, 1.4, 12.1, 4.0, "screen cv");
const tie = [["Tree vs Logistic + poly", "0.5567 vs 0.5286: a difference of 0.03 against a fold spread of 0.14"], ["Can't be told apart", "below half the spread (§19), so the one with fewer add-ons wins: the tree (p. 332)"], ["Selection confidence: Low", "clear over the baseline, but not over the runner-up"]];
tie.forEach(([h, b], i) => {
  const x = 0.6 + i * 4.1;
  circleNum(s, i + 1, x, 5.65, 0.55);
  s.addText([
    { text: h, options: { bold: true, fontSize: 16, color: C.text2, breakLine: true } },
    { text: b, options: { fontSize: 14, color: C.text1 } },
  ], { x: x + 0.7, y: 5.6, w: 3.2, h: 1.25, valign: "top", margin: 0, isTextBox: true });
});
source(s, "Render of Demonstration/Heart Failure/Demonstration Appendix.md, DR-15 (excerpt).");
s.addNotes("Nested cross-validation: 10 outer folds, the same for every configuration; 5 inner folds tune depth, leaf size, penalty and degree. Models compared on F2 at a threshold of 0.5. Flag-everyone scores 0.7032 in cross-validation.");

// ---- 11. Test once ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Worked example" });
s.addText("One test, approved by the user, reported as found", { placeholder: "title" });
fitImage(s, SCR("h4_final.png"), 2600, 1288, 0.6, 1.4, 8.4, 5.3, "screen final");
sideCard(s, 9.3, 1.4, 3.4, 1.55, "Approved first", "The test set was used once, only after the user approved it.");
sideCard(s, 9.3, 3.15, 3.4, 1.55, "Checked twice", "The test F2 was recomputed independently from the saved predictions.");
sideCard(s, 9.3, 4.9, 3.4, 1.65, "Nothing moved after", "\"Do not change the model, threshold or criterion after seeing the result.\"");
source(s, "Render of Demonstration/Heart Failure/Demonstration Appendix.md, DR-19 (excerpt).");
s.addNotes("The final tree: depth 3, at least 20 patients per leaf, threshold 0.2 chosen from out-of-fold probabilities on the training patients only.");

// ---- 12. What it supports ----
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Worked example" });
s.addText("The success criterion was not met — and the report says so", { placeholder: "title" });
fitImage(s, FIG("fig4_pr_curve.png"), 2035, 1374, 0.6, 1.4, 6.2, 4.6, "figure 4");
const res = [["0.68", "test F2 of the tree (fold spread 0.09)"], ["0.70", "test F2 of flagging every patient"], ["16 of 19", "deaths flagged (recall 0.84)"], ["16 of 42", "flagged patients died (precision 0.38)"]];
res.forEach(([n, l], i) => {
  const x = 7.2 + (i % 2) * 2.85, y = 1.5 + Math.floor(i / 2) * 1.55;
  s.addText([
    { text: n, options: { fontSize: 32, bold: true, color: i === 1 ? C.accent3 : C.accent1, breakLine: true } },
    { text: l, options: { fontSize: 14, color: C.text1 } },
  ], { x, y, w: 2.65, h: 1.35, valign: "top", margin: 0, isTextBox: true });
});
s.addText([
  { text: "Success needed F2 above 0.79. ", options: { bold: true, color: C.text2 } },
  { text: "With 19 deaths among 60 held-out patients, only large differences in F2 can be detected. The result is an average over patients like these; it says nothing about the worst individual prediction (p. 347).", options: { color: C.text1 } },
], { x: 7.2, y: 4.7, w: 5.5, h: 1.8, fontSize: 15, valign: "top", margin: 0, isTextBox: true });
source(s, "Figure 4 and Results of Demonstration/Heart Failure/Demonstration Report.md.");
s.addNotes("The required F2 was 0.7038 plus the fold spread 0.0865, i.e. 0.7903. The tree flags 42 of 60 patients; in practice it differs from flagging everyone only through one low-risk group, which the held-out patients do not show to be safe.");

// ---- 13. Status ----
pres.addSection({ title: "Where it stands" });
s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Where it stands" });
s.addText("Where it stands", { placeholder: "title" });
s.addText([
  { text: "Heart Failure: all five steps done; kept as the reference", options: { bullet: true, breakLine: true } },
  { text: "Sepsis (PhysioNet 2019): steps 1–3 closed; it prompted one FRAMEWORK change, the diagnosis error for imbalanced classes (p. 91)", options: { bullet: true, breakLine: true } },
  { text: "Next: Sepsis step 4, then the Mobile Price dataset", options: { bullet: true, breakLine: true } },
  { text: "Then: build Code/advisor/ from the interim cores", options: { bullet: true } },
], { placeholder: "body" });
s.addNotes("Each dataset is used to move the method closer to the book: where the contract or the guide leads to something the authors would not do, it is changed under FRAMEWORK and the change is logged in the analysis that prompted it.");

(async () => {
  await pres.writeFile({ fileName: OUTFILE });
  await applyTheme(OUTFILE, THEME);
  console.log("wrote", OUTFILE);
})();
