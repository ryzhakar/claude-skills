---
name: schema-resolution
description: >
  Establish the one schema in force: the shape a project declares for its records — the
  written statements it keeps.
  Before a record is written, read, promoted, or audited; when a record's place or shape
  is in question; "which schema", "where does this go", "what kinds exist", "does this
  conform", or any doubt about the declared shape.
---

<settle-the-scope>
Resolve a schema for one scope — one project, holding one human owner, one goal set (what the project pursues), one charter (the project's governing file, loaded at every start), one set of records, and one schema; never stretch a scope across two projects.

Hold exactly one schema in force over a scope; never hold a second beside it.
</settle-the-scope>

<resolve-the-schema-in-force>
Follow the chain of pointers starting at the one the charter holds — a pointer being a record whose content is another record's home — reading each target in turn and following any pointer that target holds; never stop on a target that holds a pointer.

Take the schema that chain reaches as the schema in force; never read another source once that schema is in hand.

Count a missing or unreadable target as a chain reaching no schema; never stop the resolution on one.

Read the project's configuration file at `.claude/memento.yaml` when the chain reaches no schema; never look elsewhere for a project's own schema.

Take the shipped default — the schema at `config/default.yaml` in this plugin — when the project has no configuration file; never treat a missing configuration file as a missing schema.

Take the whole of whichever source answers first; never merge two sources.

Let a project's configuration file replace the shipped default outright; never fill a gap in one source from another.
</resolve-the-schema-in-force>

<take-the-schema-as-declared>
Read five declarations from the schema in force: the record kinds a scope admits, each with the one home its records live in and the tier — the storage level — holding them; the event kinds a scope writes down as they happen; the depth of checking a kind's content passes before it stands; the form a record's kind takes — how a record states which kind it is; and the form a record's provenance takes — how a record states where it came from; never read in a shape the schema leaves undeclared.

Find the schema's own kind, home, and tier declared beside every other kind; never place the schema outside what it declares.

Let the pointer in the charter bring the schema along with it; never copy the schema's content into that file.

Take the schema as the owner's own declaration; never author one in the owner's place.

Amend the schema on the owner's word; never amend it otherwise.

Record what each amendment replaced; never leave it unrecorded.
</take-the-schema-as-declared>

<check-every-record-against-the-schema>
Read a record's kind by the kind form the schema declares; never take a record's kind from anywhere else.

Check a record on three points: that its kind is one the scope admits, that it sits at the home that kind gives, and that its provenance matches the declared form; never pass a record on fewer.

Leave the event kinds to `event-capture` and the checking depth to `record-promotion`; never apply either declaration here.
</check-every-record-against-the-schema>

<stop-the-check-at-the-shipped-default>
Count a project's configuration file among a scope's records; never leave one outside them.

Take a configuration file's own kind, home, and provenance form from the shipped default; never take them from that configuration file itself.

Resolve the schema in force before a configuration file's own check; never hold resolution for that check.

Keep the shipped default outside a scope's records; never count it as one.

Check the shipped default against nothing; never search for a schema behind it.
</stop-the-check-at-the-shipped-default>
