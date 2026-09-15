---
name: skill-creation
description: >
  Create a skill — written instructions to be read and followed.
  Triggers: "create a skill", "write a skill", "new skill", "add a skill",
  "make this repeatable"; or any request to turn a procedure into a reusable skill.
---

<settle-the-skill>
Name the one procedure the skill performs, in a sentence, before writing a line; never write from an unnamed procedure.

Cover one procedure per skill; never cover a second.

Write a skill for behavior that works by being read; never for behavior that acts without being read.
</settle-the-skill>

<place-the-skill>
Write the skill this procedure produces to `.claude/skills/<skill-name>/SKILL.md` in the project it serves — the directory the work lives in; never place that skill outside that path.
</place-the-skill>

<write-the-frontmatter>
Open the skill with YAML frontmatter carrying `name` and `description`; never omit either.

Never carry a version field in the frontmatter.

Take `name` from the procedure named above — two or three words naming what it does, lowercase and hyphen-joined; never carry a fourth.

Set the directory name to `name`; never let the two differ.

Write `description` in two parts — one sentence naming the behavior, then `Triggers:` followed by the phrases and conditions that fire the skill; never write it in another shape.

Put every trigger condition in the description; never put one in the body — everything below the frontmatter.
</write-the-frontmatter>

<write-the-body>
Structure the body in XML tags; never structure it another way.

Name each tag as an imperative verb phrase; never name a tag for its content alone.

Carry every instruction in tag content; never carry one outside a tag.

Carry a tag's whole meaning in its content; never give a tag an attribute.

Inside a tag write prose and inline backticks; never write anything else.

Order the body as the procedure runs; never depart from that order.

Keep everything the skill needs inside it for one read; never point outside it to fetch.

Move what two skills both need into a third skill; never copy shared content into two skills.

Reference another skill by name, which arrives loaded rather than fetched; never by its path.
</write-the-body>

<write-the-instructions>
Write one instruction per sentence; never spread one across two.

Write every instruction as a command; never as a suggestion.

Cap each sentence at one emphatic word — `never`, `always`, `only`, `must`; never carry two.

Count an emphatic word where it is used; never where it is named.

Pair every positive instruction with the prohibition of that same instruction; never pair it with the prohibition of another concern.

State the policy; never argue for it.

Name the behavior the skill requires; never narrate a failure to meet it.

Hold one term per concept from its first use; never introduce a second term for a concept already named.

Define every term outside ordinary English, the file system, Markdown, YAML, and XML — and every common word carrying a narrow sense — in the sentence that first uses it; never leave one undefined.

Write anything a person will read in ordinary words; never in words that person would not use.

Keep every sentence that instructs or forbids; never keep another.
</write-the-instructions>

<verify-the-skill>
Read the finished skill against every instruction above; never deliver a skill that breaks one.
</verify-the-skill>
