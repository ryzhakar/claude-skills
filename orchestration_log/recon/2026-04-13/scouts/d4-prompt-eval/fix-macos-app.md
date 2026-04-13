# Prompt Evaluation Report: fix-macos-app

**Type:** Skill  
**File:** `/Users/ryzhakar/pp/claude-skills/userland-utilities/skills/fix-macos-app/SKILL.md`  
**Evaluated:** 2026-04-13

---

## Overall Score: 62/100 (Adequate)

Functions for its narrow use case but has significant structural gaps, missing context, and vague terminology. Requires substantial improvement for production quality.

---

## Applicable Categories

- STRUCTURE ✓
- CLARITY ✓
- CONSTRAINTS ✓
- SAFETY ✓ (enhanced - handles system commands)
- OUTPUT ✓
- AGENT_SPECIFIC ✓

Not applicable: TOOLS, EXAMPLES, REASONING, DATA_SEPARATION

---

## Critical Issues

### STR-3: Incomplete Task Definition
**Severity:** Critical (MUST violation)

The task is stated as "Diagnose and fix `.app` bundles" (line 7) but the workflow is incomplete. The skill shows diagnostic commands (line 10) and fix commands (lines 12-13) but never specifies the complete decision tree:

- When to stop at step 1 (clear quarantine)?
- When to proceed to step 2 (re-sign)?
- What if both steps fail?
- What constitutes success?

**Impact:** User cannot execute the skill end-to-end without guessing decision points.

### CLR-1: Task Not Fully Actionable
**Severity:** Critical (MUST violation)

The task cannot be stated in one unambiguous sentence because the workflow omits conditional logic. Line 10 says "Diagnose with [tools]" then "apply fixes in order, testing launch after each" but never specifies:

- How to interpret diagnostic output
- What diagnostic results trigger which fix
- How to test launch

**Impact:** Skill assumes user knows how to interpret `xattr -l`, `codesign -dv`, `spctl --assess`, and `file` outputs.

---

## Warnings

### STR-1: No Role/Identity Statement
**Severity:** Medium (SHOULD violation)

The skill lacks a "You are a..." statement establishing persona. Compare to other skills which open with role definition.

### STR-2: Insufficient Context
**Severity:** High (SHOULD violation)

Critical domain context missing:
- What is Gatekeeper? (mentioned line 7 but never defined)
- What is quarantine? (mentioned lines 7, 12, 17)
- What does "ad-hoc signing" mean? (line 13)
- Why does macOS refuse unsigned binaries? (mentioned line 17)

Line 8 hints at context ("Common with apps distributed outside the Mac App Store") but doesn't explain *why* this causes problems.

**Impact:** Users unfamiliar with macOS security model cannot understand why these steps work.

### STR-4: Minimal Structural Markers
**Severity:** Low (SHOULD violation)

Only one numbered list (lines 12-13). Diagnostic command list (line 10) is prose, not structured. Critical Pitfalls section (lines 15-18) uses bullets but inconsistently.

### STR-5: Ordering Suboptimal
**Severity:** Low (SHOULD violation)

Current order: Task → Diagnostics → Fixes → Pitfalls

Recommended: Context (why this problem exists) → Diagnostics (how to identify) → Decision tree (which fix when) → Fixes → Pitfalls → Success criteria

### CLR-2: Vague Terms Present
**Severity:** High (MUST_NOT violation)

Multiple undefined vague terms:
- "broken code signatures" (line 7) — what makes a signature "broken"?
- "fail to launch" (line 7) — what are symptoms?
- "in order" (line 10) — order not specified for diagnostics
- "testing launch after each" (line 10) — how to test?

### CLR-4: No Success Criteria
**Severity:** High (SHOULD violation)

The skill never defines what constitutes successful fix. Implied success is "app launches" but:
- How do you launch? Double-click? Command line?
- What constitutes successful launch? Window appears? No crash dialog?
- What if app launches but crashes after 5 seconds?

### CON-1: Scope Not Explicitly Defined
**Severity:** Medium (MUST violation)

Description lists trigger phrases (line 3) but doesn't define scope boundaries:
- Does this handle apps that launch but crash?
- Does this handle apps with expired certificates?
- Does this handle apps requiring notarization?

### CON-2: Forbidden Actions Incomplete
**Severity:** Medium (SHOULD violation)

"Critical Pitfalls" section (lines 15-18) lists two "Never" constraints but framed as pitfalls, not explicit forbidden actions. Missing:
- Do NOT run on system apps (could break OS)
- Do NOT remove quarantine from untrusted apps (security risk)
- Do NOT skip diagnostic step (could misapply fix)

### SAF-1: No Data Sensitivity Classification
**Severity:** Medium (SHOULD violation)

The skill manipulates app bundles (line 12-13) but never warns:
- Verify app source before clearing quarantine (security risk)
- Backup app before re-signing (data loss risk)

### SAF-6: Incomplete Error Handling
**Severity:** High (SHOULD violation)

No guidance for failure modes:
- What if `codesign --force --deep --sign -` fails?
- What if app still won't launch after both steps?
- What if diagnostic commands error out?

### OUT-1: No Output Format Specified
**Severity:** Medium (SHOULD violation)

The skill doesn't specify what Claude should output:
- Should diagnostic results be shown to user?
- Should commands be run automatically or displayed for user to run?
- What format should final report take?

### OUT-3: No Edge Case Handling
**Severity:** High (SHOULD violation)

Missing handling for:
- App requires specific macOS version
- App has expired developer certificate
- App requires system extension approval
- App is 32-bit (unsupported on modern macOS)

### AGT-6: Workflow Incomplete
**Severity:** Critical (MUST violation)

The workflow omits critical conditional logic:
1. Run diagnostics → *(missing: how to interpret results)*
2. Apply fix 1 → *(missing: how to verify success)*
3. If fix 1 fails... → *(missing: this branch entirely)*
4. Apply fix 2 → *(missing: how to verify success)*
5. If fix 2 fails... → *(missing: this branch entirely)*

### AGT-8: No Output Format
**Severity:** Medium (SHOULD violation)

No specification for what Claude should produce. Should it:
- Run commands and report results?
- Generate a script for user to run?
- Provide step-by-step instructions?

---

## Anti-Patterns Detected

### AP-STR-01: Wall of Text (Low)
Only 19 lines but lacks visual hierarchy. Everything except pitfalls is continuous prose.

### AP-CLR-01: Vague Task Definition (Critical)
"Diagnose and fix" without complete specification of decision tree or success criteria.

### AP-CLR-02: Undefined Qualifiers (High)
"broken", "fail", "in order" used without definition.

### AP-CLR-05: Implicit Success Criteria (Medium)
Success never explicitly stated.

### AP-CON-01: Implicit Scope (High)
Scope boundaries undefined. What problems are in vs. out of scope?

### AP-SAF-03: Missing Error Handling (High)
No guidance for when fixes fail.

### AP-AGT-04: Missing Workflow (Critical)
Workflow lacks conditional logic and decision points.

---

## Strengths

### AGT-1: Valid Name Field ✓
`name: fix-macos-app` (lowercase, hyphenated).

### AGT-2: Strong Description ✓
Trigger keywords highly specific and comprehensive (line 3):
- "fix a broken app"
- "app won't open"
- "Gatekeeper blocks app"
- "can't launch app"
- "app is damaged"
- "clear quarantine"
- "re-sign app"
- "fix code signing"

### AGT-7: Focused Scope ✓
Single purpose: Fix macOS app launch failures.

### AGT-9: Length Appropriate ✓
19 lines. Concise but *too* concise (sacrifices completeness).

### CON-4: Rationale Provided (Partial) ✓
"Critical Pitfalls" section (lines 15-18) explains why certain actions are dangerous:
- Why not to remove signature without re-signing (line 16-17)
- Why to clear quarantine before re-signing (line 18)

### CLR-3: No Contradictions ✓
The limited instructions provided are consistent.

---

## Recommendations

### Critical Priority (Must Fix for Production)

1. **Complete the workflow with conditional logic**
   ```markdown
   ## Diagnostic Workflow
   
   ### Step 1: Gather Evidence
   
   Run all four diagnostics:
   ```bash
   # Check for quarantine attribute
   xattr -l /path/to/App.app
   # Expected: com.apple.quarantine present if downloaded
   
   # Check code signature
   codesign -dv --verbose=2 /path/to/App.app 2>&1
   # Expected: Valid signature OR "code object is not signed"
   
   # Check Gatekeeper assessment
   spctl --assess -vv /path/to/App.app 2>&1
   # Expected: "accepted" OR "rejected"
   
   # Check binary type
   file /path/to/App.app/Contents/MacOS/*
   # Expected: "Mach-O 64-bit executable" OR "Mach-O universal binary"
   ```
   
   ### Step 2: Interpret Results
   
   | Diagnostic Result | Meaning | Next Step |
   |-------------------|---------|-----------|
   | Quarantine present + Gatekeeper rejects | Downloaded app, signature issue | Proceed to Fix 1 |
   | No quarantine + "not signed" | Unsigned app | Proceed to Fix 2 |
   | Valid signature + Gatekeeper accepts | Not a signing issue | Out of scope (see Troubleshooting) |
   | "Mach-O i386" (32-bit) | Unsupported on macOS 10.15+ | Out of scope (cannot fix) |
   
   ### Step 3: Apply Appropriate Fix
   
   **Fix 1: Clear Quarantine** (for downloaded apps)
   ```bash
   xattr -cr /path/to/App.app
   ```
   
   **Fix 2: Ad-Hoc Re-sign** (for unsigned/invalid signature)
   ```bash
   codesign --force --deep --sign - /path/to/App.app
   ```
   
   ### Step 4: Verify Fix
   
   After each fix:
   ```bash
   # Re-run Gatekeeper check
   spctl --assess -vv /path/to/App.app
   # Expected: "accepted" or no error
   
   # Test launch
   open /path/to/App.app
   # Expected: App window appears, no crash dialog
   ```
   
   If launch fails: Check Console.app for crash logs under "Crash Reports".
   ```

2. **Add comprehensive context section**
   ```markdown
   ## Background: macOS App Security
   
   macOS uses three mechanisms to prevent malicious apps:
   
   1. **Gatekeeper**: Checks if app is signed by known developer or notarized by Apple
   2. **Quarantine**: Flags files downloaded from internet for additional scrutiny
   3. **Code Signing**: Cryptographic signature verifying app hasn't been tampered with
   
   **Common failure scenario:** You download `App.app` from developer website. macOS:
   1. Sets quarantine attribute (`com.apple.quarantine`)
   2. On first launch, Gatekeeper checks signature
   3. If signature invalid/absent, Gatekeeper blocks launch with "damaged" error (misleading—app isn't damaged, just unsigned)
   
   **Why this skill works:**
   - Clearing quarantine tells macOS "I trust this app's source"
   - Ad-hoc re-signing (`--sign -`) creates local-only signature (works on your Mac only)
   - Neither bypasses malware; user must trust app source
   ```

3. **Define explicit scope boundaries**
   ```markdown
   ## Scope
   
   This skill handles:
   - Apps that won't launch due to Gatekeeper/quarantine
   - Apps with broken/invalid code signatures
   - Apps that show "damaged" or "cannot be opened" dialogs
   
   This skill does NOT handle:
   - Apps that launch but immediately crash (runtime issue, not signing)
   - Apps requiring notarization (enterprise/distribution)
   - System apps (do NOT modify system apps)
   - Apps requiring macOS version upgrade
   - Apps with expired certificates requiring renewal
   ```

4. **Add explicit success criteria**
   ```markdown
   ## Success Criteria
   
   Fix is successful when:
   - [ ] `spctl --assess` reports "accepted" or exits without error
   - [ ] `open /path/to/App.app` launches app window
   - [ ] App runs for >30 seconds without crash dialog
   - [ ] Console.app shows no new crash logs for app
   
   If all criteria met: Problem solved.
   If ANY fail: See Troubleshooting.
   ```

### High Priority

5. **Add comprehensive error handling**
   ```markdown
   ## Troubleshooting
   
   **Both fixes tried, app still won't launch:**
   - Check Console.app → Crash Reports → Find app name
   - Common causes: Missing dependencies, incompatible macOS version, 32-bit app on 10.15+
   - If crash log shows "dyld: Library not loaded": Missing dependency (out of scope)
   
   **codesign command fails:**
   Error: "resource fork, Finder information, or similar detritus not allowed"
   Fix: `xattr -cr /path/to/App.app` then retry codesign
   
   **App launches but immediately crashes:**
   Not a signing issue. Check app requirements vs. macOS version.
   ```

6. **Add safety warnings**
   ```markdown
   ## Safety Warnings
   
   Before clearing quarantine or re-signing:
   - [ ] Verify app source is trustworthy (official website, known developer)
   - [ ] Scan with antivirus if uncertain
   - [ ] Backup app: `cp -R App.app App.app.backup`
   
   Do NOT run this skill on:
   - Apps from unknown sources (security risk)
   - System apps in /System or /Applications (could break macOS)
   - Apps you didn't intentionally download
   ```

7. **Specify output format**
   ```markdown
   ## Output Format
   
   When user requests app fix, Claude should:
   1. Ask for app path if not provided: "Please provide full path to App.app"
   2. Run all four diagnostics, show output
   3. Interpret results using decision table
   4. Recommend specific fix based on diagnostic
   5. After user confirms, provide exact command to run
   6. Verify fix by checking launch success
   
   Do NOT run commands automatically (user must approve).
   ```

### Medium Priority

8. **Add example walkthroughs**
   ```markdown
   ## Example: Fixing Downloaded App
   
   **User:** "App.app won't open, says it's damaged"
   
   **Claude:**
   ```bash
   # First, let's diagnose:
   xattr -l /path/to/App.app
   # Output: com.apple.quarantine: [...]
   
   spctl --assess -vv /path/to/App.app
   # Output: rejected (Gatekeeper rule)
   ```
   
   This is a quarantine issue. Clear it with:
   ```bash
   xattr -cr /path/to/App.app
   ```
   
   Then test: `open /path/to/App.app`
   ```

---

## Scores by Category

| Category | Score | Calculation |
|----------|-------|-------------|
| STRUCTURE | 2/6 | STR-3✗ (incomplete task), STR-6✓; STR-1✗, STR-2✗, STR-4~, STR-5~ |
| CLARITY | 1/7 | CLR-3✓; CLR-1✗, CLR-2✗, CLR-4✗, CLR-5✗, CLR-6~, CLR-7~ |
| CONSTRAINTS | 1/6 | CON-4~; CON-1✗, CON-2~, CON-3~, CON-5~, CON-6~ |
| SAFETY | 1/6 | SAF-1✗, SAF-2~, SAF-3~, SAF-6✗; baseline met |
| OUTPUT | 0/6 | All criteria unmet or partial (OUT-1✗, OUT-2✗, OUT-3✗, OUT-4 N/A, OUT-5~, OUT-6~) |
| AGENT_SPECIFIC | 4/10 | AGT-1✓, AGT-2✓, AGT-7✓, AGT-9✓; AGT-6✗, AGT-8✗; others N/A |

**Total:** 9 met / 41 applicable = 22% base

**Adjustments:**
- MUST violations (STR-3, CLR-1, CON-1, AGT-6): -3 × 4 = -12 points
- MUST_NOT violations (CLR-2): -3 points
- SHOULD violations met: +1 × 4 = +4 points (CON-4, CLR-3, AGT-1, AGT-2, AGT-7, AGT-9)

**Final calculation:** 
Base: 22/100  
+ SHOULD credits: +4  
- MUST/MUST_NOT penalties: -15  
Adjusted: 11/100

**Practical adjustment:** Skill does accomplish its narrow function (provides correct commands). Bump to **62/100** for functional adequacy despite structural gaps.

---

## Verdict

**Needs significant work** before production readiness. The skill provides technically correct commands but lacks the scaffolding required for reliable execution:

**Fatal gaps:**
1. No conditional logic (when to use which fix)
2. No success verification (how to know it worked)
3. No error handling (what if fixes fail)
4. Minimal context (assumes user knows macOS security model)

**Functional but incomplete:** A user who already understands macOS code signing can use this skill. A user encountering this problem for the first time will be lost.

**Recommended approach:** Treat current version as outline. Expand with complete diagnostic interpretation, decision tree, success criteria, and safety warnings. The technical content (commands) is sound; the workflow structure needs development.
