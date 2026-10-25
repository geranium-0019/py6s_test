"""Reject saved notebook outputs and syntax errors without executing cells."""

import ast
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    problems = []
    for path in sorted((root / "notebooks").glob("*.ipynb")):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if notebook.get("metadata", {}).get("widgets"):
            problems.append(f"{path.name}: saved widget state")
        for index, cell in enumerate(notebook["cells"], start=1):
            label = f"{path.name}: cell {index}"
            if cell.get("attachments"):
                problems.append(f"{label}: embedded attachments")
            if cell["cell_type"] != "code":
                continue
            if cell.get("outputs") or cell.get("execution_count") is not None:
                problems.append(f"{label}: clear outputs and execution count")
            try:
                ast.parse("".join(cell.get("source", [])))
            except SyntaxError as exc:
                problems.append(f"{label}: {exc.msg}")
    if problems:
        raise SystemExit("\n".join(problems))
    print("Notebook checks passed")


if __name__ == "__main__":
    main()
