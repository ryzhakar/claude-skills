import re

WORD_PATTERN = re.compile(r"[A-Za-z0-9']+")
SEQUENCE_LENGTH = 3


def words(text: str) -> list[str]:
    """Return the lowercased matches of the word pattern in order, as the public word list other units count and join."""
    return [match.lower() for match in WORD_PATTERN.findall(text)]


def shared_phrases(text: str, other: str) -> list[str]:
    """Return each three-word sequence both texts hold, in order of first appearance in the first text."""
    other_sequences = set(_word_sequences(words(other)))
    return [
        sequence
        for sequence in dict.fromkeys(_word_sequences(words(text)))
        if sequence in other_sequences
    ]


def _word_sequences(word_list: list[str]) -> list[str]:
    """Return each run of three consecutive words joined by single spaces."""
    return [
        " ".join(word_list[start : start + SEQUENCE_LENGTH])
        for start in range(len(word_list) - SEQUENCE_LENGTH + 1)
    ]
