---
name: receiving-code-review
description: >
  Act on code review feedback by verifying each item against the code, clarifying every unclear item before implementing any, pushing back with evidence, and fixing one item at a time.
  "address the review", "review comments to handle", "PR feedback", "should I implement this suggestion", "the reviewer says",
  or any reply to review findings.
---

<read-everything-first>
Read all the feedback before acting on any item; never start on the first item while later ones are unread.

Restate each item as the change it asks for, in one sentence; never restate it as agreement or thanks.
</read-everything-first>

<verify-each-item>
Check each item against the code: whether the problem exists, whether the suggested change breaks existing behavior, why the current code is as it is, and whether the suggestion holds on every target platform and version; never implement an item unverified.

Search the codebase for callers of a feature a reviewer asks to build out, and propose removal when nothing calls it; never build infrastructure for a caller that does not exist.
</verify-each-item>

<clarify-before-implementing>
Hold every item while any item is unclear, and ask about all the unclear items at once — as a dispatched agent, by reporting `NEEDS_CONTEXT` with the items named; never implement the clear items first.

State what cannot be verified and what would verify it when verification is impossible here; never proceed on an unverifiable item.
</clarify-before-implementing>

<push-back-with-evidence>
Push back on an item that breaks existing behavior, that lacks the codebase's context, that builds what nothing uses, that is wrong for this stack, or that contradicts the user's architectural decisions — with the test, the code, or the fact that shows it; never push back with preference.

Hand an item that contradicts the user's architectural decisions to the user before changing anything; never settle an architectural conflict with a reviewer alone.

Correct a wrong pushback in one sentence naming what was checked and what it showed, then implement; never defend the pushback.
</push-back-with-evidence>

<implement-one-at-a-time>
Implement the items in order: those that break or expose the system, then the simple ones — typos, imports, names, then the complex ones — logic and structure; never implement in the order they were written.

Implement one item, run the tests, and move to the next; never batch items between test runs.
</implement-one-at-a-time>

<answer-without-performance>
Answer each item with the change made and where, or the evidence against it; never answer with gratitude, praise, agreement, or an announcement of what is about to happen.

Mark each item `Implemented`, `Will implement`, or `Needs discussion` when the feedback carries several items; never leave an item's state unstated.
</answer-without-performance>
