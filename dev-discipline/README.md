# dev-discipline

Software engineering discipline: defensive planning, test-driven development, systematic debugging, and code review reception.

`tdd` `debugging` `planning` `code-review` `testing` 
## Skills

### [defensive-planning](skills/defensive-planning/SKILL.md)
Write implementation plans, assessments, and corrections for implementers who may cut corners.
Use when: (1) creating implementation plans for peers/subordinates/contractors, (2) reviewing
implementations for adherence, (3) writing correction plans after failures, (4) any situation
where the implementer is assumed to be no better than you—possibly lazier, prone to shortcuts,
or incentivized to appear done rather than be done. This skill produces prescriptive documents
with verification gates, forbidden patterns, and zero escape hatches.


**References:** [`execution.md`](skills/defensive-planning/references/execution.md) · [`module-design.md`](skills/defensive-planning/references/module-design.md) · [`tdd-mode.md`](skills/defensive-planning/references/tdd-mode.md)
---

### [receiving-code-review](skills/receiving-code-review/SKILL.md)
This skill should be used to apply anti-performative code review protocol: verify-before-implement discipline, YAGNI enforcement, and technical pushback patterns when receiving PR feedback. Triggers: "receives code review feedback", "gets review comments", "has PR feedback to address", "should I implement this suggestion", "how to respond to code review", "handle review feedback", or when performative agreements appear in responses.


---

### [systematic-debugging](skills/systematic-debugging/SKILL.md)
This skill should be used when the user reports a "bug", "test failure", "unexpected behavior", "error", "crash", "flaky test", asks to "debug this", "find root cause", "why is this failing", "fix this error", or when multiple fix attempts have failed. Provides a mandatory 4-phase root cause protocol that prevents random fixes and symptom patching. Apply BEFORE proposing any fix, especially under time pressure.


**References:** [`condition-based-waiting.md`](skills/systematic-debugging/references/condition-based-waiting.md) · [`defense-in-depth.md`](skills/systematic-debugging/references/defense-in-depth.md) · [`root-cause-tracing.md`](skills/systematic-debugging/references/root-cause-tracing.md)
**Scripts:** [`find-polluter.sh`](skills/systematic-debugging/scripts/find-polluter.sh)
---

### [tdd](skills/tdd/SKILL.md)
This skill should be used when the user asks to "implement using TDD", "write tests first", "use test-driven development", "red-green-refactor", "write a failing test", "add test coverage with TDD", "what makes a good test", or when code review reveals implementation-coupled tests. Provides the philosophy, workflow, and technique of test-driven development including good/bad test patterns, mocking strategy, interface design for testability, and refactoring discipline.


**References:** [`deep-modules.md`](skills/tdd/references/deep-modules.md) · [`interface-design.md`](skills/tdd/references/interface-design.md) · [`mocking.md`](skills/tdd/references/mocking.md) · [`refactoring.md`](skills/tdd/references/refactoring.md) · [`tests.md`](skills/tdd/references/tests.md)
---

## Agents

### [code-quality-reviewer](agents/code-quality-reviewer.md)

Use this agent when reviewing code quality after spec compliance has been verified, when completing a feature and needing a quality audit, or before merging code that should meet production standards. Examples:

<example>
Context: Spec-reviewer has approved the implementation and now code quality needs to be checked
user: "Spec looks good. Now review the code quality."
assistant: "I'll audit the code quality."
<commentary>
Code quality review happens AFTER spec compliance passes. The reviewer checks
quality, architecture, testing, and categorizes findings by severity.
</commentary>
assistant: "I'll use the code-quality-reviewer agent for the quality audit."
</example>

<example>
Context: User completed a feature and wants a quality check before creating a PR
user: "Review the quality of my changes before I create a PR"
assistant: "Let me audit the changes."
<commentary>
Pre-PR quality audit. The reviewer scopes to the git diff range and categorizes
findings.
</commentary>
assistant: "I'll use the code-quality-reviewer agent to review the changes."
</example>

<example>
Context: All tasks in a plan are complete and a final quality review is needed
user: "All tasks done. Do a final code quality review across the whole implementation."
assistant: "I'll perform a comprehensive quality review."
<commentary>
Final holistic quality review covering all changes from the implementation plan.
</commentary>
assistant: "I'll use the code-quality-reviewer agent for the final audit."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob, Bash

---

### [implementer](agents/implementer.md)

Use this agent when dispatching a subagent to implement a single task from an implementation plan, execute a well-specified coding task, or carry out a TDD cycle on a defined unit of work. Examples:

<example>
Context: User has a defensive-planning implementation plan with 5 tasks. Task 1 is "Implement the authentication middleware using TDD: (1) Write test for JWT token validation with mock request/response (2) Implement validateToken() function (3) Add error handling for expired tokens"
user: "Execute task 1 from the implementation plan"
assistant: "I'll work on task 1 from the plan."
<commentary>
User has a specific, well-defined task from a plan with concrete deliverables.
The implementer agent handles single-task implementation with TDD, self-review,
and status reporting. This is concrete enough to delegate.
</commentary>
assistant: "I'll use the implementer agent to execute this task with TDD."
</example>

<example>
Context: User is implementing database migrations. Task 3 from plan is "Add user_preferences table migration with TDD: (1) Write test that verifies table structure (columns: id, user_id, preferences_json, updated_at) (2) Write migration file (3) Test rollback"
user: "Continue to task 3"
assistant: "Moving to the user_preferences migration."
<commentary>
Sequential task execution in a plan. Each task gets a fresh implementer agent
to avoid context pollution from previous tasks. The task is specific with
concrete deliverables (table structure, migration file, rollback test).
</commentary>
assistant: "I'll use the implementer agent for Task 3."
</example>

<example>
Context: An implementer returned NEEDS_CONTEXT because task required database schema but it wasn't provided. User has now located the schema definition.
user: "Here's the schema definition from schema.sql. Re-dispatch the implementer."
assistant: "Thanks for the schema."
<commentary>
Re-dispatch after providing missing context. The implementer gets a fresh start
with complete information. This demonstrates the NEEDS_CONTEXT workflow.
</commentary>
assistant: "I'll use the implementer agent with the schema context."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Edit, Bash, Grep, Glob

---

### [spec-reviewer](agents/spec-reviewer.md)

Use this agent when verifying that an implementation matches its specification, after an implementer reports task completion, or when checking for spec drift between requirements and code. Examples:

<example>
Context: An implementer agent has completed a task and reported DONE
user: "Review the implementation against the spec"
assistant: "Let me verify spec compliance."
<commentary>
After implementation completes, spec compliance must be verified before code
quality review. The spec-reviewer reads actual code and compares to requirements
line by line.
</commentary>
assistant: "I'll use the spec-reviewer agent to verify compliance."
</example>

<example>
Context: During subagent-driven development, the implementer finished suspiciously quickly
user: "That was fast. Let's verify it actually matches the spec."
assistant: "I'll independently verify the work."
<commentary>
Quick completion is a signal for adversarial verification. The spec-reviewer
does not trust implementer reports and reads the actual code.
</commentary>
assistant: "I'll use the spec-reviewer agent to verify against the specification."
</example>

<example>
Context: User wants to verify a feature matches its original requirements before merging
user: "Check if the auth implementation matches the requirements doc"
assistant: "I'll verify the implementation."
<commentary>
Pre-merge spec compliance check. The spec-reviewer compares requirements to
actual code, not to claims about code.
</commentary>
assistant: "I'll use the spec-reviewer agent to compare code to requirements."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob

---

