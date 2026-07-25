import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_add_book_returns_created_book():
    collection = BookCollection()
    created = collection.add_book("Dune", "Frank Herbert", 1965)
    assert created.title == "Dune"
    assert created.author == "Frank Herbert"
    assert created.year == 1965
    assert created.read is False
    assert collection.books[-1] == created

def test_add_book_persists_to_data_file():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    reloaded = BookCollection()
    book = reloaded.find_book_by_title("The Hobbit")
    assert book is not None
    assert book.author == "J.R.R. Tolkien"
    assert book.year == 1937
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_only_marks_matching_book():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)

    result = collection.mark_as_read("Dune")
    assert result is True
    dune = collection.find_book_by_title("Dune")
    hobbit = collection.find_book_by_title("The Hobbit")
    assert dune is not None
    assert hobbit is not None
    assert dune.read is True
    assert hobbit.read is False

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result, message = collection.remove_book("The Hobbit")
    assert result is True
    assert message == "Removed 'The Hobbit' by J.R.R. Tolkien."
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_not_found_returns_feedback():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result, message = collection.remove_book("Nonexistent Book")
    assert result is False
    assert message == "Book 'Nonexistent Book' was not found."

def test_remove_book_case_insensitive_and_trimmed_title():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result, message = collection.remove_book("  dUnE  ")
    assert result is True
    assert message == "Removed 'Dune' by Frank Herbert."
    assert collection.find_book_by_title("Dune") is None

def test_remove_book_returns_suggestion_for_partial_match():
    collection = BookCollection()
    collection.add_book("Dune Messiah", "Frank Herbert", 1969)
    result, message = collection.remove_book("Dune")
    assert result is False
    assert message == "No exact match for 'Dune'. Did you mean: Dune Messiah?"
    assert collection.find_book_by_title("Dune Messiah") is not None

def test_remove_book_from_empty_collection():
    collection = BookCollection()
    result, message = collection.remove_book("Dune")
    assert result is False
    assert message == "Book 'Dune' was not found."

def test_list_by_year():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    collection.add_book("Animal Farm", "George Orwell", 1945)
    collection.add_book("Brave New World", "Aldous Huxley", 1932)
    collection.add_book("Nineteen Eighty-Four", "George Orwell", 1949)
    
    books_1949 = collection.list_by_year(1949)
    assert len(books_1949) == 2
    assert all(b.year == 1949 for b in books_1949)
    
    books_1945 = collection.list_by_year(1945)
    assert len(books_1945) == 1
    assert books_1945[0].title == "Animal Farm"

def test_list_by_year_empty():
    collection = BookCollection()
    collection.add_book("1984", "George Orwell", 1949)
    
    books_2000 = collection.list_by_year(2000)
    assert len(books_2000) == 0
    assert books_2000 == []
