---
name: quick-review
description: Quick 3-point code review checklist for bare except clauses, missing type hints, and unclear variable names
---

# Quick Review

Run this lightweight checklist when the user asks for a fast code review.

## 3-Point Checklist

- [ ] No bare `except:` clauses
- [ ] Functions and public methods have type hints
- [ ] Variable names are clear and descriptive

## Output Format

Report findings as:

```
## Quick Review: [filename]

1. Bare except clauses: [PASS/FAIL] [finding]
2. Type hints: [PASS/FAIL] [finding]
3. Variable names: [PASS/FAIL] [finding]

### Summary
[X] items need attention
```
