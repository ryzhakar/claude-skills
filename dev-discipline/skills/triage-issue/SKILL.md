---
name: triage-issue
description: >
  Diagnose a reported bug to its root cause and write an issue document carrying a test-first fix plan, without fixing the code.
  "triage this", "this is broken", "investigate a bug", "find the root cause and file it", "write up this bug", "file an issue",
  or any bug report that asks for a diagnosis rather than a fix.
---

<take-the-problem-statement>
Take the problem — what the reporter sees and, when stated, what they expected — from the request; never start without one.

Ask one question, `What problem are you seeing?`, when the request names no problem; never ask a second question.
</take-the-problem-statement>

<investigate-the-cause>
Run the investigation of `systematic-debugging` — reproduce and read, trace to the source, compare with working code, test one hypothesis — up to its fix step; never change product code during triage.

Find where the bug surfaces, which code path carries it, why that path produces the wrong result, and what other code shares the same pattern — the faulty construct behind the cause; never stop at the first of the four.
</investigate-the-cause>

<classify-the-issue>
Split the issue into one issue per cause when the investigation finds several independent causes — causes that each need their own fix; never merge two such causes into one issue.

Classify each issue as a regression — it worked before, a missing feature — it was not built, or a design flaw — it works as written and is written wrong; never leave one unclassified.

State for each issue the scope — one module, an integration between modules, or a systemic pattern — the smallest change that fixes the cause, and the outermost interfaces — the functions or endpoints that callers outside the changed module use — the fix touches; never state a fix wider than the cause.
</classify-the-issue>

<plan-the-fix>
Name `improve-architecture` as the fix when the cause is a design flaw that needs a new module boundary; never plan such a flaw as a sequence of fixes.

Write the fix plan as an ordered sequence of red-green cycles in the shape `tdd` prescribes, each cycle naming one test through the unit's outermost interface and the least change that passes it; never write all tests before any change.

Describe each test as the behavior a caller observes; never describe it by a file path, a line number, or a private function.

Add one refactor step after the last cycle when cleanup is needed; never put a refactor between cycles.
</plan-the-fix>

<write-the-issue>
Write one issue document per issue to the project's issue directory — `issues/`, `docs/issues/`, or the directory the project already uses, created as `docs/issues/` when none exists — named `<slug>.md` with `<slug>` the issue's title in lowercase hyphenated words; never return a document as conversation text.

Give each document a title and four sections: `Problem` — actual behavior, expected behavior, reproduction; `Root cause` — the classification, where the bug surfaces, the code path, why the path fails, the other code sharing the pattern; `Fix plan` — the scope, the smallest change, the outermost interfaces touched, the cycles, the refactor step; `Acceptance criteria` — the cause is fixed, the new tests pass, the existing tests pass, the behavior of the other code sharing the pattern is unchanged by the fix; never leave a section out.

Write the hypotheses tested and why reproduction failed in the `Root cause` section when the bug cannot be reproduced; never withhold a partial diagnosis.

Write `none` beside any item an issue cannot fill; never leave an item blank.

Write `improve-architecture` in `Fix plan` in place of the cycles for a design flaw handed to it; never write cycles for such a flaw.

Add the acceptance of the RFC — the proposal `improve-architecture` writes — as a further item in `Acceptance criteria` for such a flaw; never leave its acceptance out.

Cite each sibling document — another issue from the same investigation — by its title in the `Root cause` section of each document; never leave a sibling uncited.

Describe modules, behaviors, and contracts in the document; never describe file paths or line numbers.

Print each document's path, then its root cause in one sentence; never print more.
</write-the-issue>
