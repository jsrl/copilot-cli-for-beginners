def print_menu():
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


def get_book_details():
    """Collect and validate book information from user input.
    
    Prompts the user to enter book title, author, and publication year.
    Enforces that title and author are non-empty strings. The year is converted
    to an integer; if the input is invalid or empty, it defaults to 0.
    
    Returns:
        tuple: A tuple containing (title, author, year)
            - title (str): The book title (non-empty)
            - author (str): The book author (non-empty)
            - year (int): The publication year (0 if invalid or not provided)
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

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
