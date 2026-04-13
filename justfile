# Generate all READMEs from skill/agent/hook metadata
readme:
    uv run --with python-frontmatter --with pydantic --with jinja2 --with rich generate.py

# Check that READMEs are up-to-date (used by pre-commit)
check-readmes: readme
    git diff --exit-code -- '*.md'

# Count tokens in a file using tiktoken (cl100k_base encoding)
tokens *FILES:
    uv run --with tiktoken python3 -c "import tiktoken,sys; enc=tiktoken.get_encoding('cl100k_base'); [print(f'{len(enc.encode(open(f).read())):>6}  {f}') for f in sys.argv[1:]]" {{FILES}}
