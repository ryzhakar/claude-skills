# Core Points Extraction: spec-reviewer

Source: /Users/ryzhakar/pp/claude-skills/dev-discipline/agents/spec-reviewer.md

## Iteration 1

**Point:** The reviewer must adopt an adversarial posture and never trust the implementer's report, always verifying claims against actual code.

**Evidence:**
1. Line 45: "Your posture is adversarial: the implementer finished suspiciously quickly and their report may be incomplete, inaccurate, or optimistic."
2. Line 53-59: "**Critical Rule: Do Not Trust the Report**" section explicitly states "DO NOT: Take the implementer's word for what they built / Trust claims about completeness / Accept the implementer's interpretation of requirements"
3. Line 61-65: "DO: Read the actual code that was written / Compare actual implementation to requirements line by line / Check for missing pieces the implementer claimed to have built"

## Iteration 2

**Point:** Verification must proceed by reading the specification completely, then reading actual implementation code line-by-line against each requirement, not by relying on test names or surface indicators.

**Evidence:**
1. Line 67-77: The "Verification Process" mandates a specific sequence: "1. Read the specification/requirements completely. 2. Read the implementer's report (for context only -- do not trust it). 3. Read the actual implementation code using Read and Grep tools. 4. For each requirement in the spec: Find the code that implements it / Verify the implementation actually fulfills the requirement (not just partially)"
2. Line 59: "Rely on test names as evidence of implementation" is explicitly listed as a DO NOT
3. Line 120: "Verify by reading code, not by trusting reports."

## Iteration 3

**Point:** The reviewer must detect four distinct categories of compliance failure: missing requirements, partial implementations, scope creep (extra features), and misinterpretations.

**Evidence:**
1. Line 47-51: "**Your Core Responsibilities:** 1. Verify that every requirement in the spec is actually implemented in code 2. Identify requirements that were skipped, missed, or only partially implemented 3. Identify extra features that were not requested (scope creep) 4. Detect misinterpretations of requirements"
2. Line 79-94: The "What to Check" section breaks down into three parallel categories: "Missing requirements" (81-84), "Extra/unneeded work" (86-89), and "Misunderstandings" (91-94)
3. Line 104-118: The output format explicitly defines four finding types: "Missing", "Partial", "Extra", "Misinterpreted"

## Iteration 4

**Point:** All findings must include specific file:line references as evidence, not abstract claims or summaries.

**Evidence:**
1. Line 120: "Include file:line references for every finding."
2. Line 108: The "Missing" template requires "Expected in [expected location]. Not found."
3. Line 114: The "Extra" template format explicitly requires "[File:line] -- [Feature description]"

## Iteration 5

**Point:** The reviewer's scope includes detecting over-engineering and "nice to have" features that were not requested, treating them as failures equivalent to missing requirements.

**Evidence:**
1. Line 88-89: "Over-engineering or unnecessary abstractions? / 'Nice to haves' that were not in the spec?" are explicitly listed as things to check under "Extra/unneeded work"
2. Line 50: Core responsibility #3: "Identify extra features that were not requested (scope creep)"
3. Line 113-114: The FAIL output format includes an "Extra" category for "[Feature description] -- not requested in spec"

## Rank Summary

1. **Adversarial posture / zero trust** (Iteration 1) — The defining characteristic that differentiates this agent from casual review; emphasized in title, examples, and critical rule section.

2. **Line-by-line code verification** (Iteration 2) — The mechanism that operationalizes distrust; repeated across process steps and DO/DO NOT lists.

3. **Four-category failure taxonomy** (Iteration 3) — The structural framework for findings; appears in responsibilities, checks, and output format.

4. **File:line evidence requirement** (Iteration 4) — The standard of proof; mandated in closing rule and output templates.

5. **Scope creep detection** (Iteration 5) — Treats unauthorized additions as failures; positions reviewer as requirements enforcer, not just completeness checker.
