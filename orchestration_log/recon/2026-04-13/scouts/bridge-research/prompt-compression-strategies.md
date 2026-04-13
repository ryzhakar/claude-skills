# Prompt Compression Strategies: Official Documentation Research

Scout: bridge-research | Date: 2026-04-13 | Revision: 2 (full rewrite with comprehensive citations)

---

## 1. Prompt Compression -- Achieving Behavioral Compliance with Fewer Tokens

### 1.1 Imperative vs Explanation Trade-offs

**Official position:** Anthropic explicitly recommends providing context/motivation behind instructions over bare imperatives.

> "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses."

**Example from docs:**
- Less effective: `NEVER use ellipses`
- More effective: `Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.`

The docs note: "Claude is smart enough to generalize from the explanation." This means a brief rationale can replace multiple specific rules -- the explanation teaches the principle, and Claude infers the edge cases.

**Resolution of the compression tension:** CLAUDE.md guidance says to keep under 200 lines and cut anything that doesn't prevent mistakes. The prompting guide says to add rationale. These reconcile as follows: explain constraints that require generalization (Claude needs to apply the rule to unforeseen cases). Use bare imperatives for constraints that are binary/mechanical (always/never rules with no edge cases). The question is: "Does Claude need to reason about when/how to apply this?" If yes, explain. If it's categorical, command.

**Citation:** [Prompting best practices > Add context to improve performance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

### 1.2 Claude 4.6 and Aggressive Emphasis Markers ("CRITICAL", "MUST")

Anthropic's official guidance explicitly warns against aggressive emphasis with Claude 4.6:

> "Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models. If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'"

This is a direct quote from the official docs. The guidance is clear: **Claude 4.6 responds worse to aggressive emphasis** -- it overtriggers. Calm, normal instructions produce better calibrated behavior.

**Additional evidence from the "Overthinking" section:**

> "Replace blanket defaults with more targeted instructions. Instead of 'Default to using [tool],' add guidance like 'Use [tool] when it would enhance your understanding of the problem.'"

> "Remove over-prompting. Tools that undertriggered in previous models are likely to trigger appropriately now. Instructions like 'If in doubt, use [tool]' will cause overtriggering."

**Migration note (Claude 4.6):**

> "Tune anti-laziness prompting: If your prompts previously encouraged the model to be more thorough or use tools more aggressively, dial back that guidance. Claude 4.6 models are significantly more proactive and may overtrigger on instructions that were needed for previous models."

**Citation:** [Prompting best practices > Tool usage](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md); [Prompting best practices > Migration considerations](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

### 1.3 When Elaboration Helps vs Hurts

**Helps:**
- Explaining WHY a constraint exists (lets Claude generalize)
- Providing 3-5 examples (most reliable steering mechanism)
- Describing the desired output format positively ("do X" beats "don't do Y")
- Being specific about desired behavior (4.6 migration: "Consider describing exactly what you'd like to see in the output")

**Hurts:**
- Telling Claude what it already knows (the Skill authoring guide's core principle)
- Repeating instructions that previous models needed but 4.6 no longer requires
- Adding blanket "always do X" instructions that cause overtriggering
- Explaining obvious concepts in skills (the 150-token "bad example" vs the 50-token "good example")

**From Skill best practices:**

> "Default assumption: Claude is already very smart. Only add context Claude doesn't already have. Challenge each piece of information: 'Does Claude really need this explanation?' 'Can I assume Claude knows this?' 'Does this paragraph justify its token cost?'"

**Good example (50 tokens):**
```markdown
## Extract PDF text
Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Bad example (150 tokens):**
```markdown
## Extract PDF text
PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available...
```

**Citation:** [Skill authoring best practices > Concise is key](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

---

## 2. Progressive Disclosure Mechanics in Claude Code

### 2.1 Three-Level Loading Architecture

The official architecture defines three distinct loading levels:

| Level | When Loaded | Token Cost | Content |
|-------|-------------|------------|---------|
| **Level 1: Metadata** | Always (at startup) | ~100 tokens per Skill | `name` and `description` from YAML frontmatter |
| **Level 2: Instructions** | When Skill is triggered | Under 5k tokens | SKILL.md body |
| **Level 3+: Resources** | As needed | Effectively unlimited | Bundled files executed via bash |

**Key mechanism:** "Claude loads this metadata at startup and includes it in the system prompt. This lightweight approach means you can install many Skills without context penalty; Claude only knows each Skill exists and when to use it."

**Loading detail:** "When a Skill is triggered, Claude uses bash to read SKILL.md from the filesystem, bringing its instructions into the context window. If those instructions reference other files (like FORMS.md or a database schema), Claude reads those files too using additional bash commands. When instructions mention executable scripts, Claude runs them via bash and receives only the output (the script code itself never enters context)."

**Citation:** [Agent Skills Overview > How Skills work](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md)

### 2.2 How `@references` Work in CLAUDE.md -- EAGER Loading

The `@path/to/file` syntax in CLAUDE.md causes **eager loading** -- imports are expanded at launch time:

> "Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them."

Properties:
- Both relative and absolute paths are allowed
- Relative paths resolve relative to the containing file, not the working directory
- Recursive imports are supported, with a maximum depth of **five hops**
- First external import triggers an approval dialog
- HTML block-level comments in CLAUDE.md (`<!-- notes -->`) are stripped before injection, but comments inside code blocks are preserved

**Example:**
```markdown
See @README for project overview and @package.json for available npm commands.
# Additional Instructions
- git workflow @docs/git-instructions.md
```

**Citation:** [Memory > Import additional files](https://code.claude.com/docs/en/memory.md)

### 2.3 How References Differ in SKILL.md vs CLAUDE.md

**CLAUDE.md `@references`:** EAGER. Expanded at session start. Content is loaded into context immediately and stays there for every API call.

**SKILL.md file references:** LAZY. References in SKILL.md use standard markdown link syntax `[label](path)`. These are NOT expanded at startup. They are not even expanded when the skill is triggered. Claude reads them via bash Read tool only when the skill content directs it to and Claude determines it needs them:

> "Claude accesses these files only when referenced. The filesystem model means each content type has different strengths."

> "When you request something that matches a Skill's description, Claude reads SKILL.md from the filesystem via bash. Only then does this content enter the context window."

**There is no `@import` syntax in SKILL.md.** The reference mechanism is markdown links:
```markdown
**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
```

This is a critical architectural difference:
- CLAUDE.md `@imports` = eager (always loaded at session start)
- SKILL.md markdown links = lazy (loaded on demand when Claude decides)

**Citation:** [Agent Skills Overview > Three types of Skill content](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md); [Claude Code Skills > Add supporting files](https://code.claude.com/docs/en/skills.md)

### 2.4 `disable-model-invocation: true` -- Confirmed to Exist

This field is officially documented with well-defined behavior:

> "Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with `/name`. Default: `false`."

Effect on context loading:

| Frontmatter | You can invoke | Claude can invoke | When loaded into context |
|---|---|---|---|
| (default) | Yes | Yes | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | **Description NOT in context**, full skill loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context, full skill loads when invoked |

**Key finding:** `disable-model-invocation: true` reduces context cost to **absolute zero** until you manually invoke the skill. Not even the description is loaded. This is the most aggressive compression mechanism available.

**Citation:** [Claude Code Skills > Control who invokes a skill](https://code.claude.com/docs/en/skills.md)

### 2.5 Activation Cost: Skill Description Budget

> "Skill descriptions are loaded into context so Claude knows what's available. All skill names are always included, but if you have many skills, descriptions are shortened to fit the character budget, which can strip the keywords Claude needs to match your request. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters."

> "Front-load the key use case: descriptions longer than 250 characters are truncated in the skill listing to reduce context usage."

Tunable via `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.

**Citation:** [Claude Code Skills > Skill descriptions are cut short](https://code.claude.com/docs/en/skills.md)

### 2.6 Skill Content Lifecycle and Compaction Behavior

> "When you or Claude invoke a skill, the rendered SKILL.md content enters the conversation as a single message and stays there for the rest of the session."

> "Auto-compaction carries invoked skills forward within a token budget. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens. Claude Code fills this budget starting from the most recently invoked skill, so older skills can be dropped entirely after compaction if you have invoked many in one session."

**Implication:** Skills that need to survive compaction should front-load their most critical content in the first 5,000 tokens.

**Citation:** [Claude Code Skills > Skill content lifecycle](https://code.claude.com/docs/en/skills.md)

---

## 3. Skill and Agent Sizing -- Length Limits and Context Bloat

### 3.1 SKILL.md Body Size Limit

**Official recommendation: under 500 lines.**

> "Keep SKILL.md body under 500 lines for optimal performance. Split content into separate files when approaching this limit."

> "Use the patterns below to organize instructions, code, and resources effectively" (referring to progressive disclosure patterns).

**Citation:** [Skill authoring best practices > Token budgets](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

### 3.2 CLAUDE.md Recommended Size

**Official recommendation: under 200 lines.**

> "Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."

> "Rule of thumb: Keep CLAUDE.md under 200 lines. If it's growing, move reference content to skills or split into `.claude/rules/` files."

**Migration path when too large:** "Move detailed content into separate files referenced with `@path` imports, or split your instructions across `.claude/rules/` files."

**Citation:** [Memory > Write effective instructions](https://code.claude.com/docs/en/memory.md); [Features overview > CLAUDE.md vs Skill comparison](https://code.claude.com/docs/en/features-overview.md)

### 3.3 Auto Memory Size Cap

> "The first 200 lines of MEMORY.md, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start."

> "This limit applies only to MEMORY.md. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence."

**Citation:** [Memory > How it works](https://code.claude.com/docs/en/memory.md)

### 3.4 When Context Bloat Degrades Performance

The docs provide multiple signals about degradation:

1. **Skill description truncation:** When too many skills are installed, descriptions get truncated to fit the 1%-of-context-window budget, causing misrouting.

2. **Post-compaction skill loss:** Skills share a combined 25,000-token compaction budget. Older skills are dropped if many were invoked.

3. **First 5,000 tokens rule:** After compaction, each skill retains only its first 5,000 tokens.

4. **CLAUDE.md adherence degradation:** "Longer files consume more context and reduce adherence."

5. **General context cost warning from features overview:** "Too much [context] can fill up your context window, but it can also add noise that makes Claude less effective; skills may not trigger correctly, or Claude may lose track of your conventions."

**Citation:** [Claude Code Skills > Skill content lifecycle](https://code.claude.com/docs/en/skills.md); [Features overview > Understand context costs](https://code.claude.com/docs/en/features-overview.md)

### 3.5 Skill Description Field Limits

- `name`: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words ("anthropic", "claude")
- `description`: Maximum 1024 characters (hard validation limit), must be non-empty, no XML tags
- **Effective display limit:** 250 characters (truncated beyond this in skill listing context)

**Citation:** [Claude Code Skills > Frontmatter reference](https://code.claude.com/docs/en/skills.md); [Agent Skills Overview > Skill structure](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md)

---

## 4. XML Tags vs Markdown -- Structural Format for Instruction Following

### 4.1 Official Recommendation

Anthropic explicitly recommends XML tags for structured prompts:

> "XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs. Wrapping each type of content in its own tag (e.g. `<instructions>`, `<context>`, `<input>`) reduces misinterpretation."

**Best practices for XML tags:**
- Use consistent, descriptive tag names across prompts
- Nest tags when content has a natural hierarchy

### 4.2 When to Use Which

**XML tags are recommended for:**
- Mixing different content types (instructions + context + examples + inputs)
- Controlling output format (e.g., `<smoothly_flowing_prose_paragraphs>` tags)
- Providing few-shot examples (wrap in `<example>` / `<examples>` tags)
- Separating long documents with metadata (`<document index="n">`, `<document_content>`, `<source>`)
- Wrapping behavioral directive blocks in system prompts

**Markdown is the native format for:**
- CLAUDE.md files (loaded as markdown)
- SKILL.md content (the skill system itself is markdown)
- `.claude/rules/` files
- Subagent definitions (markdown body)

### 4.3 XML Tags in Anthropic's Own System Prompt Patterns

The prompting best practices page provides extensive real-world XML-tagged instruction blocks used by Anthropic:

```xml
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the
tool calls, make all of the independent tool calls in parallel...
</use_parallel_tool_calls>
```

```xml
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's
intent is unclear, infer the most useful likely action and proceed...
</default_to_action>
```

```xml
<do_not_act_before_instructions>
Do not jump into implementation or change files unless clearly instructed to
make changes...
</do_not_act_before_instructions>
```

```xml
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any
long-form content, write in clear, flowing prose...
</avoid_excessive_markdown_and_bullet_points>
```

```xml
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a
specific file, you MUST read the file before answering...
</investigate_before_answering>
```

```xml
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend
design, this creates what users call the "AI slop" aesthetic...
</frontend_aesthetics>
```

**Pattern:** Anthropic uses XML tags to wrap behavioral directives in system prompts. The tag names are descriptive and serve as both delimiters and semantic labels. This is the recommended approach for API-level system prompts.

### 4.4 XML for Output Format Control

> "Tell Claude what to do instead of what not to do."
> "Instead of: 'Do not use markdown in your response'"
> "Try: 'Your response should be composed of smoothly flowing prose paragraphs.'"
> Also: "Write the prose sections of your response in `<smoothly_flowing_prose_paragraphs>` tags."

XML tags as format indicators are a distinct technique: using an XML tag to define where content should go rather than just wrapping instructions.

### 4.5 Token Efficiency Comparison

XML tags add approximately 2-4 tokens per tag pair. Markdown headers add approximately 2-3 tokens. The structural benefit of XML for complex prompts outweighs the marginal token cost. For simple lists of rules (like in CLAUDE.md), markdown bullets are more token-efficient.

**Practical guidance:**

| Content Type | Recommended Format | Why |
|---|---|---|
| Behavioral constraints in system prompts | XML tags | Unambiguous parsing, official pattern |
| Skill instructions | Markdown | Native format for SKILL.md |
| CLAUDE.md rules | Markdown bullets | Scannable, concise |
| Multi-section prompts mixing instructions + data | XML tags | Prevents misinterpretation |
| Few-shot examples | `<example>` XML tags | Explicitly recommended by Anthropic |
| Document structure in prompts | `<document>` XML tags | Explicit recommendation for metadata |
| Output format control | XML tags | "Write in `<tag>` tags" pattern |

**Citation:** [Prompting best practices > Structure prompts with XML tags; Control the format of responses](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

---

## 5. Constraint Density vs Explained Constraints

### 5.1 Explained Constraints Achieve Better Compliance

The docs consistently favor explained constraints over dense rule lists:

> "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses."

The ellipsis example is canonical: the bare imperative `NEVER use ellipses` is labeled "Less effective," while the version with rationale ("read aloud by text-to-speech engine") is labeled "More effective."

### 5.2 For CLAUDE.md: Specificity Over Density

> "Write instructions that are concrete enough to verify."

Examples from the docs:
- "Use 2-space indentation" instead of "Format code properly"
- "Run `npm test` before committing" instead of "Test your changes"
- "API handlers live in `src/api/handlers/`" instead of "Keep files organized"

### 5.3 For Skills: Match Freedom to Fragility

The Skill best practices doc introduces a specificity spectrum:

**High freedom** (text-based instructions): When multiple approaches are valid, decisions depend on context, heuristics guide the approach. Example: code review checklists.

**Medium freedom** (pseudocode/scripts with parameters): When a preferred pattern exists, some variation is acceptable. Example: report generation templates.

**Low freedom** (specific scripts, no parameters): When operations are fragile, consistency is critical, a specific sequence must be followed. Example: database migrations with exact command sequences.

> "Think of Claude as a robot exploring a path: Narrow bridge with cliffs on both sides: There's only one safe way forward. Provide specific guardrails and exact instructions (low freedom). Open field with no hazards: Many paths lead to success. Give general direction and trust Claude to find the best route (high freedom)."

**Citation:** [Skill authoring best practices > Set appropriate degrees of freedom](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

### 5.4 Thinking Guidance: General Instructions Beat Prescriptive Steps

> "Prefer general instructions over prescriptive steps. A prompt like 'think thoroughly' often produces better reasoning than a hand-written step-by-step plan. Claude's reasoning frequently exceeds what a human would prescribe."

This is both more token-efficient AND more effective.

### 5.5 Tell What To Do, Not What Not To Do

> "Instead of: 'Do not use markdown in your response'"
> "Try: 'Your response should be composed of smoothly flowing prose paragraphs.'"

Positive instructions are both more token-efficient (no negation overhead) and more effective (Claude knows what TO do rather than only what to avoid).

**Citation:** [Prompting best practices > Control the format of responses; Leverage thinking](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)

---

## 6. Examples vs Rules -- Token-Efficiency Trade-off

### 6.1 Official Position: Examples Are the Most Reliable Steering Mechanism

> "Examples are one of the most reliable ways to steer Claude's output format, tone, and structure. A few well-crafted examples (known as few-shot or multishot prompting) can dramatically improve accuracy and consistency."

### 6.2 Recommended Example Count

> "Include 3-5 examples for best results."

### 6.3 Example Quality Criteria

When adding examples, make them:
- **Relevant:** Mirror your actual use case closely
- **Diverse:** Cover edge cases and vary enough that Claude doesn't pick up unintended patterns
- **Structured:** Wrap examples in `<example>` tags (multiple in `<examples>` tags) so Claude can distinguish them from instructions

### 6.4 Example Tagging Format

```xml
<examples>
  <example>
    Input: Added user authentication with JWT tokens
    Output:
    feat(auth): implement JWT-based authentication
    Add login endpoint and token validation middleware
  </example>
  <example>
    Input: Fixed bug where dates displayed incorrectly in reports
    Output:
    fix(reports): correct date formatting in timezone conversion
    Use UTC timestamps consistently across report generation
  </example>
</examples>
```

### 6.5 Examples with Thinking

> "Multishot examples work with thinking. Use `<thinking>` tags inside your few-shot examples to show Claude the reasoning pattern. It will generalize that style to its own extended thinking blocks."

### 6.6 Self-Generated Examples

> "You can also ask Claude to evaluate your examples for relevance and diversity, or to generate additional ones based on your initial set."

### 6.7 When Rules Beat Examples

The docs suggest rules are preferred when:
- The instruction is a simple, verifiable constraint ("Use 2-space indentation") -- a rule is ~5 tokens vs an example at 50+
- The behavior is binary (do/don't)
- The context is obvious and doesn't need demonstration

Examples are preferred when:
- Output format, tone, or structure needs steering
- The pattern is complex enough that a rule would be ambiguous
- Edge cases matter and a few demonstrations teach the pattern better than enumeration

### 6.8 Skill-Specific Examples Pattern

The Skill best practices guide provides a distinct "Examples pattern" for skills:

> "For Skills where output quality depends on seeing examples, provide input/output pairs just like in regular prompting."

This uses a slightly different format inside skills -- markdown-formatted input/output pairs rather than XML tags, since skills are markdown documents. The docs show commit message examples, code review examples, and template-filling examples.

**Citation:** [Prompting best practices > Use examples effectively](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md); [Skill authoring best practices > Examples pattern](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

---

## 7. Skill Description Frontmatter -- How Claude Code Uses It

### 7.1 How Descriptions Drive Skill Discovery

The description is the primary mechanism for skill selection:

> "Each Skill has exactly one description field. The description is critical for skill selection: Claude uses it to choose the right Skill from potentially 100+ available Skills. Your description must provide enough detail for Claude to know when to select this Skill, while the rest of SKILL.md provides the implementation details."

From the Claude Code docs:

> "If omitted, uses the first paragraph of markdown content."

### 7.2 Character Limits (Complete Reference)

| Constraint | Value | Source |
|---|---|---|
| `name` max length | 64 characters | Agent Skills Overview |
| `name` allowed chars | lowercase letters, numbers, hyphens only | Agent Skills Overview |
| `name` prohibited content | XML tags, reserved words ("anthropic", "claude") | Agent Skills Overview |
| `description` max length | 1,024 characters (hard validation limit) | Agent Skills Overview |
| `description` display truncation | 250 characters (in skill listing) | Claude Code Skills |
| Total description budget | 1% of context window, fallback 8,000 characters | Claude Code Skills |
| Budget override | `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var | Claude Code Skills |

### 7.3 Writing Triggering Descriptions

**Always write in third person:**

> "The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems."
> - Good: "Processes Excel files and generates reports"
> - Avoid: "I can help you process Excel files"
> - Avoid: "You can use this to process Excel files"

**Include both what AND when:**

```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

```yaml
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

```yaml
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Avoid vague descriptions:**

```yaml
# BAD -- will not trigger correctly
description: Helps with documents
description: Processes data
description: Does stuff with files
```

### 7.4 How Description Interacts with `disable-model-invocation`

When `disable-model-invocation: true` is set, the description is NOT loaded into the system prompt at all. This means:
- Zero context cost
- No possibility of auto-triggering
- The description becomes purely for human reference and `/` autocomplete display

When `disable-model-invocation` is false (default), the description is loaded into the system prompt alongside all other skill descriptions, competing within the 1%-of-context-window budget.

### 7.5 Naming Conventions

Official recommendation: use gerund form (verb + -ing):
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`
- `testing-code`
- `writing-documentation`

**Acceptable alternatives:**
- Noun phrases: `pdf-processing`, `spreadsheet-analysis`
- Action-oriented: `process-pdfs`, `analyze-spreadsheets`

**Avoid:**
- Vague names: `helper`, `utils`, `tools`
- Overly generic: `documents`, `data`, `files`
- Reserved words: `anthropic-helper`, `claude-tools`

**Citation:** [Skill authoring best practices > Writing effective descriptions; Naming conventions](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md); [Claude Code Skills > Frontmatter reference](https://code.claude.com/docs/en/skills.md)

---

## 8. Reference (`@`) Syntax -- Exact Behavior

### 8.1 `@` in CLAUDE.md: Eager Expansion

**Behavior:** `@path/to/file` references in CLAUDE.md are expanded at session launch. The referenced file's content is inlined into the context alongside the CLAUDE.md content.

**Properties:**
- Both relative and absolute paths supported
- Relative paths resolve relative to the containing file, not the working directory
- Recursive imports up to 5 hops deep
- First external import triggers an approval dialog
- Imported content persists through compaction (project-root CLAUDE.md survives compaction and is re-read from disk)
- Home directory paths supported: `@~/.claude/my-project-instructions.md`
- HTML block comments are stripped from loaded content (saves tokens for maintainer notes)

**Example:**
```markdown
See @README for project overview and @package.json for available npm commands.
# Additional Instructions
- git workflow @docs/git-instructions.md
```

**AGENTS.md interop:**
```markdown
@AGENTS.md

## Claude Code
Use plan mode for changes under `src/billing/`.
```

**Citation:** [Memory > Import additional files](https://code.claude.com/docs/en/memory.md)

### 8.2 File References in SKILL.md: Lazy, Non-`@` Syntax

SKILL.md files do NOT use `@` import syntax. They use standard markdown link syntax `[label](path)`. These are NOT expanded at load time. Claude reads them via bash tools when it determines they are needed:

> "Reference supporting files from SKILL.md so Claude knows what each file contains and when to load it."

```markdown
## Additional resources
- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

**There is no `@import` mechanism in SKILL.md.** The behavior is fundamentally different:

| Feature | CLAUDE.md `@path` | SKILL.md `[label](path)` |
|---|---|---|
| Expansion timing | Eager (session start) | Lazy (when Claude reads) |
| Mechanism | Pre-processor expansion | Claude's Read tool |
| Token cost | Immediate, every request | On-demand, only when needed |
| Recursion | Up to 5 hops | One level recommended |
| Approval dialog | Yes (first time) | No (Claude reads files normally) |

**Citation:** [Agent Skills Overview > Level 3: Resources and code](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md); [Skill authoring best practices > Progressive disclosure patterns](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md); [Claude Code Skills > Add supporting files](https://code.claude.com/docs/en/skills.md)

### 8.3 Nesting Depth Warning for Skills

> "Claude may partially read files when they're referenced from other referenced files. When encountering nested references, Claude might use commands like `head -100` to preview content rather than reading entire files, resulting in incomplete information."

> "Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md to ensure Claude reads complete files when needed."

**Bad (too deep):**
```
SKILL.md -> advanced.md -> details.md -> actual info
```

**Good (one level):**
```
SKILL.md -> advanced.md
SKILL.md -> reference.md
SKILL.md -> examples.md
```

### 8.4 Table of Contents for Long Reference Files

> "For reference files longer than 100 lines, include a table of contents at the top. This ensures Claude can see the full scope of available information even when previewing with partial reads."

**Citation:** [Skill authoring best practices > Avoid deeply nested references; Structure longer reference files](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)

---

## 9. Synthesis: Token-Cost Hierarchy and Compression Strategies

### 9.1 Token-Cost Hierarchy (cheapest to most expensive)

1. **Zero cost:** `disable-model-invocation: true` skills (nothing loaded until manual invocation)
2. **Zero cost:** Hooks (run externally, unless they return context)
3. **~100 tokens each:** Skill metadata (name + description, always loaded for model-invocable skills)
4. **Variable, on-demand:** Skill body (loaded when triggered, recommended under 5k tokens)
5. **Variable, on-demand:** Skill reference files (loaded only when Claude reads them)
6. **Conditional:** `.claude/rules/` with `paths:` frontmatter (loaded when Claude reads matching files)
7. **Every request:** `.claude/rules/` without path scope (loaded at session start)
8. **Every request:** CLAUDE.md content (loaded at session start, present in every API call)
9. **Every request:** CLAUDE.md `@imports` (eagerly expanded into CLAUDE.md content)
10. **Every request:** MCP tool names (loaded at start, full schemas deferred until use)

### 9.2 Compression Techniques with Official Backing

| Technique | Official Support | Citation |
|---|---|---|
| Move procedures from CLAUDE.md to skills | Explicit: "moving specialized instructions into skills keeps your base context smaller" | [Costs > Move instructions](https://code.claude.com/docs/en/costs.md) |
| Keep CLAUDE.md under 200 lines | Explicit: "target under 200 lines" | [Memory > Write effective instructions](https://code.claude.com/docs/en/memory.md) |
| Keep SKILL.md under 500 lines | Explicit: "under 500 lines for optimal performance" | [Skill best practices > Token budgets](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md) |
| Use path-scoped rules | Explicit: "only apply when Claude is working with files matching the specified patterns" | [Memory > Path-specific rules](https://code.claude.com/docs/en/memory.md) |
| Front-load description in first 250 chars | Explicit: "descriptions longer than 250 characters are truncated" | [Claude Code Skills > Frontmatter reference](https://code.claude.com/docs/en/skills.md) |
| Remove "CRITICAL"/"MUST" on Claude 4.6 | Explicit: "dial back any aggressive language" | [Prompting best practices > Tool usage](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md) |
| Provide rationale instead of bare imperatives | Explicit: "context or motivation...can help Claude better understand" | [Prompting best practices > Add context](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md) |
| Use 3-5 examples instead of enumerating rules | Explicit: "Include 3-5 examples for best results" | [Prompting best practices > Use examples](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md) |
| Wrap behavioral directives in XML tags | Explicit (all official examples use this pattern) | [Prompting best practices > Structure prompts with XML tags](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md) |
| Assume Claude's baseline knowledge | Explicit: "Only add context Claude doesn't already have" | [Skill best practices > Concise is key](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md) |
| Use `context: fork` to isolate verbose work | Explicit: "results summarized and returned to your main conversation" | [Claude Code Skills > Run skills in a subagent](https://code.claude.com/docs/en/skills.md) |
| Tell Claude what to do, not what not to do | Explicit: positive framing is "more effective" | [Prompting best practices > Control the format](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md) |
| Use hooks for deterministic enforcement | Explicit: "use hooks to enforce behavior deterministically" | [Claude Code Skills > Skill content lifecycle](https://code.claude.com/docs/en/skills.md) |
| Use `disable-model-invocation: true` for manual-only skills | Explicit: "Description not in context" | [Claude Code Skills > Control who invokes](https://code.claude.com/docs/en/skills.md) |
| Strip HTML comments from CLAUDE.md | Implicit: "Block-level HTML comments are stripped before injection" | [Memory > How CLAUDE.md files load](https://code.claude.com/docs/en/memory.md) |
| Use general instructions over prescriptive steps | Explicit: "often produces better reasoning than a hand-written step-by-step plan" | [Prompting best practices > Thinking](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md) |

### 9.3 Key Anti-Patterns for Claude 4.6

1. **Over-emphasis:** "CRITICAL", "MUST", "ALWAYS" cause overtriggering on 4.6. Use calm, direct language.
2. **Blanket defaults:** "Default to using [tool]" causes overuse. Replace with conditional: "Use [tool] when it would enhance your understanding."
3. **Safety hedges from older models:** "If in doubt, use [tool]" -- remove for 4.6.
4. **Redundant explanations:** Explaining what PDFs are in a PDF-processing skill wastes tokens.
5. **Deep nesting:** References 2+ levels deep from SKILL.md get partially read. Keep one level deep.
6. **Vague descriptions:** "Helps with documents" will not trigger correctly against 100+ skills.
7. **Anti-laziness prompting:** "Be thorough and comprehensive" / "ALWAYS check" -- 4.6 is already proactive.
8. **Negative framing:** "Don't use markdown" -- use positive: "Write in flowing prose paragraphs."
9. **Overlong CLAUDE.md:** Files over 200 lines "reduce adherence."
10. **Multiple options without a default:** Presenting many approaches confuses; provide a default with an escape hatch.

---

## 10. Documentation Sources Consulted

All findings are derived from the following official Anthropic documentation pages, fetched 2026-04-13:

| # | Page | URL | Key Topics |
|---|---|---|---|
| 1 | Prompting best practices | [link](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md) | XML tags, examples, emphasis, formatting, tool usage, agentic systems, migration |
| 2 | Skill authoring best practices | [link](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md) | Conciseness, progressive disclosure, descriptions, examples pattern, degrees of freedom, token budgets |
| 3 | Agent Skills Overview | [link](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md) | Three-level loading, skill structure, field requirements, architecture |
| 4 | Claude Code Skills | [link](https://code.claude.com/docs/en/skills.md) | Frontmatter reference, `disable-model-invocation`, description budgets, compaction, supporting files, lifecycle |
| 5 | Memory (CLAUDE.md) | [link](https://code.claude.com/docs/en/memory.md) | `@import` syntax, size recommendations, loading behavior, rules, path-scoped rules |
| 6 | Features overview | [link](https://code.claude.com/docs/en/features-overview.md) | Context cost by feature, loading timeline, feature comparison tables |
| 7 | Managing costs | [link](https://code.claude.com/docs/en/costs.md) | Token reduction strategies, CLAUDE.md-to-skill migration |
| 8 | What's new in Claude 4.6 | [link](https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6.md) | Adaptive thinking, model changes, deprecations |
| 9 | Prompt engineering overview | [link](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview.md) | Navigation to best practices |

**Note:** WebSearch was unavailable in this environment (Vertex AI policy restriction). All findings are from official Anthropic documentation only. Community patterns and third-party guides were not consulted.
