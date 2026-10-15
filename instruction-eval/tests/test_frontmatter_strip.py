import pytest

from instruction_eval.conditions import UnclosedFrontmatter, strip_frontmatter


def test_frontmatter_block_and_one_following_newline_are_removed():
    assert strip_frontmatter("---\nname: x\n---\nbody\n", "a.md") == "body\n"


def test_file_without_frontmatter_is_returned_unchanged():
    assert strip_frontmatter("body\n---\nmore\n", "a.md") == "body\n---\nmore\n"


def test_only_one_newline_after_closing_fence_is_removed():
    assert strip_frontmatter("---\nk: v\n---\n\nbody", "a.md") == "\nbody"


def test_closing_fence_must_be_the_whole_line():
    text = "---\nk: ---\n--- x\n----\n---\nbody"
    assert strip_frontmatter(text, "a.md") == "body"


def test_closing_fence_at_end_of_file_leaves_empty_text():
    assert strip_frontmatter("---\nk: v\n---", "a.md") == ""


def test_opening_fence_must_be_the_whole_first_line():
    assert strip_frontmatter("--- x\nk\n---\nbody", "a.md") == "--- x\nk\n---\nbody"


def test_unclosed_frontmatter_is_refused_with_the_path():
    with pytest.raises(UnclosedFrontmatter, match="^unclosed frontmatter: dir/a.md$"):
        strip_frontmatter("---\nk: v\nbody\n", "dir/a.md")
