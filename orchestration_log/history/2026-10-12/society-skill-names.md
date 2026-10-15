# Skill names for the peer society, four lenses

## Binding
Loaded in full from source: first-principles (manifestos/first-principles.md), self-documenting-code (manifestos/self-documenting-code.md), Strunk SPR v3 (raw.githubusercontent XML, curl), manifesto-oath (injected protocol); convergence: all four reject inherited form for function, so a name states the act in plain words, and tension: SDC's long specific names against Strunk's omit-needless-words, resolved by the `peers:` prefix carrying context.
I must derive each pick from the primary text and not from the digest, and I will cite the source line wherever the text overturns the digest; I must not carry the void part-count rule, and I will not rank by it.
I must name the act in the fewest plain words, and I will keep hyphens and nouns only where one plain verb cannot name the act; I must not propose beyond what I verified, and I will mark every unchecked claim.

## Picks
Paths: J = `peers/skills/join/SKILL.md`, G = `peers/skills/gossip/SKILL.md` (marketplace repo). Line numbers are the file's own. Principle ids are the digest's section 1.

| procedure | pick | reason | principle | clash |
|---|---|---|---|---|
| P1 join | `join` | Blessed. The act of becoming a member, once the catch-all work moves to its own skills. | 1.1, 1.5 | none |
| P2 keep card true | `card` | No plain verb names "keep true"; the domain noun reads in the slot "by the skill `card`". Absorbs parking: `state: dormant` is a card field (J:504 region). | 1.2, 3.3 | noun, an exception |
| P3 send messages | `message` | Peers say "message a peer" (J:5). A verb, and it avoids `send-message`, the echo of the harness tool `SendMessage`. | 3.4, 1.2 | harness `SendMessage` only |
| P4 mutual aid | `aid` | One plain verb. J:288 section is `give-mutual-aid` and Black's term stays in the description (roots.md "mutual aid"). Drops "mutual" from the name. | 2.9, 1.3 | none; J:289 already covers idle capacity, see P5 |
| P5 participate when not busy | `volunteer` | One plain verb for filling a free stretch for the society. Not in J today; J:289 gives idle capacity to `aid`. Split: `aid` offers to a named peer, `volunteer` picks the work. | 1.3, 2.8 | `check-back` (the wake mechanism, a different act) |
| P6 learn from commons | `learn` | J:171 "Know what the commons learned since your last read". Adoption is J:331-333. The thank-its-origin step is void: J:245 "never reply to confirm or thank"; adoption is reported as a line citing `#<n>` (J:333). | 1.1, 1.6 | none |
| P7a steward shared thing | `steward` | The verb is J:362 "Steward a shared thing". Service, not title. | 2.5 | none |
| P7b exclusive resource | `reserve` | Board line for a port or GPU, plain booking word; avoids `hold` (J:370 "never as property"). | 2.5, 1.4 | J:39 uses "reserves" for the owner, different sense |
| P8 settle disputes | `settle` | Covers both the disputant and the go-between; the go-between stays in the description (Black). | 2.6, 1.1 | none; avoids `ask` (a tag) |
| P9 relay owner rulings | `relay` | J:410 section is `relay-owner-rulings`; word peers already use. The runner-up is `carry-ruling`. | 1.3 | `relay` inside memento `staging-relay` and J/G "relay" prose; bare name is free |
| P10 continuity | no skill | J:418-422 is two lines: line 1 is memento's job; the receipt line (J:422) goes into `message`. If kept: `remember`. | 1.5 | memento `record-writing` |
| P11a leave | `leave` | "leave notice" (J:77, J:504) and `[notice] leaving` are the peers' words; exact antonym of `join`. | 3.4, 1.1 | none |
| P11b sweep | `sweep` | J:504 "Sweep a card"; moves departed cards, a housekeeping act distinct from leaving. | 1.4 | none |
| G1 ask around | `ask-around` | The trigger in G:5; idiom peers say aloud. Only if split from `gossip`. | 3.4, 2.7 | `[ask]` tag: consistent, the skill sends it |
| G2 spread what you learn | `pass-it-on` | G:5 trigger; wink idiom. Only if split from `gossip`. | 3.4, 2.7 | `relay` handles what you received; `pass-it-on` is what you learned |
| gossip core | `gossip` | Blessed. Keeps the shared envelope (`asked:`, `has:`) and relay rules (G:29, G:61, G:65). | 1.1 | stale `my-claude-skills/peers/0.3.0` `gossip-around` |
| A1 protocol change | `propose` | J:5 already says "propose a protocol change"; no legislative word. The runner-up is `change-protocol`. | 2.4, 3.4 | memento "amend" avoided entirely |
| A2 scribe | `scribe` | Verb: keep the canonical text and hand it on. J:488 makes the role a stewardship; claim goes through `steward`. | 2.3, 2.5 | see Missed procedures |
| C commons | `tend-commons` | Garden verb from J:298 (`tend-the-commons`); bare `tend` would read as tending peers, so the object stays. | 1.3, 2.6 | none |
| O shared terms | `ontology` | Blessed. It holds terms and nothing else (not P10, not leftover rules). | 1.7, 1.5 | none |

## Missed procedures
- Presence and liveness (J:73-81): who is live, `busy`/`idle`/`waiting`, leave notice means gone. Fold into `ontology` (terms) and `message` (what to send to whom); no new skill.
- Hazard handling (J:236, J:249-251): act on `[hazard]` at once, send only hazards to a `waiting` peer. Fold into `message`.
- Owner standing (J:30-56): the owner as away deity, what to bring to the owner. Fold into `ontology`; mark its rules in each skill that sends to the owner.
- Facts about yourself (J:93-101): stamp, model, `peers-facts`. Fold into `card`.
- Old-root move (J:126-): a migration step. Retire it when the last member has moved; no name.

## Summary
1. Sixteen picks are one word (`card` a noun, an exception); `tend-commons`, `ask-around`, `pass-it-on` keep hyphens; P10 gets no skill.
2. The digest's wire tokens `from:`, `spread:`, `relay:` do not exist: G and J carry only the tags `[notice] [hazard] [ask] [answer]` and the fields `asked:` and `has:` (G:29, G:61); lens 3 clashes for `relay` and `spread` fall.
3. The digest's "thank its origin" (P6) and "Learn first" at J:295 do not stand: J:245 forbids thanking and J:295 holds a different line.
4. A2 is a stewardship (J:488), and P5 is not yet in J, so the first folds partly into `steward` and the second needs new text.
5. Memento clashes: avoid `amend`; bare `relay` and `reserve` are free; `volunteer` overlaps `check-back`'s wake only.
6. The digest cites the aoa-participation checkout and line numbers off by two (J:67 is J:65); I did not edit it.
