FENCE = "---"


class UnclosedFrontmatter(ValueError):
    """Raised when a text opens a frontmatter block it never closes."""


def strip_frontmatter(text: str, path: str) -> str:
    """Return the text without its leading frontmatter block, refusing an unclosed block."""
    lines = text.split("\n")
    if lines[0] != FENCE:
        return text
    closing_index = next((i for i, line in enumerate(lines[1:], 1) if line == FENCE), None)
    if closing_index is None:
        raise UnclosedFrontmatter(f"unclosed frontmatter: {path}")
    return "\n".join(lines[closing_index + 1:])
