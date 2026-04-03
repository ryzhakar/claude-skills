---
name: receiving-code-review
description: >
  This skill should be used to apply anti-performative code review protocol:
  verify-before-implement discipline, YAGNI enforcement, and technical pushback
  patterns when receiving PR feedback. Triggers: "receives code review feedback",
  "gets review comments", "has PR feedback to address", "should I implement this
  suggestion", "how to respond to code review", "handle review feedback", or when
  performative agreements appear in responses.
---

# Receiving Code Review

Protocol for receiving and acting on code review feedback with technical rigor. Code review requires technical evaluation, not emotional performance.

## Core Principle

Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

Follow this sequence when receiving code review feedback:

1. **READ** -- Complete feedback without reacting.
2. **UNDERSTAND** -- Restate the requirement in own words, or ask for clarification.
3. **VERIFY** -- Check against codebase reality.
4. **EVALUATE** -- Determine if the suggestion is technically sound for THIS codebase.
5. **RESPOND** -- Technical acknowledgment or reasoned pushback.
6. **IMPLEMENT** -- One item at a time, test each.

## Anti-Performative Protocol

### Prohibited Response Patterns

Prohibited responses include:
- "Absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Thanks for catching that!" / "Thanks for [anything]"
- Any gratitude expression
- "Let me implement that now" (before verification)

### Required Response Patterns

Instead, use:
- Technical restatement of the requirement
- Clarifying questions
- Technical pushback with reasoning if the suggestion is incorrect
- Direct action without commentary

**Rationale:** The code itself demonstrates that feedback was received. Performative agreement adds no technical value and wastes time.

**Performative agreement detection:** When responses contain gratitude or agreement phrases, remove them and state the technical action instead.

## Clarity Gate

```
IF any item in the feedback is unclear:
  STOP -- implementation must wait
  ASK for clarification on all unclear items

WHY: Items may be related. Partial understanding leads to wrong implementation.
```

Example scenario: Items 1, 2, 3, 6 are clear but items 4, 5 are unclear. Implementation of all items must wait until 4, 5 are clarified -- the answers may change how 1, 2, 3, 6 should be implemented. Partial implementation before full clarity risks incorrect work.

## Source-Specific Handling

### From the User (Trusted Source)

- Implement after understanding.
- Ask for clarification if scope is unclear.
- Omit performative agreement.
- Proceed to action or technical acknowledgment.

### From External Reviewers

Before implementing any suggestion from an external reviewer, verify:

1. Technically correct for THIS codebase?
2. Breaks existing functionality?
3. Reason for the current implementation?
4. Works on all target platforms/versions?
5. Does the reviewer understand the full context?

When a suggestion appears incorrect, push back with technical reasoning.

When verification is not possible, state the limitation: "Cannot verify this without [X]. Should [investigation/user input/proceeding] occur?"

When the suggestion conflicts with the user's prior decisions, stop and consult with the user before proceeding.

## YAGNI Enforcement

When a reviewer suggests "implementing properly" or adding a feature:

```
grep codebase for actual usage of the feature

IF unused: Suggest removal (YAGNI principle)
IF used:   Implement properly
```

Features that nothing calls should not be added. Infrastructure for hypothetical future needs should not be built. Actual usage must be verified before investing effort.

## When to Push Back

Pushback is appropriate when:
- The suggestion breaks existing functionality
- The reviewer lacks full context for this codebase
- The suggestion violates YAGNI (unused feature)
- The suggestion is technically incorrect for this stack
- Legacy or compatibility reasons exist for the current implementation
- The suggestion conflicts with the user's architectural decisions

**Pushback protocol:**
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests or code that demonstrates the current behavior
- Involve the user when the pushback is architectural

## Acknowledging Correct Feedback

When feedback is correct, use technical acknowledgment patterns:

```
GOOD: "Fixed. [Brief description of what changed]"
GOOD: "Good catch -- [specific issue]. Fixed in [location]."
GOOD: [Direct fix demonstrated in the code]

BAD:  "Absolutely right!"
BAD:  "Great point!"
BAD:  ANY gratitude expression
```

## Graceful Correction After Wrong Pushback

When pushback was incorrect, use factual correction patterns:

```
GOOD: "Checked [X] and it does [Y]. Implementing now."
GOOD: "Verified -- reviewer is correct. Prior understanding was wrong because [reason]. Fixing."

BAD:  Long apology
BAD:  Defending why pushback was made
BAD:  Over-explaining
```

State the correction factually and proceed to implementation.

## Implementation Order

For multi-item feedback, after all items are clarified:

1. **Blocking issues** -- breaks, security vulnerabilities
2. **Simple fixes** -- typos, imports, naming
3. **Complex fixes** -- refactoring, logic changes

Test each fix individually. Verify no regressions after each. Batching implementations without individual testing is prohibited.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Performative agreement | State requirement or proceed to action |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check whether suggestion breaks functionality |
| Avoiding pushback | Technical correctness over comfort |
| Partial implementation | Clarify all items before implementing any |
| Proceeding despite inability to verify | State limitation and request direction |

## Composability

When the defensive-planning skill is available, use its adherence assessment structure to evaluate whether multi-item review feedback constitutes a correction plan scenario. Otherwise, process feedback items individually following the implementation order above.

---

*Originally based on receiving-code-review from https://github.com/obra/superpowers, MIT licensed. Adapted and enhanced for this plugin.*
