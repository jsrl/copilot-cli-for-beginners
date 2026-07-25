"""Utility functions for Book Collection CLI input and output."""

from datetime import date
from typing import List, Tuple

from books import Book


def print_menu() -> None:
    """Print the main CLI menu."""
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    while True:
        choice = input("Choose an option (1-5): ").strip()
        
        if not choice:
            print("Error: Please enter a choice. Cannot be empty.")
            continue
        
        if not choice.isdigit():
            print("Error: Please enter a number between 1 and 5.")
            continue
        
        if choice not in ("1", "2", "3", "4", "5"):
            print("Error: Please enter a number between 1 and 5.")
            continue
        
        return choice


def get_book_details() -> Tuple[str, str, int]:
    """Collect and validate book information from user input.

    Prompts the user to enter book title, author, and publication year.
    Enforces that title and author are non-empty strings. The year must be a
    positive integer that is not in the future.

    Returns:
        Tuple[str, str, int]: A tuple containing (title, author, year)
            - title (str): The book title (non-empty)
            - author (str): The book author (non-empty)
            - year (int): The publication year (valid positive year)
    """
    title = ""
    while not title:
        title = input("Enter book title: ").strip()
        if not title:
            print("Error: Book title cannot be empty.")

    author = ""
    while not author:
        author = input("Enter author: ").strip()
        if not author:
            print("Error: Author cannot be empty.")

    current_year = date.today().year
    while True:
        year_input = input("Enter publication year: ").strip()
        if not year_input:
            print("Error: Publication year cannot be empty.")
            continue
        if not year_input.isdigit():
            print("Error: Publication year must be a valid number.")
            continue

        year = int(year_input)
        if year <= 0:
            print("Error: Publication year must be greater than 0.")
            continue
        if year > current_year:
            print(f"Error: Publication year cannot be after {current_year}.")
            continue
        break

    return title, author, year


def print_books(books: List[Book]) -> None:
    """Print books in a user-friendly numbered list."""
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
