---
name: lite-cycle
description: >
  Run the dev-cycle loop over one spec at the lowest cost tier — an opus prescriber writes a prescription per unit, disposable haiku executors follow it literally, and the suborchestrator running this skill reviews each unit itself and integrates.
  "run the lite cycle", "implement this cheaply", "implement with haiku executors", "prescribe and execute", or any dev-cycle run the user marks lite in the dispatch.
---

<read-the-parents-first>
Read the `dev-cycle` skill and the `agentic-delegation` skill whole before any step below; never run this skill without both.

Follow every rule of the `dev-cycle` skill from its `plan-the-units` stage on, except where a sentence below replaces it; never re-decide a rule it already fixes.
</read-the-parents-first>

<take-the-spec>
Take the absolute spec path from the dispatch — the message that launched this run; never take it from elsewhere.

Leave spec capture to the orchestrator above; never run the spec-capturer from this skill.

Write the status file at the path the `dev-cycle` skill fixes after each launch, verdict, integration, and escalation; never hold the state in the conversation alone.

Plan the units as the `dev-cycle` skill prescribes; never skip a step of its planning.

Assign every unit to haiku — the lowest model tier; never assign a unit to another tier.
</take-the-spec>

<prescribe-each-unit>
Launch `prescriber` once per unit, on opus, with the spec path, the unit's contract and gates copied from the plan, the unit's input paths, and the prescription path — `briefs/prescriber-${unit}.md` under the artifact directory the `dev-cycle` skill fixes, `${unit}` the unit's name in the plan; never launch it with another item.

Hold the executor launch until the prescription is on disk; never launch an executor without one.
</prescribe-each-unit>

<launch-the-executor>
Launch `executor` in the background, on haiku, with the prescription path and the integration branch as its whole brief; never add a third item.

Discard an executor after its report; never continue one through `SendMessage`.
</launch-the-executor>

<review-each-unit-yourself>
Invoke the `dev-discipline:tdd` skill with the `Skill` tool before the first review; never review without its text in this context.

Review each `DONE` unit yourself — the spec review by the `dev-cycle` plugin's `spec-reviewer` procedure, the quality review by its `code-quality-reviewer` procedure; never launch a reviewer.

Write one verdict file and one report file per review round at the paths the `dev-cycle` skill fixes; never leave either unwritten.

Read each changed file in full from the executor's worktree — the path on the `Worktree:` line of its report — before recording a requirement as met or unmet in the verdict file; never record from the executor's report.
</review-each-unit-yourself>

<integrate-each-passed-unit>
Integrate a unit on `Verdict: PASS` and `Ready to merge: Yes` as the `dev-cycle` skill's `integrate-the-units` prescribes; never integrate on other values.
</integrate-each-passed-unit>

<re-prescribe-after-a-failed-review>
Launch `prescriber` again after a `FAIL` verdict or an open finding, with the unit's original inputs, the failed prescription's path, and the report file's path; never launch it without the report file's path.

Pass it `briefs/prescriber-${unit}-2.md`, then `-3.md`, as the prescription path; never pass an earlier path again.

Launch a fresh executor with the correction prescription's path and the integration branch, from which it starts and redoes the whole unit; never hand a report file to an executor.
</re-prescribe-after-a-failed-review>

<escalate-on-the-third-failure>
Escalate a unit at its third failed review-fix cycle, as the `dev-cycle` skill counts them, by stopping work on it and listing it on the `Units returned:` line with its last prescription path and last verdict path; never run a fourth cycle.

Continue the other units after an escalation; never stop the run for one returned unit.
</escalate-on-the-third-failure>

<report-to-the-orchestrator>
End with a report of these lines: `Status:` — `DONE` when `Units returned:` reads `none`, `BLOCKED` otherwise; `Integration branch:` — its name; `Units integrated:` — their names, or `none`; `Units returned:` — each name with its last prescription path and last verdict path, or `none`; `Status file:` — its path; never omit a line.
</report-to-the-orchestrator>
