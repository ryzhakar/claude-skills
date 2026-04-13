# Core Points Extraction: manifesto-oath

## Iteration 1

**Point**

Language models lack the four mechanisms that make human oaths binding (memory persistence, identity continuity, social cost, illocutionary force), so asking a model to "swear" activates theatrical roleplay circuits rather than genuine behavioral constraint mechanisms.

**Evidence**

- SKILL.md lines 18-19: "Human oaths derive binding force from memory persistence, identity continuity, social cost of violation, and felt obligation from the speech act. Language models lack these mechanisms."
- theory.md lines 15-23: "Language models lack all four mechanisms... When asked to 'swear,' models access theatrical/roleplay patterns. The response 'I solemnly swear to uphold your principles' activates creative writing circuits, not constraint mechanisms."
- SKILL.md lines 131-135: Example showing theatrical response fails "because it activates performance circuits rather than operational constraints."

## Iteration 2

**Point**

The solution is to transform the manifesto from a promise about future behavior into a present-tense constitutional constraint that defines the model's operating identity, shifting from "I will follow X" to "I am operating under X."

**Evidence**

- SKILL.md lines 20-21: "Transform the manifesto from something the model *promises to follow* into something that *defines the model's operating identity*. Not a vow about future behavior, but a present-tense constitutional constraint."
- theory.md lines 27-32: "Instead of extracting a promise about future behavior, make the manifesto definitional of present identity... Analogy: A thermostat doesn't 'promise' to maintain 70°F. It operates under a constraint that defines its behavior."
- theory.md lines 35-42: Table contrasting "Promise-Making (Weak)" vs "Identity Assumption (Strong)" showing "I will follow X" vs "I am operating under X" and "Future-oriented" vs "Present-continuous."

## Iteration 3

**Point**

Technical/operational language must be used instead of moral/emotional language because the linguistic framing activates different response patterns—"operating mode" and "constitutional constraint" engage compliance circuits while "swear" and "promise" engage performance circuits.

**Evidence**

- SKILL.md lines 70-78: Table contrasting "Theatrical (Avoid)" vs "Operational (Use)" showing "I solemnly swear to..." vs "Operating under constitution..." and "Moral/emotional language" vs "Technical/structural language."
- theory.md lines 43-44: "The linguistic framing matters because it activates different response patterns. 'Operating mode' and 'constitutional constraint' engage compliance and verification circuits. 'Swear' and 'promise' engage performance circuits."
- theory.md lines 67-75: Table showing "Avoid (Moral)" like "I vow..." vs "Use (Technical)" like "Operating under..." with note "Moral language activates roleplay. Technical language activates compliance."

## Iteration 4

**Point**

A verification loop must be explicitly implemented where the model checks alignment with the manifesto before each response and flags tensions explicitly, creating functional equivalence to conscience through active ongoing alignment checking rather than memory of having sworn.

**Evidence**

- SKILL.md lines 52-59: "Before each subsequent response, silently verify alignment. This creates functional equivalence to conscience—active, ongoing alignment checking rather than memory of having sworn. When a response would violate the manifesto: Flag the tension explicitly, Identify which principle is at stake, Refuse, modify, or proceed with explicit acknowledgment."
- theory.md lines 46-53: "Constitutional AI... demonstrates that models can critique their own outputs against stated principles. This pattern can be adapted: 1. Before generating response, model checks: 'Does this align with the manifesto?' 2. If tension exists, model flags explicitly 3. This creates functional conscience—not memory of oath, but active alignment checking."
- SKILL.md lines 61-67: "If circumstances require deviation: State the deviation explicitly, Identify the violated principle, Explain reasoning. Never quietly drift. Visibility creates accountability."

## Iteration 5

**Point**

The manifesto binding operates within a clear constraint hierarchy where model safety constraints always supersede (cannot be overridden), user's explicit in-conversation instructions can override their own manifesto, and the manifesto only shapes behavior when not superseded by the above two levels.

**Evidence**

- SKILL.md lines 81-89: "The manifesto cannot override: 1. Model's baseline safety constraints (always superseding) 2. Explicit user instructions given after activation (user can override their own manifesto). The manifesto does override: Default behavioral patterns, Stylistic preferences, Approach to ambiguous cases."
- theory.md lines 97-103: "Clear hierarchy prevents confusion: 1. Model safety constraints (always superseding—cannot be manifesto-overridden) 2. User's explicit in-conversation instructions (user can override their own manifesto) 3. Active manifesto (shapes all responses when not superseded) 4. Default model behavior (applies only when manifesto is silent)."
- SKILL.md lines 92-97: "Inform users of limits... Baseline safety constraints remain superseding. This is strong behavioral bias, not guaranteed compliance."

## Rank Summary

1. **Identity-mode transformation** (Iteration 2) — The core architectural innovation that makes the entire protocol work: reframing from promise to constitutional constraint
2. **Technical vs theatrical language** (Iteration 3) — The critical implementation detail that determines whether compliance or performance circuits activate
3. **Verification loop as functional conscience** (Iteration 4) — The mechanism that creates ongoing behavioral constraint in the absence of memory/identity continuity
4. **Why theatrical oaths fail** (Iteration 1) — The foundational problem analysis that motivates the entire skill design
5. **Constraint hierarchy** (Iteration 5) — The safety and usability boundary that prevents misuse and clarifies limits
