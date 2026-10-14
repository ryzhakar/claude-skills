#!/bin/bash
# SessionStart: print peer-protocol text. Argument: join | compact.
# Silent unless the registry root exists. Never creates it. Never fails the session.
set -u
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$SCRIPT_DIR")}"

# Gate: no registry directory, no peer protocol.
ROOT="${CLAUDE_PEERS_ROOT:-}"
if [ -z "$ROOT" ]; then
  if [ -n "${XDG_DATA_HOME:-}" ]; then ROOT="$XDG_DATA_HOME/claude-peers"
  elif [ -n "${HOME:-}" ]; then ROOT="$HOME/.local/share/claude-peers"
  fi
fi
[ -n "$ROOT" ] && [ -d "$ROOT" ] || exit 0

case "${1:-}" in
  join|compact) ;;
  *) exit 0 ;;
esac

TEMPLATE="$PLUGIN_ROOT/hooks/templates/peer-$1.txt"
[ -f "$TEMPLATE" ] && [ -r "$TEMPLATE" ] || exit 0

ESCAPED_ROOT="$(printf '%s' "$ROOT" | sed -e 's/[&|\\]/\\&/g')"
sed -e "s|<root>|$ESCAPED_ROOT|g" "$TEMPLATE" 2>/dev/null
exit 0
