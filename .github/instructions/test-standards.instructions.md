---
applyTo: "**/tests/test_*.py"
---

# Pytest Test Standards

Apply these rules when creating or editing pytest tests.

## File and Test Naming

- Place tests in `samples/book-app-project/tests/`.
- Use file pattern `test_*.py`.
- Name tests descriptively with `test_<behavior>_<expected_result>`.

## Test Structure

- Keep tests focused: one behavior per test.
- Prefer Arrange-Act-Assert flow with clear separation.
- Use fixtures for repeated setup instead of copy/paste setup blocks.
- Avoid inter-test dependencies; every test must run independently.

## Assertions and Coverage

- Assert outcomes, not implementation details.
- Include happy-path and edge-case coverage:
  - empty input,
  - invalid values,
  - missing data,
  - not-found cases.
- For exceptions, use `pytest.raises` and assert the error message when meaningful.

## Reliability

- Keep tests deterministic (no reliance on timing, random state, or network).
- Avoid side effects across tests; clean up temporary files/resources.
- Prefer temporary directories/files (for example `tmp_path`) for file I/O tests.

## Style in Tests

- Add type hints where they improve readability (especially fixtures/helpers).
- Keep test helpers small and local unless reused broadly.
- Use clear failure messages when custom assertions are necessary.