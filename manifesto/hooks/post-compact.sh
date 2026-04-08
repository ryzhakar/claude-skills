#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
manifestos=$(detect_manifestos)

RESOLVE_INSTRUCTIONS="To resolve each entry:
- Plain name (e.g. 'decomplect'): find the matching file in ${MANIFESTO_DIR}/manifestos/ by keyword
- URL (starts with http): fetch the full text
- Local path (starts with ./ or /): read relative to ${PROJECT_DIR}"

if [ -n "$manifestos" ]; then
    escaped=$(escape_json "$manifestos")
    cat <<EOF
MANIFESTO RE-BINDING REQUIRED — context was just compacted.

Declared manifestos:
${escaped}

${RESOLVE_INSTRUCTIONS}

Re-load each manifesto's full text and re-apply the manifesto-oath skill. Previous bindings did not survive compaction. This is non-negotiable.
EOF
else
    cat <<EOF
MANIFESTO PLUGIN ACTIVE — context was just compacted. If manifestos were previously bound, re-apply the manifesto-oath skill. Repo manifestos available in: ${MANIFESTO_DIR}/manifestos/.
EOF
fi
