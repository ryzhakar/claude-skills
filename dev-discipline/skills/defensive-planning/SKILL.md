---
name: defensive-planning
description: >
  Write an implementation plan, or a correction plan after a failed review, that leaves the implementer no decision, no option, and no unverifiable step.
  "write an implementation plan", "plan the implementation", "write the plan for the implementer", "correction plan", "the implementer cut corners",
  or any request for a plan another agent will execute.
---

<assume-the-implementer-cuts-corners>
Write every line for an implementer — the agent that will execute the plan — who will read an ambiguity as permission and a passing test as completion; never write a line that trusts it.

Pick one answer for every choice the work holds; never write `decide whether`, `either`, `or`, `if needed`, or `consider`.
</assume-the-implementer-cuts-corners>

<map-the-files-and-contracts>
List every file the work creates or changes, each with the one responsibility it holds; never leave a file for the implementer to discover.

Fix for each unit — one outermost interface, the surface callers of the unit use, and the one to three files behind it — the contract: the interface's signature with typed parameters and return, a docstring of one sentence on one line, and the behaviors a test proves through the interface; never fix a signature beneath the outermost interface, which the implementer designs through `tdd`.

Order the units so each unit's contract exists before a unit that calls it; never order a caller before its callee.
</map-the-files-and-contracts>

<write-each-unit>
Write each unit as: the contract, the files, the exact steps, the verification gates, and the scope boundary — what the unit does not touch; never write a unit missing one of the five.

State every step as an action on a named file with the code or signature it adds; never write `similar to`, `as above`, `TBD`, `TODO`, or `add appropriate handling`.

Name every type and function a later unit uses exactly as an earlier unit declared it; never introduce a name the plan did not declare.
</write-each-unit>

<write-the-gates>
Write each verification gate as a command and the exact output it requires, such as `grep -n "= \[\]" src/schemas/*.py` requiring zero matches; never write a gate as a checkbox or an adjective.

Write a gate for the test run requiring its summary line to show every test passed and none skipped; never write a gate the implementer can satisfy by reading the output loosely.

Write a gate that checks the output's content for each behavior in the contract; never let a passing run stand for a correct result.
</write-the-gates>

<forbid-the-patterns>
List under a heading `Forbidden patterns` each construction the implementer will reach for and the plan refuses, such as a default empty list, a `pass` body, a `TODO`, an `at least one of` validation standing for a required field, a comment; never leave a tempting shortcut unnamed.

Write each forbidden pattern as the code it bans; never write it as a principle.
</forbid-the-patterns>

<define-done>
Write under a heading `Definition of done` a numbered list of binary checks — each passes or fails with no judgement; never write a check that reads `ensure`, `verify`, or `appropriate`.
</define-done>

<review-the-plan>
Point each requirement of the task to the unit that implements it and list every requirement no unit covers; never ship a gap.

Scan the plan for `TBD`, `TODO`, `later`, `similar`, `appropriate`, a step without code, and a name no unit declared, and fix each; never ship one.

Check that every name a later unit uses matches the signature an earlier unit declared; never ship a mismatch.
</review-the-plan>

<write-a-correction-plan>
Write a correction plan — a plan written after a review found the implementation short — in the same form as an implementation plan, with three additions; never write one as a list of complaints.

Name under a heading `Failure modes observed` each shortcut the implementer took, with the evidence from the code; never name a hypothetical one.

Forbid each escape hatch the implementer used, as the code it used; never forbid one it did not.

Add a gate that catches each defect the previous gates passed; never reuse a gate that passed a broken result unchanged.
</write-a-correction-plan>

<write-the-plan-to-disk>
Write the plan to the path the caller supplied, or to the project's plan directory when none was supplied, and return that path; never return the plan as conversation text.
</write-the-plan-to-disk>
