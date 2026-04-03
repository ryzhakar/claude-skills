# Terminology Extraction Protocol

Optional pre-step before gap detection. Use when working with complex business domains,
domain experts, or documentation where the same concept appears under multiple names.

## When to Run This

- Starting from documentation authored by multiple people
- Domain has industry-specific jargon or overlapping terms
- Stakeholders use different words for the same concept
- Prior conversations show terminology confusion

Skip when the domain is well-understood and vocabulary is already consistent.

## Extraction Process

### 1. Scan for Domain Terms

Read existing documentation and conversation history. Collect:

- **Nouns**: entities, actors, artifacts, states (Order, Customer, Invoice, Draft)
- **Verbs**: actions, transitions, operations (submit, approve, fulfill, cancel)
- **Concepts**: abstract ideas, rules, policies (eligibility, escalation, SLA)

Focus exclusively on domain terms. Skip programming concepts (array, endpoint, handler)
unless they carry domain-specific meaning.

### 2. Identify Ambiguities

Flag three categories of problems:

| Problem | Example | Risk |
|---------|---------|------|
| Same word, different concepts | "account" = Customer AND User | Specs describe wrong entity |
| Different words, same concept | "purchase", "order", "transaction" | Inconsistent specs, duplicated logic |
| Vague or overloaded terms | "process the request", "handle the data" | Undefined behaviors slip through |

### 3. Propose Canonical Glossary

For each concept, select ONE canonical term and list aliases to avoid:

| Term | Definition | Aliases to Avoid |
|------|-----------|-----------------|
| **Order** | A customer's request to purchase items | Purchase, transaction, request |
| **Customer** | A person or org that places orders | Client, buyer, account |

Rules for term selection:
- Pick the term domain experts use most naturally in conversation
- One sentence definition — what it IS, not what it does
- Be opinionated: pick one winner, list the rest as aliases to avoid

### 4. Express Relationships

State how terms relate with explicit cardinality:

```
- An **Invoice** belongs to exactly one **Customer**
- An **Order** produces one or more **Invoices**
- A **User** may or may not represent a **Customer**
```

### 5. Write the Artifact

Create `UBIQUITOUS_LANGUAGE.md` in the project root with:

- **Grouped term tables** — cluster by subdomain, lifecycle stage, or actor type
- **Relationships section** — cardinality and ownership between terms
- **Flagged ambiguities** — terms used inconsistently with resolution recommendations
- **Example dialogue** — 3-5 exchanges between dev and domain expert demonstrating
  precise term usage and clarifying concept boundaries

### 6. Index the Artifact

Add a reference to the glossary in CLAUDE.md or equivalent project index so future
sessions can find and update it.

## Updating an Existing Glossary

When re-running after new conversations:

1. Read the existing `UBIQUITOUS_LANGUAGE.md`
2. Add new terms discovered in subsequent discussion
3. Update definitions where understanding has evolved
4. Re-flag new ambiguities
5. Revise example dialogue to incorporate new terms
