#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 <pollution-path> <test-command> <test-file>..." >&2
  echo "example: $0 .git 'uv run pytest' tests/test_*.py" >&2
  exit 64
}

[ $# -ge 3 ] || usage

pollution_path="$1"
test_command="$2"
shift 2

if [ -e "$pollution_path" ]; then
  echo "pollution exists before any test: $pollution_path" >&2
  exit 2
fi

for test_file in "$@"; do
  if $test_command "$test_file" > /dev/null 2>&1; then rc=0; else rc=$?; fi
  echo "testing: $test_file (exit $rc)"
  if [ -e "$pollution_path" ]; then
    echo "polluter: $test_file"
    echo "created: $pollution_path"
    ls -la "$pollution_path"
    exit 1
  fi
done
echo "no polluter among $# test files"
