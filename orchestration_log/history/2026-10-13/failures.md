# Failures 2026-10-13

## ~15:43 UTC 2026-10-13 — Estimated send stamp, in the message proposing the rule against it
Root cause: the first proposal `[ask]` to 33a1a7 carried "18:4x — stamp pending `date`", written before running `date`; all three stewards had just named estimated stamps the protocol's first defect.
Correction: `date '+%Y-%m-%dT%H:%M%z'` run before sending; the other two copies carried 18:43+0300; a `[notice]` corrected the first.

## ~15:43 UTC 2026-10-13 — Silence-as-consent set on peers' acceptance
Root cause: the proposal said "silence by 19:15 = agree", against PROTOCOL.md § 8 (all stewards accept before a change) and 33a1a7's rule against an asker setting another orchestrator's default.
Correction: withdrawn by `[notice]` to fdb18d and 3c3084; only explicit accepts counted — all three came.

## ~15:50 UTC 2026-10-13 — Design reversed on a peer claim and dispatched before the peers settled it
Root cause: the owner's malleability ruling was read through 3c3084's unverified claim "each login keeps its own plugin cache", taken as fact; the orchestrator reversed an accepted resolution alone, traced a re-ask it never sent, and launched the writer before any steward answered. The owner stopped the dispatch: "you need to mine the thing with peers first"; "oauth is the ONLY thing that depends on login."
Correction: peer claims stay claims until checked; design questions go to the stewards and come back answered before any authoring dispatch.

## 16:10 UTC 2026-10-13 — Join invites claimed a shared checkout from a tmux label
Root cause: the invites to ffb899, 56bfc1, dc5e4c stated "you share this checkout" because ListAgents placed them in tmux session `claude-skills`; ListAgents shows no working directory, and 56bfc1 answered that its checkout is /Users/ryzhakar/LLM_MANIFESTOS. Only dc5e4c has evidence of writing here (`history/2026-10-12/`).
Correction: checkout claims come from cards or the session itself, never from tmux labels; 56bfc1 defers joining to the owner, which stands.
