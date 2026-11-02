# AI usage log

| Date | Tool / model | What was generated | Human direction | Reviewed by / how |
|---|---|---|---|---|
| 2026-11-02 | Claude, claude.ai chat app, Claude Fable 5.1 | `backend/educator_loop/*` (question bank, engine, prompt loader, API router); rewrite of `backend/llm_query.py` into the shared model wrapper (original by a teammate, see its header), `prompts/*` draft wording, `tests/`, `scripts/check_prompt_coverage.py`, this docs skeleton | Torian Styles set the scope (two loops + bank, template-generated answers, interest rewrap with educator approval), chose the six competencies, and reported bugs from live runs (negative-number framing, repeated "toys" framing, parser shape, dropped expression) that drove the guards in `engine.check_rewrap` | Torian Styles ran the app end to end against the live OpenAI API and the test suite offline. [CUE: note anything you changed by hand] |

Note: this code was produced in the chat app, not Claude Code, so commits carry no automatic
trailer; the commit message names the tool and model instead, per CONTRIBUTING.md.
