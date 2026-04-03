#!/usr/bin/env python3
"""
Template for AST-based mass edits in Python codebases.

Usage:
    python3 template_transformer.py <file1.py> <file2.py> ...

Customize the Transformer class below for your specific transformation.
"""
import ast
import sys
from pathlib import Path


class ExampleTransformer(ast.NodeTransformer):
    """
    Customize this transformer for your specific edit.

    Examples:
    - Rename function parameters
    - Change decorator arguments
    - Update import statements
    - Modify function calls
    """

    def __init__(self):
        super().__init__()
        self.changes_made = 0

    def visit_Call(self, node: ast.Call) -> ast.Call:
        """
        Example: Rename keyword argument 'arg' to 'column' in specific function calls.

        Customize this method based on your transformation needs.
        """
        # Guard clause for idempotency - only transform relevant nodes
        if isinstance(node.func, ast.Name) and node.func.id in ("AggregateExpr", "WindowExpr"):
            for keyword in node.keywords:
                if keyword.arg == "arg":
                    print(f"  Renaming 'arg' → 'column' in {node.func.id}()")
                    keyword.arg = "column"
                    self.changes_made += 1

        # Always call generic_visit to continue traversing
        return self.generic_visit(node)

    # Add more visit_* methods as needed:
    # def visit_FunctionDef(self, node): ...
    # def visit_ClassDef(self, node): ...
    # def visit_Import(self, node): ...


def transform_file(file_path: Path) -> bool:
    """Transform a single Python file using AST."""
    try:
        print(f"\n📝 Processing: {file_path}")

        # Read original file
        source = file_path.read_text()

        # Parse to AST
        tree = ast.parse(source)

        # Apply transformation
        transformer = ExampleTransformer()
        new_tree = transformer.visit(tree)

        # Generate new source
        new_source = ast.unparse(new_tree)

        # Write back
        file_path.write_text(new_source)

        if transformer.changes_made > 0:
            print(f"  ✅ Made {transformer.changes_made} changes")
        else:
            print(f"  ℹ️  No changes needed")

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 template_transformer.py <file1.py> <file2.py> ...")
        print("\nExample:")
        print("  python3 template_transformer.py src/**/*.py")
        sys.exit(1)

    files = [Path(f) for f in sys.argv[1:]]
    total_changes = 0

    print(f"🚀 Starting AST transformation on {len(files)} files")
    print("=" * 60)

    for file_path in files:
        if transform_file(file_path):
            total_changes += 1

    print("\n" + "=" * 60)
    print(f"✅ Transformation complete: {total_changes} files modified")
    print("\nNext steps:")
    print("  1. Run: ruff format .")
    print("  2. Review: git diff")
    print("  3. Test: run your test suite")
    print("  4. Clear caches: rm -rf **/__pycache__")


if __name__ == "__main__":
    main()
