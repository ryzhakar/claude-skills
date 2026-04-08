# Domain-Specific Context Examples

How to construct minimal context briefs for dev agents. These illustrate the parent skill's minimal context principle applied to common development scenarios.

## Cargo.toml Dependency Audit

**Minimal context:**
> "The project uses Leptos 0.8, Tailwind CSS v4 (standalone binary, no Node.js), and Postgres via sqlx. Read `/path/to/Cargo.toml`. For each dependency, note version and purpose. Check for version conflicts with the specified Leptos and sqlx versions."

**NOT:**
> "Here's the full project architecture [3000 words], the design system [2000 words], the coding conventions [1500 words]. Now check Cargo.toml."

## Tailwind v4 Compatibility Check

**Minimal context:**
> "Check if library X supports Tailwind v4. The project uses Tailwind v4 standalone (no Node.js, no tailwind.config.js). Fetch the library's documentation and check for Tailwind-related configuration."

**Key constraint:** Tailwind v4 standalone eliminates Node.js dependency — this is the critical compatibility criterion.

## Type Signature Verification (sonnet-level)

**Minimal context:**
> "Verify that library X's auth API is compatible with the project's user model. Read `/path/to/models/user.rs` and fetch library X's auth documentation. Check: does the library accept our User struct fields? Are return types compatible?"

**Why sonnet:** Reasoning about type signatures and API compatibility requires more than pattern-matching.
