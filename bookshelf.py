class Bookshelf:

    def __init__(self, name):
        """Initialize Bookshelf class."""
        self.name = name
        self.books = []

    def __str__(self):
        """Define rules for printing class objects."""
        return "Bookshelf {}, {} books".format(self.name, self.get_number_of_books())

    def add_book(self, book):
        """Add a book to the bookshelf."""
        self.books.append(book)

    def get_number_of_books(self):
        """Return the number of books in the bookshelf."""
        return len(self.books)

    def print_books(self):
        """Print all the books in the bookshelf."""
        for book in self.books:
            print(book)

    def remove_book(self, book_title):
        """Remove a book from the bookshelf."""
        if book_title in self.books:
            self.books.remove(book_title)
