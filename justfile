# Generate all READMEs from skill/agent/hook metadata
readme:
    uv run --with python-frontmatter --with pydantic --with jinja2 --with rich generate.py

# Check that READMEs are up-to-date (used by pre-commit)
check-readmes: readme
    git diff --exit-code -- '*.md'

# Count tokens in a file using tiktoken (cl100k_base encoding)
tokens *FILES:
    uv run --with tiktoken python3 -c "import tiktoken,sys; enc=tiktoken.get_encoding('cl100k_base'); [print(f'{len(enc.encode(open(f).read())):>6}  {f}') for f in sys.argv[1:]]" {{FILES}}

# Run every hook test suite in the marketplace; list the hooks that have none
hooks-test:
    #!/usr/bin/env python3
    import json, re, subprocess, sys
    from pathlib import Path

    root = Path(".")
    rows = []
    suites = []
    for cfg in sorted(root.glob("*/hooks/hooks.json")):
        plugin = cfg.parent.parent
        tests = [d for d in (plugin / "tests", plugin / "hooks" / "tests") if d.is_dir()]
        corpus = "\n".join(
            f.read_text(errors="ignore") for d in tests for f in d.rglob("*") if f.is_file()
        )
        for event, groups in json.loads(cfg.read_text()).get("hooks", {}).items():
            for group in groups:
                for hook in group.get("hooks", []):
                    command = hook.get("command", "")
                    found = re.search(r"\$\{CLAUDE_PLUGIN_ROOT\}/(\S+)", command)
                    script = found.group(1) if found else command
                    name = Path(script).name
                    rows.append((plugin.name, event, script, name in corpus))
        for d in tests:
            if d not in suites:
                suites.append(d)

    print("hook inventory (plugin | event | script | tests)")
    for plugin, event, script, tested in rows:
        print(f"  {plugin} | {event} | {script} | {'yes' if tested else 'no'}")

    sys.stdout.flush()
    status = 0
    if suites:
        status = subprocess.call(
            ["uv", "run", "--with", "pytest", "pytest", "-q", *map(str, suites)]
        )
    else:
        print("no hook test suites found")

    untested = sorted({(p, s) for p, _, s, t in rows if not t})
    print("hooks with no tests:")
    for plugin, script in untested:
        print(f"  {plugin}/{script}")
    if not untested:
        print("  none")
    sys.exit(status)
