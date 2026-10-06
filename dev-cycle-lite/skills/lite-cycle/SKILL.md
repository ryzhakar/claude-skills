---
name: lite-cycle
description: >
  Run the dev-cycle loop over one spec at the lowest cost tier — an opus prescriber writes a prescription per unit, disposable haiku executors follow it literally, and the suborchestrator running this skill reviews each unit itself and integrates.
  "run the lite cycle", "implement this cheaply", "implement with haiku executors", "prescribe and execute", or any dev-cycle run the owner marks lite.
---

<read-the-parents-first>
Read the `dev-cycle` skill and the `agentic-delegation` skill whole before any step below; never run this skill without both.

Follow every rule of the `dev-cycle` skill from its `plan-the-units` stage on, except where a sentence below replaces it; never re-decide a rule it already fixes.
</read-the-parents-first>

<take-the-spec>
Take the spec path from the dispatch — the orchestrator above provisions the spec-capturer; never run the spec-capturer from this skill.

Plan the units as the `dev-cycle` skill prescribes, assigning every unit to haiku; never assign a unit to another tier.
</take-the-spec>

<prescribe-each-unit>
Launch `prescriber` once per unit, on opus, with the spec path, the unit's contract and gates from the plan, the unit's input paths, the project root, and the prescription path — `briefs/prescriber-${unit}.md` under the artifact directory; never launch an executor without its prescription on disk.

Take the prescription as the executor's whole brief, with the integration branch as the one addition; never add another sentence to it.
</prescribe-each-unit>

<launch-the-executor>
Launch `executor` in the background, on haiku, with the prescription path and the integration branch; never launch it on another tier or with another item.

Discard an executor after its report; never continue one through `SendMessage`.

Launch `prescriber` again with the findings file's path after a `FAIL` verdict or an open finding, to write a correction prescription at a path with `-2`, `-3` appended, then launch a fresh executor with it; never hand findings to an executor without the prescriber rewriting them.
</launch-the-executor>

<review-each-unit-yourself>
Invoke the `dev-discipline:tdd` skill with the `Skill` tool before the first review; never review without its text in this context.

Review each `DONE` unit yourself — the spec review by the `dev-cycle` plugin's `spec-reviewer` procedure, the quality review by its `code-quality-reviewer` procedure — writing the verdict file and the report file at the paths the `dev-cycle` skill fixes; never launch a reviewer and never skip either review.

Read each changed file in full from the executor's worktree before marking a requirement; never mark from the executor's report.
</review-each-unit-yourself>

<escalate-on-the-third-failure>
Stop at the third failed review-fix cycle of a unit, as the `dev-cycle` skill prescribes, and return the unit to the orchestrator above with its last prescription path and its last verdict path; never raise an executor's tier.
</escalate-on-the-third-failure>

<report-to-the-orchestrator>
End with a report of these lines: `Status:` `DONE` or `BLOCKED`, `Integration branch:`, `Units integrated:`, `Units returned:` each with its prescription and verdict paths or `none`, `Status file:` its path; never end without the status file written.
</report-to-the-orchestrator>
