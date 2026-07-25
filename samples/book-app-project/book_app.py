"""CLI entry point for managing the local book collection."""

from datetime import date
import sys
from typing import List

from books import Book, BookCollection


# Global collection instance
collection = BookCollection()


def show_books(books: List[Book]) -> None:
    """Display books in a user-friendly format.

    Args:
        books (List[Book]): Collection of books to print.
    """
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def _prompt_non_empty(prompt: str, field_name: str) -> str:
    """Prompt until the user provides a non-empty value.

    Args:
        prompt (str): Prompt message shown to the user.
        field_name (str): User-facing field label used in validation messages.

    Returns:
        str: A trimmed non-empty value.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{field_name} cannot be empty.")


def _prompt_valid_year(prompt: str) -> int:
    """Prompt until the user enters a valid publication year.

    Args:
        prompt (str): Prompt message shown to the user.

    Returns:
        int: A positive year that is not in the future.
    """
    current_year = date.today().year
    while True:
        year_str = input(prompt).strip()
        if not year_str:
            print("Year cannot be empty.")
            continue
        if not year_str.isdigit():
            print("Year must be a number.")
            continue

        year = int(year_str)
        if year <= 0:
            print("Year must be greater than 0.")
            continue
        if year > current_year:
            print(f"Year cannot be after {current_year}.")
            continue
        return year


def handle_list() -> None:
    """Handle the list command."""
    books = collection.list_books()
    show_books(books)


def handle_list_unread() -> None:
    """Handle the list unread command."""
    books = collection.get_unread_books()
    show_books(books)


def handle_list_between() -> None:
    """Handle the list between command."""
    print("\nFind Books Between Two Years\n")

    while True:
        start_year = _prompt_valid_year("Start year: ")
        end_year = _prompt_valid_year("End year: ")
        if start_year > end_year:
            print("Start year must be less than or equal to end year.")
            continue
        break

    books = collection.list_by_year_range(start_year, end_year)
    show_books(books)


def handle_add() -> None:
    """Handle the add command."""
    print("\nAdd a New Book\n")

    title = _prompt_non_empty("Title: ", "Title")
    author = _prompt_non_empty("Author: ", "Author")
    year = _prompt_valid_year("Year: ")
    collection.add_book(title, author, year)
    print("\nBook added successfully.\n")


def handle_remove() -> None:
    """Handle the remove command."""
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    _, message = collection.remove_book(title)

    print(f"\n{message}\n")


def handle_find() -> None:
    """Handle the find command."""
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def show_help() -> None:
    """Print command help text."""
    print("""
Book Collection Helper

Commands:
  list          - Show all books
  list unread   - Show only unread books
  list between  - Show books published between two years
  add           - Add a new book
  remove        - Remove a book by title
  find          - Find books by author
  help          - Show this help message
""")


def main() -> None:
    """Run the command-line app dispatcher."""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        if len(sys.argv) == 2:
            handle_list()
        elif len(sys.argv) == 3 and sys.argv[2].lower() == "unread":
            handle_list_unread()
        elif len(sys.argv) == 3 and sys.argv[2].lower() == "between":
            handle_list_between()
        else:
            print("Unknown list option. Use 'list', 'list unread', or 'list between'.\n")
            show_help()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
