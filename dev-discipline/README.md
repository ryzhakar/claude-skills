# dev-discipline

Software engineering discipline: defensive planning, test-driven development, systematic debugging, code review reception, bug triage, and architecture improvement.

`tdd` `debugging` `planning` `code-review` `testing` `triage` `architecture` `refactoring` 
## Skills

### [defensive-planning](skills/defensive-planning/SKILL.md)

Write implementation plans, assessments, and corrections for implementers who may cut corners. Use when: creating implementation plans, reviewing implementations for adherence, writing correction plans after failures, or when the implementer may choose appearing done over being done. Produces prescriptive documents with verification gates, forbidden patterns, and zero escape hatches.


---

### [improve-architecture](skills/improve-architecture/SKILL.md)

Explores codebases for architectural friction, discovers module-deepening opportunities, and proposes refactors through multi-design exploration. Triggers: "improve architecture", "find refactoring opportunities", "deepen shallow modules", "reduce coupling", "simplify module structure", mentions of architectural friction or module boundaries. Writes refactor RFC as a report file.


---

### [receiving-code-review](skills/receiving-code-review/SKILL.md)

This skill should be used to apply anti-performative code review protocol: verify-before-implement discipline, YAGNI enforcement, and technical pushback patterns when receiving PR feedback. Triggers: "receives code review feedback", "gets review comments", "has PR feedback to address", "should I implement this suggestion", "how to respond to code review", "handle review feedback", or when performative agreements appear in responses.


---

### [systematic-debugging](skills/systematic-debugging/SKILL.md)

Mandatory 4-phase root cause protocol for bugs, test failures, errors, or unexpected behavior. Prevents random fixes and symptom patching. Apply BEFORE proposing any fix, especially when multiple attempts have failed or time pressure tempts guessing.


**Scripts:** [`find-polluter.sh`](skills/systematic-debugging/scripts/find-polluter.sh)
---

### [tdd](skills/tdd/SKILL.md)

This skill should be used when the user asks to "implement using TDD", "write tests first", "use test-driven development", "red-green-refactor", "write a failing test", "add test coverage with TDD", "what makes a good test", or when code review reveals implementation-coupled tests. Provides the philosophy, workflow, and technique of test-driven development including good/bad test patterns, mocking strategy, interface design for testability, and refactoring discipline.


---

### [triage-issue](skills/triage-issue/SKILL.md)

Autonomously diagnoses bugs, traces root causes, designs TDD fix plans, and writes issue documents. Triggers: bug reports, "this is broken", "triage an issue", "investigate a bug", "find the root cause", "file an issue for this bug", autonomous problem diagnosis.


---

## Agents

### [code-quality-reviewer](agents/code-quality-reviewer.md)

Use this agent when reviewing code quality after spec compliance has been verified, when completing a feature and needing a quality audit, or before merging code that should meet production standards. Examples:

<example>
Context: Spec-reviewer has approved the implementation and now code quality needs to be checked.
user: "Spec looks good. Now review the code quality."
assistant: "I'll use the code-quality-reviewer agent for the quality audit."
</example>

<example>
Context: User completed a feature and wants a quality check before creating a PR.
user: "Review the quality of my changes before I create a PR"
assistant: "I'll use the code-quality-reviewer agent to review the changes."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob, Bash

---

### [implementer](agents/implementer.md)

Use this agent when dispatching a subagent to implement a single task from an implementation plan, execute a well-specified coding task, or carry out a TDD cycle on a defined unit of work. Examples:

<example>
Context: User has an implementation plan with 5 tasks. Task 1 specifies TDD for authentication middleware.
user: "Execute task 1 from the implementation plan"
assistant: "I'll use the implementer agent to execute this task with TDD."
</example>

<example>
Context: Sequential task execution. Task 3 specifies database migration with table structure and rollback test.
user: "Continue to task 3"
assistant: "I'll use the implementer agent for Task 3."
</example>

<example>
Context: Implementer returned NEEDS_CONTEXT. User provides the missing schema definition.
user: "Here's the schema definition from schema.sql. Re-dispatch the implementer."
assistant: "I'll use the implementer agent with the schema context."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Edit, Bash, Grep, Glob

---

### [spec-reviewer](agents/spec-reviewer.md)

Use this agent when verifying that an implementation matches its specification, after an implementer reports task completion, or when checking for spec drift between requirements and code. Examples:

<example>
Context: An implementer agent has completed a task and reported DONE.
user: "Review the implementation against the spec"
assistant: "I'll use the spec-reviewer agent to verify compliance."
</example>

<example>
Context: User wants to verify a feature matches its original requirements before merging.
user: "Check if the auth implementation matches the requirements doc"
assistant: "I'll use the spec-reviewer agent to compare code to requirements."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob

---

