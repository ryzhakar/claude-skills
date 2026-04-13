# Strunk Analysis: fix-macos-app

## Critical & Severe

### R10 (Active Voice) - Severe

**Line 7: "Diagnose and fix `.app` bundles that fail to launch due to Gatekeeper, quarantine, or broken code signatures."**
- Active imperative: "Diagnose and fix." No violation.

**Line 8: "Common with apps distributed outside the Mac App Store."**
- Elliptical construction (implied "This is common...").
- Severity: Minor
- Suggested revision: "Apps distributed outside the Mac App Store commonly exhibit these issues."

**Line 10: "Diagnose with `xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file` on the binary."**
- Active imperative. No violation.

**Line 10: "Then apply fixes in order, testing launch after each:"**
- Active imperative: "apply fixes" and "testing launch." No violation.

**Line 17: "Avoid making one passive depend directly upon another:"**
- Active imperative: "Avoid making." No violation.

**Line 18: "Never just remove a signature"**
- Active imperative with prohibition. No violation.

**Line 18: "macOS refuses to launch unsigned binaries"**
- Active voice: "macOS refuses." No violation.

**Line 19: "Quarantine can interfere with the signing process."**
- Active voice: "Quarantine can interfere." No violation.

### R12 (Concrete Language) - Severe

**Line 8: "Common with apps distributed outside the Mac App Store."**
- "Apps distributed outside" is concrete enough (identifies source).
- No violation.

**Line 10: "Diagnose with `xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file` on the binary."**
- Specific commands with exact flags. Excellent concreteness.
- No violation.

**Line 12-13: Step numbers and commands**
```
1. **Clear quarantine:** `xattr -cr /path/to/App.app`
2. **Re-sign ad-hoc:** `codesign --force --deep --sign - /path/to/App.app`
```
- Specific commands with exact syntax. Excellent concreteness.
- No violation.

**Line 18: "POSIX error 153"**
- Specific error code. Excellent concreteness.
- No violation.

### R13 (Needless Words) - Moderate

**Line 1-3 (description): "This skill should be used when the user asks to 'fix a broken app', 'app won't open', 'Gatekeeper blocks app', 'can't launch app', 'app is damaged', 'clear quarantine', 're-sign app', 'fix code signing', or mentions macOS security preventing an app from launching."**
- Very long trigger list. In frontmatter context (metadata), this is appropriate.
- Not prose proper. N/A for style analysis.

**Line 7: "Diagnose and fix `.app` bundles that fail to launch due to Gatekeeper, quarantine, or broken code signatures."**
- Could be tighter: "Fix `.app` bundles that fail to launch due to Gatekeeper, quarantine, or broken signatures." (Remove "Diagnose and" if next line covers diagnosis)
- Severity: Minor
- Analysis: "Diagnose and fix" establishes two-step process, so not needless.

**Line 8: "Common with apps distributed outside the Mac App Store."**
- All words tell. No needless words.
- No violation.

**Line 10: "Then apply fixes in order, testing launch after each:"**
- "in order" - needed for clarity.
- "after each" - needed for clarity.
- No needless words.
- No violation.

**Line 17: "Avoid making one passive depend directly upon another:"**
- "directly" adds specificity (not just any dependence).
- No needless words.
- No violation.

**Line 18: "Never just remove a signature (`codesign --remove-signature`) without re-signing."**
- "just" is emphasis word.
- Severity: Minor
- Analysis: "just" emphasizes the incompleteness of the action. Serves purpose.
- Acceptable.

## Moderate

### R11 (Positive Form) - Moderate

**Line 7: "bundles that fail to launch"**
- "fail to" is negative.
- Severity: Minor
- Analysis: "fail to launch" is standard technical terminology for this error condition. Alternative "bundles that won't launch" or "non-launching bundles" aren't clearer.
- Acceptable - technical precision.

**Line 17: "Avoid making one passive depend directly upon another"**
- "Avoid" is negative prohibition.
- Severity: Moderate
- Suggested revision: "Keep each passive construction independent" OR "Use only one passive construction per dependency chain"
- But in context of "Critical Pitfalls" section, negative prohibition is conventional.

**Line 18: "Never just remove a signature... without re-signing."**
- Double negative structure: "Never... without"
- Severity: Moderate
- Suggested revision: "Always re-sign after removing a signature" OR "Remove a signature only when immediately followed by re-signing"

**Line 18: "macOS refuses to launch unsigned binaries"**
- "refuses" is positive verb (active denial).
- No violation.

### R15 (Parallel Construction) - Moderate

**Line 10: "Diagnose with `xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file` on the binary."**
- List of commands: all are command names except last.
- Pattern: command, command, command, "and command on the binary"
- Severity: Minor
- Suggested revision: "Diagnose with `xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file` (on the binary)." OR make all parallel by adding context to each.
- Current form acceptable - final element slight variation for clarity.

**Lines 12-13: Numbered fix steps**
```
1. **Clear quarantine:** `xattr -cr /path/to/App.app`
2. **Re-sign ad-hoc:** `codesign --force --deep --sign - /path/to/App.app`
```
- Pattern: NUMBER. **[Action]:** `[command]`
- Both perfectly parallel.
- No violation.

**Lines 18-19: Pitfall list**
```
- **Never just remove a signature** (`codesign --remove-signature`) without re-signing. macOS refuses to launch unsigned binaries (POSIX error 153).
- **Clear quarantine before re-signing.** Quarantine can interfere with the signing process.
```
- First bullet: Bold prohibition + parenthetical command + explanation + parenthetical error.
- Second bullet: Bold imperative + explanation.
- Not strictly parallel but both follow: **[Action/Prohibition].** [Explanation]
- Severity: Minor
- Both bullets could follow same pattern more strictly, but current form is clear.

### R18 (Emphatic Position) - Moderate

**Line 7: "Diagnose and fix `.app` bundles that fail to launch due to Gatekeeper, quarantine, or broken code signatures."**
- Ends with "broken code signatures" - one of three causes, not the most important element.
- Severity: Minor
- Could be restructured to emphasize action: "Fix `.app` bundles that fail to launch due to Gatekeeper, quarantine, or broken signatures by diagnosing and re-signing."
- Current form acceptable - cause list is important context.

**Line 8: "Common with apps distributed outside the Mac App Store."**
- Ends with "Mac App Store" - the source/distribution channel.
- Could emphasize commonality: "Apps distributed outside the Mac App Store commonly show these issues."
- Severity: Minor

**Line 10: "Then apply fixes in order, testing launch after each:"**
- Ends with "after each" - timing clause.
- Severity: Minor
- Could be: "Then apply fixes in order, testing launch between each step." OR "After each fix, test launch."
- Current form acceptable.

**Line 18: "macOS refuses to launch unsigned binaries (POSIX error 153)."**
- Ends with parenthetical error code - technical detail, not main point.
- Severity: Moderate
- Suggested revision: "macOS refuses to launch unsigned binaries, throwing POSIX error 153." (Ends with error as consequence, not parenthetical)
- OR: "Unsigned binaries trigger POSIX error 153; macOS refuses to launch them."

**Line 19: "Quarantine can interfere with the signing process."**
- Ends with "signing process" - the affected thing.
- Could be: "The signing process fails when quarantine attributes remain." (Ends with cause)
- Severity: Minor
- Current form acceptable.

## Minor & Stylistic

### Style observations

**Line 5: "# Fix Broken macOS App Bundles"**
- Clear title. No issue.

**Line 7-8: Opening two sentences**
- First sentence: active imperative
- Second sentence: elliptical observation
- Different structures but both clear.
- No violation.

**Line 10: Series with serial comma**
- "`xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file`"
- Serial comma present. Good per R2.

**Line 15: "## Critical Pitfalls"**
- Section header. Clear.

**Lines 12-13: Numbered list format**
- Clean, parallel structure with bolded actions and code commands.
- Excellent clarity.

**Lines 18-19: Bullet list in "Critical Pitfalls"**
- Bold lead-ins with explanations.
- Standard format for warnings/pitfalls.

### Comma usage

**Line 10: "Diagnose with `xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file` on the binary."**
- Serial commas present. Correct per R2.

**Line 10: "Then apply fixes in order, testing launch after each:"**
- Comma before participial phrase "testing launch." Acceptable per R3 (participial phrases may be set off).

**Line 18: "Never just remove a signature (`codesign --remove-signature`) without re-signing."**
- No comma before "without" - this is correct (no comma before subordinating conjunction when clause follows main).

## Summary

**Critical/Severe findings:** 0
**Moderate findings:** 4
- R11 (positive form): 2 instances (negative constructions)
- R18 (emphatic position): 1 instance (parenthetical in emphatic position)
- R10 (active voice): 1 instance (elliptical construction)

**Minor findings:** 7
- R10: 1 instance (elliptical construction)
- R11: 1 instance ("fail to" but technical term)
- R13: 1 instance ("just" as emphasis)
- R15: 2 instances (minor parallelism variations)
- R18: 3 instances (minor emphasis placement)

**Overall assessment:** Prose is exceptionally concise and concrete. Excellent use of specific commands, error codes, and technical details. Document is very short (19 lines of actual content), which contributes to clarity and economy. Most "violations" are minor and several are justified by technical writing conventions.

**Strengths:**
- Outstanding concreteness (specific commands, flags, error codes)
- Excellent economy - every word tells
- Clear imperative mood throughout
- Numbered steps perfectly parallel
- Very tight, focused scope

**Weaknesses:**
- 2 negative constructions could be positive (though context may justify)
- 1 parenthetical detail (POSIX error) in emphatic position
- Minor elliptical construction in line 8

**Recommended focus:** Rephrase "Never... without" to positive form ("Always re-sign after"); move POSIX error code out of parenthetical to stronger position; expand elliptical construction in line 8 for clarity.

**Special notes:**
- This is the shortest document analyzed (19 lines vs 140 and 181 in the others)
- High information density per line
- Technical writing genre justifies some deviations (negative prohibitions in warnings, technical terminology)
- Overall quality very high for technical reference material
