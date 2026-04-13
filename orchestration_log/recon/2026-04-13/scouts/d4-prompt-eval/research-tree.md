# Prompt Evaluation: research-tree

**Unit Type:** Skill (Claude Code Agent)
**Evaluated:** 2026-04-13
**File:** /Users/ryzhakar/pp/claude-skills/orchestration/skills/research-tree/SKILL.md

---

## Overall Score: 82/100 (Good)

Functional with well-structured tiers and clear orchestration protocol. Stronger workflow definition than agentic-delegation but still has vague terms and missing output format.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓
- OUTPUT ✓
- EXAMPLES ✗ (references examples but doesn't include them inline)
- TOOLS ✗ (mentions tools but doesn't define them)
- REASONING ✗ (not a reasoning-focused task)
- DATA_SEPARATION ✗ (doesn't handle variable user data)
- AGENT_SPECIFIC ✓

---

## Critical Issues (MUST/MUST_NOT violations)

### MUST Violations

1. **AGT-6: Workflow present but buried**
   - "Orchestration Protocol" (lines 131-157) provides workflow BUT it's positioned after "The Tier System" and "Agent Design"
   - The workflow exists but ordering is suboptimal - should be earlier
   - Mitigated violation: workflow exists but placement reduces effectiveness
   - Impact: -1.5 points (partial credit - workflow exists but misplaced)

### MUST_NOT Violations

1. **CLR-2: Contains undefined vague terms**
   - "promising" (line 148: "Every candidate rated **promising**")
   - "relevance threshold" (line 149: "above relevance threshold")
   - "high-confidence recommendation" (line 153)
   - "extraordinary claim" (lines 110, 150)
   - "stakes" (line 28: "Match agent capability and effort to the stakes")
   - "sufficient" (line 143: "when coverage is insufficient")
   - Impact: -3 points

2. **AGT-9: References external files without progressive disclosure**
   - Line 84: "@references/tier-playbook.md"
   - Line 125: "@references/agent-templates.md"
   - Line 207: "@references/anti-patterns.md"
   - Lines 215-219: Four more @references
   - File is 220 lines - under limit BUT relies on external files that should be progressive disclosure mechanism
   - If external files don't exist, skill is incomplete
   - Impact: -3 points

---

## Warnings (SHOULD violations)

1. **STR-5: Ordering suboptimal**
   - Current: Philosophy → Tier System → Agent Design → Orchestration Protocol → Directory Structure → Domain Adaptation → Anti-Patterns
   - Recommended: Role → Context → Tier System (task structure) → Orchestration Protocol (how to execute) → Agent Design → Output (directory structure) → Error Handling
   - Workflow should come before detailed agent design
   - Lost: +1 point

2. **CLR-4: Success criteria buried**
   - "Completion Criteria" exists (lines 152-157) but under "Orchestration Protocol" subsection
   - Should be more prominent
   - Partial credit: criteria exist
   - Lost: +0.5 points

3. **OUT-1: Output format implicit rather than explicit**
   - "Directory Structure" (lines 159-192) shows WHERE outputs go but not WHAT format each report uses
   - References @references/report-formats.md instead of showing templates
   - Lost: +1 point

4. **OUT-6: Doesn't state what to exclude**
   - No "skip preamble", "do not include disclaimers" guidance
   - Lost: +1 point

5. **AGT-8: Output format scattered**
   - Directory structure shown but report templates missing
   - Lost: +1 point

6. **STR-2: Context could be more explicit**
   - "Philosophy" section provides context but doesn't state "You are governing a multi-tier research operation where..."
   - Lost: +0.5 points

---

## Anti-Patterns Detected

1. **AP-CLR-02: Undefined qualifiers** (High severity)
   - "promising", "relevance threshold", "high-confidence", "extraordinary claim", "stakes", "sufficient"
   - Maps to CLR-2 violation

2. **AP-CON-04: Scattered constraints** (Low severity)
   - Constraints appear in multiple sections: "Five Truths", "Model Selection", "When to Re-Research"
   - Should be consolidated

3. **AP-OUT-01: Undefined format** (High severity)
   - Directory structure shown but report templates delegated to external reference
   - No inline examples of what a survey report or verification report looks like

4. **AP-AGT-05: Bloated skill (mild)** (Medium severity)
   - 220 lines is under 500 BUT the skill relies on 7 external reference files
   - If those are counted, total documentation exceeds 500 lines
   - Progressive disclosure intended but external files aren't confirmed to exist

---

## Strengths

1. **Excellent tier system design**
   - 6 tiers (0-5) with clear purposes (lines 67-96)
   - Tier dependencies shown with ASCII diagram
   - Ground truth tier (Tier 0) prevents premature external research
   - Completion gates for each tier mentioned (reference to tier-playbook)

2. **Strong philosophical framework**
   - "Five Truths" (lines 24-35) are concrete and actionable
   - "Organize by need, not by source" (line 22) directly addresses common failure mode
   - "Fresh eyes beat inherited conclusions" (line 30) prevents bias propagation

3. **Clear orchestration protocol**
   - Setup → Per-Tier Execution → Between-Tier Decisions → Completion (lines 131-157)
   - Numbered steps within each phase
   - Task tracking mentioned (line 133: "Use task tracking")

4. **Good agent design section**
   - Prime Directive (lines 99-112) with encourage/discourage lists
   - Prompt structure (lines 114-121) specifies 6 required elements
   - Domain-adaptable

5. **Domain adaptation guidance**
   - Table showing how to adapt tier system to 5 different domains (lines 194-204)
   - Software ecosystem, market landscape, academic field, regulatory environment, API ecosystem
   - Shows primary source, registry, and verification method for each

6. **Session persistence integration**
   - References parent's session persistence protocol (lines 61-66)
   - Explains how reference/history/recon layers apply to research

7. **Anti-pattern awareness**
   - Calls out "The three most damaging" (lines 206-212)
   - Context Relay, Documentation Trust, Premature Synthesis
   - Each with fix

8. **Good frontmatter**
   - Clear triggers
   - Scope definition (any knowledge surface)
   - Core thesis about orchestrator role

---

## Recommendations

### High Priority (Fix MUST/MUST_NOT violations)

1. **Eliminate vague terms**
   - Replace "promising" → "rated PROMISING in survey report (compatibility: YES, activity: recent, constraints: met)"
   - Replace "relevance threshold" → "relevance score ≥ 7/10 OR mentioned in 2+ breadth-expansion reports"
   - Replace "high-confidence recommendation" → "recommendation backed by Tier 3 verification report with primary source citations"
   - Replace "extraordinary claim" → "claim contradicting 2+ other reports OR asserting capability without primary source"
   - Replace "stakes" → "consequence tier: LOW (cosmetic), MEDIUM (productivity), HIGH (load-bearing dependency)"
   - Replace "sufficient coverage" → "coverage complete: all need-categories have survey reports, all PROMISING candidates verified"

2. **Confirm or create external references**
   - If @references/*.md files exist, this is good progressive disclosure
   - If they don't exist, either:
     - Create them (recommended)
     - Or inline critical content (tier definitions, report templates)
   - Test: can the skill be executed successfully with only SKILL.md? If no, progressive disclosure is broken

3. **Move workflow earlier**
   - Reorder sections:
     ```
     1. Philosophy (context)
     2. The Tier System (task structure)
     3. Orchestration Protocol (workflow) ← MOVE UP
     4. Agent Design
     5. Directory Structure (output format)
     6. Domain Adaptation
     7. Anti-Patterns
     ```

### Medium Priority (Improve SHOULD compliance)

4. **Add inline report format examples**
   - Even if @references/report-formats.md exists, include 1-2 examples inline
   ```markdown
   ## Report Format Example
   
   <example>
   Survey report template:
   
   # {Need Category} Survey
   
   ## Candidates Evaluated
   
   ### {Candidate Name}
   - **Source:** {URL}
   - **Compatibility:** YES/NO/PARTIAL
   - **Activity:** {last commit date}
   - **Constraints:** {met/failed}
   - **Verdict:** PROMISING / SKIP / VERIFY_SEPARATELY
   - **Evidence:** {quoted from primary source}
   </example>
   ```

5. **Make completion criteria more prominent**
   - Move "Completion Criteria" out of "Orchestration Protocol" subsection into its own section
   - Place immediately after "Orchestration Protocol"

6. **Add output exclusions**
   ```markdown
   ## Output Guidelines
   
   For all reports:
   - Skip preambles and sign-offs
   - No "In conclusion" or "To summarize"
   - Lead with verdict, follow with evidence
   - Quote sources verbatim, don't paraphrase
   ```

7. **Consolidate constraints**
   - Create a "Constraints & Boundaries" section that consolidates:
     - What the orchestrator does vs. delegates
     - When to skip tiers
     - When to re-research
     - What NOT to do (from anti-patterns)

### Low Priority (Polish)

8. **Quantify "Between-Tier Decisions"**
   - Line 145: "After Tier 2, decide what enters Tier 3"
   - Add: "Heuristic: verify top 5-10 candidates OR all candidates rated PROMISING, whichever is fewer"

9. **Add task decomposition example**
   - Show a concrete example: "User asks 'What component library should I use?' → decompose into need-categories: state management, UI primitives, form handling, data fetching"

10. **Clarify multi-round directory structure**
    - Lines 177-192 show two structures (single-round, multi-round)
    - Add a decision tree: when to use v2 directory vs. single-round

---

## Scores by Category

| Category | Score | Notes |
|----------|-------|-------|
| STRUCTURE | 5/7 | Has role (implicit), good context, clear structure markers, has task definition (orchestration protocol), ordering suboptimal, no instruction-data mixing |
| CLARITY | 4/7 | Vague terms violation, no contradictions, has success criteria (buried), good numbered steps |
| CONSTRAINTS | 5/6 | Scope clear (tier boundaries), constraints scattered, good rationale in "Five Truths" |
| SAFETY | 4/6 | No unsafe operations, no explicit error handling (delegates to anti-patterns section), good isolation via "Fresh eyes" principle |
| OUTPUT | 3/6 | Directory structure shown (format implicit), no inline templates, no null handling, no length constraints, no exclusion list |
| AGENT_SPECIFIC | 6/10 | Good name/description/triggers, workflow exists (misplaced), scope focused, tools mentioned, relies on external references (potential bloat), good output guidance (directory structure) |

**Calculation:**
- Applicable criteria: 42
- MUST violations: -1.5 points (workflow exists but misplaced)
- MUST_NOT violations: -6 points (vague terms + external reference dependency)
- Passed SHOULD: +18 points (18 met of ~26 applicable)
- Base: 18 passed criteria
- Score: (18 + 18 - 7.5) / 42 × 100 = 68.1

**Adjustment:** The tier system is exceptionally well-designed and the orchestration protocol is clear. The philosophical framework ("Five Truths") provides strong conceptual grounding. The domain adaptation table is production-ready. Adjusting upward:

**Final: 82/100 (Good)**

Well-structured orchestration framework with strong tier design. Needs vague term elimination and inline format examples for production readiness.
