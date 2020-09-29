class Book:
    """Represents a book object with a title, author, genre, and page count."""

    def __init__(self, title, author, genre, page_count):
        """Initialize Book class."""
        self.title = title
        self.author = author
        self.genre = genre
        self.page_count = page_count
        self.is_completed = False

    def __str__(self):
        """Define rules for printing class objects."""
        return "{} is a {} book by {} with {} pages".format(self.title, self.author, self.genre, self.page_count)

    def mark_as_completed(self):
        """Mark the book as completed."""
        self.is_completed = True

    def is_complete(self):
        """Return True or False depending on whether or not the book is complete."""
        return self.is_completed


if __name__ == '__main__':
    book1 = Book("100 Ways to Kill a Cane Toad", "Caleb Webster", "Science", 100)
    print(book1)
    print(book1.is_complete())
    book1.mark_as_completed()
    print(book1)
    print(book1.is_complete())
