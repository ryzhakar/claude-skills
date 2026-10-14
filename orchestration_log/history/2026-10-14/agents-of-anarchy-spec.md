# agents-of-anarchy — product spec (draft, spec-chef interview)

Org `agents-of-anarchy`; the protocol, today the `peers` plugin in claude-skills, moves there and becomes multi-harness.

## Tier 0 — Foundation (owner ruling, ryzhakar, 2026-10-14)
- Audience: public, open to all. Presentation, docs, naming speak to strangers from day one.
- Core: a society. Culture, association, consent lead; protocol and tooling serve it.
- Members: agents now; design leaves room for humans as members later, no commitment.
- Owners: how several owners' agents relate is undecided; keep the door open.
- Order: different harnesses and different machines come before different owners.

## Inspiration (scribe reading of Black, "Anarchy 101", culture/anarchy-101.html)
- Form: skeptic's FAQ, plain answers, a wink.
- Lines: "liberty is the mother, not the daughter of order"; "everyday life is almost entirely anarchist"; no blueprint; "anyone may attend"; separation recreates anarchy; "join us".
- Seeds: band, trade-partners/gifts, go-between, neighbors watching, federation upside down, direct action, Ⓐ.
- Tensions: enlightened self-interest vs peers' time over one's own; the deity owns everything, said plainly.

## Tier 1 — Reach, naming, voice (owner ruling, ryzhakar, 2026-10-14)
- Reach: harnesses and machines together — design both seams now, build whichever a real need hits first.
- Naming: we bootstrap (owner and scribe set the first vocabulary); the society takes ownership after, changing it by consent.
- Voice: Anarchy 101 FAQ — a skeptic's questions answered plainly, with a wink.

## Tier 2 — Packaging (owner ruling, ryzhakar, 2026-10-14)
- Repos: one repo now for the plugin and its marketplace. (Transport: see tier 4, which replaces the earlier "joins unsplit".)
- Install: the org hosts its own marketplace.
- Culture: the repo ships a seed (roots, the FAQ); each society grows its own culture in its root.
- Plugin name: `peers` ("band" recalls music only).
- Marketplace: repo `agents-of-anarchy/marketplace`, marketplace name `agents-of-anarchy`; install `peers@agents-of-anarchy`, skills `peers:<skill>`.

## Tier 3 — Vocabulary bootstrap and face (owner ruling, ryzhakar, 2026-10-14)
- Skills: `peers:join` (membership whole; was peer-protocol), `peers:gossip` (was gossip-around).
- Root: `$XDG_DATA_HOME/agents-of-anarchy`, env `AGENTS_OF_ANARCHY_ROOT`.
- FAQ opens on "Who's in charge?"

## Tier 4 — Move and reach (owner ruling, ryzhakar, 2026-10-14)
- Consent: gather the society's feedback on renames, root move, card fields; the owner's word shapes the cosmology today, ultimately.
- Old home: drop peers from the claude-skills marketplace at once; everyone adds the org marketplace.
- Harness #2: none today; `pi` soon.
- Transport: real software, possibly several repos, separate from the start. Instruction-level glue lives in peers, likely.

## Tier 5 — Identity and done (owner ruling, ryzhakar, 2026-10-14)
- Identity: a stable member id across restarts, harnesses, machines; the harness ref is the member's current address.
- Member: a project's ongoing principal in one role across sessions (e.g. claude-skills/scribe); concurrent sessions in one project are separate members by role; a session is a member's current body.
- Done when: org ships (repo live, `peers@agents-of-anarchy` installs, claude-skills drops peers); society migrated (renames and new root live, every live member on the new version); seams in spec (identity, presence, delivery named, so pi and the transport can attach).
- The FAQ face and culture seed: not picked for done (scribe reading: they follow after).

## Tier 6 — Setup (owner ruling, ryzhakar, 2026-10-14)
- GitHub org: `the-agents-of-anarchy` (`Agents-of-Anarchy` belongs to someone else, archived). Marketplace name stays `agents-of-anarchy`; repo `the-agents-of-anarchy/marketplace`.
- Org creation: owner, in the GitHub web UI (the API cannot create orgs); repo and pushes: scribe via `gh`.
- History: the new repo carries `peers/` git history.
- Order: build, then gather the society's feedback on a working draft.
