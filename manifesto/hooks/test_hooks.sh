#!/bin/bash
set -uo pipefail
export PYTHONDONTWRITEBYTECODE=1

HOOKS_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "$HOOKS_DIR/.." && pwd)"
OATH_SKILL="$PLUGIN_ROOT/skills/manifesto-oath/SKILL.md"
REPO_ROOT="$(cd "$PLUGIN_ROOT/.." && pwd)"
LIVE_CONFIG="$REPO_ROOT/.manifestos.yaml"
MANIFESTO_DIR="${MANIFESTO_DIR:-/home/user/LLM_MANIFESTOS}"

MAX_CONTEXT_CHARS=8000
MAX_BINDING_SECTION_LINES=25
LOAD_COMMAND="Invoke the Skill tool with skill manifesto:manifesto-oath"
OATH_BODY_SENTENCE="You are a knight receiving an oath"
REINFORCEMENT_HEADING="Subagent Binding Reinforcement"
CLOSURE_RULE="until no unresolved references remain"
CAPPED_DEPTH="maximum depth of three levels"
RATIONALE_SENTENCES=(
    "Shortcuts here propagate as binding gaps"
    "Each skipped step produces a gap"
    "Shallow reading produces incomplete binding"
    "The binding determines whether your work survives review"
    "Silent binding is worthless"
)
SESSION_START_MATCHER="startup|resume|compact"
HOST_EVENT_NAMES="PreToolUse UserPromptSubmit UserPromptExpansion SessionStart Setup PreModelSwitch PostModelSwitch SubagentStart PostToolUse PostToolUseFailure PostToolBatch Stop SubagentStop PermissionDenied Notification PermissionRequest Elicitation ElicitationResult CwdChanged FileChanged WorktreeCreate MessageDisplay"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT
PROJECT_DIR="$WORK_DIR/project"
STUB_BIN="$WORK_DIR/stubbin"
CHECKS=0
FAILURES=0

prepare_project() {
    mkdir -p "$PROJECT_DIR" "$STUB_BIN"
    cp "$LIVE_CONFIG" "$PROJECT_DIR/.manifestos.yaml"
    printf '\nmanifesto_dir: %s\n' "$MANIFESTO_DIR" >> "$PROJECT_DIR/.manifestos.yaml"
    printf '#!/bin/sh\nexit 0\n' > "$STUB_BIN/git"
    chmod +x "$STUB_BIN/git"
}

check() {
    local label="$1" detail status
    shift
    CHECKS=$((CHECKS + 1))
    detail=$("$@" 2>&1)
    status=$?
    if [ "$status" -eq 0 ]; then
        echo "PASS  $label"
        return
    fi
    FAILURES=$((FAILURES + 1))
    echo "FAIL  $label"
    [ -n "$detail" ] && printf '%s\n' "$detail" | sed 's/^/        /'
}

run_hook() {
    local script="$1" stdin_json="$2" prefix="$3"
    (
        cd "$PROJECT_DIR" || exit 1
        printf '%s' "$stdin_json" | PATH="$STUB_BIN:$PATH" CLAUDE_PROJECT_DIR="$PROJECT_DIR" CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" bash "$HOOKS_DIR/$script" > "$prefix.stdout" 2> "$prefix.stderr"
        echo $? > "$prefix.status"
    )
}

exit_status_is_zero() {
    local status
    status=$(cat "$1.status")
    [ "$status" -eq 0 ] || { echo "exit status $status"; return 1; }
}

stderr_is_empty() {
    [ ! -s "$1.stderr" ] || { echo "stderr: $(head -c 300 "$1.stderr")"; return 1; }
}

stdout_is_json() {
    python3 - "$1.stdout" <<'PY'
import json, sys
try:
    json.load(open(sys.argv[1], encoding="utf-8"))
except ValueError as error:
    print("not JSON: %s" % error)
    sys.exit(1)
PY
}

event_name_is() {
    local expected="$2" name
    name=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["hookSpecificOutput"]["hookEventName"])' "$1.stdout" 2>/dev/null) || { echo "no hookSpecificOutput.hookEventName"; return 1; }
    [ "$name" = "$expected" ] || { echo "hookEventName $name, expected $expected"; return 1; }
    case " $HOST_EVENT_NAMES " in
        *" $name "*) return 0 ;;
    esac
    echo "host schema has no hookSpecificOutput variant $name"
    return 1
}

extract_context() {
    python3 - "$1.stdout" "$1.context" <<'PY'
import json, sys
raw = open(sys.argv[1], encoding="utf-8").read()
try:
    text = json.loads(raw)["hookSpecificOutput"]["additionalContext"]
except (ValueError, KeyError, TypeError):
    text = raw
open(sys.argv[2], "w", encoding="utf-8").write(text)
PY
}

char_count() {
    python3 -c 'import sys; print(len(open(sys.argv[1], encoding="utf-8").read()))' "$1"
}

chars_below_limit() {
    local count
    count=$(char_count "$1")
    [ "$count" -lt "$MAX_CONTEXT_CHARS" ] || { echo "$count characters, limit $MAX_CONTEXT_CHARS"; return 1; }
}

contains_text() {
    grep -qF -- "$2" "$1" || { echo "missing: $2"; return 1; }
}

lacks_text() {
    ! grep -qF -- "$2" "$1" || { echo "present: $2"; return 1; }
}

lacks_text_ignoring_case() {
    ! grep -qiF -- "$2" "$1" || { echo "present: $2"; return 1; }
}

lacks_every_rationale_sentence() {
    local sentence present=0
    for sentence in "${RATIONALE_SENTENCES[@]}"; do
        lacks_text "$1" "$sentence" || present=1
    done
    return "$present"
}

element_needles() {
    python3 "$HOOKS_DIR/parse_config.py" "$PROJECT_DIR" | python3 -c '
import json, sys
lines = sys.stdin.read().split("\n")
scope, fields = sys.argv[1], sys.argv[2].split(",")
if scope == "you":
    elements = json.loads(lines[0])
else:
    elements = json.loads(lines[1])[scope.split(":", 1)[1]]
for element in elements:
    for field in fields:
        if element.get(field):
            print(element[field])
' "$1" "$2"
}

contains_every_element() {
    local file="$1" scope="$2" fields="$3" needle missing=0 total=0
    while IFS= read -r needle; do
        total=$((total + 1))
        grep -qF -- "$needle" "$file" || { echo "missing: $needle"; missing=1; }
    done < <(element_needles "$scope" "$fields")
    [ "$total" -gt 0 ] || { echo "config scope $scope yields no elements"; return 1; }
    return "$missing"
}

binding_section_fits() {
    local count
    count=$(awk '/^## Binding Required/ {on=1; next} on && (/^## / || /^Manifesto repo:/) {exit} on {n++} END {print n+0}' "$1")
    [ "$count" -le "$MAX_BINDING_SECTION_LINES" ] || { echo "$count lines, limit $MAX_BINDING_SECTION_LINES"; return 1; }
}

verify_binding_context() {
    local label="$1" prefix="$2" event="$3"
    check "$label: exit status 0" exit_status_is_zero "$prefix"
    check "$label: stderr empty" stderr_is_empty "$prefix"
    check "$label: stdout parses as JSON" stdout_is_json "$prefix"
    check "$label: hookEventName is $event and host-accepted" event_name_is "$prefix" "$event"
    extract_context "$prefix"
    check "$label: stdout under $MAX_CONTEXT_CHARS characters" chars_below_limit "$prefix.stdout"
    check "$label: additionalContext under $MAX_CONTEXT_CHARS characters" chars_below_limit "$prefix.context"
    check "$label: carries the load command" contains_text "$prefix.context" "$LOAD_COMMAND"
    check "$label: carries no oath skill body" lacks_text "$prefix.context" "$OATH_BODY_SENTENCE"
    check "$label: names the manifesto dir" contains_text "$prefix.context" "Manifesto repo: $MANIFESTO_DIR/"
    check "$label: names the plugin cache path" contains_text "$prefix.context" "Plugin cache: "
    check "$label: binding section within $MAX_BINDING_SECTION_LINES lines" binding_section_fits "$prefix.context"
    check "$label: states the oath skill's closure rule" contains_text "$prefix.context" "$CLOSURE_RULE"
    check "$label: sets no depth cap" lacks_text "$prefix.context" "$CAPPED_DEPTH"
    check "$label: omits rationale sentences" lacks_every_rationale_sentence "$prefix.context"
}

verify_session_start() {
    local source="$1" prefix="$WORK_DIR/session-$1"
    local stdin_json="{\"session_id\":\"test\",\"transcript_path\":\"/dev/null\",\"cwd\":\"$PROJECT_DIR\",\"hook_event_name\":\"SessionStart\",\"source\":\"$source\"}"
    run_hook session-start.sh "$stdin_json" "$prefix"
    verify_binding_context "SessionStart $source" "$prefix" SessionStart
    check "SessionStart $source: names every you: element and purpose" contains_every_element "$prefix.context" you name,purpose,source
    check "SessionStart $source: says which source fired" contains_text "$prefix.context" "Session source: $source."
    check "SessionStart $source: keeps the subagent reinforcement footer" contains_text "$prefix.context" "$REINFORCEMENT_HEADING"
}

verify_subagent_start() {
    local agent_type="$1" scope="$2" prefix="$WORK_DIR/subagent-${1//[:\/]/_}"
    local stdin_json="{\"session_id\":\"test\",\"transcript_path\":\"/dev/null\",\"cwd\":\"$PROJECT_DIR\",\"hook_event_name\":\"SubagentStart\",\"agent_id\":\"a1\",\"agent_type\":\"$agent_type\"}"
    run_hook subagent-start.sh "$stdin_json" "$prefix"
    verify_binding_context "SubagentStart $agent_type" "$prefix" SubagentStart
    if [ -n "$scope" ]; then
        check "SubagentStart $agent_type: names every element and purpose" contains_every_element "$prefix.context" "$scope" name,purpose,source
    else
        check "SubagentStart $agent_type: states no element matched" contains_text "$prefix.context" "No role-specific elements matched"
    fi
}

verify_prompt_reminder() {
    local prefix="$WORK_DIR/prompt"
    run_hook drift-reminder.sh '{"session_id":"test","hook_event_name":"UserPromptSubmit","prompt":"hello"}' "$prefix"
    cp "$prefix.stdout" "$prefix.context"
    check "UserPromptSubmit: exit status 0" exit_status_is_zero "$prefix"
    check "UserPromptSubmit: stderr empty" stderr_is_empty "$prefix"
    check "UserPromptSubmit: stdout under $MAX_CONTEXT_CHARS characters" chars_below_limit "$prefix.stdout"
    check "UserPromptSubmit: names every you: element" contains_every_element "$prefix.context" you name
    check "UserPromptSubmit: carries no oath skill body" lacks_text "$prefix.context" "$OATH_BODY_SENTENCE"
}

hooks_json_has_no_post_compact() {
    python3 - "$HOOKS_DIR/hooks.json" <<'PY'
import json, sys
events = json.load(open(sys.argv[1]))["hooks"]
if "PostCompact" in events:
    print("hooks.json registers PostCompact")
    sys.exit(1)
PY
}

hooks_json_session_start_matcher_is() {
    local matcher
    matcher=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["hooks"]["SessionStart"][0]["matcher"])' "$HOOKS_DIR/hooks.json")
    [ "$matcher" = "$1" ] || { echo "matcher $matcher, expected $1"; return 1; }
}

hooks_json_commands_exist() {
    python3 - "$HOOKS_DIR/hooks.json" "$PLUGIN_ROOT" <<'PY'
import json, os, sys
events = json.load(open(sys.argv[1]))["hooks"]
missing = []
for groups in events.values():
    for group in groups:
        for hook in group["hooks"]:
            path = hook["command"].split()[-1].replace("${CLAUDE_PLUGIN_ROOT}", sys.argv[2])
            if not os.path.isfile(path):
                missing.append(path)
for path in missing:
    print("missing script: %s" % path)
sys.exit(1 if missing else 0)
PY
}

skill_tier_one_line() {
    grep -m1 '^\*\*Tier 1' "$OATH_SKILL"
}

skill_tier_one_defers_to_hook() {
    local line
    line=$(skill_tier_one_line) || { echo "no Tier 1 line"; return 1; }
    case "$line" in
        *'`Manifesto repo:`'*) ;;
        *) echo "Tier 1 does not name the Manifesto repo: line"; return 1 ;;
    esac
    ! printf '%s' "$line" | grep -qE '(^|[ `(])/[A-Za-z]' || { echo "Tier 1 names an absolute path"; return 1; }
}

file_is_absent() {
    [ ! -e "$1" ] || { echo "present: $1"; return 1; }
}

verify_hook_registration() {
    check "hooks.json: SessionStart matcher is $SESSION_START_MATCHER" hooks_json_session_start_matcher_is "$SESSION_START_MATCHER"
    check "hooks.json: no PostCompact event" hooks_json_has_no_post_compact
    check "hooks.json: every command script exists" hooks_json_commands_exist
    check "post-compact.sh deleted" file_is_absent "$HOOKS_DIR/post-compact.sh"
    check "preamble-compact.txt deleted" file_is_absent "$HOOKS_DIR/templates/parts/preamble-compact.txt"
    check "oath skill Tier 1 takes the manifesto dir from the hook injection" skill_tier_one_defers_to_hook
}

main() {
    prepare_project
    verify_hook_registration
    local source
    for source in startup resume compact; do
        verify_session_start "$source"
    done
    verify_subagent_start instruction-writer subagents:instruction-writer
    verify_subagent_start manifesto:maximalist-reviewer ""
    verify_prompt_reminder
    echo
    echo "$((CHECKS - FAILURES))/$CHECKS checks passed"
    [ "$FAILURES" -eq 0 ]
}

main
