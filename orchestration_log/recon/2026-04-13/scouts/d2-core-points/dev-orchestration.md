# Core Points: dev-orchestration

## Iteration 1

**Point**

The orchestrator never writes, debugs, or reads implementation code — it only dispatches agents, interprets status, and routes work through the lifecycle loop.

**Evidence**

1. SKILL.md line 226: "Code in orchestrator context. The orchestrator dispatches and decides. It does not write code, read implementation files, or debug test failures."
2. SKILL.md line 116: "Agents commit their own work with descriptive messages. If fixes are needed, dispatch a fix agent — the orchestrator does not edit code, does not commit code, does not debug code."
3. SKILL.md line 162: "The orchestrator reads status codes from completion summaries. Any analysis beyond the code itself — classifying concerns, diagnosing blockers — is delegated."

## Iteration 2

**Point**

Spec compliance review must always precede quality review, and reviewing quality before spec compliance wastes effort on code that may not meet requirements.

**Evidence**

1. SKILL.md line 128: "Two-stage review after each unit. Order is mandatory: spec compliance first, code quality second. Reviewing quality before confirming spec compliance wastes effort on code that may not meet requirements."
2. SKILL.md line 136: "Only after spec compliance passes. Dispatch the code-quality-reviewer with the git diff range."
3. SKILL.md line 230: "Reviewing quality before spec compliance. Polishing code that doesn't meet requirements is wasted work."
4. agent-dispatch.md line 39: "Dispatch order: spec review BEFORE quality review. Always."

## Iteration 3

**Point**

After 3 review-fix cycles without PASS, the orchestrator must stop and escalate rather than continuing to loop, because the problem is structural (spec ambiguity, architectural mismatch, or implementer quality limitation).

**Evidence**

1. SKILL.md line 149: "After 3 review-fix cycles without PASS, stop. The problem is structural — see @references/lifecycle-loops.md for escalation protocol."
2. lifecycle-loops.md line 151-160: "After 3 review-fix-re-review cycles on the same unit without reaching PASS: 1. STOP the review loop. 2. Assess whether the issue is: Implementer quality -- re-dispatch with a more capable model. Specification ambiguity -- the spec needs clarification. Escalate to the user. Architectural mismatch -- the unit cannot be implemented as specified because the design is wrong. Return to PLANNING. 3. Never enter a 4th review cycle without changing something structural (model, spec, or decomposition)."
3. lifecycle-loops.md line 203-210: "Test a maximum of 3 hypotheses before escalating. If 3 independent investigation agents fail to identify the root cause, this signals: The problem is architectural... The problem is environmental... The problem requires domain knowledge the agents lack. Escalate to the user with evidence gathered so far."

## Iteration 4

**Point**

Independent verification through test execution and type checking after every agent completion is mandatory, because agent self-reports are unreliable for cross-module integration failures.

**Evidence**

1. SKILL.md line 121: "Run the test suite and type checker after every implementer reports DONE. Agent self-reports are unreliable for cross-module integration — an agent may report DONE while its changes break tests in modules it didn't touch."
2. SKILL.md line 124: "This is the dev-specific application of the parent's governing principle #12: verify independently, trust artifacts not claims."
3. lifecycle-loops.md line 241: "Full test suite execution. Run all tests, not just the tests from individual units. Cross-unit failures emerge here."

## Iteration 5

**Point**

Cross-cutting reviews must decompose by concern (spec fidelity, data flow, simplicity, DRY/YAGNI) rather than by module, because module-scoped reviews miss cross-module bugs like interface mismatches and duplicated knowledge.

**Evidence**

1. SKILL.md line 199: "For multi-unit features, dispatch a cross-cutting review after integration passes. Decompose by CONCERN, not by module. Module-scoped reviews repeat shallow checks. Concern-scoped reviews find cross-cutting bugs."
2. SKILL.md line 202-208: Table showing concern decomposition with "Spec fidelity / Data flow integrity / Simplicity / DRY/YAGNI" and "What it catches" column listing cross-cutting issues.
3. SKILL.md line 209: "Fan out one agent per concern — this is the parent's fan-out-by-concern pattern applied to dev review."
4. SKILL.md line 238: "Module-scoped cross-cutting reviews. Reviewing each module independently misses cross-module issues (data flow bugs, interface mismatches, duplicated knowledge). Decompose final reviews by concern, not by module."

## Rank Summary

1. Orchestrator executes dispatch-and-route discipline only, never touching implementation code
2. Spec compliance review gates quality review (mandatory ordering to prevent wasted effort)
3. 3-cycle review limit triggers structural escalation (spec/arch/model change required)
4. Independent verification through test/type execution required after each agent (self-reports unreliable)
5. Cross-cutting reviews decompose by concern, not module (catches integration bugs)
