#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
detect_manifestos

# Gate: no config → silent exit
if [ -z "${YOU_STACK:-}" ] && [ -z "${SUBAGENT_SECTION:-}" ]; then
    exit 0
fi
if [ "${YOU_STACK:-[]}" = "[]" ] && [ "${SUBAGENT_SECTION:-\{\}}" = "{}" ]; then
    exit 0
fi

PARTS_DIR="$SCRIPT_DIR/templates/parts"

# Wrap text in the hookSpecificOutput JSON required by SubagentStart hooks.
# Plain text stdout is silently discarded; only this wrapper is injected.
emit_json() {
    python3 -c '
import json, sys
text = sys.stdin.read()
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": text}}))
'
}

# Static fallback for unmatched/missing agent types
emit_static_fallback() {
    ELEMENT_DESCRIPTION="No role-specific elements matched. Your orchestrator provides bindings in the dispatch prompt."
    REBIND_NOTE=""
    export ELEMENT_DESCRIPTION MANIFESTO_DIR PROJECT_DIR REBIND_NOTE
    {
        envsubst '${ELEMENT_DESCRIPTION} ${MANIFESTO_DIR} ${PROJECT_DIR} ${REBIND_NOTE}' < "$PARTS_DIR/preamble-subagent.txt"
        echo ""
        cat << 'FALLBACK'
If your dispatch prompt contains a constitution-binding preamble, locate and invoke `manifesto-oath` to execute binding. NEVER substitute shallow reading for the oath protocol — shallow binding produces degraded constitutional compliance and the orchestrator will reject your output.

If NO binding preamble was provided, state this explicitly in your first line of output: "No constitution binding supplied by orchestrator."

The binding determines whether your work survives review.
FALLBACK
    } | emit_json
}

# Read agent_type from stdin JSON; handle missing/malformed input
AGENT_TYPE=$(python3 -c '
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get("agent_type", ""))
except:
    print("")
' 2>/dev/null || echo "")
export AGENT_TYPE

# If SUBAGENT_SECTION is empty/missing, emit static fallback
if [ -z "${SUBAGENT_SECTION:-}" ] || [ "${SUBAGENT_SECTION}" = "{}" ]; then
    emit_static_fallback
    exit 0
fi

# Match agent_type against SUBAGENT_SECTION keys using robust cascade
MATCHED_ELEMENTS=$(python3 << 'PYEOF'
import json, os, sys

agent_type = os.environ.get("AGENT_TYPE", "").strip()
sub_raw = os.environ.get("SUBAGENT_SECTION", "{}")

try:
    sub = json.loads(sub_raw)
except:
    sub = {}

if not sub or not isinstance(sub, dict):
    sys.exit(1)

def match_key(agent_type, keys):
    """Robust cascade: exact → strip-prefix → suffix → other."""
    if not agent_type:
        return keys.get("other")

    # a. Exact match
    if agent_type in keys:
        return keys[agent_type]

    # b. Strip prefix (qualified name → bare name)
    bare = agent_type.split(":")[-1] if ":" in agent_type else None
    if bare and bare in keys:
        return keys[bare]

    # c. Suffix match — any key is a suffix of agent_type
    for k in keys:
        if k != "other" and agent_type.endswith(k):
            return keys[k]

    # d. Fall back to other
    return keys.get("other")

elements = match_key(agent_type, sub)
if elements is None:
    sys.exit(1)

print(json.dumps(elements))
PYEOF
) || true

if [ -z "$MATCHED_ELEMENTS" ]; then
    emit_static_fallback
    exit 0
fi

# Render matched elements as natural language
export MATCHED_ELEMENTS
ELEMENT_DESCRIPTION=$(python3 << 'PYEOF'
import json, os

elements = json.loads(os.environ["MATCHED_ELEMENTS"])
n = len(elements)
count_word = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight"}.get(n, str(n))
sentences = [f"Your constitution has {count_word} element{'s' if n != 1 else ''}."]

for el in elements:
    name = el["name"]
    purpose = el.get("purpose")
    source = el.get("source")
    if purpose and source:
        verb = "fetch it from" if source.startswith("http") else "read it from"
        sentences.append(f'"{name}" governs your {purpose} — {verb} {source}.')
    elif purpose:
        sentences.append(f'"{name}" governs your {purpose}.')
    elif source:
        verb = "fetch it from" if source.startswith("http") else "read it from"
        sentences.append(f'"{name}" is part of your constitution — {verb} {source}.')
    else:
        sentences.append(f'"{name}" is part of your constitution.')

print(" ".join(sentences))
PYEOF
)

REBIND_NOTE=""

export ELEMENT_DESCRIPTION MANIFESTO_DIR PROJECT_DIR REBIND_NOTE
{
    envsubst '${ELEMENT_DESCRIPTION} ${MANIFESTO_DIR} ${PROJECT_DIR} ${REBIND_NOTE}' < "$PARTS_DIR/preamble-subagent.txt"
    echo ""
    envsubst '${ELEMENT_DESCRIPTION} ${MANIFESTO_DIR} ${PROJECT_DIR} ${REBIND_NOTE}' < "$PARTS_DIR/binding-core.txt"

    # Inline footer: subagent extra elements
    cat << 'FOOTER'

If your dispatch prompt contains additional constitution elements beyond those listed here, bind those as well using the same protocol.
FOOTER
} | emit_json
