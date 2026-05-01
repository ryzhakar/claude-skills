#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/ensure-repo.sh"

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
detect_manifestos

# Gate: no config → silent exit
if [ -z "${YOU_STACK:-}" ] || [ "$YOU_STACK" = "[]" ]; then
    exit 0
fi

export MANIFESTO_DIR

python3 << 'PYEOF'
import json, os, yaml, glob

stack = json.loads(os.environ.get("YOU_STACK", "[]"))
manifesto_dir = os.environ.get("MANIFESTO_DIR", "")
manifestos_path = os.path.join(manifesto_dir, "manifestos") if manifesto_dir else ""

taglines = []
for el in stack:
    name = el.get("name", "")
    if not name:
        continue

    if manifestos_path and os.path.isdir(manifestos_path):
        name_lower = name.lower().replace("-", " ").replace("_", " ")
        for md_file in glob.glob(os.path.join(manifestos_path, "*.md")):
            try:
                with open(md_file) as f:
                    content = f.read()
                if content.startswith("---"):
                    end = content.index("---", 3)
                    fm = yaml.safe_load(content[3:end])
                    if isinstance(fm, dict):
                        file_name = os.path.splitext(os.path.basename(md_file))[0]
                        title = fm.get("title", "").lower()
                        file_slug = file_name.lower().replace("-", " ")
                        if (name_lower in file_slug or
                                file_slug in name_lower or
                                name_lower in title):
                            tagline = fm.get("tagline", "")
                            if tagline:
                                taglines.append(tagline)
                            break
            except Exception:
                continue

if taglines:
    reminder = "Active bindings: " + " · ".join(f'"{t}"' for t in taglines)
    # Keep under 200 chars
    if len(reminder) > 200:
        reminder = reminder[:197] + "..."
    print(reminder)
PYEOF

exit 0
