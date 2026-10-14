import re

WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")
SEQUENCE_LENGTH = 3


def words(text: str) -> list[str]:
    """Return the lowercased matches of the word pattern in order."""
    return [match.lower() for match in WORD_PATTERN.findall(text)]


def shared_phrases(text: str, other: str) -> list[str]:
    """Return each three-word sequence both texts hold, in order of first appearance in the first text."""
    ...
