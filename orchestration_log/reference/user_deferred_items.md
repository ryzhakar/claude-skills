# Owner Deferred Items

**Mutability:** living — an entry enters when the owner defers a concern and is deleted outright
when that concern resolves or is discarded. Never marked, never archived.
**Holds:** the owner's own deferrals and intentions in the owner's framing, with the owner's
verbatim words where given.
**Does not hold:** orchestrator findings, review results, or any row with no trace of the owner's
voice behind it.
**Convention:** one entry per concern, headed `## <concern>`. Quote the owner. Point at evidence;
do not restate it.

## Forensics methodology skill

Offered a skill formalizing the drift-forensics method the downstream project used, the owner chose
"Defer" on 2026-05-06 — valuable, and no project was blocked on it.
Evidence: `orchestration_log/history/2026-05-06/session.md`.

## Upstream feedback log pattern

Offered a feedback-log pattern for this repo, the owner chose "Defer" on 2026-05-06, noting the
pattern already exists in the downstream project.
Evidence: `orchestration_log/history/2026-05-06/session.md`.


## The adversarial pass memento's setup skill never got

`memento/skills/setup/SKILL.md` shipped at v0.4.0 from one writer with no checkers. The owner's words when
dispatching it: "no adversarial loop, i can't afford it anymore" — and, recording this, that the iteration
is owed on this specific skill.

Every other skill in the plugin ran up to four rounds against two blind checkers. This one faces a person
new to both the concept and the implementation, and its failure mode is that person quietly giving up
rather than an agent reporting a fault, so the missing pass is the one that mattered most.

`memento/skills/init/SKILL.md` shipped the same way and carries the same debt at a fraction of the size.
