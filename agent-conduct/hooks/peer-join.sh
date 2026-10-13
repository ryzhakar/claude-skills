#!/bin/bash
# SessionStart: print peer-protocol text. Argument: join | compact.
# Silent unless $HOME/.claude-peers exists. Never creates it. Never fails the session.
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$SCRIPT_DIR")}"

# Gate: no peers directory, no peer protocol.
[ -n "${HOME:-}" ] && [ -d "$HOME/.claude-peers" ] || exit 0

case "${1:-}" in
  join|compact) ;;
  *) exit 0 ;;
esac

TEMPLATE="$PLUGIN_ROOT/hooks/templates/peer-$1.txt"
[ -f "$TEMPLATE" ] && [ -r "$TEMPLATE" ] || exit 0

cat "$TEMPLATE" 2>/dev/null
exit 0
