# python-tools

Python development tooling: debug type errors in uv-managed projects with pyright, and perform AST-based mass structural edits across codebases.

`python` `type-checking` `pyright` `ast` `refactoring` `uv` 
## Skills

### [python-ast-mass-edit](skills/python-ast-mass-edit/SKILL.md)
Systematic workflow for AST-based mass edits in Python codebases. Use when editing 3+ files with structural changes (decorators, function signatures, imports, class definitions). Includes pre-surveying with grep/pyright, idempotent transformations, and validation protocol. NOT for simple string replacements or <5 instances.

**Scripts:** [`template_transformer.py`](skills/python-ast-mass-edit/scripts/template_transformer.py)
---

### [uv-pyright-debug](skills/uv-pyright-debug/SKILL.md)
Debug type errors in uv-managed Python projects by accessing true pyright diagnostics. Use when IDE shows type errors but standalone pyright reports 0 errors, or when systematic analysis of type errors is needed before mass edits. Critical for projects using pydantic models where Field() defaults may not be properly inferred.

**Scripts:** [`analyze_errors.py`](skills/uv-pyright-debug/scripts/analyze_errors.py) · [`line_index_errors.py`](skills/uv-pyright-debug/scripts/line_index_errors.py)
---

