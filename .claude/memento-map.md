# claude-skills map

| path | kind | load | purpose |
|---|---|---|---|
| CLAUDE.md | charter | self | goals, session start, prime directives, pointers |
| orchestration_log/reference/ground-truth.md | frame | self | the problem as given |
| orchestration_log/reference/conventions.md | directive | self | how to work: rules with grounds |
| orchestration_log/reference/architecture_log.md | change | need | how the system's core changed |
| .claude/memento.yaml | schema | self | record kinds, homes, formats, admission |
| .claude/memento-map.md | map | start | index of records |
| orchestration_log/history/{date}/events*.md | events | start (tail) | one line per event |
| orchestration_log/history/{date}/session*.md | digest | start (close block) | a span's narrative and close block |
| orchestration_log/reference/capabilities.md | fact | need | what the system is and does, dated |
| orchestration_log/reference/user_deferred_items.md | deferral | need | what the owner put off |
| orchestration_log/reference/ | reference | latent | upstream specifications as supplied |
| orchestration_log/history/{date}/failures*.md | failure | latent | diagnosed failures |
| orchestration_log/archive/ | archived | latent | out of force, kept |
| orchestration_log/recon/{date}/ | scratch | latent | drafts, claims, worker returns |
