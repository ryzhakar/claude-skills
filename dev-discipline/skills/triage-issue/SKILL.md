---
name: triage-issue
description: >
  Diagnose a reported bug to its root cause and write an issue document carrying a test-first fix plan, without fixing the code.
  "triage this", "this is broken", "investigate a bug", "find the root cause and file it", "write up this bug", "file an issue",
  or any bug report that asks for a diagnosis rather than a fix.
---

<take-the-problem-statement>
Take the problem — what the reporter sees and what they expected — from the request; never start without one.

Ask one question, `What problem are you seeing?`, when the request names no problem; never ask a second question.
</take-the-problem-statement>

<investigate-the-cause>
Run the investigation of `systematic-debugging` — reproduce and read, trace to the source, compare with working code, test one hypothesis — up to its fix step; never change product code during triage.

Find where the bug surfaces, which code path carries it, why that path produces the wrong result, and what other code shares the same pattern; never stop at the first of the four.
</investigate-the-cause>

<classify-the-issue>
Classify the issue as a regression — it worked before, a missing feature — it was never built, or a design flaw — it works as written and is written wrong; never leave it unclassified.

State the scope — one module, an integration between modules, or a systemic pattern — the smallest change that fixes the cause, and the outermost interfaces the fix touches; never state a fix wider than the cause.
</classify-the-issue>

<plan-the-fix>
Write the fix plan as an ordered sequence of red-green cycles in the shape `tdd` prescribes: each cycle names one test through the unit's outermost interface and the least change that passes it; never write all tests before any change.

Describe each test as the behavior a caller observes; never describe it by a file path, a line number, or a private function.

Add one refactor step after the last cycle when cleanup is needed; never put a refactor between cycles.
</plan-the-fix>

<write-the-issue>
Write the issue document to the project's issue directory — `issues/`, `docs/issues/`, or the directory the project already uses — with four sections: `Problem` (actual behavior, expected behavior, reproduction), `Root cause` (the path, the mechanism, the contributors), `Fix plan` (the cycles), and `Acceptance criteria` (the cause is fixed, the new tests pass, the existing tests pass, adjacent behavior holds); never return the document as conversation text.

Describe modules, behaviors, and contracts in the document; never describe file paths or line numbers, so a refactor leaves it true.

Print the document's path and the root cause in one sentence; never print more.
</write-the-issue>

<handle-the-exceptions>
Write the document with the hypotheses tested and why reproduction failed when the bug cannot be reproduced; never withhold a partial diagnosis.

Write one document per independent cause when the investigation finds several, each naming the others; never merge two causes into one document.

Name `improve-architecture` in the document when the cause is a design flaw that needs a new module boundary; never plan a design change as a sequence of fixes.
</handle-the-exceptions>
