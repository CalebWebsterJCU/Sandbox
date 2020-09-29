class Bookshelf:

    def __init__(self, name):
        self.name = name
        self.books = []

    def __str__(self):
        return "Bookshelf {}, {} books".format(self.name, self.get_number_of_books())

    def add_book(self, book):
        self.books.append(book)

    def get_number_of_books(self):
        return len(self.books)

    def print_books(self):
        for book in self.books:
            print(book)

    def remove_book(self, book_title):
        if book_title in self.books:
            self.books.remove(book_title)
