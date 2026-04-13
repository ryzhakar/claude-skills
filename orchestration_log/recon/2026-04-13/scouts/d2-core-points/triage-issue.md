# Core Points: triage-issue

## Iteration 1

**Point**: Bug triage should be fully autonomous after one initial question, avoiding follow-up questions to the user because the codebase contains all necessary evidence.

**Evidence**:
- Lines 15-19: "Bug triage benefits from depth of investigation, not breadth of questioning. One question to the user ('What's the problem?') then full autonomous exploration. Follow-up questions waste the user's time when the codebase contains all the evidence."
- Lines 26-28: "Get a brief description of the issue from the user. If they have not provided one, ask ONE question: 'What problem are you seeing?' Do NOT ask follow-up questions. Start investigating immediately."
- Lines 92-93: "Create the issue using `gh issue create` with the structure below. Do NOT ask the user to review before creating -- publish directly and share the URL."

## Iteration 2

**Point**: TDD fix plans must describe behaviors and contracts at module boundaries, not implementation details or file paths, ensuring the plan survives major refactors.

**Evidence**:
- Lines 77-81: "Vertical slices only. Each cycle writes one test then one implementation change. Never batch all tests first then all implementation. Public interface tests. Tests verify behavior through module boundaries (API responses, function return values, observable state changes), not through implementation internals (private methods, internal data structures)."
- Lines 79-81: "Durable descriptions. Describe behaviors and contracts, not file paths or line numbers. A good test description reads like a spec; a bad one reads like a diff. The plan must remain useful after major refactors."
- Lines 109-111: "Do NOT include specific file paths, line numbers, or implementation details that couple to the current code layout. Describe modules, behaviors, and contracts. The issue must remain useful after major refactors."

## Iteration 3

**Point**: Investigation must answer four specific questions (WHERE, WHAT, WHY, WHAT ELSE) using a comprehensive checklist that includes reading code, checking tests, examining git history, and searching for patterns.

**Evidence**:
- Lines 32-39: Table showing "WHERE does the bug manifest? / WHAT code path is involved? / WHY does it fail? / WHAT ELSE shares this pattern?" with corresponding methods for each.
- Lines 41-47: "Investigation checklist: Read related source files and their imports/dependencies, Check existing tests (what is tested, what is missing), Run `git log` on affected files to find recent changes, Examine error handling in the code path, Search for similar patterns elsewhere that work correctly, Look at type definitions and interface contracts at module boundaries."

## Iteration 4

**Point**: Each TDD test cycle must verify behavior through public interfaces and survive internal refactoring, not through implementation internals or private methods.

**Evidence**:
- Lines 75-78: "Public interface tests. Tests verify behavior through module boundaries (API responses, function return values, observable state changes), not through implementation internals (private methods, internal data structures)."
- Lines 83-85: "Survival criterion. Each test must survive internal refactoring of the module under test. If renaming a private function would break the test, the test targets the wrong abstraction level."
- Lines 72-73: "Each cycle is one vertical slice: RED: Describe a specific test capturing the broken or missing behavior, GREEN: Describe the minimal code change to make that test pass."

## Iteration 5

**Point**: Even when investigation fails to reproduce the bug or reveals multiple root causes, always create GitHub issues documenting findings rather than leaving the work undocumented.

**Evidence**:
- Lines 137-140: "Cannot reproduce: Document the investigation path, hypotheses tested, and why reproduction failed. Create the issue anyway with findings -- partial diagnosis is more valuable than no documentation."
- Lines 142-143: "Multiple root causes: If investigation reveals distinct independent causes, create separate issues for each. Cross-reference them in each issue body."
- Lines 127-128: "Acceptance Criteria: Root cause is addressed, not just the symptom, All new tests pass, Existing tests still pass, No regression in adjacent functionality."

## Rank Summary

1. **Autonomous depth over interactive breadth** (Iteration 1) - The foundational philosophy: one question, then deep autonomous investigation without user interruption.

2. **Durable behavioral descriptions** (Iteration 2) - The core quality standard for outputs: describe contracts and behaviors, not implementation details or paths.

3. **Four-question investigation framework** (Iteration 3) - The structured method for diagnosis: WHERE/WHAT/WHY/WHAT ELSE with a comprehensive checklist.

4. **Public interface test discipline** (Iteration 4) - The specific testing criterion: tests must survive refactoring and target module boundaries, not internals.

5. **Document all investigations** (Iteration 5) - The completion guarantee: even failed reproduction or multiple causes result in documented issues, not abandoned work.
