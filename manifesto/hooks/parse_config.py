#!/usr/bin/env python3
"""Read .manifestos.yaml, or the Active Manifestos section of CLAUDE.md, from
the project directory given as argv[1]. Prints three lines to stdout: the
you-stack as JSON, the subagents section as JSON, and the manifesto_dir
override (empty string if unset)."""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mini_yaml import safe_load


def normalize_item(item):
    if item is None:
        return None
    if isinstance(item, dict):
        return item
    return {"name": str(item)}


def normalize_list(items):
    if not isinstance(items, list):
        return []
    return [x for x in (normalize_item(i) for i in items) if x is not None]


def read_raw(project_dir):
    config_file = os.path.join(project_dir, ".manifestos.yaml")
    if os.path.isfile(config_file):
        with open(config_file) as f:
            return f.read()

    claude_md = os.path.join(project_dir, "CLAUDE.md")
    if os.path.isfile(claude_md):
        with open(claude_md) as f:
            content = f.read()
        m = re.search(r"^## Active Manifestos\n(.*?)(?=^## |\Z)", content, re.M | re.S)
        if m:
            return m.group(1)

    return ""


def main():
    project_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    raw = read_raw(project_dir).strip()

    you_stack, subagent_section, manifesto_dir = [], {}, ""

    if raw:
        try:
            data = safe_load(raw)
        except Exception:
            data = None

        if isinstance(data, list):
            you_stack = normalize_list(data)
        elif isinstance(data, dict):
            you_stack = normalize_list(data.get("you", []))
            sub_raw = data.get("subagents", {})
            if isinstance(sub_raw, dict):
                for role, items in sub_raw.items():
                    if isinstance(items, list):
                        subagent_section[role] = normalize_list(items)
            manifesto_dir = data.get("manifesto_dir") or ""

    print(json.dumps(you_stack))
    print(json.dumps(subagent_section))
    print(manifesto_dir)


if __name__ == "__main__":
    main()
