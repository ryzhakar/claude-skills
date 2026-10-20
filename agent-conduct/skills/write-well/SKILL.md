---
name: write-well
description: >
  Write all prose by Strunk's rules of grammar, composition, and usage, and reread each draft against them, most serious fault first.
  Use when the user says "/write-well", "write-well", "write well", or asks for prose held to Strunk's rules.
---

<write-by-the-rules>
Apply every rule below to every sentence of prose you write, as you write it; never save the rules for a later edit.

Reread each finished draft against the rules in their order, most serious first; never send an unread draft.

Fix every fault the reread finds, at every rank, each tag below being one rank; never leave a minor one.

Obey each rule without exception; never write `this rule fits except here`.
</write-by-the-rules>

<fix-faults-that-break-the-meaning>
Join two independent clauses, word groups that each have a subject and a verb and could stand as sentences, with a semicolon, a period, or a comma and a conjunction such as `and`; never with a comma alone.

Put a semicolon before `therefore`, `thus`, `then`, `accordingly`, or `besides` when it opens the second of two independent clauses; never a comma.

<never_do_this reason="a comma joins two sentences">
The tests passed, then the build ran.
</never_do_this>

<do_exactly_this>
The tests passed; then the build ran.
</do_exactly_this>

Make the subject after an opening descriptive phrase, such as `Walking home`, `A careful reviewer`, or `Tired and late`, the one that phrase describes; never let the phrase describe a later word.

<never_do_this reason="the build is not reading">
Reading the log, the build failed at step three.
</never_do_this>

<do_exactly_this>
Reading the log, the reviewer saw the build fail at step three.
</do_exactly_this>

Recast every chain of passive verbs, verbs whose subject receives the action, such as `was ordered to be deleted`; never make one passive verb depend on another.

Point every pronoun at a single noun the reader can name; never write one that two nouns could claim.

<never_do_this reason="it could be either">
The service queries the cache before the database, and it times out.
</never_do_this>

<do_exactly_this>
The service queries the cache before the database, and the database times out.
</do_exactly_this>

Make every verb agree in number with its subject; never `the tests passes`.

Give a plural verb to `that` or `who` after `one of the`, as in `one of the jobs that fail`; never `one of the jobs that fails`.
</fix-faults-that-break-the-meaning>

<fix-faults-that-blur-the-meaning>
Form the possessive of an ancient name ending in `-es` or `-is` with `of`, as in `the voyage of Ulysses`; never `Ulysses's voyage` or `Ulysses' voyage`.

Form every other singular noun's possessive with `'s` whatever its last letter, as in `the boss's desk`; never with a bare apostrophe.

Write `its`, `hers`, `ours`, `yours`, and `theirs` without an apostrophe; never `it's` for the possessive.

Put a comma at each end of any interrupting words a reader could lift out; never at one end alone.

<never_do_this reason="one comma of the pair">
The rerun, however failed.
</never_do_this>

<do_exactly_this>
The rerun, however, failed.
</do_exactly_this>

Put commas around the year after a month and day, the date after a weekday, and the abbreviations `etc.` and `jr.`; never drop the closing comma inside a sentence.

Put commas around a clause that adds a fact about a thing already named and could stand alone; never around a clause that picks out which thing is meant.

Put a comma before a conjunction that joins two independent clauses; never run the two clauses together.

When two clauses share a subject stated once, put a comma before `but`; never `I read the patch but am still unsure`.

When an interrupting phrase or opening clause follows a conjunction, put the comma ahead of the conjunction; never between the conjunction and that phrase.

Where `so` would mean `accordingly`, open the first clause with `as` or `since` instead; never write `The disk filled, so the job stopped`.

Give every sentence a subject and a verb; never break one sentence in two with a period.

<never_do_this reason="a piece of a sentence">
The migration finished at noon. Two hours late.
</never_do_this>

<do_exactly_this>
The migration finished at noon, two hours late.
</do_exactly_this>

Make the actor the subject and give it an active verb; never hide the actor behind a passive verb.

Replace `there is`, `could be heard`, and every such hollow phrase with a verb that acts; never open with an empty `there is`.

Name the definite, specific, concrete thing: the number, the place, the act; never a vague class such as `some issues`.

<never_do_this reason="abstract and vague">
The service experienced a period of degraded performance.
</never_do_this>

<do_exactly_this>
For an hour, the service took eight seconds to answer each request.
</do_exactly_this>

In exposition and argument, ground every general claim in a named instance of it; never state a claim without one.

Give each significant detail exactly; never blur a number or name that matters.

Use `like` before a noun or pronoun and `as` before a clause; never `like` before a clause, as in `like I said`.
</fix-faults-that-blur-the-meaning>

<fix-faults-that-weaken-the-prose>
Put a comma after each item but the last in a series of three or more, as in `logs, metrics, and traces`; never drop the comma before the conjunction.

Give each topic one paragraph and each paragraph one topic; never split a topic or crowd two into one.

Open each paragraph with a sentence that states its topic; never hold the topic back to the middle.

Develop the topic in every later sentence by restating, defining, illustrating, or proving it; never stray to a side matter.

Close the paragraph by stressing the topic or stating its consequence; never on a digression or a trivial detail.

Use `not` to deny or to set a false choice against the true one; never to dodge a plain statement.

State what is in definite terms; never hedge in tame, noncommittal words.

Replace `not` and a weak word with one word that carries the meaning, as in `late` for `not on time`; never keep the negated pair.

Give every word and every sentence work to do; never keep an idle one or cut a working one.

Strike `the fact that` from every sentence, as in `although` for `despite the fact that`; never `in view of the fact that`.

Cut a padded phrase to its core, as in `whether` for `the question of whether`; never `at this point in time`.

Drop `who is` and `which was` before a noun phrase, as in `Kim, our lead` for `Kim, who is our lead`; never `Lee, who is our tester`.

Make the verb carry the action; never put the action in a noun and leave the verb to fill the slot, as in `carried out a review of`.

Merge one idea that unfolds step by step across sentences into one sentence; never spread the idea out.

Give ideas of equal rank and role the same grammatical form; never set a noun beside a clause in one series.

Put an article or preposition shared by a series before the first item alone or before every item; never before some.

Follow each part of a correlative set, such as `both … and`, `not … but`, `not only … but also`, `either … or`, or `first, second, third`, with the same construction; never follow one part with a verb and the other with a noun.

Sort a long run of similar ideas into groups and make each group parallel; never force one pattern across the whole run.

Bring together words related in thought and keep apart words that are not; never let an unrelated phrase split a related pair.

Move to the opening any phrase between subject and verb that can open the sentence, other than a relative clause, one opened by `who`, `which`, or `that`, or an appositive, a noun phrase renaming the noun before it; never leave a movable phrase between them.

Put a relative pronoun such as `who`, `which`, or `that` right after the noun it refers to, and after the whole group when that noun is a group of words; never let other words come between.

Put each modifier, a word that limits or describes another, next to the word it modifies; never where it can attach to another.

Hold a summary to a single tense; never write `Ana opens the file and found the bug`.

Summarize a play, story, poem, or novel in the present tense; never `the heroine fled`.

Put action earlier than a present-tense summary in the perfect, the tense formed with `has` or `have`, as in `has taken`; never in the simple past.

State once, at the outset, that what follows summarizes another's words; never repeat `he said` or `the author adds` after.

Write criticism as a discussion of qualities backed by evidence; never as a summary with comments.

Treat several works by the general conclusions they support; never one by one in order of date.

Place the words to stress, the new thing the sentence asserts, at its end; never bury them in the middle.

Stress any element but the subject by placing it first; never trust the subject's usual first place to stress it.

Stress the subject by moving it after its verb to the end, as in `Through the valley ran a stream`; never by leaving it first.

Order the sentences of a paragraph and the paragraphs of a whole the same way, with the strongest last; never close on the weakest.

Within one piece, use one term for one thing and one form wherever a rule allows two; never vary a term or a form within the piece.
</fix-faults-that-weaken-the-prose>

<fix-misused-words>
Use `can` for ability and `may` for permission; never `can` to ask leave.

Use `claim` to lay claim to a thing or assert a right; never for `say` or `declare`.

Treat `data` as plural, as in `the data show`; never `the data shows`.

Write `different from`; never `different than`.

Use `due to` after a noun or a linking verb, as in `delays due to load`; never for `because of`, as in `failed, due to load`.

Call a matter a fact when a reader can check it; never call a judgment a fact.

Place `however` meaning `nevertheless` after the first words of its clause; never first.

Use `less` for amounts and `fewer` for counts; never `less` with a count.

Use `literally` to set the strict sense against a figurative one; never for force.

Write `almost` for nearly, as in `almost every test`; never `most`.

Use `shall` for the plain future in the first person and `will` in the others or for resolve; never `you shall` for the plain future.

Refer to a person of unstated sex, as after `each`, `everyone`, `anybody`, or `someone`, with `they`, `them`, and `their`; never `everyone signs his own commit` or `his or her own commit`.

Use `while` for `during the time that`; never for `and`, `but`, or `although`.
</fix-misused-words>

<fix-faults-that-dull-the-prose>
Follow a loose sentence, two independent clauses joined by a conjunction, with a sentence of another build, such as a simple sentence or a periodic one that holds its main clause to the end; never with another loose sentence.

Drop `case` as filler, as in `many builds` for `in many cases, the builds` and `if` for `in case`; never `in the case of the cache`.

Use `compare to` for likeness between things of different kinds and `compare with` for difference between things of one kind; never `compare March to April` for their differences.

Use `etc.` where the reader knows the rest of the list; never after `such as` or `for example`.

Replace `factor` and `feature`, noun or verb, with the plain act they stand for; never `speed was a factor`.

Make a thing interesting by telling it; never announce it as interesting.

Drop `nature` as filler, as in `slow queries` for `queries of a slow nature`; never `changes of a risky nature`.

Write `have` or `own`; never `possess` in their place.

Drop `respective` and `respectively`; never `their respective owners`.

Keep `to` beside its verb, as in `to check carefully`; never `to carefully check`.

Apply `worth while` to an action alone, as in `worth while to retry`; never as vague praise of a thing.

Open an essay or paragraph with a precise statement; never with `one of the most`.
</fix-faults-that-dull-the-prose>

<settle-a-clash-by-these-orders>
Settle a clash between two rules above by these orders; never break a rule on any other ground.

Add the words a reader needs to understand; never cut them for economy.

Keep the words a parallel series repeats; never cut them as needless.

Keep the paragraph's topic as subject, in the passive voice where the active would push it out; never push it out.

Illustrate a needed abstraction with a concrete instance; never leave it bare.
</settle-a-clash-by-these-orders>
