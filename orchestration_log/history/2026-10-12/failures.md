# Failures 2026-10-12

## ~20:35 UTC 2026-10-12 — The inventory agent died on the account's session limit
Root cause: HTTP 429 `session limit · resets 2:50am (Europe/Kiev)` killed the sonnet inventory agent mid-run, after it wrote a partial report (4852 bytes, 23:25 EEST); the same limit held this session, so the death notification, the 23:41 check-back wake, and the reset reached it together only at the owner's "resume", 2026-10-13 09:35 UTC — about ten hours idle past the reset.
Correction: the agent is resumed through its transcript (`SendMessage` to its id) per the 2026-10-06 rule; no reset-aligned wake could be set, since no turn ran between the death and the reset.

## ~10:40 UTC 2026-10-13 — Nine owner decisions buried in a chat dump in internal vocabulary
Root cause: the brief's nine open decisions went to the owner as a compressed numbered list ("gate.py's 5 checks", "write-digest L11-18", "decision 5") inside a status message, not through `AskUserQuestion`; most were calls derivable from the owner's own rulings, and the one real question — where the plugin's line falls — never stood alone. The owner: "i don't even know what you're talking about. you burying some questions somewhere does not equal actually escalating anything."
Correction: escalate through `AskUserQuestion` only, each question self-contained in plain words naming what the owner recognizes, the most influential first; decide what the owner's rulings already settle and report it after.

## ~10:45 UTC 2026-10-13 — The split and the name went to the owner unthought
Root cause: the orchestrator relayed the brief's split as "three writer skills stay", flattening the brief's own finding that two of them carry general lines, and so asked the clean seven/three question the owner had already rejected; it read the owner's "simmer on this more" as the owner deferring the name, when it directed the orchestrator to think, and relayed an agent's candidates with no derivation of its own. The owner: "until you know what's in those 3 skills, you cannot know if there is anything you should own"; "have you given this ANY thought at all?"
Correction: the orchestrator reads the skills itself before asking about the line, derives the name itself, and walks the owner through each technical call one question at a time.
