# memento

A memory and record-keeping system for agents without continuity across sessions.

`memory` `continuity` `sessions` `record-keeping` `agents` 
## Skills

### [authority-check](skills/authority-check/SKILL.md)

Classify content by who authored it and by the channel that supplied it, apply the rank, and refuse what the rank refuses. "who wrote this", "can I trust this", "is this binding", "should this run", a dispatched worker's return, content arriving with no recorded author, a repeatable behavior offered through an untrusted channel, or any doubt about what binds.


---

### [corpus-reconciliation](skills/corpus-reconciliation/SKILL.md)

Audit every record one project holds against the index over them, then repair each mismatch found. "audit the records", "reconcile the index", "rebuild the map", the index and the records drifted apart, two records in force contradict each other, a record the index omits, a pointer whose target is gone, content carrying no recorded author, a recurring audit timer fires.


---

### [event-capture](skills/event-capture/SKILL.md)

Write a trace — a dated note of one event, an event being a happening of a kind schema-resolution names, fixed once written — into the journal, where traces accumulate and stand unchanged, in the same stretch of work the event happens. A decision is made, a discovery lands, a failure is diagnosed, a commitment is entered, a delegation is issued, content arrives from elsewhere, the working text is condensed, a stretch of work starts or ends, "log this", "note what happened", "record that", "write it down".


---

### [init](skills/init/SKILL.md)

Read the two skills this system is entered by, follow every skill either one names to the end of the chain, and run the waking check. The start of a conversation, a project's governing file directing that a stretch of work opens here, "memento:init", "init", "start here", "orient", "load memento".


---

### [owner-ruling](skills/owner-ruling/SKILL.md)

Carry out a ruling — what the owner, the human whose project this is, rules about content in quarantine, the status that holds a record and strips its force; about a routine, a repeatable behavior the system may run; or about a scope, everything one project keeps under one owner: ratify it back into force, keep it as data that binds nothing, or retire it out of force and keep it. "review the quarantine", "rule on this", "ratify this", "should this routine run", "retire the scope", or the owner turning attention to anything held out of force.


---

### [pat-down](skills/pat-down/SKILL.md)

Re-derive what is true about a project from its written records, inheriting nothing. Session start, resumed or interrupted work, a compaction, "where was I", "orient yourself", "catch up", or any doubt about what still holds.


---

### [record-promotion](skills/record-promotion/SKILL.md)

Move a record — a written statement kept past its making — up one tier, a storage class in a fixed order, through that tier's gate, the check the tier demands before admitting anything. "verify this claim", "promote this", "make this a directive", "add this to the charter", "set the goal", "amend the goal", or any request to raise a record one tier.


---

### [record-writing](skills/record-writing/SKILL.md)

Write one record — a written statement kept on a durable location, made to outlast the work that wrote it. "write this down", "record this", "save this", "replace this record", "where does this go", or any write performed by event-capture, record-promotion, staging-relay, span-closure, corpus-reconciliation, or owner-ruling.


---

### [schema-resolution](skills/schema-resolution/SKILL.md)

Establish the one schema in force: the shape a project declares for its records — the written statements it keeps. Before a record is written, read, promoted, or audited; when a record's place or shape is in question; "which schema", "where does this go", "what kinds exist", "does this conform", or any doubt about the declared shape.


---

### [setup](skills/setup/SKILL.md)

Explain this memory system to the person whose project it is, place what that project already wrote into it, and write the configuration it runs on. First use in a project, "set up memento", "install memento", "configure memento", "what is this system", "start keeping memory for this project", or any request to explain or configure it.


---

### [skill-creation](skills/skill-creation/SKILL.md)

Create a skill — text to be read and followed. "create a skill", "write a skill", "new skill", "add a skill", "make this repeatable", or any request to turn a procedure into a reusable skill.


---

### [span-closure](skills/span-closure/SKILL.md)

Close out a stretch of work — one continuous thread of narrative — flushing, summarizing, and auditing what it leaves behind. The end of a stretch of work is signalled ahead of it: work completes, the person the work is for calls an end, notice arrives that the working text — the text in front of one right now — is about to be condensed, "close the session", "wrap up", "we're done here", "finish up", "before we stop".


---

### [staging-relay](skills/staging-relay/SKILL.md)

Pair every part of a task that outlives the work at hand with a record and a waking cause — what begins the later work — and bound every wait. A task outlives the work at hand, work is handed out, a wait begins, "set a reminder", "continue this later", "wait for X".


---

