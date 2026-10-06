---
name: receiving-code-review
description: >
  Act on code review feedback — each item being one change a reviewer asks for, so a comment asking for two changes holds two items — by verifying each against the code, clarifying every unclear item before implementing any, pushing back with evidence, and implementing one item at a time.
  "address the review", "review comments to handle", "PR feedback", "should I implement this suggestion", "the reviewer says",
  or any reply to review findings.
---

<read-everything-first>
Read all the feedback before acting on any item; never start on the first item while later ones are unread.

Restate each clear item as the change it asks for, and quote each unclear item as written, in one sentence each in the first message to the user; never restate an item as agreement or thanks.
</read-everything-first>

<verify-each-item>
Verify each item against the code: whether the problem exists, whether the item's change breaks existing behavior, why the current code is as it is, and whether the change holds on every operating system and language-runtime version the project declares as supported in its configuration or exercises in its continuous integration, a platform that cannot run here counting as unverifiable; never implement an item unverified.

Search the codebase for callers — code outside the tests that calls the feature today — of a feature a reviewer asks to extend; never extend a feature without the search.

Propose removal of the feature when it has no caller; never build or extend a feature that has no caller.
</verify-each-item>

<clarify-before-implementing>
Hold every item while any item is unclear; never implement the clear items first.

Ask the user about all the unclear items at once — as a dispatched agent, by reporting `NEEDS_CONTEXT` with the items named; never ask about them one at a time.

State what cannot be verified and what would verify it when verification is impossible here; never leave an unverifiable item unstated.

Hold an unverifiable item alone, unless it is also unclear; never proceed on it.
</clarify-before-implementing>

<push-back-with-evidence>
Hand an item that contradicts an architectural decision the user stated in the session or recorded in `CLAUDE.md` to the user before pushing back on it or changing that item; never settle such a conflict with the reviewer alone.

Push back, in the reply to the user, on an item whose change breaks existing behavior, that lacks the codebase's context, that builds what has no caller, or that is wrong for this stack — with the test, the code, or the fact that shows it; never push back with preference.

Correct a wrong pushback in one sentence naming what was verified and what it showed; never defend the pushback.

Implement the item after the correction; never leave a corrected item unimplemented.
</push-back-with-evidence>

<implement-one-at-a-time>
Implement the items in order: those fixing a crash, data loss, or a security hole, then the simple ones — typos, imports, names, then the complex ones — logic, structure, tests; never implement in the order they were written.

Implement one item at a time; never implement two before a test run.

Run the tests after each item; never start the next item before the run.

Fix the item or the test when a test fails; never move to the next item on a failing run.
</implement-one-at-a-time>

<answer-without-performance>
Answer each item, in the reply to the user, with the change made and where, the evidence against it, or what holds it; never answer with gratitude, praise, agreement, or an announcement of what is about to happen.

Mark each item `Implemented`, `Held` — unclear, or clear and waiting on an unclear item — or `Needs discussion` — pushed back, unverifiable, or handed to the user — when the feedback carries several items; never leave an item's state unstated.
</answer-without-performance>
