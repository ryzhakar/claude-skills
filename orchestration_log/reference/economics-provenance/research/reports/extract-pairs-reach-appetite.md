# Reach and appetite by model and effort

## Binding

- first-principles (114 lines, whole): I must check each figure against its source atom (unit, caption, file, line), and I will not carry a figure from one effort level, site or suite to another by analogy.
- cargo-cult-science (89 lines, whole): I must not fool myself, and I will report every cell that disagrees with the anchor check and every empty cell, never an interpolated or remembered number.
- stop-yapping (131 lines, whole): I must write cells and fragments, and I will not pad the report with preamble, hedging or restatement.
- oath skill: 126 lines, whole; counts by `wc -l`; binding sent to `main` and `team-lead` before any input opened. `docs/conventions.md` read from the copy loaded into this session, not re-read from disk.

## Sources

Paths under `recon/2026-10-24/scratch/research-model-capability-and-effort/` unless a URL.

| file | what | date | who measured |
|---|---|---|---|
| `haiku55-charts.tsv`, `-announce.txt` | Haiku 5.5 announcement chart points (aria-labels, extracted by `charts.py` from `raw-haiku55`) and page text | 2026-10-07 (announce:13) | Anthropic; GDPval-AA scores credited to Artificial Analysis |
| `sonnet55-charts.tsv`, `-announce.txt` | Sonnet 5.5 announcement, same form | 2026-09-28 (announce:13) | Anthropic ("see the Sonnet 5.5 System Card", announce:71) |
| `opus55-charts.tsv`, `-announce.txt` | Opus 5.5 announcement, same form | 2026-09-22 (announce:12) | Anthropic; WANDR run offline with a 980k-token budget (announce:241) |
| `fable52-charts.tsv`, `-announce.txt` | Fable and Mythos 5.2 announcement, same form | 2026-11-09 (announce:15) | Anthropic |
| `about-claude-models-optimizing-for-cost-and-intelligence.md` | Anthropic docs, cost and intelligence; effort tables and run references | runs 2026-09-19 to 2026-11-04 (refs 3, 7, 8) | Anthropic |
| `aa-claude-fable-5-1` | Artificial Analysis model page; its page data holds 27 Claude records, every effort of the four models, parsed as JSON by `extract-pairs-reach-appetite/aarec.py` | fetched 2026-11-12 15:01 (mtime); release dates in records | Artificial Analysis, Anthropic first-party endpoint (`performanceDataSource`) |
| `aa-artificialanalysis-ai-methodology-intelligence-benchmarking` | AA Intelligence Index v5.0.1 suite table: tasks, repeats, scoring, weights | "Version 5.0.1 November 2026 to current" | Artificial Analysis |
| `reports/verify-spend-model-figures.md` | independent check, anchors D3, F8, N0 | 2026-11-12 | sibling agent |
| openrouter.ai/compare/anthropic/claude-opus-5.5/anthropic/claude-sonnet-5.5 | Throughput (p50), provider Anthropic | "Benchmark data updated Nov 4, 2026"; fetched 2026-11-12 | OpenRouter |
| openrouter.ai/compare/anthropic/claude-haiku-5.5/anthropic/claude-fable-5.2 | same | "updated Nov 10, 2026"; fetched 2026-11-12 | OpenRouter |

Anchors: every cell the check confirmed matches mine (SWE-bench Pro rows of D3 at cost doc :374, :434-437; Terminal-Bench 4.0 points of F8; AA output-token counts of N0, now paired from parsed records, not adjacency). No disagreement.

## Reach

Effort names: announcement charts print Low/Med/High/Xhigh/Max; the cost doc `low`/`high`; AA slugs `-low`, `-high`, and the bare slug for max (shortName "(max)"). Mapping is by name; Med and Xhigh dropped; nothing interpolated. "Stand-in" rows are Fable 5.1 where the source has no Fable 5.2 series.

Publisher charts (score as printed; dollar beside it, labelled by the chart's x-axis; `(:n)` = TSV line):

| benchmark | model | file | low | high | max | y-axis / x-axis label |
|---|---|---|---|---|---|---|
| Terminal-Bench 4.0 | Haiku 5.5 | haiku55-charts.tsv | 12.7% $0.42 (:44) | 24.8% $1.04 (:46) | 39.2% $2.64 (:48) | "Score (pass@1, %)" / "Cost per attempt (USD, log scale)" |
| Terminal-Bench 4.0 | Sonnet 5.5 | sonnet55-charts.tsv | 20.0% $0.76 (:1) | 43.0% $1.94 (:3) | 70.6% $12.54 (:5) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| Terminal-Bench 4.0 | Opus 5.5 | opus55-charts.tsv | 38.5% $1.29 (:1) | 64.2% $3.88 (:3) | 64.8% $11.24 (:5) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| Terminal-Bench 4.0 | Fable 5.1 (stand-in) | opus55-charts.tsv | 40.2% $5.70 (:6) | 49.4% $10.50 (:8) | 55.8% $19.50 (:10) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| FrontierCode v1.1, main set | Sonnet 5.5 | sonnet55-charts.tsv | 29.3% $0.19 (:21) | 49.4% $0.42 (:23) | 46.2% $20.78 (:25) | "Score (%)" / "Cost per task (USD, log scale)" |
| FrontierCode v1.1, main set | Opus 5.5 | opus55-charts.tsv | 47.3% $0.40 (:26) | 54.0% $1.09 (:28) | 54.4% $6.19 (:30) | "Score (%)" / "Cost per task (USD, log scale)" |
| FrontierCode v1.1, main set | Fable 5.1 (stand-in) | opus55-charts.tsv | 52.8% $2.47 (:31) | 50.3% $5.27 (:33) | 50.3% $12.82 (:35) | "Score (%)" / "Cost per task (USD, log scale)" |
| FrontierCode 2.0 | Fable 5.2 | fable52-charts.tsv | 34.2% $2.10 (:1) | 45.3% $6.72 (:3) | 45.6% $44.70 (:5) | "Score (%)" / "Cost per task (USD, log scale)" |
| FrontierCode 2.0 | Opus 5.5 | fable52-charts.tsv | 14.7% $0.75 (:6) | 34.5% $2.42 (:8) | 45.5% $12.82 (:10) | "Score (%)" / "Cost per task (USD, log scale)" |
| CursorBench 4.0 | Sonnet 5.5 | sonnet55-charts.tsv | 35.8% $0.50 (:41) | 47.8% $1.67 (:43) | 55.5% $9.67 (:45) | "Score (%)" / "Cost per task (USD, log scale)" |
| CursorBench 4.0 | Opus 5.5 | opus55-charts.tsv | 43.7% $1.18 (:51) | 56.0% $3.97 (:53) | 57.8% $13.43 (:55) | "Score (%)" / "Cost per task (USD, log scale)" |
| CursorBench 4.0 | Fable 5.1 (stand-in) | opus55-charts.tsv | 45.1% $5.44 (:56) | 49.2% $9.08 (:58) | 51.8% $17.28 (:60) | "Score (%)" / "Cost per task (USD, log scale)" |
| AA-Briefcase v1.1 | Sonnet 5.5 | sonnet55-charts.tsv | 1264.0 $0.87 (:61) | 1634.0 $3.95 (:63) | 1811.0 $29.19 (:65) | "Elo" / "Cost per task (USD, log scale)" |
| AA-Briefcase v1.1 | Opus 5.5 | sonnet55-charts.tsv | 1285.0 $1.15 (:66) | 1705.0 $6.27 (:68) | 1822.0 $21.05 (:70) | "Elo" / "Cost per task (USD, log scale)" |
| GDPval-AA v2.1 | Haiku 5.5 | haiku55-charts.tsv | 1125.0 $0.01 (:17) | 1420.0 $0.09 (:19) | 1620.0 $0.87 (:21) | "Elo, as reported" / "Cost per task (USD, log scale)" |
| GDPval-AA v2.1 | Sonnet 5.5 | haiku55-charts.tsv | 1179.0 $0.22 (:23) | 1551.0 $0.62 (:25) | 1840.0 $6.78 (:27) | "Elo, as reported" / "Cost per task (USD, log scale)" |
| GDPval-AA v2.1 | Opus 5.5 | opus55-charts.tsv | 1224 $0.21 (:71) | 1692 $1.54 (:73) | 1846 $8.92 (:75) | "Elo" / "Estimated cost per task (USD, log scale)" |
| GDPval-AA v2.1 | Fable 5.1 (stand-in) | opus55-charts.tsv | 1450 $1.41 (:76) | 1617 $3.43 (:78) | 1735 $9.59 (:80) | "Elo" / "Estimated cost per task (USD, log scale)" |
| OSWorld 2.1 (offline subset) | Haiku 5.5 | haiku55-charts.tsv | 42.0% $0.07 (:1) | 61.3% $0.18 (:3) | 72.4% $0.61 (:5) | "Partial-credit score (%)" / "Cost per attempt (USD, log scale)" |
| OSWorld 2.1 (offline subset) | Sonnet 5.5 | haiku55-charts.tsv | 57.9% $0.68 (:7) | 73.2% $1.38 (:9) | 83.9% $5.73 (:11) | "Partial-credit score (%)" / "Cost per attempt (USD, log scale)" |
| Humanity’s Last Exam (no tools) | Haiku 5.5 | haiku55-charts.tsv | 30.9% $0.003 (:33) | 39.7% $0.02 (:35) | 45.9% $0.21 (:37) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| Humanity’s Last Exam (no tools) | Sonnet 5.5 | haiku55-charts.tsv | 41.4% $0.03 (:39) | 47.9% $0.08 (:41) | 56.9% $0.89 (:43) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| Humanity’s Last Exam (with tools) | Fable 5.2 | fable52-charts.tsv | 68.4% $0.19 (:54) | 71.5% $0.63 (:56) | 74.2% $4.51 (:58) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| Humanity’s Last Exam (with tools) | Opus 5.5 | fable52-charts.tsv | 57.4% $0.08 (:59) | 63.9% $0.29 (:61) | 67.7% $2.18 (:63) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| AutomationBench | Opus 5.5 | opus55-charts.tsv | 23.3% $0.50 (:96) | 32.0% $0.70 (:98) | 40.0% $1.37 (:100) | "Pass rate (%)" / "Cost per task (USD, log scale)" |
| WANDR | Opus 5.5 | opus55-charts.tsv | 31.2% $1.20 (:116) | 67.3% $16.88 (:118) | 72.3% $37.92 (:120) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| WANDR | Fable 5.1 (stand-in) | opus55-charts.tsv | 63.3% $23.25 (:121) | 66.7% $33.62 (:123) | 68.7% $49.02 (:125) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| WANDR (relaxed score) | Fable 5.2 | fable52-charts.tsv | 71.4% $12.66 (:24) | 79.3% $29.20 (:26) | 82.1% $53.11 (:28) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| WANDR (relaxed score) | Opus 5.5 | fable52-charts.tsv | 31.2% $1.25 (:29) | 67.3% $17.31 (:31) | 72.3% $38.68 (:33) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| BenchCAD 2.1 (with tools) | Fable 5.2 | fable52-charts.tsv | 26.9 $1.89 (:39) | 61.0 $9.99 (:41) | 83.5 $50.77 (:43) | "Score (0–100)" / "Cost per attempt (USD, log scale)" |
| BenchCAD 2.1 (with tools) | Opus 5.5 | fable52-charts.tsv | 6.3 $0.03 (:44) | 29.7 $2.57 (:46) | 65.3 $19.86 (:48) | "Score (0–100)" / "Cost per attempt (USD, log scale)" |
| Chartography (no tools) | Fable 5.2 | fable52-charts.tsv | 64.2% $0.03 (:69) | 69.8% $0.07 (:71) | 73.4% $0.75 (:73) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| Chartography (no tools) | Opus 5.5 | fable52-charts.tsv | 57.0% $0.02 (:74) | 59.2% $0.03 (:76) | 64.4% $0.49 (:78) | "Score (%)" / "Cost per attempt (USD, log scale)" |
| CVE Rediscovery | Opus 5.5 | fable52-charts.tsv | 59.4% $0.11 (:89) | 70.0% $0.43 (:91) | 81.3% $2.98 (:93) | "Advisories found (%)" / "Cost per attempt (USD, log scale)" |

Opus 5.5 Terminal-Bench 4.0 and CursorBench 4.0 also appear in `sonnet55-charts.tsv:6-10, 46-50` with the same scores. Charts plot "Cost per attempt" on some axes while the text says "cost per task" (sonnet55-announce:72); both kept as labelled.

Anthropic cost doc:

| benchmark | model | place | low | high | max | unit |
|---|---|---|---|---|---|---|
| SWE-bench Pro subset (478) | Opus 5.5 | about-claude-models-optimizing-for-cost-and-intelligence.md:434,436 | 87.4% $0.11/task | 95.3% $0.29/task | empty: no max run (refs: low, medium, high, xhigh) | % of tasks solved |
| SWE-bench Pro subset (478) | Sonnet 5.5 | about-claude-models-optimizing-for-cost-and-intelligence.md:374 | empty: runs at medium, high only | 87.6% $0.11/solved task | empty | % of tasks solved |
| SWE-bench Pro subset (463) | Fable 5.2 | about-claude-models-optimizing-for-cost-and-intelligence.md:383 | 94.6% $0.39/solved task | 96.3% $1.39/solved task | empty | % of tasks solved |
| SWE-bench Pro subset (463) | Opus 5.5 | about-claude-models-optimizing-for-cost-and-intelligence.md:383 | empty on 463 | 95.5% $0.30/solved task | empty | % of tasks solved |
| DeepResearch Bench II (44) | Fable 5.2 | about-claude-models-optimizing-for-cost-and-intelligence.md:438,440 | 54.5% $1.49/task | 57.7% $4.82/task | empty | rubric score % |
| defect-search (internal) | Opus 5.5 | about-claude-models-optimizing-for-cost-and-intelligence.md:930 | F1 0.489 $38/run | F1 0.850 $236/run | empty | mean F1, 10 runs |
| defect-search (internal) | Fable 5.2 | about-claude-models-optimizing-for-cost-and-intelligence.md:930 | F1 0.866 $357/run | F1 0.909 $563/run | empty | mean F1, 10 runs |
| defect-search (internal) | Sonnet 5.5 | about-claude-models-optimizing-for-cost-and-intelligence.md:930 | empty | F1 0.760 $103/run | empty | mean F1, 10 runs |

Artificial Analysis Intelligence Index v5.0.1, one run per record (`aa-claude-fable-5-1` page data, record slug given; the file has 0 newlines, so no line). Fractions as stored (pass@1 aggregated over repeats); suite sizes from the methodology table: TB4.0 66×3, FC2.0 132×3, TB-Sci 70×3, CritPt 40×5, HLE-D 1000×1, AutoB 657×1, GDP.pdf 100×5, Briefcase 91×1 (Elo), Omniscience 3000×1 (index).

| model | effort | record | II | TB4.0 | FC2.0 | TB-Sci | CritPt | HLE-D | AutoB | GDP.pdf | Briefcase Elo | Omniscience |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Haiku 5.5 | low | claude-haiku-5-5-low | 18.62 | 0.126 | 0.080 | 0.019 | 0.215 | 0.141 | 0.229 | 0.112 | 1114 | 2.2 |
| Haiku 5.5 | high | claude-haiku-5-5-high | 29.87 | 0.217 | 0.232 | 0.100 | 0.450 | 0.237 | 0.337 | 0.172 | 1441 | 5.3 |
| Haiku 5.5 | max | claude-haiku-5-5 | 36.48 | 0.328 | 0.349 | 0.200 | 0.435 | 0.296 | 0.354 | 0.208 | 1573 | 12.3 |
| Sonnet 5.5 | low | claude-sonnet-5-5-low | 25.65 | 0.207 | 0.071 | 0.105 | 0.260 | 0.206 | 0.494 | 0.160 | 1268 | 20.3 |
| Sonnet 5.5 | high | claude-sonnet-5-5-high | 41.52 | 0.439 | 0.257 | 0.343 | 0.515 | 0.338 | 0.594 | 0.252 | 1634 | 18.7 |
| Sonnet 5.5 | max | claude-sonnet-5-5 | 54.54 | 0.636 | 0.417 | 0.533 | 0.590 | 0.533 | 0.718 | 0.258 | 1816 | 30.5 |
| Opus 5.5 | low | claude-opus-5-5-low | 34.75 | 0.313 | 0.158 | 0.243 | 0.360 | 0.417 | 0.529 | 0.256 | 1279 | 39.0 |
| Opus 5.5 | high | claude-opus-5-5-high | 51.84 | 0.566 | 0.359 | 0.490 | 0.595 | 0.556 | 0.632 | 0.288 | 1682 | 42.4 |
| Opus 5.5 | max | claude-opus-5-5 | 59.11 | 0.596 | 0.464 | 0.590 | 0.680 | 0.679 | 0.695 | 0.262 | 1801 | 48.1 |
| Fable 5.2 | low | claude-fable-5-2-low | 53.92 | 0.545 | 0.384 | 0.538 | 0.600 | 0.608 | 0.680 | 0.268 | 1563 | 62.9 |
| Fable 5.2 | high | claude-fable-5-2-high | 61.82 | 0.596 | 0.491 | 0.700 | 0.730 | 0.738 | 0.714 | 0.218 | 1677 | 64.0 |
| Fable 5.2 | max | claude-fable-5-2 | 64.56 | 0.596 | 0.488 | 0.733 | 0.765 | 0.802 | 0.764 | 0.242 | 1785 | 66.8 |

## Appetite

Only Artificial Analysis gives tokens per pair. Suite total = `canonicalIntelligenceIndexTokenCount.output` over the 9-evaluation suite ("Output Tokens Used to Run Artificial Analysis Intelligence Index"); per-task = `intelligenceIndexOutputTokensPerTask.output` ("Weighted average number of output tokens used to run one task"); per evaluation = `outputTokensPerTask`. AA counts tokens "reported by each model's API provider where available" (methodology). Relative-to-low is derived (pair total / same model's low total).

| model | effort | suite output tokens | of which reasoning | per task (weighted) | vs low | TB4.0 tok/task | FC2.0 tok/task | HLE-D tok/task | AA $/task |
|---|---|---|---|---|---|---|---|---|---|
| Haiku 5.5 | low | 29,899,488 | 15,432,795 | 28,161 | 1.00 (derived) | 70,285 | 25,867 | 3,306 | $0.044 |
| Haiku 5.5 | high | 89,814,062 | 62,937,860 | 88,064 | 3.00 (derived) | 166,080 | 83,425 | 22,015 | $0.159 |
| Haiku 5.5 | max | 297,721,915 | 256,967,578 | 225,966 | 9.96 (derived) | 346,826 | 254,933 | 93,329 | $0.411 |
| Sonnet 5.5 | low | 21,348,593 | 6,217,790 | 20,856 | 1.00 (derived) | 40,277 | 10,474 | 1,358 | $0.511 |
| Sonnet 5.5 | high | 54,656,782 | 30,412,603 | 58,421 | 2.56 (derived) | 76,655 | 27,588 | 10,546 | $1.636 |
| Sonnet 5.5 | max | 335,221,511 | 274,036,315 | 285,387 | 15.70 (derived) | 382,429 | 315,985 | 80,244 | $10.021 |
| Opus 5.5 | low | 21,114,634 | 6,455,516 | 19,060 | 1.00 (derived) | 37,782 | 14,073 | 1,586 | $0.976 |
| Opus 5.5 | high | 56,144,369 | 29,608,722 | 60,071 | 2.66 (derived) | 100,178 | 42,739 | 9,493 | $3.465 |
| Opus 5.5 | max | 218,145,408 | 173,363,510 | 173,313 | 10.33 (derived) | 252,948 | 199,997 | 59,682 | $10.036 |
| Fable 5.2 | low | 34,856,849 | 13,740,509 | 35,860 | 1.00 (derived) | 52,872 | 25,509 | 3,070 | $3.097 |
| Fable 5.2 | high | 85,274,482 | 49,752,004 | 97,841 | 2.45 (derived) | 157,872 | 104,935 | 11,476 | $9.078 |
| Fable 5.2 | max | 274,763,289 | 208,268,619 | 273,776 | 7.88 (derived) | 376,804 | 419,818 | 43,214 | $26.539 |

Publisher sources print no token count per pair. The cost doc gives one relative statement (:902, ref 3, "Compare models, work per task"): Opus 5.5 `low` used "a little over half of Sonnet 5.5's output tokens" at Sonnet's default `high` on SWE-bench Pro; no number.

## Dollars

- Announcement charts: per task or per attempt as each x-axis says (column in Reach); not per solved task. Three Sonnet 5.5 Terminal-Bench 4.0 dollar series exist for one score series: $0.76/$1.94/$12.54 (sonnet55-charts.tsv:1,3,5), and on the Haiku page $0.62/$1.46/$10.44 at $0.10 cache reads and $0.79/$1.97/$14.15 at $0.20 (haiku55-charts.tsv:50-59). Opus 5.5 CursorBench low/xhigh: $1.18 and $6.99 (opus55:51,54) against $1.17 and $6.98 (sonnet55:46,49). Opus WANDR $1.20 (opus55:116) against WANDR relaxed $1.25 (fable52:29), same 31.2%.
- Cost doc: per task in the effort table (:430 "Costs are per task, not per solved task"); per solved task in Compare models (:374-375) and the 463-problem sentence (:383); per run for defect search (:930).
- AA: `costPerTask` per evaluation and the weighted `intelligenceIndexCostPerTask` (in Appetite and pairs.json); per task, with live cache-hit rates (methodology). No per-solved figure printed.

## Derived

Work units per 100,000 output tokens = AA score fraction × 100000 / AA `outputTokensPerTask`, same record, same run (arithmetic per cell in pairs.json). A work unit is one task's score fraction; for FC2.0 the score may hold rubric credit, so it is not strictly tasks solved. II, Briefcase (Elo) and Omniscience (index) give no work unit: no figure.

| model | effort | TB4.0 | FC2.0 | TB-Sci | CritPt | HLE-D |
|---|---|---|---|---|---|---|
| Haiku 5.5 | low | 0.18 | 0.31 | 0.03 | 1.75 | 4.26 |
| Haiku 5.5 | high | 0.13 | 0.28 | 0.06 | 0.93 | 1.08 |
| Haiku 5.5 | max | 0.09 | 0.14 | 0.05 | 0.29 | 0.32 |
| Sonnet 5.5 | low | 0.51 | 0.68 | 0.22 | 5.18 | 15.17 |
| Sonnet 5.5 | high | 0.57 | 0.93 | 0.23 | 3.76 | 3.20 |
| Sonnet 5.5 | max | 0.17 | 0.13 | 0.10 | 0.42 | 0.66 |
| Opus 5.5 | low | 0.83 | 1.13 | 0.47 | 8.21 | 26.29 |
| Opus 5.5 | high | 0.56 | 0.84 | 0.32 | 4.13 | 5.86 |
| Opus 5.5 | max | 0.24 | 0.23 | 0.19 | 0.70 | 1.14 |
| Fable 5.2 | low | 1.03 | 1.51 | 0.54 | 10.06 | 19.81 |
| Fable 5.2 | high | 0.38 | 0.47 | 0.29 | 3.53 | 6.43 |
| Fable 5.2 | max | 0.16 | 0.12 | 0.16 | 0.62 | 1.86 |

No derived figure for any publisher chart or cost-doc series: they print no tokens, and AA's tokens come from different runs and different suites.

## Speed

| model | AA low | AA high | AA max | OpenRouter p50 | this project |
|---|---|---|---|---|---|
| Haiku 5.5 | 217.5 | 228.2 | 255.6 | 177.0 | none given |
| Sonnet 5.5 | 137.2 | 139.4 | 145.9 | 112.0 | 109.4 |
| Opus 5.5 | 107.0 | 105.4 | 115.4 | 63.0 | 89.9 |
| Fable 5.2 | 96.9 | 97.8 | 96.0 | 83.0 | 76.0 (Fable 5.1: 73.3) |

- AA: `headline.outputSpeed` in each record, tokens per second; "Output tokens divided by total request time, including time to first token"; Anthropic first-party endpoint; "Speed and latency metrics average each endpoint's runs over the past 5 days"; rendered "Output speed 115 tok/s" for Opus max on the page. Fetched 2026-11-12.
- OpenRouter: "Throughput (p50)", provider Anthropic; effort, streaming and definition not stated on the page. Search summaries quoted other OpenRouter snapshots (Opus 76.0, Sonnet 88.0 to 116); not fetched, not used.
- This project: lead's own transcripts, 2026-11-12, as given in the brief; not re-measured.
- Not fetched: agentsroom.dev Claude Code measurement (HTTP 413 twice).

## Instructions found in the sources

None addressed to the reader. Keyword scan of every used file: 5 hits, all in the AA methodology page, which quotes benchmark system prompts (the check found the same). The search tool appended a reminder to cite sources; tool scaffolding, not a source.

## Not determined

- Publisher series at an effort the source never ran: Opus 5.5 SWE-bench Pro max; Sonnet 5.5 SWE-bench Pro low and max; Fable 5.2 SWE-bench Pro, DeepResearch Bench II and defect search at max; Sonnet 5.5 defect search at low and max. Cheapest source: the system cards of each model.
- Fable 5.2 on Terminal-Bench 4.0, FrontierCode v1.1, CursorBench 4.0, GDPval-AA, WANDR (non-relaxed) in publisher charts: absent; Fable 5.1 stands in. AA covers Terminal-Bench 4.0 for 5.2.
- Tokens per task in any publisher run: not printed. Cheapest source: system cards or Anthropic eval logs.
- FrontierCode-AA 2.0 per-task score: whether partial credit enters the fraction; AA methodology section on FrontierCode-AA 2.0 settles it.
- AA per-task weighting of `intelligenceIndexOutputTokensPerTask`: stated "weighted average", weights read from the methodology table only.
- Speed by effort on OpenRouter and the effort behind this project's figures; Haiku 5.5 measurement of this project: none given. Cheapest: OpenRouter activity page per effort; the lead's transcripts for Haiku.

Scratch left for the lead: `recon/2026-10-24/scratch/extract-pairs-reach-appetite/` (`aarec.py`, `build.py`, `aa-pairs-raw.json`, `aa-speed-raw.json`, `tables.md`, `pairs.json`).

Result: PASS
