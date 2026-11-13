# Example: Awesome-Leptos Ecosystem Research

Condensed transcript of a full research-tree execution against the awesome-leptos ecosystem for the Саме Те Mail Club project (Leptos 0.8 / Axum / Postgres / Tailwind CSS v4).

**Research question:** "Which libraries from the awesome-leptos index should this project adopt, with special interest in Tailwind-compatible component libraries?"

---

## Setup

```
research/awesome-leptos/
├── index.md
├── categories/ (6 reports)
├── deep-dives/ (14 reports)
└── synthesis/recommendations.md
```

## index (1 haiku agent)

Fetched `https://github.com/leptos-rs/awesome-leptos` README. Parsed into structured index: 10 categories, 98 entries.

Orchestrator read ONLY the last 20 lines (statistics + category list) to plan `survey` fan-out.

## survey + ground-truth (9 haiku agents, parallel)

**Category surveyors (6 agents):**
- Styling and Design → 7 entries assessed
- Components → 7 entries assessed
- Libraries → 34 entries assessed (largest category)
- Quality of Life → 2 entries assessed
- Tools → 6 entries assessed
- Lower-priority (Resources, Templates, Macros, Blogs) → 42 entries combined

**Project auditors (3 agents):**
- UI audit → 19 components, 11 server functions, 11 CSS classes, 134 i18n keys, 9 pain points ranked
- Dependency audit → Leptos 0.8.17 pinned, full dep tree, version constraints mapped
- Architecture audit → 26 server functions, 7 routes, auth system, 56 E2E tests, 10 DX gaps ranked

All 9 agents launched in one message. Completed in ~2.5 minutes wall time.

**survey results (from completion summaries, not full reports):**
- ADOPT candidates: tracing-subscriber-wasm, leptos_i18n (already adopted)
- EVALUATE candidates: leptos-struct-table, leptix, leptosfmt
- Notable: all Tailwind component libraries either imposed design opinions or were archived

## verify (10 haiku agents, parallel)

**Candidate verifiers (4 agents):**
- leptos_i18n → VERIFIED: already adopted, v0.6.1, Leptos 0.8 exact match
- tracing-subscriber-wasm → VERIFIED: 8 lines integration, exact dep match, framework-agnostic
- leptos-struct-table → DEFER: Tailwind v4 token integration untested, current tables adequate
- leptix → SKIP: not headless (injects CSS), 40 downloads, "no guarantees"

**Breadth expansion (2 agents):**
- crates.io scan found ~400 leptos crates; 6 high-signal unlisted finds
- Production deps inspection (5 Leptos+Tailwind sites): zero use a component library

**New find verifiers (3 agents):**
- leptos_query (47.5K downloads) → SKIP: pinned to Leptos 0.6, incompatible
- leptos_ui → SKIP: class-merging macro, not a component library
- biji-ui → DEFER: 25+ headless components but too early for this project

**Tailwind component lib deep search (1 agent):**
- Found cloud-shuttle/radix-leptos: claimed 57+ headless primitives, v0.9, Leptos 0.8

All 10 agents launched in one message. Completed in ~2.5 minutes.

## resolve (2 haiku agents)

**Contradiction detected:** Components surveyor said "Rust Radix archived Feb 2, 2026." Tailwind search agent said "radix-leptos has 57+ primitives, production-ready."

**Resolution:** Both correct — different projects. RustForWeb/radix (multi-framework) = archived. cloud-shuttle/radix-leptos (Leptos-only) = active.

**Follow-up deep-dive on radix-leptos:**
- VERIFIED: v0.9, Leptos 0.8.8, 57+ headless components, 1865 tests
- BUT: `disabled` prop takes `bool` not `Signal<bool>` → breaks hydration gate pattern
- DataTable component disabled due to compile errors
- VERDICT: DEFER — ActionForm integration risk too high for current project

## synthesize (1 sonnet agent)

Read all 21 reports. Produced final recommendations:

**ADOPT NOW (1):** `tracing-subscriber-wasm` — 8 lines, fills WASM observability gap

**ALREADY ADOPTED:** `leptos_i18n` — no action needed

**EVALUATE:** `leptosfmt` (30-min POC), `radix-leptos` (future phases only)

**Component library answer: No.** Every candidate has a disqualifying problem. Production evidence confirms: zero of 5 real Leptos SSR sites use a component library. More valuable than any adoption: three internal refactors eliminating ~150 lines of boilerplate.

---

## Metrics

| Metric | Value |
|--------|-------|
| Total agents launched | 22 |
| Haiku agents | 21 |
| Sonnet agents | 1 (synthesis only) |
| Reports produced | 21 |
| Entries assessed | 98 (awesome-list) + ~50 (crates.io expansion) |
| Wall time (estimated) | ~15 minutes across all phases |
| Orchestrator context consumed | Minimal — task notifications and phase-transition decisions only |
| Contradictions detected | 1 (resolved) |
| ADOPT recommendations | 1 (tracing-subscriber-wasm) |
| Libraries eliminated | ~140+ |

## Lessons Learned

1. **The ungrounded synthesis was premature.** An initial synthesis without project audits produced generic recommendations. The grounded synthesis (after all phases) was materially different.
2. **Haiku hallucinated once.** The crates.io search agent reported download counts that were plausible but couldn't be independently verified. The `resolve` phase caught the important one (Radix).
3. **Breadth expansion found the most significant candidate** (radix-leptos) that wasn't on the awesome list. Without breadth expansion, the synthesis would have concluded "no headless option exists."
4. **Production deps inspection was the strongest signal.** Knowing that zero production sites use a component library grounded the "don't adopt one" recommendation more convincingly than any individual library assessment.
5. **Project audits changed the recommendations.** The UI audit revealed that pain points were minor boilerplate (hydration gates, form fields), not missing components. This shifted the advice from "find a library" to "extract three internal helpers."
