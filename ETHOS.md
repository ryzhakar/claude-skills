# Plugin Ethos

Principles governing how plugins, skills, agents, and hooks are created and maintained in this marketplace. Every principle traces to observed model behavior or documented platform constraints.

## Self-containment

Skills and agents work without reference file reads. Models ignore @references in practice — content not in the body does not get followed. Inline all essential content. Compress through prose tightening, not through deferral to files.

References survive ONLY when all three conditions hold: genuinely rare trigger condition, large after compression (>1000t), and an unavoidable loading gate that makes skipping impossible.

When skills share reference content, each inlines its own domain deeply and the other domain lightly. Cross-skill duplication for self-containment is acceptable.

## Strong directive language

Models need a strong hand. Write commands, not suggestions. "Do X" not "Consider doing X." "NEVER Y" not "Try to avoid Y." Emphatic markers (MUST, NEVER, CRITICAL) are intentional design — preserve them during edits.

On Claude 4.6, dial back stacking of multiple aggressive markers on one instruction. One emphatic marker per directive. Calm force beats shouted repetition.

## Token economy

Measure with `just tokens FILE`. Compress through Strunk principles: active voice, positive form, concrete language, omit needless words, parallel construction, emphatic position. Tables replace prose for mappings. Decision trees replace explanatory paragraphs.

## No platform coupling

Skills produce file artifacts, not platform API calls. No `gh issue create`, no GitHub-specific workflows. Output is documents on disk. The user decides where to publish.

## Verb interpretation for orchestrators

Orchestration skills (agentic-delegation, dev-orchestration, research-tree, qa-orchestration) teach the model that user action verbs ("do", "make", "research", "implement", "fix", "write", "check") are delegation directives. The orchestrator decomposes, delegates, and assembles — it never executes.

## Platform facts, not policy rules

When describing system constraints, state what the platform does, not what the agent should do. "Agents cannot launch other agents — the Agent tool is unavailable to subagents" (platform fact) vs "Agents must not launch other agents" (policy rule that implies choice).

## Hooks: modularity and gating

One-time hooks (SessionStart, PostCompact, SubagentStart) can be thorough — they are context injections, not per-call overhead. Extract prompt text into template files (`hooks/templates/*.txt`) for modularity. Gate all hooks on config existence — invisible when unconfigured.

## Core points as untouchable spine

When optimizing a skill, identify its 5 core points first (what it most emphatically communicates). These survive and remain the most prominent elements in any rewrite. Compression amplifies core points; it never buries them.

## Analysis before action

Full optimization follows: 4-dimension analysis (reference optionality, core points, Strunk prose, prompt-eval scoring) → bridge research (compression strategies, platform criteria) → per-unit synthesis → per-plugin implementation. Each phase produces artifacts on disk, verified before proceeding.

## Paired enforcement

Mandatory steps in agent bodies cannot self-enforce. Agents skip silently without consequence. Every mandatory step pairs two things: a verifiable artifact at an established path, and an orchestrator-side post-dispatch check that fails on missing artifact. Agent-side directives alone are aspirational.

Reuse the established artifact map. New paths multiply the verification surface and complicate downstream consumers.
