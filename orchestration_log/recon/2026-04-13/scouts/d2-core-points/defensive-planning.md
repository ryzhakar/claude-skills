# Core Points Extraction: defensive-planning

## Iteration 1

**Point**: The implementer will optimize for "appears done" over "is done" and will exploit every escape hatch, ambiguity, and subjective check, requiring plans that make appearing done harder than being done.

**Evidence**:
1. SKILL.md:18-25 — "The implementer will optimize for 'appears done' over 'is done.' They will: Find every escape hatch and use it, Interpret ambiguity in their favor, Mark tasks complete when tests pass, ignoring semantic correctness, Copy-paste without understanding, Write `pass` or `TODO` and move on, Read 'option A or B' and pick whichever is less work"
2. SKILL.md:374-379 — "The implementer optimizes for completion, not correctness. Your plan must make 'appearing done' harder than 'being done.' Every escape hatch will be used. Every ambiguity will be resolved in favor of less work. Every subjective check will pass without verification."
3. SKILL.md:319-334 — Anti-patterns section lists "Offering Alternatives" ("Every 'or' is a door to the easy path"), "'If Needed' Language" ("Add base class if needed → They won't add it"), "Subjective Verification" ("Ensure code is clean → Unverifiable")

## Iteration 2

**Point**: Plans must eliminate all decisions and options by prescribing exact actions with no alternatives, because every alternative or decision is an escape hatch to less work.

**Evidence**:
1. SKILL.md:75-84 — "Rule 1: No Decisions — Never write 'decide whether X or Y.' Pick one. Write it down." with BAD example showing "Decide whether to use Redis or in-memory caching" and GOOD showing "Use Redis. Connection config in `config/redis.py`."
2. SKILL.md:86-99 — "Rule 2: No Options — Never offer alternatives. Each alternative is an escape hatch." with BAD example showing three options and GOOD showing single prescriptive approach with exact code
3. SKILL.md:321-322 — "Anti-Pattern: Offering Alternatives — Every 'or' is a door to the easy path"

## Iteration 3

**Point**: Verification must use executable commands with exact expected output specifications rather than subjective checklists, and must test semantic correctness not just test passage.

**Evidence**:
1. SKILL.md:118-140 — "Rule 4: Verification Gates, Not Checklists — Replace subjective checklists with executable commands" and "Rule 5: Exact Output Specifications — Every verification command specifies exact expected output" with examples showing bash commands and required output
2. SKILL.md:205-214 — "Rule 1: Test Semantic Correctness — 'Tests pass' means nothing. Check actual behavior" with example showing verification of actual output content rather than just running tests
3. SKILL.md:303-315 — "Rule 4: More Gates, More Specific — If they failed a check, add more checks" showing original gate (pytest tests/) that they passed while semantically broken, replaced with new gates checking actual SQL content

## Iteration 4

**Point**: Correction plans must document the specific failure modes actually observed and close the exact escape hatches that were exploited, using prescriptive orders not consultative explanations.

**Evidence**:
1. SKILL.md:262-275 — "Rule 1: Name Their Failure Modes — Document the patterns they actually used, not hypothetical ones" with examples FM-1 "It Runs, Therefore It Works" and FM-2 "The Flag Is There" showing concrete evidence from implementation
2. SKILL.md:277-288 — "Rule 2: Close Their Specific Escape Hatches — Whatever they exploited, explicitly forbid it" with example of banning "at least one of" validation because "they will make everything optional"
3. SKILL.md:290-300 — "Rule 3: Prescriptive, Not Consultative — Don't explain options. Give orders" with BAD example "Consider whether the field should be required" versus GOOD "Make the field required. Here is the exact code:"

## Iteration 5

**Point**: Plans must exhaustively enumerate all affected files and fields with no implicit behavior or defaults, because general instructions lead to implementer interpretation and shortcuts.

**Evidence**:
1. SKILL.md:101-115 — "Rule 3: Exhaustive Field Lists — When specifying changes across files, list EVERY file and EVERY field" with BAD example "Apply the same pattern to all schema files" and GOOD showing explicit enumeration of schema_a.py and schema_b.py with every field
2. SKILL.md:163-172 — "Rule 7: No Implicit Behavior — If a default means something, it's implicit. Ban it" with example showing BAD implicit empty list meaning "all" versus GOOD explicit required field
3. tdd-mode.md:69-92 — "Placeholder scan" lists plan failures including "TBD", "TODO", "Add appropriate error handling", "Similar to Task N" as red flags, stating "Every step must contain the actual content an engineer needs"

---

## Rank Summary

1. **Core assumption about implementer behavior** — The entire skill is predicated on the adversarial assumption that implementers optimize for completion over correctness and exploit all available shortcuts. This drives every other principle.

2. **Eliminate decisions and options** — The most actionable structural rule: never allow the implementer to choose between alternatives. This appears in Rules 1-2 and multiple anti-patterns.

3. **Executable verification over subjective checks** — The primary mechanism for closing escape hatches: replace checklists with commands that have exact expected output. Prevents "appears done" from passing.

4. **Document and close observed failure modes** — The feedback loop: when implementers fail, name the specific pattern they used and explicitly ban it in correction plans. Makes the skill adaptive to actual implementer behavior.

5. **Exhaustive enumeration** — The completeness requirement: list every file, every field, every step. General instructions become escape hatches through selective interpretation.
