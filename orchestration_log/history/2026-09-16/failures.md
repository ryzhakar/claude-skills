
## Session limit killed thirteen agents at once, 2026-09-17 ~00:15

Running at 17 of the 20-agent ceiling, the whole fleet died on one limit boundary: five authors, eight checkers. Blast radius scales with concurrency, and the three limit deaths this session hit 2, then 9, then 13 — each at a higher running count than the last.

Recovery cost nothing but time. Twelve agents had written nothing; their drafts and reports were untouched and restarted clean. One had begun applying edits — corpus-reconciliation sat at 1252 tokens against the 1267 it started from — so its restart carries an instruction to read the draft as it stands rather than assume either end state.

Nothing was lost. Two dying agents had already reported substantive findings in their notifications, including the resolution of corpus-reconciliation's sharpest defect, and those survive in the restart prompts.

The lesson is not to run fewer agents. It is that a fleet at the ceiling shares one failure, so every dispatch prompt must be reconstructible from the orchestrator's own notes — which is what made a thirteen-agent restart a single turn's work.

## An agent ran three hours and died on the output ceiling, 2026-09-17 ~03:15

A compliance checker on `schema-resolution` ran roughly three hours against a thirty-minute ceiling for every comparable check, then terminated on the 64,000-token output maximum. It was never going to finish. It had been generating without bound the whole time.

This inverts the liveness heuristic the 2026-09-15 failures record established. That entry held that transcript size answers whether a process lives but never whether an agent works. Here growth was worse than uninformative — it was actively misleading, since the transcript grew steadily and the growth was the symptom. A size check would have reported health right up to the death.

The recovery cost nothing: rather than killing a possibly-working agent on suspicion, a second checker was dispatched to a separate output path to race it. Whichever landed first would unblock the work, and no result could be lost either way. Racing beats killing whenever the output paths differ and the work is idempotent.

What actually distinguishes a doomed agent from a slow one is elapsed time against the observed distribution for that task type, not any property of the transcript. Twenty comparable checks had completed between eleven and thirty minutes; six times the longest of them was the signal.

### It recurred, so it is the brief, not the agent

A second compliance checker died on the same 64,000-token output ceiling within the hour, auditing a different skill. Two deaths out of roughly twenty-five compliance runs, and file size does not explain it — one target was the corpus's largest skill at 1663 tokens, the other among its smallest at 806.

What both share is the brief. `checker-compliance-brief.md` has the checker write all 31 extracted instructions into the report before reading the draft, then append a finding per instruction as it checks. That is a deliberate design — the two-phase split exists to stop lenient audits, and writing the extraction first is what makes the split verifiable. But it puts an unbounded transcript between the agent and its verdict, and an agent that starts elaborating inside that structure has nothing to stop it.

The fix is not to abandon two-phase checking, which earned its place. It is to cap the extraction's form: one line per instruction, no commentary, and a stated ceiling. Left unchanged for this build because both deaths were absorbed by racing a replacement, and changing the brief mid-build would have made the remaining reports incomparable with the twenty-odd already collected.
