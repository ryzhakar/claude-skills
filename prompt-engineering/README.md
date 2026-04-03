# prompt-engineering

Evaluate and optimize Claude system prompts using Anthropic-grounded patterns.

`prompts` `prompt-engineering` `evaluation` `optimization` 
## Skills

### [prompt-eval](skills/prompt-eval/SKILL.md)
This skill should be used when the user asks to "evaluate a prompt", "review a system prompt", "assess prompt quality", "check if this prompt is good", "audit this prompt", "grade this prompt", or "what's wrong with this prompt". Provides systematic evaluation of Claude system prompts against Anthropic's official guidance. Returns structured assessment with scores and specific findings.


**References:** [`anti-patterns.md`](skills/prompt-eval/references/anti-patterns.md) · [`evaluation-criteria.md`](skills/prompt-eval/references/evaluation-criteria.md) · [`improvement-patterns.md`](skills/prompt-eval/references/improvement-patterns.md) · [`ordering-guide.md`](skills/prompt-eval/references/ordering-guide.md) · [`term-blacklists.md`](skills/prompt-eval/references/term-blacklists.md)
**Examples:** [`sample-evaluation.md`](skills/prompt-eval/examples/sample-evaluation.md)
---

### [prompt-optimize](skills/prompt-optimize/SKILL.md)
This skill should be used when the user asks to "improve this prompt", "optimize a prompt", "fix this system prompt", "make this prompt better", "refactor this prompt", "enhance prompt quality", or "rewrite this prompt". Applies improvement patterns from Anthropic guidance to fix identified issues. Works best after prompt-eval identifies problems, but can also be used standalone.


**Examples:** [`sample-optimization.md`](skills/prompt-optimize/examples/sample-optimization.md)
---

