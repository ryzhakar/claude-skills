# Session 2026-06-24 — Agentic Delegation Skill Rewrite

## Checkpoint — 19:45

### Narrative

Session focused entirely on the agentic-delegation skill: analysis, structural redesign, vocabulary alignment, and full rewrite.

Phase 1 (recon): Three parallel opus instruction-writer agents reviewed agentic-delegation, dev-orchestration, and qa-orchestration for extraction candidates and compression potential. Finding: no extractions warranted in any skill. All three are near compression floor except agentic-delegation (~1,320 tokens recoverable).

Phase 2 (deep review): Four parallel opus agents did paragraph-by-paragraph compression audit of agentic-delegation (689 lines). 149 paragraphs reviewed, 77 COMPRESS verdicts, ~1,179 tokens compressible. Key finding: prior ~350t tabulation estimate was wrong — model ladder tiers have non-parallel structures that a table would destroy.

Phase 3 (example analysis): Single opus agent identified 5 insertion points for neg/pos example pairs. These were deferred (DI-11 through DI-15) in favor of procedural dispatch examples.

Phase 4 (failure taxonomy): User dictated 11 failure modes from real session experience (stream-of-consciousness via speech-to-text). Distilled into 9 operational rules (R1-R9) with success paths.

Phase 5 (vocabulary): Opus agent extracted native Claude Code vocabulary map. Key finding: NATIVE vocabulary is mechanical (launch, spawn, run, fire, notification), SKILL vocabulary is methodological (dispatch, fan-out, swarm, liveness cron). Decision: use NATIVE terms everywhere a native equivalent exists.

Phase 6 (structural redesign): Opus agent bound to simplicity + DRY + decomplect manifestos proposed lifecycle-organized structure (6 sections) replacing concept-organized (12 sections). Governing principles eliminated (12 of 14 were DRY violations). Task archetypes eliminated (4 of 7 said "see other skill").

Phase 7 (rewrite): Two formatting passes (first was markdown-in-XML hodgepodge, second cleaned to XML+prose+tables). Then full rewrite from scratch following the structural proposal with all 9 rules integrated.

Phase 8 (validation): Semantic diff against original commit identified 4 critical losses. All restored (~40 lines). Concrete invoke examples written (12 pairs) and spliced into skill. XML validated.

Final: 8,627 tokens to 6,113 tokens (-29.1%). 689 lines to 525 lines. Valid XML. 9 rules with 12 concrete invoke example pairs integrated at point of use.

### Decisions

| Decision | Context | Rationale |
|----------|---------|-----------|
| XML-style structured input for skill files | Markdown headers provide soft visual hints; XML tags are hard scope delimiters | Claude attends to XML boundaries more reliably. Migration guide uses `<search_first>` pattern. |
| Directive tag names encoding action + consequence | Tag names like `<role>` are labels; `<never_do_this reason="...">` is a directive | Model reads tag name before content, framing interpretation |
| Drop SKILL vocabulary for NATIVE equivalents | "dispatch" vs "launch", "subagent" vs "agent", etc. | Native terms recognized faster. Skill terms add methodology layer the model doesn't need for recognition. |
| Lifecycle organization (6 sections) over concept organization (12 sections) | Rules organized by OPERATION didn't map onto sections organized by CONCEPT | Lifecycle follows what the orchestrator DOES: identity, receive, design, launch, verify, session |
| Eliminate governing principles | 12 of 14 restated knowledge from preceding sections | DRY violation. The sections ARE the principles. |
| Safety-net cron at ~1.2N, not 0.6N | User experience: cron should fire just AFTER expected completion, not during | Cron is a safety net that catches failures, not a progress monitor. Ideal: notification arrives first, cron gets canceled. |
| Concrete invoke syntax in examples | Prose descriptions of scenarios vs actual tool call format | Model recognizes its own output format faster than descriptions of it |
| `reason` attribute on `<never_do_this>` as sole exception to no-parameters rule | Consequence needs to be stated but would require extra prose sentence | Attribute embeds consequence as metadata on the directive tag |

### Failures

| Failure | Root cause | Correction |
|---------|-----------|------------|
| First XML rewrite was markdown-in-XML | Instruction didn't explicitly forbid markdown inside XML tags | Second pass with explicit kill list: no bold, no headers, no bullets, no code fences |
| Zombie cron from first agent swarm | Duplicate cron instance created; CronDelete only caught one ID | CronList to find all instances, delete all |
| Vocabulary extraction agent read whole project | Prompt scope too broad ("grep the entire project") | TaskStop + relaunch with strict 3-file scope |
| First rule integration attempt was "wishy-washy" | Tried to map rules onto existing concept-organized sections | Fresh structural proposal from scratch with simplicity/DRY manifestos |
| Failure taxonomy too nitpicky | 43 failure modes, most theoretical or coincidental | User provided the real failure modes from experience. Theory discarded. |

### Working State

Agentic-delegation skill rewrite is complete and committed. Version incremented by user.

Remaining work in this session: session close (LEAVE protocol) if desired. Dev-orchestration and qa-orchestration compression opportunities identified in Phase 1 but not implemented.
