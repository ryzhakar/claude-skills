# dev-discipline

Software engineering discipline with development lifecycle orchestration. Plan-implement-review-fix loop, outermost-test-first signature-first TDD, defensive planning, systematic debugging, code review, bug triage, architecture improvement, worktree-isolated implementation agents, and a review chain enforced by hooks.

`tdd` `debugging` `planning` `code-review` `testing` `triage` `architecture` `refactoring` `orchestration` `lifecycle` `worktree` 
## Skills

### [defensive-planning](skills/defensive-planning/SKILL.md)

Write an implementation plan, or a correction plan after a failed review, that leaves the implementer — the agent that will execute the plan — no decision, no option, and no unverifiable step. "write an implementation plan", "plan the implementation", "write the plan for the implementer", "correction plan", "the implementer cut corners", or any request for a plan another agent will execute.


---

### [dev-orchestration](skills/dev-orchestration/SKILL.md)

Drive the plan, implement, review, fix, and integrate loop over software work through the implementer, spec-reviewer, and code-quality-reviewer agents, as an extension of agentic-delegation. "implement a feature end-to-end", "execute an implementation plan", "build this with agents", "orchestrate development", "run the dev loop", "implement using subagents", "dispatch implementers", "coordinate implementation and review", or any coding task an orchestrator delegates.


---

### [improve-architecture](skills/improve-architecture/SKILL.md)

Find architectural friction — places where understanding a codebase breaks down — explore in parallel several designs for a deepened module — one hiding more implementation behind a smaller interface — and write an RFC — a proposal document — recommending one. "improve the architecture", "find refactoring opportunities", "deepen shallow modules", "reduce coupling", "simplify the module structure", "this module is hard to navigate", or any mention of architectural friction or module boundaries.


---

### [receiving-code-review](skills/receiving-code-review/SKILL.md)

Act on code review feedback — each item being one change a reviewer asks for, so a comment asking for two changes holds two items — by verifying each against the code, clarifying every unclear item before implementing any, pushing back with evidence, and implementing one item at a time. "address the review", "review comments to handle", "PR feedback", "should I implement this suggestion", "the reviewer says", or any reply to review findings.


---

### [systematic-debugging](skills/systematic-debugging/SKILL.md)

Find the root cause of a bug, a test failure, an error, or an unexpected behavior before changing any code, then fix the cause once. "debug this", "why does this fail", "the test is failing", "find the root cause", "this keeps breaking", "the fix didn't work", a build or integration failure, or any fix attempt that follows a failed one.


**Scripts:** [`find-polluter.sh`](skills/systematic-debugging/scripts/find-polluter.sh)
---

### [tdd](skills/tdd/SKILL.md)

Build code by writing one failing test through the surface its callers use before any code, designing the functions beneath that surface before filling them, and refactoring once every test passes. "tdd", "write tests first", "test-driven development", "red-green-refactor", "implement using tdd", "write a failing test", "design the signatures", "outside in", or any request to write code that carries behavior.


---

### [triage-issue](skills/triage-issue/SKILL.md)

Diagnose a reported bug to its root cause and write an issue document carrying a test-first fix plan, without fixing the code. "triage this", "this is broken", "investigate a bug", "find the root cause and file it", "write up this bug", "file an issue", or any bug report that asks for a diagnosis rather than a fix.


---

## Agents

### [code-quality-reviewer](agents/code-quality-reviewer.md)

Review the quality of a unit's changed code against the tdd skill's rules and the design checks below, and write a report file whose Ready to merge line gates the merge. Use it after the spec-reviewer has passed a unit, to audit a completed feature, or before merging code that must meet production standards. Examples:

<example>
Context: The spec-reviewer has passed the implementation and the code quality needs checking.
user: "Spec looks good. Now review the code quality."
assistant: "I'll launch the code-quality-reviewer agent for the quality audit."
</example>

<example>
Context: A feature is complete and needs a quality check before a PR.
user: "Review the quality of my changes before I create a PR"
assistant: "I'll launch the code-quality-reviewer agent to review the changes."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob, Bash, Skill

---

### [implementer](agents/implementer.md)

Use this agent to implement one unit from an implementation plan, carry out a well-specified coding task, or run a TDD cycle on a defined unit of work, inside its own git worktree. Examples:

<example>
Context: An implementation plan has five units. Unit 1 fixes the outermost contract of an authentication middleware.
user: "Execute unit 1 from the implementation plan"
assistant: "I'll launch the implementer agent for unit 1."
</example>

<example>
Context: Sequential units. Unit 3 specifies a database migration with its table structure and rollback test.
user: "Continue to unit 3"
assistant: "I'll launch the implementer agent for unit 3."
</example>

<example>
Context: The implementer returned NEEDS_CONTEXT naming a missing schema definition.
user: "Here's the schema definition from schema.sql. Continue the implementer."
assistant: "I'll continue the implementer with the schema context."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Edit, Bash, Grep, Glob, Skill

---

### [spec-reviewer](agents/spec-reviewer.md)

Verify that an implementation in a worktree matches its specification and write a verdict file reading PASS or FAIL. Use it after an implementer reports a unit complete, or when requirements and code may have drifted. Examples:

<example>
Context: An implementer agent has completed a unit and reported DONE.
user: "Review the implementation against the spec"
assistant: "I'll launch the spec-reviewer agent to verify compliance."
</example>

<example>
Context: A feature must match its original requirements before merging.
user: "Check if the auth implementation matches the requirements doc"
assistant: "I'll launch the spec-reviewer agent to compare the code to the requirements."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob, Bash

---

