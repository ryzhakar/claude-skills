---
name: prescriptive-planning
description: >
  Write a prescription — an implementation plan, or a correction plan after a failed review — that leaves the executor — the agent that will execute it — no decision, no option, no signature to invent, and no unverifiable step.
  "write a prescription", "prescribe the implementation", "write the plan for the executor", "correction prescription", "the executor cut corners",
  or any request for a plan the executor will execute literally.
---

<write-for-the-executor>
Write every step — one action on a named file — so that a gate — a command and the exact output it requires — checks its result; never write a step no gate checks.

Pick one answer for every choice the request — what was asked for — leaves open; never write `decide whether`, `either`, `if needed`, `consider`, or an `or` offering the executor alternatives in the prescription's prose, where quoted code is exempt.

Order the prescription's sections as: `Files and contracts`, `Failure modes observed` for a correction prescription, the units `Unit 1` to `Unit N`, `Forbidden patterns`, `Requirement coverage`, `Definition of done`; never order them otherwise.
</write-for-the-executor>

<take-the-correction-inputs>
Write a correction prescription — a prescription written after a review found the implementation of an executed prescription incomplete — in the same form as a first prescription, from the executed prescription and the review report, whose paths the caller — the agent or person that requested the prescription — supplies; never write one as a list of complaints.

Name under a heading `Failure modes observed` each failure mode — a shortcut, a construction that satisfies a gate without doing the work, that the review report names — with the code it cites as evidence; never leave a failure mode the review report names unnamed.
</take-the-correction-inputs>

<list-the-files-and-contracts>
List every file the prescription creates or changes, each with the one responsibility it holds, under a heading `Files and contracts`; never leave a file for the executor to discover.

List beneath each file, for each unit — one outermost interface, the function or endpoint callers outside the unit use, and the zero to three files behind it, not counting the file that declares the interface or the tests — the contract: the interface's signature — its name, typed parameters, and typed return — a docstring — one sentence on one line beneath the signature — the behaviors a test proves through the interface, and for an interface that is a data type its fields with their types; never leave a unit without its contract.

Fix every signature beneath the outermost interface, with its docstring, under `Files and contracts` beneath the unit's contract; never leave one to the executor.

Order the units so each unit's contract exists before a unit that calls it; never order a caller before its callee.
</list-the-files-and-contracts>

<write-each-unit>
Label each unit `Unit N` and each gate within it `Gate M`, counting from 1; never leave one unlabelled.

Write each unit as: its contract and files copied verbatim from `Files and contracts`, the steps, the gates, and the scope boundary — what the unit does not touch; never write a unit missing one of the five.

State every step as an action on a named file — the signature it adds to the file declaring the interface and the behaviors the body beneath it satisfies, the behavior each test it adds proves, the behaviors a file behind the outermost interface satisfies, or the exact lines an edit to existing code removes and adds; never write `similar to`, `as above`, `TBD`, `TODO`, or `add appropriate handling`.

Name every type and function a later unit uses exactly as an earlier unit declared it; never rename one between units.

Use type and function names the prescription, the project, or its libraries declare; never introduce one none of them declares.
</write-each-unit>

<write-the-gates>
Write each gate as a command and the exact output it requires, with a regular expression for any part that varies, as in `passed in [0-9.]+s`; never write a gate as a checkbox or an adjective.

Write in each unit a gate for the test run requiring its summary line to show every test passed and none skipped; never write a gate the executor can satisfy by reading the output loosely.

Write one gate per behavior in the contract that runs the interface on an input from that behavior and requires the exact return value or response; never let a passing run stand for a correct result.

Write for an interface that is a data type a gate that constructs it with each field and requires the exact field values; never leave a data type without one.

Add, in a correction prescription, to the unit of the executed prescription that holds the code the evidence cites — restated in this prescription — a gate that catches each failure mode the executed prescription's gates passed; never reuse unchanged a gate that passed a broken result.
</write-the-gates>

<forbid-the-patterns>
List under a heading `Forbidden patterns` each shortcut the executor will reach for and the prescription forbids, such as a default empty list, a `pass` body, a `TODO`, an `at least one of` validation standing for a required field, a comment; never leave a tempting shortcut unnamed.

Write each forbidden pattern as the code it forbids; never write it as a principle.

Copy, in a correction prescription, the executed prescription's forbidden patterns into this list, then forbid each failure mode as the code the executor used; never omit one.
</forbid-the-patterns>

<check-the-prescription>
Point each requirement the request states — for a correction prescription, each failure mode under `Failure modes observed` — to the unit that implements it, in a list under a heading `Requirement coverage`; never leave a requirement unpointed.

Add a unit for every requirement no unit covers; never ship a gap.

Scan the prescription's prose outside `Forbidden patterns` and outside quoted code for the words `write-for-the-executor` bans, for `TBD`, `TODO`, `later`, `similar`, `appropriate`, a step with none of signature, behavior, or code, and a type or function name that no unit, the project, or its libraries declare; never skip a term of the scan.

Fix each hit of the scan; never ship one.

Check that every name a later unit uses matches the signature an earlier unit declared; never ship a mismatch.
</check-the-prescription>

<define-done>
Write under a heading `Definition of done` a numbered list of binary checks — one check per gate, restating the gate's command and required output, each passing or failing with no judgement and citing its gate as `Unit N, Gate M`; never write a check that reads `ensure`, `verify`, or `appropriate`.
</define-done>

<write-the-prescription-to-disk>
Write the prescription to the output path the caller supplied, or, when none was supplied, to `docs/plans/<slug>.md` relative to the project root, creating the directory when absent, with `<slug>` built by dropping the word `correction` from the request, taking the first three words after its verb in lowercase hyphenated words, and appending `-correction` for a correction prescription; never return the prescription as conversation text.

Return that path as the result; never return more.
</write-the-prescription-to-disk>
