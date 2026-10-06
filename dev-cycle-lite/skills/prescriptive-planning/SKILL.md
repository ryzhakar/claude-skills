---
name: prescriptive-planning
description: >
  Write a prescription — an implementation plan, or a correction plan after a failed review — that leaves the executor — the agent that will execute it — no decision, no option, no signature to invent, and no unverifiable step.
  "write a prescription", "prescribe the implementation", "write the plan for the executor", "correction prescription", "the executor cut corners",
  or any request for a plan a disposable agent will execute literally.
---

<write-for-the-executor>
Write every line so that no ambiguity grants the executor permission and no passing test alone counts as completion; never write a line that trusts the executor.

Pick one answer for every choice the request — what was asked for — leaves open; never write `decide whether`, `either`, `or`, `if needed`, or `consider` in the prescription's prose, where quoted code is exempt.
</write-for-the-executor>

<write-a-correction-prescription>
Write a correction prescription — a prescription written after a review found the implementation of an executed prescription incomplete — in the same form as a first prescription, with the three additions below, from the executed prescription and the review report, whose paths the caller — the agent or person that requested the prescription — supplies; never write one as a list of complaints.

Name under a heading `Failure modes observed` each failure mode — a shortcut the review report names — with the code it cites as evidence; never name a hypothetical one.

Forbid each failure mode, as the code the executor used, in the same `Forbidden patterns` list, repeating the executed prescription's patterns; never omit one.

Add to the unit that holds the failing code a gate that catches each failure mode the executed prescription's gates passed; never reuse unchanged a gate that passed a broken result.
</write-a-correction-prescription>

<list-the-files-and-contracts>
List every file the prescription creates or changes, each with the one responsibility it holds, under a heading `Files and contracts`; never leave a file for the executor to discover.

List for each unit — one outermost interface, the surface callers of the unit use, and the zero to three files behind it, not counting the file that declares the interface or the tests — the contract: the interface's signature — its name, typed parameters, and typed return — a docstring — one sentence on one line beneath the signature — the behaviors a test proves through the interface, and for an interface that is a data type its fields with their types; never leave a unit without its contract.

Fix every signature beneath the outermost interface, with its docstring, in the prescription; never leave one to the executor.

Order the units so each unit's contract exists before a unit that calls it; never order a caller before its callee.
</list-the-files-and-contracts>

<write-each-unit>
Write each unit as: its contract and files from the `Files and contracts` list, the steps — each an action on a named file, the verification gates — each a command and the exact output it requires, and the scope boundary — what the unit does not touch; never write a unit missing one of the five.

State every step as an action on a named file — the signature it adds to the file declaring the interface, the behavior each test it adds proves, the behaviors a file behind the outermost interface satisfies, or the exact lines an edit to existing code removes and adds; never write `similar to`, `as above`, `TBD`, `TODO`, or `add appropriate handling`.

Name every type and function a later unit uses exactly as an earlier unit declared it; never rename one between units.

Use type and function names the prescription, the project, or its libraries declare; never introduce one none of them declares.
</write-each-unit>

<write-the-gates>
Write each verification gate as a command and the exact output it requires, with a pattern for any part that varies such as a run time, as in `grep -n "= \[\]" src/schemas/*.py` requiring zero matches; never write a gate as a checkbox or an adjective.

Write a gate for the test run requiring its summary line to show every test passed and none skipped; never write a gate the executor can satisfy by reading the output loosely.

Write a gate that runs the interface on an input from each behavior in the contract and requires the exact return value or response; never let a passing run stand for a correct result.

Write for an interface that is a data type a gate that constructs it with each field and requires the exact field values; never leave a data type without one.
</write-the-gates>

<forbid-the-patterns>
List under a heading `Forbidden patterns` each shortcut — a construction that satisfies a gate without doing the work — the executor will reach for and the prescription forbids, such as a default empty list, a `pass` body, a `TODO`, an `at least one of` validation standing for a required field, a comment; never leave a tempting shortcut unnamed.

Write each forbidden pattern as the code it forbids; never write it as a principle.
</forbid-the-patterns>

<check-the-prescription>
Point each requirement the request states — for a correction prescription, each failure mode under `Failure modes observed` — to the unit that implements it, in a list under a heading `Requirement coverage`; never leave a requirement unpointed.

Add a unit for every requirement no unit covers; never ship a gap.

Scan the prescription's prose outside `Forbidden patterns` and outside quoted code for the words `write-for-the-executor` bans, for `TBD`, `TODO`, `later`, `similar`, `appropriate`, a step with none of signature, behavior, or code, and a type or function name that no unit, the project, or its libraries declare; never skip a term of the scan.

Fix each hit of the scan; never ship one.

Check that every name a later unit uses matches the signature an earlier unit declared; never ship a mismatch.
</check-the-prescription>

<define-done>
Write under a heading `Definition of done` a numbered list of binary checks — one check per gate, each passing or failing with no judgement and citing its gate as `unit N, gate M`, counting in prescription order; never write a check that reads `ensure`, `verify`, or `appropriate`.
</define-done>

<write-the-prescription-to-disk>
Write the prescription to the output path the caller supplied, or to `docs/plans/<slug>.md` with `<slug>` the first three words after the request's verb in lowercase hyphenated words, the word `correction` dropped, `-correction` appended for a correction prescription, when none was supplied; never return the prescription as conversation text.

Return that path as the result; never return more.
</write-the-prescription-to-disk>
