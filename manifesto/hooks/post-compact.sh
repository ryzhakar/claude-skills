#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGINS_CACHE_DIR="$(cd "$SCRIPT_DIR/../../../.." 2>/dev/null && pwd)"
if [[ "$PLUGINS_CACHE_DIR" != *"plugins"* ]] || [[ "$PLUGINS_CACHE_DIR" != *"cache"* ]]; then
    PLUGINS_CACHE_DIR="$HOME/.claude/plugins/cache"
fi
export PLUGINS_CACHE_DIR
source "$SCRIPT_DIR/ensure-repo.sh"

detect_manifestos

# Gate: no config → silent exit
YOU_EMPTY=false
{ [ -z "${YOU_STACK:-}" ] || [ "$YOU_STACK" = "[]" ]; } && YOU_EMPTY=true
if $YOU_EMPTY; then
    exit 0
fi

# PostCompact requires hookSpecificOutput JSON — plain text goes to debug log only.
emit_json() {
    python3 -c '
import json, sys
text = sys.stdin.read()
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostCompact", "additionalContext": text}}))
'
}

# Render orchestrator elements as natural language prose
ELEMENT_DESCRIPTION=$(python3 << 'PYEOF'
import json, os

stack = json.loads(os.environ["YOU_STACK"])
n = len(stack)
count_word = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight"}.get(n, str(n))
sentences = [f"Your constitution has {count_word} element{'s' if n != 1 else ''}."]

for el in stack:
    name = el["name"]
    purpose = el.get("purpose")
    source = el.get("source")
    if purpose and source:
        sentences.append(f'"{name}" governs your {purpose} — fetch it from {source}.' if source.startswith("http") else f'"{name}" governs your {purpose} — read it from {source}.')
    elif purpose:
        sentences.append(f'"{name}" governs your {purpose}.')
    elif source:
        sentences.append(f'"{name}" is part of your constitution — fetch it from {source}.' if source.startswith("http") else f'"{name}" is part of your constitution — read it from {source}.')
    else:
        sentences.append(f'"{name}" is part of your constitution.')

print(" ".join(sentences))
PYEOF
)

REBIND_NOTE="Previous bindings, oath state, and interplay analyses were lost in compaction. Re-read and rebind everything from source."

export ELEMENT_DESCRIPTION MANIFESTO_DIR REBIND_NOTE
PARTS_DIR="$SCRIPT_DIR/templates/parts"
SKILL_MD="$SCRIPT_DIR/../skills/manifesto-oath/SKILL.md"
{
    envsubst '${ELEMENT_DESCRIPTION} ${MANIFESTO_DIR} ${REBIND_NOTE} ${PLUGINS_CACHE_DIR}' < "$PARTS_DIR/preamble-compact.txt"
    echo ""
    envsubst '${ELEMENT_DESCRIPTION} ${MANIFESTO_DIR} ${REBIND_NOTE} ${PLUGINS_CACHE_DIR}' < "$PARTS_DIR/binding-core.txt"
    echo ""
    echo "## Manifesto Oath Protocol (injected from skill)"
    echo ""
    cat "$SKILL_MD"

    # Inline footer: compacted user-elements recovery + subagent dispatch note
    cat << 'FOOTER'

## User-Provided Constitution Elements

The elements above are the BASE STACK. If the user previously provided additional constitution elements in this session, those bindings were also lost in compaction.

User-provided elements cannot be reliably recovered from a compacted summary — the compaction may have elided exactly that information. Do not attempt to reconstruct them from inference. Instead: ask the user to re-specify any elements they added during the session before this compaction. Once re-specified, load and bind them using the same full protocol and layer them on top of the base stack.

## Subagent Constitution Dispatch

The SubagentStart hook injects role-matched constitution bindings into subagents automatically. You MAY add extra elements in dispatch prompts to augment the automatic stack.
FOOTER
} | emit_json
