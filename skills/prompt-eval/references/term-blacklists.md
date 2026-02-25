# Term Blacklists for Prompt Evaluation

Lists of terms that indicate vague, problematic, or inefficient prompt language. Use during evaluation to flag issues.

---

## Vague Qualitative Terms

Terms that require definition but are often used without one:

### Quality Descriptors
- good / bad
- appropriate / inappropriate
- relevant / irrelevant
- proper / improper
- suitable / unsuitable
- acceptable / unacceptable
- adequate / inadequate
- sufficient / insufficient

### Quantity Descriptors
- short / long (without word count)
- brief / detailed (without specification)
- few / many / several
- some / most / all (when precision needed)
- comprehensive (without scope)
- thorough (without criteria)

### Evaluation Terms
- best / worst
- optimal / suboptimal
- ideal / non-ideal
- important / unimportant
- significant / insignificant
- reasonable / unreasonable
- clear / unclear (ironic when used vaguely)

### Timing Terms
- soon / later
- quickly / slowly (without time bounds)
- as needed / when necessary
- if appropriate / if relevant

---

## Filler Phrases (Token Waste)

Phrases that add no information value:

### Unnecessary Politeness
- Please be sure to
- I would like you to
- Could you please
- It would be great if you could
- I'd appreciate it if

### Hedging Language
- Try to / Attempt to
- Do your best to
- If possible
- When you can
- As much as possible

### Redundant Qualifiers
- Very / Really / Quite / Extremely
- Basically / Essentially / Fundamentally
- Actually / Literally
- In order to (just use "to")
- The fact that

### Verbose Constructions
- "It is important to note that" → just state the thing
- "Please make sure that" → just give the instruction
- "You should be aware that" → just state the fact
- "Keep in mind that" → just include the information
- "Don't forget to" → just give the instruction

---

## Contradictory Instruction Pairs

Pairs that often appear together but conflict:

| Instruction A | Instruction B | Conflict |
|---------------|---------------|----------|
| Be thorough | Be concise | Thoroughness requires length |
| Be comprehensive | Keep it brief | Comprehensiveness requires detail |
| Include all details | Be succinct | Mutually exclusive |
| Explain in depth | Keep response short | Depth requires space |
| Be creative | Follow exactly | Creativity needs freedom |
| Be formal | Be conversational | Tone contradiction |
| Be cautious | Act decisively | Approach contradiction |

### Resolution Pattern
Instead of conflicting pairs, use specific guidance:
```
❌ Be thorough but concise.
✅ Provide analysis of 3 key factors. Use 2-3 sentences per factor.
```

---

## Ambiguous Instruction Verbs

Verbs that require clarification:

### Analysis Verbs (need scope)
- Analyze → Analyze what aspects?
- Evaluate → Evaluate against what criteria?
- Assess → Assess for what purpose?
- Review → Review for what issues?
- Examine → Examine what elements?

### Action Verbs (need parameters)
- Process → Process how?
- Handle → Handle in what way?
- Deal with → What action specifically?
- Address → What does addressing look like?
- Manage → Manage to what end?

### Output Verbs (need format)
- Summarize → In how many sentences?
- Describe → At what level of detail?
- Explain → For what audience?
- List → How many items?
- Outline → In what structure?

---

## Dangerous Assumptions

Phrases that assume Claude will infer correctly:

### Implicit Knowledge
- "As you know..." → Claude may not know
- "Obviously..." → May not be obvious to Claude
- "Of course..." → Don't assume
- "Naturally..." → State explicitly
- "You understand that..." → Verify understanding

### Implicit Instructions
- "Do the right thing" → Define "right"
- "Use common sense" → Not reliable
- "Be smart about it" → Not actionable
- "Figure it out" → Needs guidance
- "You know what to do" → State explicitly

### Implicit Constraints
- "Within reason" → Define bounds
- "Don't go overboard" → Specify limits
- "Keep it sensible" → Quantify
- "Use good judgment" → Provide criteria

---

## Agent-Specific Vague Terms

For Claude Code agent/skill prompts:

### Vague Trigger Descriptions
- "helps with" → specify trigger phrases
- "assists in" → specify trigger phrases
- "for working with" → list exact use cases
- "handles" → list specific actions

### Vague Scope
- "various tasks" → list specific tasks
- "multiple purposes" → define purposes
- "general assistance" → too broad
- "whatever is needed" → no bounds

---

## Detection Regex Patterns

For automated scanning:

```python
VAGUE_TERMS = [
    r'\b(good|bad|appropriate|relevant|proper)\b',
    r'\b(short|long|brief|detailed)\b(?!\s+\d)',  # Allow "short 50 words"
    r'\b(best|optimal|ideal)\b',
    r'\b(important|significant|reasonable)\b',
    r'\b(as needed|when necessary|if appropriate)\b',
    r'\b(try to|attempt to|do your best)\b',
    r'\b(thorough|comprehensive)\b(?!.*\b\d+\b)',  # Allow with numbers
]

FILLER_PHRASES = [
    r'please be sure to',
    r'i would like you to',
    r'it is important to note that',
    r'keep in mind that',
    r'don\'t forget to',
    r'in order to',
]

CONTRADICTIONS = [
    (r'thorough', r'concise'),
    (r'comprehensive', r'brief'),
    (r'detailed', r'short'),
    (r'creative', r'exact'),
]
```

---

## Replacement Guide

| Instead of | Use |
|------------|-----|
| "good summary" | "3-sentence summary" |
| "appropriate length" | "100-150 words" |
| "relevant information" | "information about X, Y, Z" |
| "be thorough" | "cover these 5 aspects" |
| "detailed analysis" | "analyze each of these 4 dimensions" |
| "short response" | "respond in 2-3 sentences" |
| "as needed" | "when X condition occurs" |
| "if appropriate" | "if the data shows Y" |
| "use good judgment" | "prefer option A when X, option B when Y" |

---

## Evaluation Checklist

When reviewing a prompt for vague terms:

1. [ ] No undefined quality descriptors
2. [ ] All quantities specified (word counts, item counts)
3. [ ] No contradictory instruction pairs
4. [ ] Analysis verbs have defined scope
5. [ ] Output verbs have format specification
6. [ ] No reliance on implicit knowledge
7. [ ] No "use good judgment" without criteria
8. [ ] Trigger descriptions (for agents) use specific phrases
