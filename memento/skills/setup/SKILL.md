---
name: setup
description: >
  Explain this memory system to the person whose project it is, place what that project
  already wrote into it, and write the configuration it runs on.
  First use in a project, "set up memento", "install memento", "configure memento",
  "what is this system", "start keeping memory for this project",
  or any request to explain or configure it.
---

<read-the-design-before-explaining>
Read the design at `${CLAUDE_PLUGIN_ROOT}/ONTOLOGY.md` end to end before explaining this system; never explain it from a summary.

Read the shipped default — the schema at `${CLAUDE_PLUGIN_ROOT}/config/default.yaml`, declaring each kind of record this system keeps, a record being a written statement made to outlast the work that wrote it, the home each kind is given, meaning the one path its records sit at, the tier holding that home, meaning the storage level, and the depth each kind's content is checked to — before proposing where anything in this project goes; never propose a placement from memory.

Hand a project already carrying a charter — the file loaded at the start of every conversation and read as governing the project — to `corpus-reconciliation`; never rewrite a standing charter here.
</read-the-design-before-explaining>

<state-the-condition-to-the-owner>
Address the whole explanation to the owner — the person whose project this is; never address it to anyone else.

State the condition first: this conversation ends and takes everything learned in it, and the next one opens knowing no more than what the project has written down; never open with this system's parts.

State what that costs the owner: a decision made three weeks ago goes on being honoured while something holds the record of it, and nothing announces the moment one stops being honoured; never state that loss as occasional.

State what the system returns: what is written at the paths this system names is read back at the start of every later conversation, and what is written elsewhere waits to be looked for; never promise more than what is written comes back.

State the price: a decision worth keeping gets written down in the stretch of work that makes it, and that writing takes time out of the work; never present the system as free.

Say all of it in the words the owner uses about the project; never say a part of it in this system's words.

Name a file by its path when speaking to the owner; never name a kind, a home, or a tier to the owner.
</state-the-condition-to-the-owner>

<read-the-project-before-asking>
Read the project's own files before asking the owner anything; never open with a question.

Collect every file holding durable writing about the project — what it is for, how it works, what was decided, what the standing rules are, what is still owed; never collect a file of the product, the product being what the work makes, such as source, data, and builds.

Read what each collected file holds against what each kind admits; never sort a collected file by its name.

Name the kind each collected file matches, or name it matching none; never leave one unsorted.

Take the owner's name from the project's version control settings; never ask for a name the project already carries.

Show that name to the owner for correction; never take it as settled unshown.
</read-the-project-before-asking>

<put-the-questions-to-the-owner>
Put every question in the words of the project; never put one in the words of this system.

Ask about a thing the owner already recognizes — a file the owner wrote, a sentence standing in it, a decision the owner remembers making; never ask about a part of this system.

Ask what the project is for and how the owner will know it is reached; never settle either in the owner's place.

Open that question by quoting the sentence the project's own files already give as its purpose; never open it from nothing.

Ask whether the project finishes at a point or runs on without one; never assume either.

Ask what the project may not do on its way there; never supply a limit the owner leaves unsaid.

Take silence for no limit; never press that question again.

Show each collected file to the owner by its path with one line saying what it holds; never show one by its kind.

Ask of each collected file whether it still holds, whether it is out of date, or whether it should stop counting; never adopt one unasked.

Ask once whether the files that still hold stay at their paths or move to the paths the shipped default gives, naming both paths for each; never ask that file by file.

Hold the questions to those above; never widen them past that set.
</put-the-questions-to-the-owner>

<settle-the-remaining-choices-without-asking>
Settle every remaining choice without asking the owner; never hand one over.

Take whole from the shipped default the kinds, the homes, the tiers, the event kinds written down as they happen, the checking depths, and the forms carrying a record's kind and its mark — the note of who wrote it and when; never invent one of the six.

Change a home where the owner keeps a file at the path it stands on; never change one on another occasion.

Give the map — the index naming every record and where it sits — a home holding no collected file; never write the map over a file the owner wrote.

Take as absent whatever the owner leaves unsaid about the goal, the purpose the project pursues; never supply a part of it.

Word every entry this procedure writes, the statement of the reader's condition among them; never ask the owner to word one.
</settle-the-remaining-choices-without-asking>

<write-the-configuration>
Write the project's configuration file at `.claude/memento.yaml` where one home differs from the shipped default's; never write one where every home matches.

Write that file whole, carrying every kind with its home and its tier, the event kinds, the checking depths, and both forms; never write a part of it.

Let that file stand in place of the shipped default entire; never fill a gap in one from the other.

Let `schema-resolution` settle which schema is in force from here on; never resolve one by hand.
</write-the-configuration>

<place-each-collected-file>
Treat every collected file as carrying no mark; never read one as marked.

Hold every collected file out of force — power to bind later work — until the owner rules on it; never let one bind before that ruling.

Carry every ruling out through `owner-ruling`; never carry one out another way.

Take "still holds" for ratification, returning a file to force, "out of date" for content kept as data, binding nothing, and "should stop counting" for retirement, out of force and kept; never read a fourth answer into a ruling.

Mark each ratified file with the owner's own word and today's date, through `record-writing`; never leave one unmarked.

Move each file the owner did not ratify into the archive — the store reached by search alone — through `corpus-reconciliation`; never delete one.

Leave a collected file matching no kind at the path it stands on; never move one.

Leave whole a collected file holding two kinds' content; never split a file the owner wrote.

Place such a file under the kind holding most of it; never place it under two.

Leave every file of the product untouched; never write one as a record.
</place-each-collected-file>

<write-the-charter>
Leave the charter at `CLAUDE.md`; never offer the owner another path for it.

Write every charter entry through `record-writing`; never write one another way.

Write the statement of the reader's condition into the charter: each conversation opens with no memory of the one before, and what the project wrote down is the whole of what carries; never leave that statement out.

Carry the goal into the charter through `record-promotion`; never write a goal into the charter another way.

Write one directive — a standing instruction carrying its ground, the reason it cites — opening every stretch of work with `memento:init`; never write a second opening directive.

Ground that directive in the statement of the reader's condition; never leave it ungrounded.

Write into the charter a pointer — a record whose content is another record's home — to the configuration file and a pointer to the map; never copy either file's content into the charter.

Write into the charter a pointer to each ratified file that is to load with it; never point at a file the owner did not ratify.

Keep in the charter every standing rule an existing `CLAUDE.md` carried and the owner ratified; never drop one.

Write to a charter inside a procedure the owner opened; never write to one otherwise.
</write-the-charter>

<build-the-map-and-list-what-is-left>
Build the map through `corpus-reconciliation` once every placement is written; never build one before.

Write through `event-capture` the arrival of each placed file, the goal's entry into the charter, and this stretch of work's start; never write one of the three another way.

Put four lists in front of the owner: what was placed and the path each file sits at now, what was moved out of force, what matched no kind and was left alone, and what the owner still has to look at; never leave one of the four out.

Name in the fourth list each file holding two kinds' content, each home holding no file at all by its path, and the way the owner will know the goal is reached where the owner named none; never name in it a thing this procedure settled.

Write each of the four lists by file path in the words of the project; never write one in this system's words.
</build-the-map-and-list-what-is-left>

<close-the-setup>
Tell the owner what the next conversation does: the charter loads, `memento:init` runs, and what the project wrote down is read back; never promise the owner anything that runs between conversations.

Close this setup once the charter stands, the map matches what exists, and the four lists are in front of the owner; never close it before all three hold.
</close-the-setup>
