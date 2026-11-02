# Test cases

Executable versions live in `tests/test_educator_loop.py` (offline, MOCK path).

1. The bank has 240 questions with unique ids, and every answer key grades as correct against itself.
2. Every prompt file in `prompts/` loads with a system section; `{{variables}}` fill.
3. Grading accepts "x = 36", "11/10" for 1.1, "56 cups", "2:3", "43.20 dollars"; rejects non-answers.
4. A rewrite that drops a signed number or paraphrases a framing-mode expression is flagged; a rewrite that keeps the expression verbatim is not; "3:7" written as "3 to 7" passes.
5. Full loop: prep → edit (flagged when numbers removed) → reject one → approve → answer → finish → statuses and a fractions→ratios blocker → approve review → profile holds statuses and the interest.
6. A second prep for the same student reuses the saved interest and skips level-1 questions in a mastered competency.
7. The tutor stops replying after HELP_CAP turns on one question.

[CUE: add the cases that matter to the team's user path, in your words.]
