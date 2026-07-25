"""Store and manage a small book collection in a local JSON file.

Example:
    >>> library = BookCollection()
    >>> _ = library.add_book("Dune", "Frank Herbert", 1965)
    >>> library.mark_as_read("dune")
    True
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple

DATA_FILE = "data.json"


@dataclass
class Book:
    """Represent one book entry in the collection.

    Attributes:
        title (str): Book title shown to the user.
        author (str): Book author name.
        year (int): Publication year.
        read (bool): Whether the user has marked the book as read.
    """

    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    """Manage books in memory and persist them to ``data.json``.

    Example:
        >>> collection = BookCollection()
        >>> book = collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        >>> book.read
        False

    Gotchas:
        - ``DATA_FILE`` is a relative path, so the file is created in the
          current working directory.
        - This class does not implement file locking for concurrent writes.
    """

    def __init__(self) -> None:
        """Create an empty collection and load existing books from disk.

        Example:
            >>> collection = BookCollection()
            >>> isinstance(collection.books, list)
            True
        """
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from ``DATA_FILE`` into memory.

        Returns:
            None: Updates ``self.books`` in place.

        Example:
            >>> collection = BookCollection()
            >>> collection.load_books()
            >>> isinstance(collection.list_books(), list)
            True
        """
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the in-memory collection to ``DATA_FILE``.

        Returns:
            None: Writes the current collection to disk.

        Raises:
            OSError: If the file cannot be opened or written.

        Example:
            >>> collection = BookCollection()
            >>> collection.save_books()
        """
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new unread book and persist the updated collection.

        Args:
            title (str): Book title.
            author (str): Book author.
            year (int): Publication year.

        Returns:
            Book: The newly created ``Book`` object.

        Raises:
            OSError: If persisting the updated collection fails.

        Example:
            >>> collection = BookCollection()
            >>> book = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> book.title
            'Dune'
        """
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        """Return all books currently stored in memory.

        Returns:
            List[Book]: A list of ``Book`` objects.

        Gotchas:
            The returned list is the internal list. Mutating it directly
            bypasses persistence until ``save_books()`` is called.

        Example:
            >>> collection = BookCollection()
            >>> books = collection.list_books()
            >>> isinstance(books, list)
            True
        """
        return self.books

    @staticmethod
    def _normalize_text(value: str) -> str:
        """Normalize user input for case-insensitive text matching.

        Args:
            value (str): Raw text value to normalize.

        Returns:
            str: Normalized text with surrounding whitespace removed and
                case-folded for robust matching.
        """
        return value.strip().casefold()

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by title using trimmed, case-insensitive matching.

        Args:
            title (str): Title text to search for.

        Returns:
            Optional[Book]: The matching ``Book`` if found, otherwise ``None``.

        Example:
            >>> collection = BookCollection()
            >>> _ = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.find_book_by_title("dune").author
            'Frank Herbert'
        """
        normalized_title = self._normalize_text(title)
        for book in self.books:
            if self._normalize_text(book.title) == normalized_title:
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        """Mark a book as read by title.

        Args:
            title (str): Title of the book to mark as read.

        Returns:
            bool: ``True`` if the book exists (already read or newly marked),
            ``False`` if no matching book is found.

        Raises:
            OSError: If the updated read status cannot be persisted.

        Example:
            >>> collection = BookCollection()
            >>> _ = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.mark_as_read("dune")
            True
        """
        book = self.find_book_by_title(title)
        if not book:
            return False

        if not book.read:
            book.read = True
            self.save_books()
        return True

    def remove_book(self, title: str) -> Tuple[bool, str]:
        """Remove a book by title and return status feedback.

        Args:
            title (str): Title to remove.

        Returns:
            Tuple[bool, str]: A tuple ``(success, message)`` where:
            - ``success`` is ``True`` when a book was removed.
            - ``message`` explains the result or offers close matches.

        Raises:
            OSError: If removing a matched book cannot be persisted.

        Example:
            >>> collection = BookCollection()
            >>> _ = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> collection.remove_book("dune")[0]
            True
        """
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
        """Find all books by a given author.

        Args:
            author (str): Author name to match.

        Returns:
            List[Book]: All books whose author matches case-insensitively.

        Example:
            >>> collection = BookCollection()
            >>> _ = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> len(collection.find_by_author("frank herbert"))
            1
        """
        return [b for b in self.books if b.author.lower() == author.lower()]

    def list_by_year(self, year: int) -> List[Book]:
        """Find all books published in a given year.

        Args:
            year (int): Publication year to filter by.

        Returns:
            List[Book]: All books with the exact matching publication year.

        Example:
            >>> collection = BookCollection()
            >>> _ = collection.add_book("Dune", "Frank Herbert", 1965)
            >>> len(collection.list_by_year(1965))
            1
        """
        return [b for b in self.books if b.year == year]
