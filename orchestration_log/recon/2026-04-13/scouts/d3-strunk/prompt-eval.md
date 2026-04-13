# Strunk Analysis: prompt-eval Skill

## Critical & Severe

### 1. Passive obscures agent (R10 - Severe)
**Location**: Line 16, Purpose section  
**Text**: "Evaluate any Claude system prompt to identify:"  
**Issue**: Opens with passive imperative that obscures the agent. While imperatives are technically active voice grammatically, this construction creates distance between reader and action.  
**Revision**: "Use this skill to identify:" or "This skill identifies:"  
**Justification**: R10 demands active voice as default. While imperatives can be acceptable in instructions, the tone here suggests agent ambiguity rather than command clarity.

### 2. Abstract construction weakens claim (R12 - Severe)
**Location**: Line 23, Evaluation Workflow  
**Text**: "Produce a structured evaluation report with severity-ranked findings and actionable recommendations."  
**Issue**: Abstract nouns ("findings", "recommendations") without concrete examples of what these look like.  
**Revision**: "Produce a report that ranks each violation by severity (Critical/Severe/Moderate) and specifies concrete fixes."  
**Justification**: R12 demands concrete language. "Findings" and "recommendations" are vague containers; reader needs specific examples of what these entail.

### 3. Vague language in critical instruction (R12 - Severe)
**Location**: Line 29, Step 1  
**Text**: "Read the prompt to evaluate (user provides path or content)"  
**Issue**: Parenthetical is vague about mechanism. How does user provide? What format?  
**Revision**: "Read the prompt file (user gives you the file path or pastes the prompt text)"  
**Justification**: R12 requires definite language. "Provides" is abstract; "gives you the file path or pastes" is concrete.

### 4. Needless words dilute instruction (R13 - Severe)
**Location**: Line 38, Step 2  
**Text**: "Reference @../../references/evaluation-criteria.md — it covers applicability rules for all evaluation categories."  
**Issue**: "it covers" is needless padding after em-dash which already signals explanation.  
**Revision**: "Reference @../../references/evaluation-criteria.md — applicability rules for all evaluation categories."  
**Justification**: R13 demands omitting needless words. The em-dash already indicates the file's contents; "it covers" adds no information.

### 5. Passive construction obscures actor (R10 - Severe)
**Location**: Lines 59-60, Step 3  
**Text**: "For violations, record:"  
**Issue**: Passive imperative. Who records? The evaluator (Claude), but this is implicit.  
**Revision**: "When you find violations, record:" or "Record each violation:"  
**Justification**: R10 requires active voice. Making the agent explicit improves clarity.

### 6. Weak negative construction (R11 - Severe)
**Location**: Line 145, Quick Evaluation Mode  
**Text**: "If any critical item fails, flag for full evaluation."  
**Issue**: "If any... fails" is negative framing of a positive condition.  
**Revision**: "When a critical item fails, conduct full evaluation."  
**Justification**: R11 demands positive form. "If any" creates double processing (any = at least one, fails = negative).

## Moderate

### 7. Needless phrase repetition (R13 - Moderate)
**Location**: Lines 161-164, Reference Files  
**Text**: Each reference line ends with "— it covers [description]"  
**Issue**: Formulaic repetition of "it covers" four times in succession.  
**Revision**: Use parallel construction without the repeated "it covers": "- @../../references/evaluation-criteria.md — complete criteria tables with check methods"  
**Justification**: R13 forbids needless words. The pattern "file — description" is sufficient; "it covers" adds nothing after the first instance.

### 8. Non-parallel list items (R15 - Moderate)
**Location**: Lines 17-21, Purpose section  
**Text**: List mixes noun phrases ("Structural issues", "Clarity... problems", "Missing safety guardrails", "Tool specification issues") with one different form ("Agent-specific problems (for Claude Code agents/skills)")  
**Issue**: Last item includes explanatory parenthetical; others don't. Inconsistent structure.  
**Revision**: Either add parallel parentheticals to all, or remove from last: "Agent-specific anti-patterns"  
**Justification**: R15 requires parallel construction for coordinate ideas. All five items are types of issues to identify; they should use the same grammatical form.

### 9. Buried emphatic point (R18 - Moderate)
**Location**: Line 23  
**Text**: "Produce a structured evaluation report with severity-ranked findings and actionable recommendations."  
**Issue**: Key outcome "report" appears early; sentence ends weakly with generic "recommendations."  
**Revision**: "Identify violations by severity, then produce actionable recommendations in a structured report."  
**Justification**: R18 places emphatic words at end. "Report" is the deliverable; it should be emphasized, not "recommendations."

### 10. Weak final position (R18 - Moderate)
**Location**: Line 168, Example Evaluation  
**Text**: "See `examples/sample-evaluation.md` for a complete evaluation report example."  
**Issue**: Sentence ends with redundant "example" (already said "see... for").  
**Revision**: "See `examples/sample-evaluation.md` for a complete evaluation report."  
**Justification**: R18 demands emphatic final position. "Example" is weak and redundant after "see... for"; "report" is stronger.

### 11. Vague pronoun reference (R12 - Moderate)
**Location**: Line 34, Step 1.3  
**Text**: "Note applicable categories (see Step 2)"  
**Issue**: "Note" is vague. Note where? Note how? For what purpose?  
**Revision**: "List which categories apply to this prompt (see Step 2)"  
**Justification**: R12 requires concrete language. "Note" could mean mentally remember, write down, or something else. "List" is specific.

### 12. Abstract measurement language (R12 - Moderate)
**Location**: Lines 67-74, Step 4 calculation  
**Text**: "Score = (passed / applicable) × 100"  
**Issue**: While mathematically precise, "passed" and "applicable" are abstract. No concrete example.  
**Revision**: Add concrete example: "Example: If 15 of 20 applicable criteria pass, score = (15/20) × 100 = 75%"  
**Justification**: R12 demands concrete examples alongside abstract formulas. The formula alone forces reader to imagine application.

### 13. Needless phrase (R13 - Moderate)
**Location**: Line 133, Quick Evaluation Mode  
**Text**: "For rapid assessment, check critical items only:"  
**Issue**: "For rapid assessment" is needless given the header "Quick Evaluation Mode" already establishes speed purpose.  
**Revision**: "Check critical items only:"  
**Justification**: R13 forbids needless words. The section header already signals this is the fast method.

### 14. Weak negative phrasing (R11 - Moderate)
**Location**: Line 137, item 2  
**Text**: "No vague terms? (CLR-2)"  
**Issue**: Negative question construction is indirect.  
**Revision**: "Uses concrete terms? (CLR-2)" or "Language is concrete? (CLR-2)"  
**Justification**: R11 demands positive form. "No vague terms" requires reader to negate a negative.

### 15. Weak negatives in checklist (R11 - Moderate)
**Location**: Lines 138, 140, 141  
**Text**: "No contradictions?", "No implicit constraints?", "No unsafe data access?"  
**Issue**: Negative questions throughout checklist.  
**Revision**: "Free of contradictions?", "Constraints explicit?", "Data access safe?"  
**Justification**: R11 prefers positive form. While questions allow some negative formulation, affirmative constructions are clearer.

## Minor & Stylistic

### 16. Subject-predicate separation (R16 - Minor)
**Location**: Lines 36-37, Step 2  
**Text**: "Reference @../../references/evaluation-criteria.md — it covers applicability rules for all evaluation categories."  
**Issue**: Not strictly a violation (this is an imperative), but the em-dash creates distance between command and its object.  
**Revision**: Already covered by finding #4 above.  
**Justification**: R16 prefers related words together, though em-dash usage here is defensible for emphasis.

### 17. Slightly weak opening (R18 - Minor)
**Location**: Line 10, top-level heading  
**Text**: "# System Prompt Evaluation"  
**Issue**: Generic title doesn't emphasize distinctive value.  
**Revision**: "# Systematic Claude Prompt Evaluation" or "# Prompt Quality Assessment Against Anthropic Standards"  
**Justification**: R18 values emphatic positioning. "Evaluation" is generic; the distinctive element (systematic/Anthropic-based) should be prominent.

### 18. Comma splice potential (R5 - Minor)
**Location**: Line 53, Step 3.1  
**Text**: "Review criteria in @../../references/evaluation-criteria.md — it covers complete criteria tables with check methods"  
**Issue**: While em-dash technically avoids comma splice, the second clause is independent and could stand alone.  
**Revision**: "Review criteria in @../../references/evaluation-criteria.md (complete criteria tables with check methods)"  
**Justification**: R5 forbids joining independent clauses with comma. Em-dash is acceptable but parenthetical might be cleaner.

### 19. Inconsistent reference format (R15 - Minor)
**Location**: Lines 38, 61, 62, 63, 161-164  
**Text**: References use two formats: "@path — it covers description" vs "@path — description"  
**Issue**: Parallel items (reference links) should use parallel structure throughout.  
**Revision**: Choose one format and apply consistently. Prefer: "@path — description" (shorter, per R13)  
**Justification**: R15 requires parallel construction for similar items. All references should follow identical pattern.

### 20. Slightly wordy score interpretation (R13 - Minor)
**Location**: Line 148, Score Interpretation header  
**Text**: "## Score Interpretation"  
**Issue**: Not actually wordy, but the table below is well-structured. No violation, just noting clarity.  
**Justification**: Section is clear; this is not a true finding.

### 21. Filler phrase in Step 4 (R13 - Minor)
**Location**: Line 66, Step 4  
**Text**: "### Step 4: Calculate Score"  
**Issue**: "Calculate Score" is fine, but could be more active.  
**Revision**: "### Step 4: Score the Prompt" or "### Step 4: Calculate Quality Score"  
**Justification**: R13 and R10 prefer active constructions. "Calculate Score" is acceptable but "Score the prompt" is slightly more direct.

### 22. Hedge word weakens claim (R11 - Minor)
**Location**: Line 172  
**Text**: "Evaluation is against Anthropic's official guidance, not subjective preference"  
**Issue**: Not a violation, actually. This is a positive assertion. No finding.  
**Justification**: False alarm; sentence structure is sound.

### 23. Slightly buried subject (R18 - Minor)
**Location**: Line 43, Conditionally apply section  
**Text**: "- TOOLS: If tools/functions defined"  
**Issue**: Conditional clause comes after category name, burying the condition.  
**Revision**: "- TOOLS: Apply if tools/functions are defined" or "- TOOLS (when tools/functions defined)"  
**Justification**: R18 suggests emphatic elements at end, but this list format is defensible as-is.

### 24. Expository phrase (R13 - Stylistic)
**Location**: Line 175, final sentence  
**Text**: "Use the prompt-optimize skill to fix identified issues"  
**Issue**: "identified" is mildly redundant (issues just mentioned are obviously identified).  
**Revision**: "Use the prompt-optimize skill to fix these issues"  
**Justification**: R13 forbids needless words. "Identified" adds little; "these" suffices with context.

### 25. List article inconsistency (R15 - Stylistic)
**Location**: Lines 40-41  
**Text**: "**Always apply**: STRUCTURE, CLARITY, CONSTRAINTS, SAFETY, OUTPUT" (no articles)  
vs.  
Lines 43-48 with full explanatory phrases  
**Issue**: First list uses bare terms; second uses phrases. Style differs.  
**Revision**: Maintain parallel structure: either all bare category names, or all with brief descriptions.  
**Justification**: R15 demands parallel construction in lists. Category presentation should be consistent.

## Summary

**Total findings**: 25 (6 Severe, 10 Moderate, 9 Minor/Stylistic)

**Most pervasive issue**: **Needless words (R13)** — Multiple instances of padding phrases ("it covers", "for rapid assessment", repeated reference formulas) that dilute the prose without adding meaning. The skill frontmatter itself advocates for "structured" and "systematic" evaluation, but the instruction text doesn't model the economy it implicitly values.

**Secondary pattern**: **Weak negative constructions (R11)** — Quick evaluation checklist relies heavily on negative questions ("No vague terms?", "No contradictions?") when positive formulations would be clearer and more direct.

**Overall assessment**: The skill is functionally clear and well-organized, but prose suffers from institutional/technical writing habits: passive constructions, abstract language, formulaic repetition, and hedge phrases. Most violations are Moderate severity, meaning the text is comprehensible but lacks the vigor and directness that Strunk advocates. The structure (numbered steps, clear sections, reference links) is excellent; the sentence-level prose needs tightening.

**Architectural strength**: The skill does excel at parallel construction in its template sections (Output Format, Score Interpretation table) and maintains good paragraph unity (Rule 8). The workflow breakdown is logical and each step has clear scope.

**Recommended focus**: Apply R13 (omit needless words) and R10 (active voice) systematically. The diff between current state and revised state would be substantial but straightforward — primarily removing filler and converting passive constructions to active imperatives.
