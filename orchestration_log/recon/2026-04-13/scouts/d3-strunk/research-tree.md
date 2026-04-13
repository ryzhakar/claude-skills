# Prose Quality Analysis: research-tree Skill
## Strunk's Elements of Style Evaluation

**Document:** `/Users/ryzhakar/pp/claude-skills/orchestration/skills/research-tree/SKILL.md`  
**Rules Applied:** R10 (active voice), R11 (positive form), R12 (concrete language), R13 (needless words), R15 (parallel construction), R18 (emphatic position)  
**Date:** 2026-04-13

---

## Critical & Severe

### R10: Active Voice (Severity: Severe)

**Line 63:** "For multi-session research (ecosystem surveys spanning days, ongoing market monitoring), the parent's session persistence protocol applies."

- **Issue:** Passive construction obscures agency
- **Rule:** Active voice is usually more direct and vigorous
- **Revision:** "For multi-session research (ecosystem surveys spanning days, ongoing market monitoring), apply the parent's session persistence protocol."
- **Effect:** Clearer imperative; reader knows what to do

**Line 88:** "Parse the primary research surface into a structured map. The orchestrator reads ONLY the summary statistics to plan the Tier 2 fan-out."

- **Issue:** Second sentence passive-ish with weak "reads ONLY"
- **Rule:** Active voice more direct
- **Revision:** "Parse the primary research surface into a structured map. Read ONLY the summary statistics to plan the Tier 2 fan-out."
- **Effect:** Consistent imperative voice throughout; maintains orchestrator's agency

**Line 154-155:** "No unresolved contradictions"

- **Issue:** Negative passive construction
- **Rule:** Positive form + active voice preferred
- **Revision:** "Resolve all contradictions"
- **Effect:** Positive, actionable statement

### R12: Concrete Language (Severity: Severe)

**Line 22:** "Research is not a procedure. It is a series of decisions about scope, depth, and course correction."

- **Issue:** "Series of decisions" remains somewhat abstract
- **Rule:** Prefer specific to general
- **Revision:** "Research is not a procedure. It is deciding where to look, how deep to go, and when to change course."
- **Effect:** More concrete actions; echoes line 18 effectively
- **Note:** This is borderline; the original is reasonably concrete, but the revision makes the decisions more tangible

---

## Moderate

### R11: Positive Form (Severity: Moderate)

**Line 30:** "When re-researching at higher fidelity, do NOT feed prior conclusions to new agents."

- **Issue:** Negative instruction where positive clearer
- **Rule:** Put statements in positive form
- **Revision:** "When re-researching at higher fidelity, give new agents raw context only (project facts, source URLs)."
- **Effect:** Tells reader what to do, not just what to avoid

**Line 34:** "If you're summarizing one agent's findings to another, you've broken the model."

- **Issue:** Negative consequence framing
- **Rule:** Positive form more definite
- **Revision:** "Point agents to files directly; never relay content."
- **Effect:** Clearer action; already partially present in line 34

**Line 59:** "Inherit ONLY facts — project context, source URLs, raw metadata. Never ratings, opinions, or recommendations from the first round."

- **Issue:** "Never" construction negates rather than asserts
- **Rule:** Positive form
- **Revision:** "Inherit ONLY facts: project context, source URLs, raw metadata. Exclude all ratings, opinions, and recommendations from the first round."
- **Effect:** Maintains prohibition but frames positively

**Line 107:** "Don't stop at the provided list."

- **Issue:** Negative instruction
- **Rule:** Positive form
- **Revision:** "Search beyond the provided list."
- **Effect:** Direct instruction

**Line 109:** "Don't trust claims without primary-source verification."

- **Issue:** Negative warning
- **Rule:** Positive form
- **Revision:** "Verify all claims against primary sources."
- **Effect:** Actionable directive

**Line 110:** "Don't conflate similarly-named entities."

- **Issue:** Negative prohibition
- **Rule:** Positive form
- **Revision:** "Distinguish similarly-named entities by exact names, URLs, maintainer identity, publication dates."
- **Effect:** Tells what to do with specific actions

**Line 111:** "Don't make strategic recommendations."

- **Issue:** Negative prohibition
- **Rule:** Positive form
- **Revision:** "Report findings with evidence. Leave strategic recommendations to the synthesis agent."
- **Effect:** Positive instruction already present in second sentence

**Line 139:** "Do not read full reports unless arbitration is needed."

- **Issue:** Negative instruction
- **Rule:** Positive form
- **Revision:** "Read full reports only when arbitration is needed."
- **Effect:** Frames as conditional action rather than prohibition

**Line 157:** "The stakeholder's specific question has a definitive, grounded answer"

- **Issue:** This is actually good positive form; no issue found

### R13: Needless Words (Severity: Moderate)

**Line 4-6:** "Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes, academic fields, regulatory environments, curated indices, or any domain requiring breadth-first exploration followed by depth-first verification."

- **Issue:** "or any domain requiring" is somewhat redundant after listing examples
- **Rule:** Omit needless words
- **Revision:** "Govern multi-agent research across any knowledge surface: technology ecosystems, market landscapes, academic fields, regulatory environments, curated indices — anything requiring breadth-first exploration followed by depth-first verification."
- **Effect:** Tighter construction; "anything" more economical than "any domain"

**Line 26:** "Which component library?" is a need. "Components" is a source category. They produce different research trees."

- **Issue:** "They produce" could be tighter
- **Rule:** Omit needless words
- **Revision:** "Which component library?" is a need. "Components" is a source category. Different trees result."
- **Effect:** More economical

**Line 42:** "Fetch, parse, count, categorize"

- **Issue:** No issue; economical list

**Line 46:** "The cheapest model that can reliably do the task is the right model."

- **Issue:** "that can reliably do the task" is verbose
- **Rule:** Omit needless words
- **Revision:** "Use the cheapest model that reliably completes the task."
- **Effect:** Active voice + economy

**Line 48-49:** "A second round at higher fidelity is warranted when:"

- **Issue:** "is warranted when" is passive and wordy
- **Rule:** Active voice + economy
- **Revision:** "Re-research at higher fidelity when:"
- **Effect:** Active, economical

**Line 65:** "Read the parent's session-persistence reference for the full ARRIVE/WORK/LEAVE lifecycle."

- **Issue:** No significant wordiness

**Line 83:** "For skip conditions and heuristics, see @references/tier-playbook.md — it covers tier definitions, completion gates, and agent count heuristics."

- **Issue:** "it covers" is weak filler
- **Rule:** Omit needless words
- **Revision:** "For skip conditions and heuristics, see @references/tier-playbook.md: tier definitions, completion gates, and agent count heuristics."
- **Effect:** Colon more economical than "it covers"

**Line 85:** "Before evaluating any external option, establish what the stakeholder actually has and needs."

- **Issue:** "actually" is filler
- **Rule:** Omit needless words
- **Revision:** "Before evaluating external options, establish what the stakeholder has and needs."
- **Effect:** Tighter

**Line 117:** "Every agent prompt specifies:"

- **Issue:** No wordiness

**Line 122:** "For prompt quality, apply general prompt engineering principles (clear role, specific instructions, constrained output)."

- **Issue:** "For prompt quality" could be more economical
- **Rule:** Omit needless words
- **Revision:** "Apply general prompt engineering principles: clear role, specific instructions, constrained output."
- **Effect:** Colon replaces wordy setup

**Line 154:** "Synthesis report exists"

- **Issue:** Could be more economical with parallel construction to other criteria
- **Revision:** "Synthesis complete" or "Final synthesis written"
- **Effect:** Matches active form of other criteria

### R15: Parallel Construction (Severity: Moderate)

**Line 26-27:** "Organize by need, not by source." ... "Your research should be organized by what the STAKEHOLDER needs to decide."

- **Issue:** First sentence uses "organize," second uses "should be organized" (passive)
- **Rule:** Parallel construction for related ideas
- **Revision:** "Organize by need, not by source." ... "Organize your research by what the STAKEHOLDER needs to decide."
- **Effect:** Consistent active voice maintains parallel

**Line 104-107:** Encourage section — three numbered items

- **Issue:** Item 1 and 2 are imperatives, but item 3 is "Report evidence, not conclusions"
- **Rule:** Parallel structure
- **Status:** Already parallel; all three are imperatives. No issue.

**Line 108-111:** Discourage section — three numbered items

- **Issue:** All three start with "Don't" — structurally parallel but could use positive form
- **Rule:** Parallel + positive form
- **Revision:** See R11 recommendations
- **Effect:** Maintains parallel while improving positivity

**Line 115-121:** Agent prompt structure — six numbered items

- **Issue:** Items 1-5 are noun phrases, item 6 is "The prime directive"
- **Rule:** Parallel construction
- **Status:** Actually parallel; all are things the prompt specifies. No issue.

**Line 135-141:** Per-Tier Execution — six numbered steps

- **Issue:** Steps mix imperatives ("Design," "Launch," "Mark," "Gate check," "Scan," "Launch")
- **Rule:** Parallel construction
- **Status:** All imperatives; structurally parallel. No issue.

**Line 146-150:** After Tier 2 decision bullets

- **Issue:** All four items follow pattern "Every X → Y agent"
- **Rule:** Parallel construction
- **Status:** Excellent parallel construction. No issue.

**Line 152-157:** Completion criteria — four bullets

- **Issue:** Mixed construction: "exists," "is backed," "No unresolved," "has a definitive"
- **Rule:** Parallel construction
- **Revision:** Make all completion criteria follow same pattern (e.g., all noun phrases or all complete sentences)
  - "Synthesis report complete"
  - "All high-confidence recommendations backed by verification reports"
  - "All contradictions resolved"
  - "Stakeholder's specific question answered definitively with grounded evidence"
- **Effect:** Consistent parallel structure; easier to scan

### R18: Emphatic Position (Severity: Moderate)

**Line 18:** "Govern multi-agent research across any knowledge surface. The orchestrator decides where to look, how deep to go, and when to change course. Agents do the looking."

- **Issue:** Final sentence ends weakly with "the looking"
- **Rule:** Emphatic words at the end
- **Revision:** "Govern multi-agent research across any knowledge surface. The orchestrator decides where to look, how deep to go, and when to change course. Agents execute."
- **Effect:** Stronger ending; "execute" more forceful than "do the looking"

**Line 22:** "Research is not a procedure. It is a series of decisions about scope, depth, and course correction. The tiers below are default gravity — not a script."

- **Issue:** Ends strongly with "not a script" — good contrast
- **Status:** Good use of emphatic position. No issue.

**Line 28:** "Verification depth must match claim consequence. An option that saves 10 lines of code needs a surface skim. An option that becomes a load-bearing dependency needs source-level verification. Match agent capability and effort to the stakes of the claim."

- **Issue:** Final sentence ends with "stakes of the claim" — reasonably emphatic
- **Status:** Acceptable. Could be stronger but serves its purpose.

**Line 34:** "If you're summarizing one agent's findings to another, you've broken the model."

- **Issue:** Ends strongly with "broken the model"
- **Status:** Good emphatic position. No issue.

**Line 46:** "Ten cheap agents in parallel beat two expensive agents in sequence: the synthesis step handles quality."

- **Issue:** Ends with "handles quality" — somewhat weak
- **Rule:** Emphatic position
- **Revision:** "Ten cheap agents in parallel beat two expensive agents in sequence: quality emerges in synthesis."
- **Effect:** "Synthesis" in emphatic position; more forceful

**Line 95:** "Produces the final deliverable answering the stakeholder's original question."

- **Issue:** Ends with "original question" — weak
- **Rule:** Emphatic position
- **Revision:** "Produces the final deliverable: a definitive answer to the stakeholder's original question."
- **Effect:** "Question" more emphatic after colon setup

---

## Minor & Stylistic

### R13: Needless Words (Severity: Minor)

**Line 12:** "The orchestrator governs agents that write durable reports to disk. It never does the research itself."

- **Issue:** "It never does the research itself" — "itself" potentially redundant
- **Rule:** Omit needless words
- **Revision:** "The orchestrator governs agents that write durable reports to disk. It never does the research."
- **Effect:** Slightly tighter; meaning unchanged
- **Note:** "Itself" adds emphasis, so this is genuinely minor

**Line 32:** "The orchestrator detects; agents act."

- **Issue:** No wordiness; excellent economy
- **Status:** Model of concision. No issue.

**Line 54:** "Second-round rules:"

- **Issue:** Colon implies list follows — good
- **Status:** No issue.

**Line 56-59:** Second-round rules bullets

- **Issue:** Fourth bullet has nested structure with long list
- **Rule:** Economy
- **Status:** Acceptable; the elaboration is necessary for clarity

**Line 121:** "For scope boundaries — what to research and explicitly what NOT to research"

- **Issue:** "explicitly" is potentially redundant given "what NOT to"
- **Rule:** Omit needless words
- **Revision:** "For scope boundaries — what to research and what to exclude"
- **Effect:** More economical

### R15: Parallel Construction (Severity: Minor)

**Line 69-80:** Tier system diagram

- **Issue:** Tier descriptions vary in construction
  - "GROUND TRUTH — what does the stakeholder actually have and need?"
  - "INDEX — parse the primary source into a structured map"
  - "SURVEY — fan out by need-category, assess candidates"
  - "VERIFY — deep-dive promising candidates against primary sources"
  - "RESOLVE — detect and resolve contradictions across reports"
  - "SYNTHESIZE — one capable agent reads ALL reports, writes final verdict"
- **Rule:** Parallel construction
- **Analysis:** Tiers 0-1 are questions/imperatives, Tiers 2-5 are imperative verb phrases, Tier 5 adds agent specification. Mixed but acceptable given differing nature of each tier.
- **Status:** Minor issue; perfect parallel might sacrifice clarity

**Line 54-59:** Second-round rules — four bullets

- **Issue:** 
  - "**Separate directory** — agents don't see first-round reports"
  - "**Higher-capability models** for verification"
  - "**Need-driven organization** (not source-driven)"
  - "**Inherit ONLY facts** — project context, source URLs, raw metadata. Never ratings..."
- **Rule:** Parallel construction
- **Analysis:** First bullet is sentence, second is fragment, third is noun phrase, fourth is imperative
- **Revision:** Standardize to fragments or imperatives:
  - "**Separate directory** — prevents agents from seeing first-round reports"
  - "**Higher-capability models** — use for verification tasks"
  - "**Need-driven organization** — not source-driven categories"
  - "**Factual inheritance only** — project context, source URLs, raw metadata (exclude ratings, opinions, recommendations)"
- **Effect:** More consistent parallel structure

### R18: Emphatic Position (Severity: Minor)

**Line 83:** "For skip conditions and heuristics, see @references/tier-playbook.md — it covers tier definitions, completion gates, and agent count heuristics."

- **Issue:** Ends with "agent count heuristics" — reasonably emphatic
- **Status:** Acceptable; the list concludes with meaningful content

**Line 125:** "For domain-adaptable skeletons, see @references/agent-templates.md — it provides prompt templates for every agent type."

- **Issue:** Ends with "every agent type" — emphatic enough
- **Status:** Acceptable

---

## Summary

### Overall Assessment

The research-tree skill demonstrates **strong prose quality** with sophisticated use of imperatives, concrete language, and parallel construction. The document effectively uses Strunk's principles for technical instruction writing. Primary opportunities for improvement:

1. **Active Voice (R10):** Several passive constructions could be more direct (moderate severity)
2. **Positive Form (R11):** Multiple "don't" and "never" instructions could be reframed positively (moderate severity)
3. **Parallel Construction (R15):** Completion criteria and second-round rules lists have minor inconsistencies (minor severity)
4. **Needless Words (R13):** Scattered opportunities to tighten constructions (mostly minor)
5. **Emphatic Position (R18):** Few sentences end weakly (minor severity)

### Strengths

- **Concrete Language (R12):** Excellent throughout — specific examples, definite assertions, vivid comparisons
- **Economy (R13):** Generally tight prose; little padding
- **Parallel Construction (R15):** Most lists are well-structured (Encourage/Discourage, Agent Design, Per-Tier Execution)
- **Emphatic Position (R18):** Many sentences end strongly ("not a script," "broken the model")

### Quantitative Summary

- **Critical/Severe findings:** 4 (R10: 3, R12: 1)
- **Moderate findings:** 18 (R11: 8, R13: 6, R15: 2, R18: 2)
- **Minor/Stylistic findings:** 6 (R13: 2, R15: 2, R18: 2)

### Recommended Priority

1. Convert passive constructions to active voice (R10) — improves directness and vigor
2. Reframe negative instructions positively (R11) — clearer, more actionable
3. Standardize parallel construction in completion criteria (R15) — easier to scan
4. Tighten wordy phrases (R13) — respects reader's time

The document is already well-written. These revisions would elevate it from very good to excellent by Strunk's standards.
