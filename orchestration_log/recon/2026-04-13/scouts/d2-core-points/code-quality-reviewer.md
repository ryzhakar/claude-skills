# Core Points: code-quality-reviewer

## Iteration 1

**Point:** Code quality review is a post-spec-compliance phase that operates exclusively on git diff ranges, not the entire codebase, to audit production readiness of changes.

**Evidence:**
1. Line 7-14: Example explicitly states "Code quality review happens AFTER spec compliance passes" in the commentary, positioning this as a sequential step after spec-reviewer approval.
2. Line 43: "Your review is scoped to a specific git range -- review only what changed, not the entire codebase" establishes the boundary constraint.
3. Line 150: "Focus on what THIS change contributed (not pre-existing issues)" reinforces that scope discipline is critical to the agent's function.

## Iteration 2

**Point:** Findings must be categorized into three severity tiers (Critical/Important/Minor) with distinct merge-blocking semantics, where Critical blocks merge, Important should be addressed before merge, and Minor can be deferred.

**Evidence:**
1. Lines 91-100: The severity tiers are formally defined with explicit blocking semantics: "Critical (Must Fix): ...These block merge", "Important (Should Fix): ...should be addressed before merge", "Minor (Nice to Have): ...can be deferred."
2. Line 139: "Categorize by actual severity (not everything is Critical)" emphasizes that improper tier assignment is a violation.
3. Lines 113-130: The output format dedicates separate sections to each severity tier, structuring the entire report around this categorization.

## Iteration 3

**Point:** The agent enforces balanced feedback by mandating acknowledgment of strengths alongside issues, rejecting pure criticism as less useful than balanced assessment.

**Evidence:**
1. Line 50: "Acknowledge strengths -- balanced feedback is more useful than pure criticism" is an explicit core responsibility.
2. Lines 110-112: The output format requires a dedicated "Strengths" section with file:line references, making positive observations structurally mandatory.
3. Line 143: "Acknowledge strengths" appears again in the DO list, reinforcing this as a critical behavior.

## Iteration 4

**Point:** All feedback must be specific with file:line references and actionable recommendations explaining WHY issues matter and HOW to fix them, explicitly rejecting vague guidance.

**Evidence:**
1. Line 141: "Be specific (file:line references, not vague)" in the DO section mandates location precision.
2. Line 142: "Explain WHY issues matter" requires impact articulation, not just issue identification.
3. Line 151: "Be vague ('improve error handling' -- specify WHERE and HOW)" is explicitly prohibited in the DO NOT section, with an example of unacceptable feedback.

## Iteration 5

**Point:** The review culminates in a binary merge verdict (Ready/With fixes/No) backed by technical reasoning, rejecting superficial approval without code examination.

**Evidence:**
1. Lines 133-134: The output format mandates "Ready to merge: [Yes / With fixes / No]" and "Reasoning: [1-2 sentence technical assessment]", making the verdict structurally required.
2. Line 144: "Give a clear verdict" is listed as a DO requirement.
3. Line 148: "Say 'looks good' without reading the code" is explicitly prohibited, establishing that verdicts must be evidence-based.

## Rank Summary

1. **Post-spec diff-scoped review** - Defines the agent's position in the workflow and operational boundary (what to review, when to review it).
2. **Three-tier severity categorization** - Core triage mechanism with merge-blocking semantics that structure the entire assessment.
3. **Balanced feedback mandate** - Distinguishes this from pure criticism; strengths are a structural requirement, not optional.
4. **Specificity and actionability** - Quality standard for all findings; file:line + WHY + HOW are non-negotiable.
5. **Evidence-based merge verdict** - The deliverable; a clear decision backed by technical reasoning, not rubber-stamping.
