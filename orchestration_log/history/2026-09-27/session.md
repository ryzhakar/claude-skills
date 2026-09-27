# Session 2026-09-27

Resumed onto a review of the `agent-conduct:work-silently` proposal. The skill's text was clean; its mechanism was not — silence lived only in context and died at compaction or resume. A marker file plus a SessionStart hook fixed it, and the proposal's commits were re-cut without attribution before merging to main.

The owner then asked for the discontinuous-existence material to leave orchestration. A design pass framed it as supervising dispatched agents; the owner rejected that: continuing to exist concerns the agent, not agents. `check-back` shipped in agent-conduct on that footing, with a Stop hook that keeps a turn going while work is pending and no wake is set, and a resume notice naming what died.

Plugin dependencies arrived with it. The dependency scan declared orchestration → memento from migration leftovers; the owner ruled that unintended, and orchestration was stripped of every memento mention and both retired stubs, landing at 5.0.0.

A staging script destroyed the uncommitted work once; every agent still held its edits and restored them. Later commits staged in a scratch worktree with the main tree kept as backup, verified byte for byte before anything was replaced.

Dependencies were verified live in the harness. The owner's installed copies predate the field and need updating to activate it.

Open: this repo has no memento project config, so its records sit off-schema; no baseline home exists here. The owed adversarial pass on memento's `setup` and `init` stands.
