import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    @staticmethod
    def _normalize_text(value: str) -> str:
        return value.strip().casefold()

    def find_book_by_title(self, title: str) -> Optional[Book]:
        normalized_title = self._normalize_text(title)
        for book in self.books:
            if self._normalize_text(book.title) == normalized_title:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if not book:
            return False

        if not book.read:
            book.read = True
            self.save_books()
        return True

    def remove_book(self, title: str) -> Tuple[bool, str]:
        """Remove a book by title and return status feedback."""
        normalized_title = self._normalize_text(title)
        if not normalized_title:
            return False, "Please provide a non-empty book title."

        book = self.find_book_by_title(normalized_title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True, f"Removed '{book.title}' by {book.author}."

        close_matches = [
            b.title
            for b in self.books
            if normalized_title in self._normalize_text(b.title)
        ]
        if close_matches:
            suggestions = ", ".join(close_matches[:3])
            return (
                False,
                f"No exact match for '{title.strip()}'. Did you mean: {suggestions}?",
            )

        return False, f"Book '{title.strip()}' was not found."

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]

    def list_by_year(self, year: int) -> List[Book]:
        """Find all books published in a given year."""
        return [b for b in self.books if b.year == year]
