# Failures 2026-10-05

## 23:23 — The remote harness re-prompts every turn that ends with no visible text
Root cause: `work-silently` ends each silent turn with the empty string. In this cloud session the harness answers an empty turn with `[Your previous response had no visible output. Please continue and produce a user-visible response.]`, which starts a new turn at once; two consecutive silent turns produced two re-prompts within a minute, so silence here is a loop, not a wait.
Correction: silence held for the body of every turn; each turn now ends with one line of state, the shortest that is true, and nothing else. Recorded for `agent-conduct:work-silently`: the empty-string ending is a platform fact of the local CLI, not of the remote harness, and the skill needs a stated fallback for a harness that refuses an empty turn.

## 23:32 — A draft was edited while its compliance check was running
Root cause: usability reports arrive before compliance reports, and the usability fixes to `defensive-planning` were written while its compliance checker still held the round-1 text; the checker noticed the mtime change, discarded its first read, and audited the new version, so its count mixes two drafts.
Correction: from round 2 on, a draft changes only after both of its round's reports have landed; a report that arrives against a changed draft is re-run rather than read.
