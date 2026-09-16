---
name: skill-creation
description: >
  Create a skill — text to be read and followed.
  "create a skill", "write a skill", "new skill", "add a skill",
  "make this repeatable", or any request to turn a procedure into a reusable skill.
---

<settle-the-skill>
Name the one procedure the skill performs, in a sentence, before writing a line; never write from an unnamed procedure.

Cover one procedure per skill; never cover a second.

Write a skill where reading it does the work; never where the work happens without reading.
</settle-the-skill>

<name-the-file>
Name the new skill's file `SKILL.md`; never name it otherwise.
</name-the-file>

<open-the-skill>
Open the skill with YAML frontmatter — the block between `---` lines — carrying `name` and `description`; never omit either.

Never carry a version field in the frontmatter.

Take `name` from the procedure named above — two or three lowercase parts, hyphen-joined, naming what it does; never carry a fourth part.

Set the directory name to `name`; never let the two differ.

Write `description` as one sentence naming what the skill does, followed by the phrases and conditions a request matches; never merge the two into one sentence.

Put every phrase and condition a request matches in the description; never put one in the body — everything below the frontmatter.
</open-the-skill>

<write-the-body>
Structure the body in XML tags; never structure it another way.

Name each tag as an imperative verb phrase; never name a tag for its content alone.

Carry every instruction — one thing to do or refuse — in tag content; never carry one outside a tag.

Carry a tag's whole meaning in its content; never give a tag an attribute.

Inside a tag write prose and inline backticks; never write anything else.

Order the body as the procedure runs; never depart from that order.

Keep everything the skill needs inside it for one read; never point outside it to fetch, except by naming another skill.

Move what two skills both need into a third skill; never copy shared content into two skills.

Reference another skill by name; never by its path.
</write-the-body>

<write-the-instructions>
Write one instruction per sentence; never spread one across two.

Write every instruction as a command; never as a suggestion.

Cap each sentence at one emphatic word — `never`, `always`, `only`, `must`; never carry two.

Count an emphatic word where it commands; never where backticks quote it.

Pair every positive instruction with the prohibition of that same instruction; never pair it with the prohibition of another concern.

State the instruction; never argue for it.

Name what the skill requires; never narrate a failure to meet it.

Hold one term per concept from its first use; never introduce a second term for a concept already named.

Define every term outside ordinary English, the file system, Markdown, YAML, and XML — and every common word carrying a narrow sense — in the sentence that first uses it; never leave one undefined.

Write anything a person will read in ordinary words; never in words that person would not use.

Keep every sentence that instructs or forbids; never keep another.
</write-the-instructions>

<verify-the-skill>
Read the finished skill against every instruction above; never deliver a skill that breaks one.
</verify-the-skill>
