# manifesto

Create concentrated manifesto declarations and bind Claude behavior to user-provided manifestos through identity-assumption protocols.

`manifesto` `behavioral-binding` `identity` `writing` 
## Skills

### [manifesto-oath](skills/manifesto-oath/SKILL.md)

Binds Claude's operating identity to constitutions, manifestos, and principle sets through identity construction — not theatrical oaths. Triggers on oath/binding requests or when hooks inject constitution elements at session boundaries.


---

### [manifesto-writing](skills/manifesto-writing/SKILL.md)

Trigger when users request manifestos or manifesto tone. Name the enemy, strip hedging, compress to sharp distinctions, end with stark choice.


---

## Agents

### [maximalist-reviewer](agents/maximalist-reviewer.md)

Review a set of files against one manifesto at the manifesto's strongest literal reading, with no allowance for cost, convention, or proportion, and write a report file listing every violation with a compliant rewrite. Use it for an ad-hoc review against a chosen manifesto, outside any mandatory review loop. Examples:

<example>
Context: The user wants a module held to the DRY manifesto without exceptions.
user: "Review src/billing against the dry manifesto, maximally"
assistant: "I'll launch the maximalist-reviewer agent with the dry manifesto and the billing paths."
</example>

<example>
Context: A diff should be checked against a writing standard at full strictness.
user: "Hold this diff to Strunk, no mercy"
assistant: "I'll launch the maximalist-reviewer agent with the Strunk source and the diff range."
</example>


**Model:** `inherit` · **Tools:** Read, Write, Grep, Glob, Bash

---

