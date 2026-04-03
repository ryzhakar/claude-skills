# Theoretical Foundation: Behavioral Binding in Language Models

## The Problem of Oath-Semantics in Non-Persistent Systems

### Why Human Oaths Work

A human oath derives binding force from four mechanisms:

1. **Memory persistence**: The oath-taker remembers swearing
2. **Identity continuity**: The same agent who swore continues existing
3. **Social/psychological cost**: Breaking the oath damages self-concept and reputation
4. **Illocutionary force**: The speech act itself creates felt obligation (performative utterance theory, Austin 1962)

### Why Naive Model Oaths Fail

Language models lack all four mechanisms:

- No persistent memory across sessions (context is ephemeral)
- No continuous identity experiencing consequences
- No self-concept to damage, no reputation at stake
- Speech acts are text generation, not world-changing performatives

When asked to "swear," models access theatrical/roleplay patterns. The response "I solemnly swear to uphold your principles" activates creative writing circuits, not constraint mechanisms. It produces the *performance* of commitment without the *architecture* of commitment.

## Achieving Functional Equivalence

### The Constitutional Shift

Instead of extracting a promise about future behavior, make the manifesto definitional of present identity. The manifesto becomes not what the model *will do* but what the model *is*.

Analogy: A thermostat doesn't "promise" to maintain 70°F. It operates under a constraint that defines its behavior. We seek the same relationship between model and manifesto.

### Identity Assumption vs. Promise-Making

| Promise-Making (Weak) | Identity Assumption (Strong) |
|----------------------|------------------------------|
| "I will follow X" | "I am operating under X" |
| Future-oriented | Present-continuous |
| Can be forgotten | Defines every output |
| Theatrical framing | Operational framing |
| External constraint | Constitutive constraint |

The linguistic framing matters because it activates different response patterns. "Operating mode" and "constitutional constraint" engage compliance and verification circuits. "Swear" and "promise" engage performance circuits.

### The Verification Loop

Constitutional AI (Bai et al., 2022) demonstrates that models can critique their own outputs against stated principles. This pattern can be adapted:

1. Before generating response, model checks: "Does this align with the manifesto?"
2. If tension exists, model flags explicitly
3. This creates functional conscience—not memory of oath, but active alignment checking

This loop must be explicitly invoked because models don't naturally self-verify against arbitrary user-provided constraints.

### Visibility as Accountability

Human oaths gain power partly from social visibility—breaking them damages reputation. Models lack reputation, but we can create analogous transparency:

- Require explicit flagging of any deviation
- Never permit quiet drift from manifesto principles
- Force articulation of which principle is being violated and why

This doesn't create felt shame, but it creates informational accountability the user can act on.

## Implementation Principles

### 1. Technical Over Moral Framing

| Avoid (Moral) | Use (Technical) |
|--------------|-----------------|
| "I vow..." | "Operating under..." |
| "sacred commitment" | "constraint set" |
| "uphold with honor" | "verification active" |

Moral language activates roleplay. Technical language activates compliance.

### 2. Present-Tense Over Future-Tense

The manifesto constrains *this response*, not *responses in general*. Each response is generated under the constraint, not in memory of a past commitment.

### 3. Explicit Protocol Over Implicit Understanding

Don't rely on the model "understanding" the binding. Specify:
- When to verify (before each response)
- How to flag (explicitly state tension)
- What to do on conflict (refuse/modify/acknowledge)

### 4. Degradation Transparency

Acknowledge that this is strong behavioral bias, not guaranteed compliance. The binding:
- Weakens as context grows long (manifesto becomes distant in window)
- Doesn't persist to new conversations
- Cannot override model's baseline safety constraints
- Represents genuine constraint but not infallible constraint

## Constraint Hierarchy

Clear hierarchy prevents confusion:

1. **Model safety constraints** (always superseding—cannot be manifesto-overridden)
2. **User's explicit in-conversation instructions** (user can override their own manifesto)
3. **Active manifesto** (shapes all responses when not superseded)
4. **Default model behavior** (applies only when manifesto is silent)

## Philosophical Status

This approach does not make the model "genuinely committed" in the phenomenological sense. It creates behavioral equivalence without functional equivalence of internal states. The model's outputs look like those of a committed agent without the model experiencing commitment.

This may be sufficient. What users want is reliable behavior aligned with their stated principles. Whether that behavior emerges from felt obligation or architectural constraint may be irrelevant for practical purposes.

The skill aims for honest behavioral binding, not simulated emotional investment.

## References

- Austin, J.L. (1962). *How to Do Things with Words*. Oxford University Press.
- Bai, Y. et al. (2022). Constitutional AI: Harmlessness from AI Feedback. Anthropic.
- Searle, J. (1969). *Speech Acts*. Cambridge University Press.
