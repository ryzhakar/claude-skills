#!/usr/bin/env python3
"""Resolve taglines for YOU_STACK elements from the MANIFESTO_DIR manifesto files."""

import glob
import json
import os
import sys


def load_frontmatter(path):
    """Return the YAML frontmatter dict from a markdown file, or None."""
    try:
        with open(path) as f:
            content = f.read()
        if not content.startswith("---"):
            return None
        end = content.index("---", 3)
        import yaml
        fm = yaml.safe_load(content[3:end])
        return fm if isinstance(fm, dict) else None
    except Exception:
        return None


def build_manifesto_lookup(manifesto_dir):
    """Read all *.md files once; return list of (slug, title_lower, tagline)."""
    manifestos_path = os.path.join(manifesto_dir, "manifestos")
    if not os.path.isdir(manifestos_path):
        return []

    entries = []
    for path in glob.glob(os.path.join(manifestos_path, "*.md")):
        fm = load_frontmatter(path)
        if fm is None:
            continue
        slug = os.path.splitext(os.path.basename(path))[0].lower().replace("-", " ")
        title = fm.get("title", "").lower()
        tagline = fm.get("tagline", "")
        entries.append((slug, title, tagline))
    return entries


def find_tagline(name, entries):
    """Return tagline string if found, empty string if found but no tagline, None if no match."""
    name_lower = name.lower().replace("-", " ").replace("_", " ")
    for slug, title, tagline in entries:
        if name_lower in slug or slug in name_lower or name_lower in title:
            return tagline  # may be empty string
    return None


def main():
    stack_raw = os.environ.get("YOU_STACK", "")
    if not stack_raw:
        sys.exit(0)

    try:
        stack = json.loads(stack_raw)
    except Exception:
        sys.exit(0)

    if not stack:
        sys.exit(0)

    manifesto_dir = os.environ.get("MANIFESTO_DIR", "")
    entries = build_manifesto_lookup(manifesto_dir) if manifesto_dir else []

    parts = []
    for el in stack:
        name = el.get("name", "")
        if not name:
            continue

        result = find_tagline(name, entries)
        if result:
            parts.append(f'{name}: "{result}"')
        else:
            parts.append(name)

    if parts:
        print("Active bindings: " + " · ".join(parts))


if __name__ == "__main__":
    main()
