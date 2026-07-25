"""Tests for the book app CLI entry point."""

from typing import Iterator

import pytest

import book_app
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch) -> Iterator[None]:
    """Use a temporary data file and collection for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))
    monkeypatch.setattr(book_app, "collection", BookCollection())
    yield


def test_handle_list_unread_shows_only_unread_books(capsys) -> None:
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)
    book_app.collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    book_app.collection.mark_as_read("Dune")

    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "The Hobbit" in output and "Dune" not in output


def test_handle_list_unread_shows_no_books_found_when_collection_is_empty(capsys) -> None:
    book_app.handle_list_unread()

    output = capsys.readouterr().out
    assert "No books found." in output


def test_main_dispatches_list_unread_command(monkeypatch) -> None:
    called = {"list": 0, "list_unread": 0}

    def fake_list() -> None:
        called["list"] += 1

    def fake_list_unread() -> None:
        called["list_unread"] += 1

    monkeypatch.setattr(book_app.sys, "argv", ["book_app.py", "list", "unread"])
    monkeypatch.setattr(book_app, "handle_list", fake_list)
    monkeypatch.setattr(book_app, "handle_list_unread", fake_list_unread)

    book_app.main()
    assert called == {"list": 0, "list_unread": 1}


def test_main_dispatches_list_unread_command_case_insensitively(monkeypatch) -> None:
    called = {"list_unread": 0}

    def fake_list_unread() -> None:
        called["list_unread"] += 1

    monkeypatch.setattr(book_app.sys, "argv", ["book_app.py", "list", "UnReAd"])
    monkeypatch.setattr(book_app, "handle_list_unread", fake_list_unread)

    book_app.main()
    assert called["list_unread"] == 1


def test_main_dispatches_list_between_command(monkeypatch) -> None:
    called = {"list": 0, "list_between": 0}

    def fake_list() -> None:
        called["list"] += 1

    def fake_list_between() -> None:
        called["list_between"] += 1

    monkeypatch.setattr(book_app.sys, "argv", ["book_app.py", "list", "between"])
    monkeypatch.setattr(book_app, "handle_list", fake_list)
    monkeypatch.setattr(book_app, "handle_list_between", fake_list_between)

    book_app.main()
    assert called == {"list": 0, "list_between": 1}


def test_main_dispatches_list_between_command_case_insensitively(monkeypatch) -> None:
    called = {"list_between": 0}

    def fake_list_between() -> None:
        called["list_between"] += 1

    monkeypatch.setattr(book_app.sys, "argv", ["book_app.py", "list", "BeTwEeN"])
    monkeypatch.setattr(book_app, "handle_list_between", fake_list_between)

    book_app.main()
    assert called["list_between"] == 1


def test_handle_list_between_shows_books_within_range(capsys, monkeypatch) -> None:
    book_app.collection.add_book("Brave New World", "Aldous Huxley", 1932)
    book_app.collection.add_book("1984", "George Orwell", 1949)
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)

    entered_values = iter(["1940", "1950"])
    monkeypatch.setattr("builtins.input", lambda _: next(entered_values))

    book_app.handle_list_between()

    output = capsys.readouterr().out
    assert "1984" in output
    assert "Brave New World" not in output
    assert "Dune" not in output


def test_handle_list_between_shows_no_books_found_for_empty_results(capsys, monkeypatch) -> None:
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)

    entered_values = iter(["1800", "1801"])
    monkeypatch.setattr("builtins.input", lambda _: next(entered_values))

    book_app.handle_list_between()

    output = capsys.readouterr().out
    assert "No books found." in output


def test_handle_list_between_retries_when_range_is_reversed(capsys, monkeypatch) -> None:
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)

    entered_values = iter(["2000", "1990", "1960", "1970"])
    monkeypatch.setattr("builtins.input", lambda _: next(entered_values))

    book_app.handle_list_between()

    output = capsys.readouterr().out
    assert "Start year must be less than or equal to end year." in output
    assert "Dune" in output


def test_handle_list_between_retries_when_year_input_is_invalid(capsys, monkeypatch) -> None:
    book_app.collection.add_book("Dune", "Frank Herbert", 1965)

    entered_values = iter(["", "nineteen sixty", "1960", "", "1970"])
    monkeypatch.setattr("builtins.input", lambda _: next(entered_values))

    book_app.handle_list_between()

    output = capsys.readouterr().out
    assert "Year cannot be empty." in output
    assert "Year must be a number." in output
    assert "Dune" in output


def test_main_list_with_unknown_option_shows_error(capsys, monkeypatch) -> None:
    monkeypatch.setattr(book_app.sys, "argv", ["book_app.py", "list", "other"])

    book_app.main()

    output = capsys.readouterr().out
    assert "Unknown list option. Use 'list', 'list unread', or 'list between'." in output


def test_show_help_includes_list_unread_command(capsys) -> None:
    book_app.show_help()

    output = capsys.readouterr().out
    assert "list unread   - Show only unread books" in output


def test_show_help_includes_list_between_command(capsys) -> None:
    book_app.show_help()

    output = capsys.readouterr().out
    assert "list between  - Show books published between two years" in output
