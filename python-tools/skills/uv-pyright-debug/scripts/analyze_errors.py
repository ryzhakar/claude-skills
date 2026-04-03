#!/usr/bin/env python3
"""
Analyze pyright JSON output to identify error patterns and frequency.
Usage: uv run pyright file.py --outputjson | python3 analyze_errors.py
"""
import json
import sys
from collections import Counter


def main():
    data = json.load(sys.stdin)
    errors = data.get("generalDiagnostics", [])

    if not errors:
        print("✅ No errors found!")
        return

    # Pattern analysis
    patterns = Counter()
    rules = Counter()

    for error in errors:
        msg = error["message"]
        rule = error.get("rule", "unknown")
        rules[rule] += 1

        # Categorize by message pattern
        if "Arguments missing" in msg:
            patterns["Arguments missing (multiple params)"] += 1
        elif "Argument missing" in msg:
            patterns["Argument missing (single param)"] += 1
        elif "No parameter named" in msg:
            patterns["No parameter named"] += 1
        elif "cannot be assigned" in msg:
            patterns["Type mismatch"] += 1
        elif "not defined" in msg:
            patterns["Name not defined"] += 1
        else:
            patterns["Other"] += 1

    # Report summary
    print(f"📊 Pyright Error Analysis")
    print(f"{'='*60}")
    print(f"Total errors: {len(errors)}")
    print()

    print("Error Pattern Distribution:")
    for pattern, count in patterns.most_common():
        pct = (count / len(errors)) * 100
        print(f"  {pattern:40} {count:4} ({pct:5.1f}%)")
    print()

    print("Top Error Rules:")
    for rule, count in rules.most_common(5):
        print(f"  {rule:40} {count:4}")
    print()

    # Show first 10 errors with line numbers
    print("First 10 Errors (with line numbers):")
    for i, error in enumerate(errors[:10], 1):
        line = error["range"]["start"]["line"] + 1
        msg = error["message"][:100]
        print(f"  {i:2}. Line {line:4}: {msg}")


if __name__ == "__main__":
    main()
