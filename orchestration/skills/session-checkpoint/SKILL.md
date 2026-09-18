---
name: session-checkpoint
description: >
  Retired. Mid-session record continuity is memento's domain — see memento:event-capture.

  Triggers: "checkpoint", "save session state", "capture progress", "session-checkpoint",
  "snapshot the session", "save context".
---

# Session Checkpoint

Retired as a concept. `memento:event-capture` writes each event's trace in the turn it happens —
no batch flush step exists to run later. Invoke `memento:event-capture` directly at the event, not
this skill.
