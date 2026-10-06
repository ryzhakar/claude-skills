---
name: defensive-planning
description: >
  Write an implementation plan, or a correction plan after a failed review, that leaves the implementer — the agent that will execute the plan — no decision, no option, and no unverifiable step.
  "write an implementation plan", "plan the implementation", "write the plan for the implementer", "correction plan", "the implementer cut corners",
  or any request for a plan another agent will execute.
---

<write-for-the-implementer>
Write every line so that no ambiguity grants the implementer permission and no passing test stands for completion; never write a line that trusts the implementer.

Pick one answer for every choice the work holds; never write `decide whether`, `either`, `or`, `if needed`, or `consider` in the plan's prose, where quoted code is exempt.
</write-for-the-implementer>

<list-the-files-and-contracts>
List every file the work creates or changes, each with the one responsibility it holds; never leave a file for the implementer to discover.

List for each unit — one outermost interface, the surface callers of the unit use, and the one to three files behind it, not counting the file that declares the interface or the tests, or none for an interface that is a data type — the contract: the interface's signature with typed parameters and return, a docstring of one sentence on one line, the behaviors a test proves through the interface, and for an interface that is a data type its fields with their types; never leave a unit without its contract.

Leave, as the one exception to the rules above, every signature beneath the outermost interface to the implementer, who designs it through `tdd`; never fix one in the plan.

Order the units so each unit's contract exists before a unit that calls it; never order a caller before its callee.
</list-the-files-and-contracts>

<write-each-unit>
Write each unit as: the contract, the files, the steps — each an action on a named file, the verification gates — each a command and the exact output it requires, and the scope boundary — what the unit does not touch; never write a unit missing one of the five.

State every step as an action on a named file — the signature it adds to the file declaring the interface, the behavior each test it adds proves, or the behaviors a file behind the outermost interface satisfies; never write `similar to`, `as above`, `TBD`, `TODO`, or `add appropriate handling`.

Name every type and function a later unit uses exactly as an earlier unit declared it; never introduce a type or function name that the plan, the project, or its libraries did not declare.
</write-each-unit>

<write-the-gates>
Write each verification gate as a command and the exact output it requires, with a pattern for any part that varies such as a run time, as in `grep -n "= \[\]" src/schemas/*.py` requiring zero matches; never write a gate as a checkbox or an adjective.

Write a gate for the test run requiring its summary line to show every test passed and none skipped; never write a gate the implementer can satisfy by reading the output loosely.

Write a gate that runs the interface on an input from each behavior in the contract and requires the exact return value or response; never let a passing run stand for a correct result.
</write-the-gates>

<forbid-the-patterns>
List under a heading `Forbidden patterns` each shortcut — a construction that satisfies a gate without doing the work — the implementer will reach for and the plan forbids, such as a default empty list, a `pass` body, a `TODO`, an `at least one of` validation standing for a required field, a comment; never leave a tempting shortcut unnamed.

Write each forbidden pattern as the code it forbids; never write it as a principle.
</forbid-the-patterns>

<define-done>
Write under a heading `Definition of done` a numbered list of binary checks — each passes or fails with no judgement and cites the gate that proves it as `unit N, gate M`, counting in plan order; never write a check that reads `ensure`, `verify`, or `appropriate`.
</define-done>

<write-a-correction-plan>
Write a correction plan — a plan written after a review found the implementation of an executed plan, whose path the caller supplies, short — in the same form as an implementation plan, with the three additions below; never write one as a list of complaints.

Name under a heading `Failure modes observed` each shortcut the implementer took, with the evidence from the code; never name a hypothetical one.

Forbid each shortcut the implementer used, as the code it used, beside the patterns the executed plan already forbids; never omit one it used.

Add a gate that catches each defect the executed plan's gates passed; never reuse a gate that passed a broken result unchanged.
</write-a-correction-plan>

<check-the-plan>
Point each requirement of the task — for a correction plan, each failure mode under `Failure modes observed` — to the unit that implements it, in a list under a heading `Requirement coverage`; never leave a requirement unpointed.

Add a unit for every requirement no unit covers; never ship a gap.

Scan the plan's prose outside `Forbidden patterns` and outside quoted code for `TBD`, `TODO`, `later`, `similar`, `appropriate`, a step with none of signature, behavior, or code, and a type or function name that no unit, the project, or its libraries declare; never skip a term of the scan.

Fix each hit of the scan; never ship one.

Check that every name a later unit uses matches the signature an earlier unit declared; never ship a mismatch.
</check-the-plan>

<write-the-plan-to-disk>
Write the plan to the path the caller supplied, or to `docs/plans/<slug>.md` with `<slug>` the first three words of the task statement in lowercase hyphenated words, `-correction` appended for a correction plan, when none was supplied; never return the plan as conversation text.

Return that path as the result; never return more.
</write-the-plan-to-disk>
