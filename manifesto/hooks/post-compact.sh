#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
detect_manifestos

# Gate: no config → silent exit (both sections empty)
YOU_EMPTY=false
SUB_EMPTY=false
{ [ -z "${YOU_STACK:-}" ] || [ "$YOU_STACK" = "[]" ]; } && YOU_EMPTY=true
{ [ -z "${SUBAGENT_SECTION:-}" ] || [ "$SUBAGENT_SECTION" = "{}" ]; } && SUB_EMPTY=true
if $YOU_EMPTY && $SUB_EMPTY; then
    exit 0
fi

# Render orchestrator elements as natural language prose
if $YOU_EMPTY; then
    ELEMENT_DESCRIPTION="No orchestrator-specific constitution elements are configured."
else
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
fi

SUBAGENT_NOTE=$(python3 << 'PYEOF'
import json, os

sub = json.loads(os.environ.get("SUBAGENT_SECTION", "{}"))
if not sub:
    print("No subagent-specific constitution bindings are configured.")
else:
    lines = ["When dispatching subagents, embed the relevant bindings in each dispatch prompt. Subagents do not inherit your constitution — you supply theirs."]
    for role, elements in sub.items():
        role_label = f'Role "{role}"' if role != "other" else "All other subagents"
        el_parts = []
        for el in elements:
            name = el["name"]
            purpose = el.get("purpose")
            source = el.get("source")
            if purpose and source:
                verb = "fetch from" if source.startswith("http") else "read from"
                el_parts.append(f'"{name}" ({purpose}, {verb} {source})')
            elif purpose:
                el_parts.append(f'"{name}" ({purpose})')
            elif source:
                verb = "fetch from" if source.startswith("http") else "read from"
                el_parts.append(f'"{name}" ({verb} {source})')
            else:
                el_parts.append(f'"{name}"')
        lines.append(f"{role_label}: {', '.join(el_parts)}.")
    print(" ".join(lines))
PYEOF
)

PREAMBLE="MANDATORY CONSTITUTION RE-BINDING — CONTEXT WAS JUST COMPACTED.

Your previous constitutional bindings DID NOT survive compaction. They are DESTROYED. Every manifesto, every interplay analysis, every tension resolution, every unified operating mode — GONE.

You MUST reconstruct the entire binding from scratch NOW before doing ANY other work."

HOOK_TRIGGER="per compaction"

REBIND_NOTE="Your previous reads are DESTROYED. You must re-read everything from scratch. Previous bindings, oath state, and interplay analyses are GONE — rebuild completely from zero."

USER_ELEMENTS_NOTE="The elements above are the BASE STACK. If the user previously provided additional constitution elements in this session, those bindings are ALSO destroyed by compaction.

User-provided elements cannot be reliably recovered from a compacted summary — the compaction may have elided exactly that information. Do not attempt to reconstruct them from inference. Instead: ask the user to re-specify any elements they added during the session before this compaction. Once re-specified, load and bind them using the same full protocol and layer them on top of the base stack."

export ELEMENT_DESCRIPTION SUBAGENT_NOTE MANIFESTO_DIR PROJECT_DIR PREAMBLE HOOK_TRIGGER REBIND_NOTE USER_ELEMENTS_NOTE
envsubst '${ELEMENT_DESCRIPTION} ${SUBAGENT_NOTE} ${MANIFESTO_DIR} ${PROJECT_DIR} ${PREAMBLE} ${HOOK_TRIGGER} ${REBIND_NOTE} ${USER_ELEMENTS_NOTE}' < "$SCRIPT_DIR/templates/constitution-binding.txt"
