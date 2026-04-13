# Strunk Analysis: agentic-delegation

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 69: "There is exactly ZERO reasons to do something in orchestrator context"**
- **Problem:** Perfunctory "there is" construction obscures direct statement
- **Revision:** "Orchestrator context requires exactly zero work."
- **Effect:** Active construction, more forceful

**Line 81: "Context consumed by 'quickly checking' is permanently lost."**
- **Problem:** Passive voice obscures agent and weakens force
- **Revision:** "Quickly checking permanently consumes context."
- **Effect:** Active verb shows direct causation

**Line 232: "Give each agent the MINIMUM context needed to complete its task."**
- **Note:** Imperative (active) - CORRECT

**Line 276: "Cost: zero orchestrator context. Information: preserved at full fidelity."**
- **Problem:** Headword fragments with implied passive ("is preserved")
- **Revision:** "Cost: zero orchestrator context. Information: full fidelity remains."
- **Effect:** Active verb completes the thought

### R12 (Concrete Language) - Severe

**Line 53: "What 'Negligible Cost' Actually Means"**
- **Problem:** Abstract section promises concrete examples (delivers them well in body)
- **Note:** Body DOES deliver concrete examples; header is acceptable as it frames what follows

**Line 162: "Sonnet output insufficient? (rare — usually means the task needs decomposition, not a better model)"**
- **Problem:** "Insufficient" is vague; what specific failure signals?
- **Revision:** "Sonnet output shows contradictions, shallow reasoning, or missing key connections? (rare — usually means the task needs decomposition, not a better model)"
- **Effect:** Specific failure modes replace abstract "insufficient"

**Line 225: "Every extra file, every extra paragraph of background, is: Potential for distraction"**
- **Problem:** "Potential for" abstracts the consequence
- **Revision:** "Every extra file, every extra paragraph of background: distracts agents, invites misinterpretation, wastes context window."
- **Effect:** Concrete verbs replace abstract nouns

### R13 (Needless Words) - Moderate

**Line 232: "Give each agent the MINIMUM context needed to complete its task."**
- **Problem:** "needed to complete its task" is implied by "minimum context"
- **Revision:** "Give each agent minimum context."
- **Effect:** 6 words → 5 words; "task" is already established

**Line 338: "launch all independent agents in a single message"**
- **Note:** "independent" might be needless (implied by parallel fan-out), but it serves clarity by contrasting with sequential pipeline. ACCEPTABLE.

**Line 426: "If failures: delegate investigation (see above)"**
- **Problem:** "(see above)" adds no value; Investigation archetype appears at line 405
- **Revision:** "If failures: delegate investigation"
- **Effect:** Removes needless parenthetical

**Line 463: "The ARRIVE/WORK/LEAVE lifecycle protocol maintains living reference documents (what's true now), frozen session history (what happened then), and disposable recon data (raw scouting)."**
- **Problem:** Parentheticals are explanatory glosses, not needless. CORRECT.

**Line 486: "Re-launch, don't debug."**
- **Note:** Perfect economy. EXEMPLARY.

### R11 (Positive Form) - Moderate

**Line 69: "There is exactly ZERO reasons to do something in orchestrator context: any work you see as miniscule on the planning phase can baloon-up unexpectedly."**
- **Problem:** Double negative ("zero reasons" + list of rationalizations contradicting negative)
- **Revision:** "All work belongs in agent context: any task that seems minuscule during planning can balloon unexpectedly."
- **Effect:** Positive assertion replaces negative evasion

**Line 311: "No agent needs another's output, or just the same inputs?"**
- **Problem:** Negative question format forces reader to negate
- **Revision:** "Does B truly need A's output, or can B work from the same inputs?"
- **Effect:** Positive question structure

**Line 429: "Never run long validation procedures in orchestrator context."**
- **Note:** "Never" is strong negative word (Strunk approves these per R11). ACCEPTABLE.

**Line 494: "Never dispatch two parallel agents that write to the same file."**
- **Note:** "Never" + concrete prohibition = strong negative (acceptable per Strunk). CORRECT.

## Moderate

### R15 (Parallel Construction) - Moderate

**Line 34-38: Table comparing "Traditional thinking" vs "Correct thinking"**
- **Problem:** Left column varies structure: some questions ("Is this worth...?"), some statements ("That's too small...")
- **Effect on readability:** Minor; the contrasts are still clear
- **Suggested revision:** Make all left-column entries questions OR all statements
  - "Should I delegate this?" / "Why would I do this myself?"
  - "Is it too small to delegate?" / "Are small tasks cheapest to delegate?"
- **Severity:** Moderate (table comprehension slightly reduced)

**Line 92-93: "Haiku agents gather, extract, count, list, and report. They never decide, judge, evaluate, or recommend."**
- **Note:** Perfect parallel construction in both sentences. EXEMPLARY.

**Line 104-110: "Fails at:" list**
- **Note:** All items are gerund phrases (noun phrases). Perfect parallelism. CORRECT.

**Line 473-477: Numbered principles**
- **Problem:** Principle 1 is descriptive statement; others are imperatives
  - 1: "Your context is expensive. Agent calls are cheap." (statement)
  - 2: "Decompose aggressively." (imperative)
  - 3: "Haiku is the default." (statement)
- **Revision:** Make all imperatives:
  - 1: "Treat context as expensive. Treat agent calls as cheap."
  - 2: "Decompose aggressively."
  - 3: "Default to haiku."
- **Effect:** Consistent command voice throughout

### R18 (Emphatic Position) - Moderate

**Line 18: "Decompose. Delegate. Assemble. Your context window is the most expensive resource in the system."**
- **Note:** Ends strongly with key point. CORRECT.

**Line 31-32: "This means the decision calculus is inverted:"**
- **Problem:** Ends weakly with passive "is inverted"
- **Revision:** "This inverts the decision calculus:"
- **Effect:** Active verb in emphatic position

**Line 49: "When you have 8 things to check, don't check them — launch 8 agents."**
- **Note:** Ends with the action directive. CORRECT.

**Line 164: "The cost of routinely using sonnet for haiku work adds up."**
- **Problem:** Ends weakly with vague "adds up"
- **Revision:** "Routinely using sonnet for haiku work accumulates unnecessary cost."
- **Effect:** Concrete noun "cost" in emphatic position

**Line 218: "This keeps the orchestrator in control of cost, parallelism, and quality governance."**
- **Note:** Ends with strong triad. CORRECT.

**Line 359: "Detect bad output through completion summaries (extraordinary claims, contradictions, suspiciously short reports)."**
- **Problem:** Ends with parenthetical examples rather than main point
- **Revision:** "Use completion summaries to detect bad output: extraordinary claims, contradictions, suspiciously short reports."
- **Effect:** Colon structure keeps examples subordinate; main point emphasized

## Minor & Stylistic

### R10 (Active Voice) - Minor instances

**Line 141: "Your context is the most expensive resource."**
- **Note:** "Is" is linking verb, not passive. CORRECT.

**Line 273: "Agent A writes report → Orchestrator reads report → Orchestrator summarizes in Agent B's prompt"**
- **Note:** Active verbs throughout. EXEMPLARY diagram.

### R13 (Needless Words) - Minor instances

**Line 103: "Any task requiring judgment starts at sonnet."**
- **Note:** No waste. CORRECT.

**Line 205: "The iteration rule: Agents never launch other agents."**
- **Note:** Economical. CORRECT.

### R12 (Concrete Language) - Minor

**Line 457: "15 speculative haiku agents exploring different angles cost less than reading one comprehensive document yourself."**
- **Note:** Specific numbers, concrete comparison. EXEMPLARY.

## Summary

### Severity Distribution
- **Severe:** 7 findings (R10: 4, R12: 3)
- **Moderate:** 11 findings (R13: 3, R11: 4, R15: 1, R18: 3)
- **Minor:** 4 observations (exemplary cases noted)

### Pattern Analysis

**Strengths:**
- Extensive use of concrete examples (lines 42-48, 54-65, 94-110)
- Strong imperative voice in governing principles
- Parallel construction in many lists (lines 92-93, 104-110)
- Emphatic positioning in key directives (lines 18, 49, 486)

**Recurring weaknesses:**
1. **Perfunctory constructions** (R10): "There is/are" patterns appear multiple times
2. **Passive voice** (R10): Appears in explanatory sections where active would strengthen
3. **Abstract consequences** (R12): "Potential for X" instead of concrete verbs
4. **Negative formulations** (R11): Some guidance states what NOT to do without clear positive alternative
5. **Non-parallel principle lists** (R15): Mixed statement/imperative structures in summary sections

### Recommended Revision Priority

1. **High priority (Severe):** Convert perfunctory "there is" constructions to active voice (R10)
2. **High priority (Severe):** Replace abstract nouns with concrete verbs in consequence lists (R12)
3. **Medium priority (Moderate):** Reframe negative prohibitions as positive directives (R11)
4. **Medium priority (Moderate):** Align parallel structure in governing principles list (R15)
5. **Low priority (Minor):** Polish emphatic positioning in summary statements (R18)

### Overall Assessment

The document demonstrates **strong command of concrete, specific language** (R12) and **effective use of active voice in directives** (R10). The prose is generally vigorous and clear. Primary weaknesses appear in:
- Explanatory/transitional sections where passive and perfunctory constructions dilute force
- Summary sections where parallel structure breaks down
- Prohibitions that rely on negative form without stating positive alternative

The document would benefit from a systematic pass to:
1. Convert all "there is/are" to active constructions
2. Recast abstract consequences as concrete verbs
3. Ensure governing principles maintain consistent imperative voice
4. Place emphatic words (cost, context, delegation) in final position consistently
