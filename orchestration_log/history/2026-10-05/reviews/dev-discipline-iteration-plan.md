# dev-discipline iteration — plan, 2026-10-05

Status: prepared, awaiting GO. GO executes every section below without a further question. GO with the word `3.0.0` sets that version instead of 2.2.0; nothing else in the GO message is read as a parameter.

## 1. Target

dev-discipline makes an agent write software the owner's way: a plan fixes contracts and gates; an implementer builds each unit by writing the outermost test first, pretend-calling functions that do not exist, declaring their signatures, recursing to the leaves, passing side effects down from the top, and refactoring once green; two reviewers check the contract and the code against those rules; a hook layer makes the review chain inevitable; debugging, triage, architecture, and review-receipt follow the same discipline. Every file is rewritten under `memento:skill-creation`; names, procedures, agents, and hook count stay.

## 2. Measured baseline (cl100k, exact)

| File | Tokens | Target |
|---|---|---|
| skills/tdd | 1559 | ≤1400, procedure replaced |
| skills/dev-orchestration | 6115 | ≤3000 |
| skills/defensive-planning | 2741 | ≤1300 |
| skills/systematic-debugging | 2589 | ≤1400 |
| skills/triage-issue | 1226 | ≤800 |
| skills/improve-architecture | 1441 | ≤1000 |
| skills/receiving-code-review | 1385 | ≤700 |
| agents/implementer | 1509 | ≤1000 |
| agents/spec-reviewer | 1333 | ≤900 |
| agents/code-quality-reviewer | 1728 | ≤1100 |
| hooks/templates ×3 | 415 | ≤240 |
| total | 22041 | ≤12840 |

Targets are ceilings. A file that needs fewer words ships smaller. A file that cannot meet its ceiling without cutting a core point ships over it, and the overage is recorded as residue.

## 3. Writing standard and rulings carried into every checker prompt

Standard: `memento/skills/skill-creation/SKILL.md`, read whole. Prose standard: Strunk SPR v3 (`.claude/manifesto-repo/LLM_MANIFESTOS/instructions/strunk_spr_v3_complete.xml`, fallback `https://raw.githubusercontent.com/ryzhakar/LLM_MANIFESTOS/refs/heads/main/instructions/strunk_spr_v3_complete.xml`). Reasoning: first-principles manifesto, same repository, `manifestos/first-principles.md`.

Rulings a checker applies before reporting a finding:

1. A sibling skill or agent named by name is never a defect.
2. A term another skill owns takes a gloss sufficient to parse its sentence and no more.
3. An enumeration that defines its items where it lists them is compliant.
4. Every tag's verb recurs in the tag's content; a verb that fails to recur is a fault only against a new synonym, not against a term the skill already owns. The checker sweeps every tag, never a sample.
5. The name `tdd` stands; the one-to-three-parts rule is not reported against it.
6. The artifact contract is prose inside a tag; a checker does not report the absence of a table.
7. Agent bodies are judged by the instruction rules of `<write-the-instructions>` and `<write-the-body>`, not by `<open-the-skill>`; agent frontmatter is judged against the platform field list in §6.
8. A hook template is one unconditional command in prose; a checker reports any condition, enumeration, or rationale in it.
9. A file under the skill's own directory, such as its `scripts/`, is inside the skill; a pointer to it is not a fetch outside.

## 4. Cross-cutting design decisions

D1. Outer contract, inner design. The plan fixes, per unit, the outermost interface — the signature a caller outside the unit uses — with a one-line docstring, the behaviors a test proves through it, and the verification gates. The implementer designs every signature beneath it through `tdd`. `spec-reviewer` compares code to the outer contract. `code-quality-reviewer` compares the inner design to `tdd`'s rules.

D2. Side effects at the top. Every clock, random source, filesystem, network, database, process-environment, and subprocess call is initialized at the outermost level and passed down as a parameter. `tdd` states it; `code-quality-reviewer` checks it.

D3. No comments. Any comment in product code is a Critical finding. Docstrings are one sentence on one line. Hook scripts shipped by this plugin obey the same rule.

D4. Tests stay at the barrier. Tests exercise the outermost interface; nothing below it, except the exceptional lower-level unit, which gets property-based tests (`hypothesis` in Python, `fast-check` in TypeScript, the language's equivalent elsewhere). Pinning tests — a test asserting an exact current value or sequence — only where behavior is unconventional and nothing else holds it.

D5. Review chain made real. SubagentStop output reaches the subagent, not the parent (platform fact, hooks.md). New layer, one script `hooks/review-chain.py`, python3 stdlib, no comments, tested:
   - `SubagentStop` `^(dev-discipline:)?implementer$` → record pending stage `spec-review` {agent_id, since, first 300 chars of `last_assistant_message`}.
   - `SubagentStop` `^(dev-discipline:)?spec-reviewer$` → record pending `quality-review`.
   - `SubagentStop` `^(dev-discipline:)?code-quality-reviewer$` → record pending `merge-decision`.
   - `PostToolUse` `^Agent$` → when `tool_input.subagent_type` names a dev-discipline agent: `status: completed` records the stage that agent's stop opens and returns `additionalContext` with that stage's mandate; `status: async_launched` retires the oldest pending stage the launched agent satisfies (`spec-reviewer` retires `spec-review`, `code-quality-reviewer` retires `quality-review`, `implementer` retires `merge-decision`).
   - `Stop` → while a `spec-review` or `quality-review` stage is pending, return `hookSpecificOutput.additionalContext` carrying that stage's mandate and the recorded message head, at most 3 consecutive continuations per stage, then clear it; a pending `merge-decision` is injected once and cleared.
   - State at `${CLAUDE_PLUGIN_DATA}/review-chain/<session_id>.json`, pruned after 7 days; registry unreachable → no claim.
   - Tests: `hooks/tests/test_review_chain.py`, pytest, driving the script through stdin and stdout only, `CLAUDE_PLUGIN_DATA` pointed at a temp dir. Justfile recipe `hooks-test`.
   - Templates: `review-mandate.txt`, `quality-review-mandate.txt`, `merge-mandate.txt`, each one unconditional command in prose, no condition, no rationale.
   - Old `*-stop.sh` scripts deleted.

D6. Worktree facts, not re-rooting policy. Platform refuses edits and commands that resolve to the main checkout from an isolated subagent (≥2.1.203). Implementer: resolve every path in the brief relative to the repository root inside the worktree; report the worktree path. Reviewers: no isolation, read the implementer's worktree by absolute path, every git command carries `-C <worktree>`. Re-rooting prose removed from all three.

D7. Base branch. A subagent worktree branches from the default branch. The brief names the integration branch; the implementer's first command merges it into the worktree branch; the orchestrator derives `BASE_SHA` with `git -C <worktree> merge-base HEAD <integration-branch>`.

D8. Preload. `implementer` frontmatter: `skills: [dev-discipline:tdd]`, `tools` include `Skill`; body: follow the preloaded `tdd`, invoke it with the Skill tool when absent from context.

D9. Tools. `spec-reviewer` gains `Bash`. Both reviewers keep `Write` for the verdict file. `implementer` keeps `Read, Write, Edit, Bash, Grep, Glob` plus `Skill`.

D10. No questions in flight. Implementer never asks; it reports `NEEDS_CONTEXT` or `BLOCKED`. `triage-issue` asks for the problem statement once when the request names none, never a second question. `improve-architecture` writes ranked candidates and a recommendation into the RFC instead of asking which to explore.

D11. Integration is delegated. The orchestrator launches an integration agent to merge a unit branch into the integration branch, run the full suite, and report; the orchestrator removes the worktree only after that report and after no continuation of that implementer remains.

D12. Status lives in a file. The orchestration status block is written to `orchestration_log/recon/${DATE}/dev-status.md` by the orchestrator after each state change, not into the conversation.

D13. Version 2.2.0 by default; `marketplace.json` mirrors `plugin.json`; READMEs regenerated by `just readme`.

## 5. Per-file specification

Each entry: core points (survive every cut, most prominent in the file), tag order (imperative verb phrases), terms defined at first use, and what is cut.

### skills/tdd/SKILL.md — rewrite from the owner's process
Description: build code by writing the outermost failing test first, designing the signatures beneath it before any body, and refactoring once green. Triggers: "tdd", "write tests first", "test-driven", "red-green-refactor", "implement using tdd", "design the signatures", "outside in", any request to write behavior-carrying code.
Core points: (1) one failing test at the outermost interface before any code; (2) signatures first — pretend-call functions that do not exist, then declare them with stub bodies, recursing to foreign calls or primitives; (3) side effects initialized at the top and passed down; (4) no comments, one-line docstrings, names carry the meaning; (5) refactor with hindsight only after green, tests never cross the barrier, lower levels fuzzed.
Tags: `<find-the-outermost-interface>` (defines interface barrier, outermost interface, foreign call) → `<write-one-failing-test>` → `<pretend-call-the-missing-functions>` (defines pretend call, call site) → `<declare-the-signatures>` (defines stub body; precise types no stricter than the caller needs; one-line docstring; spend most effort here) → `<recurse-to-the-leaves>` → `<pass-side-effects-down>` (defines side effect, pure function) → `<fill-bodies-to-green>` → `<refactor-with-hindsight>` → `<let-the-code-speak>` (comment ban, names, named constants) → `<keep-tests-at-the-barrier>` (mock only foreign services; never own modules; property tests for the exceptional lower unit; pinning only when demanded) → `<add-the-next-test>` (vertical slice; never horizontal) → `<verify-the-unit>`.
Cut: code examples, horizontal-slicing diagram, "confirm with the user", "get user approval", composability hedges, attribution footer, module-design heuristics (named in defensive-planning).

### skills/dev-orchestration/SKILL.md — delta-only extension of agentic-delegation
Description: drive the plan–implement–review–fix–integrate loop with the implementer, spec-reviewer, and code-quality-reviewer agents after reading `agentic-delegation`. Triggers kept.
Core points: (1) read `agentic-delegation` first, hard gate; (2) every implementer launch is followed by spec review, then quality review, then a merge decision — the hook layer continues the turn until each launches; (3) git is the source of branch and SHAs, files are the source of verdicts; (4) continue an agent for a scoped fix, launch fresh for a fundamental failure, cap at three review-fix cycles then change something structural; (5) the orchestrator writes no code, reads no implementation, debugs nothing — it launches, routes, and records.
Tags: `<read-the-parent-first>` → `<fix-the-artifact-paths>` (worktree, plan file, spec verdict, quality report, status file, mandates; `${DATE}`, `${branch}`, `${timestamp}` defined) → `<plan-the-units>` (unit = one outermost interface, 1–3 files, 2–10 minutes; plan through `defensive-planning`; order foundations first) → `<launch-the-implementer>` (brief sections: contract, integration branch, input paths relative to repo root, scope boundaries, scene-setting, verification gates; prompt written to a file; sonnet; background; worktree by the agent's frontmatter) → `<derive-branch-and-shas-from-git>` → `<launch-the-spec-review>` → `<launch-the-quality-review>` → `<decide-the-merge>` → `<route-on-status>` (DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED; continue vs fresh) → `<cap-the-fix-loop>` → `<escalate-to-debugging>` (`systematic-debugging` by name; speculative parallel from the parent) → `<integrate-the-units>` (integration agent, full suite, cross-cutting review by concern, worktree removal) → `<audit-the-tests>` (marker audit, valuable/smoke/tautological/missing) → `<record-the-status>`.
Cut: parent economics restated, SendMessage cost narrative, anti-pattern list (each becomes a paired prohibition in place), state-machine table, verb table beyond the dev delta, CWD-drift essay (one fact and one command).

### skills/defensive-planning/SKILL.md
Description: write an implementation plan, or a correction plan after a failed review, that leaves the implementer no decision, no option, and no unverifiable step. Triggers kept, "assessment" dropped.
Core points: (1) no decisions, no options, no "if needed"; (2) every unit carries its outermost contract — signature, one-line docstring, behaviors — and leaves the inner design to `tdd`; (3) gates are commands with exact required output; (4) forbidden patterns named explicitly, definition of done binary; (5) plan self-review: coverage, placeholder scan, type consistency.
Tags: `<assume-the-implementer-cuts-corners>` → `<map-the-files-and-contracts>` → `<write-each-unit>` → `<write-the-gates>` → `<forbid-the-patterns>` → `<define-done>` → `<review-the-plan>` → `<write-a-correction-plan>` (name the observed failure modes, close each escape hatch used, add gates that catch what passed) → `<write-the-plan-to-disk>` (path from `dev-orchestration`'s contract or the project's plan directory).
Cut: adherence assessment (owned by `spec-reviewer`), plan execution protocol, status table, two-stage review ordering, TDD micro-task code blocks, quick-reference gate commands, closing homily, attribution.

### skills/systematic-debugging/SKILL.md
Core points: (1) no fix before the root cause is found; (2) read the error whole, reproduce, diff recent changes, instrument each boundary; (3) one hypothesis, one minimal change, one variable; (4) a failing test before the fix, defense at every layer the bad data crossed; (5) three failed fixes means the architecture is wrong — stop and report.
Tags: `<investigate-before-fixing>` → `<reproduce-and-read>` → `<trace-to-the-source>` (bisection with `scripts/find-polluter.sh`, generalized: pollution path, test command, test files) → `<compare-with-working-code>` → `<test-one-hypothesis>` (parallel hypotheses through `agentic-delegation` by name) → `<fix-the-root-cause>` → `<wait-for-conditions>` (condition with timeout, never a fixed sleep; a fixed interval only after the triggering condition, with the interval's origin named) → `<stop-at-three-failed-fixes>` → `<report-the-cause>`.
Cut: rationalization table, red-flag thought list, user-signal list, TypeScript code, four-layer essay (kept as four named layers in one sentence each), quick-reference table.

### skills/triage-issue/SKILL.md
Core points: (1) one problem statement, then autonomous investigation; (2) investigation through `systematic-debugging`'s first three phases; (3) classify: regression, missing feature, design flaw, with scope and minimal fix; (4) TDD plan in `tdd`'s shape — outermost test first, vertical slices, refactor last; (5) issue document written to disk with problem, root cause, plan, acceptance criteria, path printed.
Tags: `<take-the-problem-statement>` → `<investigate-the-cause>` → `<classify-the-issue>` → `<plan-the-fix>` → `<write-the-issue>` → `<handle-the-exceptions>` (cannot reproduce; several causes; design change → `improve-architecture`).

### skills/improve-architecture/SKILL.md
Core points: (1) a deep module hides a large implementation behind a small interface; (2) friction found by exploring as a developer: bouncing, shallow interfaces, testability extraction, coupling, test gaps; (3) dependency category decides the test strategy; (4) three or more parallel designs under distinct constraints, compared, one recommended; (5) RFC on disk, boundary tests replace shallow tests.
Tags: `<explore-for-friction>` → `<rank-the-candidates>` → `<classify-the-dependencies>` → `<frame-the-constraints>` → `<explore-designs-in-parallel>` (`agentic-delegation` by name) → `<compare-and-recommend>` → `<write-the-rfc>` → `<replace-the-tests>`.
Cut: both user questions, the Ousterhout attribution, the agent output list beyond five named items.

### skills/receiving-code-review/SKILL.md
Core points: (1) verify every item against the code before acting on any; (2) clarify every unclear item before implementing any — as an agent, through `NEEDS_CONTEXT`; (3) push back with evidence when the item is wrong for this codebase; (4) one fix at a time, tested, blocking first; (5) no performative language — the change is the acknowledgement.
Tags: `<read-everything-first>` → `<verify-each-item>` → `<clarify-before-implementing>` → `<push-back-with-evidence>` → `<implement-one-at-a-time>` → `<answer-without-performance>`.

### agents/implementer.md
Frontmatter: `model: inherit`, `isolation: worktree`, `color: green`, `skills: [dev-discipline:tdd]`, `tools: Read, Write, Edit, Bash, Grep, Glob, Skill`.
Core points: (1) verify the worktree, merge the integration branch, resolve paths from the repo root; (2) follow `tdd` for every line; (3) commit atomically in the worktree; (4) self-review against the contract and `tdd`'s rules; (5) report status honestly with the worktree path — `NEEDS_CONTEXT` or `BLOCKED` instead of a question.
Tags: `<verify-the-worktree>` → `<read-the-contract>` → `<build-through-tdd>` → `<commit-in-the-worktree>` → `<review-yourself>` → `<report-the-status>`.

### agents/spec-reviewer.md
Frontmatter: `tools: Read, Write, Grep, Glob, Bash`.
Core points: (1) distrust the report, read the code; (2) every requirement located in code or marked missing, partial, extra, misinterpreted, with `file:line`; (3) read from the worktree by absolute path, git with `-C`; (4) verdict file at the supplied path with `Verdict: PASS|FAIL` on its own line; (5) return text is the path alone.
Tags: `<refuse-a-malformed-dispatch>` → `<read-the-spec-and-the-code>` → `<match-each-requirement>` → `<write-the-verdict-file>` → `<return-the-path>`.

### agents/code-quality-reviewer.md
Frontmatter: `tools: Read, Write, Grep, Glob, Bash`.
Core points: (1) read the spec verdict first and short-circuit on FAIL; (2) review only the diff range; (3) the checklist is `tdd`'s rules: comments, docstrings, names, signatures, side effects at the top, local reasoning, tests at the barrier, no own-module mocks, no undemanded pinning, property tests below the barrier, YAGNI, knowledge duplication; (4) severity Critical/Important/Minor with `file:line`, strengths named; (5) report file with `Ready to merge: Yes|With fixes|No`, return text the path alone.
Tags: `<refuse-a-malformed-dispatch>` → `<read-the-spec-verdict-first>` → `<scope-to-the-diff>` → `<check-against-the-rules>` → `<grade-each-finding>` → `<write-the-report-file>` → `<return-the-path>`.

### hooks
`hooks.json`: three `SubagentStop` entries with anchored matchers, one `PostToolUse` entry matcher `^Agent$`, one `Stop` entry, all calling `python3 ${CLAUDE_PLUGIN_ROOT}/hooks/review-chain.py <mode>`, timeout 10. `review-chain.py` per D5. `tests/test_review_chain.py`. Three templates, one command each.

## 6. Platform facts the files state (sources fetched 2026-10-05)

- sub-agents.md: `skills:` injects full skill content at start; plugin skills address as `plugin:skill`; `isolation: worktree` branches from the default branch unless `worktree.baseRef` is `"head"`; background subagents keep a fixed built-in tool set without `AskUserQuestion`; a background subagent's result arrives as a completion notification; `SendMessage` with the agent id resumes it with full history; subagents nest to depth 3.
- worktrees.md: four isolation checks — file edits to the main checkout, command cwd in the main checkout, git redirected into it, unverifiable command shape — refused as tool errors; a changed worktree stays until the periodic sweep.
- hooks.md: `SubagentStop` output keeps the subagent running; parent injection is `PostToolUse` on `Agent`; plugin agent types are plugin-scoped; matchers are unanchored regex; `Stop` continuation capped at 8 consecutive; `Stop` input carries `background_tasks`, `session_crons`, `last_assistant_message`; `PostToolUse` on `Agent` carries `tool_input.subagent_type` and `tool_response.status` of `completed` or `async_launched`.
- Plugin agent frontmatter fields: name, description, model, effort, maxTurns, tools, disallowedTools, skills, memory, background, isolation, color.

## 7. Execution on GO

Every step ends with a commit and `git push -u origin claude/dev-discipline-iteration-yby2xn`. Commit messages: single line, conventional, scope `dev-discipline`, no attribution. One commit per rewritten file; hooks (script, tests, templates, `hooks.json`, justfile recipe) as one commit; version and marketplace as one; READMEs as one; each record file class as one.

1. `tdd` written by the orchestrator; two blind checkers launched from `briefs/checker-compliance.md` and `briefs/checker-usability.md`, reports to `orchestration_log/recon/2026-10-05/checks/tdd-{compliance,usability}-r1.md`; revise; repeat to zero filtered findings or four rounds; commit.
2. `defensive-planning`, `systematic-debugging`, `triage-issue`, `improve-architecture`, `receiving-code-review` written; ten checkers in parallel; rounds as above; one commit each.
3. Three agents written; checkers with the agent variant of the briefs; commit each.
4. `dev-orchestration` written; checkers; then one cross-file agent from `briefs/checker-cross-file.md` holding all eleven files plus `hooks.json` and templates, reporting contradictions; fix; commit.
5. Hooks: `tests/test_review_chain.py` written first and run red; `review-chain.py` written to green; templates; `hooks.json`; old scripts deleted; `just hooks-test` green; `claude plugin validate dev-discipline`; commit.
6. `plugin.json` 2.2.0, `marketplace.json`; `just readme`; commit each.
7. Verifier agent from `briefs/verifier.md`, not an author of anything: runs the hook tests, the validator, `just check-readmes`, the token counter against §2, resolves every skill and agent name any file names, checks every frontmatter field against §6, confirms no comment in shipped scripts, no table or code fence inside a skill tag, no version in frontmatter. Findings fixed and re-verified.
8. Records: `events.md` kept current through every step; `failures.md` on the first failure; `session.md` final; `architecture_log.md` entry for the hook layer (runnable, with FROM → TO and INVALIDATES); `capabilities.md` dev-discipline section and the two known-limitation rows this changes; `conventions.md` artifact-contract row; `user_deferred_items.md` untouched. Separate commits per file class. Final push.

## 8. Checker loop

Author: the orchestrator. Checkers: `general-purpose` agents on sonnet, bound by preamble (`briefs/preamble.md`) to first-principles, Strunk v3, and the standard from source, carrying the rulings of §3 inline, each report opening `PENDING` on line one and replaced by a bare integer as its final edit. Neither checker sees the other's report. The compliance checker extracts the standard's instructions one per line, capped at one line each, then checks the draft against each. The usability checker reads the draft alone and follows it literally on a case it invents, counting every point that forces a guess. Rounds cap at four; residue is recorded in `session.md`.

## 9. Residue known before writing

- `just tokens` is offline in this environment; counts come from the npm `tiktoken` encoder, identical ranks, verified on one file.
- `claude plugin validate` and a live hook run depend on the CLI in this container (2.1.289 present); a live `skills:` preload of `dev-discipline:tdd` cannot be observed here beyond the validator and the documented syntax.
- The `agent_type` for a plugin subagent is documented as plugin-scoped; the anchored matcher accepts both the scoped and the bare form so a local copy of the agents keeps working.
