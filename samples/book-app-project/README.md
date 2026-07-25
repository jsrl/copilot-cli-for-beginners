# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A Python app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Search books published between two years using `list between`
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `book_app.py` - Main CLI entry point
* `books.py` - BookCollection class with data logic
* `utils.py` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.py` - Starter pytest tests

---

## Running the App

```bash
python book_app.py list
python book_app.py list unread
python book_app.py list between
python book_app.py add
python book_app.py find
python book_app.py remove
python book_app.py help
```

### Year Range Search (`list between`)

Run:

```bash
python book_app.py list between
```

Then enter:
- `Start year`
- `End year`

Behavior:
- If start year is greater than end year, the app shows an error and asks again.
- If input is empty or not numeric, the app asks again with a validation message.
- If no books match the range, the app prints `No books found.`.

## Running Tests

```bash
python -m pytest tests/
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later
