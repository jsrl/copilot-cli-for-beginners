---
name: book-summary
description: Generate a formatted markdown book summary with overview stats, a strict table format, and standardized read-status conventions
argument-hint: path to a book collection file (JSON/CSV) or pasted list of books
---

# Book Summary

Create a clear markdown summary of a book collection.

## What to include

1. Collection title
2. Quick stats:
   - Total books
   - Read books
   - Unread books
   - Read percentage
3. Author breakdown (top authors first)
4. Year breakdown (oldest to newest)
5. A markdown table with these columns:
   - Title
   - Author
   - Year
   - Read Status (`✅ Read` or `❌ Unread`)

## Output format

Use this structure:

```markdown
# Book Collection Summary

## Overview
- Total books: X
- Read: X
- Unread: X
- Completion: X%

## By Author
| Author | Books |
|---|---:|
| Author Name | 3 |

## By Year
| Year | Books |
|---:|---:|
| 1965 | 2 |

## Books
| Title | Author | Year | Read Status |
|---|---|---:|---|
| Dune | Frank Herbert | 1965 | ✅ Read |
```

## Style rules

- Keep headings and table labels in English.
- Sort books by **year** (oldest to newest). If multiple books share the same year, sort those by title (A→Z).
- If data is missing, show `Unknown` instead of leaving blank cells.

## Output conventions

- Use `✅ Read` for books marked as read.
- Use `❌ Unread` for books not yet read.
- Keep the same labels and emoji in every output for consistency.

## Usage examples

```text
Summarize @samples/book-app-project/data.json
```

```text
/book-summary Summarize this collection and highlight unread classics
```
