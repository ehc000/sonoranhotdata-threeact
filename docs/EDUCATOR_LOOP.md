# Educator loop (Sonoran Hot Data)

The pedagogical core of the prototype: an educator prepares a competency-targeted,
interest-personalized question set and approves it; a student works it with a capped
tutor; the educator reviews a computed summary and approves what enters the student's
profile; the profile shapes the next preparation. No front end is included; the team
front end calls the HTTP surface in `backend/educator_loop/api.py`.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env         # then put the real key in .env yourself
uvicorn backend.educator_loop.api:app --reload
```

`MOCK_LLM=1` runs every path offline with canned replies (marked `MOCK:` in code).
`PROMPT_LOG=1` writes every model request to `logs/model_calls.jsonl` (ignored by git)
for `scripts/check_prompt_coverage.py`. Tests: `pytest` from the repo root (they set
`MOCK_LLM` themselves).

## Architecture

[CUE: paste the architecture diagram from docs/ARCHITECTURE.md or describe the two loops in your words]

Loop 1, preparation: `create_prep` filters the bank to the chosen competencies, asks the
model to pick ids according to the educator's instructions, asks it to rewrite each pick
around the student's interest with every number fixed, and checks in code that numbers and
(for bare-arithmetic questions) the literal expression survived. The educator edits,
rejects or regenerates per question and approves.

Loop 2, session: the student answers in any order with up to three tutor turns per question;
`finish_session` computes per-competency accuracy, help use, time-on-task, a proficiency
score, a ranking, blocker detection over the prerequisite graph, and a partial knowledge
graph, plus one model-written summary; the educator overrides statuses if needed and
approves; the profile stores the result and informs the next preparation.

## What the model does and does not do

The model picks questions, rewrites situations, gives hints, and writes the summary.
Answer keys come from templates (computed), and grading, scores, ranking, blockers and the
graph are computed from the session log. The educator approves before a student sees a
question and before anything enters a profile.

## Mocks and known limitations

- `MOCK:` paths in `backend/llm_query.py` and `engine.py` return canned text when no key is set.
- Grading is normalized string / fraction comparison; an unknown unit word marks a right answer wrong.
- The numeral and expression checks catch a lost number or a dropped expression, not a changed question; the educator's review is the real guard.
- Time-on-task starts when the client calls `/open`; help-seeking is measured as turn counts only.
- State is in memory and resets on restart.

## AI use and attribution

[CUE: write this section yourself. It needs four facts:]
- [Tools and model versions used, and for which parts of the repo: this module was generated with Claude (claude.ai chat), model Claude Fable 5.1, on 2026-11-02, in a session directed by Torian Styles; see docs/AI_USAGE_LOG.md]
- [What the team originated: problem definition, the design decisions in docs/DECISIONS.md, prompt wording in prompts/, test cases, data choices]
- [How AI output was reviewed before each commit, and by whom]
- [Where the detail lives: ATTRIBUTION.md, file headers, commit messages, docs/AI_USAGE_LOG.md]
