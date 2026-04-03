---
name: fix-macos-app
description: This skill should be used when the user asks to "fix a broken app", "app won't open", "Gatekeeper blocks app", "can't launch app", "app is damaged", "clear quarantine", "re-sign app", "fix code signing", or mentions macOS security preventing an app from launching.
---

# Fix Broken macOS App Bundles

Diagnose and fix `.app` bundles that fail to launch due to Gatekeeper, quarantine, or broken code signatures. Common with apps distributed outside the Mac App Store.

Diagnose with `xattr -l`, `codesign -dv --verbose=2`, `spctl --assess`, and `file` on the binary. Then apply fixes in order, testing launch after each:

1. **Clear quarantine:** `xattr -cr /path/to/App.app`
2. **Re-sign ad-hoc:** `codesign --force --deep --sign - /path/to/App.app`

## Critical Pitfalls

- **Never just remove a signature** (`codesign --remove-signature`) without re-signing. macOS refuses to launch unsigned binaries (POSIX error 153).
- **Clear quarantine before re-signing.** Quarantine can interfere with the signing process.
