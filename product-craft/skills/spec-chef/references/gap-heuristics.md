# Gap Detection Heuristics

Patterns for identifying missing information in documentation.

## Table of Contents
- [Persona Gaps](#persona-gaps)
- [Behavior Gaps](#behavior-gaps)
- [Assumption Gaps](#assumption-gaps)
- [Edge Case Gaps](#edge-case-gaps)
- [Success Gaps](#success-gaps)
- [Scope Gaps](#scope-gaps)

---

## Persona Gaps

**Signal phrases:**
- "users can..."
- "the system allows..."
- "people will..."

**What's missing:** WHO specifically? What are their constraints? What do they already know?

**Questions to surface:**
- Who is the PRIMARY user? (not all users, the main one)
- What's their context when they arrive?
- What's their time budget?
- What's their technical skill level?
- Who is explicitly NOT a user? (anti-personas)

---

## Behavior Gaps

**Signal phrases:**
- "handles errors gracefully"
- "provides feedback"
- "notifies the user"
- "processes the data"

**What's missing:** HOW specifically? What does the user see?

**Questions to surface:**
- What exactly appears on screen?
- How long does it take?
- What if it fails?
- Can it be undone?
- What state is preserved?

---

## Assumption Gaps

**Signal phrases:**
- Technical choices without rationale
- "We'll use X" without why
- Architecture decisions as facts

**What's missing:** WHY this choice? What alternatives were rejected?

**Questions to surface:**
- Why this technology/pattern?
- What constraints drove this?
- What would change this decision?
- Is this revisitable or locked?

---

## Edge Case Gaps

**Signal phrases:**
- Happy path descriptions only
- "Users can do X" without failure modes
- No mention of limits or boundaries

**What's missing:** What happens when things go wrong?

**Questions to surface:**
- What if input is invalid?
- What if operation times out?
- What if user abandons mid-flow?
- What if system is under load?
- What if data is corrupted?
- What about abuse/spam?

---

## Success Gaps

**Signal phrases:**
- Feature lists without outcomes
- "Build X" without measuring success
- No completion criteria

**What's missing:** How do we know it worked?

**Questions to surface:**
- What's MVP vs nice-to-have?
- How do we measure success?
- What would make this a failure?
- When is "good enough" good enough?

---

## Scope Gaps

**Signal phrases:**
- Open-ended feature descriptions
- "And more..." or "etc."
- No explicit exclusions

**What's missing:** What are we NOT building?

**Questions to surface:**
- What's explicitly out of scope?
- What's deferred to later?
- What adjacent features are NOT included?
- Where does this system's responsibility end?

---

## Detection Technique

Read each section of documentation and ask:

1. **Could two engineers interpret this differently?** → Ambiguity gap
2. **Does this assume knowledge not stated?** → Assumption gap
3. **What questions would a new team member ask?** → Context gap
4. **What could go wrong that isn't mentioned?** → Edge case gap
5. **How would we demo this?** → Behavior gap
6. **Who decides if this is done?** → Success gap
