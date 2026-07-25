---
applyTo: "**/*.py"
---

# Python Style and Typing Conventions

Use these rules whenever editing Python code in this repository.

## PEP 8

- Follow PEP 8 naming:
  - `snake_case` for variables, functions, and module names.
  - `PascalCase` for classes.
  - `UPPER_SNAKE_CASE` for constants.
- Keep imports grouped and ordered:
  1. Standard library
  2. Third-party packages
  3. Local imports
- Prefer short, readable functions with one clear responsibility.
- Use f-strings for string interpolation.
- Avoid unused variables, dead code, and commented-out code blocks.

## Type Hints

- Add type hints to every function and method signature.
- Always include explicit return types (use `-> None` when appropriate).
- Use `Optional[T]` only when `None` is truly valid.
- Use concrete generics from `typing` (for example `List[Book]`, `Dict[str, int]`, `Tuple[bool, str]`).
- Keep annotations accurate during refactors; do not leave stale types.
- Do not use `Any` unless unavoidable and justified by code context.

## Docstrings

- Public modules, classes, and functions should include docstrings.
- Use Google-style docstrings for public APIs.
- Document:
  - parameter types and meaning,
  - return values,
  - raised exceptions for I/O or validation paths.

## Error Handling

- Catch specific exceptions; never use bare `except:`.
- Validate input at function boundaries and fail with clear messages.
- Do not silently swallow failures in file or data operations.