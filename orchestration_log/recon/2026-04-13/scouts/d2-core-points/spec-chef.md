# Core Points: spec-chef

## Iteration 1

**Point:** Questions must be constrained to 2-4 concrete options with explicit trade-offs, not open-ended, because forced choice produces codifiable decisions while open questions generate unusable narrative.

**Evidence:**
- SKILL.md:66-74: "Use `AskUserQuestion` tool with constrained choices: **Rules:** - 2-4 options per question (forces concrete decisions) - Include trade-off in each option's description - One decision per question (don't bundle) - 1-4 questions per round (don't overwhelm) - 'Other' is always available (stakeholder can escape)"
- SKILL.md:111: Anti-pattern table explicitly contrasts "Don't: Ask open-ended questions" with "Do Instead: Offer 2-4 concrete options"
- SKILL.md:76-84: Anatomy demonstrates each option requires label AND description with trade-offs: "options: - label: 'Small (10-50)' description: 'Use case A, trade-off B'"

## Iteration 2

**Point:** Questions must be ordered by dependency tiers where later answers depend on earlier ones, because asking detail-level questions before foundational questions produces contradictory or impossible-to-answer choices.

**Evidence:**
- SKILL.md:44-60: "Order questions into tiers. Later tiers depend on earlier answers" followed by explicit tier dependency chain from Tier 0 Foundation through Tier 5 Success
- dependency-tiers.md:14-22: "The Principle: Some questions can't be answered without prior answers: 'What file formats?' depends on 'Who's the user?' ... **Rule:** If answering Question B requires knowing Answer A, then Question A must come first"
- dependency-tiers.md:117-138: "Mapping Your Own Tiers" section providing visual validation technique: "Can I answer Tier N without knowing Tier N-1?"

## Iteration 3

**Point:** Artifacts must be written immediately after tier completion or at most after all tiers complete, because context decay makes delayed codification produce incomplete or inaccurate documentation.

**Evidence:**
- SKILL.md:88-90: "Write artifacts IMMEDIATELY after each tier (or at most after all tiers complete). Don't wait—context decays" with emphasis capitalized on IMMEDIATELY
- SKILL.md:113: Anti-pattern contrasts "Don't: Wait to codify" with "Do Instead: Write artifacts immediately"
- SKILL.md:22: Core workflow principle lists "**Codifies immediately** (artifacts before context decays)" as one of five essential mechanisms

## Iteration 4

**Point:** Each artifact type must maintain strict concern separation (WHAT/WHO/VALUE/HOW) with single source of truth for each decision, because mixing concerns or duplicating decisions across artifacts creates maintenance failures and conflicting specifications.

**Evidence:**
- SKILL.md:92-100: Artifact separation table explicitly maps what each artifact "Contains" versus "Does NOT Contain" with Product Spec containing "Decisions, constraints, behaviors" but NOT "Technical architecture"
- artifact-separation.md:155-209: Four detailed "Common Mistakes" examples showing wrong/right separation: mixing WHAT and HOW, mixing WHO and WHAT, stories without value, and duplication
- artifact-separation.md:212-220: "Maintenance Rule: When a decision changes: 1. Update the source artifact ... 3. Don't duplicate the decision in multiple places. Single source of truth. References, not copies"

## Iteration 5

**Point:** Gap detection must scan for six specific gap types (personas, behaviors, assumptions, edge cases, success criteria, scope) using signal phrases that reveal implicit knowledge or undefined behaviors in existing documentation.

**Evidence:**
- SKILL.md:31-40: Table defining six gap types with corresponding signals: "Missing personas" signals "users without specifics", "Undefined behaviors" signals "handles errors without how", etc.
- gap-heuristics.md:15-119: Six dedicated sections each defining signal phrases, what's missing, and questions to surface for each gap type
- gap-heuristics.md:122-132: "Detection Technique" provides six systematic questions to apply to each documentation section: "Could two engineers interpret this differently? → Ambiguity gap"

## Rank Summary

1. Constrained questioning (2-4 options with trade-offs) - Most emphasized mechanism, appears in protocol, anti-patterns, and tool requirements
2. Dependency tier ordering - Core structural principle governing question sequencing across all domains
3. Immediate codification - Repeated emphasis on timing prevents context decay
4. Artifact separation - Extensive templates and mistake catalogs enforce concern boundaries
5. Gap detection taxonomy - Systematic scanning approach using six categories with signal phrases
