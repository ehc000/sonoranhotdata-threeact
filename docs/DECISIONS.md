# Design decisions

[CUE: these entries are reconstructed from the 2026-11-02 build session; rewrite each in your own words and delete any you don't stand behind.]

## 2026-11-02 — Question bank is template-generated, not model-generated
Two hundred-plus questions with trustworthy answer keys, fast. Templates compute the answer, so keys are correct by construction and ids are stable across restarts. The cost is less surface variety, which the rewrap step supplies. Rejected: generating the bank with the model once and vetting it (a few percent wrong keys until someone checks all of them); hand-authoring (no time).

## 2026-11-02 — The model picks, rewrites, hints and summarizes; everything else is computed
Grading, proficiency score, ranking, blocker detection and the knowledge graph come from the session log in code, so the educator reviews numbers rather than model prose. The summary is model-written but decorative to the decision.

## 2026-11-02 — Six competencies with a prerequisite DAG
integers → fractions → ratios → percentages; integers, fractions → linear equations; ratios, linear equations → proportions. A weak root can block several dependents, which is the demo moment for blocker detection.

## 2026-11-02 — Score and thresholds
score = 0.7 × accuracy + 0.3 × (1 − help_rate), with help_rate = tutor turns / (questions × cap). mastered ≥ 0.75, developing ≥ 0.40, struggling below. A blocker is a prerequisite that is developing or struggling under a dependent that is also developing or struggling; blockers carried over from the profile are labelled as such.

## 2026-11-02 — Interest rewrap runs before the session, under educator approval
Every rewrite is shown beside the bank text with edit / reject / regenerate. Two modes: `full` (word problems; the whole situation may move) and `framing` (bare expressions; one clause of context, expression verbatim). Code checks that every number survives (sign included) and that framing expressions appear literally; the educator catches changed meaning.

## 2026-11-02 — Tutor help is capped at three turns per question
Help use is a signal for the educator, so it is counted, not unlimited. Latency-based signals deferred.

## 2026-11-02 — No image generation for now
Considered illustrating word problems; deferred on cost (two orders of magnitude over text), latency, and the risk of images that contradict the quantities in the problem.
