# System Prompt Ordering Guide

Canonical ordering for system prompt components, synthesized from Anthropic documentation and prompt engineering tutorial.

---

## The 10-Element Ordering

Recommended order for comprehensive system prompts:

| Position | Element | Purpose | Required? |
|----------|---------|---------|-----------|
| 1 | Role/Identity | Establish persona and expertise | Recommended |
| 2 | Context/Background | Domain, audience, situation | When relevant |
| 3 | Constraints/Boundaries | What NOT to do, scope limits | Required |
| 4 | Detailed Rules | Specific behavioral rules | When complex |
| 5 | Examples | Demonstrate desired behavior | For complex tasks |
| 6 | Input Data | Variable content to process | When applicable |
| 7 | Immediate Task | What to do right now | Required |
| 8 | Reasoning Request | "Think step by step" | For complex reasoning |
| 9 | Output Format | Structure specification | Recommended |
| 10 | Prefill | Start assistant response | Optional |

---

## Element Details

### 1. Role/Identity

**What**: Define who Claude is for this task
**Why**: Role prompting is the most powerful technique for improving performance
**Pattern**:
```
You are a [specific role] with expertise in [domain].
```

**Examples**:
- `You are a senior financial analyst at a Fortune 500 company.`
- `You are a pediatric nurse explaining medical concepts to worried parents.`
- `You are a security researcher analyzing code for vulnerabilities.`

**Position rationale**: Sets context for everything that follows

---

### 2. Context/Background

**What**: Domain knowledge, business context, audience information
**Why**: Claude performs better with more contextual information
**Pattern**:
```
Context:
- This is for [audience/use case]
- The [domain] works like [explanation]
- Key terminology: [definitions]
```

**Examples**:
- Company-specific processes
- Industry terminology
- User skill level
- What the output will be used for

**Position rationale**: Informs interpretation of rules and task

---

### 3. Constraints/Boundaries

**What**: Explicit limitations on behavior and scope
**Why**: Prevents overreach and establishes safety boundaries
**Pattern**:
```
You handle:
- [in-scope item 1]
- [in-scope item 2]

You do NOT handle:
- [out-of-scope item 1]
- [out-of-scope item 2]

You cannot:
- [capability limit 1]
```

**Position rationale**: Must be established before detailed rules to frame them

---

### 4. Detailed Rules

**What**: Specific behavioral instructions and edge cases
**Why**: Covers situations not addressed by general constraints
**Pattern**:
```
Rules:
1. When [condition], do [action]
2. If [situation], then [response]
3. Never [forbidden action]
```

**Position rationale**: Builds on constraints with specifics

---

### 5. Examples

**What**: Input/output pairs demonstrating desired behavior
**Why**: Most effective tool for communicating expected behavior
**Pattern**:
```
<examples>
<example>
<input>[sample input]</input>
<output>[expected output]</output>
</example>
</examples>
```

**Best practices**:
- 3-5 diverse examples for complex tasks
- Include edge cases
- Show both input AND output
- Use tags for clear boundaries

**Position rationale**: Before task so Claude has patterns to match

---

### 6. Input Data

**What**: Variable content to be processed
**Why**: Separates data from instructions
**Pattern**:
```
<data_type>
[variable content]
</data_type>
```

**Tag naming**:
- Use descriptive names: `<email>`, `<document>`, `<code>`
- Not generic: `<data>`, `<input>`

**Position rationale**: After examples (which explain how to process it)

---

### 7. Immediate Task

**What**: Specific action to perform now
**Why**: Clear directive ensures correct action
**Pattern**:
```
Based on the above, [specific task].
```

**Examples**:
- `Analyze the document and extract the key findings.`
- `Respond to the customer's question.`
- `Review the code for security vulnerabilities.`

**Position rationale**: Near end so all context is established

---

### 8. Reasoning Request

**What**: Instruction to think before answering
**Why**: Improves accuracy on complex tasks
**Pattern**:
```
Think through your approach in <reasoning> tags before providing your answer.
```

**Critical note**: Thinking only counts when out loud. Silent thinking has no effect.

**Position rationale**: Before output format to ensure reasoning precedes answer

---

### 9. Output Format

**What**: Structure specification for response
**Why**: Ensures consistent, parseable output
**Pattern**:
```
Format your response as:
<response>
  <field1>[content]</field1>
  <field2>[content]</field2>
</response>
```

**Include**:
- Structure (XML, JSON, bullets, etc.)
- Length constraints
- What to exclude ("skip preamble")
- Edge case handling ("if unknown, use 'N/A'")

**Position rationale**: Near end for recency effect; better than at beginning

---

### 10. Prefill (Optional)

**What**: Start the assistant's response
**Why**: Enforces format, skips preamble, steers direction
**Pattern**:
```python
messages = [
    {"role": "user", "content": prompt},
    {"role": "assistant", "content": "<response>"}  # Prefill
]
```

**Use cases**:
- Force XML/JSON output
- Skip introductory text
- Maintain conversation character

**Position rationale**: Must be last (in assistant turn)

---

## Ordering Variations by Prompt Type

### Simple Query Prompt
```
1. Task (required)
2. Output format (if needed)
```

### Complex Analysis Prompt
```
1. Role
2. Context
3. Constraints
4. Rules
5. Examples
6. Input data
7. Task
8. Reasoning request
9. Output format
```

### Agent/Skill System Prompt
```
1. Role/Identity
2. Purpose statement
3. Constraints/Boundaries
4. Workflow steps
5. Output format
6. Error handling
```

### Data Processing Prompt
```
1. Context (optional)
2. Constraints
3. Examples (critical)
4. Input data (tagged)
5. Task
6. Output format
```

---

## Anti-Patterns in Ordering

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Format at beginning | Less effective than end | Move to position 9 |
| Examples after task | Pattern not established | Move before task |
| Constraints scattered | Easy to miss | Group in position 3 |
| Task before context | Missing framing | Context first |
| Data mixed with instructions | Confusion | Tag data separately |

---

## Quick Reference

**Minimal prompt**: Task + Format
**Standard prompt**: Role + Context + Constraints + Task + Format
**Complex prompt**: All 10 elements
**Agent prompt**: Role + Purpose + Constraints + Workflow + Format + Error handling

---

## Validation Checklist

When reviewing prompt ordering:

- [ ] Role/context comes before rules
- [ ] Constraints come before detailed rules
- [ ] Examples come before task
- [ ] Data is tagged and separate from instructions
- [ ] Task is near the end (after context established)
- [ ] Reasoning request (if any) comes before output format
- [ ] Output format is near the end
- [ ] Prefill (if used) is in assistant turn
