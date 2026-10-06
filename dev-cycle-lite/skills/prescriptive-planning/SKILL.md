---
name: prescriptive-planning
description: >
  Write a prescription — an implementation prescription, or a correction prescription after a failed review — that leaves the executor — the agent that will execute it — no decision, no option, no signature to invent, and no unverifiable step.
  "write a prescription", "prescribe the implementation", "write the plan for the executor", "correction prescription", "the executor cut corners",
  or any request for a plan the executor will execute literally.
---

<write-for-the-executor>
Write every step — one action on a named file — so that a gate — one line of output a command must print, matched as a Python `re` pattern — checks its result, one gate covering one or several steps; never write a step no gate checks.

Pick one answer for every choice the request — what was asked for — leaves open; never write `decide whether`, `either`, `if needed`, `consider`, or an `or` offering the executor alternatives in the prescription's prose, where quoted code is exempt.

Order the prescription's `##` sections as: `Files and contracts`, `Failure modes observed` for a correction prescription, the units — each one outermost interface, the function or endpoint callers outside the unit use, with the zero to three files behind it, not counting the file that declares the interface or the tests — as `Unit 1` to `Unit N`, `Forbidden patterns`, `Requirement coverage`, `Definition of done`, `Commit` — the one-line commit message the executor commits with; never order them otherwise.
</write-for-the-executor>

<write-a-correction-prescription>
Write a correction prescription — a prescription written after a review found the implementation of an executed prescription incomplete — in the same form as an implementation prescription, from the executed prescription and the findings file — the review's verdict or quality report, or the executor's `BLOCKED` report, naming what failed — whose paths the caller — the agent or person that requested the prescription — supplies; never write one as a list of complaints.

Write under a heading `Failure modes observed` each failure mode — a shortcut, a construction that satisfies a gate without doing the work or evades a check, that the findings file names, or the open step a `BLOCKED` report names — with the code it cites as evidence; never leave a failure mode the findings file names unwritten.
</write-a-correction-prescription>

<list-the-files-and-contracts>
List every file the prescription creates or changes, each with the one responsibility it holds, under `Files and contracts`; never leave a file for the executor to discover.

List beneath the file declaring each unit's interface the unit's contract: the interface's signature — its name, typed parameters, and typed return — a docstring — one sentence on one line beneath the signature — the behaviors a test proves through the interface, and for an interface that is a data type its fields with their types; never leave a unit without its contract.

Fix the signature and docstring of every function the interface calls inside the unit, after the unit's contract under `Files and contracts`; never leave one to the executor.

Order the units so each unit's contract exists before a unit that calls it; never order a calling unit before the unit it calls.
</list-the-files-and-contracts>

<write-each-unit>
Label each unit `Unit N` and each gate within it `Gate M`, counting from 1, and number each step from 1 across the prescription; never leave one unlabelled.

Write each unit as: its contract and files copied verbatim from `Files and contracts`, the steps, the gates, and the scope boundary — the files the prescription changes outside the unit; never write a unit missing one of the five.

State every step as an action on a named file with the exact text it adds — a signature with its docstring and body, a test, a file's whole content — or the exact lines an edit to existing code removes and adds; never state a behavior in place of text or write `similar to`, `as above`, `TBD`, `TODO`, or `add appropriate handling`.

Name every type and function a later unit uses exactly as an earlier unit declared it; never rename one between units.

Use type and function names the prescription, the project, or its libraries declare; never introduce one none of them declares.
</write-each-unit>

<write-the-gates>
Write each gate as a command and the one output line it requires, as in `pytest tests/test_export.py -q` requiring `[0-9]+ passed in [0-9.]+s`; never write a gate as a checkbox or an adjective.

Write in each unit a gate for the run of the unit's test file requiring its summary line to show every test passed and none skipped; never write a gate the executor can satisfy by reading the output loosely.

Write one gate per behavior in the contract that runs the interface on an input from that behavior and requires the exact return value, response, written file content, or raised error; never let a passing run stand for a correct result.

Write for an interface that is a data type a gate that constructs it with each field and requires the exact field values; never leave a data type without one.

Add, in a correction prescription, to each unit of the executed prescription that holds code the evidence cites — those units restated in this prescription, no other — a gate that catches each failure mode the executed prescription's gates passed; never reuse unchanged a gate that passed a broken result.
</write-the-gates>

<forbid-the-patterns>
List under `Forbidden patterns`, at least one per gate, each shortcut the executor will reach for and the prescription forbids, such as a default empty list, a `pass` body, a `TODO`, an `at least one of` validation standing for a required field, a `#` comment; never leave a gate without a forbidden pattern.

Write each forbidden pattern as the code it forbids; never write it as a principle.

Copy, in a correction prescription, the executed prescription's forbidden patterns into this list; never drop one.

Forbid, in a correction prescription, each failure mode as the code the executor used; never omit one.
</forbid-the-patterns>

<define-done>
Write under `Definition of done` a numbered list of binary checks — one check per gate, restating the gate's command and required output line, each passing or failing with no judgement and citing its gate as `Unit N, Gate M`; never write a check that reads `ensure`, `verify`, or `appropriate`.
</define-done>

<check-the-prescription>
Point each requirement — one sentence of the request, or for a correction prescription one failure mode under `Failure modes observed` — to the unit that implements it, as `requirement — Unit N` under `Requirement coverage`; never leave a requirement unpointed.

Add a unit for every requirement no unit covers; never ship a gap.

Scan the prescription's prose outside `Forbidden patterns` and outside quoted code for the words `write-for-the-executor` bans, for `TBD`, `TODO`, `later`, `similar`, `appropriate`, a step with none of signature, behavior, or code, and a type or function name that no unit, the project, or its libraries declare; never skip a term of the scan.

Fix each hit of the scan; never ship one.

Check that every name a later unit uses matches the signature an earlier unit declared; never ship a mismatch.
</check-the-prescription>

<write-the-prescription-to-disk>
Write the prescription to the output path the caller supplied; never write it elsewhere when one was supplied.

Write the prescription, when no output path was supplied, to `docs/plans/<slug>.md` relative to the project root, creating the directory when absent; never return the prescription as conversation text.

Build `<slug>` from the request with the word `correction` dropped, as its first three nouns in lowercase hyphenated words, `-correction` appended for a correction prescription; never build it otherwise.

Return that path as the result; never return more.
</write-the-prescription-to-disk>
