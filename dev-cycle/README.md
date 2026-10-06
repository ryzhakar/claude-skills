# dev-cycle

Development cycle orchestration: specify, plan, implement, review, integrate. A spec-capturer that interviews the owner, worktree-isolated implementers, spec and code-quality reviewers, and a review chain enforced by hooks.

`orchestration` `lifecycle` `specification` `planning` `code-review` `worktree` `hooks` 
## Skills

### [dev-cycle](skills/dev-cycle/SKILL.md)

Drive the specify, plan, implement, review, and integrate loop over software work through the spec-capturer, implementer, spec-reviewer, and code-quality-reviewer agents, as an extension of agentic-delegation. "specify and implement", "implement a feature end-to-end", "build this with agents", "orchestrate development", "run the dev cycle", "implement using subagents", "dispatch implementers", "coordinate implementation and review", "fix this", "refactor this", "test this", or any coding task an orchestrator delegates.


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
Context: An implementation plan has five units. Unit 1 assigns the requirements of an authentication middleware.
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

### [spec-capturer](agents/spec-capturer.md)

Interview the owner through the AskUserQuestion tool, by the spec-chef skill's protocol, and turn a request into one specification file. Use it at the start of a development cycle before any plan exists, or when a request leaves product decisions implicit. Examples:

<example>
Context: The owner asks for a feature in two sentences and no spec exists.
user: "Build invoice export for the billing module"
assistant: "I'll launch the spec-capturer agent to interview you and write the spec first."
</example>

<example>
Context: A requirements document exists but leaves scope and edge cases open.
user: "Turn docs/export-notes.md into a spec we can implement"
assistant: "I'll launch the spec-capturer agent to close the gaps with you and write the spec file."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, Skill, SendMessage, WebFetch, WebSearch

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


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob, Bash, Skill

---

