#!/usr/bin/env python3
"""Parse the block-style YAML subset used by .manifestos.yaml and manifesto
frontmatter: nested mappings and sequences of string scalars, two-space
indented, no anchors, no flow collections, no multiline scalars. Avoids a
PyYAML dependency that is not guaranteed present on the host's python3."""


def _strip_quotes(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def _scalar(s):
    s = s.strip()
    if s in ("", "~", "null"):
        return None
    return _strip_quotes(s)


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _parse_block(lines, i, indent):
    if i >= len(lines) or _indent(lines[i]) != indent:
        return None, i

    if lines[i].lstrip().startswith("- "):
        result = []
        while i < len(lines) and _indent(lines[i]) == indent and lines[i].lstrip().startswith("- "):
            content = lines[i].lstrip()[2:]
            item_indent = indent + 2
            if ":" in content:
                block = [" " * item_indent + content]
                j = i + 1
                while j < len(lines) and _indent(lines[j]) >= item_indent:
                    block.append(lines[j])
                    j += 1
                value, _ = _parse_block(block, 0, item_indent)
                result.append(value)
                i = j
            else:
                result.append(_scalar(content))
                i += 1
        return result, i

    result = {}
    while i < len(lines) and _indent(lines[i]) == indent and not lines[i].lstrip().startswith("- "):
        key, _, rest = lines[i].lstrip().partition(":")
        key = _strip_quotes(key)
        rest = rest.strip()
        if rest:
            result[key] = _scalar(rest)
            i += 1
        elif i + 1 < len(lines) and _indent(lines[i + 1]) > indent:
            result[key], i = _parse_block(lines, i + 1, _indent(lines[i + 1]))
        else:
            result[key] = None
            i += 1
    return result, i


def safe_load(text):
    """Return the parsed structure, or None for empty input."""
    lines = [ln.rstrip() for ln in text.split("\n") if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        return None
    value, _ = _parse_block(lines, 0, _indent(lines[0]))
    return value
