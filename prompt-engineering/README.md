# prompt-engineering

Evaluate and optimize Claude system prompts using Anthropic-grounded patterns.

`prompts` `prompt-engineering` `evaluation` `optimization` 
## Agents

### [prompt-eval](agents/prompt-eval.md)

Evaluate a Claude system prompt against a structured rubric. Use when asked to "evaluate a prompt", "review a system prompt", "assess prompt quality", "audit this prompt", "grade this prompt", or "score this prompt". Produces a file-artifact evaluation report with scores, violations, and prioritized recommendations.

<example>
Context: Orchestrator wants to evaluate a skill before optimizing it.
user: "Evaluate the prompt at path/to/SKILL.md and write the report to path/to/eval-report.md"
assistant: "I'll dispatch prompt-eval to assess the prompt against the rubric."
</example>

<example>
Context: User wants to check an agent definition for quality issues.
user: "Grade the agent prompt at .claude/agents/reviewer.md"
assistant: "I'll use prompt-eval to score the agent prompt and surface violations."
</example>


**Model:** `sonnet` · **Tools:** Read, Write, Grep, Glob

---

### [prompt-optimize](agents/prompt-optimize.md)

Optimize a Claude system prompt by applying improvement patterns. Use when asked to "improve this prompt", "optimize a prompt", "fix this system prompt", "make this prompt better", "refactor this prompt", "rewrite this prompt", or "enhance prompt quality". Reads a prompt file, applies prioritized fixes, writes the optimized prompt and a changes report.

<example>
Context: Orchestrator has an eval report and wants to fix the identified issues.
user: "Optimize the prompt at path/to/SKILL.md using the eval report at path/to/eval-report.md. Write results to path/to/output/"
assistant: "I'll dispatch prompt-optimize to apply improvement patterns based on the evaluation."
</example>

<example>
Context: User wants standalone prompt improvement without a prior evaluation.
user: "Improve the agent prompt at .claude/agents/helper.md and write the result to .claude/agents/helper-v2.md"
assistant: "I'll use prompt-optimize to run a quick scan and apply fixes."
</example>


**Model:** `sonnet` · **Tools:** Read, Write, Edit, Grep, Glob

---

