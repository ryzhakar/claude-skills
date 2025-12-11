#!/usr/bin/env python3
"""
Create line-indexed error report from pyright JSON output.
Usage: uv run pyright file.py --outputjson | python3 line_index_errors.py

Outputs: L<line>: <error_message>
Perfect for pre-surveying before AST-based mass edits.
"""
import json
import sys
from collections import defaultdict


def main():
    data = json.load(sys.stdin)
    errors = data.get("generalDiagnostics", [])

    if not errors:
        print("✅ No errors found!")
        return

    # Group errors by line number
    by_line = defaultdict(list)
    for error in errors:
        line = error["range"]["start"]["line"] + 1
        msg = error["message"]
        by_line[line].append(msg)

    # Print line-indexed report
    print(f"Line-Indexed Error Report ({len(errors)} total errors)")
    print("=" * 80)

    for line in sorted(by_line.keys()):
        messages = by_line[line]
        print(f"\nL{line}: ({len(messages)} errors)")
        for msg in messages:
            print(f"  • {msg}")


if __name__ == "__main__":
    main()
