# Failures 2026-08-08

## 02:58 — Orchestrator misread a maintainer directive as a build order
Root cause: "propagate this observation to the manifestos plugin" parsed as "implement content injection" instead of "document the names-only fact."
Correction: agent stopped before any write landed; task repurposed to fact codification (shipped in manifesto 3.1.3).

## 03:20 — Orchestrator ruling sanctioned a factually wrong exception boundary
Root cause: ruling V7 approved an eight-path "reads and writes" enumeration without checking the Artifact Contract's producer column; `leave-verification.md` is agent-written, orchestrator-read.
Correction: independent verifier flagged the misattribution; boundary rewritten verb-accurate with a single definer before land (`ce49a77`).

## 02:53–03:43 — Agents repeatedly went idle without delivering final reports
Root cause: completion messages crossing with status checks; the harness blocks subagent report-file writes (verifier); probable context exhaustion after the largest job (migrator).
Correction: work verified from disk artifacts each time; reports recovered via continuation where possible; no work lost.

## 03:05 — Stale safety-net cron fired against an already-resolved dispatch
Root cause: CronDelete failed on an ID mismatch; the one-shot fired anyway.
Correction: the fired check no-op'd; later crons deleted promptly on completion.
