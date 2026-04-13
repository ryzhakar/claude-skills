# Core Points Analysis: fix-macos-app

## Iteration 1

**Point**: The skill addresses macOS Gatekeeper and quarantine issues that prevent apps distributed outside the Mac App Store from launching.

**Evidence**:
- Line 3: Description triggers include "Gatekeeper blocks app", "can't launch app", "app is damaged", "clear quarantine"
- Line 8: "Diagnose and fix `.app` bundles that fail to launch due to Gatekeeper, quarantine, or broken code signatures. Common with apps distributed outside the Mac App Store."
- Line 12: First fix step is "Clear quarantine: `xattr -cr /path/to/App.app`"

## Iteration 2

**Point**: Diagnostic commands must be run before applying fixes to understand the specific issue.

**Evidence**:
- Line 10: "Diagnose with `xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file` on the binary."
- Line 10: "Then apply fixes in order, testing launch after each:" (implies diagnosis comes first)
- Line 8: "Diagnose and fix" (diagnosis listed before fixing)

## Iteration 3

**Point**: Never remove code signatures without immediately re-signing, as macOS refuses to launch unsigned binaries.

**Evidence**:
- Line 17: "Never just remove a signature (`codesign --remove-signature`) without re-signing. macOS refuses to launch unsigned binaries (POSIX error 153)."
- Line 16: Section titled "Critical Pitfalls" emphasizes this is a critical mistake
- Line 13: The recommended fix is "Re-sign ad-hoc: `codesign --force --deep --sign - /path/to/App.app`" (re-signing, not removing)

## Iteration 4

**Point**: Fixes must be applied in a specific order: clear quarantine first, then re-sign.

**Evidence**:
- Line 10: "Then apply fixes in order, testing launch after each:"
- Line 12-13: Lists "1. Clear quarantine" followed by "2. Re-sign ad-hoc"
- Line 18: "Clear quarantine before re-signing. Quarantine can interfere with the signing process."

## Iteration 5

**Point**: The skill file is short and contains only 4 distinct core points.

**Evidence**:
The file is only 19 lines long and covers:
1. The problem domain (Gatekeeper/quarantine issues)
2. Diagnostic approach
3. Critical pitfall (never remove without re-signing)
4. Correct fix ordering

There are no additional distinct, pervasive points beyond these four. The content is intentionally focused and concise, providing specific commands and warnings without elaboration.

## Rank Summary

1. **Most Important**: Never remove code signatures without re-signing (Iteration 3) - This is explicitly called out as a "Critical Pitfall" and explains the severe consequence (POSIX error 153, app won't launch).

2. **Second**: Fixes must be applied in specific order: quarantine first, then re-sign (Iteration 4) - Also in the "Critical Pitfalls" section and explains why (quarantine interferes with signing).

3. **Third**: The skill addresses Gatekeeper/quarantine for non-App Store apps (Iteration 1) - Defines the entire problem domain and scope.

4. **Fourth**: Diagnostic commands precede fixes (Iteration 2) - Important procedural point but less emphasized than the critical pitfalls.

5. **N/A**: Only 4 distinct points exist in this concise skill file (Iteration 5) - The skill is intentionally brief and focused.
