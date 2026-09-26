#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$SCRIPT_DIR")}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# Gate: no marker, no silence to restore.
[ -f "$PROJECT_DIR/.claude/work-silently" ] || exit 0

cat "$SCRIPT_DIR/templates/silence-mandate.txt"
echo
# Skill body at runtime, frontmatter stripped.
awk 'fm < 2 { if ($0 == "---") fm++; next } { print }' "$PLUGIN_ROOT/skills/work-silently/SKILL.md"
exit 0
