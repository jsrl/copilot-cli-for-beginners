---
applyTo: "**/*.json"
---

# JSON Data Quality Standards

Use these rules when editing or generating JSON data files in this repository.

## General JSON Rules

- Output must be valid JSON (double quotes, no trailing commas, UTF-8 text).
- Keep arrays and objects consistently formatted and readable.
- Preserve existing schema unless the task explicitly requires schema changes.

## Book Entry Validation (`samples/book-app-project/data.json`)

Each book item must include all required fields:

- `title` (string, non-empty)
- `author` (string, non-empty)
- `year` (integer, positive, not in the future)
- `read` (boolean)

## Data Integrity

- Reject placeholder values for required fields (for example empty author or year `0`).
- Avoid duplicate entries with the same normalized title + author + year.
- Keep value types stable across all entries (no mixed types for the same field).

## Change Safety

- When modifying existing entries, update only intended fields.
- Do not remove required keys from existing records.
- Keep records semantically consistent with application behavior.