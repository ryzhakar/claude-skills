# Generate all READMEs from skill/agent/hook metadata
readme:
    uv run --with python-frontmatter --with pydantic --with jinja2 --with rich generate.py

# Check that READMEs are up-to-date (used by pre-commit)
check-readmes: readme
    git diff --exit-code -- '*.md'
